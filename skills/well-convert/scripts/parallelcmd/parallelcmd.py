#!/usr/bin/env python3

import os
import time
import socket
import queue
import threading
from threading import Thread

import logging
import sys
import argparse

import subprocess
import shlex
import signal
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import itertools
from string import Formatter
import sqlite3
import random
import datetime

mq = queue.Queue()
slot = dict()
active_ps = dict()
active = mp.Value("i", 0)
dbname = "pardb" if os.getenv("PARDB") is None else os.getenv("PARDB")
dbfile = dbname + ".sqlite"
db_retries = 10
db_retry_delay = 0.2


def log(*args, sep=" "):
    logging.debug(sep.join(map(str, args)))


def info(*args, sep=" "):
    logging.info(sep.join(map(str, args)))


def is_sqlite_lock_error(exc: Exception) -> bool:
    return isinstance(exc, sqlite3.OperationalError) and any(
        token in str(exc).lower() for token in ("locked", "busy")
    )


def execute_sql_with_retry(con, sql, params=None, retries=None, retry_delay=None):
    max_retries = db_retries if retries is None else retries
    delay = db_retry_delay if retry_delay is None else retry_delay
    last_exc = None
    for attempt in range(max_retries):
        try:
            cur = con.cursor()
            if params is None:
                cur.execute(sql)
            else:
                cur.execute(sql, params)
            return cur
        except Exception as e:
            last_exc = e
            if is_sqlite_lock_error(e) and attempt < max_retries - 1:
                log(
                    f"SQLite locked/busy. Retry {attempt + 1}/{max_retries} in {delay:.2f}s:",
                    e,
                )
                try:
                    con.rollback()
                except Exception:
                    pass
                time.sleep(delay)
                continue
            raise
    raise last_exc


def hello(counter: mp.Value):
    workerid = threading.get_native_id()
    with counter.get_lock():
        slot[workerid] = counter.value
        counter.value += 1
    affinity = None
    logging.debug(f"Worker: pid={os.getpid()} ID={counter.value}, TID={workerid}")
    return 0


def timedelta_parse(text):
    """
    Convert input string to timedelta.
    format: [[[d-]h:]m:]s
    """
    tokens = text.replace("-", ":").split(":")
    vals = {
        key: float(val)
        for val, key in zip(tokens[::-1], ("seconds", "minutes", "hours", "days"))
    }
    return datetime.timedelta(**vals)


def execute(
    verbose=False,
    dryrun=False,
    randomorder=False,
    prefix=None,
    max_jobs=None,
    check_timeleft=None,
    wait_interval=None,
    id_list=None,
    timeout=None,
):
    ## check in
    hostname = socket.gethostname()
    workerid = threading.get_native_id()
    nomorejob = False
    finished = 0

    while True:
        ## wait a random to avoid contention at once
        time.sleep(random.randint(0, 10))

        if check_timeleft is not None and check_timeleft > 0:
            jobid = os.getenv("SLURM_JOB_ID", None)
            assert jobid is not None, "SLURM_JOB_ID not found in environment variables."
            cmd = f"squeue -h -j {jobid} -o %L"
            proc = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
            timestr = proc.stdout.decode("utf-8").strip()
            try:
                left = timedelta_parse(timestr).total_seconds()
            except Exception as e:
                ## "INVALID" when remaining time is less than a few seconds
                log(f"{slot[workerid]}: Exception parsing time string '{timestr}':", e)
                left = 0.0
            log(
                f"{slot[workerid]}: SLURM job {jobid} remaining time: {left:.2f} seconds"
            )

            if left < check_timeleft:
                log(
                    f"{slot[workerid]}: Remaining time {left:.2f} seconds is less than threshold {check_timeleft}. Stop fetching new jobs."
                )
                break

        with sqlite3.connect(dbfile) as con:
            while True:
                try:
                    con.execute("BEGIN EXCLUSIVE;")
                    cur = con.cursor()
                    id_clause = ""
                    if id_list:
                        ids = ",".join(map(str, id_list))
                        id_clause = f" AND Seq IN ({ids})"
                    if randomorder:
                        sql = f"SELECT Seq, Command FROM parjob WHERE Exitval is NULL{id_clause} ORDER BY RANDOM() LIMIT 1;"
                    else:
                        sql = f"SELECT Seq, Command FROM parjob WHERE Exitval is NULL{id_clause} LIMIT 1;"
                    cur.execute(sql)
                    row = cur.fetchone()
                    if not row:
                        log(f"{slot[workerid]}: No more job")
                        nomorejob = True
                        break

                    (
                        taskid,
                        cmd,
                    ) = row
                    cur.execute(
                        f"UPDATE parjob SET Starttime = unixepoch('now'), Exitval = -1000 WHERE Seq = {taskid};"
                    )
                    log(f"{slot[workerid]}: taskid, cmd:", taskid, cmd)
                    assert cur.rowcount == 1
                    con.commit()
                    break
                except Exception as e:
                    log(f"{slot[workerid]}: Exception:", e)
                    pass

        if nomorejob:
            if wait_interval is not None and wait_interval > 0:
                print(
                    f"{slot[workerid]}: No job available. Waiting {wait_interval}s before retry..."
                )
                time.sleep(wait_interval)
                nomorejob = False
                continue
            break

        bashargs = ["bash", "-c", cmd]
        if prefix is not None:
            bashargs = shlex.split(prefix) + bashargs
        if verbose:
            log("%d: cmd:" % taskid, shlex.join(bashargs))

        if dryrun:
            info("dryrun: %s" % shlex.join(bashargs))
            with sqlite3.connect(dbfile) as con:
                execute_sql_with_retry(
                    con,
                    "UPDATE parjob SET Starttime = NULL, Exitval = NULL WHERE Seq = ?;",
                    (taskid,),
                )
                con.commit()
            finished += 1
            if max_jobs is not None and finished >= max_jobs:
                break
            continue

        if not dryrun:
            starttime = time.time()
            with active.get_lock():
                active.value += 1

            p = subprocess.Popen(
                bashargs,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=False,
                start_new_session=True,
                env=os.environ.copy(),
            )
            with active.get_lock():
                active_ps[workerid] = p

            with sqlite3.connect(dbfile) as con:
                execute_sql_with_retry(
                    con,
                    "UPDATE parjob SET Hostname = ?, PID = ? WHERE Seq = ?;",
                    (hostname, p.pid, taskid),
                )
                con.commit()

            timed_out = False

            def _kill_on_timeout():
                nonlocal timed_out
                timed_out = True
                try:
                    os.killpg(os.getpgid(p.pid), signal.SIGKILL)
                except Exception:
                    pass

            timer = None
            if timeout is not None and timeout > 0:
                timer = threading.Timer(timeout, _kill_on_timeout)
                timer.start()

            try:
                for line in iter(p.stdout.readline, ""):
                    mq.put((workerid, taskid, line))
            except Exception as e:
                log(f"{slot[workerid]}: Exception:", e)

            p.wait()

            if timer is not None:
                timer.cancel()

            ## check out
            mq.put((workerid, taskid, None))
            with active.get_lock():
                active.value -= 1
                del active_ps[workerid]

            runtime = time.time() - starttime
            exitval = -124 if timed_out else p.returncode

            if timed_out:
                info("%d: Timeout after %ss. Killed." % (taskid, timeout))
            elif verbose:
                log("%d: Done: %s" % (taskid, p.returncode))

            with sqlite3.connect(dbfile) as con:
                execute_sql_with_retry(
                    con,
                    f"UPDATE parjob SET Exitval = {exitval}, JobRuntime = {runtime} WHERE Seq = {taskid};",
                )
                con.commit()
            finished += 1

            if max_jobs is not None and finished >= max_jobs:
                break
    return 0


def jobcount():
    def dojob():
        with sqlite3.connect(dbfile) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT count(1), sum(case when Exitval >= 0 then 1 else 0 end) FROM parjob;"
            )
            row = cur.fetchone()
            (
                total,
                done,
            ) = row
        return (total, done)

    for attempt in range(db_retries):
        try:
            return dojob()
        except Exception as e:
            log(f"jobcount Exception (attempt {attempt + 1}/{db_retries}):", e)
            if attempt < db_retries - 1:
                time.sleep(db_retry_delay)
    raise RuntimeError(f"jobcount failed after {db_retries} attempts")


def cmdlist(argv):
    """
    return list of list
    """
    cmds = list()
    _args = list()
    _type = 0  ## 0: regular, 1: file
    for x in argv:
        if x == ":::":
            cmds.append(_args)
            _args = list()
            _type = 0
        elif x == "::::":
            cmds.append(_args)
            _args = list()
            _type = 1
        else:
            if _type == 1:
                f = sys.stdin if x == "-" else open(x, "r")
                try:
                    for line in f:
                        if line.startswith("#") or line.strip() == "":
                            continue
                        _args.append(line.rstrip())
                finally:
                    if f is not sys.stdin:
                        f.close()
            else:
                _args.append(x)

    cmds.append(_args)

    return cmds


def progress(done, total, dashboard=False, progress=False, timeskip=0.0):
    def putline():
        os.system("tput ll")
        print("\r", end="", flush=True)
        print(
            "Processing/Done/Total/Completed(%%)/Time(sec): %d/%d/%d/%.01f%%/%.02fs"
            % (
                active.value,
                done,
                total,
                float(done) / total * 100,
                time.time() - t0,
            ),
            end="",
            flush=True,
        )
        if not dashboard:
            print("")
        os.system("tput el")

    extra = 1 if progress else 0
    t0 = time.time()
    t1 = time.time()
    t2 = time.time()
    while True:
        workerid, taskid, line = mq.get()
        if (workerid is None) or (done == total):
            total, done = jobcount()
            putline()
            break

        if line is not None:
            if time.time() - t2 > timeskip:
                t2 = time.time()
            else:
                continue

            if dashboard:
                os.system("tput ll")
                print("\r", end="", flush=True)
                os.system("tput sc")
                for i in range(slot[workerid] + extra):
                    os.system("tput cuu1")
                print("%d:" % taskid, line.rstrip(), end="", flush=True)
                os.system("tput el")
                os.system("tput rc")
            else:
                print("%d:" % taskid, line, end="", flush=True)

            if progress:
                ## try not too frequent
                if time.time() - t1 > 2:
                    total, done = jobcount()
                    putline()
                    t1 = time.time()
                else:
                    pass


def print_table(cur, rows, row_format):
    colnames = [desc[0] for desc in cur.description]
    bars = ["-" * len(desc[0]) for desc in cur.description]
    print(row_format.format(*colnames))
    print(row_format.format(*bars))
    for row in rows:
        print(
            row_format.format(
                *map(
                    lambda x: str(x) if not isinstance(x, float) else "%.2f" % x,
                    row,
                )
            )
        )


def selectdb(cur, filter=None):
    if filter is None:
        filter = "1=1"

    cur.execute(
        "SELECT Seq, "
        "datetime(Starttime, 'unixepoch', 'localtime') as Starttime, "
        "Hostname, PID, JobRuntime, Exitval, Command "
        "FROM parjob "
        f"WHERE {filter};"
    )
    rows = cur.fetchall()
    row_format = " {:>4} {:<19} {:<22} {:>8} {:>11} {:>7} {:<80}"
    print_table(cur, rows, row_format)
    return rows, row_format


def checkdb(args):
    with sqlite3.connect(dbfile) as con:
        filter = "1=1"
        if args.where is not None:
            filter = f"{args.where}"
        if args.like is not None:
            filter = "Command LIKE '%s'" % args.like.replace("'", "''")
        if args.id:
            if not isinstance(args.id, list):
                args.id = [args.id]
            filter = "Seq IN (%s)" % ",".join(map(str, args.id))

        if args.nonzero:
            nonzero_clause = "Exitval > 0"
            filter = (
                f"({filter}) AND {nonzero_clause}"
                if filter != "1=1"
                else nonzero_clause
            )

        # con.row_factory = sqlite3.Row
        cur = con.cursor()
        # cur.execute("SELECT count(1) as Total, sum(case when Exitval >= 0 then 1 else 0 end) as Finished FROM parjob")
        if args.list:
            selectdb(cur, filter)
        else:
            cur.execute(
                "SELECT count(1) as Total, "
                "sum(case when Exitval IS NULL then 1 else 0 end) as Pending, "
                "sum(case when Exitval == -1000 then 1 else 0 end) as Running, "
                "sum(case when Exitval == 0 then 1 else 0 end) as Success, "
                "sum(case when Exitval > 0 then 1 else 0 end) as Failed, "
                "sum(case when Exitval < 0 and Exitval != -1000 then 1 else 0 end) as Error "
                "FROM parjob;"
            )
            row = cur.fetchone()
            row_format = " {:>5} | {:>7} {:>7} | {:>7} {:>6} {:>5}"
            print_table(cur, [row], row_format)


def resetdb(args):
    with sqlite3.connect(dbfile) as con:
        filter = "Exitval <> 0"
        if args.where is not None:
            filter = f"{args.where}"
        if args.like is not None:
            filter = "Command LIKE '%s'" % args.like.replace("'", "''")
        if args.all:
            filter = "1=1"
        if args.nonzero:
            nonzero_clause = "Exitval > 0"
            filter = (
                f"({filter}) AND {nonzero_clause}"
                if filter != "1=1"
                else nonzero_clause
            )
        if args.id:
            if not isinstance(args.id, list):
                args.id = [args.id]
            filter = "Seq IN (%s)" % ",".join(map(str, args.id))

        cur = con.cursor()
        rows, row_format = selectdb(cur, filter)
        # (count,) = cur.fetchone()
        count = len(rows)
        ans = input("%d number of rows will be reset. Continue? (Y/N): " % count)
        if ans == "Y" or ans == "y":
            cur = execute_sql_with_retry(
                con,
                f"UPDATE parjob SET Starttime = NULL, Hostname = NULL, PID = NULL, JobRuntime = NULL, Exitval = NULL WHERE {filter};",
            )
            info("Reset: %d" % cur.rowcount)
            con.commit()
        else:
            print("Aborted.")


def deletedb(args):
    with sqlite3.connect(dbfile) as con:
        filter = "Exitval <> 0"
        if args.like is not None:
            filter = "Command LIKE '%s'" % args.like.replace("'", "''")
        if args.all:
            filter = "1=1"
        if args.id:
            if not isinstance(args.id, list):
                args.id = [args.id]
            filter = "Seq IN (%s)" % ",".join(map(str, args.id))

        cur = con.cursor()
        rows, row_format = selectdb(cur, filter)
        count = len(rows)
        ans = input("%d number of rows will be deleted. Continue? (Y/N): " % count)
        if ans == "Y" or ans == "y":
            cur = execute_sql_with_retry(con, f"DELETE FROM parjob WHERE {filter};")
            info("Delete: %d" % cur.rowcount)
            con.commit()
        else:
            print("Aborted.")


def updatedb(args):
    with sqlite3.connect(dbfile) as con:
        filter = "1 = 1"
        if args.like is not None:
            filter = "Command LIKE '%s'" % args.like.replace("'", "''")

        if args.id:
            if not isinstance(args.id, list):
                args.id = [args.id]
            filter = "Seq IN (%s)" % ",".join(map(str, args.id))

        cur = con.cursor()
        rows, row_format = selectdb(cur, filter)
        replace_a, replace_b = args.replace.split(",")
        for row in rows:
            cmd = row[-1]
            new_cmd = cmd.replace(replace_a, replace_b)

            print(
                row_format.format(
                    *map(
                        lambda x: str(x) if not isinstance(x, float) else "%.2f" % x,
                        row,
                    )
                ),
                "->",
                new_cmd,
            )

        count = len(rows)
        ans = input("%d number of rows will be updated. Continue? (Y/N): " % count)
        if ans == "Y" or ans == "y":
            affected_rowcount = 0
            for row in rows:
                seq = row[0]
                cmd = row[-1]
                new_cmd = cmd.replace(replace_a, replace_b)

                cur = execute_sql_with_retry(
                    con, "UPDATE parjob SET Command = ? WHERE Seq = ?;", (new_cmd, seq)
                )
                affected_rowcount += cur.rowcount

            info("Updated: %d" % affected_rowcount)
            con.commit()
        else:
            print("Aborted.")


def initdb(args):
    if args.append and args.force:
        raise SystemExit("--append and --force cannot be used together.")

    cmds = args.cmds
    args_list = cmds[1:]
    cmd = " ".join(args.cmd)
    ## check if cmd has valid formatter
    valid = any(a is not None or b is not None for _, a, b, _ in Formatter().parse(cmd))
    if not valid:
        cmd += " {}" * len(args_list)

    task_list = list()
    for i, argpair in enumerate(itertools.product(*args_list)):
        fullcmd = cmd.format(*argpair)
        task_list.append((i, fullcmd))

    with sqlite3.connect(dbfile) as con:
        cur = con.cursor()
        # Enable WAL mode
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'parjob';"
        )
        table_exists = cur.fetchone() is not None

        if table_exists and args.force:
            cur.execute("DROP TABLE parjob;")
            table_exists = False

        if table_exists and not args.append:
            raise SystemExit(
                "parjob table already exists in %s. Use --append to add tasks to the existing queue."
                % (dbfile,)
            )

        if not table_exists:
            sql = (
                "CREATE TABLE IF NOT EXISTS parjob ("
                "  Seq INTEGER PRIMARY KEY AUTOINCREMENT,"
                "  Starttime FLOAT(44),"
                "  Hostname TEXT,"
                "  PID INT,"
                "  JobRuntime FLOAT(44),"
                "  Exitval BIGINT,"
                "  Command TEXT);"
            )
            cur.execute(sql)
            info("%s created" % (dbfile))

        inserted_rows = 0
        for i, cmd in task_list:
            cur.execute("SELECT 1 FROM parjob WHERE Command = ?;", (cmd,))
            exists = cur.fetchone()
            if args.check_dup and exists:
                info("Already exists. Skip: %s" % cmd)
            else:
                cur = execute_sql_with_retry(
                    con, "INSERT INTO parjob (Command) VALUES (?);", (cmd,)
                )
                inserted_rows += cur.rowcount
        con.commit()
        info("%d tasks added." % (inserted_rows))
        # res = cur.execute("select count(*) from parjob;")
        # (ntotal,) = res.fetchone()
        # print("%d Total added." % (ntotal))


def exec(args):
    total, done = jobcount()

    if args.dashboard:
        ## print empty lines to leave space for each worker
        for i in range(args.nworkers + 1):
            print("")

    p = threading.Thread(
        target=progress,
        args=(
            done,
            total,
            args.dashboard,
            args.progress,
            args.timeskip,
        ),
    )
    p.start()

    counter = mp.Value("i", 0)
    # pool = ProcessPoolExecutor(max_workers=args.nworkers, initializer=hello, initargs=(counter,))
    pool = ThreadPoolExecutor(
        max_workers=args.nworkers, initializer=hello, initargs=(counter,)
    )

    with pool as executor:
        future_list = list()
        for index in range(args.nworkers):
            future = executor.submit(
                execute,
                verbose=args.verbose,
                dryrun=args.dryrun,
                randomorder=args.randomorder,
                prefix=args.prefix,
                max_jobs=args.max_jobs,
                check_timeleft=args.check_timeleft,
                wait_interval=args.wait,
                id_list=args.id if args.id is not None else None,
                timeout=args.timeout,
            )
            future_list.append(future)

        for future in future_list:
            future.result()

        mq.put((None, None, None))
        p.join()


def run(args):
    initdb(args)
    exec(args)


def add_default_run_subcommand(argv, subcommand_names):
    if any(x in ("-h", "--help") for x in argv):
        return argv

    if any(x in subcommand_names for x in argv):
        return argv

    idx = 0
    while idx < len(argv):
        token = argv[idx]
        if token in ("--db", "--log_level"):
            idx += 2
            continue
        if token.startswith("--db=") or token.startswith("--log_level="):
            idx += 1
            continue
        break

    out = list(argv)
    out.insert(idx, "run")
    return out


if __name__ == "__main__":

    def usage():
        # print(
        #     "USAGE: %s <OPTIONS> [ ::: <ARGUMENTS> ]* [ :::: ARGFILE ]*" % (sys.argv[0])
        # )
        parser_main.print_help()
        # parser_args.print_help()
        sys.exit()

    parser_main = argparse.ArgumentParser(prog="OPTIONS")
    parser_main.add_argument("--db", metavar="NAME", help="DB name")
    parser_main.add_argument(
        "--db_retries",
        type=int,
        default=10,
        metavar="N",
        help="Max retries when SQLite database is locked",
    )
    parser_main.add_argument(
        "--log_level",
        choices=["debug", "info"],
        default="info",
        help="Set log level (debug or info)",
    )

    subparsers = parser_main.add_subparsers(
        title="subcommands", description="valid subcommands", dest="command"
    )

    ## subcommand: check
    parser = subparsers.add_parser("check")
    parser.add_argument("-l", "--list", action="store_true", help="list")
    parser.add_argument(
        "--nonzero", action="store_true", help="show only nonzero return tasks"
    )
    parser.add_argument("--where", metavar="EXPR", help="where statement")
    parser.add_argument("--like", metavar="PATTERN", help="like statement")
    parser.add_argument("--id", type=int, metavar="ID", help="select by id", nargs="+")
    parser.set_defaults(func=checkdb)

    ## subcommand: reset
    parser = subparsers.add_parser("reset")
    parser.add_argument("--where", metavar="EXPR", help="where statement")
    parser.add_argument("--like", metavar="PATTERN", help="like statement")
    parser.add_argument("-a", "--all", action="store_true", help="reset all")
    parser.add_argument(
        "--nonzero", action="store_true", help="reset only nonzero return tasks"
    )
    parser.add_argument("--id", type=int, metavar="ID", help="reset by id", nargs="+")
    parser.set_defaults(func=resetdb)

    ## subcommand: delete
    parser = subparsers.add_parser("delete")
    parser.add_argument("--like", metavar="PATTERN", help="like statement")
    parser.add_argument("-a", "--all", action="store_true", help="delete all")
    parser.add_argument("--id", type=int, metavar="ID", help="remove by id", nargs="+")
    parser.set_defaults(func=deletedb)

    ## subcommand: init
    parser = subparsers.add_parser("init")
    parser.set_defaults(func=initdb)
    parser.add_argument("cmd", help="command to execute", nargs=argparse.REMAINDER)
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument("-a", "--append", action="store_true", help="append")
    parser.add_argument(
        "-f", "--force", action="store_true", help="overwrite existing table"
    )
    parser.add_argument(
        "--check_dup", action="store_true", help="allow duplicate commands"
    )

    ## subcommand: exec
    parser = subparsers.add_parser("exec")
    parser.set_defaults(func=exec)
    parser.add_argument(
        "--id", type=int, metavar="ID", help="run only these job IDs", nargs="+"
    )
    parser.add_argument(
        "-j", "--nworkers", type=int, metavar="N", help="Number of workers", default=4
    )
    parser.add_argument("--progress", action="store_true", help="print progress")
    parser.add_argument("--dashboard", action="store_true", help="print only last line")
    parser.add_argument("--dryrun", action="store_true", help="dryrun")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument(
        "--timeskip", type=float, metavar="SECONDS", help="timeskip", default=0.0
    )
    parser.add_argument("--randomorder", action="store_true", help="randomorder")
    parser.add_argument("--prefix", metavar="CMD", help="command prefix")
    parser.add_argument(
        "--max_jobs",
        type=int,
        metavar="N",
        help="maximum number of jobs per process to run",
    )
    parser.add_argument(
        "--check_timeleft",
        type=float,
        metavar="SECONDS",
        help="check timeleft (seconds)",
    )
    parser.add_argument(
        "--wait",
        type=float,
        default=None,
        metavar="SECONDS",
        help="wait SECONDS and retry when no job is available (default: exit immediately)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        metavar="SECONDS",
        help="kill task and move to next if it runs longer than SECONDS (exit code -124)",
    )

    ## subcommand: run (init + exec)
    parser = subparsers.add_parser("run")
    parser.set_defaults(func=run)
    parser.add_argument("cmd", help="command to execute", nargs=argparse.REMAINDER)
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument(
        "--id", type=int, metavar="ID", help="run only these job IDs", nargs="+"
    )
    parser.add_argument("-a", "--append", action="store_true", help="append")
    parser.add_argument(
        "-f", "--force", action="store_true", help="overwrite existing table"
    )
    parser.add_argument(
        "--check_dup", action="store_true", help="allow duplicate commands"
    )
    parser.add_argument(
        "-j", "--nworkers", type=int, metavar="N", help="Number of workers", default=4
    )
    parser.add_argument("--progress", action="store_true", help="print progress")
    parser.add_argument("--dashboard", action="store_true", help="print only last line")
    parser.add_argument("--dryrun", action="store_true", help="dryrun")
    parser.add_argument(
        "--timeskip", type=float, metavar="SECONDS", help="timeskip", default=0.0
    )
    parser.add_argument("--randomorder", action="store_true", help="randomorder")
    parser.add_argument("--prefix", metavar="CMD", help="command prefix")
    parser.add_argument(
        "--max_jobs",
        type=int,
        metavar="N",
        help="maximum number of jobs per process to run",
    )
    parser.add_argument(
        "--check_timeleft",
        type=float,
        metavar="SECONDS",
        help="check timeleft (seconds)",
    )
    parser.add_argument(
        "--wait",
        type=float,
        default=None,
        metavar="SECONDS",
        help="wait SECONDS and retry when no job is available (default: exit immediately)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        metavar="SECONDS",
        help="kill task and move to next if it runs longer than SECONDS (exit code -124)",
    )

    ## subcommand: update
    parser = subparsers.add_parser("update")
    parser.add_argument(
        "--replace",
        metavar="OLD,NEW",
        help="replace statement in the form of 'old,new'",
        required=True,
    )
    parser.add_argument("--like", metavar="PATTERN", help="like statement")
    parser.add_argument("--id", type=int, metavar="ID", help="reset by id", nargs="+")
    parser.set_defaults(func=updatedb)

    raw_argv = add_default_run_subcommand(sys.argv[1:], set(subparsers.choices.keys()))
    cmds = cmdlist(raw_argv)
    args, _unknown = parser_main.parse_known_args(cmds[0])
    if len(_unknown) > 0:
        idx_list = [i for i, x in enumerate(cmds[0]) if x in subparsers.choices.keys()]
        idx = min(idx_list) if len(idx_list) > 0 else 0

        ## re-arrange and try again
        for x in reversed(_unknown):
            cmds[0].remove(x)
            cmds[0].insert(idx, x)

        args, _unknown = parser_main.parse_known_args(cmds[0])
        if len(_unknown) > 0:
            print("Unknown options:", _unknown)
            usage()

    level = logging.DEBUG if args.log_level == "debug" else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    log("Python version:", ".".join(map(str, sys.version_info[:3])))
    log("Python info:", sys.version)

    if (
        args.command in ("init", "run", None)
        and len(cmds) == 1
        and not sys.stdin.isatty()
    ):
        stdin_args = [
            line.rstrip()
            for line in sys.stdin
            if not line.startswith("#") and line.strip() != ""
        ]
        if stdin_args:
            cmds.append(stdin_args)

    args.cmds = cmds

    if args.db is not None:
        dbname = args.db
        dbfile = dbname + ".sqlite"

    db_retries = max(1, args.db_retries)

    if args.command is None:
        usage()
    args.func(args)
    sys.exit(0)
