from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.7.0"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'genesis',
     'default_range': 'string',
     'description': 'A schema for representing datacards in the Genesis project. A '
                    'datacard is a structured metadata document that describes a '
                    'dataset: what it is, where it came from, who created it, how '
                    'it can be accessed, and how it can be used.  Datacards serve '
                    'both humans (who need to understand a dataset before using '
                    'it) and machines (automated pipelines that ingest, catalog, '
                    'and validate datasets). In Genesis, every dataset — '
                    'regardless of size, sensitivity, or publication state — '
                    'should have a datacard.  A datacard can be created at the '
                    'same time as the dataset, or as early in the workflow as '
                    'possible.',
     'id': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
     'imports': ['linkml:types'],
     'name': 'genesis_datacard',
     'prefixes': {'adms': {'prefix_prefix': 'adms',
                           'prefix_reference': 'https://www.w3.org/TR/vocab-adms/'},
                  'datacite': {'prefix_prefix': 'datacite',
                               'prefix_reference': 'https://schema.datacite.org/meta/kernel-4.7/'},
                  'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'genesis': {'prefix_prefix': 'genesis',
                              'prefix_reference': 'https://example.org/genesis_datacard/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'},
                  'xsd': {'prefix_prefix': 'xsd',
                          'prefix_reference': 'http://www.w3.org/2001/XMLSchema#'}},
     'source_file': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
     'subsets': {'accessibility_if_applicable': {'description': 'These fields are '
                                                                'optional, but '
                                                                'recommended, for '
                                                                'datacards of '
                                                                'datasets that are '
                                                                'intended to be '
                                                                'shared or '
                                                                'accessed by '
                                                                'others,  whether '
                                                                'internally within '
                                                                'a project or '
                                                                'organization, '
                                                                'with external '
                                                                'collaborators, or '
                                                                'publicly. They '
                                                                'provide '
                                                                'additional '
                                                                'information about '
                                                                'how to access the '
                                                                'dataset,  '
                                                                'including any '
                                                                'restrictions or '
                                                                'requirements for '
                                                                'access, which can '
                                                                'enhance '
                                                                'accessibility and '
                                                                'support reuse of '
                                                                'the dataset by '
                                                                'others. They may '
                                                                'not be applicable '
                                                                'to all datasets, '
                                                                'but should be '
                                                                'included when '
                                                                'relevant and '
                                                                'available to '
                                                                'provide important '
                                                                'context for '
                                                                'users, both '
                                                                'humans and '
                                                                'machines, about '
                                                                'how to access the '
                                                                'dataset.',
                                                 'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                                 'name': 'accessibility_if_applicable'},
                 'accessibility_required': {'description': 'These fields are '
                                                           'required for datacards '
                                                           'of datasets that are '
                                                           'intended to be shared '
                                                           'or accessed by '
                                                           'others,  whether '
                                                           'internally within a '
                                                           'project or '
                                                           'organization, with '
                                                           'external '
                                                           'collaborators, or '
                                                           'publicly. These fields '
                                                           'provide critical '
                                                           'information about how '
                                                           'the dataset can be '
                                                           'accessed, requested, '
                                                           'retrieved, cited, and '
                                                           'reused by others,  in '
                                                           'addition to '
                                                           'information on how to '
                                                           'contact the point of '
                                                           'contact(s) for access '
                                                           'requests, and any '
                                                           'restrictions or '
                                                           'requirements for '
                                                           'access,  which is '
                                                           'essential for enabling '
                                                           'accessibility and '
                                                           'reuse of the dataset '
                                                           'by others.',
                                            'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                            'name': 'accessibility_required'},
                 'ai_usability_if_applicable': {'description': 'These fields are '
                                                               'optional, but '
                                                               'recommended, for '
                                                               'datacards of '
                                                               'datasets that are '
                                                               'intended to be '
                                                               'used for AI '
                                                               'training, '
                                                               'evaluation, or '
                                                               'other AI-related '
                                                               'purposes. They '
                                                               'provide additional '
                                                               'information about '
                                                               'the restrictions, '
                                                               'biases, risks, '
                                                               'safety '
                                                               'considerations, '
                                                               'and other factors '
                                                               'related to using '
                                                               'the dataset for AI '
                                                               'purposes  that can '
                                                               'enhance '
                                                               'responsible use of '
                                                               'the dataset for AI '
                                                               'purposes by '
                                                               'others. They may '
                                                               'not be applicable '
                                                               'to all datasets, '
                                                               'but should be '
                                                               'included when '
                                                               'relevant and '
                                                               'available to '
                                                               'provide important '
                                                               'context for '
                                                               'users,  both '
                                                               'humans and '
                                                               'machines, about '
                                                               'the usability of '
                                                               'the dataset for AI '
                                                               'purposes.',
                                                'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                                'name': 'ai_usability_if_applicable'},
                 'ai_usability_required': {'description': 'These fields are '
                                                          'required for datacards '
                                                          'of datasets that are '
                                                          'intended to be used for '
                                                          'AI training, '
                                                          'evaluation, or other '
                                                          'AI-related purposes. '
                                                          'These fields provide '
                                                          'critical information '
                                                          'about the allowed ai '
                                                          'use for AI purposes. '
                                                          'This information is '
                                                          'essential for enabling '
                                                          'responsible use of the '
                                                          'dataset for AI purposes '
                                                          'by others,  as it '
                                                          'informs users about the '
                                                          'permissions, '
                                                          'restrictions, and '
                                                          'requirements for using '
                                                          'the dataset for AI '
                                                          'purposes,  which are '
                                                          'key factors in '
                                                          'determining whether and '
                                                          'how a dataset can be '
                                                          'used by AI.',
                                           'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                           'name': 'ai_usability_required'},
                 'discoverability_if_applicable': {'description': 'Optional, but '
                                                                  'recommended, '
                                                                  'for datacards '
                                                                  'of datasets '
                                                                  'that are '
                                                                  'intended to be '
                                                                  'discoverable  '
                                                                  'in catalogs and '
                                                                  'repositories, '
                                                                  'to support '
                                                                  'basic '
                                                                  'findability. '
                                                                  'These fields '
                                                                  'may not be '
                                                                  'applicable to '
                                                                  'all datasets,  '
                                                                  'but should be '
                                                                  'included when '
                                                                  'relevant and '
                                                                  'available to '
                                                                  'enhance '
                                                                  'discoverability '
                                                                  'and provide '
                                                                  'important '
                                                                  'context  for '
                                                                  'users, both '
                                                                  'humans and '
                                                                  'machines.',
                                                   'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                                   'name': 'discoverability_if_applicable'},
                 'discoverability_required': {'description': 'These essential '
                                                             'fields are designed '
                                                             'to facilitate '
                                                             'discovery using the '
                                                             'datacard metadata. '
                                                             'These encompass the '
                                                             'minimum set of '
                                                             'metadata fields that '
                                                             'should be included '
                                                             'in all datacards for '
                                                             'datasets in catalogs '
                                                             'and repositories, to '
                                                             'support basic '
                                                             'findability.',
                                              'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                              'name': 'discoverability_required'},
                 'governed_use_if_applicable': {'description': 'These fields are '
                                                               'optional, but '
                                                               'recommended, for '
                                                               'datacards of '
                                                               'datasets that are '
                                                               'intended to be '
                                                               'shared or accessed '
                                                               'under specific '
                                                               'governance or '
                                                               'oversight. They '
                                                               'provide additional '
                                                               'information about '
                                                               'the governance and '
                                                               'oversight for the '
                                                               'dataset that can '
                                                               'enhance '
                                                               'responsible '
                                                               'sharing and use of '
                                                               'the dataset by '
                                                               'others. They may '
                                                               'not be applicable '
                                                               'to all datasets, '
                                                               'but should be '
                                                               'included when '
                                                               'relevant and '
                                                               'available to '
                                                               'provide important '
                                                               'context for users, '
                                                               'both humans and '
                                                               'machines, about '
                                                               'the governance and '
                                                               'oversight for the '
                                                               'dataset.',
                                                'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                                'name': 'governed_use_if_applicable'},
                 'governed_use_required': {'description': 'These fields are '
                                                          'required for datacards '
                                                          'of datasets that are '
                                                          'intended to be shared '
                                                          'or accessed under '
                                                          'specific governance or '
                                                          'oversight,  such as '
                                                          'datasets that are '
                                                          'subject to security '
                                                          'controls, export '
                                                          'control, IRB oversight, '
                                                          'or other types of '
                                                          'formal review and '
                                                          'approval processes. '
                                                          'These fields provide '
                                                          'critical information '
                                                          'about the governance '
                                                          'and oversight for the '
                                                          'dataset,  which is '
                                                          'essential for ensuring '
                                                          'that the dataset is '
                                                          'shared and accessed in '
                                                          'compliance with '
                                                          'applicable regulations, '
                                                          'policies, and ethical '
                                                          'considerations, and for '
                                                          'enabling responsible '
                                                          'use of the dataset by '
                                                          'others.',
                                           'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                           'name': 'governed_use_required'},
                 'interoperability_if_applicable': {'description': 'These fields '
                                                                   'are optional, '
                                                                   'but '
                                                                   'recommended, '
                                                                   'for datacards '
                                                                   'of datasets '
                                                                   'that are '
                                                                   'intended to be '
                                                                   'interoperable. '
                                                                   'They provide '
                                                                   'additional '
                                                                   'information '
                                                                   'about the '
                                                                   'meaning, data '
                                                                   'representation '
                                                                   'and structure, '
                                                                   'provenance,  '
                                                                   'related '
                                                                   'resources and '
                                                                   'integrity of '
                                                                   'the dataset '
                                                                   'that can '
                                                                   'enhance '
                                                                   'interoperability '
                                                                   'and support '
                                                                   'integration '
                                                                   'with other '
                                                                   'datasets or '
                                                                   'systems. They '
                                                                   'may not be '
                                                                   'applicable to '
                                                                   'all datasets, '
                                                                   'but should be '
                                                                   'included when '
                                                                   'relevant and '
                                                                   'available.',
                                                    'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                                    'name': 'interoperability_if_applicable'},
                 'interoperability_required': {'description': 'These fields are '
                                                              'required for '
                                                              'datacards of '
                                                              'datasets that are '
                                                              'intended to be '
                                                              'interoperable,  '
                                                              'meaning they are '
                                                              'intended to be '
                                                              'integrated with '
                                                              'other datasets or '
                                                              'systems, or used in '
                                                              'combination with '
                                                              'other datasets. '
                                                              'These fields '
                                                              'provide critical '
                                                              'information about '
                                                              'the meaning, data '
                                                              'representation and '
                                                              'structure, '
                                                              'provenance,  '
                                                              'related resources '
                                                              'and integrity of '
                                                              'the dataset.',
                                               'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                               'name': 'interoperability_required'},
                 'reference_only_do_not_include': {'description': 'These fields '
                                                                  'are provided '
                                                                  'for reference '
                                                                  'only and should '
                                                                  'not be included '
                                                                  'in a final, '
                                                                  'completed '
                                                                  'datacard.',
                                                   'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                                   'name': 'reference_only_do_not_include'},
                 'required': {'description': 'Required for all datacards, '
                                             'regardless of intended use or '
                                             'sharing level and use.',
                              'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                              'name': 'required'},
                 'reusability_if_applicable': {'description': 'These fields are '
                                                              'optional, but '
                                                              'recommended, for '
                                                              'datacards of '
                                                              'datasets that are '
                                                              'intended to be '
                                                              'reusable. They '
                                                              'provide additional '
                                                              'information about '
                                                              'the license, '
                                                              'stewardship,  and '
                                                              'data quality of the '
                                                              'dataset that can '
                                                              'enhance reuse and '
                                                              'support informed '
                                                              'decision-making by '
                                                              'users about  '
                                                              'whether and how to '
                                                              'reuse the dataset '
                                                              'for a particular '
                                                              'purpose. These '
                                                              'include optional '
                                                              'domain-specific '
                                                              'metadata fields '
                                                              'that can provide '
                                                              'important context '
                                                              'about the dataset '
                                                              'for users in '
                                                              'specific scientific '
                                                              'domains,  such as '
                                                              'scientific domain, '
                                                              'data type, and '
                                                              'experimental '
                                                              'method, which can '
                                                              'be critical for '
                                                              'determining the '
                                                              'relevance and  '
                                                              'suitability of the '
                                                              'dataset for '
                                                              'specific research '
                                                              'questions or '
                                                              'analyses. They may '
                                                              'not be applicable '
                                                              'to all datasets, '
                                                              'but should be '
                                                              'included when '
                                                              'relevant and '
                                                              'available to '
                                                              'provide important '
                                                              'context for users,  '
                                                              'both humans and '
                                                              'machines, about the '
                                                              'reuse potential of '
                                                              'the dataset.',
                                               'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                               'name': 'reusability_if_applicable'},
                 'reusability_required': {'description': 'These fields are '
                                                         'required for datacards '
                                                         'of datasets that are '
                                                         'intended to be '
                                                         'reusable,  meaning they '
                                                         'are intended to be '
                                                         'reused by others for the '
                                                         'same or different '
                                                         'purposes. These fields '
                                                         'provide critical '
                                                         'information about the '
                                                         'the authorship, license, '
                                                         'stewardship, and '
                                                         'data_quality. This '
                                                         'information is essential '
                                                         'for enabling reuse of '
                                                         'the dataset by others,  '
                                                         'as it informs users '
                                                         'about the permissions, '
                                                         'responsibilities, and '
                                                         'quality of the dataset,  '
                                                         'which are key factors in '
                                                         'determining whether and '
                                                         'how a dataset can be '
                                                         'reused for a particular '
                                                         'purpose.',
                                          'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
                                          'name': 'reusability_required'}}} )

class IdentifierTypeEnum(str, Enum):
    """
    The type of identifier, following a controlled vocabulary (e.g., DOI, UUID, ARK).
    """
    ark = "ark"
    doi = "doi"
    handle = "handle"
    local = "local"
    purl = "purl"
    url = "url"
    urn = "urn"
    uuid = "uuid"
    other = "other"
    unregistered = "unregistered"


class OverallSensitivityEnum(str, Enum):
    """
    Controlled vocabulary for the human-readable top-level sensitivity posture of the asset. This field is intended to provide a high-level summary of the overall sensitivity posture of the asset.
    """
    Public = "Public"
    """
    No sensitivity; publicly shareable.
    """
    Unclassified_Uncontrolled = "Unclassified_Uncontrolled"
    """
    Unclassified but uncontrolled; may have minimal sensitivity;  generally shareable with minimal controls.
    """
    CUI = "CUI"
    """
    CUI (Controlled Unclassified Information);  requires handling per CUI guidelines; access controls required.
    """
    UCNI = "UCNI"
    """
    UCNI (Unclassified Controlled Nuclear Information);  requires handling per UCNI guidelines; strict access controls required.
    """
    Classified = "Classified"
    """
    Classified information; requires handling per classification level and guide;  strict access controls required.
    """
    Legacy_Controlled = "Legacy_Controlled"
    """
    Legacy controlled information; may have specific handling requirements based on legacy controls;  access controls required.
    """
    Mixed = "Mixed"
    """
    Mixed sensitivity; contains a combination of sensitive and non-sensitive information;  handling requirements depend on the specific content; access controls required.
    """
    Other_Controlled = "Other_Controlled"
    """
    Other controlled information; may have specific handling requirements based on other controls;  access controls required.
    """


class SourceMarkingSchemeEnum(str, Enum):
    """
    Controlled vocabulary that identifies the authoritative source marking regime for the asset. This describes the marking scheme used to identify sensitive information in the dataset,  which is important for users to understand how sensitivity is indicated and what markings to look for when handling the dataset.
    """
    DOE_CUI = "DOE_CUI"
    DOE_UCNI = "DOE_UCNI"
    EO13526_Classified = "EO13526_Classified"
    AEA_RD_FRD_TFNI = "AEA_RD_FRD_TFNI"
    DOD_CUI = "DOD_CUI"
    DHS_CUI = "DHS_CUI"
    Legacy_OUO = "Legacy_OUO"
    Legacy_Site_Specific = "Legacy_Site_Specific"
    Other_Agency = "Other_Agency"
    None_ = "None"


class AccessLevelEnum(str, Enum):
    """
    The access level of the document being described.
    """
    Open = "Open"
    """
    Anyone can discover and access without special permissions.
    """
    Restricted = "Restricted"
    """
    Data may be discoverable, but users must satisfy basic access requirements (authentication, institutional affiliation, registration, agreement to terms, etc.). Approval is generally automatic or administrative.
    """
    Controlled = "Controlled"
    """
    Access is granted only after review and explicit authorization based on the requester, intended use, legal requirements, or security considerations. Requests may be denied.
    """


class DatacardCreationMethodEnum(str, Enum):
    """
    How this datacard was created or most recently updated.
    """
    Manual = "Manual"
    """
    Created entirely manually by a human author.
    """
    Automated = "Automated"
    """
    Generated entirely by a pipeline, AI model, or other automated process.
    """
    Hybrid = "Hybrid"
    """
    Created using a combination of manual and automated methods. This field supports automation of downstream quality assessment and provenance tracking after human authorship, or an inverse approach where the creation method is automated and used to determine how much trust to place in the datacard content.
    """


class RoleEnum(str, Enum):
    """
    The role of a type (person, organization, AI model, or software tool) in relation to the datacard or dataset. This describes the role of an agent (which could be a person, organization, AI model, or software tool) in relation to an activity or asset.
Aligns with CRediT taxonomy (https://zenodo.org/records/18421449) where applicable, but is extended to cover additional roles relevant to datasets and datacards, such as data collection, curation, sponsorship, and access provision.
    """
    Conceptualization = "Conceptualization"
    """
    Ideas; formulation or evolution of overarching research goals and aims. Identifying issues, questions or problems that warrant research. Developing research questions and hypotheses. Developing research frameworks, tools or experimental paradigms. Refining and adapting overarching research goals and aims.
    """
    Data_Curation = "Data_Curation"
    """
    Management activities to annotate (produce metadata), scrub data and maintain research data  (including software code, where it is necessary for interpreting the data itself) for initial use and later re-use. Conducting tasks like data processing, cleaning, cataloging, annotating, archiving modeling, and retention. Integrating and aggregating data in diverse formats and from diverse sources. Managing and updating data descriptions and metadata, including maintaining version control and associated documentation. Developing or implementing data preservation strategies to ensure data remains findable, accessible, interoperable and reusable.
    """
    Formal_Analysis = "Formal_Analysis"
    """
    Application of statistical, mathematical, computational, or other formal techniques to analyse or synthesize study data. Uncovering patterns and identifying relationships between variables and quantitative or qualitative datasets. Performing statistical tests to compare different groups within a study or evaluate change. Applying AI and machine learning models to predict outcomes. Developing computational simulations to model complex systems or phenomena.
    """
    Funding_Acquisition = "Funding_Acquisition"
    """
    Acquisition of the financial support for the project leading to this publication [dataset]. Identifying suitable funding sources, assessing eligibility and communicating requirements with the team members. Developing grant proposals and coordinating the submission process. Developing budgets and allocating funds to match project scope and funder expectations.
    """
    Investigation = "Investigation"
    """
    Conducting a research and investigation process, specifically performing the experiments, or data/evidence collection. Following or modifying methods to collect or generate data through, for quantitative and/or qualitative research approaches. Testing research hypotheses and documenting the research process. Searching and reviewing the literature, samples, data and other evidence. Reporting findings for further discussion, analysis, and exchange of ideas.
    """
    Methodology = "Methodology"
    """
    Development or design of methodology; creation of models. Developing quantitative and/or qualitative methodologies and frameworks. Defining search strategies and determining criteria for systematic literature reviews. Determining study design such as participant selection, materials, settings, data characteristics, data collection, measurement, and analysis techniques.
    """
    Project_Administration = "Project_Administration"
    """
    Management and coordination responsibility for the research activity planning and execution. Monitoring and reporting progress, timelines, budgets, and compliance with ethical, governance, legal, health, safety, and other relevant standards. Recruiting participants needed for the research method (e.g. for interviews, focus groups, surveys, fieldwork, clinical trials). Organizing logistics for expeditions, fieldwork, equipment setup, and space allocation that support research operations. Managing correspondence with team members, journal editors, and various institutional departments.
    """
    Resources = "Resources"
    """
    Provision of study materials, reagents, materials, patients, laboratory samples, animals, instrumentation, computing resources, or other analysis tools. Preparing, transporting or managing access to samples, artefacts, tools, equipment, documents, archives, and digital/physical infrastructure. Inventory management, safekeeping of samples and providing reports on availability and state of resources. Calibrating and maintaining instruments and equipment. Coordinating data storage solutions and computational resources.
    """
    Software = "Software"
    """
    Programming, software development; designing computer programs; implementation of the computer code and supporting algorithms; testing of existing code components. Designing, developing, testing, debugging, implementing, documenting, sharing and maintaining code. Developing, maintaining, managing and optimizing digital infrastructure, libraries, and databases. Conducting data extraction, data mining, and parsing content for qualitative or quantitative data collection and analysis. Ensuring interoperability, functionality, and scalability of code, databases, systems or platforms across different environments.
    """
    Supervision = "Supervision"
    """
    Oversight and leadership responsibility for the research activity planning and execution, including mentorship external to the core team. Overseeing researchers and other team members by setting milestones, tracking progress, ensuring quality of deliverables, and promoting adherence to ethics and integrity norms. Teaching, training, moderating and providing personal or professional advice to team members. Guiding teams in refining methods, interpreting results, and addressing interpersonal challenges. Collecting, logging, and reporting individual contributions to research.
    """
    Validation = "Validation"
    """
    Verification, whether as a part of the activity or separate, of the overall replication/reproducibility of results/experiments and other research outputs. Ensuring the integrity, rigor and reliability of data, methods, results and resources through reviewing, verification, benchmarking, factchecking and replicating. Conducting pilot tests or preliminary studies to validate data collection instruments and protocols. Appraising studies included in systematic reviews and ensuring compliance with established review standards or reporting frameworks. Testing computational models or simulations against known outcomes for accuracy.
    """
    Visualization = "Visualization"
    """
    Preparation, creation and/or presentation of the published work, specifically visualization/data presentation. Using data to create charts, graphs or figures. Creating videos and other interactive media for communicating the findings.
    """
    Writing_Original_Draft = "Writing_Original_Draft"
    """
    Preparation, creation and/or presentation of the published work, specifically writing the initial draft (including substantive translation). Creating the first and full version of an article. Drafting substantial original text within a section or across sections in an article.
    """
    Writing_Review_Editing = "Writing_Review_Editing"
    """
    Preparation, creation and/or presentation of the published work by those from the original research group, specifically critical review, commentary or revision – including pre- or post-publication stages. Reviewing, copy-editing, refining language and providing comments and suggestions. Revising content based on feedback from internal and external reviewers. Providing review input of figures, tables, and supplementary materials.
    """
    Data_Collection = "Data_Collection"
    """
    Extension of the CRediT taxonomy to capture the specific contribution of collecting or generating the data,  which is a critical part of many research projects, especially those that involve empirical data collection or experimental work.
    """
    Other = "Other"
    """
    Any other role not covered by the above CRediT taxonomy.
    """


class ProductTypeEnum(str, Enum):
    """
    The type of product described by this datacard.  These align with and extend the STI Product Types.
    """
    Technical_Report = "Technical_Report"
    """
    Documents reporting scientific and technical Information (STI).
    """
    Paper_or_Proceedings = "Paper_or_Proceedings"
    """
    Conference paper or proceedings.  Note that this is distinct from a journal article, which should be categorized as Journal_Article.
    """
    Journal_Article = "Journal_Article"
    """
    Journal Article.
    """
    Software_Manual = "Software_Manual"
    """
    The software manual that accompanies the software package.
    """
    Data = "Data"
    """
    A dataset; data may be numeric, graphic, or visual.
    """
    Collection = "Collection"
    """
    A collection of scientific and technical information (STI) products, such as a special issue of a journal, a conference proceedings, or a project data repository.
    """
    Computer_Related = "Computer_Related"
    """
    Computer-related products, such as software packages, pipelines, or automated processes.
    """
    Model = "Model"
    """
    A computational model, simulation, or trained machine learning model.
    """
    Agent = "Agent"
    """
    An AI agent or automated system.
    """


class ObjectTypeEnum(str, Enum):
    """
    Primary type of digital object described by this card. Used for alignment to other card types. Examples: a datacard describing a dataset would use dataset; 
a datacard describing a software tool would use software; 
a datacard describing an AI agent would use ai_agent; 
  
a datacard describing an infrastructure would use infrastructure; 
  
a datacard describing a resource would use resource; 
  
a datacard describing any other type of object would use other.
This is a high-level categorization to facilitate filtering and discovery, and alignment to other card types (e.g., software cards, model cards, agent cards). It is not intended to capture detailed scientific domain categories  (e.g., physics, chemistry, earth science) or data type categories (e.g., image, text, tabular).
    """
    Dataset = "Dataset"
    """
    A dataset, which may be described by a datacard.
    """
    Model = "Model"
    """
    A model, which may be described by a datacard.
    """
    Software = "Software"
    """
    A software tool, pipeline, or automated process.
    """
    AI_Agent = "AI_Agent"
    """
    An AI agent, which may be described by a datacard.
    """
    Infrastructure = "Infrastructure"
    """
    An infrastructure, which may be described by a datacard.
    """
    Resource = "Resource"
    """
    A resource, which may be described by a datacard.
    """
    Other = "Other"
    """
    Any other type of object not covered by the above categories.
    """


class DatasetTypeEnum(str, Enum):
    """
    OSTI DOE Data Explorer type code.
    """
    GD = "GD"
    """
    Genome/Genetic Data — DNA/RNA sequences, genomic annotations
    """
    IM = "IM"
    """
    Image — photographs, scans, microscopy, visualizations
    """
    ND = "ND"
    """
    Numeric Data — measurements, time series, tabular, sensor readings
    """
    SM = "SM"
    """
    Specialized Mix — multiple data types combined
    """
    FP = "FP"
    """
    Figure/Plot — charts, graphs, plots as primary deliverable
    """
    I = "I"
    """
    Interactive Resource — web apps, interactive visualizations, dashboards
    """
    MM = "MM"
    """
    Multimedia — audio, video, combined media
    """
    MD = "MD"
    """
    Model — computational models, simulations, trained ML models
    """
    AS = "AS"
    """
    Automated Software — scripts, analysis pipelines, workflows
    """
    IP = "IP"
    """
    Instrumentation/Protocols — experimental protocols, instrument specs
    """
    IG = "IG"
    """
    Integrated Genomic Resources — combined genomic databases and tools
    """


class ReleaseStatusEnum(str, Enum):
    """
    Current publication and governance state of this dataset.
    """
    Draft = "Draft"
    """
    The dataset is a work in progress. It is in draft form and not yet ready for sharing or publication.
    """
    Under_Review = "Under_Review"
    """
    The dataset has been submitted for review by internal or external stakeholders. It is not yet approved for sharing or publication.
    """
    Approved = "Approved"
    """
    The dataset has been reviewed and approved for sharing or publication, but has not yet been released.
    """
    Published = "Published"
    """
    The dataset has been published and is available for access and use.  Does not necessarily indicate that the dataset was reviewed and approved by a formal governing body. Reference security section, and categorization tags, and most importantly,  the reviews section for details on the review and approval status of the dataset.
    """
    Deprecated = "Deprecated"
    """
    The dataset has been superseded or retired and should not be used.
    """


class StateEnum(str, Enum):
    """
    Current lifecycle position:
    """
    Raw = "Raw"
    """
    Data as collected in its original, unprocessed form.
    """
    Processing = "Processing"
    """
    Data actively being cleaned, transformed, or reduced.
    """
    QA = "QA"
    """
    Data undergoing quality assurance or validation.
    """
    Analysis = "Analysis"
    """
    Data in active scientific analysis.
    """
    Review = "Review"
    """
    Data under formal review (security, export, IRB, etc.).
    """
    Embargo = "Embargo"
    """
    Data under temporary restriction or embargo, withheld from release.
    """
    Published = "Published"
    """
    Data that has been published and is available for access and use.
    """
    Archived = "Archived"
    """
    Data that is no longer actively maintained but preserved for historical record or reference.
    """
    not_applicable = "not_applicable"
    """
    Lifecycle state does not apply to this dataset.
    """


class AuthorizationRequiredEnum(str, Enum):
    """
    Controlled vocabulary for whether authorization is required to access the dataset.
    """
    Account = "Account"
    """
    Registered account is required to access the dataset.
    """
    User_Agreement = "User_Agreement"
    """
    User agreement is required to access the dataset.
    """
    Data_Use_Agreement = "Data_Use_Agreement"
    """
    Formal Data Use Agreement (DUA) is required to access the dataset.
    """
    Sponsor_Approval = "Sponsor_Approval"
    """
    Approval from the dataset sponsor is required to access the dataset.
    """
    Export_Control_Review = "Export_Control_Review"
    """
    Export control review is required to access the dataset.
    """
    IRB_Approval = "IRB_Approval"
    """
    Institutional Review Board (IRB) approval is required to access the dataset.
    """
    Other = "Other"
    """
    Other authorization requirements may apply to access the dataset: describe in access_restrictions.
    """


class NeedToKnowBasisEnum(str, Enum):
    """
    Controlled vocabulary for the basis of need-to-know restrictions on access to the dataset.
    """
    Mission_Need = "Mission_Need"
    """
    Authentication is required to access the dataset based on mission needs or operational requirements.
    """
    Job_Duty = "Job_Duty"
    """
    Authentication is required to access the dataset based on job duties or role-based access controls.
    """
    Project_Program_Association = "Project_Program_Association"
    """
    Authentication is required to access the dataset based on association with a specific project or program.
    """
    Agreement_Defined = "Agreement_Defined"
    """
    Authentication is required to access the dataset based on terms defined in a user agreement, data use agreement, or other formal agreement.
    """
    DGB_Exception_Waiver = "DGB_Exception_Waiver"
    """
    Authentication is required to access the dataset based on an exception or waiver granted by the Data Governance Board (DGB) or other governing body.
    """


class AuthenticationTypeEnum(str, Enum):
    """
    Controlled vocabulary for types of authentication required to access the dataset.
    """
    None_ = "None"
    """
    No authentication is required to access the dataset.
    """
    API_Key = "API_Key"
    """
    API key is required to access the dataset.
    """
    OAuth2 = "OAuth2"
    """
    OAuth2 authentication is required to access the dataset.
    """
    SAML = "SAML"
    """
    SAML authentication is required to access the dataset.
    """
    Certificate = "Certificate"
    """
    Certificate-based authentication is required to access the dataset.
    """
    OpenID_Connect = "OpenID_Connect"
    """
    OpenID Connect authentication is required to access the dataset.
    """
    Basic_Auth = "Basic_Auth"
    """
    Basic authentication is required to access the dataset.
    """
    Bearer_Token = "Bearer_Token"
    """
    Bearer token authentication is required to access the dataset.
    """
    Other = "Other"
    """
    Other types of authentication may be required to access the dataset.
    """


class RelationshipTypeEnum(str, Enum):
    """
    Controlled vocabulary for the relationship between a source dataset and the dataset described in the datacard.
    """
    is_derived_from = "is_derived_from"
    """
    The dataset described in the datacard was derived from the source dataset.
    """
    is_based_on = "is_based_on"
    """
    The dataset described in the datacard is part of the source dataset.
    """
    is_part_of = "is_part_of"
    """
    The dataset described in the datacard is a version of the source dataset.
    """
    has_part = "has_part"
    """
    The dataset described in the datacard is related to the source dataset in some way that is not captured by the other relationship types.
    """
    references = "references"
    """
    The dataset described in the datacard references the source dataset.
    """
    other = "other"
    """
    Any other relationship not covered by the above categories.
    """


class ExtendedRelationshipEnum(str, Enum):
    """
    Extended relationship types for more specific relationships between a source dataset and software and models.
    """
    used_to_create = "used_to_create"
    """
    The source dataset was used to create the dataset described in the datacard.
    """
    used_to_process = "used_to_process"
    """
    The source dataset was used to process the dataset described in the datacard.
    """
    used_to_analyze = "used_to_analyze"
    """
    The source dataset was used to analyze the dataset described in the datacard.
    """
    recorded_by = "recorded_by"
    """
    The dataset described in the datacard was recorded by the source dataset.
    """
    trained_on = "trained_on"
    """
    The dataset described in the datacard was trained on the source dataset.
    """
    evaluated_on = "evaluated_on"
    """
    The dataset described in the datacard was evaluated on the source dataset.
    """


class StewardshipLevelEnum(str, Enum):
    """
    Controlled vocabulary for the stewardship level/management of the dataset.
    """
    Project_Managed = "Project_Managed"
    """
    Project level stewardship; dataset is maintained by the project or research team that created it,  with maintenance and updates occurring based on project resources and priorities.
    """
    Repository_Managed = "Repository_Managed"
    """
    Repository level stewardship; dataset is maintained by the repository or catalog system where it is hosted,  with ongoing maintenance, updates, and curation to ensure long-term accessibility and usability.
    """
    Externally_Managed = "Externally_Managed"
    """
    Externally managed stewardship; dataset is maintained by an external organization or entity,  such as a government agency, research institution, or commercial provider.
    """
    not_applicable = "not_applicable"
    """
    Stewardship level is not applicable or not known for this dataset.
    """


class ScienceDomainEnum(str, Enum):
    """
    Controlled vocabulary for the scientific domain or discipline of the dataset. Extends OSTI's identified Subject Areas.'
    """
    Biology_and_Medicine = "Biology and Medicine"
    """
    The fields of biology and medicine, including subfields such as molecular biology, ecology, evolutionary biology, and medical research.
    """
    Chemistry = "Chemistry"
    """
    The field of chemistry, including subfields such as organic chemistry, inorganic chemistry, and physical chemistry.
    """
    Energy_Storage_Conversion_and_Utilization = "Energy Storage, Conversion, and Utilization"
    """
    The field of energy storage, conversion, and utilization, including subfields such as battery technology, fuel cells, and renewable energy systems.
    """
    Engineering = "Engineering"
    """
    The field of engineering, including subfields such as mechanical engineering, electrical engineering, and civil engineering.
    """
    Environmental_Sciences = "Environmental Sciences"
    """
    The field of environmental sciences, including subfields such as ecology, climate science, and environmental chemistry.
    """
    Fission_and_Nuclear_Technologies = "Fission and Nuclear Technologies"
    """
    The field of fission and nuclear technologies, including subfields such as nuclear reactor physics, nuclear fuel cycle, and nuclear materials.
    """
    Fossil_Fuels = "Fossil Fuels"
    """
    The field of fossil fuels, including subfields such as petroleum engineering, coal science, and natural gas technology.
    """
    Geosciences = "Geosciences"
    """
    The field of geosciences, including subfields such as geology, geophysics, and geochemistry.
    """
    Materials = "Materials"
    """
    The field of materials science, including subfields such as materials characterization, materials synthesis, and materials modeling.
    """
    Mathematics_and_Computing = "Mathematics and Computing"
    """
    The fields of mathematics and computing, including subfields such as algebra, calculus, artificial intelligence, machine learning, and data science.
    """
    National_Defense = "National Defense"
    """
    The field of national defense, including subfields such as military technology, defense systems, and security studies.
    """
    Physics = "Physics"
    """
    The field of physics, including subfields such as particle physics, condensed matter physics, and astrophysics.
    """
    Power_Generation_and_Distribution = "Power Generation and Distribution"
    """
    The field of power generation and distribution, including subfields such as electrical power systems, renewable energy integration, and smart grid technologies.
    """
    Renewable_Energy = "Renewable Energy"
    """
    The field of renewable energy, including subfields such as solar energy, wind energy, and bioenergy.
    """
    Other = "Other"
    """
    Extends the OSTI Subject Areas; the field is related to a scientific domain not covered by the above categories.
    """


class UpdateFrequencyEnum(str, Enum):
    """
    Controlled vocabulary for how frequently the dataset is updated.
    """
    None_ = "None"
    """
    The dataset is not updated after its initial release.
    """
    Ad_Hoc = "Ad_Hoc"
    """
    The dataset is updated on an ad hoc basis, without a regular schedule.
    """
    Monthly = "Monthly"
    """
    The dataset is updated on a monthly basis.
    """
    Quarterly = "Quarterly"
    """
    The dataset is updated on a quarterly basis.
    """
    Annually = "Annually"
    """
    The dataset is updated on an annual basis.
    """
    Continuously = "Continuously"
    """
    The dataset is updated continuously, with new data added as it becomes available.
    """
    Other = "Other"
    """
    Other update frequency.
    """


class FundingSourceEnum(str, Enum):
    """
    Controlled vocabulary for the funding source of the dataset.
    """
    DOE_Program_SC = "DOE_Program_SC"
    """
    U.S. Department of Energy (DOE) - Office of Science
    """
    DOE_Program_NNSA = "DOE_Program_NNSA"
    """
    U.S. Department of Energy (DOE) - National Nuclear Security Administration
    """
    LDRD = "LDRD"
    """
    Laboratory Directed Research and Development (LDRD) funding
    """
    WFO = "WFO"
    """
    Work for Others (WFO) funding from a non-DOE entity
    """
    CRADA = "CRADA"
    """
    Cooperative Research and Development Agreement (CRADA) funding from a non-DOE entity
    """
    Other_Federal = "Other_Federal"
    """
    Other federal government funding source (e.g., NSF, NIH, DOD)
    """
    State_Government = "State_Government"
    """
    State government funding source
    """
    Subcontract = "Subcontract"
    """
    Subcontract funding from a prime contractor
    """
    Industry = "Industry"
    """
    Industry or commercial entity
    """
    Nonprofit = "Nonprofit"
    """
    Nonprofit organization or foundation
    """
    Internal = "Internal"
    """
    Internal project or institutional funding
    """
    Other = "Other"
    """
    Other funding source not covered by the above categories
    """


class IntendedPartnerClassEnum(str, Enum):
    """
    Controlled vocabulary for the intended partner class for sharing datasets. Specifies the intended partner classes or user groups that are allowed to access the dataset.
    """
    Internal_Team = "Internal_Team"
    """
    The dataset is intended to be shared only within the internal project team or organization.
    """
    Tri_Lab = "Tri_Lab"
    """
    The dataset is intended to be shared with other DOE national laboratories.
    """
    DOE_NNSA_Lab = "DOE_NNSA_Lab"
    """
    The dataset is intended to be shared with DOE National Nuclear Security Administration (NNSA) laboratories.
    """
    Federal_Partner = "Federal_Partner"
    """
    The dataset is intended to be shared with federal government partners outside of DOE.
    """
    Contractor = "Contractor"
    """
    The dataset is intended to be shared with contractors or commercial partners.
    """
    Academic_Researchers = "Academic_Researchers"
    """
    The dataset is intended to be shared with academic researchers or institutions.
    """
    External_Research_Partner = "External_Research_Partner"
    """
    The dataset is intended to be shared with external research partners or collaborators.
    """
    Industry_Partner = "Industry_Partner"
    """
    The dataset is intended to be shared with industry partners or commercial entities.
    """
    Public = "Public"
    """
    The dataset is intended to be shared publicly, with no restrictions on access.
    """
    Other = "Other"
    """
    The dataset is intended to be shared with some other partner class or user group
    """


class ClassificationLevelEnum(str, Enum):
    """
    Controlled vocabulary for the official classification level, if the asset is classified.
Can be used for filtering and discovery in catalogs.
    """
    Top_Secret = "Top_Secret"
    Secret = "Secret"
    Confidential = "Confidential"


class ClassificationCategoryEnum(str, Enum):
    """
    Controlled vocabulary for the official classification category/categories, if applicable.
Can be used for filtering and discovery in catalogs.
    """
    NSI = "NSI"
    """
    National Security Information datasets, including data related to national defense, intelligence, and security operations.
    Can include Top Secret, Secret, and Confidential information that is not related to nuclear weapons or materials.
    """
    RD = "RD"
    """
    Comprises all data related to: the design, manufacture, or use of nuclear weapons;  production of special nuclear material (SNM);  or use of SNM in the production of energy.  RD does not include data removed from the Restricted Data category,  i.e., data that is designated Formerly Restricted Data (FRD) or Transclassified Foreign Nuclear Information (TFNI).
    """
    FRD = "FRD"
    """
    Formerly Restricted Data datasets, still a category of classified information related to nuclear weapons.  It does not mean it is formerly classified and therefore is now unclassified.  FRD is jointly determined by DoD and DOE to relate primarily to the military use of nuclear weapons, and is safeguarded as defense information (e.g., weapon yield, deployment locations, weapons safety and storage, and stockpile quantities).
    """
    TFNI = "TFNI"
    """
    Transclassified Foreign Nuclear Information datasets, information from any intelligence source  that concerns the nuclear programs of foreign governments that was removed from the RD category (by transclassification)  under section 142 of the Atomic Energy Act, by past joint agreements between DOE and the Director of Central Intelligence,  or past and future agreements with the Director of National Intelligence.  When removed from the RD category, TFNI information is stored, transmitted, and destroyed in the same ways as NSI of the same classification level.  DoD and DOE have separate systems for controlling nuclear information.
    """
    Other_Classified = "Other_Classified"
    """
    Other classified datasets that do not fall under the NSI, RD, FRD, or TFNI categories, but are still classified under EO 13526 or other applicable classification authorities. 
      This can include datasets related to sensitive intelligence sources and methods, classified research and development projects, and other types of classified information that require protection.
    """


class UKMDAStatusEnum(str, Enum):
    """
    Controlled vocabulary for the indication of whether the asset is subject to UK MDA-specific handling.
    """
    Yes = "Yes"
    """
    The asset is subject to UK MDA-specific handling.
    """
    No = "No"
    """
    The asset is not subject to UK MDA-specific handling.
    """
    Unknown = "Unknown"
    """
    It is unknown whether the asset is subject to UK MDA-specific handling.
    """
    not_applicable = "not_applicable"
    """
    UK MDA-specific handling is not applicable to this asset.
    """


class NormalizedControlBasisEnum(str, Enum):
    """
    Controlled vocabulary for the interpreted control basis used for governance where source materials contain legacy, mixed, or non-standard constructs.  This does not replace authoritative source markings.
    """
    Classified = "Classified"
    CUI = "CUI"
    UCNI = "UCNI"
    Public_Release_Approved = "Public_Release_Approved"
    Legacy_Needs_Mapping = "Legacy_Needs_Mapping"
    Other_Controlled = "Other_Controlled"


class YesNoEnum(str, Enum):
    """
    Controlled vocabulary for fields with "Yes" or "No" values. Use quotes to ensure these are treated as strings, not booleans.
    """
    Yes = "Yes"
    No = "No"


class YesNoConditionalEnum(str, Enum):
    """
    Controlled vocabulary for fields with "Yes", "No", or "Conditional" values. Use quotes to ensure these are treated as strings, not booleans.
    """
    Yes = "Yes"
    No = "No"
    Conditional = "Conditional"


class YesNoUnknownEnum(str, Enum):
    """
    Controlled vocabulary for fields with "Yes", "No", or "Unknown" values. Use quotes to ensure these are treated as strings, not booleans.
    """
    Yes = "Yes"
    No = "No"
    Unknown = "Unknown"


class YesNoUnknownNotApplicableEnum(str, Enum):
    """
    Controlled vocabulary for fields with "Yes", "No", "Unknown", or "not_applicable" values. Use quotes to ensure these are treated as strings, not booleans.
    """
    Yes = "Yes"
    No = "No"
    Unknown = "Unknown"
    not_applicable = "not_applicable"


class YesNoPendingUnknownEnum(str, Enum):
    """
    Controlled vocabulary for fields with "Yes", "No", "Pending_Review", or "Unknown" values. Use quotes to ensure these are treated as strings, not booleans.
    """
    Yes = "Yes"
    No = "No"
    Pending_Review = "Pending_Review"
    Unknown = "Unknown"


class ExportControlBasisEnum(str, Enum):
    """
    Controlled vocabulary for the basis of the export control classification of the dataset.
    """
    ITAR = "ITAR"
    EAR = "EAR"
    DOE_Nuclear_Export_Control = "DOE_Nuclear_Export_Control"
    Other = "Other"
    not_applicable = "not_applicable"


class ForeignNationalAccessStatusEnum(str, Enum):
    """
    Controlled vocabulary for Governance-facing outcome field indicating whether foreign national access is allowed, restricted, prohibited, or conditional, based on the combined effect of applicable export, classification, dissemination, agreement, or other source-authoritative constraints.
    """
    Allowed = "Allowed"
    Restricted = "Restricted"
    Prohibited = "Prohibited"
    Conditional = "Conditional"
    Unknown = "Unknown"


class PrivacyControlBasisEnum(str, Enum):
    """
    Controlled vocabulary for the basis of the privacy control classification of the dataset, based on applicable regulations, policies, or standards.
    """
    HIPPA = "HIPPA"
    Privacy_Act = "Privacy_Act"
    Human_Subjects = "Human_Subjects"
    Other_Regulated_Privacy = "Other_Regulated_Privacy"
    Site_Specific = "Site_Specific"
    not_applicable = "not_applicable"


class IPRestrictionTypeEnum(str, Enum):
    """
    Controlled vocabulary for the type of IP-based access restriction applied to the dataset.
    """
    Proprietary = "Proprietary"
    Limited_Rights = "Limited_Rights"
    Restricted_Rights = "Restricted_Rights"
    Government_Purpose_Rights = "Government_Purpose_Rights"
    Unlimited_Rights = "Unlimited_Rights"
    Third_Party_Licensed = "Third_Party_Licensed"
    None_ = "None"


class AgreementTypeEnum(str, Enum):
    """
    Controlled vocabulary for the type of agreement required for access to the dataset.
    """
    DUA = "DUA"
    CRADA = "CRADA"
    MOU = "MOU"
    NDA = "NDA"
    LICENSE = "LICENSE"
    WFO = "WFO"
    OTHER = "OTHER"


class PublicReleaseStatusEnum(str, Enum):
    """
    Controlled vocabulary for the public release status of the dataset,  indicating whether it has been approved for public release and sharing.
    """
    Approved = "Approved"
    Pending = "Pending"
    Not_Approved = "Not_Approved"
    Requires_STI_Review = "Requires_STI_Review"


class RecordStatusEnum(str, Enum):
    """
    Controlled vocabulary for the records status of the dataset,  indicating whether it is considered a record that must be retained according to applicable records management policies and regulations.
    """
    Federal_Record = "Federal_Record"
    Contractor_Record = "Contractor_Record"
    Non_Record = "Non_Record"
    Mixed = "Mixed"
    Unknown = "Unknown"



class NamedThing(ConfiguredBaseModel):
    """
    Abstract base class providing identity and human-readable metadata.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })


class GenesisDatacardClass(ConfiguredBaseModel):
    """
    Top-level Genesis datacard document container. This is the root class for all datacard documents.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'If supports_accessibility is Yes, then '
                                   'accessibility must be present.',
                    'postconditions': {'slot_conditions': {'accessibility': {'name': 'accessibility',
                                                                             'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'supports_accessibility': {'equals_string': 'Yes',
                                                                                     'name': 'supports_accessibility'}}}},
                   {'description': 'If supports_interoperability is "Yes", then '
                                   'interoperability must be present."',
                    'postconditions': {'slot_conditions': {'interoperability': {'name': 'interoperability',
                                                                                'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'supports_interoperability': {'equals_string': 'Yes',
                                                                                        'name': 'supports_interoperability'}}}},
                   {'description': 'If supports_reusability is "Yes", then reusability '
                                   'must be present."',
                    'postconditions': {'slot_conditions': {'reusability': {'name': 'reusability',
                                                                           'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'supports_reusability': {'equals_string': 'Yes',
                                                                                   'name': 'supports_reusability'}}}},
                   {'description': 'If supports_governed_use is "Yes", then '
                                   'governed_use must be present."',
                    'postconditions': {'slot_conditions': {'governed_use': {'name': 'governed_use',
                                                                            'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'supports_governed_use': {'equals_string': 'Yes',
                                                                                    'name': 'supports_governed_use'}}}},
                   {'description': 'If supports_ai_usability is "Yes", then '
                                   'ai_usability must be present."',
                    'postconditions': {'slot_conditions': {'ai_usability': {'name': 'ai_usability',
                                                                            'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'supports_ai_usability': {'equals_string': 'Yes',
                                                                                    'name': 'supports_ai_usability'}}}}],
         'slot_usage': {'accessibility': {'name': 'accessibility', 'required': False},
                        'ai_usability': {'name': 'ai_usability', 'required': False},
                        'discoverability': {'name': 'discoverability',
                                            'required': True},
                        'governed_use': {'name': 'governed_use', 'required': False},
                        'interoperability': {'name': 'interoperability',
                                             'required': False},
                        'reusability': {'name': 'reusability', 'required': False},
                        'supports_accessibility': {'name': 'supports_accessibility',
                                                   'required': True},
                        'supports_ai_usability': {'name': 'supports_ai_usability',
                                                  'required': True},
                        'supports_discoverability': {'name': 'supports_discoverability',
                                                     'required': True},
                        'supports_governed_use': {'name': 'supports_governed_use',
                                                  'required': True},
                        'supports_interoperability': {'name': 'supports_interoperability',
                                                      'required': True},
                        'supports_reusability': {'name': 'supports_reusability',
                                                 'required': True}},
         'tree_root': True})

    supports_discoverability: YesNoEnum = Field(default=..., description="""\"Yes\" | \"No\" - \"Yes\" is required for all datacards to indicate whether the dataset described in the datacard is intended to be discoverable in catalogs and repositories, to support basic findability. Indicates whether the dataset described in the datacard is intended to be discoverable in catalogs and repositories, to support basic findability.
This is a high-level indication of whether the dataset is intended to be discoverable,  and does not necessarily indicate that the dataset is currently discoverable or that it meets all criteria for discoverability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'], 'in_subset': ['required']} })
    supports_accessibility: YesNoEnum = Field(default=..., description="""\"Yes\" | \"No\" - Indicates whether the dataset described in the datacard is intended to be shared or accessed by others, whether internally within a project or organization, with external collaborators, or publicly.
This is a high-level indication of whether the dataset is intended to be accessible,  and does not necessarily indicate that the dataset is currently accessible or that it meets all criteria for accessibility.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'], 'in_subset': ['required']} })
    supports_interoperability: YesNoEnum = Field(default=..., description="""\"Yes\" | \"No\" - Indicates whether the dataset described in the datacard is intended to be interoperable, meaning it is intended to be integrated with other datasets or systems, or used in combination with other datasets.
This is a high-level indication of whether the dataset is intended to be interoperable,  and does not necessarily indicate that the dataset is currently interoperable or that it meets all criteria for interoperability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'], 'in_subset': ['required']} })
    supports_reusability: YesNoEnum = Field(default=..., description="""\"Yes\" | \"No\" - Indicates whether the dataset described in the datacard is intended to be reusable, meaning it is intended to be reused by others for the same or different purposes.
This is a high-level indication of whether the dataset is intended to be reusable,  and does not necessarily indicate that the dataset is currently reusable or that it meets all criteria for reusability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'], 'in_subset': ['required']} })
    supports_governed_use: YesNoEnum = Field(default=..., description="""\"Yes\" | \"No\" - Indicates whether the dataset described in the datacard is intended to be shared or accessed under specific governance or oversight, such as datasets that are subject to security controls, export control, IRB oversight, or other types of formal review and approval processes.
This is a high-level indication of whether the dataset is intended to be shared or accessed under specific governance or oversight,  and does not necessarily indicate that the dataset is currently shared or accessed under specific governance or oversight, or that it meets all criteria for governed use.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'], 'in_subset': ['required']} })
    supports_ai_usability: YesNoEnum = Field(default=..., description="""\"Yes\" | \"No\" - Indicates whether the dataset described in the datacard is intended to be used for AI training, evaluation, or other AI-related purposes.
This is a high-level indication of whether the dataset is intended to be used for AI purposes,  and does not necessarily indicate that the dataset is currently used for AI purposes or that it meets all criteria for AI usability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'], 'in_subset': ['required']} })
    discoverability: DiscoverabilityClass = Field(default=..., description="""Metadata fields that support the discoverability of the dataset, which is a key aspect of the FAIR principles and essential for enabling users to find and access the dataset in catalogs and repositories.
These fields provide critical information about the dataset that can enhance its discoverability and help users understand its relevance and suitability for their needs.
The discoverability capability is required for all datacards to support basic findability in catalogs and repositories, but the specific fields""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'],
         'in_subset': ['discoverability_required']} })
    accessibility: Optional[AccessibilityClass] = Field(default=None, description="""Metadata fields that support the accessibility of the dataset, which is a key aspect of the FAIR principles and essential for enabling users to access and use the dataset.
These fields provide critical information about how to access the dataset, including any restrictions or requirements for access, which can enhance accessibility and support reuse of the dataset by others.
The accessibility capability is required for datacards of datasets that are intended to be shared or accessed by others, whether internally within a project or organization, with external collaborators, or publicly.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'], 'in_subset': ['accessibility_required']} })
    interoperability: Optional[InteroperabilityClass] = Field(default=None, description="""Metadata fields that support the interoperability of the dataset, which is a key aspect of the FAIR principles and essential for enabling users to integrate the dataset with other datasets or systems, or use it in combination with other datasets.
These fields provide critical information about the meaning, data representation and structure, provenance, related resources and integrity of the dataset that can enhance interoperability and support integration with other datasets or systems.
The interoperability capability is required for datacards of datasets that are intended to be interoperable, meaning they are intended to be integrated with other datasets or systems, or used in combination with other datasets.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'],
         'in_subset': ['interoperability_required']} })
    reusability: Optional[ReusabilityClass] = Field(default=None, description="""Metadata fields that support the reusability of the dataset, which is a key aspect of the FAIR principles and essential for enabling users to reuse the dataset for the same or different purposes.
These fields provide critical information about the authorship, license, stewardship, and data quality of the dataset that can enhance reuse and support informed decision-making by users about whether and how to reuse the dataset for a particular purpose.
The reusability capability is required for datacards of datasets that are intended to be reusable, meaning they are intended to be reused by others for the same or different purposes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'], 'in_subset': ['reusability_required']} })
    governed_use: Optional[GovernedUseClass] = Field(default=None, description="""Metadata fields that support the governed use of the dataset, which is essential for ensuring that the dataset is shared and accessed in compliance with applicable regulations, policies, and ethical considerations, and for enabling responsible use of the dataset by others. These fields provide critical information about the governance and oversight for the dataset, which can enhance responsible sharing and use of the dataset by others. The governed_use capability is required for datacards of datasets that are intended to be shared or accessed  under specific governance or oversight, such as datasets that are subject to security controls,  export control, or other types of formal review and approval processes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'], 'in_subset': ['governed_use_required']} })
    ai_usability: Optional[AIUsabilityClass] = Field(default=None, description="""Metadata fields that support the AI usability of the dataset, which is essential for enabling responsible use of the dataset for AI purposes by others.
These fields provide critical information about the allowed ai use for AI purposes, as well as  any restrictions, biases, risks, safety considerations, and other factors related to using the dataset  for AI purposes that can enhance responsible use of the dataset for AI purposes by others.
The ai_usability capability is required for datacards of datasets  that are intended to be used for AI training, evaluation, or other AI-related purposes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GenesisDatacardClass'], 'in_subset': ['ai_usability_required']} })

    @field_validator('supports_discoverability')
    def pattern_supports_discoverability(cls, v):
        pattern=re.compile(r"Yes")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid supports_discoverability format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid supports_discoverability format: {v}"
            raise ValueError(err_msg)
        return v


class DiscoverabilityClass(ConfiguredBaseModel):
    """
    Metadata elements that enhance the discoverability of this datacard and dataset,  such as identification, categorization, release status, contacts, authors, sensitivity and workflow information.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'At least one author is required when '
                                   'release_status = Approved',
                    'postconditions': {'slot_conditions': {'authors': {'name': 'authors',
                                                                       'required': True}}},
                    'preconditions': {'slot_conditions': {'release_status': {'equals_string': 'Approved',
                                                                             'name': 'release_status'}}}},
                   {'description': 'At least one author is required when '
                                   'release_status = Published.',
                    'postconditions': {'slot_conditions': {'authors': {'name': 'authors',
                                                                       'required': True}}},
                    'preconditions': {'slot_conditions': {'release_status': {'equals_string': 'Published',
                                                                             'name': 'release_status'}}}},
                   {'description': 'publisher is required when release_status = '
                                   'Approved or Published.',
                    'postconditions': {'slot_conditions': {'dataset_publisher': {'name': 'dataset_publisher',
                                                                                 'required': True}}},
                    'preconditions': {'slot_conditions': {'release_status': {'in_subset': ['Approved',
                                                                                           'Published'],
                                                                             'name': 'release_status'}}}}],
         'slot_usage': {'additional_contacts': {'name': 'additional_contacts',
                                                'required': False},
                        'authors': {'name': 'authors', 'required': True},
                        'contact': {'name': 'contact', 'required': True},
                        'contributors': {'name': 'contributors', 'required': False},
                        'datacard': {'name': 'datacard', 'required': True},
                        'dataset_description': {'name': 'dataset_description',
                                                'required': True},
                        'dataset_publisher': {'name': 'dataset_publisher',
                                              'required': False},
                        'facilities': {'name': 'facilities', 'required': False},
                        'identification': {'name': 'identification', 'required': True},
                        'product_type': {'name': 'product_type', 'required': True},
                        'release_status': {'name': 'release_status', 'required': True},
                        'research_organizations': {'name': 'research_organizations',
                                                   'required': True},
                        'sensitivity': {'name': 'sensitivity', 'required': True},
                        'sponsor_organizations': {'name': 'sponsor_organizations',
                                                  'required': True},
                        'sponsoring_doe_program_office': {'name': 'sponsoring_doe_program_office',
                                                          'required': False},
                        'sponsoring_doe_subprogram': {'name': 'sponsoring_doe_subprogram',
                                                      'required': False},
                        'workflow': {'name': 'workflow', 'required': True}}})

    datacard: DataCardClass = Field(default=..., description="""Metadata about the datacard itself (not the dataset),  including its sensitivity, creation method, and change log.\"""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['prov:Entity'], 'domain_of': ['DiscoverabilityClass']} })
    identification: DatasetIdentificationClass = Field(default=..., description="""Section of Level 1 metadata elements that identify and provide basic information about the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_required']} })
    dataset_description: DatasetDescriptionClass = Field(default=..., description="""Required, essential metadata fields that provide a high-level description of the dataset,  including its science domain, a description, and keywords.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_required']} })
    product_type: ProductTypeEnum = Field(default=..., description="""Extended from OSTI Product Types.  Select the single best-fit from controlled vocabulary: Technical_Report | Paper_or_Proceedings | Journal_Article | Softare_Manual | Data | Collection | Computer_Related | Model | Agent""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_required']} })
    dataset_type: Optional[DatasetTypeEnum] = Field(default=None, description="""OSTI DOE Data Explorer type code. Select the single best-fit from the ObjectTypeEnum controlled vocabulary (e.g., GD for genomic data, IM for image, ND for numeric data).""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_if_applicable']} })
    release_status: ReleaseStatusEnum = Field(default=..., description="""The release status of the dataset, following a controlled vocabulary: Draft | Under_Review | Approved | Published | Deprecated | Approved | Published | Deprecated
This provides important context about the lifecycle stage of the dataset  and can inform users about its readiness for use.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_required']} })
    dataset_publisher: Optional[PublisherClass] = Field(default=None, description="""The publisher of the dataset, described by a name and ror_id if available.
Required for datasets with release_status = approved | published This provides important provenance information about the dataset and can inform trust and maintenance practices.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass']} })
    contact: ContactClass = Field(default=..., description="""Contact information for questions about access to or use of this dataset. This can provide users with a direct point of contact for inquiries about the dataset, which can facilitate communication and support responsible use of the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_required']} })
    additional_contacts: Optional[list[ContactClass]] = Field(default=None, description="""Additional contacts (e.g., instrument PI, data steward). Can include person or organization agent_types for the Contact.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_if_applicable']} })
    sponsor_organizations: list[SponsorOrganizationClass] = Field(default=..., description="""Organizations that funded or sponsored this dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_required']} })
    sponsoring_doe_program_office: Optional[str] = Field(default=None, description="""The DOE program office that sponsored or funded the research that produced this dataset. E.g., 'Office of Science' or 'National Nuclear Security Administration'""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_if_applicable']} })
    sponsoring_doe_subprogram: Optional[str] = Field(default=None, description="""The DOE subprogram that sponsored or funded the research that produced this dataset. E.g., 'Advanced Scientific Computing Research' or 'Predictive Science Academic Alliance Program'""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_if_applicable']} })
    research_organizations: list[ResearchOrganizationClass] = Field(default=..., description="""Organizations that created or collected the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_required']} })
    facilities: Optional[list[FacilityClass]] = Field(default=None, description="""User facilities, HPC centers, or research infrastructure used to collect, process, or store the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_if_applicable']} })
    sensitivity: SensitivityClass = Field(default=..., description="""Metadata fields that capture the sensitivity of the datacard and the dataset it describes, which is critical for ensuring proper handling and access controls based on the sensitivity of the asset.
These fields provide important context about the sensitivity of the dataset,  which can inform filtering and discovery in catalogs,  but authoritative source markings and metadata fields should be used for access control and governance decisions.
NOTE: Sensitivity terminology is still under Genesis governance review. Vocabulary may evolve.""", json_schema_extra = { "linkml_meta": {'aliases': ['datacard_sensitivity', 'Genesis Sensitivity'],
         'domain_of': ['DiscoverabilityClass', 'DataCardClass'],
         'in_subset': ['discoverability_required']} })
    workflow: WorkflowClass = Field(default=..., description="""Workflow & Lifecycle Block:
Describes the technical and processing lifecycle position of the dataset. 
discoverability.workflow.state   — describes the technical/processing lifecycle position of the data itself (raw → archived)
reuasability.release_status   — describes the publication and governance state of the dataset record (draft → deprecated)
These should be logically consistent. Common alignments:
discoverability.workflow.state=raw|processing|qa|analysis → reuasability.release_status=draft
discoverability.workflow.state=review                     → reuasability.release_status=under_review
discoverability.workflow.state=embargo|published          → reuasability.release_status=approved|published discoverability.workflow.state=archived                   → reuasability.release_status=deprecated|published""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_required']} })
    authors: list[AgentClass] = Field(default=..., description="""At least one author required when release_status = approved | published.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_required'],
         'list_elements_unique': True} })
    contributors: Optional[list[AgentClass]] = Field(default=None, description="""Supporting contributors who are not primary authors. e.g., sample preparers, annotators, reviewers, submitters. For draft or in-workflow data, populate with known contributors.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiscoverabilityClass'],
         'in_subset': ['discoverability_if_applicable'],
         'list_elements_unique': True} })


class AccessibilityClass(ConfiguredBaseModel):
    """
    Metadata elements that describe the accessibility of this dataset,  such as access policy, and dataset scale information. This is important for users to understand how they can access the dataset and any restrictions that may apply.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'access': {'name': 'access', 'required': True},
                        'access_policy': {'name': 'access_policy', 'required': True},
                        'dataset_scale': {'name': 'dataset_scale', 'required': False}}})

    access_policy: AccessPolicyClass = Field(default=..., description="""Access Policy block: Describes who can access this dataset and under what conditions. access_policy.sensitivity_tier describes the dataset's access sensitivity — the same subject as security.sensitivity_tier above, reproduced here for access control systems that evaluate this block independently.  It will typically carry the same value as security.sensitivity_tier. Both are independent of datacard.sensitivity_tier. See NOTE ON SENSITIVITY TIERS above. Required for Genesis Dataset Readiness Model level 2 and above, and when release_status is published.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessibilityClass'], 'in_subset': ['accessibility_required']} })
    access: AccessClass = Field(default=..., description="""Access Endpoints information.  This can include the current location/landingpage, and intended repository information, such as access instructions and APIs. Intended to provide information on how to access the dataset for humans and machines.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessibilityClass'], 'in_subset': ['accessibility_required']} })
    dataset_scale: Optional[DatasetScaleClass] = Field(default=None, description="""A block to describe the scale of the dataset, records (and units), bytes (compressed and uncompressed).
This can provide important information about the size and scope of the dataset, which can inform users about the computational resources that may be required to work with it effectively.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:size', 'dcterms:extent', 'datacite:size'],
         'domain_of': ['AccessibilityClass'],
         'in_subset': ['accessibility_if_applicable']} })


class InteroperabilityClass(ConfiguredBaseModel):
    """
    Metadata elements that describe the interoperability of this dataset,  such as context of data collection, data structure, provenance, related resource, schema, and integrity. This is important for users to understand how they can use the dataset and what tools or software they may need to work with it.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'data_structure': {'name': 'data_structure', 'required': True},
                        'dates': {'name': 'dates', 'required': False},
                        'domain_metadata': {'name': 'domain_metadata',
                                            'required': False},
                        'provenance': {'name': 'provenance', 'required': True},
                        'related_resources': {'name': 'related_resources',
                                              'required': False},
                        'semantic_layer': {'name': 'semantic_layer',
                                           'required': False}}})

    data_structure: DataStructureClass = Field(default=..., description="""Placeholder for additional dataset characteristics metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['InteroperabilityClass'],
         'in_subset': ['interoperability_required']} })
    provenance: ProvenanceClass = Field(default=..., description="""Provenance information about the dataset, including its origin, history,  and any transformations/processing it has undergone.
This can provide important context for understanding the dataset and can inform users  about its reliability and suitability for their intended use and facilitate reuse and reproducibility.""", json_schema_extra = { "linkml_meta": {'domain_of': ['InteroperabilityClass'],
         'in_subset': ['interoperability_required']} })
    dates: Optional[DatesClass] = Field(default=None, description="""Class slot for important dataset dates metadata (e.g., collection, issued, modified dates).""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:ItemList'],
         'domain_of': ['InteroperabilityClass'],
         'in_subset': ['interoperability_if_applicable']} })
    semantic_layer: Optional[SemanticLayerClass] = Field(default=None, description="""Required for Genesis Readiness Framework Level 3 datasets intended for federated or cross-domain use. 
Populate schema_url at minimum.
Contains elements to provide a machine-readable semantic layer for the dataset, which can enhance discoverability, interoperability, and usability of the data for AI/ML applications.""", json_schema_extra = { "linkml_meta": {'domain_of': ['InteroperabilityClass'],
         'in_subset': ['interoperability_if_applicable']} })
    related_resources: Optional[RelatedResourcesClass] = Field(default=None, description="""Related Resources: Links to related datasets, publications, software, and AI models. 
The base relationship vocabulary for relations (RelationshipTypeEnum) is shared across all resource types;  is_derived_from | is_based_on | is_part_of | has_part | references | other
ExtendedRelationshipEnum (software and AI models): used_to_create | used_to_process | used_to_analyze | trained_on | evaluated_on""", json_schema_extra = { "linkml_meta": {'domain_of': ['InteroperabilityClass'],
         'in_subset': ['interoperability_if_applicable']} })
    domain_metadata: Optional[DomainMetadataClass] = Field(default=None, description="""A block for capturing domain-specific metadata that may be relevant for understanding and using the dataset effectively.
This can include fields that are specific to certain scientific domains or types of data,  which can provide users with important context and insights about the dataset.
Domain-specific metadata fields supplement the Discoverable card  and should not replace the common metadata expected by the datacard.""", json_schema_extra = { "linkml_meta": {'domain_of': ['InteroperabilityClass'],
         'in_subset': ['interoperability_if_applicable']} })


class ReusabilityClass(ConfiguredBaseModel):
    """
    Metadata elements that describe the reusability of this dataset,  such as license and rights, stewardship, data quality, integrity, and citation information.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'additional_licenses': {'name': 'additional_licenses',
                                                'required': False},
                        'citation': {'name': 'citation', 'required': False},
                        'data_quality': {'name': 'data_quality', 'required': True},
                        'integrity': {'name': 'integrity', 'required': True},
                        'license': {'name': 'license', 'required': False},
                        'stewardship': {'name': 'stewardship', 'required': False}}})

    license: Optional[LicenseClass] = Field(default=None, description="""Block to capture a license under which the dataset is released. This indicates the legal permissions and restrictions associated with using the dataset and can inform users about how they are allowed to use, share, and build upon the data. A public/open license is not always the governing instrument for use, some controlled datasets may not have an SPDX-style reuse license at all, and use may instead be governed by contract, agreement, institutional review, or repository policy.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ReusabilityClass'], 'in_subset': ['reusability_if_applicable']} })
    additional_licenses: Optional[list[LicenseClass]] = Field(default=None, description="""Additional licenses governing this dataset, if multiple licenses apply. This can provide users with a more complete understanding of the legal permissions and restrictions associated with using the dataset, especially in cases where different parts of the dataset may be subject to different licenses.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ReusabilityClass'], 'in_subset': ['reusability_if_applicable']} })
    stewardship: Optional[StewardshipClass] = Field(default=None, description="""Stewardship & Versioning Block to capture information about dataset maintenance, updates, versioning, and reviews.
This can provide users with important information about how the dataset is maintained and updated over time, which can inform their confidence in the dataset's quality and reliability and can help them understand how the dataset evolves over time.
NOTE ON VERSIONING: Three fields work together to describe versioning:
discoverability.identification.version        — the version number of this dataset
discoverability.identification.supersedes /
discoverability.identification.superseded_by  — links to prior and successor versions
reusability.stewardship.versioning_strategy — how versioning is managed over time""", json_schema_extra = { "linkml_meta": {'domain_of': ['ReusabilityClass'], 'in_subset': ['reusability_if_applicable']} })
    data_quality: DataQualityClass = Field(default=..., description="""Block containing elements to provide information about the quality of the dataset,  including any known issues, limitations, or uncertainties that may affect its suitability for AI/ML applications.
This can provide users with important context about the dataset's quality and reliability, which can inform their decisions about using the dataset in AI/ML workflows""", json_schema_extra = { "linkml_meta": {'domain_of': ['ReusabilityClass'], 'in_subset': ['reusability_required']} })
    citation: Optional[CitationClass] = Field(default=None, description="""Citation information for the dataset, if applicable. Required when release_status = approved | published.
This can provide users with the necessary information to properly cite  the dataset in their work, which can facilitate proper attribution and recognition  for the creators and maintainers of the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ReusabilityClass'], 'in_subset': ['reusability_if_applicable']} })
    integrity: IntegrityClass = Field(default=..., description="""Contains elements describing checksums enable automated validation of data integrity after transfer or storage.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ReusabilityClass'], 'in_subset': ['reusability_if_applicable']} })


class GovernedUseClass(ConfiguredBaseModel):
    """
    Metadata elements that describe the governed use of this dataset,  such as compliance information, use governance, and review history. This is important for users to understand any compliance requirements, restrictions, or governance processes that apply to the dataset, as well as the history of any formal reviews it has undergone.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'compliance': {'name': 'compliance', 'required': True},
                        'non_sensitivity_governance_metadata': {'name': 'non_sensitivity_governance_metadata',
                                                                'required': True},
                        'review_provenance_companion': {'name': 'review_provenance_companion',
                                                        'required': False},
                        'use_governance': {'name': 'use_governance', 'required': True}}})

    use_governance: UseGovernanceClass = Field(default=..., description="""Information block to guide appropriate use and prevent misuse of this dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GovernedUseClass'], 'in_subset': ['governed_use_required']} })
    non_sensitivity_governance_metadata: NonSensitivityGovMetadataClass = Field(default=..., description="""Governance-relevant metadata that may affect sharing/use decisions but is not part of the source sensitivity/marking block itself.
This can include information about any governance considerations or requirements that are relevant to the dataset,  which can inform users about responsible use and any potential limitations or restrictions on the dataset.
Includes fields for export control, privacy, and data rights.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GovernedUseClass'], 'in_subset': ['governed_use_required']} })
    compliance: ComplianceClass = Field(default=..., description="""Populate when release_status = under_review | approved | published.
Acts as a holder for confirmation of compliance with relevant policies, standards, and requirements for the dataset.
This can provide users with important information about the dataset's adherence to relevant policies and standards,  which can inform their confidence in the dataset's quality and reliability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GovernedUseClass'],
         'in_subset': ['interoperability_if_applicable']} })
    review_provenance_companion: Optional[list[SpecificReviewClass]] = Field(default=None, description="""Reviews or assessments of the dataset, if any. Running history of all formal reviews. Add one entry per review stage in chronological order. Do not overwrite earlier entries when adding new ones.
This block extends the Genesis Sensitivity V2 review_provenance_companion (which only accepts a single review) by allowing multiple review records to be captured in a structured format,  which is especially useful for datasets that have undergone multiple reviews or have complex provenance histories.
This can provide users with insights into the quality and reliability of the dataset  based on expert evaluations or user feedback, which can inform their decisions about using the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GovernedUseClass'], 'in_subset': ['governed_use_if_applicable']} })


class AIUsabilityClass(ConfiguredBaseModel):
    """
    Metadata elements that describe the usability of this dataset for AI applications,  such as suitability for training, evaluation, or inference, and any relevant characteristics that may affect its use in AI contexts. This is important for users who are specifically interested in using the dataset for AI applications, as it provides information about how well-suited the dataset is for those purposes and any considerations they should keep in mind.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'ai_usage': {'name': 'ai_usage', 'required': True}}})

    ai_usage: AIUsageClass = Field(default=..., description="""Describes whether and how this dataset may be used in AI/ML workflows using fields from AIUsageClass. 
Be explicit — these fields are read by automated pipeline tooling.
This can provide important information about the suitability of the dataset for 
AI/ML applications and can inform users about any specific considerations or restrictions related to using the dataset in AI/ML workflows. """, json_schema_extra = { "linkml_meta": {'domain_of': ['AIUsabilityClass'], 'in_subset': ['ai_usability_required']} })


class DataCardClass(ConfiguredBaseModel):
    """
    Datacard Metadata. This class captures the core metadata elements that describe the document itself, not the dataset. It includes information such as the datacard's version, overall sensitivity, source marking, the creation of the datacard, and a change log for tracking updates to the datacard over time.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': False,
         'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    template_version: str = Field(default="1.0.0", description="""The version of the datacard template used to create this datacard.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataCardClass'],
         'ifabsent': 'string(1.0.0)',
         'in_subset': ['discoverability_required']} })
    datacard_version: str = Field(default="1.0.0", description="""Increment when the datacard is meaningfully updated. Use semantic versioning: MAJOR.MINOR.PATCH e.g., 1.0 → 1.1 for content updates; 1.x -> 2.0 for structural changes""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataCardClass', 'ChangeLogEntryClass'],
         'ifabsent': 'string(1.0.0)',
         'in_subset': ['discoverability_required']} })
    filename: str = Field(default=..., description="""The filename of the datacard document, follow naming convention: \"genesis_datacard_${SNAKE_CASE_DATASET_NAME}$.md\"""", json_schema_extra = { "linkml_meta": {'aliases': ['file_name', 'datacard_filename', 'datacard_file_name'],
         'domain_of': ['DataCardClass'],
         'in_subset': ['discoverability_required']} })
    language: str = Field(default="en", description="""The language of the datacard content, following ISO 639-1 codes (e.g., 'en' for English).""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataCardClass', 'DataStructureClass'],
         'exact_mappings': ['schema:inLanguage',
                            'dcterms:language',
                            'datacite:language'],
         'ifabsent': 'string(en)',
         'in_subset': ['discoverability_required']} })
    id: IdentifierClass = Field(default=..., description="""A unique identifier for the datacard document itself, following the format: \"doi: distinct from the dataset identifier.
Assign if the datacard is registered in a catalog or repository independently of the dataset.""", json_schema_extra = { "linkml_meta": {'aliases': ['identifier',
                     'datacard_id',
                     'datacard_identifier',
                     'PID',
                     'datacard_pid'],
         'broad_mappings': ['schema:identifier',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['DataCardClass'],
         'in_subset': ['discoverability_if_applicable']} })
    sensitivity: Optional[SensitivityClass] = Field(default=None, description="""Metadata fields that capture the sensitivity of the datacard and the dataset it describes, which is critical for ensuring proper handling and access controls based on the sensitivity of the asset.
These fields provide important context about the sensitivity of the dataset,  which can inform filtering and discovery in catalogs,  but authoritative source markings and metadata fields should be used for access control and governance decisions.
NOTE: Sensitivity terminology is still under Genesis governance review. Vocabulary may evolve.""", json_schema_extra = { "linkml_meta": {'aliases': ['datacard_sensitivity', 'Genesis Sensitivity'],
         'domain_of': ['DiscoverabilityClass', 'DataCardClass'],
         'in_subset': ['discoverability_required']} })
    creation_method: DatacardCreationMethodEnum = Field(default=..., description="""The method by which the datacard was created, following a controlled vocabulary (e.g., manual, automated, templated).
This provides context on how the datacard was generated and can inform trust and maintenance practices.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataCardClass'], 'in_subset': ['discoverability_required']} })
    created_date: date = Field(default=..., description="""The date the datacard was first created, in ISO 8601 format (YYYY-MM-DD).
This provides temporal context for the datacard and can be used for tracking its age and relevance.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataCardClass'], 'in_subset': ['discoverability_required']} })
    updated_date: Optional[date] = Field(default=None, description="""The date the datacard was last updated, in ISO 8601 format (YYYY-MM-DD). Date of most recent update; revise on every change to the datacard, including minor edits and version updates.
This provides temporal context for the datacard and can be used for tracking its currency and maintenance.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataCardClass'], 'in_subset': ['discoverability_if_applicable']} })
    change_log: list[ChangeLogEntryClass] = Field(default=..., description="""Running history of meaningful changes to this datacard. Add a new entry every time the datacard is updated.
Do not overwrite or delete prior entries.
If there have been no changes since creation, include a single entry with the creation date and the summary 'Initial creation'.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataCardClass'], 'in_subset': ['discoverability_required']} })
    created_by: list[CreatorClass] = Field(default=..., description="""All individuals, organizations, AI models, or software tools that created or updated this datacard.  List in chronological order of the contribution — e.g., if an AI model generated the initial draft and a person then edited it, list the AI model first followed by the person. This provides important provenance information about the datacard and can inform trust and maintenance practices.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataCardClass'], 'in_subset': ['discoverability_required']} })

    @field_validator('template_version')
    def pattern_template_version(cls, v):
        pattern=re.compile(r"^\d+\.\d+(\.\d+)?$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid template_version format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid template_version format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('datacard_version')
    def pattern_datacard_version(cls, v):
        pattern=re.compile(r"^\d+\.\d+(\.\d+)?$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid datacard_version format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid datacard_version format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('filename')
    def pattern_filename(cls, v):
        pattern=re.compile(r"^genesis_datacard_[a-z0-9]+(?:_[a-z0-9]+)*\.(md|ya?ml)$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid filename format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid filename format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('language')
    def pattern_language(cls, v):
        pattern=re.compile(r"^[a-z]{2}$|^not_applicable$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid language format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid language format: {v}"
            raise ValueError(err_msg)
        return v


class PublicationIdentifierClass(ConfiguredBaseModel):
    """
    A section of metadata elements that provide a collection of publication identifiers.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'relationship': {'name': 'relationship', 'required': True},
                        'type': {'identifier': True, 'name': 'type', 'required': True},
                        'value': {'name': 'value', 'required': True}}})

    type: IdentifierTypeEnum = Field(default=..., description="""The type of the Identifer (e.g., DOI, UUID, ARK), following a controlled vocabulary of identifier types.
Assign if the datacard has an identifier; required if 'id' is provided.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['datacite:identifierType'],
         'domain_of': ['PublicationIdentifierClass', 'IdentifierClass'],
         'in_subset': ['interoperability_if_applicable']} })
    value: str = Field(default=..., description="""The value of the identifier (e.g., \"10.1234/abcd\"), following the format specified by the 'type' field.
Assign if the datacard has an identifier; required if 'id' is provided.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:identifier',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['PublicationIdentifierClass', 'IdentifierClass', 'AnyValue']} })
    relationship: RelationshipTypeEnum = Field(default=..., description="""Relationship to other datasets or resources, if any.
E.g.s, \"is_derived_from\", \"is_based_on\", \"is_part_of\", \"has_part\", \"references\", \"other\"
This can include links to related datasets, publications, software, or other resources that are relevant to understanding and using the dataset effectively.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PublicationIdentifierClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DatasetClass'],
         'in_subset': ['interoperability_if_applicable']} })

    @field_validator('value')
    def pattern_value(cls, v):
        pattern=re.compile(r"^.*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid value format: {v}"
            raise ValueError(err_msg)
        return v


class IdentifierClass(ConfiguredBaseModel):
    """
    A unique identifier for an entity, following a specific format (e.g., DOI, UUID).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'type': {'name': 'type', 'required': True},
                        'value': {'name': 'value', 'required': False}}})

    type: IdentifierTypeEnum = Field(default=..., description="""The type of the Identifer (e.g., DOI, UUID, ARK), following a controlled vocabulary of identifier types.
Assign if the datacard has an identifier; required if 'id' is provided.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['datacite:identifierType'],
         'domain_of': ['PublicationIdentifierClass', 'IdentifierClass'],
         'in_subset': ['interoperability_if_applicable']} })
    value: Optional[str] = Field(default=None, description="""The value of the identifier (e.g., \"10.1234/abcd\"), following the format specified by the 'type' field.
Assign if the datacard has an identifier; required if 'id' is provided.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:identifier',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['PublicationIdentifierClass', 'IdentifierClass', 'AnyValue']} })

    @field_validator('value')
    def pattern_value(cls, v):
        pattern=re.compile(r"^.*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid value format: {v}"
            raise ValueError(err_msg)
        return v


class ChangeLogEntryClass(ConfiguredBaseModel):
    """
    An individual entry in the change log, documenting a specific change to the datacard.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'change_date': {'identifier': True,
                                        'name': 'change_date',
                                        'required': True},
                        'datacard_version': {'name': 'datacard_version',
                                             'required': True},
                        'summary': {'name': 'summary', 'required': True}}})

    change_date: str = Field(default=..., description="""The date of a specific change to the datacard, in ISO 8601 format (YYYY-MM-DD).
This provides temporal context for each change and can be used for tracking the history of the datacard.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ChangeLogEntryClass'],
         'in_subset': ['discoverability_required']} })
    datacard_version: str = Field(default="1.0.0", description="""Increment when the datacard is meaningfully updated. Use semantic versioning: MAJOR.MINOR.PATCH e.g., 1.0 → 1.1 for content updates; 1.x -> 2.0 for structural changes""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataCardClass', 'ChangeLogEntryClass'],
         'ifabsent': 'string(1.0.0)',
         'in_subset': ['discoverability_required']} })
    summary: str = Field(default=..., description="""A brief description of what was changed in a specific update to the datacard and why. Update this text for all subsequent revisions. This provides context for each change and can be used for understanding the evolution of the datacard over time. Brief description of what changed and why. e.g., \"Updated license to CC-BY-4.0\", e.g., \"Added checksum after file transfer to OSTI\", e.g., \"Corrected collection end date\",""", json_schema_extra = { "linkml_meta": {'domain_of': ['ChangeLogEntryClass'],
         'in_subset': ['discoverability_required']} })

    @field_validator('change_date')
    def pattern_change_date(cls, v):
        pattern=re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid change_date format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid change_date format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('datacard_version')
    def pattern_datacard_version(cls, v):
        pattern=re.compile(r"^\d+\.\d+(\.\d+)?$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid datacard_version format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid datacard_version format: {v}"
            raise ValueError(err_msg)
        return v


class CreatorClass(ConfiguredBaseModel):
    """
    An individual, organization, AI model, or software tool that created or updated the datacard or dataset.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'contribution_date': {'description': 'The ISO 8601 date of '
                                                             'this specific '
                                                             'contribution',
                                              'identifier': True,
                                              'name': 'contribution_date',
                                              'required': True},
                        'creator': {'description': 'Container for the agent (person, '
                                                   'organization, AI model, or '
                                                   'software tool) responsible for '
                                                   'this contribution.',
                                    'name': 'creator',
                                    'range': 'AgentClass',
                                    'required': True}}})

    contribution_date: str = Field(default=..., description="""The ISO 8601 date of this specific contribution""", json_schema_extra = { "linkml_meta": {'domain_of': ['CreatorClass']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })
    creator: AgentClass = Field(default=..., description="""Container for the agent (person, organization, AI model, or software tool) responsible for this contribution.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CreatorClass'], 'in_subset': ['discoverability_required']} })

    @field_validator('contribution_date')
    def pattern_contribution_date(cls, v):
        pattern=re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid contribution_date format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid contribution_date format: {v}"
            raise ValueError(err_msg)
        return v


class AgentClass(ConfiguredBaseModel):
    """
    An individual, organization, AI model, or software tool that created the datacard or dataset in the role indicated. AgentClass rules indicate that the selected slot must be filled in based on the agent_type, and the other three must be left blank. This allows for flexibility in representing different types of contributors while maintaining clear rules for which fields to use.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'If person is present, organization must be absent',
                    'postconditions': {'slot_conditions': {'organization': {'name': 'organization',
                                                                            'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'person': {'name': 'person',
                                                                     'value_presence': 'PRESENT'}}}},
                   {'description': 'If person is present, ai_model must be absent',
                    'postconditions': {'slot_conditions': {'ai_model': {'name': 'ai_model',
                                                                        'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'person': {'name': 'person',
                                                                     'value_presence': 'PRESENT'}}}},
                   {'description': 'If person is present, the software must be absent',
                    'postconditions': {'slot_conditions': {'software': {'name': 'software',
                                                                        'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'person': {'name': 'person',
                                                                     'value_presence': 'PRESENT'}}}},
                   {'description': 'If organization is present, person must be absent',
                    'postconditions': {'slot_conditions': {'person': {'name': 'person',
                                                                      'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'organization': {'name': 'organization',
                                                                           'value_presence': 'PRESENT'}}}},
                   {'description': 'If organization is present, ai_model must be '
                                   'absent',
                    'postconditions': {'slot_conditions': {'ai_model': {'name': 'ai_model',
                                                                        'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'organization': {'name': 'organization',
                                                                           'value_presence': 'PRESENT'}}}},
                   {'description': 'If organization is present, software must be '
                                   'absent',
                    'postconditions': {'slot_conditions': {'software': {'name': 'software',
                                                                        'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'organization': {'name': 'organization',
                                                                           'value_presence': 'PRESENT'}}}},
                   {'description': 'If ai_model is present, person must be absent',
                    'postconditions': {'slot_conditions': {'person': {'name': 'person',
                                                                      'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'ai_model': {'name': 'ai_model',
                                                                       'value_presence': 'PRESENT'}}}},
                   {'description': 'If ai_model is present, organization must be '
                                   'absent',
                    'postconditions': {'slot_conditions': {'organization': {'name': 'organization',
                                                                            'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'ai_model': {'name': 'ai_model',
                                                                       'value_presence': 'PRESENT'}}}},
                   {'description': 'If ai_model is present, software must be absent',
                    'postconditions': {'slot_conditions': {'software': {'name': 'software',
                                                                        'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'ai_model': {'name': 'ai_model',
                                                                       'value_presence': 'PRESENT'}}}},
                   {'description': 'If software is present, person must be absent',
                    'postconditions': {'slot_conditions': {'person': {'name': 'person',
                                                                      'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'software': {'name': 'software',
                                                                       'value_presence': 'PRESENT'}}}},
                   {'description': 'If software is present, organization must be '
                                   'absent',
                    'postconditions': {'slot_conditions': {'organization': {'name': 'organization',
                                                                            'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'software': {'name': 'software',
                                                                       'value_presence': 'PRESENT'}}}},
                   {'description': 'If software is present, ai_model must be absent',
                    'postconditions': {'slot_conditions': {'ai_model': {'name': 'ai_model',
                                                                        'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'software': {'name': 'software',
                                                                       'value_presence': 'PRESENT'}}}}],
         'slot_usage': {'ai_model': {'multivalued': False, 'name': 'ai_model'},
                        'organization': {'multivalued': False, 'name': 'organization'},
                        'person': {'multivalued': False, 'name': 'person'},
                        'software': {'inlined': True,
                                     'inlined_as_list': False,
                                     'multivalued': False,
                                     'name': 'software'}}})

    person: Optional[PersonClass] = Field(default=None, description="""A human individual.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AgentClass', 'ContactClass']} })
    organization: Optional[OrganizationClass] = Field(default=None, description="""An organization or group of individuals.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AgentClass']} })
    ai_model: Optional[AIModelClass] = Field(default=None, description="""An AI model.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AgentClass']} })
    software: Optional[SoftwareClass] = Field(default=None, description="""Software associated with this dataset, if any. 
This can include links to software tools, libraries, or frameworks that were used to generate, process, or analyze the dataset,  which can provide users with additional context and insights about the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AgentClass', 'RelatedResourcesClass'],
         'in_subset': ['interoperability_if_applicable']} })


class PersonClass(ConfiguredBaseModel):
    """
    A human individual.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'role': {'name': 'role', 'required': False}}})

    given_name: Optional[str] = Field(default=None, description="""The given name(s) of a person.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PersonClass']} })
    family_name: Optional[str] = Field(default=None, description="""The family name(s) of a person.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PersonClass']} })
    orcid: Optional[str] = Field(default=None, description="""The ORCID identifier for a person, in URL format (e.g., https://orcid.org/0000-0002-1825-0097).""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:sameAs',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['PersonClass'],
         'in_subset': ['discoverability_if_applicable']} })
    email: Optional[str] = Field(default=None, description="""The email address of a person.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PersonClass'], 'in_subset': ['discoverability_if_applicable']} })
    affiliation: Optional[AffiliationClass] = Field(default=None, description="""An organization with which a person is affiliated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PersonClass']} })
    role: Optional[list[RoleEnum]] = Field(default=None, description="""The role, using the CRediT taxonomy, of a type (person, organization, AI model,  or software tool) in relation to the datacard or dataset. CRediT roles include: Conceptualization, Data_Curation, Formal_Analysis, Funding_Acquisition, Investigation, Methodology, Project_Administration, Resources, Software, Supervision, Validation, Visualization, Writing_Original_Draft, Writing_Review_and_Editing. This has been extended with an Other role to capture contributions that do not fit within the CRediT taxonomy.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PersonClass',
                       'OrganizationClass',
                       'AIModelClass',
                       'SoftwareClass']} })

    @field_validator('orcid')
    def pattern_orcid(cls, v):
        pattern=re.compile(r"^https?://orcid\.org/[0-9A-Z]{4}-[0-9A-Z]{4}-[0-9A-Z]{4}-[0-9A-Z]{4}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid orcid format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid orcid format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('email')
    def pattern_email(cls, v):
        pattern=re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid email format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid email format: {v}"
            raise ValueError(err_msg)
        return v


class AffiliationClass(ConfiguredBaseModel):
    """
    An organization with which an entity is affiliated.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    ror_id: Optional[str] = Field(default=None, description="""The ROR identifier for an organization, in URL format (e.g., https://ror.org/03yrm5c26).""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:sameAs',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AffiliationClass',
                       'OrganizationClass',
                       'LocationClass',
                       'PublisherClass',
                       'SponsorOrganizationClass'],
         'in_subset': ['discoverability_if_applicable']} })

    @field_validator('ror_id')
    def pattern_ror_id(cls, v):
        pattern=re.compile(r"^https?://ror\.org/[a-z0-9]{9}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ror_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ror_id format: {v}"
            raise ValueError(err_msg)
        return v


class OrganizationClass(NamedThing):
    """
    An organization or group of individuals.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'role': {'name': 'role', 'required': False}}})

    ror_id: Optional[str] = Field(default=None, description="""The ROR identifier for an organization, in URL format (e.g., https://ror.org/03yrm5c26).""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:sameAs',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AffiliationClass',
                       'OrganizationClass',
                       'LocationClass',
                       'PublisherClass',
                       'SponsorOrganizationClass'],
         'in_subset': ['discoverability_if_applicable']} })
    role: Optional[list[RoleEnum]] = Field(default=None, description="""The role, using the CRediT taxonomy, of a type (person, organization, AI model,  or software tool) in relation to the datacard or dataset. CRediT roles include: Conceptualization, Data_Curation, Formal_Analysis, Funding_Acquisition, Investigation, Methodology, Project_Administration, Resources, Software, Supervision, Validation, Visualization, Writing_Original_Draft, Writing_Review_and_Editing. This has been extended with an Other role to capture contributions that do not fit within the CRediT taxonomy.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PersonClass',
                       'OrganizationClass',
                       'AIModelClass',
                       'SoftwareClass']} })
    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })

    @field_validator('ror_id')
    def pattern_ror_id(cls, v):
        pattern=re.compile(r"^https?://ror\.org/[a-z0-9]{9}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ror_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ror_id format: {v}"
            raise ValueError(err_msg)
        return v


class ResearchOrganizationClass(OrganizationClass):
    """
    An organization that conducted research or provided resources for the dataset. This describes the organizations that conducted research or provided resources for the dataset,  which is important for acknowledging contributions and understanding potential conflicts of interest.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'ror_id': {'description': 'The ROR ID of the research '
                                                  'organization, if available. E.g., '
                                                  'https://ror.org/02vwzrd76',
                                   'name': 'ror_id'}}})

    ror_id: Optional[str] = Field(default=None, description="""The ROR ID of the research organization, if available. E.g., https://ror.org/02vwzrd76""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:sameAs',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AffiliationClass',
                       'OrganizationClass',
                       'LocationClass',
                       'PublisherClass',
                       'SponsorOrganizationClass'],
         'in_subset': ['discoverability_if_applicable']} })
    role: Optional[list[RoleEnum]] = Field(default=None, description="""The role, using the CRediT taxonomy, of a type (person, organization, AI model,  or software tool) in relation to the datacard or dataset. CRediT roles include: Conceptualization, Data_Curation, Formal_Analysis, Funding_Acquisition, Investigation, Methodology, Project_Administration, Resources, Software, Supervision, Validation, Visualization, Writing_Original_Draft, Writing_Review_and_Editing. This has been extended with an Other role to capture contributions that do not fit within the CRediT taxonomy.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PersonClass',
                       'OrganizationClass',
                       'AIModelClass',
                       'SoftwareClass']} })
    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })

    @field_validator('ror_id')
    def pattern_ror_id(cls, v):
        pattern=re.compile(r"^https?://ror\.org/[a-z0-9]{9}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ror_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ror_id format: {v}"
            raise ValueError(err_msg)
        return v


class FacilityClass(OrganizationClass):
    """
    A facility where research was conducted or resources were provided for the dataset. This describes the facilities where research was conducted or resources were provided for the dataset,  which is important for acknowledging contributions and understanding potential conflicts of interest.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'ror_id': {'description': 'The ROR ID of the facility, if '
                                                  'available. E.g., '
                                                  'https://ror.org/02vwzrd76',
                                   'name': 'ror_id'}}})

    location: Optional[LocationClass] = Field(default=None, description="""Point location for facility-based experimental data, if applicable. description: should include the place name and, location details e.g., \"SNS Beamline 1B, Oak Ridge National Laboratory, TN, USA\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['FacilityClass'], 'in_subset': ['discoverability_if_applicable']} })
    ror_id: Optional[str] = Field(default=None, description="""The ROR ID of the facility, if available. E.g., https://ror.org/02vwzrd76""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:sameAs',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AffiliationClass',
                       'OrganizationClass',
                       'LocationClass',
                       'PublisherClass',
                       'SponsorOrganizationClass'],
         'in_subset': ['discoverability_if_applicable']} })
    role: Optional[list[RoleEnum]] = Field(default=None, description="""The role, using the CRediT taxonomy, of a type (person, organization, AI model,  or software tool) in relation to the datacard or dataset. CRediT roles include: Conceptualization, Data_Curation, Formal_Analysis, Funding_Acquisition, Investigation, Methodology, Project_Administration, Resources, Software, Supervision, Validation, Visualization, Writing_Original_Draft, Writing_Review_and_Editing. This has been extended with an Other role to capture contributions that do not fit within the CRediT taxonomy.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PersonClass',
                       'OrganizationClass',
                       'AIModelClass',
                       'SoftwareClass']} })
    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })

    @field_validator('ror_id')
    def pattern_ror_id(cls, v):
        pattern=re.compile(r"^https?://ror\.org/[a-z0-9]{9}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ror_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ror_id format: {v}"
            raise ValueError(err_msg)
        return v


class LocationClass(ConfiguredBaseModel):
    """
    A physical location associated with a facility or organization.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'description': {'name': 'description', 'required': True}}})

    description: str = Field(default=..., description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })
    ror_id: Optional[str] = Field(default=None, description="""The ROR identifier for an organization, in URL format (e.g., https://ror.org/03yrm5c26).""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:sameAs',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AffiliationClass',
                       'OrganizationClass',
                       'LocationClass',
                       'PublisherClass',
                       'SponsorOrganizationClass'],
         'in_subset': ['discoverability_if_applicable']} })

    @field_validator('ror_id')
    def pattern_ror_id(cls, v):
        pattern=re.compile(r"^https?://ror\.org/[a-z0-9]{9}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ror_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ror_id format: {v}"
            raise ValueError(err_msg)
        return v


class AIModelClass(ConfiguredBaseModel):
    """
    An AI model, including its name, version, and provider.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'accessed_date': {'description': 'The ISO 8601 date when the '
                                                         'AI model was accessed for '
                                                         'use in creating or updating '
                                                         'the datacard.',
                                          'name': 'accessed_date',
                                          'required': True},
                        'relationship': {'description': 'The relationship of this AI '
                                                        'model to the datacard or '
                                                        'dataset (e.g., '
                                                        'used_for_datacard_creation, '
                                                        'used_for_data_processing, '
                                                        'other).',
                                         'name': 'relationship',
                                         'range': 'ExtendedRelationshipEnum',
                                         'required': True}}})

    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    version: Optional[str] = Field(default=None, description="""Version of software, tool, or library.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIModelClass',
                       'SoftwareClass',
                       'SchemaReferenceClass',
                       'DatasetIdentificationClass',
                       'DataServiceClass']} })
    accessed_date: str = Field(default=..., description="""The ISO 8601 date when the AI model was accessed for use in creating or updating the datacard.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIModelClass']} })
    identifier: IdentifierClass = Field(default=..., description="""A unique identifier for the datacard document itself, following the format: \"doi: distinct from the dataset identifier. Assign if the datacard is registered in a catalog or repository independently of the dataset.""", json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'broad_mappings': ['schema:identifier',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AIModelClass',
                       'SoftwareClass',
                       'NamedIdentifierClass',
                       'DatasetClass'],
         'in_subset': ['interoperability_if_applicable']} })
    role: Optional[list[RoleEnum]] = Field(default=None, description="""The role, using the CRediT taxonomy, of a type (person, organization, AI model,  or software tool) in relation to the datacard or dataset. CRediT roles include: Conceptualization, Data_Curation, Formal_Analysis, Funding_Acquisition, Investigation, Methodology, Project_Administration, Resources, Software, Supervision, Validation, Visualization, Writing_Original_Draft, Writing_Review_and_Editing. This has been extended with an Other role to capture contributions that do not fit within the CRediT taxonomy.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PersonClass',
                       'OrganizationClass',
                       'AIModelClass',
                       'SoftwareClass']} })
    relationship: ExtendedRelationshipEnum = Field(default=..., description="""The relationship of this AI model to the datacard or dataset (e.g., used_for_datacard_creation, used_for_data_processing, other).""", json_schema_extra = { "linkml_meta": {'domain_of': ['PublicationIdentifierClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DatasetClass'],
         'in_subset': ['interoperability_if_applicable']} })

    @field_validator('version')
    def pattern_version(cls, v):
        pattern=re.compile(r"^\d+\.\d+(\.\d+)?$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid version format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid version format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('accessed_date')
    def pattern_accessed_date(cls, v):
        pattern=re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid accessed_date format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid accessed_date format: {v}"
            raise ValueError(err_msg)
        return v


class SoftwareClass(ConfiguredBaseModel):
    """
    A software tool, including its name, version, and provider.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'relationship': {'description': 'The relationship of this '
                                                        'software to the datacard or '
                                                        'dataset (e.g., '
                                                        'used_for_datacard_creation, '
                                                        'used_for_data_processing, '
                                                        'other).',
                                         'name': 'relationship',
                                         'range': 'ExtendedRelationshipEnum',
                                         'required': True},
                        'role': {'name': 'role', 'required': False}}})

    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    version: Optional[str] = Field(default=None, description="""Version of software, tool, or library.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIModelClass',
                       'SoftwareClass',
                       'SchemaReferenceClass',
                       'DatasetIdentificationClass',
                       'DataServiceClass']} })
    identifier: IdentifierClass = Field(default=..., description="""A unique identifier for the datacard document itself, following the format: \"doi: distinct from the dataset identifier. Assign if the datacard is registered in a catalog or repository independently of the dataset.""", json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'broad_mappings': ['schema:identifier',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AIModelClass',
                       'SoftwareClass',
                       'NamedIdentifierClass',
                       'DatasetClass'],
         'in_subset': ['interoperability_if_applicable']} })
    role: Optional[list[RoleEnum]] = Field(default=None, description="""The role, using the CRediT taxonomy, of a type (person, organization, AI model,  or software tool) in relation to the datacard or dataset. CRediT roles include: Conceptualization, Data_Curation, Formal_Analysis, Funding_Acquisition, Investigation, Methodology, Project_Administration, Resources, Software, Supervision, Validation, Visualization, Writing_Original_Draft, Writing_Review_and_Editing. This has been extended with an Other role to capture contributions that do not fit within the CRediT taxonomy.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PersonClass',
                       'OrganizationClass',
                       'AIModelClass',
                       'SoftwareClass']} })
    relationship: ExtendedRelationshipEnum = Field(default=..., description="""The relationship of this software to the datacard or dataset (e.g., used_for_datacard_creation, used_for_data_processing, other).""", json_schema_extra = { "linkml_meta": {'domain_of': ['PublicationIdentifierClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DatasetClass'],
         'in_subset': ['interoperability_if_applicable']} })

    @field_validator('version')
    def pattern_version(cls, v):
        pattern=re.compile(r"^\d+\.\d+(\.\d+)?$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid version format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid version format: {v}"
            raise ValueError(err_msg)
        return v


class DomainMetadataClass(NamedThing):
    """
    Domain-specific metadata relevant to the dataset,  which may include specific fields or structures relevant to the scientific domain of the dataset.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    science_domain: Optional[ScienceDomainEnum] = Field(default=None, description="""Scientific domain or discipline this dataset primarily relates to. Extends the the list of OSTI Subject Areas with an Other category for datasets that do not fit into the OSTI list. Controlled vocabulary: Biology and Medicine | Chemistry | Energy Storage, Conversion, and Utilization | Engineering | Environmental Sciences | Fission and Nuclear Technologies | Fossil Fuels | Geosciences | Materials | Mathematics and Computing | National Defense | Physics | Power Generation and Distribution | Renewable Energy""", json_schema_extra = { "linkml_meta": {'domain_of': ['DomainMetadataClass', 'DatasetDescriptionClass'],
         'in_subset': ['discoverability_if_applicable']} })
    schema_reference: Optional[SchemaReferenceClass] = Field(default=None, description="""Reference to a schema or controlled vocabulary that defines the domain-specific metadata fields used in the domain_metadata block.
This can provide users with information about the structure and semantics of the domain-specific metadata,  which can inform their understanding of the dataset and how to work with the domain-specific metadata""", json_schema_extra = { "linkml_meta": {'domain_of': ['DomainMetadataClass'],
         'in_subset': ['interoperability_if_applicable']} })
    fields: Optional[dict[str, DomainMetadataFieldValueClass]] = Field(default=None, description="""Field names, their corresponding values, data types, units, and descriptions for domain-specific metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DomainMetadataClass']} })
    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })


class SchemaReferenceClass(IdentifierClass):
    """
    A reference to a schema that describes the structure of the dataset or domain metadata. This can include links to formal schema definitions, data dictionaries, or other structured representations of the dataset's content.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    version: Optional[str] = Field(default=None, description="""Version of software, tool, or library.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIModelClass',
                       'SoftwareClass',
                       'SchemaReferenceClass',
                       'DatasetIdentificationClass',
                       'DataServiceClass']} })
    type: IdentifierTypeEnum = Field(default=..., description="""The type of the Identifer (e.g., DOI, UUID, ARK), following a controlled vocabulary of identifier types.
Assign if the datacard has an identifier; required if 'id' is provided.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['datacite:identifierType'],
         'domain_of': ['PublicationIdentifierClass', 'IdentifierClass'],
         'in_subset': ['interoperability_if_applicable']} })
    value: Optional[str] = Field(default=None, description="""The value of the identifier (e.g., \"10.1234/abcd\"), following the format specified by the 'type' field.
Assign if the datacard has an identifier; required if 'id' is provided.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:identifier',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['PublicationIdentifierClass', 'IdentifierClass', 'AnyValue']} })

    @field_validator('version')
    def pattern_version(cls, v):
        pattern=re.compile(r"^\d+\.\d+(\.\d+)?$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid version format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid version format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('value')
    def pattern_value(cls, v):
        pattern=re.compile(r"^.*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid value format: {v}"
            raise ValueError(err_msg)
        return v


class DomainMetadataFieldValueClass(ConfiguredBaseModel):
    """
    A domain-specific metadata value keyed by the field name.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    field_value: Optional[str] = Field(default=None, description="""The value for a specific domain metadata field.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DomainMetadataFieldValueClass'],
         'in_subset': ['interoperability_if_applicable']} })
    data_type: Optional[str] = Field(default=None, description="""The data type of a feature or variable, following a controlled vocabulary from  (e.g., float, int, string, boolean, datetime, other). This can provide important information about the nature of the data and can inform users about how to interpret and work with the dataset.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:dataType'],
         'domain_of': ['DomainMetadataFieldValueClass', 'FeatureClass'],
         'in_subset': ['interoperability_if_applicable']} })
    unit: Optional[str] = Field(default=None, description="""The unit of measurement for a feature, if applicable.
This can provide important context for interpreting the values of the feature and can inform users about how to work with the data effectively.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:unitText'],
         'domain_of': ['DomainMetadataFieldValueClass', 'FeatureClass'],
         'in_subset': ['interoperability_if_applicable']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })


class DatasetIdentificationClass(NamedThing):
    """
    A section of metadata elements that identify and provide basic information about the dataset.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'project': {'ifabsent': 'string(genesis)',
                                    'name': 'project',
                                    'required': False},
                        'version': {'description': 'Dataset version using semantic '
                                                   'versioning: MAJOR.MINOR.PATCH '
                                                   'Increment MAJOR for breaking '
                                                   'changes, MINOR for additions, '
                                                   'PATCH for corrections. Start at '
                                                   '1.0.0 for first release. See '
                                                   'supersedes / superseded_by below '
                                                   'for linking versions, and '
                                                   'stewardship.versioning_strategy '
                                                   'for how versions are managed.',
                                    'ifabsent': 'string(1.0.0)',
                                    'in_subset': ['discoverability_required'],
                                    'name': 'version',
                                    'required': True}}})

    project: Optional[str] = Field(default="genesis", description="""Single human-readable name from the project, Genesis project or sub-project this dataset belongs to. e.g., genesis | genesis-fusion | genesis-lightsource Use the same name in the datacard filename.""", json_schema_extra = { "linkml_meta": {'aliases': ['project_name', 'genesis_project', 'sub_project'],
         'domain_of': ['DatasetIdentificationClass', 'TagsClass'],
         'ifabsent': 'string(genesis)',
         'in_subset': ['discoverability_required']} })
    version: str = Field(default="1.0.0", description="""Dataset version using semantic versioning: MAJOR.MINOR.PATCH Increment MAJOR for breaking changes, MINOR for additions, PATCH for corrections. Start at 1.0.0 for first release. See supersedes / superseded_by below for linking versions, and stewardship.versioning_strategy for how versions are managed.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIModelClass',
                       'SoftwareClass',
                       'SchemaReferenceClass',
                       'DatasetIdentificationClass',
                       'DataServiceClass'],
         'ifabsent': 'string(1.0.0)',
         'in_subset': ['discoverability_required']} })
    primary_id: IdentifierClass = Field(default=..., description="""Primary persistent identifier block for this dataset. type can be DOI, ARK, UUID, or any other globally unique identifier. value should follow the format specified by the type. This is the main identifier for the dataset  and should be globally unique and resolvable if possible.""", json_schema_extra = { "linkml_meta": {'aliases': ['primary_identifier',
                     'main_id',
                     'main_identifier',
                     'dataset_id',
                     'dataset_identifier',
                     'PID',
                     'dataset_pid'],
         'domain_of': ['DatasetIdentificationClass'],
         'exact_mappings': ['schema:identifier',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'in_subset': ['discoverability_required']} })
    additional_ids: Optional[list[IdentifierClass]] = Field(default=None, description="""Additional identifiers for this dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetIdentificationClass'],
         'exact_mappings': ['adms:identifier'],
         'in_subset': ['discoverability_if_applicable']} })
    supersedes: Optional[IdentifierClass] = Field(default=None, description="""Identifier of the prior version this dataset replaces.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetIdentificationClass'],
         'in_subset': ['discoverability_if_applicable']} })
    superseded_by: Optional[IdentifierClass] = Field(default=None, description="""Identifier of the newer version that replaces this dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetIdentificationClass'],
         'in_subset': ['discoverability_if_applicable']} })
    parent_collection: Optional[NamedIdentifierClass] = Field(default=None, description="""Class collection or experimental campaign this dataset belongs to. Use when this dataset is one of many in a larger organized collection or ensemble.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetIdentificationClass'],
         'in_subset': ['discoverability_if_applicable']} })
    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })

    @field_validator('version')
    def pattern_version(cls, v):
        pattern=re.compile(r"^\d+\.\d+(\.\d+)?$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid version format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid version format: {v}"
            raise ValueError(err_msg)
        return v


class NamedIdentifierClass(ConfiguredBaseModel):
    """
    A named identifier for an entity, consisting of a name, and an Identifier class for the value.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'name': {'name': 'name', 'required': True}}})

    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    identifier: IdentifierClass = Field(default=..., description="""A unique identifier for the datacard document itself, following the format: \"doi: distinct from the dataset identifier. Assign if the datacard is registered in a catalog or repository independently of the dataset.""", json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'broad_mappings': ['schema:identifier',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AIModelClass',
                       'SoftwareClass',
                       'NamedIdentifierClass',
                       'DatasetClass'],
         'in_subset': ['interoperability_if_applicable']} })


class DatasetDescriptionClass(ConfiguredBaseModel):
    """
    A section of metadata elements that describe the dataset,  including its content, context, and characteristics. At a minimum, a summary is required to provide a brief overview of the dataset,  even for early-stage datasets that are still in development  and may not have all details finalized.  This allows for the creation of datacards early in the workflow,  which can be updated as more information becomes available.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'If task_subcategory is present, then task_category '
                                   'must be present.',
                    'postconditions': {'slot_conditions': {'task_category': {'name': 'task_category',
                                                                             'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'task_subcategory': {'name': 'task_subcategory',
                                                                               'value_presence': 'PRESENT'}}}}]})

    science_domain: Optional[ScienceDomainEnum] = Field(default=None, description="""Scientific domain or discipline this dataset primarily relates to. Extends the the list of OSTI Subject Areas with an Other category for datasets that do not fit into the OSTI list. Controlled vocabulary: Biology and Medicine | Chemistry | Energy Storage, Conversion, and Utilization | Engineering | Environmental Sciences | Fission and Nuclear Technologies | Fossil Fuels | Geosciences | Materials | Mathematics and Computing | National Defense | Physics | Power Generation and Distribution | Renewable Energy""", json_schema_extra = { "linkml_meta": {'domain_of': ['DomainMetadataClass', 'DatasetDescriptionClass'],
         'in_subset': ['discoverability_if_applicable']} })
    dataset_summary: str = Field(default=..., description="""A brief summary of the dataset, including its key characteristics and intended use. Recommend 1-3 sentences that provide a high-level overview of the dataset, its purpose, and its potential applications. This should be a concise overview that provides users with a quick  understanding of what the dataset is about and whether it may be relevant to their needs.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetDescriptionClass'],
         'in_subset': ['discoverability_required']} })
    purpose: Optional[str] = Field(default=None, description="""The purpose for which the dataset was created. What gap does it fill? Include the scientific question or problem it was intended to address.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetDescriptionClass'],
         'in_subset': ['discoverability_if_applicable']} })
    collection_methodology: Optional[str] = Field(default=None, description="""How was data acquired? e.g., experimental sensors | computational simulation | human annotation | derived from prior datasets""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetDescriptionClass'],
         'in_subset': ['discoverability_if_applicable']} })
    data_characteristics: Optional[str] = Field(default=None, description="""Key structural and content characteristics: scale, dimensionality, temporal coverage, spatial resolution.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetDescriptionClass'],
         'in_subset': ['discoverability_if_applicable']} })
    limitations: Optional[str] = Field(default=None, description="""Known limitations, gaps, or caveats users should be aware of before using this dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetDescriptionClass'],
         'in_subset': ['discoverability_if_applicable']} })
    tags: Optional[TagsClass] = Field(default=None, description="""Structured tags block for catalog filtering and discovery, including project, science, object_type, and risk.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetDescriptionClass'],
         'in_subset': ['discoverability_if_applicable']} })
    task_category: Optional[list[str]] = Field(default=None, description="""Primary task category or categories for this dataset. Helps ML practitioners find relevant datasets in the catalog. e.g.,  classification | regression | segmentation | detection | generation | translation | summarization | ranking | anomaly_detection | clustering | reinforcement_learning | other""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['task', 'ml_task'],
         'domain_of': ['DatasetDescriptionClass'],
         'in_subset': ['discoverability_if_applicable']} })
    task_subcategory: Optional[list[str]] = Field(default=None, description="""More specifictask subcategory or subcategories. e.g.,  binary_classification | multi_class_classification | multi_label_classification | image_segmentation | object_detection | time_series_forecasting | named_entity_recognition | question_answering | other""", json_schema_extra = { "linkml_meta": {'aliases': ['task_sub', 'ml_task_sub', 'ml_sub_task'],
         'domain_of': ['DatasetDescriptionClass'],
         'in_subset': ['discoverability_if_applicable']} })
    keywords: list[str] = Field(default=..., description="""Terms that describe this dataset and aid discovery. Include domain terms, methods, instruments, and relevant ontology terms.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetDescriptionClass'],
         'in_subset': ['discoverability_required']} })


class UseGovernanceClass(ConfiguredBaseModel):
    """
    Information to guide appropriate use and prevent misuse of this dataset. This section provides guidance on the intended use of the dataset,  any permitted uses, and any restrictions or limitations on how the dataset can be used.  This is important for ensuring that users understand the appropriate contexts for using the dataset and any potential risks or ethical considerations associated with its use.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    current_use: str = Field(default=..., description="""For in-workflow data: what is this dataset actively being used for right now? Distinct from intended_use.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UseGovernanceClass'], 'in_subset': ['governed_use_required']} })
    intended_use: Optional[str] = Field(default=None, description="""Tasks or workflows this dataset is designed to support. e.g., ML training | physics analysis | benchmarking | visualization""", json_schema_extra = { "linkml_meta": {'domain_of': ['UseGovernanceClass'],
         'in_subset': ['governed_use_if_applicable']} })
    permitted_use: Optional[str] = Field(default=None, description="""Uses this dataset is designed and intended to support. Genesis governance expects explicit permitted use metadata at the governance level, which is why this field is distinct from intended_use. Be explicit about what this dataset is suitable for, to guide users and prevent misuse. e.g., AI workflows | research and publication | internal analysis | educational use""", json_schema_extra = { "linkml_meta": {'domain_of': ['UseGovernanceClass'],
         'in_subset': ['governed_use_if_applicable']} })
    out_of_scope_use: Optional[str] = Field(default=None, description="""Uses this dataset should NOT be applied to. e.g., clinical decision-making | real-time control systems""", json_schema_extra = { "linkml_meta": {'domain_of': ['UseGovernanceClass'],
         'in_subset': ['governed_use_if_applicable']} })
    prohibited_use: Optional[str] = Field(default=None, description="""Uses that are explicitly prohibited for this dataset, either due to ethical considerations, safety concerns, or other governance reasons. Genesis governance expects explicit prohibited use metadata at the governance level, which is why this field is distinct from intended_use. Be explicit about what this dataset should not be used for, to guide users and prevent misuse. e.g., commercial use | AI workflows | redistribution | use by foreign nationals |clinical decision-making | real-time control systems""", json_schema_extra = { "linkml_meta": {'domain_of': ['UseGovernanceClass'],
         'in_subset': ['governed_use_if_applicable']} })


class SensitivityClass(ConfiguredBaseModel):
    """
    Sensitivity metadata for Genesis assets. This structure is intended to preserve authoritative source markings/designations while minimizing redundant manual entry. It separates actual source marking/control information from adjacent governance metadata such as export control, privacy, rights, release, and records status.
    Design_principles:
    Preserve authoritative source markings/designations as primary source of truth.
    Use one overall sensitivity summary field for display/discovery, but not as the sole governance basis.
    Keep UCNI distinct from generic CUI.
    Treat OUO and other deprecated labels as legacy provenance, not modern primary control categories.
    Keep export, privacy/PII/PHI, rights, agreement, release, and records metadata outside the sensitivity block.
    Do not create or imply a Genesis-private marking scheme.
    Prefer structured canonical fields plus a preserved source marking string over many overlapping flags.
    Support source-agency-aware controls where non-DOE-originated material is in scope.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'If classified_status = "Yes", classification level '
                                   'is required.',
                    'postconditions': {'slot_conditions': {'classification_level': {'name': 'classification_level',
                                                                                    'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'classified_status': {'equals_string': 'Yes',
                                                                                'name': 'classified_status'}}}},
                   {'description': 'If classified_status = "Yes", '
                                   'classification_category must contain at least one '
                                   'value.',
                    'postconditions': {'slot_conditions': {'classification_category': {'name': 'classification_category',
                                                                                       'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'classified_status': {'equals_string': 'Yes',
                                                                                'name': 'classified_status'}}}},
                   {'description': 'If ucni_status = "Yes", UCNI must not be '
                                   'represented solely through generic CUI category '
                                   'fields.',
                    'postconditions': {'slot_conditions': {'cui_specified_categories': {'name': 'cui_specified_categories',
                                                                                        'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'ucni_status': {'equals_string': 'Yes',
                                                                          'name': 'ucni_status'}}}},
                   {'description': 'If source_marking_scheme = "Legacy_OUO", '
                                   'legacy_label_source should be populated.',
                    'postconditions': {'slot_conditions': {'legacy_label_source': {'name': 'legacy_label_source',
                                                                                   'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'source_marking_scheme': {'equals_string': 'Legacy_OUO',
                                                                                    'name': 'source_marking_scheme'}}}},
                   {'description': 'If source_marking_scheme = "Legacy_OUO" and '
                                   'current basis has not been resolved,\n'
                                   '  normalized_control_basis should be present',
                    'postconditions': {'slot_conditions': {'normalized_control_basis': {'name': 'normalized_control_basis',
                                                                                        'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'source_marking_scheme': {'equals_string': 'Legacy_OUO',
                                                                                    'name': 'source_marking_scheme'}}}},
                   {'description': 'If the overall_sensitivity is Classified, then the '
                                   'classified_status must be "Yes".',
                    'postconditions': {'slot_conditions': {'classified_status': {'equals_string': 'Yes',
                                                                                 'name': 'classified_status'}}},
                    'preconditions': {'slot_conditions': {'overall_sensitivity': {'equals_string': 'Classified',
                                                                                  'name': 'overall_sensitivity'}}}},
                   {'description': 'If the overall_sensitivity is CUI, then the '
                                   'cui_status must be "Yes" and classified_status '
                                   'must be "No".',
                    'postconditions': {'slot_conditions': {'classified_status': {'equals_string': 'No',
                                                                                 'name': 'classified_status'},
                                                           'cui_status': {'equals_string': 'Yes',
                                                                          'name': 'cui_status'}}},
                    'preconditions': {'slot_conditions': {'overall_sensitivity': {'equals_string': 'CUI',
                                                                                  'name': 'overall_sensitivity'}}}},
                   {'description': 'If the overall_sensitivity is UCNI then the '
                                   'ucni_status must be "Yes".',
                    'postconditions': {'slot_conditions': {'ucni_status': {'equals_string': 'Yes',
                                                                           'name': 'ucni_status'}}},
                    'preconditions': {'slot_conditions': {'overall_sensitivity': {'equals_string': 'UCNI',
                                                                                  'name': 'overall_sensitivity'}}}}],
         'slot_usage': {'classified_status': {'name': 'classified_status',
                                              'required': True},
                        'cui_status': {'name': 'cui_status', 'required': True},
                        'overall_sensitivity': {'name': 'overall_sensitivity',
                                                'required': True},
                        'source_marking_scheme': {'name': 'source_marking_scheme',
                                                  'required': True},
                        'source_marking_string': {'name': 'source_marking_string',
                                                  'required': True},
                        'ucni_status': {'name': 'ucni_status', 'required': True}}})

    overall_sensitivity: OverallSensitivityEnum = Field(default=..., description="""Human-readable top-level sensitivity posture of the asset. This is a summary field only and does not replace the authoritative fields such as the classification_status, classification_level, export_control_basis, or privacy_control_basis fields.
This can be used for filtering and discovery in catalogs, but authoritative source markings and metadata fields should be used for access control and governance decisions.
Uses the OverallSensitivityEnum controlled vocabulary, which includes values such as: public | unclassified_uncontrolled | cui | ucni | classified | legacy_controlled | mixed | other_controlled
Use \"public\" for unclassified, non-sensitive assets that can be shared publicly.""", json_schema_extra = { "linkml_meta": {'aliases': ['datacard_sensitivity', 'overall_sensitivity_level'],
         'broad_mappings': ['schema:specialUsageRestriction',
                            'dcterms:rights',
                            'datacite:rights'],
         'domain_of': ['SensitivityClass'],
         'in_subset': ['discoverability_required']} })
    source_marking_string: str = Field(default=..., description="""Exact marking/banner/control text as it appears on the source artifact or in the authoritative review/release output, if applicable.
This provides the authoritative source marking information for the asset, which is critical for ensuring proper handling and access controls based on the sensitivity of the asset.
If no source markings apply to the asset, this field should be filled with \"not_applicable\".
If the asset has multiple source markings, list them separated by // with no spaces
Examples: \"not_applicable\" | \"CUI//SP-EXPT//NOFORN\" | \"SECRET//RD//SIGMA 15\" | \"OFFICIAL USE ONLY\"
This field does not replace the individual metadata fields for classification status,  classification level, export control basis, or privacy control basis,  which should still be filled out based on the authoritative source markings.
Source_marking_string is provenance-preserving and may contain source-agency-specific constructs not otherwise modeled in DOE-native structured fields; source_marking_scheme should identify that regime.""", json_schema_extra = { "linkml_meta": {'aliases': ['marking',
                     'official_marking',
                     'source_marking',
                     'source_markings',
                     'marking_string',
                     'marking_banner',
                     'control_text'],
         'domain_of': ['SensitivityClass'],
         'in_subset': ['discoverability_required']} })
    source_marking_scheme: SourceMarkingSchemeEnum = Field(default=..., description="""Identifies the authoritative source marking regime, for the source_marking_string field,  following a controlled vocabulary of source marking schemes: SourceMarkingSchemeEnum. Examples include: DOE_CUI | DOE_UCNI | EO13526_Classified | AEA_RD_FRD_TFNI | DOD_CUI | DHS_CUI | Legacy_OUO | Legacy_Site_Specific | Other_Agency | None
This provides important context for interpreting the source_marking_string field, as different marking schemes may have different formats and meanings for the markings.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'], 'in_subset': ['discoverability_required']} })
    classified_status: YesNoEnum = Field(default=..., description="""\"Yes\" | \"No\" - Indicates whether the asset is classified.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'], 'in_subset': ['discoverability_required']} })
    classification_level: Optional[ClassificationLevelEnum] = Field(default=None, description="""Official classification level, if the asset is classified. If classified_status is \"Yes\", the classification level of the asset,  following the controlled vocabulary: Top_Secret | Secret | Confidential""", json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'],
         'in_subset': ['discoverability_if_applicable']} })
    classification_category: Optional[list[ClassificationCategoryEnum]] = Field(default=None, description="""Official classification category, if the asset is classified. If classified_status = \"Yes\", the classification category of the asset,  following controlled vocabulary NSI | RD | TFNI | \"Other Classified\"""", min_length=1, json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'],
         'in_subset': ['discoverability_if_applicable'],
         'list_elements_unique': True} })
    classified_control_markings: Optional[list[str]] = Field(default=None, description="""Additional classified dissemination/caveat/handling markings appearing with classified content, e.g., NOFORN, CNWDI, SIGMA 14, SIGMA 15, ORCON,REL TO USA, GBR. List all that apply, each as a separate entry.  This provides important context for handling and access controls for classified assets.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'],
         'in_subset': ['discoverability_if_applicable'],
         'list_elements_unique': True} })
    cui_status: YesNoEnum = Field(default=..., description="""\"Yes\" | \"No\" - Indicates whether the asset is Controlled Unclassified Information (CUI).""", json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'], 'in_subset': ['discoverability_required']} })
    cui_basic_categories: Optional[list[str]] = Field(default=None, description="""Basic CUI categories applicable to this asset, if it is CUI. Use the DOE/ISOO-authoritative CUI Basic categories or subcategories. List all that apply, each as a separate entry.  This provides important context for handling and access controls for CUI assets.""", min_length=1, json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'],
         'in_subset': ['discoverability_if_applicable'],
         'list_elements_unique': True} })
    cui_specified_categories: Optional[list[str]] = Field(default=None, description="""Specified CUI categories applicable to this asset, if it is CUI. Use the DOE/ISOO-authoritative CUI Specified categories or subcategories. List all that apply, each as a separate entry.  This provides important context for handling and access controls for CUI assets.""", min_length=1, json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'],
         'in_subset': ['discoverability_if_applicable'],
         'list_elements_unique': True} })
    cui_limited_dissemination_controls: Optional[list[str]] = Field(default=None, description="""Applicable CUI limited dissemination controls such as NOFORN, DL ONLY, REL TO USA, GBR, DISPLAY ONLY USA, GBR, RELIDO, or other authoritative values. Ordering/formatting should follow authoritative agency guidance. If cui_limited_dissemination_controls contains NOFORN, REL TO..., DISPLAY ONLY..., or similar controls, then governed_use.non_sensitivity_governance_metadata.foreign_national_access_status should be consistent with those controls.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'],
         'in_subset': ['discoverability_if_applicable'],
         'list_elements_unique': True} })
    ucni_status: YesNoEnum = Field(default=..., description="""\"Yes\" | \"No\" - Indicates whether the asset contains UCNI. UCNI is represented separately and should not be treated as an ordinary CUI category value. This provides important context for handling and access controls for UCNI assets.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'], 'in_subset': ['discoverability_required']} })
    uk_mda_status: Optional[UKMDAStatusEnum] = Field(default=None, description="""\"Yes\" | \"No\" - Indicates whether the asset is subject to UK MDA-specific handling. Optional and may be used where relevant to local/site governance.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'],
         'in_subset': ['discoverability_if_applicable']} })
    legacy_label_source: Optional[list[str]] = Field(default=None, description="""Preserves deprecated or local historical control labels such as OUO, SBU, or site-specific legacy markings as provenance/source information only.""", min_length=1, json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'],
         'in_subset': ['discoverability_if_applicable'],
         'list_elements_unique': True} })
    normalized_control_basis: Optional[list[NormalizedControlBasisEnum]] = Field(default=None, description="""Optional interpreted control basis used for governance where source materials contain legacy, mixed, or non-standard constructs. This does not replace authoritative source markings.
If source_marking_scheme = Legacy_OUO and the legacy marking is unresolved to a current standard marking,  this should be populated as \"Legacy_Needs_Mapping\" to indicate that the control basis is legacy and needs interpretation for governance purposes.""", min_length=1, json_schema_extra = { "linkml_meta": {'domain_of': ['SensitivityClass'],
         'in_subset': ['discoverability_if_applicable'],
         'list_elements_unique': True} })


class WorkflowClass(ConfiguredBaseModel):
    """
    Workflow & Lifecycle:
    Describes the technical and processing lifecycle position of the dataset. See NOTE ON WORKFLOW STATE vs. RELEASE STATUS in the header for expected alignment with release_status.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'If state is Published, then embargo_until must be '
                                   'absent.',
                    'postconditions': {'slot_conditions': {'embargo_until': {'name': 'embargo_until',
                                                                             'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'state': {'equals_string': 'Published',
                                                                    'name': 'state'}}}},
                   {'description': 'If state is Embargo, then embargo_until must be '
                                   'present.',
                    'postconditions': {'slot_conditions': {'embargo_until': {'name': 'embargo_until',
                                                                             'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'state': {'equals_string': 'Embargo',
                                                                    'name': 'state'}}}}],
         'slot_usage': {'state': {'name': 'state',
                                  'range': 'StateEnum',
                                  'required': True}}})

    state: StateEnum = Field(default=..., description="""Current lifecycle position of the data itself, following StateEnum controlled vocabulary (e.g., raw, processing, qa, analysis, review, embargo, published, archived). NOTE ON DISCOVERABILITYWORKFLOW STATE vs. REUSABILITY RELEASE STATUS: discoverability.workflow.state   — describes the technical/processing lifecycle position of the data itself (raw → archived)
    reuasability.release_status   — describes the publication and governance state of the dataset record (draft → deprecated)
These should be logically consistent. Common alignments:
  discoverability.workflow.state=raw|processing|qa|analysis → reuasability.release_status=draft
  discoverability.workflow.state=review                     → reuasability.release_status=under_review
  discoverability.workflow.state=embargo|published          → reuasability.release_status=approved|published
  discoverability.workflow.state=archived                   → reuasability.release_status=deprecated|published""", json_schema_extra = { "linkml_meta": {'domain_of': ['WorkflowClass'], 'in_subset': ['discoverability_required']} })
    is_intermediate: Optional[YesNoEnum] = Field(default=None, description="""\"Yes\" | \"No\" - Whether this dataset is an intermediate output, as opposed to a final deliverable. \"No\" if this is final. This can inform how users interpret the dataset and its suitability for different use cases.""", json_schema_extra = { "linkml_meta": {'domain_of': ['WorkflowClass'], 'in_subset': ['discoverability_if_applicable']} })
    pipeline_stage: Optional[str] = Field(default=None, description="""Freetext position in processing pipeline. e.g., \"post-detector, pre-reconstruction\" e.g., \"raw telemetry, pre-calibration\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['WorkflowClass'], 'in_subset': ['discoverability_if_applicable']} })
    embargo_until: Optional[date] = Field(default=None, description="""Required if state=embargo. ISO 8601 date after which release is permitted.""", json_schema_extra = { "linkml_meta": {'domain_of': ['WorkflowClass'], 'in_subset': ['discoverability_if_applicable']} })


class AccessPolicyClass(ConfiguredBaseModel):
    """
    Access policy for the dataset. Describes the access level and any restrictions or requirements for accessing the dataset, which is critical information for users to understand how they can access the dataset and any potential barriers to access.  Access policy is DISTINCT from sensitivity, which describes the nature of the data and its potential risks)  and from release status (which describes the publication state of the dataset). access_policy.access_level is a required field that indicates the level of permissions required for users to access the dataset, following AccessLevelEnum.
    open: no additional permissions required beyond standard account registration and agreement to terms of service. This indicates that the dataset is freely accessible to the public and can be used without any special permissions or restrictions. Note that \"open\" does not necessarily mean that the dataset is free of copyright or other legal restrictions, but rather that there are no additional access controls in place. Users may still need to comply with any applicable laws or regulations when using the dataset.
    restricted: access may be granted to users who meet certain criteria, such as being part of a specific research community, having a legitimate research purpose, or agreeing to specific terms and conditions. This indicates that the dataset is not freely accessible to the public and that users must meet certain requirements or restrictions in order to access it. The specific criteria for access may vary depending on the dataset and the organization providing it, but could include things like institutional affiliation, research purpose, or agreement to specific terms and conditions.
    controlled: access is tightly controlled and may require specific authorization, agreements, or approvals. This indicates that the dataset contains sensitive information and that only authorized users can access it.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'If access_level is Restricted, '
                                   'authorization_required must be present.',
                    'postconditions': {'slot_conditions': {'authorization_required': {'name': 'authorization_required',
                                                                                      'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'access_level': {'equals_string': 'Restricted',
                                                                           'name': 'access_level'}}}},
                   {'description': 'If access_level is Controlled, '
                                   'authorization_required must be present.',
                    'postconditions': {'slot_conditions': {'authorization_required': {'name': 'authorization_required',
                                                                                      'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'access_level': {'equals_string': 'Controlled',
                                                                           'name': 'access_level'}}}},
                   {'description': 'If authorization_required includes "Other", then '
                                   'access_restrictions must be present.',
                    'postconditions': {'slot_conditions': {'access_restrictions': {'name': 'access_restrictions',
                                                                                   'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'authorization_required': {'has_member': {'equals_string': 'Other'},
                                                                                     'name': 'authorization_required'}}}}]})

    access_level: AccessLevelEnum = Field(default=..., description="""The access level of the dataset, following AccessLevelEnum controlled vocabulary: open | controlled | restricted This provides important context about who can access the dataset and can inform users about potential barriers to access and use. This does not replace the authoritative source markings and metadata fields for classification, CUI, or other sensitivity designations,  which should still be filled out based on the authoritative source markings.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessPolicyClass', 'IntendedRepositoryClass'],
         'in_subset': ['accessibility_required']} })
    access_restrictions: Optional[str] = Field(default=None, description="""Freetext description of access restrictions. e.g., \"Requires signed DUA\" | \"None - publicly accessible\" | \"Access limited to cleared personnel with need-to-know\" | \"Requires two-factor authentication and secure VPN access\" Any specific access restrictions or requirements for the dataset,  beyond what is indicated by the classification and sensitivity markings. This can provide more detailed information about who is allowed to access the  dataset and under what conditions, which can inform users about potential barriers to access and use.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessPolicyClass'],
         'in_subset': ['accessibility_if_applicable']} })
    authorization_required: Optional[list[AuthorizationRequiredEnum]] = Field(default=None, description="""List of authorizations required. When formal authorization is required to access the dataset, add terms from the following AuthorizationRequiredEnum controlled vocabulary  (e.g., \"none\", \"account\", \"export_control_review\", \"user_agreement\", \"other\").""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessPolicyClass'],
         'in_subset': ['accessibility_if_applicable']} })
    intended_partner_classes: Optional[list[IntendedPartnerClassEnum]] = Field(default=None, description="""The intended partner classes/types (list) that are expected to access and use this dataset, if applicable. Uses the IntendedPartnerClassEnum controlled vocabulary: internal_team tri_lab doe_nnsa_lab federal_partner contractor academic_researchers external_research_partner public industry_partners other This can provide insight into the target audience for the dataset and can inform users about the typical or intended user base.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessPolicyClass'],
         'in_subset': ['accessibility_if_applicable']} })
    approved_environments: Optional[list[str]] = Field(default=None, description="""Approved environments for accessing or using the dataset, if applicable. e.g., \"Secure Enclave A\", \"On-Premises HPC Cluster\", \"Cloud Environment B\" And empty list ([]) if there are no specific approved environments or if the dataset is publicly accessible. null or absent means it has not yet been determined whether approved environments are required. This can inform users about where they are allowed to access and use the dataset,  which can be important for compliance with security requirements.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessPolicyClass'],
         'in_subset': ['accessibility_if_applicable']} })
    policy_url: Optional[str] = Field(default=None, description="""URL to the official access policy or data use agreement governing this dataset. This can provide users with direct access to the full terms and conditions for using the dataset, which can inform their understanding of legal and ethical requirements.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessPolicyClass'],
         'in_subset': ['accessibility_if_applicable']} })
    policy_text: Optional[str] = Field(default=None, description="""Inline summary if no policy_url exists. This can provide users with a quick overview of the key terms and conditions  for using the dataset, which can inform their understanding of legal and ethical requirements.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessPolicyClass'],
         'in_subset': ['accessibility_if_applicable']} })

    @field_validator('policy_url')
    def pattern_policy_url(cls, v):
        pattern=re.compile(r"^https?://.+$|^not_applicable$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid policy_url format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid policy_url format: {v}"
            raise ValueError(err_msg)
        return v


class LicenseClass(ConfiguredBaseModel):
    """
    License information for the dataset.  This describes the legal terms under which the dataset can be used,  which is critical for users to understand their rights and obligations when using the dataset. [pub] Required when release_status = approved | published. Use \"pending\" if not yet assigned.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'If spdx_id is Other, then name must be present and '
                                   'populated with the license name.',
                    'postconditions': {'slot_conditions': {'name': {'name': 'name',
                                                                    'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'spdx_id': {'equals_string': 'Other',
                                                                      'name': 'spdx_id'}}}}],
         'slot_usage': {'name': {'name': 'name', 'pattern': '^.{3,}$'}}})

    spdx_id: Optional[str] = Field(default=None, description="""The SPDX license identifier for the dataset, use the SPDX license identifier: https://spdx.org/licenses/ e.g., CC-BY-4.0 | CC0-1.0 | Apache-2.0 | MIT (e.g., \"SPDX-License-Identifier: CC-BY-4.0  Use \"other\" if not in SPDX registry.  Use \"pending\" if not yet assigned. This provides a standardized way to indicate the license for the dataset and can inform users about the legal permissions and restrictions associated with using the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['LicenseClass'], 'in_subset': ['reusability_if_applicable']} })
    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    url: Optional[str] = Field(default=None, description="""URL to the official access policy or data use agreement governing this dataset. This can provide users with direct access to the full terms and conditions for using the dataset, which can inform their understanding of legal and ethical requirements.""", json_schema_extra = { "linkml_meta": {'domain_of': ['LicenseClass', 'PreferredCitationClass'],
         'in_subset': ['reusability_if_applicable']} })
    known_contractual_rights: Optional[str] = Field(default=None, description="""Any known contractual rights or obligations associated with this dataset  that may not be fully captured by the license or access policy information. This can include information about data sharing agreements,  third-party restrictions, or other legal considerations that users should be  aware of when working with the dataset. Important because DOE/NNSA datasets may have complex contractual arrangements that  impact how the data can be used and shared beyond license terms.""", json_schema_extra = { "linkml_meta": {'domain_of': ['LicenseClass'], 'in_subset': ['reusability_if_applicable']} })

    @field_validator('name')
    def pattern_name(cls, v):
        pattern=re.compile(r"^.{3,}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('url')
    def pattern_url(cls, v):
        pattern=re.compile(r"^https?://.+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid url format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid url format: {v}"
            raise ValueError(err_msg)
        return v


class PublisherClass(NamedThing):
    """
    The publisher of the dataset, which may be an individual, organization, or other entity responsible for making the dataset available to users. This describes the publisher of the dataset, which is important for acknowledging contributions and providing contact information for users who may have questions or need support when using the dataset.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    ror_id: Optional[str] = Field(default=None, description="""The ROR identifier for an organization, in URL format (e.g., https://ror.org/03yrm5c26).""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:sameAs',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AffiliationClass',
                       'OrganizationClass',
                       'LocationClass',
                       'PublisherClass',
                       'SponsorOrganizationClass'],
         'in_subset': ['discoverability_if_applicable']} })
    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })

    @field_validator('ror_id')
    def pattern_ror_id(cls, v):
        pattern=re.compile(r"^https?://ror\.org/[a-z0-9]{9}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ror_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ror_id format: {v}"
            raise ValueError(err_msg)
        return v


class ContactClass(ConfiguredBaseModel):
    """
    Primary point of contact for questions about this dataset.  This describes who to contact for questions about the dataset,  which is important for users who may need additional information or support when using the dataset. A contact is required for all datasets, regardless of sensitivity or release status.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'person': {'name': 'person', 'required': True}}})

    person: PersonClass = Field(default=..., description="""A human individual.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AgentClass', 'ContactClass']} })
    valid_until: Optional[str] = Field(default=None, description="""Date after which this contact may no longer be valid., in ISO 8601 format (YYYY-MM-DD). Use for project-bound contacts (students, postdocs, term staff).""", json_schema_extra = { "linkml_meta": {'domain_of': ['ContactClass'], 'in_subset': ['discoverability_if_applicable']} })
    succession_note: Optional[str] = Field(default=None, description="""Who to contact if this contact is no longer reachable. e.g., \"Contact the ORNL data management office at data@ornl.gov\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['ContactClass'], 'in_subset': ['discoverability_if_applicable']} })

    @field_validator('valid_until')
    def pattern_valid_until(cls, v):
        pattern=re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid valid_until format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid valid_until format: {v}"
            raise ValueError(err_msg)
        return v


class SponsorOrganizationClass(NamedThing):
    """
    An organization that funded or sponsored the creation of the dataset. This describes the organizations that provided financial or other support for the creation of the dataset,  which is important for acknowledging contributions and understanding potential conflicts of interest.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'name': {'description': 'The name of the sponsoring '
                                                'organization. E.g., DOE Office of '
                                                'Science | NNSA | NSF',
                                 'in_subset': ['discoverability_required'],
                                 'name': 'name'},
                        'ror_id': {'description': 'The ROR ID of the sponsoring '
                                                  'organization, if available. E.g., '
                                                  'https://ror.org/02vwzrd76',
                                   'in_subset': ['discoverability_if_applicable'],
                                   'name': 'ror_id'}}})

    ror_id: Optional[str] = Field(default=None, description="""The ROR ID of the sponsoring organization, if available. E.g., https://ror.org/02vwzrd76""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:sameAs',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AffiliationClass',
                       'OrganizationClass',
                       'LocationClass',
                       'PublisherClass',
                       'SponsorOrganizationClass'],
         'in_subset': ['discoverability_if_applicable']} })
    award_number: Optional[str] = Field(default=None, description="""Award number(s) associated with the funding for this dataset. E.g., DE-AC05-00OR22725""", json_schema_extra = { "linkml_meta": {'domain_of': ['SponsorOrganizationClass'],
         'in_subset': ['discoverability_if_applicable']} })
    funding_source: Optional[FundingSourceEnum] = Field(default=None, description="""Funder or sponsor of the research that produced this dataset. From controlled vocabulary FundingSourceEnum doe_program_sc doe_program_nnsa ldrd wfo crada other_federal state_government subcontract industry nonprofit internal other""", json_schema_extra = { "linkml_meta": {'domain_of': ['SponsorOrganizationClass'],
         'in_subset': ['discoverability_if_applicable']} })
    program: Optional[str] = Field(default=None, description="""The program or initiative under which this dataset was created. E.g., 'Advanced Scientific Computing Research'""", json_schema_extra = { "linkml_meta": {'domain_of': ['SponsorOrganizationClass'],
         'in_subset': ['discoverability_if_applicable']} })
    name: str = Field(default=..., description="""The name of the sponsoring organization. E.g., DOE Office of Science | NNSA | NSF""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass'],
         'in_subset': ['discoverability_required']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })

    @field_validator('ror_id')
    def pattern_ror_id(cls, v):
        pattern=re.compile(r"^https?://ror\.org/[a-z0-9]{9}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ror_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ror_id format: {v}"
            raise ValueError(err_msg)
        return v


class TagsClass(ConfiguredBaseModel):
    """
    Structured tags for catalog filtering and discovery.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'object_type': {'description': 'The type of object described '
                                                       'by this datacard, using the '
                                                       'ObjectTypeEnum controlled '
                                                       'vocabulary. E.g., dataset | '
                                                       'model | ai_agent | eval | '
                                                       'framework | software',
                                        'in_subset': ['discoverability_if_applicable'],
                                        'name': 'object_type'}}})

    project: str = Field(default=..., description="""Single human-readable name from the project, Genesis project or sub-project this dataset belongs to. e.g., genesis | genesis-fusion | genesis-lightsource Use the same name in the datacard filename.""", json_schema_extra = { "linkml_meta": {'aliases': ['project_name', 'genesis_project', 'sub_project'],
         'domain_of': ['DatasetIdentificationClass', 'TagsClass'],
         'in_subset': ['discoverability_required']} })
    science: Optional[str] = Field(default=None, description="""More specific scientific domain, sub-discipline, or topic. e.g., \"lightsource\" | \"fusion\" | \"materials\" | \"biology\" | \"synchrotron light source science\" | \"magnetic confinement fusion\" | \"materials under extreme conditions\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['TagsClass'], 'in_subset': ['discoverability_if_applicable']} })
    object_type: ObjectTypeEnum = Field(default=..., description="""The type of object described by this datacard, using the ObjectTypeEnum controlled vocabulary. E.g., dataset | model | ai_agent | eval | framework | software""", json_schema_extra = { "linkml_meta": {'domain_of': ['TagsClass'], 'in_subset': ['discoverability_if_applicable']} })


class DataStructureClass(ConfiguredBaseModel):
    """
    Dataset Characteristics: Describes the content and characteristics of the  dataset, including its scale, format, features, modalities,  and other relevant details that help users understand what the dataset contains and how it might be used.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'formats': {'description': 'The file format(s) of the dataset, '
                                                   'using the DataFormatEnum '
                                                   'controlled vocabulary. E.g., csv | '
                                                   'json | parquet | image | text | '
                                                   'relational_database',
                                    'in_subset': ['interoperability_required'],
                                    'multivalued': True,
                                    'name': 'formats',
                                    'required': True},
                        'language': {'description': 'The language(s) represented in '
                                                    'the dataset, using the ISO 639-1 '
                                                    'language codes. E.g., en | es | '
                                                    'fr | zh',
                                     'in_subset': ['interoperability_if_applicable'],
                                     'name': 'language',
                                     'required': False}}})

    formats: list[str] = Field(default=..., description="""The file format(s) of the dataset, using the DataFormatEnum controlled vocabulary. E.g., csv | json | parquet | image | text | relational_database""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataStructureClass'],
         'in_subset': ['interoperability_required']} })
    encoding: Optional[str] = Field(default=None, description="""Character encoding for text-based formats. e.g., UTF-8 | ASCII | Latin-1
UTF-8 strongly recommended. Use not_applicable for binary formats.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataStructureClass'],
         'in_subset': ['interoperability_if_applicable']} })
    schema_version: Optional[str] = Field(default=None, description="""Version of the data schema used in this dataset.
Distinct from datacard_version. Increment when field names, types, or structure change between dataset versions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataStructureClass'],
         'in_subset': ['interoperability_if_applicable']} })
    modalities: list[str] = Field(default=..., description="""Data modalities present. e.g., \"tabular\", \"image\", \"time-series\", \"text\", \"graph\", \"point-cloud\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataStructureClass'],
         'in_subset': ['interoperability_required']} })
    features: list[FeatureClass] = Field(default=..., description="""Primary variables, fields, or features. IMPORTANT: choose ONE form and use it consistently — do not mix. For basic discoverability — flat string list: e.g., 
  name: temperature
  name: pressure
  name: timestamp
  name: label
To enhance interoperability, reuse, and AI-readiness (replace flat list above):
  name: temperature
    description: Sample temperature at time of measurement
    data_type: float           # float | int | string | boolean | datetime | other
    unit: Kelvin
    range: \"273.15 - 373.15\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataStructureClass'],
         'in_subset': ['interoperability_required']} })
    splits: Optional[list[str]] = Field(default=None, description="""Dataset splits if pre-divided. Information about training, validation, and test splits for AI/ML datasets.
Example values: train, test, validation.
This can provide important context for how the dataset is structured for machine learning tasks and can inform users about how to use the data effectively for model training and evaluation.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataStructureClass'],
         'in_subset': ['interoperability_if_applicable']} })
    language: Optional[str] = Field(default="en", description="""The language(s) represented in the dataset, using the ISO 639-1 language codes. E.g., en | es | fr | zh""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataCardClass', 'DataStructureClass'],
         'exact_mappings': ['schema:inLanguage',
                            'dcterms:language',
                            'datacite:language'],
         'ifabsent': 'string(en)',
         'in_subset': ['interoperability_if_applicable']} })
    spatial_coverage: Optional[SpatialCoverageClass] = Field(default=None, description="""Spatial coverage block for geospatial datasets, if applicable.
This can include a description and slots for the bounding box coordinates. such as bounding boxes, place names, or other location-based metadata that can inform users  about the spatial context of the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataStructureClass'],
         'in_subset': ['interoperability_if_applicable']} })
    temporal_coverage: Optional[TemporalCoverageClass] = Field(default=None, description="""Temporal coverage for time-based datasets, if applicable.
Container for elements describing the start_date and end_date of the dataset's temporal coverage in ISO 8601 format (YYYY-MM-DD). e.g., start_date=2020-01-01, end_date=2020-12-31 for a dataset covering the year 2020.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:temporalCoverage',
                            'dcterms:temporal',
                            'schema:date',
                            'dcterms:date',
                            'dcterms:coverage',
                            'datacite:dateType'],
         'domain_of': ['DataStructureClass'],
         'in_subset': ['interoperability_if_applicable']} })

    @field_validator('schema_version')
    def pattern_schema_version(cls, v):
        pattern=re.compile(r"^\d+\.\d+(\.\d+)?$|^not_applicable$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid schema_version format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid schema_version format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('language')
    def pattern_language(cls, v):
        pattern=re.compile(r"^[a-z]{2}$|^not_applicable$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid language format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid language format: {v}"
            raise ValueError(err_msg)
        return v


class FeatureClass(NamedThing):
    """
    A specific feature or variable included in the dataset, including its name, description, and data type.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    data_type: Optional[str] = Field(default=None, description="""The data type of a feature or variable, following a controlled vocabulary from  (e.g., float, int, string, boolean, datetime, other). This can provide important information about the nature of the data and can inform users about how to interpret and work with the dataset.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:dataType'],
         'domain_of': ['DomainMetadataFieldValueClass', 'FeatureClass'],
         'in_subset': ['interoperability_if_applicable']} })
    unit: Optional[str] = Field(default=None, description="""The unit of measurement for a feature, if applicable.
This can provide important context for interpreting the values of the feature and can inform users about how to work with the data effectively.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:unitText'],
         'domain_of': ['DomainMetadataFieldValueClass', 'FeatureClass'],
         'in_subset': ['interoperability_if_applicable']} })
    range: Optional[str] = Field(default=None, description="""The range of values for a feature, if applicable.
This can provide important information about the expected values for a feature  and can inform users about how to work with the data effectively.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FeatureClass'], 'in_subset': ['interoperability_if_applicable']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })


class SpatialCoverageClass(ConfiguredBaseModel):
    """
    Geographic coverage of the dataset. Use for geospatial datasets or facility-based experiments.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })
    geo_location_box: Optional[GeoLocationBoxClass] = Field(default=None, description="""Geographic bounding box for geospatial datasets, if applicable.
Container for elements describing the west_bound_longitude, east_bound_longitude, south_bound_latitude, and north_bound_latitude in decimal degrees.
e.g., west_bound_longitude=-125.0, east_bound_longitude=-66.5, south_bound_latitude=24.0, north_bound_latitude=49.0 for continental US""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:spatialCoverage', 'dcterms:spatial'],
         'domain_of': ['SpatialCoverageClass'],
         'exact_mappings': ['datacite:geoLocationBox'],
         'in_subset': ['interoperability_if_applicable']} })


class GeoLocationBoxClass(ConfiguredBaseModel):
    """
    WGS84 decimal degrees; use for area coverage.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    west_bound_longitude: Optional[float] = Field(default=None, description="""Westernmost longitude in decimal degrees for geospatial datasets.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:spatialCoverage', 'dcterms:spatial'],
         'domain_of': ['GeoLocationBoxClass'],
         'exact_mappings': ['datacite:westBoundLongitude'],
         'in_subset': ['interoperability_if_applicable']} })
    east_bound_longitude: Optional[float] = Field(default=None, description="""Easternmost longitude in decimal degrees for geospatial datasets.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:spatialCoverage', 'dcterms:spatial'],
         'domain_of': ['GeoLocationBoxClass'],
         'exact_mappings': ['datacite:eastBoundLongitude'],
         'in_subset': ['interoperability_if_applicable']} })
    south_bound_latitude: Optional[float] = Field(default=None, description="""Southernmost latitude in decimal degrees for geospatial datasets.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:spatialCoverage', 'dcterms:spatial'],
         'domain_of': ['GeoLocationBoxClass'],
         'exact_mappings': ['datacite:southBoundLatitude'],
         'in_subset': ['interoperability_if_applicable']} })
    north_bound_latitude: Optional[float] = Field(default=None, description="""Northernmost latitude in decimal degrees for geospatial datasets.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:spatialCoverage', 'dcterms:spatial'],
         'domain_of': ['GeoLocationBoxClass'],
         'exact_mappings': ['datacite:northBoundLatitude'],
         'in_subset': ['interoperability_if_applicable']} })


class TemporalCoverageClass(ConfiguredBaseModel):
    """
    Time period the dataset content represents. NOTE: distinct from dates.data_collection_start/end, which describe **when** collection occurred.  Use temporal_coverage when the dataset content represents a specific time period  (e.g., satellite imagery from June 2020), and use data_collection_start/end when the dataset  was collected over a specific time period but the content is not tied to that period  (e.g., a dataset of scientific articles collected from 2015-2020).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    start_date: Optional[str] = Field(default=None, description="""Start date of the dataset's temporal coverage in ISO 8601 format (YYYY-MM-DD).""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:temporalCoverage',
                            'dcterms:temporal',
                            'schema:date',
                            'dcterms:date',
                            'dcterms:coverage',
                            'datacite:dateType'],
         'domain_of': ['TemporalCoverageClass'],
         'in_subset': ['interoperability_if_applicable']} })
    end_date: Optional[str] = Field(default=None, description="""End date of the dataset's temporal coverage in ISO 8601 format (YYYY-MM-DD).""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:temporalCoverage',
                            'dcterms:temporal',
                            'datacite:coverage'],
         'domain_of': ['TemporalCoverageClass'],
         'in_subset': ['interoperability_if_applicable']} })

    @field_validator('start_date')
    def pattern_start_date(cls, v):
        pattern=re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid start_date format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid start_date format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('end_date')
    def pattern_end_date(cls, v):
        pattern=re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid end_date format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid end_date format: {v}"
            raise ValueError(err_msg)
        return v


class DatasetScaleClass(ConfiguredBaseModel):
    """
    The scale of the dataset, including the number (and units) of records, bytes (compressed and uncompressed).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    record_count: Optional[int] = Field(default=None, description="""The number of records or rows in the dataset, if applicable.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:size', 'dcterms:extent', 'datacite:size'],
         'domain_of': ['DatasetScaleClass'],
         'in_subset': ['accessibility_if_applicable']} })
    record_unit: Optional[str] = Field(default=None, description="""The unit of measurement for the record count (e.g., samples, files, records, timesteps, images, tokens, other).""", json_schema_extra = { "linkml_meta": {'domain_of': ['DatasetScaleClass'],
         'in_subset': ['accessibility_if_applicable']} })
    compressed_bytes: Optional[int] = Field(default=None, description="""The size of the dataset in bytes when compressed, if applicable.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:size', 'dcterms:extent', 'datacite:size'],
         'domain_of': ['DatasetScaleClass'],
         'in_subset': ['accessibility_if_applicable']} })
    uncompressed_bytes: Optional[int] = Field(default=None, description="""The size of the dataset in bytes when uncompressed, if applicable.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:size', 'dcterms:extent', 'datacite:size'],
         'domain_of': ['DatasetScaleClass'],
         'in_subset': ['accessibility_if_applicable']} })


class DatesClass(ConfiguredBaseModel):
    """
    Important dates related to the dataset, such as when it was collected, issued, or modified. This helps users understand the timeline of the dataset and its relevance to their needs.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    data_collection_start: Optional[date] = Field(default=None, description="""The date when data collection for this dataset started, in ISO 8601 format (YYYY-MM-DD).""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:date',
                            'dcterms:date',
                            'dcterms:coverage',
                            'datacite:dateType'],
         'domain_of': ['DatesClass'],
         'in_subset': ['interoperability_if_applicable']} })
    data_collection_end: Optional[date] = Field(default=None, description="""The date when data collection for this dataset ended, in ISO 8601 format (YYYY-MM-DD).""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:date',
                            'dcterms:date',
                            'dcterms:coverage',
                            'datacite:dateType'],
         'domain_of': ['DatesClass'],
         'in_subset': ['interoperability_if_applicable']} })
    issued: Optional[str] = Field(default=None, description="""The ISO 8601 (YYYY-MM-DD) date the dataset was first publicly released.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['dcterms:issued', 'datacite:dateType'],
         'domain_of': ['DatesClass'],
         'exact_mappings': ['schema:datePublished'],
         'in_subset': ['interoperability_if_applicable']} })
    modified: Optional[str] = Field(default=None, description="""The ISO 8601 (YYYY-MM-DD) date the dataset was most recently modified.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['dcterms:modified', 'datacite:dateType'],
         'domain_of': ['DatesClass'],
         'exact_mappings': ['schema:dateModified'],
         'in_subset': ['interoperability_if_applicable']} })

    @field_validator('issued')
    def pattern_issued(cls, v):
        pattern=re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid issued format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid issued format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('modified')
    def pattern_modified(cls, v):
        pattern=re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid modified format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid modified format: {v}"
            raise ValueError(err_msg)
        return v


class AccessClass(ConfiguredBaseModel):
    """
    Complete the fields you know at the time of datacard creation. Repository-assigned fields (landing pages, accession numbers, access protocols) will be populated by the managing repository or catalog system at ingest — see the REPOSITORY-MANAGED block.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    current_location: str = Field(default=..., description="""Where the data physically resides right now. Use for in-workflow data not yet deposited in a repository, or for any dataset with a known internal or external storage path.
e.g., /mnt/ecs/scientific-data/project/dataset/
e.g., /lustre/orion/proj-shared/dataset/
e.g., s3://genesis-bucket/dataset/""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessClass'], 'in_subset': ['accessibility_required']} })
    publicly_facing_landing_page_url: Optional[str] = Field(default=None, description="""A publicly facing URL that provides information about the dataset and how to access it, if available.
It may differ from the current_location if the dataset is not yet publicly released or if the current_location is an internal storage path.
This can provide users with a direct point of access for learning more about the dataset and how to obtain it, which can facilitate discovery and use of the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessClass'], 'in_subset': ['accessibility_if_applicable']} })
    intended_repositories: Optional[list[IntendedRepositoryClass]] = Field(default=None, description="""Repositories you intend to deposit or have deposited this dataset in. 
The managing repository or catalog system will resolve and populate repository-assigned fields at ingest (see repository_managed slot). 
Repositories may be institutional, project-owned, community, or national  (e.g., OSTI, Zenodo, institutional data repository, project data store).""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessClass'], 'in_subset': ['accessibility_if_applicable']} })

    @field_validator('publicly_facing_landing_page_url')
    def pattern_publicly_facing_landing_page_url(cls, v):
        pattern=re.compile(r"^https?://.+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid publicly_facing_landing_page_url format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid publicly_facing_landing_page_url format: {v}"
            raise ValueError(err_msg)
        return v


class IntendedRepositoryClass(ConfiguredBaseModel):
    """
    A repositories you intend to deposit or have deposited this dataset in.  The managing repository or catalog system will resolve and populate repository-assigned fields at ingest. Repositories may be institutional, project-owned, community, or national  (e.g., OSTI, Zenodo, institutional data repository, project data store).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'name': {'identifier': False,
                                 'name': 'name',
                                 'range': 'string',
                                 'required': True}}})

    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    access_level: AccessLevelEnum = Field(default=..., description="""The access level of the dataset, following AccessLevelEnum controlled vocabulary: open | controlled | restricted This provides important context about who can access the dataset and can inform users about potential barriers to access and use. This does not replace the authoritative source markings and metadata fields for classification, CUI, or other sensitivity designations,  which should still be filled out based on the authoritative source markings.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AccessPolicyClass', 'IntendedRepositoryClass'],
         'in_subset': ['accessibility_required']} })
    is_primary: Optional[YesNoEnum] = Field(default=None, description="""\"Yes\" | \"No\" - Whether this is the primary or authoritative location for the dataset. Only one IntendedRepository should be marked as primary. 
This can help users identify the most reliable or official source for accessing the dataset,  especially if there are multiple access points or repositories where the data is available.""", json_schema_extra = { "linkml_meta": {'domain_of': ['IntendedRepositoryClass'],
         'in_subset': ['accessibility_if_applicable']} })
    date_deposited: Optional[str] = Field(default=None, description="""The date when the dataset was deposited in the repository, in ISO 8601 format (YYYY-MM-DD).
This can provide temporal context for when the dataset became available in the repository  and can inform users about the currency of the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['IntendedRepositoryClass'],
         'in_subset': ['accessibility_if_applicable']} })
    data_services: Optional[list[DataServiceClass]] = Field(default=None, description="""APIs available for accessing the dataset, if any. This can provide users with information about programmatic access options for the dataset, which can facilitate integration into AI/ML workflows and other data processing pipelines.""", json_schema_extra = { "linkml_meta": {'domain_of': ['IntendedRepositoryClass'],
         'exact_mappings': ['dcterms:DataService'],
         'in_subset': ['accessibility_if_applicable']} })

    @field_validator('date_deposited')
    def pattern_date_deposited(cls, v):
        pattern=re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid date_deposited format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid date_deposited format: {v}"
            raise ValueError(err_msg)
        return v


class DataServiceClass(NamedThing):
    """
    Class/block to populate if a Data Service / API endpoint exists for this dataset.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    endpoint: Optional[str] = Field(default=None, description="""The URL or connection string for an API endpoint that provides access to the dataset.
This can provide users with direct access to programmatic interfaces for working with the dataset,  which can facilitate integration into AI/ML workflows and other data processing pipelines.
Useful for enabling machine-actionable data documentation.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataServiceClass'],
         'exact_mappings': ['schema:WebAPI'],
         'in_subset': ['accessibility_if_applicable']} })
    documentation_url: Optional[str] = Field(default=None, description="""URL to documentation for the API or access method.
This can provide users with important information about how to use the API or access method effectively,  which can facilitate integration into AI/ML workflows and other data processing pipelines.
Useful for enabling machine-actionable data documentation.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataServiceClass'],
         'in_subset': ['accessibility_if_applicable']} })
    authentication: Optional[AuthenticationTypeEnum] = Field(default=None, description="""Whether authentication is required to access the dataset through this endpoint. This can inform users about potential barriers to access and can help them prepare for any necessary credentials or permissions needed to work with the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataServiceClass'],
         'in_subset': ['accessibility_if_applicable']} })
    version: Optional[str] = Field(default=None, description="""Version of software, tool, or library.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIModelClass',
                       'SoftwareClass',
                       'SchemaReferenceClass',
                       'DatasetIdentificationClass',
                       'DataServiceClass']} })
    rate_limit: Optional[str] = Field(default=None, description="""Any rate limits or access restrictions for the API endpoint. e.g.,  \"1000 requests/hour\",  \"5000 requests/day\",  \"1000 requests/hour and no more than 100 concurrent connections\"
This can inform users about potential limitations on how frequently they can access the dataset  through the API, which can help them plan their data processing and analysis workflows accordingly.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataServiceClass'],
         'in_subset': ['accessibility_if_applicable']} })
    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })

    @field_validator('endpoint')
    def pattern_endpoint(cls, v):
        pattern=re.compile(r"^https?://.+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid endpoint format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid endpoint format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('documentation_url')
    def pattern_documentation_url(cls, v):
        pattern=re.compile(r"^https?://.+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid documentation_url format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid documentation_url format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('version')
    def pattern_version(cls, v):
        pattern=re.compile(r"^\d+\.\d+(\.\d+)?$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid version format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid version format: {v}"
            raise ValueError(err_msg)
        return v


class ProvenanceClass(ConfiguredBaseModel):
    """
    Provenance information about the dataset, including its origin, history, and any transformations/processing it has undergone. Describes how this dataset was created, what it was derived from, and what processing was applied. This helps users understand the lineage of the dataset and assess its reliability and suitability  for their needs, and can facilitate reuse and reproducibility.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    was_generated_by: str = Field(default=..., description="""High-level description of the generating process. Even a one-line answer dramatically improves catalog value.
e.g., \"Neutron scattering experiment at SNS Beamline 1B\"
e.g., \"Monte Carlo simulation using MCNP 6.2\"
e.g., \"Derived from raw telemetry via calibration pipeline v2.1\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceClass'], 'in_subset': ['interoperability_required']} })
    source_data: Optional[list[SourceDatasetClass]] = Field(default=None, description="""Source datasets this dataset was derived from. 
Uses the SourceDatasetClass block to capture the relationship and provenance information  about the source datasets.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceClass'],
         'in_subset': ['interoperability_if_applicable']} })
    processing_steps: str = Field(default=..., description="""Key processing, cleaning, calibration, or transformation steps applied to produce this dataset.
Describe any processing steps, transformations, or cleaning that have been applied to the dataset.
This can provide important context for understanding the dataset and can inform users  about its reliability and suitability for their intended use.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceClass'], 'in_subset': ['interoperability_required']} })
    instrumentation: Optional[str] = Field(default=None, description="""Instruments, sensors, detectors, or equipment used to collect the data, if applicable. Include make, model, and version where relevant. e.g., \"Neutron scattering experiment using a He-3 position-sensitive detector at SNS Beamline 1B\" e.g., \"Data collected using a Tektronix TDS2024C oscilloscope\" e.g., \"Satellite remote sensing data from the MODIS instrument on the Terra satellite\" This can provide important context for understanding the dataset and can inform users  about its reliability and suitability for their intended use.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceClass'],
         'in_subset': ['interoperability_if_applicable']} })
    simulation_details: Optional[str] = Field(default=None, description="""For simulation-derived data: code, simulation setup, version, key parameters, and configuration for simulated datasets, if applicable.
e.g., \"Monte Carlo simulation using MCNP 6.2 with a 10x10x10 grid, 1 million particles, and physics models X, Y, Z\"
e.g., \"Molecular dynamics simulation using LAMMPS version 3Mar2020 with the following input script: ...\"
e.g., \"Climate model simulation using the Community Earth System Model (CESM) version 2.1 with the following configuration: ...\"
This can provide important context for understanding the dataset and can inform users about its reliability and suitability for their intended use.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceClass'],
         'in_subset': ['interoperability_if_applicable']} })
    software_environment: Optional[SoftwareEnvironmentClass] = Field(default=None, description="""Software environment block used to generate or process this dataset,  using SoftwareEnvironmentClass to capture details about os, container, and hpc environment.
Captures what is needed for computational reproducibility , including software environment details  for datasets that are generated or processed using specific software tools, if applicable.
This can provide important context for understanding the dataset and can inform users  about its reliability and suitability for their intended use.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceClass'],
         'in_subset': ['interoperability_if_applicable']} })


class DatasetClass(NamedThing):
    """
    Source dataset the dataset described in the datacard was derived from.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    identifier: IdentifierClass = Field(default=..., description="""A unique identifier for the datacard document itself, following the format: \"doi: distinct from the dataset identifier. Assign if the datacard is registered in a catalog or repository independently of the dataset.""", json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'broad_mappings': ['schema:identifier',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AIModelClass',
                       'SoftwareClass',
                       'NamedIdentifierClass',
                       'DatasetClass'],
         'in_subset': ['interoperability_if_applicable']} })
    relationship: Optional[RelationshipTypeEnum] = Field(default=None, description="""Relationship to other datasets or resources, if any.
E.g.s, \"is_derived_from\", \"is_based_on\", \"is_part_of\", \"has_part\", \"references\", \"other\"
This can include links to related datasets, publications, software, or other resources that are relevant to understanding and using the dataset effectively.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PublicationIdentifierClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DatasetClass'],
         'in_subset': ['interoperability_if_applicable']} })
    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })


class SourceDatasetClass(DatasetClass):
    """
    A source dataset that the dataset described in this datacard was derived from,  including its identifier and relationship to the current dataset.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    identifier: IdentifierClass = Field(default=..., description="""A unique identifier for the datacard document itself, following the format: \"doi: distinct from the dataset identifier. Assign if the datacard is registered in a catalog or repository independently of the dataset.""", json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'broad_mappings': ['schema:identifier',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['AIModelClass',
                       'SoftwareClass',
                       'NamedIdentifierClass',
                       'DatasetClass'],
         'in_subset': ['interoperability_if_applicable']} })
    relationship: Optional[RelationshipTypeEnum] = Field(default=None, description="""Relationship to other datasets or resources, if any.
E.g.s, \"is_derived_from\", \"is_based_on\", \"is_part_of\", \"has_part\", \"references\", \"other\"
This can include links to related datasets, publications, software, or other resources that are relevant to understanding and using the dataset effectively.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PublicationIdentifierClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DatasetClass'],
         'in_subset': ['interoperability_if_applicable']} })
    name: str = Field(default=..., description="""Human-readable name or local string key for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'AffiliationClass',
                       'AIModelClass',
                       'SoftwareClass',
                       'DomainMetadataFieldValueClass',
                       'NamedIdentifierClass',
                       'LicenseClass',
                       'FeatureClass',
                       'IntendedRepositoryClass']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })


class SoftwareEnvironmentClass(ConfiguredBaseModel):
    """
    Software environment used to generate or process this dataset.  Captures what is needed for computational reproducibility.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    os: Optional[str] = Field(default=None, description="""Operating system used in the software environment for generating or processing this dataset, if applicable.
e.g., \"RHEL 8.6\" | \"Ubuntu 22.04\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['SoftwareEnvironmentClass'],
         'in_subset': ['interoperability_if_applicable']} })
    compiler: Optional[str] = Field(default=None, description="""Compiler used in the software environment for generating or processing this dataset, if applicable.
e.g., \"GCC 11.3.0\" | \"Intel oneAPI 2023.1\" | \"Clang 14.0.6\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['SoftwareEnvironmentClass'],
         'in_subset': ['interoperability_if_applicable']} })
    container: Optional[str] = Field(default=None, description="""Containerization technology used in the software environment  for generating or processing this dataset, if applicable.
e.g., docker://registry/image:tag | singularity://registry/image:tag | \"Docker 20.10.12\" | \"Singularity 3.8.7\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['SoftwareEnvironmentClass'],
         'in_subset': ['interoperability_if_applicable']} })
    hpc_environment: Optional[str] = Field(default=None, description="""HPC environment or platform used in the software environment for generating or processing this dataset, if applicable.
e.g., \"module load python/3.10 cuda/11.8 openmpi/4.1\"
e.g., \"Orion HPC at Oak Ridge National Laboratory sourcing the following environment modules...\"
e.g., \"Summit HPC at Oak Ridge National Laboratory sourcing the following environment modules...\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['SoftwareEnvironmentClass'],
         'in_subset': ['interoperability_if_applicable']} })
    notes: Optional[str] = Field(default=None, description="""Additional environment details, key library versions, or reference to a full environment manifest.
e.g., \"See requirements.txt in dataset root\"
e.g., \"numpy 1.24, pytorch 2.0.1, h5py 3.8.0\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['SoftwareEnvironmentClass'],
         'in_subset': ['interoperability_if_applicable']} })


class StewardshipClass(ConfiguredBaseModel):
    """
    Stewardship & Versioning:
    This block describes how the dataset is stewarded and how its versioning is managed over time,  which is important for maintaining the dataset, tracking changes, and ensuring users can access the most up-to-date information. NOTE ON VERSIONING: Three fields work together to describe versioning:
    discoverability.identification.version        — the version number of this dataset
    discoverability.identification.supersedes /
    discoverability.identification.superseded_by  — links to prior and successor versions
    **reusability.stewardship.versioning_strategy — how versioning is managed over time**
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'level': {'description': 'The stewardship level of the dataset '
                                                 'from a controlled vocabulary, '
                                                 'StewardshipLevelEnum, indicating the '
                                                 'management level of stewardship.',
                                  'in_subset': ['reusability_if_applicable'],
                                  'name': 'level',
                                  'range': 'StewardshipLevelEnum'},
                        'versioning_strategy': {'description': 'The strategy for '
                                                               'managing dataset '
                                                               'versions over time, '
                                                               'such as semantic '
                                                               'versioning, date-based '
                                                               'versioning, or custom '
                                                               'versioning schemes.',
                                                'name': 'versioning_strategy'}}})

    level: Optional[StewardshipLevelEnum] = Field(default=None, description="""The stewardship level of the dataset from a controlled vocabulary, StewardshipLevelEnum, indicating the management level of stewardship.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StewardshipClass'], 'in_subset': ['reusability_if_applicable']} })
    maintainer: Optional[AgentClass] = Field(default=None, description="""Person or organization responsible for ongoing maintenance of the dataset over time, if different from the contact.
This can provide users with a point of contact for ongoing maintenance and updates to the dataset,  which can facilitate communication and support responsible use of the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StewardshipClass'], 'in_subset': ['reusability_if_applicable']} })
    update_frequency: Optional[UpdateFrequencyEnum] = Field(default=None, description="""How often the dataset is updated or expected to be updated, if applicable.
Controlled vocab includes \"none\", \"ad_hoc\", \"monthly\", \"quarterly\", \"annually\", \"continuously\", \"other\"
This can inform users about the currency of the dataset and can help them plan for when new data may become available.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StewardshipClass'], 'in_subset': ['reusability_if_applicable']} })
    retention_policy: Optional[str] = Field(default=None, description="""Information about the dataset's retention policy, including how long the dataset will be retained  and any conditions for its removal or archiving.
e.g., \"Retained for 10 years per DOE data management policy\"
This can provide users with important information about the longevity of the dataset  and can inform their decisions about using and citing the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StewardshipClass'], 'in_subset': ['reusability_if_applicable']} })
    versioning_strategy: Optional[str] = Field(default=None, description="""The strategy for managing dataset versions over time, such as semantic versioning, date-based versioning, or custom versioning schemes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StewardshipClass'], 'in_subset': ['reusability_if_applicable']} })


class NonSensitivityGovMetadataClass(ConfiguredBaseModel):
    """
    Governance-relevant metadata that may affect sharing/use decisions but is not part of the source sensitivity/marking block itself.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    export_control: ExportControlClass = Field(default=..., description="""Includes fields related to export control considerations for the dataset, if applicable.
This can provide users with important information about any export control restrictions or requirements that may apply to the dataset,  which can inform their decisions about using and sharing the data responsibly.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NonSensitivityGovMetadataClass'],
         'in_subset': ['governed_use_required']} })
    privacy: PrivacyClass = Field(default=..., description="""Includes fields related to privacy considerations for the dataset, if applicable.
This can provide users with important information about any privacy restrictions or requirements that may apply to the dataset,  which can inform their decisions about using and sharing the data responsibly.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NonSensitivityGovMetadataClass'],
         'in_subset': ['governed_use_required']} })
    rights_release_records: RightsReleaseRecordsClass = Field(default=..., description="""Information about rights release records for the dataset, if applicable.
This can provide users with important information about any rights or permissions associated with the dataset,  which can inform their decisions about using and sharing the data responsibly.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NonSensitivityGovMetadataClass'],
         'in_subset': ['governed_use_required']} })


class ExportControlClass(ConfiguredBaseModel):
    """
    Export control information for the dataset, which describes any export control restrictions that apply to the dataset,  which is critical for users to understand any legal restrictions on sharing or using the dataset across international borders.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'If export_control_status = "Yes", '
                                   'export_control_basis is required. ',
                    'postconditions': {'slot_conditions': {'export_control_basis': {'name': 'export_control_basis',
                                                                                    'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'export_control_status': {'equals_string': 'Yes',
                                                                                    'name': 'export_control_status'}}}}],
         'slot_usage': {'export_control_basis': {'name': 'export_control_basis',
                                                 'required': False},
                        'export_control_status': {'name': 'export_control_status',
                                                  'required': True},
                        'foreign_national_access_status': {'name': 'foreign_national_access_status',
                                                           'required': False}}})

    export_control_status: YesNoPendingUnknownEnum = Field(default=..., description="""The export control status of the dataset, following a controlled vocabulary:  \"Yes\" | \"No\" | \"pending_review\" | \"unknown\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExportControlClass'], 'in_subset': ['governed_use_required']} })
    export_control_basis: Optional[ExportControlBasisEnum] = Field(default=None, description="""The basis for the export control status, if applicable, following a controlled vocabulary: ITAR | EAR | DOE_Nuclear_Export_Control | Other | not_applicable""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExportControlClass'],
         'in_subset': ['governed_use_if_applicable']} })
    foreign_national_access_status: Optional[ForeignNationalAccessStatusEnum] = Field(default=None, description="""Governance-facing outcome field indicating whether foreign national access is allowed, restricted, prohibited, or conditional, based on the combined effect of applicable export, classification, dissemination, agreement, or other source-authoritative constraints. This is not an export-only field.
Controlled vocabulary: Allowed | Restricted | Prohibited | Conditional | Unknown""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExportControlClass'],
         'in_subset': ['governed_use_if_applicable']} })


class PrivacyClass(ConfiguredBaseModel):
    """
    Privacy information for the dataset, which describes any privacy considerations or restrictions that apply to the dataset,  which is critical for users to understand any ethical or legal considerations related to the dataset, especially if it contains personally identifiable information (PII) or protected health information (PHI).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'phi_status': {'name': 'phi_status', 'required': False},
                        'pii_status': {'name': 'pii_status', 'required': True},
                        'privacy_control_basis': {'name': 'privacy_control_basis',
                                                  'required': False},
                        'privacy_regime_notes': {'name': 'privacy_regime_notes',
                                                 'required': False},
                        'privacy_status': {'name': 'privacy_status', 'required': True}}})

    privacy_status: YesNoPendingUnknownEnum = Field(default=..., description="""The privacy status of the dataset, following a controlled vocabulary (use quotes to distinguish from boolean values): \"Yes\" | \"No\" | \"Pending_Review\" | \"Unknown\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['PrivacyClass'], 'in_subset': ['governed_use_required']} })
    pii_status: YesNoPendingUnknownEnum = Field(default=..., description="""Whether the dataset contains personally identifiable information (PII), following a controlled vocabulary (use quotes to distinguish from boolean values):  \"Yes\" | \"No\" | \"Pending_Review\" | \"Unknown\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['PrivacyClass'], 'in_subset': ['governed_use_required']} })
    phi_status: Optional[YesNoPendingUnknownEnum] = Field(default=None, description="""Whether the dataset contains protected health information (PHI), following a controlled vocabulary (use quotes to distinguish from boolean values):  \"Yes\" | \"No\" | \"Pending_Review\" | \"Unknown\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['PrivacyClass'], 'in_subset': ['governed_use_required']} })
    privacy_control_basis: Optional[list[PrivacyControlBasisEnum]] = Field(default=None, description="""The basis for the privacy status, if applicable.
List all that apply from the following controlled vocabulary: HIPPA | Privacy_Act | Human_Subjects | Other_Regulated_Privacy | Site_Specific | not_applicable""", json_schema_extra = { "linkml_meta": {'domain_of': ['PrivacyClass'], 'in_subset': ['governed_use_if_applicable']} })
    privacy_regime_notes: Optional[str] = Field(default=None, description="""Optional notes for privacy regimes or handling nuances not captured by controlled values.
This can provide users with important context about the privacy considerations and requirements that may apply to the dataset,  which can inform their decisions about using and sharing the data responsibly.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PrivacyClass'], 'in_subset': ['governed_use_if_applicable']} })


class RightsReleaseRecordsClass(ConfiguredBaseModel):
    """
    Information about rights, release, and records status for the dataset, which describes any legal or administrative considerations related to the dataset, such as copyright status, release status, and records management status.
    This is important for users to understand any legal or administrative considerations related to the dataset, which may affect how the dataset can be used, shared, or cited.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'If agreement_required = "Yes", agreement_type must '
                                   'contain at least one value.',
                    'postconditions': {'slot_conditions': {'agreement_type': {'name': 'agreement_type',
                                                                              'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'agreement_required': {'equals_string': 'Yes',
                                                                                 'name': 'agreement_required'}}}}]})

    ip_restriction_type: Optional[IPRestrictionTypeEnum] = Field(default=None, description="""The type of intellectual property (IP) restriction that applies to the dataset, if any. 
Select one from the following controlled vocabulary: Proprietary | Limited_Rights | Restricted_Rights | Government_Purpose_Rights | Unlimited_Rights | Third_Party_Licensed | None""", json_schema_extra = { "linkml_meta": {'domain_of': ['RightsReleaseRecordsClass'],
         'in_subset': ['governed_use_if_applicable']} })
    agreement_required: YesNoEnum = Field(default=..., description="""\"Yes\" | \"No\" - Whether an agreement (e.g., data use agreement, license agreement, nondisclosure agreement) is required to access or use the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['RightsReleaseRecordsClass'],
         'in_subset': ['governed_use_required']} })
    agreement_type: Optional[AgreementTypeEnum] = Field(default=None, description="""The type of agreement required to access or use the dataset, if applicable, following a controlled vocabulary: DUA | CRADA | MOU | NDA | LICENSE | WFO | OTHER""", json_schema_extra = { "linkml_meta": {'domain_of': ['RightsReleaseRecordsClass'],
         'in_subset': ['governed_use_if_applicable']} })
    public_release_status: PublicReleaseStatusEnum = Field(default=..., description="""The public release status of the dataset.  Select one from the following controlled vocabulary: \"Approved\" | \"Pending\" | \"Not_Approved\" | \"Requires_STI_Review\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['RightsReleaseRecordsClass'],
         'in_subset': ['governed_use_required']} })
    record_status: RecordStatusEnum = Field(default=..., description="""The record status of the dataset. 
Select one from the following controlled vocabulary: federal_record | contractor_record | non_record | mixed | unknown""", json_schema_extra = { "linkml_meta": {'domain_of': ['RightsReleaseRecordsClass'],
         'in_subset': ['governed_use_required']} })


class SpecificReviewClass(ConfiguredBaseModel):
    """
    An individual review or quality assessment of the dataset.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    source_review_reference: str = Field(default=..., description="""Identifier or citation for the authoritative review/release/source document.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SpecificReviewClass'],
         'in_subset': ['governed_use_if_applicable']} })
    review_purpose: Optional[str] = Field(default=None, description="""The purpose or focus of the review, such as export control, IRB, security, quality assessment, or other.
This can provide users with important context about the nature of the review and what aspects of the dataset were evaluated,  which can inform their understanding of the dataset's quality and reliability.
e.g., \"Export control review prior to public release\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['SpecificReviewClass'],
         'in_subset': ['governed_use_if_applicable']} })
    source_review_authority: Optional[str] = Field(default=None, description="""Office, system, or authority of record for the source sensitivity determination.
This can provide users with information about the official authority responsible for the review,  which can inform their confidence in the dataset's quality and reliability.
e.g., \"DOE Office of Export Control\" | \"Institutional Review Board at XYZ University\" | \"Internal security review board\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['SpecificReviewClass'],
         'in_subset': ['governed_use_if_applicable']} })
    review_contact_name: Optional[str] = Field(default=None, description="""Human point of contact, if appropriate to capture.
This can provide users with a point of contact for questions about the review process and its outcomes,  which can facilitate communication and support responsible use of the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SpecificReviewClass'],
         'in_subset': ['governed_use_if_applicable']} })
    review_contact_email: Optional[str] = Field(default=None, description="""Contact email, if appropriate to capture.
This can provide users with a point of contact for questions about the review process and its outcomes,  which can facilitate communication and support responsible use of the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SpecificReviewClass'],
         'in_subset': ['governed_use_if_applicable']} })
    reviewed_by: Optional[AgentClass] = Field(default=None, description="""Person or role responsible for conducting the review, if applicable.
This can provide users with information about the expertise and credibility of the reviewers,  which can inform their confidence in the dataset's quality and reliability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SpecificReviewClass'],
         'in_subset': ['governed_use_if_applicable']} })
    decontrol_or_declassify_on: Optional[str] = Field(default=None, description="""For sensitive datasets, the date when the dataset can be decontrolled or declassified, if applicable.
This can provide users with information about when the dataset may become more widely available and can inform their decisions about using and citing the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SpecificReviewClass'],
         'in_subset': ['governed_use_if_applicable']} })
    review_date: Optional[str] = Field(default=None, description="""The date when the review was conducted or completed, in ISO 8601 format (YYYY-MM-DD). This can provide users with temporal context for when the review took place, which can inform their understanding of the dataset's quality and reliability at that point in time.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SpecificReviewClass'],
         'in_subset': ['governed_use_if_applicable']} })
    comments: Optional[str] = Field(default=None, description="""Additional comments or notes about the review, if any.
This can provide users with additional context and insights about the review process and its outcomes,  which can inform their understanding of the dataset's quality and reliability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SpecificReviewClass'],
         'in_subset': ['governed_use_if_applicable']} })

    @field_validator('decontrol_or_declassify_on')
    def pattern_decontrol_or_declassify_on(cls, v):
        pattern=re.compile(r"^(\d{4}-\d{2}-\d{2}|not_applicable)$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid decontrol_or_declassify_on format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid decontrol_or_declassify_on format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('review_date')
    def pattern_review_date(cls, v):
        pattern=re.compile(r"^(\d{4}-\d{2}-\d{2}|not_applicable)$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid review_date format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid review_date format: {v}"
            raise ValueError(err_msg)
        return v


class RelatedResourcesClass(ConfiguredBaseModel):
    """
    Related resources, such as publications, code repositories, or other datasets that are related to the dataset described in this datacard. This helps users find additional information and resources related to the dataset, which can enhance their understanding and ability to use the dataset effectively.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    datasets: Optional[list[DatasetClass]] = Field(default=None, description="""Related datasets, if any. 
This can include links to other datasets that are relevant to understanding and using the dataset effectively,  such as source datasets, derived datasets, or complementary datasets.""", json_schema_extra = { "linkml_meta": {'domain_of': ['RelatedResourcesClass'],
         'in_subset': ['interoperability_if_applicable']} })
    publications: Optional[list[PublicationIdentifierClass]] = Field(default=None, description="""Publications associated with this dataset, if any. 
This can include links to scholarly articles, conference papers, or other publications that describe the dataset or its use,  which can provide users with additional context and insights about the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['RelatedResourcesClass'],
         'in_subset': ['interoperability_if_applicable']} })
    software: Optional[list[SoftwareClass]] = Field(default=None, description="""Software associated with this dataset, if any. 
This can include links to software tools, libraries, or frameworks that were used to generate, process, or analyze the dataset,  which can provide users with additional context and insights about the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AgentClass', 'RelatedResourcesClass'],
         'in_subset': ['interoperability_if_applicable']} })
    ai_models: Optional[list[AIModelClass]] = Field(default=None, description="""AI models associated with this dataset, if any. 
This can include links to AI models that were trained on, evaluated using, or otherwise related to the dataset,  which can provide users with additional context and insights about the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['RelatedResourcesClass'],
         'in_subset': ['interoperability_if_applicable']} })


class ComplianceClass(ConfiguredBaseModel):
    """
    Populate when release_status = under_review | approved | published.
    Fields/slots marked [sensitive] are additionally required for the sensitive profile.
    Leave blank or omit for draft and in-workflow datasets.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    doe_data_management_plan: YesNoUnknownNotApplicableEnum = Field(default=..., description="""\"Yes\"|\"No\"|\"Unknown\"|\"not_applicable\" — Whether the dataset is in compliance with a DOE Data Management Plan (DMP), if applicable.
This can provide users with information about the dataset's data management practices and can inform their confidence in the dataset's quality and reliability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComplianceClass'], 'in_subset': ['governed_use_required']} })
    osti_elink2_metadata_compliant: YesNoUnknownNotApplicableEnum = Field(default=..., description="""\"Yes\"|\"No\"|\"Unknown\"|\"not_applicable\" — Whether the dataset is compliant with OSTI's E-Link 2.0 metadata requirements, if applicable.
This can provide users with information about the dataset's adherence to OSTI's metadata standards,  which can inform their confidence in the dataset's quality and reliability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComplianceClass'], 'in_subset': ['governed_use_required']} })
    irb_approved: YesNoUnknownNotApplicableEnum = Field(default=..., description="""\"Yes\"|\"No\"|\"Unknown\"|\"not_applicable\" — Whether the dataset has been approved by an Institutional Review Board (IRB), if applicable.
This can provide users with information about the ethical considerations and protections associated with the dataset,  which can inform their confidence in the dataset's quality and reliability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComplianceClass'], 'in_subset': ['governed_use_required']} })


class CitationClass(ConfiguredBaseModel):
    """
    Populate when release_status = approved | published. Replace ALL ${...} placeholders in the BibTeX block below before publishing.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    report_number: Optional[str] = Field(default=None, description="""Report number or other unique identifier for the dataset, if applicable.
e.g., SAND2024-XXXXX | LAUR-XX-XXXXX | ORNL/TM-2024/XXXXX
This can provide users with an additional identifier for the dataset that can be used  in citations and references.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CitationClass'], 'in_subset': ['reusability_if_applicable']} })
    preferred_citation: Optional[PreferredCitationClass] = Field(default=None, description="""Fields that can be used to create full recommended citation in bibtex format for the dataset, if applicable.
The fields author, title, year, publisher are required if preferred_citation is provided.
At least one of doi or url must be provided if preferred_citation is provided.
This can provide users with a recommended citation format for the dataset,  which can facilitate proper attribution and recognition for the creators and maintainers of the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CitationClass'], 'in_subset': ['reusability_if_applicable']} })


class PreferredCitationClass(ConfiguredBaseModel):
    """
    The preferred citation for this dataset, including a human-readable citation string and a structured BibTeX entry that can be used for programmatic citation generation. This helps ensure that users can properly cite the dataset in their work, which is important for giving credit to the creators of the dataset and for enabling others to find and access the dataset based on citations in the literature.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'slot_usage': {'url': {'description': 'A url that resolves to the dataset '
                                               'landing page or other primary '
                                               'reference for the dataset, which can '
                                               'be used in citations and for users to '
                                               'access the dataset. url: is intended '
                                               'to correspond to the bibtex url field, '
                                               'and should be populated with the same '
                                               'value.',
                                'name': 'url',
                                'required': False}}})

    author: str = Field(default=..., description="""Author(s) of the dataset, if applicable.  author: is intended as a component of a bibtex citation when preferred_citation is provided.
Required when a preferred_citation is provided.
This can provide users with information about the creators of the dataset,  which can inform their confidence in the dataset's quality and reliability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PreferredCitationClass'],
         'in_subset': ['reusability_if_applicable']} })
    title: str = Field(default=..., description="""Title of the dataset, if applicable. title: is intended as a component of a bibtex citation when preferred_citation is provided.
Required when a preferred_citation is provided.
This can provide users with information about the dataset and can inform their understanding of its content and focus.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PreferredCitationClass'],
         'in_subset': ['reusability_if_applicable']} })
    year: str = Field(default=..., description="""Year of publication or release of the dataset, if applicable. year: is intended as a component of a bibtex citation when preferred_citation is provided
Required when a preferred_citation is provided.
This can provide users with temporal context for the dataset, which can inform their understanding of its relevance and currency.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PreferredCitationClass'],
         'in_subset': ['reusability_if_applicable']} })
    publisher: Optional[str] = Field(default=None, description="""Publisher or distributing organization for the dataset, if applicable. publisher: is intended as a component of a bibtex citation when preferred_citation is provided
Required when a preferred_citation is provided.
This can provide users with information about the organization responsible for distributing the dataset,""", json_schema_extra = { "linkml_meta": {'domain_of': ['PreferredCitationClass'],
         'in_subset': ['reusability_if_applicable']} })
    howpublished: Optional[str] = Field(default=None, description="""How the dataset was published or released, if applicable (e.g., \"Online\", \"In Repository\", \"As Supplementary Material\"). how_published: is intended as a component of a bibtex citation when preferred_citation is provided
This can provide users with information about how the dataset was made available,  which can inform their understanding of its accessibility and potential use cases.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PreferredCitationClass'],
         'in_subset': ['reusability_if_applicable']} })
    doi: Optional[str] = Field(default=None, description="""Digital Object Identifier (DOI) for the dataset, if applicable. doi: is intended as a component of a bibtex citation when preferred_citation is provided
Required when a preferred_citation is provided.
This can provide users with a persistent identifier for the dataset that can be used in citations and references.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PreferredCitationClass'],
         'in_subset': ['reusability_if_applicable']} })
    url: Optional[str] = Field(default=None, description="""A url that resolves to the dataset landing page or other primary reference for the dataset, which can be used in citations and for users to access the dataset. url: is intended to correspond to the bibtex url field, and should be populated with the same value.""", json_schema_extra = { "linkml_meta": {'domain_of': ['LicenseClass', 'PreferredCitationClass'],
         'in_subset': ['reusability_if_applicable']} })
    eprinttype: Optional[str] = Field(default=None, description="""The type of eprint identifier provided in the url field, if applicable (e.g., arXiv, report_number, pubmed). eprinttype: is intended as a component of a bibtex citation when preferred_citation is provided.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PreferredCitationClass'],
         'in_subset': ['reusability_if_applicable']} })
    eprint: Optional[str] = Field(default=None, description="""The eprint identifier for the dataset, if applicable (e.g., 1234.56789, SAND2024-XXXXX). Value with correspond to the format of the eprinttype provided (e.g., arXiv, report_number, pubmed). eprint: is intended as a component of a bibtex citation when preferred_citation is provided.
This can provide users with an additional identifier for the dataset that can be used in citations and references.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PreferredCitationClass'],
         'in_subset': ['reusability_if_applicable']} })
    note: Optional[str] = Field(default=None, description="""Additional notes related to the preferred citation, if any. Is intended to align with bibtex \"note\" field when preferred_citation is provided. For legacy bibtex entries that don't accept eprinttype and eprint and that need to support an ark or other identifiers that don't fit cleanly into the existing fields, the note field can be used to capture this information in a free-text format. include a note: field use this format for the note field: note: Available at ark:/12345/abcde
This can provide users with additional context and information about the preferred citation for the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PreferredCitationClass'],
         'in_subset': ['reusability_if_applicable']} })

    @field_validator('year')
    def pattern_year(cls, v):
        pattern=re.compile(r"^\d{4}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid year format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid year format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('url')
    def pattern_url(cls, v):
        pattern=re.compile(r"^https?://.+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid url format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid url format: {v}"
            raise ValueError(err_msg)
        return v


class AIUsageClass(ConfiguredBaseModel):
    """
    AI / ML Usage:
    Describes whether and how this dataset may be used in AI/ML workflows. 
    Be explicit — these fields are read by automated pipeline tooling and AI agents.
    Conditions are required if the corresponding status for training use, inference use, or evaluation use is \"Conditional\".
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'If training_use_status = "Conditional", then '
                                   'training_use_conditions must be present.',
                    'postconditions': {'slot_conditions': {'training_use_conditions': {'name': 'training_use_conditions',
                                                                                       'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'training_use_status': {'equals_string': 'Conditional',
                                                                                  'name': 'training_use_status'}}}},
                   {'description': 'If inference_use_status = "Conditional", then '
                                   'inference_use_conditions must be present.',
                    'postconditions': {'slot_conditions': {'inference_use_conditions': {'name': 'inference_use_conditions',
                                                                                        'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'inference_use_status': {'equals_string': 'Conditional',
                                                                                   'name': 'inference_use_status'}}}},
                   {'description': 'If evaluation_use_status = "Conditional", then '
                                   'evaluation_use_conditions must be present.',
                    'postconditions': {'slot_conditions': {'evaluation_use_conditions': {'name': 'evaluation_use_conditions',
                                                                                         'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'evaluation_use_status': {'equals_string': 'Conditional',
                                                                                    'name': 'evaluation_use_status'}}}}],
         'slot_usage': {'evaluation_use_status': {'description': 'The status of '
                                                                 'whether this dataset '
                                                                 'can be used for '
                                                                 'evaluation in AI/ML '
                                                                 'workflows. "Yes" | '
                                                                 '"No" | "Conditional"',
                                                  'name': 'evaluation_use_status',
                                                  'required': True},
                        'inference_use_status': {'description': 'The status of whether '
                                                                'this dataset can be '
                                                                'used for inference in '
                                                                'AI/ML workflows. '
                                                                '"Yes" | "No" | '
                                                                '"Conditional"',
                                                 'name': 'inference_use_status',
                                                 'required': True},
                        'training_use_status': {'description': 'The status of whether '
                                                               'this dataset can be '
                                                               'used for training in '
                                                               'AI/ML workflows. "Yes" '
                                                               '| "No" | "Conditional"',
                                                'name': 'training_use_status',
                                                'required': True}}})

    training_use_status: YesNoConditionalEnum = Field(default=..., description="""The status of whether this dataset can be used for training in AI/ML workflows. \"Yes\" | \"No\" | \"Conditional\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIUsageClass'], 'in_subset': ['ai_usability_required']} })
    training_use_conditions: Optional[str] = Field(default=None, description="""If training_use_status = \"Conditional\", this field is required and describes the specific conditions or restrictions that must be met for the dataset to be used for training AI models. This can provide users with important information about any limitations or considerations they should be aware of when using the dataset for training AI models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIUsageClass'], 'in_subset': ['ai_usability_if_applicable']} })
    inference_use_status: YesNoConditionalEnum = Field(default=..., description="""The status of whether this dataset can be used for inference in AI/ML workflows. \"Yes\" | \"No\" | \"Conditional\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIUsageClass'], 'in_subset': ['ai_usability_required']} })
    inference_use_conditions: Optional[str] = Field(default=None, description="""If inference_use_status = \"Conditional\", this field is required and describes the specific conditions or restrictions that must be met for the dataset to be used for inference with AI models. This can provide users with important information about any limitations or considerations they should be aware of when using the dataset for inference with AI models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIUsageClass'], 'in_subset': ['ai_usability_if_applicable']} })
    evaluation_use_status: YesNoConditionalEnum = Field(default=..., description="""The status of whether this dataset can be used for evaluation in AI/ML workflows. \"Yes\" | \"No\" | \"Conditional\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIUsageClass'], 'in_subset': ['ai_usability_required']} })
    evaluation_use_conditions: Optional[str] = Field(default=None, description="""If evaluation_use_status = \"Conditional\", this field is required and describes the specific conditions or restrictions that must be met for the dataset to be used for evaluation of AI models. This can provide users with important information about any limitations or considerations they should be aware of when using the dataset for evaluation of AI models.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIUsageClass'], 'in_subset': ['ai_usability_if_applicable']} })
    restrictions: str = Field(default=..., description="""Any specific restrictions or conditions related to using this dataset in AI/ML workflows, if applicable.
e.g., \"Not for clinical decision-making\"
e.g., not_applicable | none | n/a
Be explicit if there are no applicable restrictions (e.g., \"not_applicable\") rather than leaving this field blank.
This can provide users with important information about any limitations or considerations they should be aware of when using the dataset in AI/ML applications.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIUsageClass'], 'in_subset': ['ai_usability_required']} })
    bias_risks: str = Field(default=..., description="""Any known or potential bias risks associated with using this dataset in AI/ML workflows, if applicable.
e.g., \"Overrepresents samples from facility X\"
e.g., \"Dataset is predominantly from one demographic group, which may introduce bias in AI models trained on this data.\"
e.g., not_applicable | none | n/a
Be explicit if there are no known or potential bias risks (e.g., \"not_applicable\") rather than leaving this field blank.
This can provide users with important information about any ethical considerations or limitations they should be aware of when using the dataset in AI/ML applications.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIUsageClass'], 'in_subset': ['ai_usability_required']} })
    safety_considerations: str = Field(default=..., description="""Any known or potential safety considerations associated with using this dataset in AI/ML workflows, if applicable.
e.g., \"Contains personally identifiable information (PII) that could pose privacy risks if not handled properly.\"
e.g., \"Dataset includes sensitive information that could be misused if not properly safeguarded.\"
e.g., not_applicable | None | N/A
Be explicit if there are no known or potential safety considerations (e.g., \"not_applicable\") rather than leaving this field blank.
This can provide users with important information about any ethical considerations or limitations they should be aware of when using the dataset in AI/ML applications.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIUsageClass'], 'in_subset': ['ai_usability_required']} })
    human_review_required: Optional[YesNoEnum] = Field(default=None, description="""\"Yes\"|\"No\" — Whether human review is recommended when using this dataset in AI/ML workflows, based on factors such as data quality, completeness, relevance, and any known risks or considerations. This can provide users with guidance on whether they should incorporate human review into their AI/ML workflows when working with this dataset, which can help mitigate potential risks and ensure responsible use of the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AIUsageClass'], 'in_subset': ['ai_usability_required']} })


class DataQualityClass(ConfiguredBaseModel):
    """
    Data Quality & Limitations:
    Be specific — vague entries reduce trust and reuse.
    Describes the quality of the dataset and any known limitations, which is important for users to understand the reliability and suitability of the  dataset for their needs.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    completeness: str = Field(default=..., description="""Information about the completeness of the dataset, including any known gaps, missing values, or limitations in the data that may affect its suitability for AI/ML applications.
e.g., \"All detector channels present; 2% of timesteps\"
e.g., \"Missing data for 5% of samples due to sensor downtime\"
e.g., \"Dataset is complete with no known gaps or missing values\"
e.g., not_applicable
This can provide users with important context about the dataset's completeness and reliability,  which can inform their decisions about using the dataset in AI/ML workflows.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataQualityClass'], 'in_subset': ['reusability_required']} })
    known_issues: str = Field(default=..., description="""Any known issues or limitations with the dataset that may affect its suitability for AI/ML applications, if applicable.
e.g., \"Sensor drift observed after 2023-06-01T12:00:00Z\"
e.g., \"Sensor calibration drift affects accuracy of measurements after June 2023\"
e.g., \"Data from Facility X may have quality issues due to known equipment problems during the data collection period\"
e.g., not_applicable
Be explicit if there are no known issues or limitations (e.g., \"not_applicable\") rather than leaving this field blank.
This can provide users with important information about any potential problems or limitations with the dataset,  which can inform their decisions about using the dataset in AI/ML workflows.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataQualityClass'], 'in_subset': ['reusability_required']} })
    validation_methods: str = Field(default=..., description="""Information about any validation methods or processes that have been applied to the dataset to assess its quality and suitability for AI/ML applications, if applicable.
e.g., \"Cross-validated against NIST SRM 640f\"
e.g., \"Dataset validated against ground truth measurements from Facility Y\"
e.g., \"Data quality assessed using method Z with the following results: ...\"
e.g., not_applicable
Be explicit if there are no validation methods or processes (e.g., \"not_applicable\") rather than leaving this field blank.
This can provide users with important information about the steps taken to validate the dataset,  which can inform their confidence in the dataset's quality and reliability for AI/ML applications.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataQualityClass'], 'in_subset': ['reusability_required']} })
    noise_characteristics: Optional[str] = Field(default=None, description="""Information about the noise characteristics of the dataset, if applicable.
e.g., \"Signal-to-noise ratio (SNR) of 20 dB across all channels\"
e.g., \"Noise level increases by 5% after June 2023 due to equipment degradation\"
e.g., \"Dataset has low noise levels with no known issues\"
e.g., not_applicable
Be explicit if there are no known noise issues or characteristics (e.g., \"not_applicable\") rather than leaving this field blank.
This can provide users with important information about the noise characteristics of the dataset,  which can inform their decisions about using the dataset in AI/ML workflows.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataQualityClass'], 'in_subset': ['reusability_if_applicable']} })
    uncertainty_notes: Optional[str] = Field(default=None, description="""Any known uncertainties or limitations in the dataset that may affect its suitability for AI/ML applications, if applicable.
e.g., \"Measurement uncertainty ±0.5% (k=2) per ISO/IEC Guide 98-3\"
e.g., \"Uncertainty increases to ±10% for measurements taken after June 2023 due to equipment degradation\"
e.g., \"Dataset has low uncertainty with no known issues\"
e.g., not_applicable
Be explicit if there are no known uncertainties or limitations (e.g., \"not_applicable\") rather than leaving this field blank.
This can provide users with important information about any uncertainties or limitations in the dataset,  which can inform their decisions about using the dataset in AI/ML workflows.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataQualityClass'], 'in_subset': ['reusability_if_applicable']} })
    missing_data_codes: Optional[MissingDataCodesClass] = Field(default=None, description="""If the dataset contains missing values, list the missing codes and their meanings using the MissingDataCodes block. 
e.g., \"-9999\", and \"Indicates sensor failure; -8888 indicates data not collected; -7777 indicates value below detection limit\"
e.g., \"NULL\", and \"Indicates missing value\"
This can provide users with important information about how missing data is represented in the dataset,  which can inform their decisions about how to handle missing values when using the dataset in AI/ML workflows""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataQualityClass'], 'in_subset': ['reusability_if_applicable']} })


class MissingDataCodesClass(ConfiguredBaseModel):
    """
    A collection of codes used in the dataset to indicate missing or null values, along with their meanings. This helps users understand how missing data is represented in the dataset, which is important for data analysis and preprocessing.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    code: str = Field(default=..., description="""A placeholder slot for any code or script associated with the dataset,  such as data processing scripts, analysis code, or code used to generate the dataset.
e.g., \"-9999\"
e.g., \"NULL\"
This can provide users with access to code that is relevant to understanding and using the dataset effectively.""", json_schema_extra = { "linkml_meta": {'domain_of': ['MissingDataCodesClass'],
         'in_subset': ['reusability_if_applicable']} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'CreatorClass',
                       'LocationClass',
                       'DomainMetadataFieldValueClass',
                       'SpatialCoverageClass',
                       'MissingDataCodesClass'],
         'exact_mappings': ['schema:description',
                            'dcterms:description',
                            'datacite:description']} })


class IntegrityClass(ConfiguredBaseModel):
    """
    Data Integrity & Validation:
    Checksums enable automated validation of data integrity after transfer or storage.
    Describes the integrity of the dataset and any validation methods used to ensure its quality,  which is important for users to assess the reliability of the dataset and understand how it was validated.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml',
         'rules': [{'description': 'If checksum_available is "Yes", then checksum_type '
                                   'and checksum_value must be present.',
                    'postconditions': {'slot_conditions': {'checksum_type': {'name': 'checksum_type',
                                                                             'value_presence': 'PRESENT'},
                                                           'checksum_value': {'name': 'checksum_value',
                                                                              'value_presence': 'PRESENT'}}},
                    'preconditions': {'slot_conditions': {'checksum_available': {'equals_string': 'Yes',
                                                                                 'name': 'checksum_available'}}}}]})

    checksum_available: Optional[YesNoEnum] = Field(default=None, description="""\"Yes\"|\"No\" — Whether a checksum is available for this dataset,  which can be used to verify the integrity of the data after transfer or storage.""", json_schema_extra = { "linkml_meta": {'domain_of': ['IntegrityClass'], 'in_subset': ['reusability_if_applicable']} })
    checksum_type: Optional[str] = Field(default=None, description="""The type of checksum available for this dataset, if applicable.
This can provide users with information about the method used to generate the checksum,  which can inform their decisions about how to use the checksum for data integrity verification.""", json_schema_extra = { "linkml_meta": {'domain_of': ['IntegrityClass'], 'in_subset': ['reusability_if_applicable']} })
    checksum_value: Optional[str] = Field(default=None, description="""The value of the checksum for this dataset, if applicable. This can be used by users to verify the integrity of the data after  transfer or storage by comparing the provided checksum value with a newly  generated checksum from the transferred or stored data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['IntegrityClass'], 'in_subset': ['reusability_if_applicable']} })
    fixity_policy: Optional[str] = Field(default=None, description="""Information about the fixity policy for this dataset,  including how often fixity checks are performed and any specific procedures  or tools used for fixity verification.
e.g., \"Monthly sha256 verification via repository integrity service\"
This can provide users with important information about the measures taken to ensure the integrity of the dataset over time,  which can inform their confidence in the dataset's reliability.""", json_schema_extra = { "linkml_meta": {'domain_of': ['IntegrityClass'], 'in_subset': ['reusability_if_applicable']} })


class SemanticLayerClass(ConfiguredBaseModel):
    """
    Semantic Layer for AI Agents This block provides a structured semantic layer that can be used by AI agents to understand and reason about the dataset and its metadata.  It includes key-value pairs that capture important information about the dataset in a format that is easily interpretable by AI systems.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    schema_url: Optional[str] = Field(default=None, description="""URL pointing to the schema or ontology that defines the semantic layer for this dataset. URL to a formal schema for this dataset, e.g., URL to a JSON Schema | XML Schema | NeXus application definition
e.g., \"https://example.com/schema/dataset_semantic_layer.json\"
e.g., \"https://example.com/ontology/dataset_semantic_layer.owl\"
e.g., not_applicable if there is no formal schema or ontology for this dataset.
Be explicit if there is no formal schema or ontology (e.g., \"not_applicable\") rather than leaving this field blank.
This can provide users with access to the formal definitions and relationships that underpin the dataset's semantic layer,  which can inform their understanding of the dataset's structure and meaning for AI/ML applications.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SemanticLayerClass'],
         'in_subset': ['interoperability_if_applicable']} })
    semantic_context: Optional[list[str]] = Field(default=None, description="""A human-readable description of the semantic context and structure of the dataset, if applicable. Semantic conventions applied. Examples: \"NetCDF CF Conventions 1.10\" | \"NeXus NXmonopd\" | \"Custom schema with the following key classes and relationships: ...\"
This can provide users with important information about the meaning and relationships  of the data elements within the dataset,  which can inform their understanding and use of the dataset for AI/ML applications.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SemanticLayerClass'],
         'in_subset': ['interoperability_if_applicable']} })


class AnyValue(ConfiguredBaseModel):
    """
    A slot that can take any value, used for fields where a controlled vocabulary is not necessary or not yet established. Use when the field can contain a wide range of values that do not fit into a predefined set, or when flexibility is needed for future expansion.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml'})

    value: Optional[str] = Field(default=None, description="""The value of the identifier (e.g., \"10.1234/abcd\"), following the format specified by the 'type' field.
Assign if the datacard has an identifier; required if 'id' is provided.""", json_schema_extra = { "linkml_meta": {'broad_mappings': ['schema:identifier',
                            'dcterms:identifier',
                            'datacite:identifier'],
         'domain_of': ['PublicationIdentifierClass', 'IdentifierClass', 'AnyValue']} })

    @field_validator('value')
    def pattern_value(cls, v):
        pattern=re.compile(r"^.*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid value format: {v}"
            raise ValueError(err_msg)
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
NamedThing.model_rebuild()
GenesisDatacardClass.model_rebuild()
DiscoverabilityClass.model_rebuild()
AccessibilityClass.model_rebuild()
InteroperabilityClass.model_rebuild()
ReusabilityClass.model_rebuild()
GovernedUseClass.model_rebuild()
AIUsabilityClass.model_rebuild()
DataCardClass.model_rebuild()
PublicationIdentifierClass.model_rebuild()
IdentifierClass.model_rebuild()
ChangeLogEntryClass.model_rebuild()
CreatorClass.model_rebuild()
AgentClass.model_rebuild()
PersonClass.model_rebuild()
AffiliationClass.model_rebuild()
OrganizationClass.model_rebuild()
ResearchOrganizationClass.model_rebuild()
FacilityClass.model_rebuild()
LocationClass.model_rebuild()
AIModelClass.model_rebuild()
SoftwareClass.model_rebuild()
DomainMetadataClass.model_rebuild()
SchemaReferenceClass.model_rebuild()
DomainMetadataFieldValueClass.model_rebuild()
DatasetIdentificationClass.model_rebuild()
NamedIdentifierClass.model_rebuild()
DatasetDescriptionClass.model_rebuild()
UseGovernanceClass.model_rebuild()
SensitivityClass.model_rebuild()
WorkflowClass.model_rebuild()
AccessPolicyClass.model_rebuild()
LicenseClass.model_rebuild()
PublisherClass.model_rebuild()
ContactClass.model_rebuild()
SponsorOrganizationClass.model_rebuild()
TagsClass.model_rebuild()
DataStructureClass.model_rebuild()
FeatureClass.model_rebuild()
SpatialCoverageClass.model_rebuild()
GeoLocationBoxClass.model_rebuild()
TemporalCoverageClass.model_rebuild()
DatasetScaleClass.model_rebuild()
DatesClass.model_rebuild()
AccessClass.model_rebuild()
IntendedRepositoryClass.model_rebuild()
DataServiceClass.model_rebuild()
ProvenanceClass.model_rebuild()
DatasetClass.model_rebuild()
SourceDatasetClass.model_rebuild()
SoftwareEnvironmentClass.model_rebuild()
StewardshipClass.model_rebuild()
NonSensitivityGovMetadataClass.model_rebuild()
ExportControlClass.model_rebuild()
PrivacyClass.model_rebuild()
RightsReleaseRecordsClass.model_rebuild()
SpecificReviewClass.model_rebuild()
RelatedResourcesClass.model_rebuild()
ComplianceClass.model_rebuild()
CitationClass.model_rebuild()
PreferredCitationClass.model_rebuild()
AIUsageClass.model_rebuild()
DataQualityClass.model_rebuild()
MissingDataCodesClass.model_rebuild()
IntegrityClass.model_rebuild()
SemanticLayerClass.model_rebuild()
AnyValue.model_rebuild()
