---
description: Convert a simulation dataset to the Well HDF5 format — preprocess, inspect, plan, generate scripts, run and monitor
---

This skill guides end-to-end conversion of a scientific simulation dataset into [the Well HDF5 format](https://github.com/PolymathicAI/the_well), a standardized layout for PDE simulation data used by the Polymathic AI project. It covers the full pipeline: extracting archives, inspecting source fields, mapping them to the Well schema, planning the conversion, generating ready-to-run HPC scripts, and monitoring the job through to validation.

## Setup

**Arguments:** collect source path and output destination (`<output_root>`) from $ARGUMENTS; ask for any not provided.
Default output filename: `<output_root>/converted/<source_basename>_well.h5`.

**Input policy:** source location is read-only — never write, rename, move, or delete files there.

**Output layout** — all artifacts go under `<output_root>`:

```
<output_root>/
├── scripts/        ← generated conversion, queue, runner, and validation scripts
├── converted/      ← Well HDF5 files and chunked outputs
├── extracted/      ← archives extracted from source (source unchanged)
├── checkpoints/    ← .progress files and resumable state
├── logs/           ← conversion logs, run summaries, error logs
├── validation/     ← validation reports and continuity checks
└── reports/        ← mapping tables, planning summaries, conversion notes
```

**Tools:** `scripts/parallelcmd/parallelcmd.py` (parallel job manager); see `scripts/parallelcmd/README.md`. Use it for all CLI examples. Install and verify (`parallelcmd.py -h` must succeed) before proceeding.

**Well spec:** fetch before starting — https://raw.githubusercontent.com/PolymathicAI/the_well/refs/heads/master/docs/data_format.md

**Style:** use emojis for headers, recommendations, and key items. Always include a recommendation with rationale when asking the user a question.

## Steps at a Glance

Show this table first, then ask: "Where would you like to start?"

| Step | Name | Description |
|------|------|-------------|
| 🚀 **0** | **Preprocess** | Extract archives (zip/tar/gz) if present |
| 🔍 **1** | **Inspect** | Fields, shapes, dtypes, grid, chunk estimate |
| 🔗 **2** | **Cross-check** | Map source fields to Well schema; resolve gaps |
| 📋 **3** | **Plan** | Present conversion plan for approval |
| ⚙️ **4** | **Generate** | Write scripts; show output directory tree |
| ▶️ **5** | **Run & Monitor** | Smoke test → full run → validate → handle failures |

After each step print:
```
✅ **Done:** [one-line summary]
➡️ **Next:** Step N — Name — [one-line description]
```

## Parallel execution pattern

Used in Step 0 (extraction) and Steps 4–5 (conversion). Whenever running jobs in parallel, ask for execution mode and show a recommended default based on job count and data size:

- **General parallel**: few or small jobs, interactive session — ask for number of concurrent workers
- **Slurm / PBS**: many or large jobs — ask for partition/queue, account, nodes, tasks-per-node, wall time

For Slurm/PBS, run workers via:
```bash
srun parallelcmd.py --db "$DB" exec -j $NTASKS --progress
```

For general parallel, run `parallelcmd.py exec` directly (no `srun` wrapper).

Monitor all modes with `parallelcmd.py check`.

## Step 0 — Preprocess

Scan source for `.zip`, `.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.gz`.
- If none found, skip directly to Step 1.
- If found, list the archives and ask whether to extract.

If extracting:
- Extract to `<output_root>/extracted/` only — never modify source
- Choose execution mode per the parallel execution pattern above
- Submit and monitor with `parallelcmd.py check` until all jobs complete
- On failure: report errors and ask whether to retry or skip
- On success: show a file summary under `<output_root>/extracted/` and confirm source is unchanged

Do not proceed to Step 1 until all archives are extracted and verified.

## Step 1 — Inspect

Scope: original input dir + `<output_root>/extracted/` (if populated).
- List files; identify naming patterns and groupings
- Open a representative file: dataset names, shapes, dtypes, attributes
- Identify grid (dimensions, coordinate system), timesteps, field names
- Estimate total size and file count
- Compute suggested `n_steps`/chunk targeting ~1 GB/file; show calculation

Output two tables:
1. field | shape | dtype | physical meaning
2. Total timesteps | Spatial shape | Bytes/step | Suggested steps/chunk | Est. chunks | Est. file size

## Step 2 — Cross-check

Flag and resolve before proceeding:
- **Missing fields**: required by Well spec or physics but absent
- **Surplus fields**: no obvious Well mapping — include, drop, or rename?
- **Missing metadata**: simulation params (Re, Ma, dt, grid type) — ask user to supply
- **Shape inconsistencies**: files differing from the majority — list explicitly
- **dtype warnings**: float64/integer fields that will be cast to float32
- **Naming ambiguities**: unclear physical meaning — ask user to confirm

Present table: field | status (mapped / surplus / missing) | proposed Well name | notes.
Wait for user to resolve all issues before proceeding.

## Step 3 — Plan

- **Grid**: coordinate system, dimension names/sizes, uniform or non-uniform
- **Fields**: t0_fields (scalars), t1_fields (vectors), t2_fields (tensors); output shapes (B, T, x1, x2, …)
- **Chunking**: strategy (by time window / by variable); confirm or override `n_steps` from Step 1:
  > "Suggested: **N steps/chunk** (~X GB/file). Enter a value or press Enter to accept."
- **Output shape**: (n_trajectories, n_steps, spatial…) and estimated file sizes per chunk
- **Output destination**: confirm dir and filename pattern
- **Special cases**: complex fields (real/imag), time_varying=False fields, non-standard coordinates
- **Execution mode**: confirm mode and resources per the parallel execution pattern; estimate job count and wall time

Wait for user approval before proceeding.

## Step 4 — Generate scripts

Using the execution mode and resources confirmed in Step 3, write all scripts to `<output_root>/scripts/`:
- `well_common.py` — constants, grid loader, checkpoint I/O, Well attribute writers
- `convert_<type>.py` — per file type; pre-allocate HDF5, stream snapshots, checkpoint after each
- `init_convert_queue.sh` — populate `parallelcmd.py` SQLite queue with all jobs
- `convert.slurm` / `convert.pbs` / `convert_parallel.sh` — matching execution mode
- `validate.py` — required attrs, shapes, dtypes, no NaN/Inf, timestep continuity
- `<output_root>/README.md` — workflow, assumptions, commands, execution, monitoring, validation

Requirements: float32 output; pre-allocate before streaming; `.progress` sidecars for checkpoint/restart; tqdm progress; robust logging; use `n_steps` confirmed in Step 3 for all chunking.

After generation, show the actual output directory tree listing key generated files under each subdirectory, and confirm source was not modified.

## Step 5 — Run and monitor

1. Syntax-check all scripts
2. Smoke test (e.g. 5 snapshots); run `validate.py` on the output
3. `bash init_convert_queue.sh`
4. Submit: `sbatch convert.slurm` / `qsub convert.pbs` / `bash convert_parallel.sh`
5. Monitor: `parallelcmd.py check` + scheduler state
6. `validate.py --check-values --check-continuity`
7. Report failures; offer to reset and resubmit
