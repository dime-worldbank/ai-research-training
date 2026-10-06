# Databricks notebook source
# MAGIC %md
# MAGIC # Exercise: Translating and Coding Interview Transcripts with AI
# MAGIC
# MAGIC This exercise shows how the **MAI Factory Conversational AI API** can support a common
# MAGIC  research task: turning long, messy, foreign-language interview
# MAGIC transcripts into a structured, English-language dataset that is ready for
# MAGIC cross-case comparison.
# MAGIC
# MAGIC We use two real (MS Teams-transcribed) interviews conducted in Italian about data processes, guided by a shared questionnaire with five thematic sections.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Pipeline
# MAGIC 1. **Read & parse** the transcript into speaker turns (docx -> structured rows)
# MAGIC 2. **Chunk** turns into batches small enough to send to the API
# MAGIC 3. **Translate** each chunk from Italian to English (AI call #1)
# MAGIC 4. **Code** the full translated transcript against the fixed rubric (AI
# MAGIC    call #2)
# MAGIC 5. **Assemble** a comparison matrix: one column per rubric variable, one
# MAGIC    row per region

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0. Setup
# MAGIC
# MAGIC First, make sure you selected the right compute. 

# COMMAND ----------

library(httr2)
library(jsonlite)
library(dplyr)
library(purrr)
library(stringr)
library(tibble)
library(tidyr)

# COMMAND ----------

# MAGIC %md
# MAGIC Set the two addresses every API call needs:
# MAGIC - `api_base_url` is the MAI Factory gateway. MEGA stores it in the environment variable
# MAGIC   `CONVERSATIONALAI_BASE_URL`, so we read it from there instead of typing it out.
# MAGIC - `CLAUDE_ENDPOINT` names the model we want behind that gateway, in this case Claude Sonnet 4.6.
# MAGIC   To try a different model, swap in another endpoint from the MAI Factory catalog. You can see the catalog [here](https://ai.worldbankgroup.org/maifactory/)

# COMMAND ----------

# The API base URL is available as an environment variable in MEGA
api_base_url <- Sys.getenv("CONVERSATIONALAI_BASE_URL")

# For this exercise we will use Claude Haiku 4.5. 
CLAUDE_ENDPOINT <- "https://azapim.worldbank.org/maifactory/bedrock/model/us.anthropic.claude-haiku-4-5-20251001-v1:0/converse"

# COMMAND ----------

# MAGIC %md
# MAGIC Point to the two interview transcripts. They are stored in a Databricks **Volume**, which is
# MAGIC why the paths start with `/Volumes/...`. Nothing is read yet; we only save the paths.

# COMMAND ----------

int1_path <- "/Volumes/prd_mega/spytho27/vpytho27/Workspace/mai_exercise/Interview 1.txt"
int2_path <- "/Volumes/prd_mega/spytho27/vpytho27/Workspace/mai_exercise/Interview 2.txt"

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## 1. Conversational AI gateway
# MAGIC
# MAGIC `call_conversational_ai()` sends one request to the gateway and returns the response as an R list.
# MAGIC Step by step, it:
# MAGIC 1. adds `mai-endpoint` (which model to use), plus any extra parameters, to the URL as query parameters
# MAGIC 2. attaches `payload` (the prompt and its settings) as the JSON body of the request
# MAGIC 3. retries up to 3 times if the request fails, waiting 2 and then 4 seconds between attempts
# MAGIC 4. sends the request and converts the JSON response into an R list
# MAGIC
# MAGIC This function works for any model in the catalog; it doesn't know anything about Claude.

# COMMAND ----------

call_conversational_ai <- function(endpoint, payload, extra_params = list()) {
  params <- c(list(`mai-endpoint` = endpoint), extra_params)

  req <- request(api_base_url) %>%
    req_url_query(!!!params) %>%
    req_body_json(payload) %>%
    req_retry(max_tries = 3, backoff = \(i) 2^i)

  resp <- req_perform(req)
  resp_body_json(resp)
}

# COMMAND ----------

# MAGIC %md
# MAGIC `call_claude()` is a Claude-specific wrapper around `call_conversational_ai()`, so the rest of the
# MAGIC notebook can send a prompt and get text back in a single line. It:
# MAGIC 1. builds the payload in the format Claude expects: a single user message with the prompt, and
# MAGIC    `max_tokens`, the maximum length of the reply
# MAGIC 2. passes `temperature` along if you set one. A temperature of 0 makes the output as consistent
# MAGIC    as possible from one run to the next, which is what we want for translation and coding.
# MAGIC 3. sends the request to `CLAUDE_ENDPOINT` and pulls the reply text out of the response

# COMMAND ----------

# Setup: one call equals one prompt in, one text response out.
call_claude <- function(prompt, max_tokens = 2048, temperature = NULL) {
  payload <- list(
    anthropic_version = "bedrock-2023-05-31",
    max_tokens = max_tokens,
    messages = list(
      list(role = "user", content = list(list(type = "text", text = prompt)))
    )
  )

  extra_params <- list()
  if (!is.null(temperature)) extra_params$temperature <- temperature

  result <- call_conversational_ai(CLAUDE_ENDPOINT, payload, extra_params)

  # Extract text and check for gateway refusals
  text <- result$output$message$content[[1]]$text
  stop_reason <- result$stopReason %||% "unknown"

  if (is.null(text) || grepl("^Sorry, the model cannot", text)) {
    detail <- paste0(
      "Gateway refused the request.",
      "\n  stopReason: ", stop_reason,
      "\n  response text: ", substr(text %||% "<NULL>", 1, 200),
      "\n  endpoint: ", CLAUDE_ENDPOINT
    )
    stop(detail, call. = FALSE)
  }

  text
}

# COMMAND ----------

# MAGIC %md
# MAGIC A quick test before we build anything on top of the connection: send a short prompt and print
# MAGIC Claude's reply. If you see a sensible answer, the gateway, the endpoint and our two functions
# MAGIC all work. If you get an error instead, fix it here before moving on.

# COMMAND ----------

#Let's test if it works
call_claude("Knock knock?")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Read a transcript
# MAGIC
# MAGIC The transcripts are txt documents where each paragraph is one speaker turn:
# MAGIC a "Speaker Name   H:MM" header line, followed by the (often auto-transcribed
# MAGIC and imperfect) spoken text.

# COMMAND ----------

# MAGIC %md
# MAGIC `read_transcript_paragraphs()` reads a transcript file into a character vector with one element per
# MAGIC paragraph. It:
# MAGIC 1. reads the file line by line as UTF-8, so Italian accents come through correctly
# MAGIC 2. removes the invisible line separator (`LINE_SEP`) that Word sometimes leaves at the start of a
# MAGIC    line, then trims surrounding spaces
# MAGIC 3. drops empty lines
# MAGIC
# MAGIC Inside each paragraph, the speaker header and the spoken text are still separated by `LINE_SEP`.
# MAGIC The next cell uses it to split them.

# COMMAND ----------

#the txt file were converted from Word documents, which uses a Unicode line separator character rather than a normal newline
LINE_SEP <- intToUtf8(8232)

read_transcript_paragraphs <- function(path) {
  raw <- readLines(path, encoding = "UTF-8", warn = FALSE)
  raw <- str_remove(raw, paste0("^", LINE_SEP))
  raw <- str_trim(raw)
  raw[nzchar(raw)]
}

# COMMAND ----------

# MAGIC %md
# MAGIC `turn_pattern` is a regular expression that recognizes a speaker turn and splits it into three
# MAGIC parts (capture groups):
# MAGIC 1. **speaker:** a name made of letters (including accented ones), spaces, apostrophes and periods
# MAGIC 2. **timestamp:** `M:SS` or `H:MM:SS`, for example `0:03` or `1:02:45`
# MAGIC 3. **text:** everything after the `LINE_SEP` that follows the timestamp
# MAGIC
# MAGIC `dotall = TRUE` lets the text part run across several lines, so a long answer is kept whole.

# COMMAND ----------

# Matches "Speaker Name   0:03<LINE_SEP><turn text, possibly several sentences>"
# so that we can separate interviewer and interviewee transcription
turn_pattern <- regex(
  paste0("^\\s*([A-Za-zÀ-ÖØ-öø-ÿ' .]+?)\\s+(\\d{1,2}:\\d{2}(?::\\d{2})?)", LINE_SEP, "(.*)$"),
  dotall = TRUE
)

# COMMAND ----------

# MAGIC %md
# MAGIC `parse_turns()` applies `turn_pattern` to every paragraph and returns a table with one row per
# MAGIC speaker turn and three columns: `speaker`, `timestamp` and `text_it` (the Italian text).
# MAGIC
# MAGIC Paragraphs that don't match the pattern, such as the title, the date or "recording started",
# MAGIC are dropped. In the text, any remaining line separators are replaced with spaces and repeated
# MAGIC whitespace is collapsed.

# COMMAND ----------

# Paragraphs that don't match (title, date, "recording started/stopped") are
# metadata, not spoken turns, and can be dropped.
parse_turns <- function(paragraphs) {
  m <- str_match(paragraphs, turn_pattern)
  matched <- !is.na(m[, 1])
  tibble(
    speaker = str_trim(m[matched, 2]),
    timestamp = str_trim(m[matched, 3]),
    text_it = str_squish(str_replace_all(m[matched, 4], LINE_SEP, " "))
  )
}

# COMMAND ----------

# MAGIC %md
# MAGIC Now we run both functions on Interview 1: read the paragraphs, parse them into turns, and
# MAGIC filter out every turn spoken by one of the `interviewers`. The result, `int1_turns`, holds only
# MAGIC the interviewee's answers.

# COMMAND ----------

# Run it on one of the interview transcripts, and immediately drop every turn from known `interviewers`

interviewers <- c("Marina Visintini", "Elda Celislami")

int1_turns <- read_transcript_paragraphs(int1_path) %>%
  parse_turns() %>%
  filter(!speaker %in% interviewers)

display(int1_turns)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Chunk turns for the API
# MAGIC
# MAGIC `chunk_turns()` adds a `chunk_id` column that assigns every turn to a chunk. It:
# MAGIC 1. estimates the size of each turn: the length of the text, plus the speaker name, plus 10
# MAGIC    characters for the timestamp and separators
# MAGIC 2. goes through the turns in order, adding each one to the current chunk
# MAGIC 3. starts a new chunk when the next turn would push the current one over `max_chars` (3,000
# MAGIC    characters by default)
# MAGIC
# MAGIC Turns are never split or reordered. A single turn longer than `max_chars` becomes a chunk on its own.
# MAGIC
# MAGIC **Why not just send each turn?**
# MAGIC Sending one turn per API call would be slow and would strip away
# MAGIC conversational context (a short "Ok." only makes sense next to the question
# MAGIC that prompted it). Instead we group consecutive turns into chunks up to a
# MAGIC character budget to stay comfortably inside the model's context window.

# COMMAND ----------

chunk_turns <- function(turns, max_chars = 3000) {
  sizes <- nchar(turns$text_it) + nchar(turns$speaker) + 10
  chunk_id <- integer(nrow(turns))
  running <- 0
  current <- 1
  for (i in seq_len(nrow(turns))) {
    if (running + sizes[i] > max_chars && running > 0) {
      current <- current + 1
      running <- 0
    }
    chunk_id[i] <- current
    running <- running + sizes[i]
  }
  turns$chunk_id <- chunk_id
  turns
}

# COMMAND ----------

# MAGIC %md
# MAGIC Apply `chunk_turns()` to Interview 1, then count the turns in each chunk.

# COMMAND ----------

# Assign each turn of the first interview to a chunk
int1_turns <- chunk_turns(int1_turns)

display(int1_turns)


# COMMAND ----------

#this is the amount of calls we will need to make to process our interview
max(int1_turns$chunk_id)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Step 1 - Translate
# MAGIC
# MAGIC We ask the model to translate turn-by-turn and preserve the
# MAGIC `Speaker | Timestamp | Text` structure exactly, so the response can be
# MAGIC parsed straight back into a data frame. Being explicit about the output
# MAGIC format is what makes an LLM call usable as a pipeline step rather than a
# MAGIC one-off chat answer.
# MAGIC
# MAGIC **Note on the translated transcript:** as the exercise is set up, the
# MAGIC translation lives only in memory for the duration of this function call
# MAGIC it's used to build the coding prompt and then discarded. That's fine for
# MAGIC this exercise, but it means you can't go back later to re-read the full
# MAGIC English transcript against a coded quote, and re-coding with a revised
# MAGIC rubric means paying to re-translate. A production version of this
# MAGIC pipeline save the translation (e.g. to a CSV file) as its own output,
# MAGIC separate from the coded table.

# COMMAND ----------

# MAGIC %md
# MAGIC First, we need to take the "rows" in our table, and transform them into plain text. For that we use the `format_turns_block` function. The `text_col` argument picks which
# MAGIC text to use: `"text_it"` for the Italian original when we translate, `"text_en"` for the English
# MAGIC translation when we code.

# COMMAND ----------

format_turns_block <- function(turns_df, text_col) {
  paste0(turns_df$speaker, " | ", turns_df$timestamp, " | ", turns_df[[text_col]],
         collapse = "\n")
}

# COMMAND ----------

# MAGIC %md
# MAGIC `build_translation_prompt()` writes the instructions for one chunk. The prompt has three parts:
# MAGIC 1. **context:** what the text is (an auto-transcribed Italian interview about EU-funded programme
# MAGIC    monitoring) and what the translation is for
# MAGIC 2. **rules:** keep names and timestamps unchanged, translate literally without summarizing,
# MAGIC    handle transcription errors sensibly, and return only the translated lines
# MAGIC 3. **the chunk itself**
# MAGIC
# MAGIC Asking for the same `Speaker | Timestamp | Text` format we send is what lets the next function
# MAGIC read the answer back into the table.

# COMMAND ----------

build_translation_prompt <- function(chunk_df) {
  block <- format_turns_block(chunk_df, "text_it")
  paste0(
    "You are translating an excerpt of an auto-transcribed Italian interview ",
    "into English for qualitative analysis. The interview concerns EU-funded ",
    "programme monitoring and reporting processes.\n\n",
    "Translate each line below from Italian to English. Keep the exact same ",
    "structure: one line per turn, formatted as\n",
    "Speaker | Timestamp | English text\n\n",
    "Rules:\n",
    "- Keep speaker names and timestamps unchanged.\n",
    "- Translate literally; do not summarize, omit, or add commentary.\n",
    "- The source is an imperfect auto-transcription (filler words, false ",
    "starts, occasional garbled words) -- translate as sensibly as possible ",
    "without inventing meaning.\n",
    "- Return ONLY the translated lines, nothing else.\n\n",
    "TRANSCRIPT EXCERPT:\n", block
  )
}

# COMMAND ----------

# MAGIC %md
# MAGIC `parse_translation_response()` reads the model's reply back into the chunk's table.

# COMMAND ----------

parse_translation_response <- function(response_text, chunk_df) {
  lines <- str_split(str_trim(response_text), "\n")[[1]]
  lines <- lines[nzchar(str_trim(lines))]
  parts <- str_split_fixed(lines, "\\s*\\|\\s*", 3)

  # Guard against the model dropping or merging a line: fall back to the
  # original turns (marked untranslated) rather than silently misaligning
  # speakers/timestamps with the wrong text.
  if (nrow(parts) != nrow(chunk_df)) {
    warning(sprintf(
      "Translation line count mismatch (expected %d, got %d) -- keeping original text for this chunk.",
      nrow(chunk_df), nrow(parts)
    ))
    return(chunk_df %>% mutate(text_en = text_it))
  }

  chunk_df %>% mutate(text_en = str_trim(parts[, 3]))
}

# COMMAND ----------

# MAGIC %md
# MAGIC `translate_chunk()` performs the actual translation, using the three functions we built before: build the prompt, send it
# MAGIC to Claude with `temperature = 0` and room for up to 3,000 tokens of output, and parse the reply.
# MAGIC It returns the chunk's table with the `text_en` column added.

# COMMAND ----------

translate_chunk <- function(chunk_df) {
  prompt <- build_translation_prompt(chunk_df)
  response <- call_claude(prompt, max_tokens = 3000, temperature = 0)
  parse_translation_response(response, chunk_df)
}

# COMMAND ----------

# MAGIC %md
# MAGIC Now we are ready to translate the first chunk of Interview 1!

# COMMAND ----------

# We will run the exercise first on a subset of chunks from one interview, and end with both transcripts in full
DEMO_CHUNKS <- 3

int1_demo <- map_dfr(
  head(split(int1_turns, int1_turns$chunk_id), DEMO_CHUNKS),
  translate_chunk
)

int1_demo %>% select(speaker, timestamp, text_it, text_en) %>% display()

# COMMAND ----------

# MAGIC %md
# MAGIC Now that we have translated our interview, we need to code it. When we code an interview, we normally want to map the answers to a series of predetermined labels. 
# MAGIC
# MAGIC For example, these interviews were about data processes followed by civil servants. 
# MAGIC - The first section of our questionnaire was about Data Collection.
# MAGIC - The first question was about the extent to which data collection processes are manual vs automated.
# MAGIC - Therefore, we want to map the answer to one of the following: Fully manual, Fully automated or Hybrid
# MAGIC
# MAGIC Every questions will have their own set of labels for coding. We define those in the `coding_rubric`

# COMMAND ----------

# DBTITLE 1, 
coding_rubric <- tribble(
  ~variable_id, ~guide_question, ~category_options,
  
  "data_entry_automation", "Which steps of end to end data collection and validation are manual, and which are automated?", "Fully manual | Fully automated | Hybrid (some manual, some automated)",
  
  "validation_responsibility", "Who does what (roles and responsibilities) across the different validation handoffs?", "Single role/unit | Multiple roles within one authority | Multiple external and internal actors",
  
  "collection_channel", "What channels, templates and tools are used to collect data from beneficiaries/implementers?", "Single IT system or portal | Multiple systems/channels | Manual or offline (email, paper, spreadsheets)",
  
  "delay_hotspot", "Where do delays most often concentrate, and how are they escalated or supported?", "At beneficiary/implementer submission | At validation/review | At handoff between units | No delays reported",
  
  "access_control_model", "How are permissions and access managed, covering roles, profiling, onboarding/offboarding?", "Role based access control | Open/shared access | Not formally managed",
  
  "data_storage_location", "Where are data entered and maintained: regional system, portals, or elsewhere?", "Regional/local system | National system directly | Mixed (local and national)",
  
  "extraction_source", "From which system(s) do you extract data for reporting?", "Same system as entry | Separate reporting/BI system | Manual export or compilation",
  
  "duplication_reentry", "At which points do duplications or repeat entries happen, and why?", "Duplication or repeat entry reported | No duplication reported",
  
  "analytic_use", "Which analyses do you use the data for, such as progress monitoring, performance, or outcomes?", "Progress monitoring only | Progress + performance | Progress + outcomes/evaluation",
  
  "responsible_unit", "Which unit is responsible for analysis, including an evaluation unit if one exists?", "Monitoring unit only | Dedicated evaluation unit exists | Split across multiple offices",
  
  "external_microdata", "Which external microdata (e.g. firms, labour, procurement) are or would be integrated, and how?", "Already integrated | Attempted, not achieved | Desired, not attempted | None mentioned",
  
  "compliance_vs_analytic_value","Which elements of required data collection are analytically useful vs. mainly driven by compliance?", "Mostly analytically useful | Mostly driven by compliance | Mixed view given",
  
  "anomaly_detection_method", "How are inconsistencies or issues in the data detected and handled?", "Automated system checks/alerts | Manual review | Combination of automated and manual",
  
  "quality_kpi_tracking", "Are there dashboards, periodic lists, or internal KPIs (update times, error rates, backlog, etc.)?", "Formal KPIs/dashboard in place | Informal/ad hoc tracking only | No tracking reported",
  
  "recurrent_error_type", "What types of errors/anomalies are most recurrent, and what do they typically depend on?", "Missing/incomplete data | Miscoding/misclassification | Timing/deadline issues | Multiple types reported",
  
  "recent_standard_change", "In the last 12 months, were there updates to standards/codifications/controls requiring action?", "Change reported, high impact | Change reported, low impact | No change reported",
  
  "data_freeze_practice", "Are there moments when data are frozen/consolidated for official reporting or audit?", "Formal freeze/consolidation process exists | No formal freeze process",
  
  "effort_hotspot", "Which process steps require the most effort, or become most demanding/complex?", "Names a specific step | General/diffuse difficulty | No hotspot reported",
  
  "external_requirement_burden", "Which external (EU or national) requirements require the most resources to implement?", "EU level requirement named | National level requirement named | Both named | None named",
  
  "simplification_opportunity", "Looking ahead, are there opportunities to simplify the process while staying compliant?", "Opportunity identified | No opportunity identified"
)


# COMMAND ----------

# MAGIC %md
# MAGIC `build_rubric_coding_prompt()` writes the coding instructions. Unlike translation, coding sends
# MAGIC the **whole** translated transcript in a single prompt, because an answer to one rubric question
# MAGIC can come up anywhere in the interview. The prompt contains:
# MAGIC 1. **the rubric:** each variable numbered, with its guide question and allowed categories
# MAGIC 2. **context:** the interviewer's lines have been removed, so the text may read as fragmented
# MAGIC 3. **the rules:** code all 20 variables, never infer, use "Not stated" when a topic isn't
# MAGIC    addressed, and quote word for word
# MAGIC 4. **the output format:** a JSON array with one object per variable, each with `variable_id`,
# MAGIC    `category_value` and `text_value`
# MAGIC 5. **the transcript**, formatted by `format_turns_block()` using the English text

# COMMAND ----------

build_rubric_coding_prompt <- function(translated_turns, rubric) {
  transcript_block <- format_turns_block(translated_turns, "text_en")
  rubric_block <- paste0(
    seq_len(nrow(rubric)), ". variable_id: ", rubric$variable_id,
    "\n   question: ", rubric$guide_question,
    "\n   allowed categories: ", rubric$category_options,
    collapse = "\n\n"
  )

  paste0(
    "You are coding an English-translated interview transcript against a ",
    "fixed rubric of ", nrow(rubric), " comparable variables. ",
    "RUBRIC:\n", rubric_block, "\n\n",
    "The transcript below has already had the interviewer's questions removed ",
    "-- every line is the interviewee speaking. Treat consecutive lines ",
    "as one continuous answer where that seems to be the case.\n\n",
    "TASK: For every variable_id listed above (all ", nrow(rubric),
    " of them, no more, no fewer), determine its value strictly from what ",
    "the interviewee explicitly says below.\n\n",
    "CRITICAL RULES:\n",
    "1. Do not infer. If the interviewee does not explicitly address a ",
    "variable, set both category_value and text_value to exactly ",
    "\"Not stated\". Never fill in a value based on what is typical, what ",
    "other regions do, or what seems implied -- only what is explicitly said ",
    "below.\n",
    "2. text_value must be verbatim, not a paraphrase or summary. Copy the ",
    "exact wording from the text below. If the evidence spans more than one ",
    "non-contiguous passage, quote each and join them with \" [...] \".\n\n",
    "Return ONLY a JSON array of ", nrow(rubric), " objects (no prose, no ",
    "markdown fences), each with exactly these fields:\n",
    "  variable_id (string, copied exactly from the rubric)\n",
    "  category_value (string, copied exactly from that variable's allowed ",
    "categories, or \"Not stated\")\n",
    "  text_value (string, one or more verbatim quotes copied exactly from ",
    "the text below, joined with \" [...] \" if not contiguous, or exactly ",
    "\"Not stated\")\n\n",
    "INTERVIEWEE (Speaker | Timestamp | English text):\n", transcript_block
  )
}

# COMMAND ----------

# MAGIC %md
# MAGIC `verify_quotes_are_correct()` checks the model's quotes against the source.
# MAGIC If any quote isn't found, it shows a warning listing the `variable_id`s to review by hand. A failed
# MAGIC check usually means the model paraphrased or tidied up the wording. The function only warns; it
# MAGIC doesn't change the coded table.

# COMMAND ----------


normalize_for_match <- function(x) {
  x <- str_replace_all(x, "[‘’]", "'")
  x <- str_replace_all(x, "[“”]", "\"")
  x <- str_replace_all(x, "…", "...")
  str_squish(str_to_lower(x))
}

verify_quotes_are_correct <- function(coded, translated_turns, interview_label) {
  source_text <- normalize_for_match(paste(translated_turns$text_en, collapse = " "))

  is_correct <- function(text_value) {
    if (is.na(text_value) || text_value == "Not stated") return(NA)
    quotes <- str_split(text_value, "\\s*\\[\\.\\.\\.\\]\\s*")[[1]]
    quotes <- normalize_for_match(quotes)
    quotes <- str_remove_all(quotes, "^[[:punct:]\\s]+|[[:punct:]\\s]+$")
    quotes <- quotes[nzchar(quotes)]
    length(quotes) > 0 && all(str_detect(source_text, fixed(quotes)))
  }

  coded <- coded %>% mutate(quote_verified = map_lgl(text_value, is_correct))
  flagged <- coded %>% filter(quote_verified %in% FALSE)

  if (nrow(flagged) > 0) {
    warning(sprintf(
      "'%s': %d quote(s) not found in the transcript text. Check variable_id(s): %s",
      interview_label, nrow(flagged), paste(flagged$variable_id, collapse = ", ")
    ))
  }

  coded
}


# COMMAND ----------

# DBTITLE 1, 
# MAGIC %md
# MAGIC `code_interview()`:
# MAGIC 1. Builds the prompt and sends it to Claude 
# MAGIC 2. parses the JSON reply into a table (stripping markdown fences if present). If the JSON can't be
# MAGIC    parsed, it shows a warning and returns an empty table instead of stopping the notebook.
# MAGIC 3. warns if the model returned more or fewer than 20 variables
# MAGIC 4. joins the answers onto the rubric by `variable_id`, so the result always has all 20 variables
# MAGIC    in rubric order, with their theme and guide question. A variable the model skipped shows up as `NA`.
# MAGIC 5. runs `verify_quotes_are_correct()` on the result

# COMMAND ----------

# DBTITLE 1, 
# Bring all coding functions together, with graceful error handling

code_interview <- function(translated_turns, rubric, interview_label) {
  prompt <- build_rubric_coding_prompt(translated_turns, rubric)
  response <- call_claude(prompt, max_tokens = 3000, temperature = 0)

  parsed <- tryCatch(
    jsonlite::fromJSON(gsub("^```(json)?\\s*|```\\s*$", "", str_trim(response)), simplifyDataFrame = TRUE),
    error = function(e) {
      warning(sprintf("Could not parse coding JSON for '%s': %s", interview_label, e$message))
      NULL
    }
  )

  if (is.null(parsed) || length(parsed) == 0) {
    return(tibble(variable_id = character(), category_value = character(), text_value = character()))
  }

  if (nrow(parsed) != nrow(rubric)) {
    warning(sprintf(
      "'%s': expected %d coded variables, got %d -- unmatched variables will show as missing.",
      interview_label, nrow(rubric), nrow(parsed)
    ))
  }

  coded <- rubric %>%
    select(variable_id, guide_question) %>%
    left_join(as_tibble(parsed), by = "variable_id")

  verify_quotes_are_correct(coded, translated_turns, interview_label)
  coded
}

# COMMAND ----------

# MAGIC %md
# MAGIC Code the demo translation from Step 1 (`int1_demo`) against the rubric. This is one API call.
# MAGIC
# MAGIC We only translated the first few chunks, so expect many variables to come back "Not stated": the
# MAGIC interviewee hasn't reached those topics yet. That is the rubric's no-inference rule at work.

# COMMAND ----------

# DBTITLE 1, 
int1_demo_coded <- code_interview(int1_demo, coding_rubric, "Interview 1 (demo)")

display(int1_demo_coded %>% mutate(across(where(is.list), as.character)))

# COMMAND ----------

# DBTITLE 1, 
# MAGIC %md
# MAGIC ## 6. Temperature sensitivity and reproducibility
# MAGIC
# MAGIC Before running the full pipeline, let's check how robust the coding step is.
# MAGIC 1. **Sensitivity:** do answers change when we raise the temperature?
# MAGIC 2. **Reproducibility:** does the same temperature give the same answer every time?
# MAGIC
# MAGIC We re-code the demo translation (`int1_demo`) at several temperatures (0, 0.3, 0.7, 1.0),
# MAGIC running each one multiple times.

# COMMAND ----------

# DBTITLE 1, 
# Code the demo translation at several temperatures, with multiple reps each
temperatures <- c(0, 0.3, 0.7, 1.0)
N_REPS <- 5   # repetitions per temperature

prompt <- build_rubric_coding_prompt(int1_demo, coding_rubric)

code_at_temp <- function(temp, rep) {
  tryCatch({
    response <- call_claude(prompt, max_tokens = 4000, temperature = temp)
    parsed  <- jsonlite::fromJSON(gsub("^```(json)?\\s*|```\\s*$", "", str_trim(response)), simplifyDataFrame = TRUE)
    as_tibble(parsed) %>%
      select(variable_id, category_value) %>%
      mutate(temperature = temp, rep = rep, .before = 1)
  }, error = function(e) {
    warning(sprintf("temp=%s rep=%d failed: %s", temp, rep, e$message))
    tibble(temperature = temp, rep = rep,
           variable_id = coding_rubric$variable_id,
           category_value = NA_character_)
  })
}

# Build the grid of (temperature, rep) pairs and run each with a short pause
runs <- expand.grid(temp = temperatures, rep = seq_len(N_REPS))

temp_results <- bind_rows(Map(function(t, r) {
  Sys.sleep(2)
  code_at_temp(t, r)
}, runs$temp, runs$rep))

cat(sprintf("Collected %d rows across %d runs.\n", nrow(temp_results), nrow(runs)))

# COMMAND ----------

# MAGIC %md
# MAGIC For each temperature, we check how consistently the model coded each variable across repetitions.
# MAGIC A variable "matches every run" if all reps returned the same category; otherwise we report how
# MAGIC many reps agreed on the most common answer.

# COMMAND ----------

# DBTITLE 1, 
# For each (variable, temperature), find how many reps agreed on the answer
agreement <- temp_results %>%
  filter(!is.na(category_value)) %>%
  count(temperature, variable_id, category_value) %>%
  group_by(temperature, variable_id) %>%
  summarise(n_reps = sum(n), max_agree = max(n), .groups = "drop")

# Summarise per temperature: what share of variables matched in all reps, all-1, etc.
for (tmp in sort(unique(agreement$temperature))) {
  sub <- agreement %>% filter(temperature == tmp)
  total <- nrow(sub)
  cat(sprintf("\nTemperature %.1f:\n", tmp))
  for (k in sort(unique(sub$n_reps):1)) {
    n_vars <- sum(sub$max_agree == k)
    if (n_vars > 0) {
      cat(sprintf("Matched %d/%d times: %d variables (%.0f%%)\n",
                  k, sub$n_reps[1], n_vars, 100 * n_vars / total))
    }
  }
}

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Run the pipeline on both transcripts
# MAGIC
# MAGIC First we will consolidate the entire pipeline in a single function,
# MAGIC and then we will run it on the two sample transcripts provided
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC `process_transcript()` puts every step together for one transcript file:
# MAGIC 1. read and parse the file into turns
# MAGIC 2. drop the interviewers' turns and assign chunks
# MAGIC 3. keep the first `max_chunks` chunks (all of them by default, since `max_chunks = Inf`)
# MAGIC 4. translate each chunk
# MAGIC 5. code the full translation against the rubric
# MAGIC 6. add a `region` column as the first column, so results from different interviews can be stacked
# MAGIC
# MAGIC To test on a smaller sample, pass for example `max_chunks = 3`.

# COMMAND ----------

process_transcript <- function(path, region, rubric, interviewers, max_chunks = Inf) {
  all_turns <- read_transcript_paragraphs(path) %>% parse_turns()
  turns <- all_turns %>% filter(!speaker %in% interviewers) %>% chunk_turns()
  n_chunks <- min(max(turns$chunk_id), max_chunks)
  chunks_to_run <- split(turns, turns$chunk_id)[seq_len(n_chunks)]
  translated_turns <- map_dfr(chunks_to_run, translate_chunk)
  code_interview(translated_turns, rubric, region) %>%
    mutate(region = region, .before = 1)
}

# COMMAND ----------

# MAGIC %md
# MAGIC The final run. For each transcript path, we use the file name without its extension
# MAGIC (`"Interview 1"`, `"Interview 2"`) as the label, run `process_transcript()` on the full
# MAGIC interview, and stack the results with `bind_rows()`.
# MAGIC
# MAGIC `all_coded` has 40 rows: 20 rubric variables for each interview. Comparing the two interviews on
# MAGIC the same `variable_id` is the cross-case comparison the rubric was designed for.
# MAGIC
# MAGIC This cell makes one translation call per chunk plus one coding call per interview, so it takes
# MAGIC noticeably longer than the demo cells.

# COMMAND ----------

# transcript_paths <- c(int1_path, int2_path)

# all_coded <- bind_rows(lapply(transcript_paths, function(p) {
#   label <- tools::file_path_sans_ext(basename(p))
#   process_transcript(p, label, coding_rubric, interviewers = interviewers)
# }))

# display(all_coded)
