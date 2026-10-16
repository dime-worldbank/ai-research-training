#!/usr/bin/env bash
#
# Validate and render the session decks listed in sessions-to-render-index-file.yml.
#
# 1. Checks that every listed .qmd exists and that its YAML front matter sets
#    `embed-resources: true` and `output-file: index.html`. If any check fails,
#    all problems are reported and nothing is rendered.
# 2. Renders each .qmd with `quarto render` so that index.html is written to
#    the same folder as the source .qmd.
#
# Usage (from anywhere in the repo):
#   macOS:   bash bootcamp/sessions/render-index-files.sh
#   Windows: same command, run in Git Bash (or the VS Code Git Bash terminal)
#
# Written for bash 3.2 (macOS default) and POSIX awk/grep, so it also runs in Git Bash.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIST_FILE="$SCRIPT_DIR/sessions-to-render-index-file.yml"
REL_SESSIONS="bootcamp/sessions"

if [ ! -f "$LIST_FILE" ]; then
  echo "ERROR: session list not found: $LIST_FILE" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Parse the session list: "day-N:" headers followed by "  - path/to/file.qmd"
# Emits one "day<TAB>path" line per entry.
# ---------------------------------------------------------------------------
ENTRIES=()
while IFS= read -r line; do
  ENTRIES+=("$line")
done < <(
  tr -d '\r' < "$LIST_FILE" | awk '
    /^[[:space:]]*#/ || /^[[:space:]]*$/ { next }
    /^[A-Za-z0-9_-]+:/ { day = $0; sub(/:.*/, "", day); next }
    /^[[:space:]]*-[[:space:]]*/ {
      path = $0
      sub(/^[[:space:]]*-[[:space:]]*/, "", path)
      sub(/[[:space:]]+#.*$/, "", path)
      sub(/[[:space:]]+$/, "", path)
      gsub(/^["\x27]|["\x27]$/, "", path)
      if (day == "") { print "NODAY\t" path } else { print day "\t" path }
    }
  '
)

if [ "${#ENTRIES[@]}" -eq 0 ]; then
  echo "ERROR: no sessions found in $LIST_FILE" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Front matter helpers
# ---------------------------------------------------------------------------

# Print the YAML front matter (between the opening --- on line 1 and the next ---).
front_matter() {
  tr -d '\r' < "$1" | awk '
    NR == 1 { if ($0 ~ /^---[[:space:]]*$/) { inside = 1; next } else { exit } }
    inside && /^---[[:space:]]*$/ { exit }
    inside { print }
  '
}

# Print the normalized value of KEY in front matter text, or nothing if absent.
fm_value() {
  local fm="$1" key="$2" raw
  raw="$(printf '%s\n' "$fm" | grep -E "^[[:space:]]*${key}:" | head -n 1 || true)"
  [ -z "$raw" ] && return 0
  printf '%s\n' "$raw" | awk -v key="$key" '{
    v = $0
    sub("^[[:space:]]*" key ":[[:space:]]*", "", v)
    sub(/[[:space:]]+#.*$/, "", v)
    sub(/[[:space:]]+$/, "", v)
    gsub(/^["\x27]|["\x27]$/, "", v)
    printf "%s", (v == "" ? "<empty>" : v)
  }'
}

# ---------------------------------------------------------------------------
# Validate all entries before rendering anything
# ---------------------------------------------------------------------------
MISSING_ERRORS=()
FM_ERRORS=()
FILES=()

for entry in "${ENTRIES[@]}"; do
  day="${entry%%$'\t'*}"
  rel="${entry#*$'\t'}"

  if [ "$day" = "NODAY" ]; then
    MISSING_ERRORS+=("'$rel' is not listed under a day-N: heading in $(basename "$LIST_FILE")")
    continue
  fi

  file="$SCRIPT_DIR/$day/$rel"
  shown="$REL_SESSIONS/$day/$rel"

  if [ ! -f "$file" ]; then
    MISSING_ERRORS+=("$day: $rel -> not found (looked for $shown)")
    continue
  fi

  fm="$(front_matter "$file")"
  if [ -z "$fm" ]; then
    FM_ERRORS+=("$shown: no YAML front matter found (file must start with ---)")
    continue
  fi

  for check in "embed-resources=true" "output-file=index.html"; do
    key="${check%%=*}"
    expected="${check#*=}"
    value="$(fm_value "$fm" "$key")"
    if [ -z "$value" ]; then
      FM_ERRORS+=("$shown: missing '$key' (expected '$key: $expected')")
    elif [ "$value" != "$expected" ]; then
      FM_ERRORS+=("$shown: '$key' is '$value' (expected '$expected')")
    fi
  done

  FILES+=("$file")
done

if [ "${#MISSING_ERRORS[@]}" -gt 0 ] || [ "${#FM_ERRORS[@]}" -gt 0 ]; then
  {
    echo "ERROR: validation failed for $(basename "$LIST_FILE"). Nothing was rendered."
    if [ "${#MISSING_ERRORS[@]}" -gt 0 ]; then
      echo ""
      echo "Files listed but not found in $REL_SESSIONS:"
      for e in "${MISSING_ERRORS[@]}"; do echo "  - $e"; done
    fi
    if [ "${#FM_ERRORS[@]}" -gt 0 ]; then
      echo ""
      echo "Front matter problems (need 'embed-resources: true' and 'output-file: index.html'):"
      for e in "${FM_ERRORS[@]}"; do echo "  - $e"; done
    fi
  } >&2
  exit 1
fi

echo "Validated ${#FILES[@]} session file(s)."

# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
if ! command -v quarto > /dev/null 2>&1; then
  echo "ERROR: 'quarto' not found on PATH. Install Quarto from https://quarto.org/docs/get-started/" >&2
  exit 1
fi

RENDERED=()
FAILED=()

for file in "${FILES[@]}"; do
  dir="$(dirname "$file")"
  name="$(basename "$file")"
  shown="${dir#"$SCRIPT_DIR"/}/$name"
  echo ""
  echo "==> Rendering $REL_SESSIONS/$shown"

  # Retry: on Windows, another process (editor, antivirus, sync client) can briefly
  # lock index.html while Quarto rewrites it ("user-mapped section open", os error 1224).
  ok=0
  for attempt in 1 2 3; do
    if (cd "$dir" && quarto render "$name") && [ -f "$dir/index.html" ]; then
      ok=1
      break
    fi
    [ "$attempt" -lt 3 ] && echo "    render failed (attempt $attempt of 3), retrying..." && sleep 2
  done

  if [ "$ok" -eq 1 ]; then
    RENDERED+=("$shown")
  else
    FAILED+=("$shown")
  fi
done

echo ""
echo "Rendered ${#RENDERED[@]} of ${#FILES[@]} file(s)."
if [ "${#FAILED[@]}" -gt 0 ]; then
  {
    echo "ERROR: these files failed to render (or no index.html was produced next to the .qmd):"
    for f in "${FAILED[@]}"; do echo "  - $REL_SESSIONS/$f"; done
  } >&2
  exit 1
fi
