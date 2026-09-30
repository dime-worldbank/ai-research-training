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
# MAGIC `Coding-Rubric.R` defines 20 comparable variables derived from the questionnaire's five sections. This exercise loads that rubric and applies it.
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

# COMMAND ----------

library(httr2)
library(jsonlite)
library(dplyr)
library(purrr)
library(stringr)
library(tibble)
library(tidyr)
library(ggplot2)

# COMMAND ----------

# The API base URL is available as an environment variable in MEGA
api_base_url <- Sys.getenv("CONVERSATIONALAI_BASE_URL")

# For this exercise we will use Clause Sonnet 4.6. You can select any other endpoint of your choice here: https://ai.worldbankgroup.org/maifactory/
CLAUDE_ENDPOINT <- "https://azapim.worldbank.org/maifactory/bedrock/model/us.anthropic.claude-sonnet-4-6/converse"

# COMMAND ----------

int1_path <- "/Volumes/prd_mega/spytho27/vpytho27/Workspace/mai_exercise/Interview 1.txt"
int2_path <- "/Volumes/prd_mega/spytho27/vpytho27/Workspace/mai_exercise/Interview 2.txt"

# COMMAND ----------

# Load the Coding Rubric
%run "./Coding_Rubric"

# COMMAND ----------

# These are the names of the colleagues who carried out the interviews. Their words will be excluded from coding.
interviewers <- c("Marina Visintini", "Elda Celislami")

# We will run the exercise first on a subset of chunks from one interview, and end with both transcripts in full
DEMO_CHUNKS <- 3

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Conversational AI gateway
# MAGIC
# MAGIC Every model is reached through the same gateway URL, with the
# MAGIC actual model chosen via the `mai-endpoint` query parameter. `call_conversational_ai()` wraps that pattern once 

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
  result$output$message$content[[1]]$text
}

# COMMAND ----------

#Let's test if it works
call_claude("I say ping, you say?")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Read a transcript
# MAGIC
# MAGIC The transcripts are txt documents where each paragraph is one speaker turn:
# MAGIC a "Speaker Name   H:MM" header line, followed by the (often auto-transcribed
# MAGIC and imperfect) spoken text. 

# COMMAND ----------

#the txt file were converted from Word documents, which uses a Unicode line separator character rather than a normal newline
LINE_SEP <- intToUtf8(8232)

read_transcript_paragraphs <- function(path) {
  raw <- readLines(path, encoding = "UTF-8", warn = FALSE)
  raw <- str_remove(raw, paste0("^", LINE_SEP)) 
  raw <- str_trim(raw)
  raw[nzchar(raw)]
}

# Matches "Speaker Name   0:03<LINE_SEP><turn text, possibly several sentences>"
# so that we can separate interviewer and interviewee transcription
turn_pattern <- regex(
  paste0("^\\s*([A-Za-zÀ-ÖØ-öø-ÿ' .]+?)\\s+(\\d{1,2}:\\d{2}(?::\\d{2})?)", LINE_SEP, "(.*)$"),
  dotall = TRUE
)

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

# Run it on one of the interview transcripts, and immediately drop every turn from known `interviewers`

int1_turns <- read_transcript_paragraphs(int1_path) %>%
  parse_turns() %>%
  filter(!speaker %in% interviewers)

display(int1_turns)
count(int1_turns, speaker)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Chunk turns for the API
# MAGIC
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

# Render a set of turns into the plain-text block we hand to the model, and
# back again once the model returns the same shape translated.
format_turns_block <- function(turns_df, text_col) {
  paste0(turns_df$speaker, " | ", turns_df$timestamp, " | ", turns_df[[text_col]],
         collapse = "\n")
}

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

translate_chunk <- function(chunk_df) {
  prompt <- build_translation_prompt(chunk_df)
  response <- call_claude(prompt, max_tokens = 3000, temperature = 0)
  parse_translation_response(response, chunk_df)
}

# COMMAND ----------

#Let's try it on some chunks!

int1_demo <- map_dfr(
  split(int1_turns, int1_turns$chunk_id)[1:DEMO_CHUNKS],
  translate_chunk
)

int1_demo %>% select(speaker, timestamp, text_it, text_en) %>% display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Step 2 - Code against the rubric
# MAGIC
# MAGIC `coding_rubric` (loaded from `Coding-Rubric.R` in step 0) defines 20
# MAGIC variables across the questionnaire's five themes. For each one, the model
# MAGIC returns:
# MAGIC - `category_value`:exactly one option from that variable's fixed list
# MAGIC - `text_value`: a verbatim quote from the transcript (or several,
# MAGIC   joined with `[...]`), never a paraphrase
# MAGIC
# MAGIC The rule that makes this comparable rather than just quote-tagging. If the transcript never addresses a variable, both fields will come back "Not stated".

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
    "fixed rubric of ", nrow(rubric), " comparable variables. The interview ",
    "is with a regional Managing Authority about EU-funded programme data ",
    "and reporting processes.\n\n",
    "RUBRIC:\n", rubric_block, "\n\n",
    "The transcript below has already had the interviewer's questions removed ",
    "-- every line is the interviewee speaking. It will read as fragmented in ",
    "places because of that; treat consecutive lines as one continuous answer ",
    "where that seems to be the case.\n\n",
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

# Models sometimes wrap JSON in ```json fences despite instructions not to.
# We can strip those defensively.
strip_code_fences <- function(text) {
  text <- str_trim(text)
  text <- str_remove(text, "^```(json)?\\s*")
  text <- str_remove(text, "```\\s*$")
  str_trim(text)
}

# Validation: Checks that every returned quote is a real substring of what was actually
# sent to the model. This catches a paraphrase or a fabricated quote. 

verify_quotes_are_correct <- function(coded, translated_turns, interview_label) {
  source_text <- paste(translated_turns$text_en, collapse = " ")

  is_correct<- function(text_value) {
    if (is.na(text_value) || text_value == "Not stated") return(TRUE)
    quotes <- str_trim(str_split(text_value, "\\s*\\[\\.\\.\\.\\]\\s*")[[1]])
    all(str_detect(source_text, fixed(quotes)))
  }

  flagged <- coded %>% filter(!map_lgl(text_value, is_correct))

  if (nrow(flagged) > 0) {
    warning(sprintf(
      "'%s': %d quote(s) not found verbatim in the transcript text. Check variable_id(s): %s",
      interview_label, nrow(flagged), paste(flagged$variable_id, collapse = ", ")
    ))
  }
}



# COMMAND ----------

# Now we can bring all of these functions together in one, so we can handle errors gracefully

code_interview <- function(translated_turns, rubric, interview_label) {
  prompt <- build_rubric_coding_prompt(translated_turns, rubric)
  response <- call_claude(prompt, max_tokens = 4000, temperature = 0)

  parsed <- tryCatch(
    jsonlite::fromJSON(strip_code_fences(response), simplifyDataFrame = TRUE),
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
    select(theme_code, theme_label, variable_id, guide_question) %>%
    left_join(as_tibble(parsed), by = "variable_id")

  verify_quotes_are_correct(coded, translated_turns, interview_label)
  coded
}

# COMMAND ----------

#Let's try on our interview subset - the one we translated before!

int1_demo_coded <- code_interview(int1_demo, coding_rubric, "Interview 1 (demo)")
display(int1_demo_coded)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Run the pipeline on both transcripts
# MAGIC
# MAGIC First we will consolidate the entire pipeline in a single function, 
# MAGIC and then we will run it on the two sample transcripts provided
# MAGIC

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

transcript_paths <- c(int1_path, int2_path)

all_coded <- bind_rows(lapply(transcript_paths, function(p) {
  label <- tools::file_path_sans_ext(basename(p))
  process_transcript(p, label, coding_rubric, interviewers = interviewers)
}))

display(all_coded)