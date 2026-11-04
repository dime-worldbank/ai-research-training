* import_ai_bootcamp_pre_survey.do
*
* 	Imports and aggregates "AI Bootcamp Baseline Survey" (ID: ai_bootcamp_pre_survey) data.
*
*	Inputs:  "C:/Users/wb357411/OneDrive - WBG/DIME Analytics/Trainings/AI-Trainings/AI-Bootcamp/Surveys/AI Bootcamp Baseline Survey_WIDE.csv"
*	Outputs: "C:/Users/wb357411/OneDrive - WBG/DIME Analytics/Trainings/AI-Trainings/AI-Bootcamp/Surveys/AI Bootcamp Baseline Survey.dta"
*
*	Output by SurveyCTO October 15, 2026 10:00 AM.

* initialize Stata
clear all
set more off
set mem 100m

* initialize workflow-specific parameters
*	Set overwrite_old_data to 1 if you use the review and correction
*	workflow and allow un-approving of submissions. If you do this,
*	incoming data will overwrite old data, so you won't want to make
*	changes to data in your local .dta file (such changes can be
*	overwritten with each new import).
local overwrite_old_data 0

* initialize form-specific parameters
local csvfile "C:/Users/wb357411/OneDrive - WBG/DIME Analytics/Trainings/AI-Trainings/AI-Bootcamp/Surveys/AI Bootcamp Baseline Survey_WIDE.csv"
local dtafile "C:/Users/wb357411/OneDrive - WBG/DIME Analytics/Trainings/AI-Trainings/AI-Bootcamp/Surveys/AI Bootcamp Baseline Survey.dta"
local corrfile "C:/Users/wb357411/OneDrive - WBG/DIME Analytics/Trainings/AI-Trainings/AI-Bootcamp/Surveys/AI Bootcamp Baseline Survey_corrections.csv"
local note_fields1 ""
local text_fields1 "q1_2 q1_2_other q1_3 q1_3_other q1_5 q1_5_other q1_7_other q2_3 q2_3_other q2_3_2 q2_3_3_other q2_5 q2_5_other upi q4_3 q4_6 instanceid"
local date_fields1 ""
local datetime_fields1 "submissiondate"

disp
disp "Starting import of: `csvfile'"
disp

* import data from primary .csv file
insheet using "`csvfile'", names clear

* drop extra table-list columns
cap drop reserved_name_for_field_*
cap drop generated_table_list_lab*

* continue only if there's at least one row of data to import
if _N>0 {
	* drop note fields (since they don't contain any real data)
	forvalues i = 1/100 {
		if "`note_fields`i''" ~= "" {
			drop `note_fields`i''
		}
	}
	
	* format date and date/time fields
	forvalues i = 1/100 {
		if "`datetime_fields`i''" ~= "" {
			foreach dtvarlist in `datetime_fields`i'' {
				cap unab dtvarlist : `dtvarlist'
				if _rc==0 {
					foreach dtvar in `dtvarlist' {
						tempvar tempdtvar
						rename `dtvar' `tempdtvar'
						gen double `dtvar'=.
						cap replace `dtvar'=clock(`tempdtvar',"MDYhms",2025)
						* automatically try without seconds, just in case
						cap replace `dtvar'=clock(`tempdtvar',"MDYhm",2025) if `dtvar'==. & `tempdtvar'~=""
						format %tc `dtvar'
						drop `tempdtvar'
					}
				}
			}
		}
		if "`date_fields`i''" ~= "" {
			foreach dtvarlist in `date_fields`i'' {
				cap unab dtvarlist : `dtvarlist'
				if _rc==0 {
					foreach dtvar in `dtvarlist' {
						tempvar tempdtvar
						rename `dtvar' `tempdtvar'
						gen double `dtvar'=.
						cap replace `dtvar'=date(`tempdtvar',"MDY",2025)
						format %td `dtvar'
						drop `tempdtvar'
					}
				}
			}
		}
	}

	* ensure that text fields are always imported as strings (with "" for missing values)
	* (note that we treat "calculate" fields as text; you can destring later if you wish)
	tempvar ismissingvar
	quietly: gen `ismissingvar'=.
	forvalues i = 1/100 {
		if "`text_fields`i''" ~= "" {
			foreach svarlist in `text_fields`i'' {
				cap unab svarlist : `svarlist'
				if _rc==0 {
					foreach stringvar in `svarlist' {
						quietly: replace `ismissingvar'=.
						quietly: cap replace `ismissingvar'=1 if `stringvar'==.
						cap tostring `stringvar', format(%100.0g) replace
						cap replace `stringvar'="" if `ismissingvar'==1
					}
				}
			}
		}
	}
	quietly: drop `ismissingvar'


	* consolidate unique ID into "key" variable
	replace key=instanceid if key==""
	drop instanceid


	* label variables
	label variable key "Unique submission ID"
	cap label variable submissiondate "Date/time submitted"
	cap label variable formdef_version "Form version used on device"
	cap label variable review_status "Review status"
	cap label variable review_comments "Comments made during review"
	cap label variable review_corrections "Corrections made during review"


	label variable q1_1 "1.1 Do you currently use generative AI for your job?"
	note q1_1: "1.1 Do you currently use generative AI for your job?"
	label define q1_1 1 "Yes" 2 "No, I use generative AI for personal use but not for work" 3 "No, I do not use generative AI for any purpose"
	label values q1_1 q1_1

	label variable q1_2 "1.2 You indicated that you do not use Generative AI for your job. Below is a lis"
	note q1_2: "1.2 You indicated that you do not use Generative AI for your job. Below is a list of common reasons. Please select all that apply."

	label variable q1_2_other "1.2 Specify other"
	note q1_2_other: "1.2 Specify other"

	label variable q1_3 "1.3 Which of the following AI tools have you ever used for work? (Select all tha"
	note q1_3: "1.3 Which of the following AI tools have you ever used for work? (Select all that apply)"

	label variable q1_3_other "1.3 Please specify the other AI tool:"
	note q1_3_other: "1.3 Please specify the other AI tool:"

	label variable q1_4 "1.4 During the LAST FOUR WEEKS, on average, how much time did you spend actively"
	note q1_4: "1.4 During the LAST FOUR WEEKS, on average, how much time did you spend actively using Generative AI for your job?"
	label define q1_4 1 "Less than 15 minutes per day" 2 "Between 15 minutes and 1 hour per day" 3 "Between 1 and 4 hours per day" 4 "More than 4 hours per day"
	label values q1_4 q1_4

	label variable q1_5 "1.5 During the LAST FOUR WEEKS, what tasks did you use Generative AI for (in you"
	note q1_5: "1.5 During the LAST FOUR WEEKS, what tasks did you use Generative AI for (in your job)? (Select all that apply)"

	label variable q1_5_other "1.5 Please specify the other task:"
	note q1_5_other: "1.5 Please specify the other task:"

	label variable q1_5_usefulness_labels "Task"
	note q1_5_usefulness_labels: "Task"
	label define q1_5_usefulness_labels 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_usefulness_labels q1_5_usefulness_labels

	label variable q1_5_use_1 "Administrative tasks (transactions, filing, paperwork)"
	note q1_5_use_1: "Administrative tasks (transactions, filing, paperwork)"
	label define q1_5_use_1 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_1 q1_5_use_1

	label variable q1_5_use_2 "Email (drafting, inbox management)"
	note q1_5_use_2: "Email (drafting, inbox management)"
	label define q1_5_use_2 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_2 q1_5_use_2

	label variable q1_5_use_3 "Writing and editing documents (reports, papers, briefs)"
	note q1_5_use_3: "Writing and editing documents (reports, papers, briefs)"
	label define q1_5_use_3 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_3 q1_5_use_3

	label variable q1_5_use_4 "Background research (literature review, fact finding, brainstorming, summarizing"
	note q1_5_use_4: "Background research (literature review, fact finding, brainstorming, summarizing documents/text written by others)"
	label define q1_5_use_4 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_4 q1_5_use_4

	label variable q1_5_use_5 "Research design (e.g. developing concept notes or grant proposals)"
	note q1_5_use_5: "Research design (e.g. developing concept notes or grant proposals)"
	label define q1_5_use_5 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_5 q1_5_use_5

	label variable q1_5_use_6 "Surveys (questionnaire development, programming, data quality checks)"
	note q1_5_use_6: "Surveys (questionnaire development, programming, data quality checks)"
	label define q1_5_use_6 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_6 q1_5_use_6

	label variable q1_5_use_7 "Data analysis and visualization (writing, revising, debugging software code)"
	note q1_5_use_7: "Data analysis and visualization (writing, revising, debugging software code)"
	label define q1_5_use_7 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_7 q1_5_use_7

	label variable q1_5_use_8 "Creating a dashboard or web app"
	note q1_5_use_8: "Creating a dashboard or web app"
	label define q1_5_use_8 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_8 q1_5_use_8

	label variable q1_5_use_9 "Creating and/or verifying a reproducibility package"
	note q1_5_use_9: "Creating and/or verifying a reproducibility package"
	label define q1_5_use_9 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_9 q1_5_use_9

	label variable q1_5_use_10 "Drafting and editing presentations"
	note q1_5_use_10: "Drafting and editing presentations"
	label define q1_5_use_10 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_10 q1_5_use_10

	label variable q1_5_use_11 "Preparing communications materials (social media posts, blogs, podcasts, infogra"
	note q1_5_use_11: "Preparing communications materials (social media posts, blogs, podcasts, infographics, etc)"
	label define q1_5_use_11 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_11 q1_5_use_11

	label variable q1_5_use_12 "Recruitment (drafting TORs, advertising, screening applicants, interviewing)"
	note q1_5_use_12: "Recruitment (drafting TORs, advertising, screening applicants, interviewing)"
	label define q1_5_use_12 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_12 q1_5_use_12

	label variable q1_5_use_97 "Other task: \${q1_5_other}"
	note q1_5_use_97: "Other task: \${q1_5_other}"
	label define q1_5_use_97 1 "Not useful at all" 2 "Slightly useful" 3 "Useful" 4 "Extremely useful"
	label values q1_5_use_97 q1_5_use_97

	label variable q1_6 "1.6 Have any of your AI-assisted work products ever been included in reports, Wo"
	note q1_6: "1.6 Have any of your AI-assisted work products ever been included in reports, Working Papers, presentations, blogs, or other outputs?"
	label define q1_6 1 "Yes" 2 "No"
	label values q1_6 q1_6

	label variable q1_7 "1.7 Was the AI use disclosed in the publication/report?"
	note q1_7: "1.7 Was the AI use disclosed in the publication/report?"
	label define q1_7 1 "I included a clear disclosure statement with details on the way AI contributed t" 2 "I mentioned AI use but did not provide details" 3 "No, I wanted to disclose but was not sure how" 4 "No, I preferred not to disclose AI use" 97 "Other (specify)"
	label values q1_7 q1_7

	label variable q1_7_other "1.7 Please specify:"
	note q1_7_other: "1.7 Please specify:"

	label variable q2_1 "2.1 Have you created an AI memory file for any of your projects?"
	note q2_1: "2.1 Have you created an AI memory file for any of your projects?"
	label define q2_1 1 "Yes" 2 "No – I know what memory files are but I've never created one" 3 "No – I do not know what memory files are"
	label values q2_1 q2_1

	label variable q2_2 "2.2 Have you ever installed and used a reusable AI skill developed by someone el"
	note q2_2: "2.2 Have you ever installed and used a reusable AI skill developed by someone else?"
	label define q2_2 1 "Yes" 2 "No – I know what skills are, but I've never used one" 3 "No – I do not know what skills are"
	label values q2_2 q2_2

	label variable q2_3 "2.3 Thinking back over the past 4 weeks, has the use of AI to support your analy"
	note q2_3: "2.3 Thinking back over the past 4 weeks, has the use of AI to support your analytical work meant that you … (Select all that apply)"

	label variable q2_3_other "2.3 Please specify:"
	note q2_3_other: "2.3 Please specify:"

	label variable q2_3_1 "2.3.1 How much more are you able to do / produce for this task by using AI?"
	note q2_3_1: "2.3.1 How much more are you able to do / produce for this task by using AI?"
	label define q2_3_1 1 "About 25% more" 2 "About 50% more" 3 "About 75% more" 4 "About twice as much" 5 "About three times as much" 6 "About four times as much" 7 "5 times as much or more"
	label values q2_3_1 q2_3_1

	label variable q2_3_2 "2.3.2 How has AI improved the quality of your work?"
	note q2_3_2: "2.3.2 How has AI improved the quality of your work?"

	label variable q2_3_3_other "2.3.3 Please specify:"
	note q2_3_3_other: "2.3.3 Please specify:"

	label variable q2_3_4 "2.3.4 If you had not used AI, would this more in-depth / advanced work have:"
	note q2_3_4: "2.3.4 If you had not used AI, would this more in-depth / advanced work have:"
	label define q2_3_4 1 "Been done later (after spending time researching / learning how to do it)" 2 "Been done by another staff member/ET" 3 "Been done by another ST" 4 "Been done by a third party (e.g. a contracted firm)" 5 "Not been done at all"
	label values q2_3_4 q2_3_4

	label variable q2_4 "2.4 Thinking back over the past 4 weeks, has your use of AI tools changed the tr"
	note q2_4: "2.4 Thinking back over the past 4 weeks, has your use of AI tools changed the transparency and/or reproducibility of your analytical products?"
	label define q2_4 1 "More of my outputs are fully reproducible (someone else could easily understand " 2 "No change" 3 "Fewer of my outputs are fully reproducible (they would be difficult for someone " 4 "I am not sure" 5 "I do not do analytical work"
	label values q2_4 q2_4

	label variable q2_5 "2.5 How do you verify the quality of AI-generated work? (Check all that apply)"
	note q2_5: "2.5 How do you verify the quality of AI-generated work? (Check all that apply)"

	label variable q2_5_other "2.5 Please specify:"
	note q2_5_other: "2.5 Please specify:"

	label variable q3_1 "3.1 Do you use GitHub to version control code for any of your current analytical"
	note q3_1: "3.1 Do you use GitHub to version control code for any of your current analytical projects?"
	label define q3_1 1 "Yes, I have active GitHub repositories for my work" 2 "Not currently, though I've used GitHub in the past" 3 "No, I am familiar with GitHub but do not use it" 4 "No, I am not familiar with GitHub" 5 "NA (I do not do analytical work)"
	label values q3_1 q3_1

	label variable q3_2 "3.2 Do you currently use GitHub CoPilot as a coding agent for work?"
	note q3_2: "3.2 Do you currently use GitHub CoPilot as a coding agent for work?"
	label define q3_2 1 "Yes, I have a GitHub CoPilot license from the WBG and am an active user" 2 "Yes, I have a GitHub CoPilot license from the WBG and have started to play aroun" 3 "No, I have used GitHub CoPilot through my personal account, but not through the " 4 "No, I have heard of GitHub CoPilot but I have never used it." 5 "What is GitHub CoPilot?"
	label values q3_2 q3_2

	label variable q3_3 "3.3 You're working with baseline survey data collected for your project. The dat"
	note q3_3: "3.3 You're working with baseline survey data collected for your project. The data is owned by the World Bank. You want AI to help to clean the raw data and generate descriptive statistics. Which of the following workflows follows WBG guidance on safe and effective use of AI? (Select one)"
	label define q3_3 1 "Use a personal ChatGPT or Claude account, but only share de-identified data" 2 "Use mAI or Microsoft 365 Copilot for de-identification, cleaning, and analysis o" 3 "Generate synthetic data that has the same structure. Provide this as context to " 4 "Don't use AI at all. Confidential data can never be used with AI tools, and the " 5 "I'm not sure"
	label values q3_3 q3_3

	label variable upi "4.1 Enter your 6-digit UPI"
	note upi: "4.1 Enter your 6-digit UPI"

	label variable q4_2 "4.2 How long have you worked at the World Bank?"
	note q4_2: "4.2 How long have you worked at the World Bank?"
	label define q4_2 1 "Less than 1 year" 2 "1-4 years" 3 "5-9 years" 4 "10-19 years" 5 "20 + years" 6 "Prefer not to answer"
	label values q4_2 q4_2

	label variable q4_3 "4.3 What are you looking to get from this Bootcamp?"
	note q4_3: "4.3 What are you looking to get from this Bootcamp?"

	label variable q4_4 "4.4 Have you taken a course/workshop on AI for Research before?"
	note q4_4: "4.4 Have you taken a course/workshop on AI for Research before?"
	label define q4_4 1 "Yes" 2 "No"
	label values q4_4 q4_4

	label variable q4_5 "4.5 How would you rate your current knowledge on AI for Research?"
	note q4_5: "4.5 How would you rate your current knowledge on AI for Research?"
	label define q4_5 1 "Very poor knowledge" 2 "Poor knowledge" 3 "Average knowledge" 4 "Good knowledge" 5 "Excellent knowledge"
	label values q4_5 q4_5

	label variable q4_6 "4.6 What is the one thing you most want to learn during the Bootcamp?"
	note q4_6: "4.6 What is the one thing you most want to learn during the Bootcamp?"






	* append old, previously-imported data (if any)
	cap confirm file "`dtafile'"
	if _rc == 0 {
		* mark all new data before merging with old data
		gen new_data_row=1
		
		* pull in old data
		append using "`dtafile'"
		
		* drop duplicates in favor of old, previously-imported data if overwrite_old_data is 0
		* (alternatively drop in favor of new data if overwrite_old_data is 1)
		sort key
		by key: gen num_for_key = _N
		drop if num_for_key > 1 & ((`overwrite_old_data' == 0 & new_data_row == 1) | (`overwrite_old_data' == 1 & new_data_row ~= 1))
		drop num_for_key

		* drop new-data flag
		drop new_data_row
	}
	
	* save data to Stata format
	save "`dtafile'", replace

	* show codebook and notes
	codebook
	notes list
}

disp
disp "Finished import of: `csvfile'"
disp

* OPTIONAL: LOCALLY-APPLIED STATA CORRECTIONS
*
* Rather than using SurveyCTO's review and correction workflow, the code below can apply a list of corrections
* listed in a local .csv file. Feel free to use, ignore, or delete this code.
*
*   Corrections file path and filename:  C:/Users/wb357411/OneDrive - WBG/DIME Analytics/Trainings/AI-Trainings/AI-Bootcamp/Surveys/AI Bootcamp Baseline Survey_corrections.csv
*
*   Corrections file columns (in order): key, fieldname, value, notes

capture confirm file "`corrfile'"
if _rc==0 {
	disp
	disp "Starting application of corrections in: `corrfile'"
	disp

	* save primary data in memory
	preserve

	* load corrections
	insheet using "`corrfile'", names clear
	
	if _N>0 {
		* number all rows (with +1 offset so that it matches row numbers in Excel)
		gen rownum=_n+1
		
		* drop notes field (for information only)
		drop notes
		
		* make sure that all values are in string format to start
		gen origvalue=value
		tostring value, format(%100.0g) replace
		cap replace value="" if origvalue==.
		drop origvalue
		replace value=trim(value)
		
		* correct field names to match Stata field names (lowercase, drop -'s and .'s)
		replace fieldname=lower(subinstr(subinstr(fieldname,"-","",.),".","",.))
		
		* format date and date/time fields (taking account of possible wildcards for repeat groups)
		forvalues i = 1/100 {
			if "`datetime_fields`i''" ~= "" {
				foreach dtvar in `datetime_fields`i'' {
					* skip fields that aren't yet in the data
					cap unab dtvarignore : `dtvar'
					if _rc==0 {
						gen origvalue=value
						replace value=string(clock(value,"MDYhms",2025),"%25.0g") if strmatch(fieldname,"`dtvar'")
						* allow for cases where seconds haven't been specified
						replace value=string(clock(origvalue,"MDYhm",2025),"%25.0g") if strmatch(fieldname,"`dtvar'") & value=="." & origvalue~="."
						drop origvalue
					}
				}
			}
			if "`date_fields`i''" ~= "" {
				foreach dtvar in `date_fields`i'' {
					* skip fields that aren't yet in the data
					cap unab dtvarignore : `dtvar'
					if _rc==0 {
						replace value=string(clock(value,"MDY",2025),"%25.0g") if strmatch(fieldname,"`dtvar'")
					}
				}
			}
		}

		* write out a temp file with the commands necessary to apply each correction
		tempfile tempdo
		file open dofile using "`tempdo'", write replace
		local N = _N
		forvalues i = 1/`N' {
			local fieldnameval=fieldname[`i']
			local valueval=value[`i']
			local keyval=key[`i']
			local rownumval=rownum[`i']
			file write dofile `"cap replace `fieldnameval'="`valueval'" if key=="`keyval'""' _n
			file write dofile `"if _rc ~= 0 {"' _n
			if "`valueval'" == "" {
				file write dofile _tab `"cap replace `fieldnameval'=. if key=="`keyval'""' _n
			}
			else {
				file write dofile _tab `"cap replace `fieldnameval'=`valueval' if key=="`keyval'""' _n
			}
			file write dofile _tab `"if _rc ~= 0 {"' _n
			file write dofile _tab _tab `"disp"' _n
			file write dofile _tab _tab `"disp "CAN'T APPLY CORRECTION IN ROW #`rownumval'""' _n
			file write dofile _tab _tab `"disp"' _n
			file write dofile _tab `"}"' _n
			file write dofile `"}"' _n
		}
		file close dofile
	
		* restore primary data
		restore
		
		* execute the .do file to actually apply all corrections
		do "`tempdo'"

		* re-save data
		save "`dtafile'", replace
	}
	else {
		* restore primary data		
		restore
	}

	disp
	disp "Finished applying corrections in: `corrfile'"
	disp
}
