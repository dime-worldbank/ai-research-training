"""
Generate an HTML descriptive-statistics report for a survey CSV export.

Variable and value labels are parsed directly from the companion Stata
import script (import_ai_bootcamp_pre_survey.do), so chart titles and
category labels match the actual question wording and response options
instead of raw SurveyCTO field codes. Individual choice text for
select-multiple questions (which the .do file does not label option-by-
option) is pulled from the original XLSForm's "choices" sheet instead.

The export follows SurveyCTO's standard "select multiple" structure: for
each multi-select question there is one string column holding all the
space-separated codes a respondent picked (e.g. "1 3 5") plus one binary
0/1 column per option (e.g. q1_3_1, q1_3_2, ...). This script detects that
pattern automatically and summarizes each multi-select question as a single
bar chart of "percent who selected this option", rather than charting each
binary column on its own.

Remaining numeric columns with an explicit Stata value label (single-select
Likert/choice questions) are charted as categorical bar charts using the
labeled response text. Any numeric column with no value label and high
cardinality is treated as continuous and summarized in a stats table.
Columns that are record identifiers, platform metadata, entirely missing,
or high-cardinality free text are excluded and listed with a reason.

Usage:
    python descriptive_stats.py [input_csv] [do_file] [xlsform] [output_html]

Defaults to the baseline survey CSV/do-file/XLSForm in ../data, ../code,
and ../documentation, and writes to ../outputs.
"""

import base64
import io
import re
import sys
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# Columns that are survey-platform metadata, not substantive variables.
KNOWN_ID_COLUMNS = {"submissiondate", "instanceid", "formdef_version", "key", "upi"}

# A categorical column with more distinct values than this is treated as
# free text / too sparse to chart meaningfully.
MAX_CATEGORIES_TO_PLOT = 20

# A column where almost every value is unique is treated as an identifier.
ID_UNIQUE_RATIO = 0.9

# A numeric column with more distinct values than this (and no value label)
# is treated as continuous rather than categorical.
CONTINUOUS_CARDINALITY_THRESHOLD = 15

# A chart answered by fewer than this many respondents is dropped entirely:
# with so few responses, every bar tends to read "100%" or "0%", which is
# more misleading than informative (e.g. q1.2, a skip-pattern question only
# the 1 person who doesn't use GenAI for work ever saw).
MIN_N_FOR_CHART = 5


# --------------------------------------------------------------------------
# Parsing labels out of the Stata .do file
# --------------------------------------------------------------------------

def parse_do_file(do_path: Path):
    """Return (var_labels, value_labels) keyed by lowercased column name.

    var_labels:   {col_lower: full question text}
    value_labels: {col_lower: {code_str: response text}}
    """
    text = do_path.read_text(encoding="utf-8", errors="replace")

    var_labels = {}
    for m in re.finditer(r'^\s*(?:cap\s+)?label variable\s+(\w+)\s+"(.*)"\s*$', text, re.MULTILINE):
        col, label = m.group(1).lower(), m.group(2)
        var_labels.setdefault(col, label)

    # "note" lines carry the untruncated question text; prefer them.
    for m in re.finditer(r'^\s*note\s+(\w+):\s*"(.*)"\s*$', text, re.MULTILINE):
        col, label = m.group(1).lower(), m.group(2)
        var_labels[col] = label

    value_label_defs = {}
    for m in re.finditer(r'^\s*label define\s+(\w+)\s+(.*)$', text, re.MULTILINE):
        group, rest = m.group(1).lower(), m.group(2)
        pairs = re.findall(r'(\d+)\s+"([^"]*)"', rest)
        value_label_defs[group] = dict(pairs)

    value_labels = {}
    for m in re.finditer(r'^\s*label values\s+(\w+)\s+(\w+)\s*$', text, re.MULTILINE):
        col, group = m.group(1).lower(), m.group(2).lower()
        if group in value_label_defs:
            value_labels[col] = value_label_defs[group]

    return var_labels, value_labels


def parse_xlsform(xlsform_path: Path):
    """Return (question_to_list, list_to_choices) from an XLSForm's
    survey/choices sheets.

    question_to_list: {question_name_lower: list_name} for select_one/select_multiple questions
    list_to_choices:  {list_name: {code_str: choice label}}
    """
    if xlsform_path is None or not xlsform_path.exists():
        return {}, {}

    survey = pd.read_excel(xlsform_path, sheet_name="survey")
    choices = pd.read_excel(xlsform_path, sheet_name="choices")

    question_to_list = {}
    for _, row in survey.iterrows():
        m = re.match(r"select_(?:one|multiple)\s+(\S+)", str(row.get("type", "")))
        name = row.get("name")
        if m and pd.notna(name):
            question_to_list[str(name).strip().lower()] = m.group(1)

    list_to_choices = {}
    for _, row in choices.iterrows():
        list_name = row.get("list_name")
        code = row.get("name")
        label = row.get("label")
        if pd.isna(list_name) or pd.isna(code) or pd.isna(label):
            continue
        try:
            code_str = str(int(float(code)))
        except (TypeError, ValueError):
            code_str = str(code).strip()
        list_to_choices.setdefault(str(list_name).strip(), {})[code_str] = str(label).strip()

    return question_to_list, list_to_choices


def strip_dedup_suffix(col: str) -> str:
    """Pandas appends '.1', '.2', ... to duplicate CSV headers; undo that
    for label lookups (the duplicate is usually the *.do-labeled* variable,
    while the un-suffixed name is the raw select-multiple indicator)."""
    return re.sub(r"\.\d+$", "", col)


# Manual short titles for chart headings, used in place of the full question
# wording (which can run to 100+ characters and overlaps other elements on
# the chart). Keyed by column name (lowercase, dedup-suffix stripped).
TITLE_OVERRIDES = {
    "q1_1": "1.1 Current use of generative AI for work",
    "q1_2": "1.2 Reasons for not using GenAI at work",
    "q1_3": "1.3 AI tools used for work",
    "q1_4": "1.4 Time spent using GenAI per day",
    "q1_5": "1.5 Tasks GenAI was used for",
    "q1_6": "1.6 AI-assisted work included in outputs?",
    "q1_7": "1.7 Was AI use disclosed?",
    "q2_1": "2.1 Created an AI memory file?",
    "q2_2": "2.2 Used a reusable AI skill from someone else?",
    "q2_3": "2.3 Effects of AI on analytical work",
    "q2_3_1": "2.3.1 Extra output produced using AI",
    "q2_3_2": "2.3.2 How AI improved work quality",
    "q2_3_4": "2.3.4 What would have happened without AI",
    "q2_4": "2.4 Effect of AI on reproducibility",
    "q2_5": "2.5 How AI output quality is verified",
    "q3_1": "3.1 Use GitHub for version control?",
    "q3_2": "3.2 Use GitHub Copilot as a coding agent?",
    "q3_3": "3.3 Safe-use knowledge check (confidential data + AI)",
    "q4_2": "4.2 Years at the World Bank",
    "q4_3": "4.3 What attendees want from the Bootcamp",
    "q4_4": "4.4 Taken an AI-for-research course before?",
    "q4_5": "4.5 Self-rated AI-for-research knowledge",
}

# Manual short category labels, used in place of the full XLSForm/do-file
# choice text where that text is long enough to overlap on a bar chart.
# Keyed by column name (lowercase, dedup-suffix stripped) -> {code: short text}.
CATEGORY_OVERRIDES = {
    "q1_1": {"1": "Yes", "2": "Personal use only, not for work", "3": "Do not use at all"},
    "q1_7": {"1": "Clear disclosure with details", "2": "Mentioned AI use, no details",
             "3": "Wanted to disclose, unsure how", "4": "Preferred not to disclose", "97": "Other"},
    "q2_1": {"1": "Yes", "2": "Know about it, never created one", "3": "Don't know what it is"},
    "q2_2": {"1": "Yes", "2": "Know about it, never used one", "3": "Don't know what it is"},
    "q2_3_4": {"1": "Done later (after learning how)", "2": "Done by another staff/ET",
               "3": "Done by another ST", "4": "Done by a third party", "5": "Not done at all"},
    "q2_4": {"1": "More reproducible", "2": "No change", "3": "Less reproducible",
             "4": "Not sure", "5": "Don't do analytical work"},
    "q3_1": {"1": "Yes, active repos", "2": "Used GitHub in the past", "3": "Familiar, but don't use it",
             "4": "Not familiar with GitHub", "5": "N/A – no analytical work"},
    "q3_2": {"1": "Active WBG Copilot user", "2": "Have WBG license, exploring",
             "3": "Used personally, not via WBG", "4": "Heard of it, never used", "5": "What is GitHub Copilot?"},
    "q3_3": {"1": "Personal account + de-identified data", "2": "mAI / M365 Copilot (cleared for Confidential)",
             "3": "Synthetic data + local scripts", "4": "Don't use AI with confidential data", "5": "Not sure"},
}


def get_var_label(col: str, var_labels: dict) -> str | None:
    for key in (col.lower(), strip_dedup_suffix(col).lower()):
        if key in TITLE_OVERRIDES:
            return TITLE_OVERRIDES[key]
    for key in (col.lower(), strip_dedup_suffix(col).lower()):
        if key in var_labels:
            return var_labels[key]
    return None


def get_value_label_map(col: str, value_labels: dict) -> dict | None:
    for key in (col.lower(), strip_dedup_suffix(col).lower()):
        if key in value_labels:
            return value_labels[key]
    return None


def get_display_choice_map(col: str, value_labels: dict, question_to_list: dict = None,
                            list_to_choices: dict = None) -> dict | None:
    """Combine, in priority order, manual short overrides > full XLSForm
    choice text > (possibly truncated) Stata value labels, for display."""
    base = strip_dedup_suffix(col).lower()
    combined = dict(get_value_label_map(col, value_labels) or {})

    if question_to_list and list_to_choices:
        list_name = question_to_list.get(base)
        if list_name:
            combined.update(list_to_choices.get(list_name, {}))

    combined.update(CATEGORY_OVERRIDES.get(base, {}))
    return combined or None


def short_label(label: str, width: int = 70) -> str:
    if label is None:
        return ""
    return label if len(label) <= width else label[: width - 1].rstrip() + "…"


def wrapped(label: str, width: int) -> str:
    return "\n".join(textwrap.wrap(label, width=width)) if label else ""


# --------------------------------------------------------------------------
# Multi-select parent/child detection
# --------------------------------------------------------------------------

def is_binary_series(s: pd.Series) -> bool:
    vals = set(s.dropna().unique())
    return len(vals) > 0 and vals.issubset({0, 1, 0.0, 1.0})


def find_multiselect_groups(df: pd.DataFrame, var_labels: dict):
    """Detect select-multiple question groups: a parent string column (raw
    space-separated codes) plus binary 0/1 child columns named parent_<code>.

    Returns: {parent_col: [(child_col, option_code), ...]}, and the set of
    all consumed child column names.
    """
    groups = {}
    consumed = set()

    for col in df.columns:
        if not (df[col].dtype == object or pd.api.types.is_string_dtype(df[col])):
            continue
        base = strip_dedup_suffix(col)
        pattern = re.compile(rf"^{re.escape(base)}_(\d{{1,3}}|97)$")
        children = [c for c in df.columns if pattern.match(c)]
        bin_children = [c for c in children if is_binary_series(df[c])]
        if bin_children:
            ordered = sorted(
                bin_children,
                key=lambda c: (c.endswith("_97"), int(pattern.match(c).group(1))),
            )
            groups[col] = [(c, pattern.match(c).group(1)) for c in ordered]
            consumed.update(bin_children)

    return groups, consumed


# Manual short-label overrides for specific multi-select questions, used in
# place of the full XLSForm choice text when that text is too long to read
# comfortably on a bar chart. Keyed by parent question name (lowercase).
SHORT_LABEL_OVERRIDES = {
    "q1_5": {
        "1": "Administrative",
        "2": "Email",
        "3": "Documents",
        "4": "Background Research",
        "5": "Research Design",
        "6": "Surveys",
        "7": "Data Analysis & Visualization",
        "8": "Dashboard / Web App",
        "9": "Reproducibility Package",
        "10": "Presentation",
        "11": "Comms Materials",
        "12": "Recruitment",
        "97": "Other",
    },
    "q1_2": {
        "1": "Can't help with my job",
        "2": "Unsure how to use it",
        "3": "No time to learn new tools",
        "4": "Preferred tools not WBG-approved",
        "5": "Unsure if WBG allows it",
        "6": "Pressure from coworkers not to",
        "7": "Ethical concerns",
        "8": "Skeptical of AI output quality",
        "9": "Worried it could replace my job",
        "10": "Worried it dilutes my creativity",
        "11": "No time to use it",
        "97": "Other",
    },
    "q1_3": {
        "1": "mAI",
        "2": "Third-party chat tool (ChatGPT, etc.)",
        "3": "MS Copilot (Word/Excel/PPT)",
        "4": "Copilot Cowork",
        "5": "Coding agent (Copilot, Codex, etc.)",
        "6": "Notebook LM",
        "7": "Image generation tool (DALL-E, etc.)",
        "8": "Vibecoding tool (Replit, etc.)",
        "9": "AI API in MEGA",
        "97": "Other",
    },
    "q2_3": {
        "1": "Spend less time on analysis",
        "2": "Rely less on STs",
        "3": "Rely less on staff/ET",
        "4": "Produce more outputs",
        "5": "Produce higher-quality outputs",
        "6": "Do more in-depth work",
        "7": "No significant change",
        "97": "Other",
    },
    "q2_3_2": {
        "1": "More confident in my work",
        "2": "More polished, ready to share",
        "3": "Fewer mistakes",
        "4": "Get better feedback from colleagues",
        "97": "Other",
    },
    "q2_5": {
        "1": "Manually review all outputs",
        "2": "Spot-check a sample",
        "3": "Peer review by colleague",
        "4": "Automated tests/QA checks",
        "5": "Compare to known benchmark",
        "6": "Only verify if result seems off",
        "7": "Multi-agent cross-verification",
        "8": "N/A – don't need verification",
        "97": "Other",
    },
    "q4_3": {
        "1": "Improve quality of my work",
        "2": "Increase my productivity",
        "3": "Build internal relationships",
        "4": "Increase innovation",
        "6": "Apply new tools to my job",
        "7": "Career growth",
        "8": "Deepen core-topic knowledge",
        "9": "Improve technical skills",
        "97": "Other",
    },
}


def item_label_for_option(parent_base: str, code: str, var_labels: dict,
                           question_to_list: dict = None, list_to_choices: dict = None) -> str:
    override = SHORT_LABEL_OVERRIDES.get(parent_base.lower(), {}).get(code)
    if override:
        return override

    if question_to_list and list_to_choices:
        list_name = question_to_list.get(parent_base.lower())
        if list_name:
            label = list_to_choices.get(list_name, {}).get(code)
            if label:
                return label

    if code == "97":
        return "Other (please specify)"

    sibling = f"{parent_base}_use_{code}"
    label = var_labels.get(sibling.lower())
    return label if label else f"Option {code}"


USEFULNESS_GROUP_RE = re.compile(r"^(.+)_use_(\d{1,3}|97)$")


def find_usefulness_groups(df: pd.DataFrame):
    """Detect per-item Likert "usefulness" groups: a family of single-select
    columns named <base>_use_<code>, one per item in a related multi-select
    question (e.g. q1_5_use_1 .. q1_5_use_12, q1_5_use_97 rating usefulness
    of each q1_5 task).

    Returns {base: [(col, code), ...]} ordered by code (97 last).
    """
    groups = {}
    for col in df.columns:
        m = USEFULNESS_GROUP_RE.match(col)
        if m:
            base, code = m.groups()
            groups.setdefault(base, []).append((col, code))

    for base, items in groups.items():
        items.sort(key=lambda t: (t[1] == "97", int(t[1])))

    return groups


# --------------------------------------------------------------------------
# Classification
# --------------------------------------------------------------------------

def classify_columns(df: pd.DataFrame, var_labels: dict, value_labels: dict, consumed_children: set, multiselect_parents: set):
    continuous, categorical_single, excluded = [], [], []

    for col in df.columns:
        if col in consumed_children:
            continue

        base_lower = strip_dedup_suffix(col).lower()
        series = df[col]
        n_non_missing = series.notna().sum()

        if col in multiselect_parents:
            # Already summarized by its own "select all that apply" chart.
            continue

        if base_lower in KNOWN_ID_COLUMNS:
            excluded.append((col, get_var_label(col, var_labels), "survey metadata/identifier"))
            continue

        if base_lower.endswith("_other"):
            excluded.append((col, get_var_label(col, var_labels), "free text (specify-other field)"))
            continue

        if n_non_missing == 0:
            excluded.append((col, get_var_label(col, var_labels), "entirely missing"))
            continue

        nunique = series.nunique(dropna=True)
        value_map = get_value_label_map(col, value_labels)

        if value_map is not None:
            categorical_single.append(col)
            continue

        if nunique / n_non_missing > ID_UNIQUE_RATIO and nunique > MAX_CATEGORIES_TO_PLOT:
            excluded.append((col, get_var_label(col, var_labels), "appears to be a unique identifier"))
            continue

        if pd.api.types.is_numeric_dtype(series):
            if nunique > CONTINUOUS_CARDINALITY_THRESHOLD:
                continuous.append(col)
            else:
                categorical_single.append(col)
        else:
            if nunique > MAX_CATEGORIES_TO_PLOT:
                excluded.append((col, get_var_label(col, var_labels), f"free text / too many distinct values ({nunique})"))
            else:
                categorical_single.append(col)

    return continuous, categorical_single, excluded


# --------------------------------------------------------------------------
# Stats / charts
# --------------------------------------------------------------------------

def continuous_stats_table(df: pd.DataFrame, columns: list, var_labels: dict) -> pd.DataFrame:
    if not columns:
        return pd.DataFrame(columns=["Variable", "N", "Missing", "Mean", "Median", "Std Dev", "Min", "Max"])
    rows = []
    for col in columns:
        s = df[col]
        label = get_var_label(col, var_labels)
        rows.append({
            "Variable": f"{col} — {short_label(label, 55)}" if label else col,
            "N": int(s.notna().sum()),
            "Missing": int(s.isna().sum()),
            "Mean": s.mean(),
            "Median": s.median(),
            "Std Dev": s.std(),
            "Min": s.min(),
            "Max": s.max(),
        })
    stats = pd.DataFrame(rows)
    for c in ["Mean", "Median", "Std Dev", "Min", "Max"]:
        stats[c] = stats[c].round(2)
    return stats


# Shades of blue, cycled across bars within a single chart so categories
# are still distinguishable without leaving the site's blue theme.
QUALITATIVE_PALETTE = ["#08306b", "#2171b5", "#4292c6", "#6baed6", "#9ecae1", "#c6dbef", "#deebf7", "#f7fbff"]


def render_bar_chart(label_counts: list, title: str, n_total: int, horizontal: bool = False) -> str:
    labels = [lc[0] for lc in label_counts]
    values = [lc[1] for lc in label_counts]
    pcts = [v / n_total * 100 if n_total else 0 for v in values]
    max_pct = max(pcts) if pcts else 1
    colors = [QUALITATIVE_PALETTE[i % len(QUALITATIVE_PALETTE)] for i in range(len(labels))]

    if horizontal:
        fig_h = max(2.5, 0.5 * len(labels) + 1)
        fig, ax = plt.subplots(figsize=(7, fig_h), dpi=130)
        wrapped_labels = [wrapped(l, 32) for l in labels]
        ax.grid(axis="x", color="#e5e5e5", linewidth=0.7, zorder=0)
        bars = ax.barh(wrapped_labels, pcts, color=colors, edgecolor="none", zorder=3)
        ax.invert_yaxis()
        ax.set_xlabel("% of respondents")
        ax.set_xlim(0, max_pct * 1.18)
        for bar, pct in zip(bars, pcts):
            ax.text(bar.get_width() + max_pct * 0.02, bar.get_y() + bar.get_height() / 2,
                    f"{pct:.0f}%", va="center", fontsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_axisbelow(True)
        ax.set_title(wrapped(title, 60), fontsize=10.5, fontweight="bold")
        fig.subplots_adjust(left=0.42, right=0.95, top=0.85 if title.count("\n") < 2 else 0.8, bottom=0.12)
    else:
        # Scale height to category count so a 2-option chart doesn't render
        # as a mostly-empty tall rectangle next to denser ones in the grid.
        fig_h = max(2.4, min(3.8, 0.5 * len(labels) + 1.8))
        fig, ax = plt.subplots(figsize=(6, fig_h), dpi=130)
        wrapped_labels = [wrapped(l, 18) for l in labels]
        ax.grid(axis="y", color="#e5e5e5", linewidth=0.7, zorder=0)
        bars = ax.bar(wrapped_labels, pcts, color=colors, edgecolor="none", zorder=3)
        ax.set_title(wrapped(title, 55), fontsize=10.5, fontweight="bold")
        ax.set_ylabel("% of respondents")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_axisbelow(True)
        ax.set_ylim(0, max_pct * 1.18)
        for bar, pct in zip(bars, pcts):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max_pct * 0.02,
                    f"{pct:.0f}%", ha="center", va="bottom", fontsize=8)
        plt.xticks(rotation=35, ha="right", fontsize=8)
        fig.subplots_adjust(bottom=0.32, top=0.82, left=0.14, right=0.97)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def chart_for_single_select(df: pd.DataFrame, col: str, var_labels: dict, value_labels: dict,
                             question_to_list: dict = None, list_to_choices: dict = None) -> tuple:
    series = df[col]
    value_map = get_display_choice_map(col, value_labels, question_to_list, list_to_choices)
    counts = series.value_counts(dropna=True)

    def code_to_label(code):
        if value_map:
            key = str(int(code)) if float(code).is_integer() else str(code)
            if key in value_map:
                return value_map[key]
        return str(code)

    # Preserve the response scale's own order (1, 2, 3, ... with "Other"/97
    # last) rather than sorting by frequency, so ordinal/Likert questions
    # (e.g. poor -> excellent) read left-to-right the way they were asked.
    def sort_key(c):
        try:
            return (0, int(c))
        except (TypeError, ValueError):
            return (1, str(c))

    ordered_codes = sorted(counts.index, key=sort_key)
    label_counts = [(code_to_label(c), int(counts[c])) for c in ordered_codes]
    n_total = int(series.notna().sum())

    title = get_var_label(col, var_labels) or col
    img = render_bar_chart(label_counts, title, n_total, horizontal=False)
    return img, title


def chart_for_multiselect(df: pd.DataFrame, parent_col: str, children: list, var_labels: dict,
                           question_to_list: dict = None, list_to_choices: dict = None) -> tuple:
    parent_base = strip_dedup_suffix(parent_col)
    n_respondents = int(df[parent_col].notna().sum())

    label_counts = []
    for child_col, code in children:
        count = int(df[child_col].fillna(0).sum())
        if count == 0:
            continue
        item_label = item_label_for_option(parent_base, code, var_labels, question_to_list, list_to_choices)
        label_counts.append((item_label, count))
    label_counts.sort(key=lambda lc: lc[1], reverse=True)

    title = get_var_label(parent_col, var_labels) or parent_col
    img = render_bar_chart(label_counts, title, n_respondents, horizontal=True)
    return img, title, n_respondents


# Sequential palette, light (low usefulness) to dark (high usefulness).
USEFULNESS_COLORS = ["#c6dbef", "#9ecae1", "#4292c6", "#084594"]


def text_color_for_bg(hex_color: str) -> str:
    """White text on dark backgrounds, near-black text on light ones, by
    relative luminance, so segment-value labels stay readable either way."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return "#ffffff" if luminance < 140 else "#1a1a1a"


def render_stacked_bar_chart(rows: list, category_labels: list, title: str) -> str:
    """rows: [(item_label, {category_label: proportion}, n), ...]"""
    fig_h = max(2.5, 0.55 * len(rows) + 1.0)
    fig, ax = plt.subplots(figsize=(8, fig_h), dpi=130)

    wrapped_labels = [wrapped(f"{label} (n={n})", 26) for label, _, n in rows]
    y_pos = range(len(rows))
    colors = USEFULNESS_COLORS[: len(category_labels)]
    text_colors = [text_color_for_bg(c) for c in colors]

    ax.grid(axis="x", color="#e5e5e5", linewidth=0.7, zorder=0)
    for i, cat in enumerate(category_labels):
        widths = [r[1].get(cat, 0.0) * 100 for r in rows]
        lefts = [sum(r[1].get(c, 0.0) * 100 for c in category_labels[:i]) for r in rows]
        bars = ax.barh(list(y_pos), widths, left=lefts, color=colors[i], edgecolor="white",
                        linewidth=0.5, label=cat, height=0.65, zorder=3)
        for bar, w in zip(bars, widths):
            if w >= 8:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
                        f"{w:.0f}%", ha="center", va="center", fontsize=7.5, color=text_colors[i])

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(wrapped_labels, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("% of respondents who answered (no-response omitted)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)
    ax.set_title(wrapped(title, 70), fontsize=10.5, fontweight="bold")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=len(category_labels),
               fontsize=8, frameon=False)
    fig.subplots_adjust(left=0.3, right=0.96, top=0.9, bottom=0.14)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def chart_for_usefulness_group(df: pd.DataFrame, base: str, items: list, var_labels: dict, value_labels: dict,
                                question_to_list: dict = None, list_to_choices: dict = None) -> tuple:
    value_map = None
    for col, _ in items:
        value_map = get_value_label_map(col, value_labels)
        if value_map:
            break
    category_codes = sorted(value_map, key=int) if value_map else []
    category_labels = [value_map[c] for c in category_codes] if value_map else []

    rows = []
    for col, code in items:
        series = df[col]
        n = int(series.notna().sum())
        if n == 0:
            continue
        proportions = series.value_counts(normalize=True, dropna=True)
        prop_by_label = {}
        for cat_code, cat_label in zip(category_codes, category_labels):
            key = int(cat_code) if float(cat_code).is_integer() else cat_code
            prop_by_label[cat_label] = float(proportions.get(key, 0.0))
        item_label = item_label_for_option(base, code, var_labels, question_to_list, list_to_choices)
        rows.append((item_label, prop_by_label, n))

    # Drop any usefulness level nobody actually selected, across every task.
    category_labels = [cat for cat in category_labels if any(r[1].get(cat, 0.0) > 0 for r in rows)]

    title = "1.5 Usefulness of GenAI by task"
    img = render_stacked_bar_chart(rows, category_labels, title)
    return img, title


# --------------------------------------------------------------------------
# HTML assembly
# --------------------------------------------------------------------------

SECTION_RE = re.compile(r"^q(\d+)_", re.IGNORECASE)

MODULE_TITLES = {
    "1": "Current Use of Generative AI",
    "2": "AI Workflows, Impact & Verification",
    "3": "GitHub, Copilot & Safe AI Use",
    "4": "Background & Expectations",
}


def section_of(col: str) -> str:
    m = SECTION_RE.match(strip_dedup_suffix(col))
    return m.group(1) if m else "Other"


def module_heading(module_key: str) -> str:
    title = MODULE_TITLES.get(module_key)
    return f"Module {module_key}: {title}" if title else "Other"


def pct_of(series: pd.Series, value) -> tuple:
    """Return (pct, count, n_non_missing) of series == value, among non-missing."""
    s = series.dropna()
    n = len(s)
    if n == 0:
        return 0.0, 0, 0
    count = int((s == value).sum())
    return count / n * 100, count, n


def top_multiselect_items(df: pd.DataFrame, parent_col: str, children: list, var_labels: dict,
                           question_to_list: dict, list_to_choices: dict, n: int = 3) -> tuple:
    base = strip_dedup_suffix(parent_col)
    n_resp = int(df[parent_col].notna().sum())
    rows = []
    for child_col, code in children:
        label = item_label_for_option(base, code, var_labels, question_to_list, list_to_choices)
        count = int(df[child_col].fillna(0).sum())
        rows.append((count / n_resp * 100 if n_resp else 0.0, label))
    rows.sort(key=lambda r: r[0], reverse=True)
    return rows[:n], n_resp


def compute_key_messages(df: pd.DataFrame, var_labels: dict, multiselect_groups: dict,
                          question_to_list: dict, list_to_choices: dict) -> dict:
    """Return {module_key: [bullet strings]}, computed live from the data."""
    messages = {}

    # --- Module 1: current use of generative AI ---
    pct_use, _, n_use = pct_of(df["q1_1"], 1)
    top_tasks, n_tasks = top_multiselect_items(df, "q1_5", multiselect_groups["q1_5"], var_labels,
                                                question_to_list, list_to_choices, n=3)
    pct_included, _, n_included = pct_of(df["q1_6"], 1)
    pct_clear, _, n_disclose = pct_of(df["q1_7"], 1)
    messages["1"] = [
        f"{pct_use:.0f}% of respondents ({n_use} answered) currently use generative AI for their job.",
        "Most-used tasks: " + ", ".join(f"{label} ({pct:.0f}%)" for pct, label in top_tasks) + ".",
        f"{pct_included:.0f}% have had AI-assisted work included in a report, paper, or other output.",
        f"Of those, only {pct_clear:.0f}% gave a clear disclosure statement — most either omitted "
        f"details or wanted to disclose but weren't sure how.",
    ]

    # --- Module 2: AI workflows, impact & verification ---
    pct_memory_unknown, _, _ = pct_of(df["q2_1"], 3)
    pct_skills_unknown, _, _ = pct_of(df["q2_2"], 3)
    top_impact, _ = top_multiselect_items(df, "q2_3", multiselect_groups["q2_3"], var_labels,
                                           question_to_list, list_to_choices, n=1)
    top_verify, _ = top_multiselect_items(df, "q2_5", multiselect_groups["q2_5"], var_labels,
                                           question_to_list, list_to_choices, n=1)
    pct_repro_same, _, _ = pct_of(df["q2_4"], 2)
    pct_repro_more, _, _ = pct_of(df["q2_4"], 1)
    messages["2"] = [
        f"Half of respondents ({pct_memory_unknown:.0f}%) don't know what an AI memory file is, and a "
        f"similar share ({pct_skills_unknown:.0f}%) don't know what a reusable AI skill is.",
        f"{top_impact[0][1]} ({top_impact[0][0]:.0f}%) is the most widely reported effect of AI on "
        f"analytical work.",
        f"Nearly half ({pct_repro_same:.0f}%) see no change in reproducibility from using AI, and only "
        f"{pct_repro_more:.0f}% report it's improved.",
        f"{top_verify[0][1]} ({top_verify[0][0]:.0f}%) is the most common way respondents verify "
        f"AI-generated output.",
    ]

    # --- Module 3: GitHub, Copilot & safe AI use ---
    pct_no_github, _, _ = pct_of(df["q3_1"], 4)
    pct_active_copilot, cnt_active, n_copilot = pct_of(df["q3_2"], 1)
    pct_exploring_copilot, cnt_exploring, _ = pct_of(df["q3_2"], 2)
    pct_combined_copilot = (cnt_active + cnt_exploring) / n_copilot * 100 if n_copilot else 0.0
    pct_safeuse_2, _, _ = pct_of(df["q3_3"], 2)
    pct_safeuse_3, _, _ = pct_of(df["q3_3"], 3)
    pct_safeuse_unsure, _, _ = pct_of(df["q3_3"], 5)
    messages["3"] = [
        f"{pct_no_github:.0f}% of respondents are not familiar with GitHub at all.",
        f"Only {pct_combined_copilot:.0f}% have a WBG GitHub Copilot license (active or exploring); "
        f"most have either never used it or never heard of it.",
        f"On the safe-use knowledge check, responses split almost evenly between two approaches "
        f"({pct_safeuse_2:.0f}% and {pct_safeuse_3:.0f}%), with {pct_safeuse_unsure:.0f}% unsure — "
        f"no one chose the two most restrictive options.",
    ]

    # --- Module 4: background & expectations ---
    pct_5_9, _, _ = pct_of(df["q4_2"], 3)
    pct_10_19, _, _ = pct_of(df["q4_2"], 4)
    top_expect, _ = top_multiselect_items(df, "q4_3", multiselect_groups["q4_3"], var_labels,
                                           question_to_list, list_to_choices, n=3)
    pct_no_course, _, _ = pct_of(df["q4_4"], 2)
    pct_poor, cnt_poor, n_knowledge = pct_of(df["q4_5"], 1)
    pct_very_poor, cnt_very_poor, _ = pct_of(df["q4_5"], 2)
    pct_low_knowledge = (cnt_poor + cnt_very_poor) / n_knowledge * 100 if n_knowledge else 0.0
    messages["4"] = [
        f"Tenure is concentrated in the middle: {pct_5_9:.0f}% have 5–9 years at the WBG and another "
        f"{pct_10_19:.0f}% have 10–19 years.",
        "Top expectations for the Bootcamp: " + ", ".join(f"{label} ({pct:.0f}%)" for pct, label in top_expect) + ".",
        f"{pct_no_course:.0f}% have not taken an AI-for-research course before.",
        f"{pct_low_knowledge:.0f}% rate their current AI-for-research knowledge as poor or very poor.",
    ]

    return messages


def build_html(df, single_charts, multiselect_groups, usefulness_groups, var_labels, value_labels,
               source_name, question_to_list=None, list_to_choices=None, key_messages=None) -> str:
    key_messages = key_messages or {}

    # Build (section, title_sort_key, html_snippet) for every chart so we can
    # group them under question-section headers in question order.
    cards = []  # (section, sort_key, html)

    for col in single_charts:
        img_b64, title = chart_for_single_select(df, col, var_labels, value_labels, question_to_list, list_to_choices)
        n = int(df[col].notna().sum())
        missing = int(df[col].isna().sum())
        html = f"""
        <div class="chart-card">
          <img src="data:image/png;base64,{img_b64}" alt="Bar chart of {col}">
          <div class="chart-meta">{col} &middot; N = {n}, Missing = {missing}</div>
        </div>
        """
        cards.append((section_of(col), title, html))

    for parent_col, children in multiselect_groups.items():
        img_b64, title, n = chart_for_multiselect(df, parent_col, children, var_labels, question_to_list, list_to_choices)
        html = f"""
        <div class="chart-card chart-card-wide">
          <img src="data:image/png;base64,{img_b64}" alt="Bar chart of {parent_col}">
          <div class="chart-meta">{parent_col} &middot; Select all that apply &middot; N = {n}</div>
        </div>
        """
        cards.append((section_of(parent_col), title, html))

    for base, items in usefulness_groups.items():
        img_b64, title = chart_for_usefulness_group(df, base, items, var_labels, value_labels, question_to_list, list_to_choices)
        html = f"""
        <div class="chart-card chart-card-wide">
          <img src="data:image/png;base64,{img_b64}" alt="Stacked bar chart of {base} usefulness">
          <div class="chart-meta">{base}_use_* &middot; Usefulness rating per item, no-response omitted</div>
        </div>
        """
        cards.append((section_of(base), title, html))

    cards.sort(key=lambda c: (c[0], c[1]))

    module_order = sorted({c[0] for c in cards}, key=lambda s: (s == "Other", s))
    nav_html = "".join(
        f'<a href="#module-{m}">{module_heading(m)}</a>' for m in module_order
    )

    sections_html = []
    current_section = None
    section_buffer = []
    for section, _, html in cards:
        if section != current_section:
            if section_buffer:
                sections_html.append(
                    f'<div class="grid">{"".join(section_buffer)}</div>'
                )
            bullets = key_messages.get(section)
            bullets_html = (
                '<ul class="key-messages">' + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"
                if bullets else ""
            )
            sections_html.append(f'<h2 id="module-{section}">{module_heading(section)}</h2>{bullets_html}')
            section_buffer = []
            current_section = section
        section_buffer.append(html)
    if section_buffer:
        sections_html.append(f'<div class="grid">{"".join(section_buffer)}</div>')

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Descriptive Statistics Report</title>
<style>
  body {{
    font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
    margin: 0;
    padding: 2rem 3rem 4rem;
    background: #fafafa;
    color: #1a1a1a;
  }}
  h1 {{ font-size: 1.6rem; margin-bottom: 0.1rem; }}
  .subtitle {{ color: #666; margin-bottom: 1.25rem; font-size: 0.9rem; }}
  nav.module-nav {{
    position: sticky;
    top: 0;
    z-index: 10;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1rem;
    background: #fafafa;
    border-bottom: 1px solid #e0e0e0;
    padding: 0.75rem 0 1rem;
    margin-bottom: 1.5rem;
  }}
  nav.module-nav a {{
    color: #4C72B0;
    font-size: 0.85rem;
    font-weight: 600;
    text-decoration: none;
    padding: 0.3rem 0.7rem;
    border: 1px solid #c9d8ec;
    border-radius: 999px;
    background: #fff;
  }}
  nav.module-nav a:hover {{ background: #eef3fa; }}
  h2 {{
    font-size: 1.2rem;
    margin-top: 2.5rem;
    border-bottom: 2px solid #4C72B0;
    padding-bottom: 0.3rem;
    scroll-margin-top: 4.5rem;
  }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 1.5rem;
    margin-top: 0.75rem;
    align-items: stretch;
  }}
  .chart-card {{
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 0.75rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .chart-card-wide {{ grid-column: 1 / -1; }}
  .chart-card img {{ max-width: 100%; height: auto; }}
  .chart-meta {{ font-size: 0.78rem; color: #777; margin-top: 0.3rem; }}
  .key-messages {{
    background: #eef3fa;
    border-left: 4px solid #4C72B0;
    border-radius: 0 6px 6px 0;
    margin: 0.75rem 0 1.25rem;
    padding: 0.9rem 1.2rem 0.9rem 1.5rem;
    font-size: 0.92rem;
    line-height: 1.5;
  }}
  .key-messages li {{ margin-bottom: 0.3rem; }}
</style>
</head>
<body>
  <h1>AI Bootcamp Baseline Survey: Descriptive Statistics</h1>
  <div class="subtitle">{len(df)} respondents &middot; {source_name} &middot; labels from import_ai_bootcamp_pre_survey.do and the XLSForm choices list</div>
  <nav class="module-nav">{nav_html}</nav>

  {''.join(sections_html) if cards else "<p>No categorical variables were detected.</p>"}
</body>
</html>
"""
    return html


def main():
    base_dir = Path(__file__).resolve().parent.parent
    default_input = base_dir / "data" / "AI Bootcamp Baseline Survey_WIDE.csv"
    default_do = base_dir / "code" / "import_ai_bootcamp_pre_survey.do"
    default_xlsform = base_dir / "documentation" / "AI_Bootcamp_Baseline_XLSForm_v2.xlsx"
    default_output = base_dir / "outputs" / "descriptive_stats.html"

    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_input
    do_path = Path(sys.argv[2]) if len(sys.argv) > 2 else default_do
    xlsform_path = Path(sys.argv[3]) if len(sys.argv) > 3 else default_xlsform
    output_path = Path(sys.argv[4]) if len(sys.argv) > 4 else default_output

    df = pd.read_csv(input_path)
    var_labels, value_labels = parse_do_file(do_path)
    question_to_list, list_to_choices = parse_xlsform(xlsform_path)

    multiselect_groups, consumed_children = find_multiselect_groups(df, var_labels)
    usefulness_groups = find_usefulness_groups(df)
    for items in usefulness_groups.values():
        consumed_children.update(col for col, _ in items)

    all_multiselect_parents = set(multiselect_groups.keys())
    low_n_dropped = [p for p in multiselect_groups if int(df[p].notna().sum()) < MIN_N_FOR_CHART]
    for parent in low_n_dropped:
        del multiselect_groups[parent]

    # Still treat dropped parents as "handled" so their raw multi-code string
    # column doesn't fall through and get picked up as its own bogus chart.
    continuous, single_charts, excluded = classify_columns(
        df, var_labels, value_labels, consumed_children, all_multiselect_parents
    )

    key_messages = compute_key_messages(df, var_labels, multiselect_groups, question_to_list, list_to_choices)

    html = build_html(
        df, single_charts, multiselect_groups, usefulness_groups, var_labels, value_labels,
        input_path.name, question_to_list, list_to_choices, key_messages,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    print(f"Single-select categorical charts: {len(single_charts)}")
    print(f"Select-all-that-apply charts: {len(multiselect_groups)} (dropped for low N: {low_n_dropped or 'none'})")
    print(f"Stacked usefulness charts: {len(usefulness_groups)}")
    print(f"Continuous variables (not rendered): {len(continuous)}")
    print(f"Excluded columns (not rendered): {len(excluded)}")
    print(f"Report written to: {output_path}")


if __name__ == "__main__":
    main()
