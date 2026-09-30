# Databricks notebook source
# MAGIC %md
# MAGIC # Coding Rubric
# MAGIC
# MAGIC Derivation: every variable below operationalizes one guide question from
# MAGIC the interview questionnaire.
# MAGIC
# MAGIC Two output fields per variable, filled in when the rubric is applied to a
# MAGIC given interview:
# MAGIC - `variable_id`_category: exactly one value from that row's category_options (separated by pipes), chosen from what the transcript explicitly says
# MAGIC - `variable_id`_text: a verbatim quote from the transcript's English translation, giving the evidence the category alone can't carry. If more than one passage is needed, they are joined by " [...] "
# MAGIC
# MAGIC CODING RULE: If the interview does not explicitly address a
# MAGIC variable, both fields must be "Not stated". A value is never filled based onwhat seems implied.

# COMMAND ----------

library(tibble)

# COMMAND ----------

coding_rubric <- tribble(
  ~theme_code, ~theme_label, ~variable_id, ~guide_question, ~category_options,
  
  "COLLECT", "End to end collection & validation", "data_entry_automation", "Which steps of end to end data collection and validation are manual, and which are automated?", "Fully manual | Fully automated | Hybrid (some manual, some automated) | Not stated",
  
  "COLLECT", "End to end collection & validation", "validation_responsibility", "Who does what (roles and responsibilities) across the different validation handoffs?", "Single role/unit | Multiple roles within one authority | Multiple external and internal actors | Not stated",
  
  "COLLECT", "End to end collection & validation", "collection_channel", "What channels, templates and tools are used to collect data from beneficiaries/implementers?", "Single IT system or portal | Multiple systems/channels | Manual or offline (email, paper, spreadsheets) | Not stated",
  
  "COLLECT", "End to end collection & validation", "delay_hotspot", "Where do delays most often concentrate, and how are they escalated or supported?", "At beneficiary/implementer submission | At validation/review | At handoff between units | No delays reported | Not stated",
  
  "ENTRY", "Data entry, access & extraction", "access_control_model", "How are permissions and access managed, covering roles, profiling, onboarding/offboarding?", "Role based access control | Open/shared access | Not formally managed | Not stated",
  
  "ENTRY", "Data entry, access & extraction", "data_storage_location", "Where are data entered and maintained: regional system, portals, or elsewhere?", "Regional/local system | National system directly | Mixed (local and national) | Not stated",
  
  "ENTRY", "Data entry, access & extraction", "extraction_source", "From which system(s) do you extract data for reporting?", "Same system as entry | Separate reporting/BI system | Manual export or compilation | Not stated",
  
  "ENTRY", "Data entry, access & extraction", "duplication_reentry", "At which points do duplications or repeat entries happen, and why?", "Duplication or repeat entry reported | No duplication reported | Not stated",
  
  "ANALYTIC", "Analytical use & interoperability", "analytic_use", "Which analyses do you use the data for, such as progress monitoring, performance, or outcomes?", "Progress monitoring only | Progress + performance | Progress + outcomes/evaluation | Not stated",
  
  "ANALYTIC", "Analytical use & interoperability", "responsible_unit", "Which unit is responsible for analysis, including an evaluation unit if one exists?", "Monitoring unit only | Dedicated evaluation unit exists | Split across multiple offices | Not stated",
  
  "ANALYTIC", "Analytical use & interoperability", "external_microdata", "Which external microdata (e.g. firms, labour, procurement) are or would be integrated, and how?", "Already integrated | Attempted, not achieved | Desired, not attempted | None mentioned | Not stated",
  
  "ANALYTIC", "Analytical use & interoperability", "compliance_vs_analytic_value","Which elements of required data collection are analytically useful vs. mainly driven by compliance?", "Mostly analytically useful | Mostly driven by compliance | Mixed view given | Not stated",
  
  "QUALITY", "Data quality & anomaly management", "anomaly_detection_method", "How are inconsistencies or issues in the data detected and handled?", "Automated system checks/alerts | Manual review | Combination of automated and manual | Not stated",
  
  "QUALITY", "Data quality & anomaly management", "quality_kpi_tracking", "Are there dashboards, periodic lists, or internal KPIs (update times, error rates, backlog, etc.)?", "Formal KPIs/dashboard in place | Informal/ad hoc tracking only | No tracking reported | Not stated",
  
  "QUALITY", "Data quality & anomaly management", "recurrent_error_type", "What types of errors/anomalies are most recurrent, and what do they typically depend on?", "Missing/incomplete data | Miscoding/misclassification | Timing/deadline issues | Multiple types reported | Not stated",
  
  "GOVERNANCE", "Governance over time & challenges", "recent_standard_change", "In the last 12 months, were there updates to standards/codifications/controls requiring action?", "Change reported, high impact | Change reported, low impact | No change reported | Not stated",
  
  "GOVERNANCE", "Governance over time & challenges", "data_freeze_practice", "Are there moments when data are frozen/consolidated for official reporting or audit?", "Formal freeze/consolidation process exists | No formal freeze process | Not stated",
  
  "GOVERNANCE", "Governance over time & challenges", "effort_hotspot", "Which process steps require the most effort, or become most demanding/complex?", "Names a specific step | General/diffuse difficulty | No hotspot reported | Not stated",
  
  "GOVERNANCE", "Governance over time & challenges", "external_requirement_burden", "Which external (EU or national) requirements require the most resources to implement?", "EU level requirement named | National level requirement named | Both named | None named | Not stated",
  
  "GOVERNANCE", "Governance over time & challenges", "simplification_opportunity", "Looking ahead, are there opportunities to simplify the process while staying compliant?", "Opportunity identified | No opportunity identified | Not stated"
)


# COMMAND ----------

