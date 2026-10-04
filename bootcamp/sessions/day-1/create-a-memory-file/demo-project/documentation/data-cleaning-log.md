# Data cleaning log

A record of problems found in the raw data and how they were handled.
Add a new row whenever a cleaning decision is made.

| Date | File | Problem | Decision | Script |
|---|---|---|---|---|
| 2026-03-20 | `household_survey.csv` | Household 1012 is entered twice with identical values | Keep one copy | `clean_household_survey.py` |
| 2026-03-20 | `household_survey.csv` | Income is `-99` for 3 households (refused to answer) | Treat as missing, not as zero | `clean_household_survey.py` |
| 2026-03-20 | `household_survey.csv` | Income is blank for 2 households | Keep as missing. Households stay in the data but are excluded from income averages | `clean_household_survey.py` |
| 2026-03-20 | `household_survey.csv` | Electricity answers written in different ways (yes, Yes, YES, No) | Convert to lowercase, then to 1/0 | `clean_household_survey.py` |
| 2026-03-21 | `district_info.csv` | District names do not match the survey (extra spaces, "riverside", "CENTRAL") | Remove spaces and use Title Case | `clean_district_info.py` |
