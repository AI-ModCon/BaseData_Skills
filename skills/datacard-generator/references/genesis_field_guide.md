# genesis_datacard

A schema for representing datacards in the Genesis project. A datacard is a structured metadata document that describes a dataset: what it is, where it came from, who created it, how it can be accessed, and how it can be used.  Datacards serve both humans (who need to understand a dataset before using it) and machines (automated pipelines that ingest, catalog, and validate datasets). In Genesis, every dataset — regardless of size, sensitivity, or publication state — should have a datacard.  A datacard can be created at the same time as the dataset, or as early in the workflow as possible.

URI: datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml

Name: genesis_datacard



## Classes

| Class | Description |
| --- | --- |
| [AccessClass](AccessClass.md) | Complete the fields you know at the time of datacard creation |
| [AccessibilityClass](AccessibilityClass.md) | Metadata elements that describe the accessibility of this dataset,  such as a... |
| [AccessPolicyClass](AccessPolicyClass.md) | Access policy for the dataset |
| [AffiliationClass](AffiliationClass.md) | An organization with which an entity is affiliated |
| [AgentClass](AgentClass.md) | An individual, organization, AI model, or software tool that created the data... |
| [AIModelClass](AIModelClass.md) | An AI model, including its name, version, and provider |
| [AIUsabilityClass](AIUsabilityClass.md) | Metadata elements that describe the usability of this dataset for AI applicat... |
| [AIUsageClass](AIUsageClass.md) | AI / ML Usage: |
| [AnyValue](AnyValue.md) | A slot that can take any value, used for fields where a controlled vocabulary... |
| [ChangeLogEntryClass](ChangeLogEntryClass.md) | An individual entry in the change log, documenting a specific change to the d... |
| [CitationClass](CitationClass.md) | Populate when release_status = approved | published |
| [ComplianceClass](ComplianceClass.md) | Populate when release_status = under_review | approved | published |
| [ContactClass](ContactClass.md) | Primary point of contact for questions about this dataset |
| [CreatorClass](CreatorClass.md) | An individual, organization, AI model, or software tool that created or updat... |
| [DataCardClass](DataCardClass.md) | Datacard Metadata |
| [DataQualityClass](DataQualityClass.md) | Data Quality & Limitations: |
| [DatasetDescriptionClass](DatasetDescriptionClass.md) | A section of metadata elements that describe the dataset,  including its cont... |
| [DatasetScaleClass](DatasetScaleClass.md) | The scale of the dataset, including the number (and units) of records, bytes ... |
| [DataStructureClass](DataStructureClass.md) | Dataset Characteristics: Describes the content and characteristics of the  da... |
| [DatesClass](DatesClass.md) | Important dates related to the dataset, such as when it was collected, issued... |
| [DiscoverabilityClass](DiscoverabilityClass.md) | Metadata elements that enhance the discoverability of this datacard and datas... |
| [DomainMetadataFieldValueClass](DomainMetadataFieldValueClass.md) | A domain-specific metadata value keyed by the field name |
| [ExportControlClass](ExportControlClass.md) | Export control information for the dataset, which describes any export contro... |
| [GenesisDatacardClass](GenesisDatacardClass.md) | Top-level Genesis datacard document container |
| [GeoLocationBoxClass](GeoLocationBoxClass.md) | WGS84 decimal degrees; use for area coverage |
| [GovernedUseClass](GovernedUseClass.md) | Metadata elements that describe the governed use of this dataset,  such as co... |
| [IdentifierClass](IdentifierClass.md) | A unique identifier for an entity, following a specific format (e |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[SchemaReferenceClass](SchemaReferenceClass.md) | A reference to a schema that describes the structure of the dataset or domain... |
| [IntegrityClass](IntegrityClass.md) | Data Integrity & Validation: |
| [IntendedRepositoryClass](IntendedRepositoryClass.md) | A repositories you intend to deposit or have deposited this dataset in |
| [InteroperabilityClass](InteroperabilityClass.md) | Metadata elements that describe the interoperability of this dataset,  such a... |
| [LicenseClass](LicenseClass.md) | License information for the dataset |
| [LocationClass](LocationClass.md) | A physical location associated with a facility or organization |
| [MissingDataCodesClass](MissingDataCodesClass.md) | A collection of codes used in the dataset to indicate missing or null values,... |
| [NamedIdentifierClass](NamedIdentifierClass.md) | A named identifier for an entity, consisting of a name, and an Identifier cla... |
| [NamedThing](NamedThing.md) | Abstract base class providing identity and human-readable metadata |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DataServiceClass](DataServiceClass.md) | Class/block to populate if a Data Service / API endpoint exists for this data... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DatasetClass](DatasetClass.md) | Source dataset the dataset described in the datacard was derived from |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[SourceDatasetClass](SourceDatasetClass.md) | A source dataset that the dataset described in this datacard was derived from... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DatasetIdentificationClass](DatasetIdentificationClass.md) | A section of metadata elements that identify and provide basic information ab... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DomainMetadataClass](DomainMetadataClass.md) | Domain-specific metadata relevant to the dataset,  which may include specific... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[FeatureClass](FeatureClass.md) | A specific feature or variable included in the dataset, including its name, d... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[OrganizationClass](OrganizationClass.md) | An organization or group of individuals |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[FacilityClass](FacilityClass.md) | A facility where research was conducted or resources were provided for the da... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ResearchOrganizationClass](ResearchOrganizationClass.md) | An organization that conducted research or provided resources for the dataset |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PublisherClass](PublisherClass.md) | The publisher of the dataset, which may be an individual, organization, or ot... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[SponsorOrganizationClass](SponsorOrganizationClass.md) | An organization that funded or sponsored the creation of the dataset |
| [NonSensitivityGovMetadataClass](NonSensitivityGovMetadataClass.md) | Governance-relevant metadata that may affect sharing/use decisions but is not... |
| [PersonClass](PersonClass.md) | A human individual |
| [PreferredCitationClass](PreferredCitationClass.md) | The preferred citation for this dataset, including a human-readable citation ... |
| [PrivacyClass](PrivacyClass.md) | Privacy information for the dataset, which describes any privacy consideratio... |
| [ProvenanceClass](ProvenanceClass.md) | Provenance information about the dataset, including its origin, history, and ... |
| [PublicationIdentifierClass](PublicationIdentifierClass.md) | A section of metadata elements that provide a collection of publication ident... |
| [RelatedResourcesClass](RelatedResourcesClass.md) | Related resources, such as publications, code repositories, or other datasets... |
| [ReusabilityClass](ReusabilityClass.md) | Metadata elements that describe the reusability of this dataset,  such as lic... |
| [RightsReleaseRecordsClass](RightsReleaseRecordsClass.md) | Information about rights, release, and records status for the dataset, which ... |
| [SemanticLayerClass](SemanticLayerClass.md) | Semantic Layer for AI Agents This block provides a structured semantic layer ... |
| [SensitivityClass](SensitivityClass.md) | Sensitivity metadata for Genesis assets |
| [SoftwareClass](SoftwareClass.md) | A software tool, including its name, version, and provider |
| [SoftwareEnvironmentClass](SoftwareEnvironmentClass.md) | Software environment used to generate or process this dataset |
| [SpatialCoverageClass](SpatialCoverageClass.md) | Geographic coverage of the dataset |
| [SpecificReviewClass](SpecificReviewClass.md) | An individual review or quality assessment of the dataset |
| [StewardshipClass](StewardshipClass.md) | Stewardship & Versioning: |
| [TagsClass](TagsClass.md) | Structured tags for catalog filtering and discovery |
| [TemporalCoverageClass](TemporalCoverageClass.md) | Time period the dataset content represents |
| [UseGovernanceClass](UseGovernanceClass.md) | Information to guide appropriate use and prevent misuse of this dataset |
| [WorkflowClass](WorkflowClass.md) | Workflow & Lifecycle: |



## Slots

| Slot | Description |
| --- | --- |
| [access](access.md) | Access Endpoints information |
| [access_level](access_level.md) | The access level of the dataset, following AccessLevelEnum controlled vocabul... |
| [access_policy](access_policy.md) | Access Policy block: Describes who can access this dataset and under what con... |
| [access_restrictions](access_restrictions.md) | Freetext description of access restrictions |
| [accessed_date](accessed_date.md) | The date when an AI model or software tool was accessed for use in  creating ... |
| [accessibility](accessibility.md) | Metadata fields that support the accessibility of the dataset, which is a key... |
| [additional_contacts](additional_contacts.md) | Additional contacts (e |
| [additional_ids](additional_ids.md) | Additional identifiers for this dataset |
| [additional_licenses](additional_licenses.md) | Additional licenses governing this dataset, if multiple licenses apply |
| [affiliation](affiliation.md) | An organization with which a person is affiliated |
| [agent](agent.md) | An entity that is a person, organization, AI model, or software tool that cre... |
| [agreement_required](agreement_required.md) | "Yes" | "No" - Whether an agreement (e |
| [agreement_type](agreement_type.md) | The type of agreement required to access or use the dataset, if applicable, f... |
| [ai_model](ai_model.md) | An AI model |
| [ai_models](ai_models.md) | AI models associated with this dataset, if any |
| [ai_usability](ai_usability.md) | Metadata fields that support the AI usability of the dataset, which is essent... |
| [ai_usage](ai_usage.md) | Describes whether and how this dataset may be used in AI/ML workflows using f... |
| [any_value](any_value.md) | A placeholder slot that can be used when the value can be of any type or is n... |
| [approved_environments](approved_environments.md) | Approved environments for accessing or using the dataset, if applicable |
| [authentication](authentication.md) | Whether authentication is required to access the dataset through this endpoin... |
| [author](author.md) | Author(s) of the dataset, if applicable |
| [authorization_required](authorization_required.md) | List of authorizations required |
| [authors](authors.md) | At least one author required when release_status = approved | published |
| [award_number](award_number.md) | Award number(s) associated with the funding for this dataset |
| [bias_risks](bias_risks.md) | Any known or potential bias risks associated with using this dataset in AI/ML... |
| [change_date](change_date.md) | The date of a specific change to the datacard, in ISO 8601 format (YYYY-MM-DD... |
| [change_log](change_log.md) | Running history of meaningful changes to this datacard |
| [change_log_entry](change_log_entry.md) | An individual entry in the change log, documenting a specific change to the d... |
| [checksum_available](checksum_available.md) | "Yes"|"No" — Whether a checksum is available for this dataset,  which can be ... |
| [checksum_type](checksum_type.md) | The type of checksum available for this dataset, if applicable |
| [checksum_value](checksum_value.md) | The value of the checksum for this dataset, if applicable |
| [citation](citation.md) | Citation information for the dataset, if applicable |
| [classification_category](classification_category.md) | Official classification category, if the asset is classified |
| [classification_level](classification_level.md) | Official classification level, if the asset is classified |
| [classified_control_markings](classified_control_markings.md) | Additional classified dissemination/caveat/handling markings appearing with c... |
| [classified_status](classified_status.md) | "Yes" | "No" - Indicates whether the asset is classified |
| [code](code.md) | A placeholder slot for any code or script associated with the dataset,  such ... |
| [collection_methodology](collection_methodology.md) | How was data acquired? e |
| [comments](comments.md) | Additional comments or notes about the review, if any |
| [compiler](compiler.md) | Compiler used in the software environment for generating or processing this d... |
| [completeness](completeness.md) | Information about the completeness of the dataset, including any known gaps, ... |
| [compliance](compliance.md) | Populate when release_status = under_review | approved | published |
| [compressed_bytes](compressed_bytes.md) | The size of the dataset in bytes when compressed, if applicable |
| [contact](contact.md) | Contact information for questions about access to or use of this dataset |
| [container](container.md) | Containerization technology used in the software environment  for generating ... |
| [contribution_date](contribution_date.md) | ISO 8601 date of an event related to the datacard or dataset |
| [contributors](contributors.md) | Supporting contributors who are not primary authors |
| [created_by](created_by.md) | All individuals, organizations, AI models, or software tools that created or ... |
| [created_date](created_date.md) | The date the datacard was first created, in ISO 8601 format (YYYY-MM-DD) |
| [creation_method](creation_method.md) | The method by which the datacard was created, following a controlled vocabula... |
| [creator](creator.md) | An individual, organization, AI model, or software tool that created the data... |
| [cui_basic_categories](cui_basic_categories.md) | Basic CUI categories applicable to this asset, if it is CUI |
| [cui_limited_dissemination_controls](cui_limited_dissemination_controls.md) | Applicable CUI limited dissemination controls such as NOFORN, DL ONLY, REL TO... |
| [cui_specified_categories](cui_specified_categories.md) | Specified CUI categories applicable to this asset, if it is CUI |
| [cui_status](cui_status.md) | "Yes" | "No" - Indicates whether the asset is Controlled Unclassified Informa... |
| [current_location](current_location.md) | Where the data physically resides right now |
| [current_use](current_use.md) | For in-workflow data: what is this dataset actively being used for right now?... |
| [data_characteristics](data_characteristics.md) | Key structural and content characteristics: scale, dimensionality, temporal c... |
| [data_collection_end](data_collection_end.md) | The date when data collection for this dataset ended, in ISO 8601 format (YYY... |
| [data_collection_start](data_collection_start.md) | The date when data collection for this dataset started, in ISO 8601 format (Y... |
| [data_quality](data_quality.md) | Block containing elements to provide information about the quality of the dat... |
| [data_services](data_services.md) | APIs available for accessing the dataset, if any |
| [data_structure](data_structure.md) | Placeholder for additional dataset characteristics metadata |
| [data_type](data_type.md) | The data type of a feature or variable, following a controlled vocabulary fro... |
| [datacard](datacard.md) | Metadata about the datacard itself (not the dataset),  including its sensitiv... |
| [datacard_version](datacard_version.md) | Increment when the datacard is meaningfully updated |
| [dataset_description](dataset_description.md) | Required, essential metadata fields that provide a high-level description of ... |
| [dataset_publisher](dataset_publisher.md) | The publisher of the dataset, described by a name and ror_id if available |
| [dataset_scale](dataset_scale.md) | A block to describe the scale of the dataset, records (and units), bytes (com... |
| [dataset_summary](dataset_summary.md) | A brief summary of the dataset, including its key characteristics and intende... |
| [dataset_type](dataset_type.md) | OSTI DOE Data Explorer type code |
| [datasets](datasets.md) | Related datasets, if any |
| [date_deposited](date_deposited.md) | The date when the dataset was deposited in the repository, in ISO 8601 format... |
| [dates](dates.md) | Class slot for important dataset dates metadata (e |
| [decontrol_or_declassify_on](decontrol_or_declassify_on.md) | For sensitive datasets, the date when the dataset can be decontrolled or decl... |
| [description](description.md) | Detailed description of the entity |
| [discoverability](discoverability.md) | Metadata fields that support the discoverability of the dataset, which is a k... |
| [documentation_url](documentation_url.md) | URL to documentation for the API or access method |
| [doe_data_management_plan](doe_data_management_plan.md) | "Yes"|"No" — Whether the dataset is in compliance with a DOE Data Management ... |
| [doi](doi.md) | Digital Object Identifier (DOI) for the dataset, if applicable |
| [domain_metadata](domain_metadata.md) | A block for capturing domain-specific metadata that may be relevant for under... |
| [east_bound_longitude](east_bound_longitude.md) | Easternmost longitude in decimal degrees for geospatial datasets |
| [email](email.md) | The email address of a person |
| [embargo_until](embargo_until.md) | Required if state=embargo |
| [encoding](encoding.md) | Character encoding for text-based formats |
| [end_date](end_date.md) | End date of the dataset's temporal coverage in ISO 8601 format (YYYY-MM-DD) |
| [endpoint](endpoint.md) | The URL or connection string for an API endpoint that provides access to the ... |
| [eprint](eprint.md) | The eprint identifier for the dataset, if applicable (e |
| [eprinttype](eprinttype.md) | The type of eprint identifier provided in the url field, if applicable (e |
| [evaluation_use_allowed](evaluation_use_allowed.md) | Whether this dataset can be used for evaluation of AI models, based on factor... |
| [export_control](export_control.md) | Includes fields related to export control considerations for the dataset, if ... |
| [export_control_basis](export_control_basis.md) | The basis for the export control status, if applicable, following a controlle... |
| [export_control_status](export_control_status.md) | The export control status of the dataset, following a controlled vocabulary: ... |
| [facilities](facilities.md) | User facilities, HPC centers, or research infrastructure used to collect, pro... |
| [facility](facility.md) | A user facility, HPC center, or research infrastructure used to collect, proc... |
| [family_name](family_name.md) | The family name(s) of a person |
| [feature](feature.md) | A block for capturing information about the dataset's features, variables, or... |
| [features](features.md) | Primary variables, fields, or features |
| [field_value](field_value.md) | The value for a specific domain metadata field |
| [fields](fields.md) | Field names, their corresponding values, data types, units, and descriptions ... |
| [filename](filename.md) | The filename of the datacard document, follow naming convention: "genesis_dat... |
| [fixity_policy](fixity_policy.md) | Information about the fixity policy for this dataset,  including how often fi... |
| [foreign_national_access_status](foreign_national_access_status.md) | Governance-facing outcome field indicating whether foreign national access is... |
| [formats](formats.md) | File formats included in this dataset |
| [funding_source](funding_source.md) | Funder or sponsor of the research that produced this dataset |
| [geo_location_box](geo_location_box.md) | Geographic bounding box for geospatial datasets, if applicable |
| [given_name](given_name.md) | The given name(s) of a person |
| [governed_use](governed_use.md) | Metadata fields that support the governed use of the dataset, which is essent... |
| [howpublished](howpublished.md) | How the dataset was published or released, if applicable (e |
| [hpc_environment](hpc_environment.md) | HPC environment or platform used in the software environment for generating o... |
| [human_review_required](human_review_required.md) | "Yes"|"No" — Whether human review is recommended when using this dataset in A... |
| [id](id.md) | A unique identifier for the datacard document itself, following the format: "... |
| [identification](identification.md) | Section of Level 1 metadata elements that identify and provide basic informat... |
| [identifier](identifier.md) | A unique identifier for the datacard document itself, following the format: "... |
| [identifiers](identifiers.md) |  |
| [inference_use_allowed](inference_use_allowed.md) | Whether this dataset can be used for inference with AI models, based on facto... |
| [instrumentation](instrumentation.md) | Instruments, sensors, detectors, or equipment used to collect the data, if ap... |
| [integrity](integrity.md) | Contains elements describing checksums enable automated validation of data in... |
| [intended_partner_classes](intended_partner_classes.md) | The intended partner classes/types (list) that are expected to access and use... |
| [intended_repositories](intended_repositories.md) | Repositories you intend to deposit or have deposited this dataset in |
| [intended_use](intended_use.md) | Tasks or workflows this dataset is designed to support |
| [interoperability](interoperability.md) | Metadata fields that support the interoperability of the dataset, which is a ... |
| [ip_restriction_type](ip_restriction_type.md) | The type of intellectual property (IP) restriction that applies to the datase... |
| [irb_approved](irb_approved.md) | "Yes"|"No" — Whether the dataset has been approved by an Institutional Review... |
| [is_intermediate](is_intermediate.md) | "Yes" | "No" - Whether this dataset is an intermediate output, as opposed to ... |
| [is_primary](is_primary.md) | "Yes" | "No" - Whether this is the primary or authoritative location for the ... |
| [issued](issued.md) | The ISO 8601 (YYYY-MM-DD) date the dataset was first publicly released |
| [keywords](keywords.md) | Terms that describe this dataset and aid discovery |
| [known_contractual_rights](known_contractual_rights.md) | Any known contractual rights or obligations associated with this dataset  tha... |
| [known_issues](known_issues.md) | Any known issues or limitations with the dataset that may affect its suitabil... |
| [language](language.md) | The language of the datacard content, following ISO 639-1 codes (e |
| [legacy_label_source](legacy_label_source.md) | Preserves deprecated or local historical control labels such as OUO, SBU, or ... |
| [level](level.md) | The level of stewardship for this dataset, following a controlled vocabulary:... |
| [license](license.md) | Block to capture a license under which the dataset is released |
| [limitations](limitations.md) | Known limitations, gaps, or caveats users should be aware of before using thi... |
| [location](location.md) | Point location for facility-based experimental data, if applicable |
| [maintainer](maintainer.md) | Person or organization responsible for ongoing maintenance of the dataset ove... |
| [missing_data_codes](missing_data_codes.md) | If the dataset contains missing values, list the missing codes and their mean... |
| [modalities](modalities.md) | Data modalities present |
| [modified](modified.md) | The ISO 8601 (YYYY-MM-DD) date the dataset was most recently modified |
| [name](name.md) | Human-readable name or local string key for the entity |
| [need_to_know_basis](need_to_know_basis.md) | If access to this dataset is restricted on a need-to-know basis, provide deta... |
| [noise_characteristics](noise_characteristics.md) | Information about the noise characteristics of the dataset, if applicable |
| [non_sensitivity_governance_metadata](non_sensitivity_governance_metadata.md) | Governance-relevant metadata that may affect sharing/use decisions but is not... |
| [normalized_control_basis](normalized_control_basis.md) | Optional interpreted control basis used for governance where source materials... |
| [north_bound_latitude](north_bound_latitude.md) | Northernmost latitude in decimal degrees for geospatial datasets |
| [note](note.md) | Additional notes related to the preferred citation, if any |
| [notes](notes.md) | Additional environment details, key library versions, or reference to a full ... |
| [object_type](object_type.md) | Primary type of digital object described by this datacard, following ObjectTy... |
| [orcid](orcid.md) | The ORCID identifier for a person, in URL format (e |
| [organization](organization.md) | An organization or group of individuals |
| [os](os.md) | Operating system used in the software environment for generating or processin... |
| [osti_elink2_metadata_compliant](osti_elink2_metadata_compliant.md) | "Yes"|"No" — Whether the dataset is compliant with OSTI's E-Link 2 |
| [out_of_scope_use](out_of_scope_use.md) | Uses this dataset should NOT be applied to |
| [overall_sensitivity](overall_sensitivity.md) | Human-readable top-level sensitivity posture of the asset |
| [parent_collection](parent_collection.md) | Class collection or experimental campaign this dataset belongs to |
| [permitted_use](permitted_use.md) | Uses this dataset is designed and intended to support |
| [person](person.md) | A human individual |
| [phi_status](phi_status.md) | Whether the dataset contains protected health information (PHI), following a ... |
| [pii_status](pii_status.md) | Whether the dataset contains personally identifiable information (PII), follo... |
| [pipeline_stage](pipeline_stage.md) | Freetext position in processing pipeline |
| [policy_text](policy_text.md) | Inline summary if no policy_url exists |
| [policy_url](policy_url.md) | URL to the official access policy or data use agreement governing this datase... |
| [preferred_citation](preferred_citation.md) | Fields that can be used to create full recommended citation in bibtex format ... |
| [primary_id](primary_id.md) | Primary persistent identifier block for this dataset |
| [privacy](privacy.md) | Includes fields related to privacy considerations for the dataset, if applica... |
| [privacy_control_basis](privacy_control_basis.md) | The basis for the privacy status, if applicable |
| [privacy_regime_notes](privacy_regime_notes.md) | Optional notes for privacy regimes or handling nuances not captured by contro... |
| [privacy_status](privacy_status.md) | The privacy status of the dataset, following a controlled vocabulary (use quo... |
| [processing_steps](processing_steps.md) | Key processing, cleaning, calibration, or transformation steps applied to pro... |
| [product_type](product_type.md) | Extended from OSTI Product Types |
| [program](program.md) | The program or initiative under which this dataset was created |
| [prohibited_use](prohibited_use.md) | Uses that are explicitly prohibited for this dataset, either due to ethical c... |
| [project](project.md) | Single human-readable name from the project, Genesis project or sub-project t... |
| [provenance](provenance.md) | Provenance information about the dataset, including its origin, history,  and... |
| [public_release_status](public_release_status.md) | The public release status of the dataset |
| [publications](publications.md) | Publications associated with this dataset, if any |
| [publicly_facing_landing_page_url](publicly_facing_landing_page_url.md) | A publicly facing URL that provides information about the dataset and how to ... |
| [publisher](publisher.md) | Publisher or distributing organization for the dataset, if applicable |
| [purpose](purpose.md) | The purpose for which the dataset was created |
| [range](range.md) | The range of values for a feature, if applicable |
| [rate_limit](rate_limit.md) | Any rate limits or access restrictions for the API endpoint |
| [record_count](record_count.md) | The number of records or rows in the dataset, if applicable |
| [record_status](record_status.md) | The record status of the dataset |
| [record_unit](record_unit.md) | The unit of measurement for the record count (e |
| [related_resources](related_resources.md) | Related Resources: Links to related datasets, publications, software, and AI ... |
| [relationship](relationship.md) | Relationship to other datasets or resources, if any |
| [release_status](release_status.md) | The release status of the dataset, following a controlled vocabulary: Draft |... |
| [report_number](report_number.md) | Report number or other unique identifier for the dataset, if applicable |
| [research_organizations](research_organizations.md) | Organizations that created or collected the data |
| [restrictions](restrictions.md) | Any specific restrictions or conditions related to using this dataset in AI/M... |
| [retention_policy](retention_policy.md) | Information about the dataset's retention policy, including how long the data... |
| [reusability](reusability.md) | Metadata fields that support the reusability of the dataset, which is a key a... |
| [review_contact_email](review_contact_email.md) | Contact email, if appropriate to capture |
| [review_contact_name](review_contact_name.md) | Human point of contact, if appropriate to capture |
| [review_date](review_date.md) | The date when the review was conducted or completed, in ISO 8601 format (YYYY... |
| [review_provenance_companion](review_provenance_companion.md) | Reviews or assessments of the dataset, if any |
| [review_purpose](review_purpose.md) | The purpose or focus of the review, such as export control, IRB, security, qu... |
| [reviewed_by](reviewed_by.md) | Person or role responsible for conducting the review, if applicable |
| [rights_release_records](rights_release_records.md) | Information about rights release records for the dataset, if applicable |
| [role](role.md) | The role, using the CRediT taxonomy, of a type (person, organization, AI mode... |
| [ror_id](ror_id.md) | The ROR identifier for an organization, in URL format (e |
| [safety_considerations](safety_considerations.md) | Any known or potential safety considerations associated with using this datas... |
| [schema_reference](schema_reference.md) | Reference to a schema or controlled vocabulary that defines the domain-specif... |
| [schema_url](schema_url.md) | URL pointing to the schema or ontology that defines the semantic layer for th... |
| [schema_version](schema_version.md) | Version of the data schema used in this dataset |
| [science](science.md) | More specific scientific domain, sub-discipline, or topic |
| [science_domain](science_domain.md) | Scientific domain or discipline this dataset primarily relates to |
| [semantic_context](semantic_context.md) | A human-readable description of the semantic context and structure of the dat... |
| [semantic_layer](semantic_layer.md) | Required for Genesis Readiness Framework Level 3 datasets intended for federa... |
| [sensitivity](sensitivity.md) | Metadata fields that capture the sensitivity of the datacard and the dataset ... |
| [simulation_details](simulation_details.md) | For simulation-derived data: code, simulation setup, version, key parameters,... |
| [software](software.md) | Software associated with this dataset, if any |
| [software_environment](software_environment.md) | Software environment block used to generate or process this dataset,  using S... |
| [source_data](source_data.md) | Source datasets this dataset was derived from |
| [source_marking_scheme](source_marking_scheme.md) | Identifies the authoritative source marking regime, for the source_marking_st... |
| [source_marking_string](source_marking_string.md) | Exact marking/banner/control text as it appears on the source artifact or in ... |
| [source_review_authority](source_review_authority.md) | Office, system, or authority of record for the source sensitivity determinati... |
| [source_review_reference](source_review_reference.md) | Identifier or citation for the authoritative review/release/source document |
| [south_bound_latitude](south_bound_latitude.md) | Southernmost latitude in decimal degrees for geospatial datasets |
| [spatial_coverage](spatial_coverage.md) | Spatial coverage block for geospatial datasets, if applicable |
| [spdx_id](spdx_id.md) | The SPDX license identifier for the dataset, use the SPDX license identifier:... |
| [splits](splits.md) | Dataset splits if pre-divided |
| [sponsor_organizations](sponsor_organizations.md) | Organizations that funded or sponsored this dataset |
| [sponsoring_doe_program_office](sponsoring_doe_program_office.md) | The DOE program office that sponsored or funded the research that produced th... |
| [sponsoring_doe_subprogram](sponsoring_doe_subprogram.md) | The DOE subprogram that sponsored or funded the research that produced this d... |
| [start_date](start_date.md) | Start date of the dataset's temporal coverage in ISO 8601 format (YYYY-MM-DD) |
| [state](state.md) | Current lifecycle position of the data itself, following StateEnum controlled... |
| [stewardship](stewardship.md) | Stewardship & Versioning Block to capture information about dataset maintenan... |
| [succession_note](succession_note.md) | Who to contact if this contact is no longer reachable |
| [summary](summary.md) | A brief description of what was changed in a specific update to the datacard ... |
| [superseded_by](superseded_by.md) | Identifier of the newer version that replaces this dataset |
| [supersedes](supersedes.md) | Identifier of the prior version this dataset replaces |
| [supports_accessibility](supports_accessibility.md) | "Yes" | "No" - Indicates whether the dataset described in the datacard is int... |
| [supports_ai_usability](supports_ai_usability.md) | "Yes" | "No" - Indicates whether the dataset described in the datacard is int... |
| [supports_discoverability](supports_discoverability.md) | "Yes" | "No" - "Yes" is required for all datacards to indicate whether the da... |
| [supports_governed_use](supports_governed_use.md) | "Yes" | "No" - Indicates whether the dataset described in the datacard is int... |
| [supports_interoperability](supports_interoperability.md) | "Yes" | "No" - Indicates whether the dataset described in the datacard is int... |
| [supports_reusability](supports_reusability.md) | "Yes" | "No" - Indicates whether the dataset described in the datacard is int... |
| [tags](tags.md) | Structured tags block for catalog filtering and discovery, including project,... |
| [task_category](task_category.md) | Primary task category or categories for this dataset |
| [task_subcategory](task_subcategory.md) | More specifictask subcategory or subcategories |
| [template_version](template_version.md) | The version of the datacard template used to create this datacard |
| [temporal_coverage](temporal_coverage.md) | Temporal coverage for time-based datasets, if applicable |
| [title](title.md) | Title of the dataset, if applicable |
| [training_use_allowed](training_use_allowed.md) | Whether this dataset can be used for training AI models, based on factors suc... |
| [type](type.md) | The type of the Identifer (e |
| [ucni_status](ucni_status.md) | "Yes" | "No" - Indicates whether the asset contains UCNI |
| [uk_mda_status](uk_mda_status.md) | "Yes" | "No" - Indicates whether the asset is subject to UK MDA-specific hand... |
| [uncertainty_notes](uncertainty_notes.md) | Any known uncertainties or limitations in the dataset that may affect its sui... |
| [uncompressed_bytes](uncompressed_bytes.md) | The size of the dataset in bytes when uncompressed, if applicable |
| [unit](unit.md) | The unit of measurement for a feature, if applicable |
| [update_frequency](update_frequency.md) | How often the dataset is updated or expected to be updated, if applicable |
| [updated_date](updated_date.md) | The date the datacard was last updated, in ISO 8601 format (YYYY-MM-DD) |
| [url](url.md) | URL to the official access policy or data use agreement governing this datase... |
| [use_governance](use_governance.md) | Information block to guide appropriate use and prevent misuse of this dataset |
| [valid_until](valid_until.md) | Date after which this contact may no longer be valid |
| [validation_methods](validation_methods.md) | Information about any validation methods or processes that have been applied ... |
| [value](value.md) | The value of the identifier (e |
| [version](version.md) | Version of software, tool, or library |
| [versioning_strategy](versioning_strategy.md) | Information about the dataset's versioning strategy, including how new versio... |
| [was_generated_by](was_generated_by.md) | High-level description of the generating process |
| [west_bound_longitude](west_bound_longitude.md) | Westernmost longitude in decimal degrees for geospatial datasets |
| [workflow](workflow.md) | Workflow & Lifecycle Block: |
| [year](year.md) | Year of publication or release of the dataset, if applicable |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [AccessLevelEnum](AccessLevelEnum.md) | The access level of the document being described |
| [AgreementTypeEnum](AgreementTypeEnum.md) | Controlled vocabulary for the type of agreement required for access to the da... |
| [AuthenticationTypeEnum](AuthenticationTypeEnum.md) | Controlled vocabulary for types of authentication required to access the data... |
| [AuthorizationRequiredEnum](AuthorizationRequiredEnum.md) | Controlled vocabulary for whether authorization is required to access the dat... |
| [ClassificationCategoryEnum](ClassificationCategoryEnum.md) | Controlled vocabulary for the official classification category/categories, if... |
| [ClassificationLevelEnum](ClassificationLevelEnum.md) | Controlled vocabulary for the official classification level, if the asset is ... |
| [DatacardCreationMethodEnum](DatacardCreationMethodEnum.md) | How this datacard was created or most recently updated |
| [DatasetTypeEnum](DatasetTypeEnum.md) | OSTI DOE Data Explorer type code |
| [ExportControlBasisEnum](ExportControlBasisEnum.md) | Controlled vocabulary for the basis of the export control classification of t... |
| [ExtendedRelationshipEnum](ExtendedRelationshipEnum.md) | Extended relationship types for more specific relationships between a source ... |
| [ForeignNationalAccessStatusEnum](ForeignNationalAccessStatusEnum.md) | Controlled vocabulary for Governance-facing outcome field indicating whether ... |
| [FundingSourceEnum](FundingSourceEnum.md) | Controlled vocabulary for the funding source of the dataset |
| [IdentifierTypeEnum](IdentifierTypeEnum.md) | The type of identifier, following a controlled vocabulary (e |
| [IntendedPartnerClassEnum](IntendedPartnerClassEnum.md) | Controlled vocabulary for the intended partner class for sharing datasets |
| [IPRestrictionTypeEnum](IPRestrictionTypeEnum.md) | Controlled vocabulary for the type of IP-based access restriction applied to ... |
| [NeedToKnowBasisEnum](NeedToKnowBasisEnum.md) | Controlled vocabulary for the basis of need-to-know restrictions on access to... |
| [NormalizedControlBasisEnum](NormalizedControlBasisEnum.md) | Controlled vocabulary for the interpreted control basis used for governance w... |
| [ObjectTypeEnum](ObjectTypeEnum.md) | Primary type of digital object described by this card |
| [OverallSensitivityEnum](OverallSensitivityEnum.md) | Controlled vocabulary for the human-readable top-level sensitivity posture of... |
| [PrivacyControlBasisEnum](PrivacyControlBasisEnum.md) | Controlled vocabulary for the basis of the privacy control classification of ... |
| [ProductTypeEnum](ProductTypeEnum.md) | The type of product described by this datacard |
| [PublicReleaseStatusEnum](PublicReleaseStatusEnum.md) | Controlled vocabulary for the public release status of the dataset,  indicati... |
| [RecordStatusEnum](RecordStatusEnum.md) | Controlled vocabulary for the records status of the dataset,  indicating whet... |
| [RelationshipTypeEnum](RelationshipTypeEnum.md) | Controlled vocabulary for the relationship between a source dataset and the d... |
| [ReleaseStatusEnum](ReleaseStatusEnum.md) | Current publication and governance state of this dataset |
| [RoleEnum](RoleEnum.md) | The role of a type (person, organization, AI model, or software tool) in rela... |
| [SourceMarkingSchemeEnum](SourceMarkingSchemeEnum.md) | Controlled vocabulary that identifies the authoritative source marking regime... |
| [StateEnum](StateEnum.md) | Current lifecycle position: |
| [StewardshipLevelEnum](StewardshipLevelEnum.md) | Controlled vocabulary for the stewardship level/management of the dataset |
| [UKMDAStatusEnum](UKMDAStatusEnum.md) | Controlled vocabulary for the indication of whether the asset is subject to U... |
| [UpdateFrequencyEnum](UpdateFrequencyEnum.md) | Controlled vocabulary for how frequently the dataset is updated |
| [YesNoConditionalEnum](YesNoConditionalEnum.md) | Controlled vocabulary for fields with "Yes", "No", or "Conditional" values |
| [YesNoEnum](YesNoEnum.md) | Controlled vocabulary for fields with "Yes" or "No" values |
| [YesNoPendingUnknownEnum](YesNoPendingUnknownEnum.md) | Controlled vocabulary for fields with "Yes", "No", "Pending_Review", or "Unkn... |
| [YesNoUnknownEnum](YesNoUnknownEnum.md) | Controlled vocabulary for fields with "Yes", "No", or "Unknown" values |
| [YesNoUnknownNotApplicableEnum](YesNoUnknownNotApplicableEnum.md) | Controlled vocabulary for fields with "Yes", "No", "Unknown", or "not_applica... |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
| [AccessibilityIfApplicable](AccessibilityIfApplicable.md) | These fields are optional, but recommended, for datacards of datasets that ar... |
| [AccessibilityRequired](AccessibilityRequired.md) | These fields are required for datacards of datasets that are intended to be s... |
| [AiUsabilityIfApplicable](AiUsabilityIfApplicable.md) | These fields are optional, but recommended, for datacards of datasets that ar... |
| [AiUsabilityRequired](AiUsabilityRequired.md) | These fields are required for datacards of datasets that are intended to be u... |
| [DiscoverabilityIfApplicable](DiscoverabilityIfApplicable.md) | Optional, but recommended, for datacards of datasets that are intended to be ... |
| [DiscoverabilityRequired](DiscoverabilityRequired.md) | These essential fields are designed to facilitate discovery using the datacar... |
| [GovernedUseIfApplicable](GovernedUseIfApplicable.md) | These fields are optional, but recommended, for datacards of datasets that ar... |
| [GovernedUseRequired](GovernedUseRequired.md) | These fields are required for datacards of datasets that are intended to be s... |
| [InteroperabilityIfApplicable](InteroperabilityIfApplicable.md) | These fields are optional, but recommended, for datacards of datasets that ar... |
| [InteroperabilityRequired](InteroperabilityRequired.md) | These fields are required for datacards of datasets that are intended to be i... |
| [ReferenceOnlyDoNotInclude](ReferenceOnlyDoNotInclude.md) | These fields are provided for reference only and should not be included in a ... |
| [Required](Required.md) | Required for all datacards, regardless of intended use or sharing level and u... |
| [ReusabilityIfApplicable](ReusabilityIfApplicable.md) | These fields are optional, but recommended, for datacards of datasets that ar... |
| [ReusabilityRequired](ReusabilityRequired.md) | These fields are required for datacards of datasets that are intended to be r... |

---

> **Note (vendored copy):** This is upstream's auto-generated schema reference index (`datacard_schema/docs/index.md`). For comprehensive field-by-field guidance, the LinkML schema at upstream's `datacard_schema/src/genesis_datacard/schema/genesis_datacard.yaml` is authoritative. Individual per-field documentation pages (e.g., `AccessClass.md`, `title.md`, etc.) are also available in the upstream `docs/` directory but are not vendored here — refer to the upstream clone at `/Users/jlbez/Documents/repositories/data-cards/datacard_schema/docs/`.
