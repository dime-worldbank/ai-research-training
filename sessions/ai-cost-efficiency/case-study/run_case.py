"""Run the three Cash Plus workflows with the Claude CLI and record token usage per task."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# The test projects must live outside this folder and outside any git repo: Claude Code also loads
# CLAUDE.md files from parent folders, and here::here() would resolve to the repo root.
here = Path(__file__).parent
runs = Path(tempfile.gettempdir()) / "cashplus-case-study"
results_dir = here / "results"

VAGUE = [
    "The balance table isn't working. Can you fix it?",
    "Can you proofread the abstract?",
    "Write a README for this project.",
]
SPECIFIC = [
    "code/02_balance.R fails with: invalid type (NULL) for variable 'hh[[v]]'. Check every "
    "variable name in that file against the columns in data/raw/baseline_hh.csv (see CLAUDE.md) "
    "and fix them. Only edit 02_balance.R.",
    "Proofread paper/abstract.md: fix typos and grammar only, don't change the content. "
    "Edit the file directly, then list the changes in one line.",
    "Replace README.md with a short README: a one-paragraph summary, the folder structure, and "
    "how to run the code (code/00_main.R). Use CLAUDE.md for the details; don't read docs/.",
]

TASKS = ["Fix the balance table", "Proofread the abstract", "Write a README"]

SCENARIOS = {
    # name: (one_session, memory_file, prompts, models per task)
    "A_one_chat": (True, False, VAGUE, ["opus", "opus", "opus"]),
    "B_new_sessions": (False, False, VAGUE, ["opus", "opus", "opus"]),
    "C_all_habits": (False, True, SPECIFIC, ["sonnet", "haiku", "haiku"]),
}
DESCRIPTIONS = {
    "A_one_chat": "A: one chat for all three tasks, Opus, vague prompts, no memory file",
    "B_new_sessions": "B: a new session per task, otherwise the same as A",
    "C_all_habits": "C: new sessions + memory file + specific prompts + smallest model that works",
}

def claude(cwd, prompt, model, resume=None):
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--model", model,
           "--setting-sources", "project", "--strict-mcp-config",
           "--permission-mode", "acceptEdits",
           "--allowedTools", "Read", "Edit", "Write", "Glob", "Grep"]
    if resume:
        cmd += ["--resume", resume]
    out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)
    return json.loads(out.stdout)

def tokens(res):
    mu = res.get("modelUsage") or {}
    if mu:
        inp = sum(m.get("inputTokens", 0) + m.get("cacheReadInputTokens", 0)
                  + m.get("cacheCreationInputTokens", 0) for m in mu.values())
        outp = sum(m.get("outputTokens", 0) for m in mu.values())
    else:
        u = res["usage"]
        inp = u["input_tokens"] + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
        outp = u["output_tokens"]
    return inp, outp

# Known typos planted in paper/abstract.md (with surrounding text so corrected words don't match).
TYPOS = [" combine ", "househods", "program increase ", "wich", "component matter ", "food are "]
SAVED_FILES = ["code/02_balance.R", "paper/abstract.md", "README.md", "output/balance_table.csv"]

def balance_table_runs(proj):
    """True if the fixed 02_balance.R now runs and writes the balance table."""
    if not shutil.which("Rscript"):
        return None
    code = 'source("code/01_clean.R"); source("code/02_balance.R")'
    ok = subprocess.run(["Rscript", "-e", code], cwd=proj, capture_output=True).returncode == 0
    return ok and (proj / "output" / "balance_table.csv").exists()

def check(proj):
    """Quality checks on what the agent produced, so the token numbers compare like with like."""
    abstract = (proj / "paper/abstract.md").read_text()
    readme = (proj / "README.md").read_text()
    total = sum(s.count(ty) for ty in TYPOS for s in [(source / "paper/abstract.md").read_text()])
    return {
        "balance_table_runs": balance_table_runs(proj),
        "typos_fixed": f"{total - sum(abstract.count(ty) for ty in TYPOS)} of {total}",
        "readme_lines": len(readme.splitlines()) if "TODO" not in readme else 0,
    }

def save_outputs(proj, name):
    """Copy what the agent produced, plus a diff against the starting project, to results/<name>/."""
    out = results_dir / name
    if out.exists():
        shutil.rmtree(out)
    for f in SAVED_FILES:
        if (proj / f).exists():
            (out / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(proj / f, out / f)
    diff = subprocess.run(["diff", "-ru", "-x", "data", "-x", "output", "-x", "CLAUDE.md", str(source), str(proj)],
                          capture_output=True, text=True).stdout
    (out / "changes.diff").write_text(diff.replace(str(source), "before").replace(str(proj), "after"))

def report(name, checks):
    runs_ok = {True: "yes", False: "NO", None: "not checked (no R)"}[checks["balance_table_runs"]]
    print(f"  Check: balance table runs: {runs_ok} | abstract typos fixed: {checks['typos_fixed']}"
          f" | README: {checks['readme_lines'] or 'not written'} lines")

# The starting project (with the broken balance table) that every workflow gets a fresh copy of.
source = here / "cashplus-project"

if __name__ == "__main__":
    if not source.exists():
        subprocess.run([sys.executable, "-I", str(here / "make_project.py"), str(source)], check=True)
    # --save-only: re-save outputs and checks from the last run without calling Claude again.
    save_only = "--save-only" in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith("--")] or list(SCENARIOS)

    print(f"Project: Cash Plus RCT ({source.name}/)")
    print("Tasks:   " + " | ".join(f"{i}. {t}" for i, t in enumerate(TASKS, 1)))

    results = {}
    for name in names:
        one_session, memory, prompts, models = SCENARIOS[name]
        proj = runs / name
        print(f"\n{DESCRIPTIONS[name]}")
        if save_only:
            rows = json.loads((results_dir / f"{name}.json").read_text())["tasks"]
        else:
            if proj.exists():
                shutil.rmtree(proj)
            shutil.copytree(source, proj)
            if memory:
                shutil.copy(here / "memory_file.md", proj / "CLAUDE.md")
            sid = None
            rows = []
            for i, (p, m) in enumerate(zip(prompts, models), 1):
                print(f"  {i}. {TASKS[i-1]:<24} [{m}] ...", end="", flush=True)
                res = claude(proj, p, m, resume=sid if one_session else None)
                if one_session:
                    sid = res["session_id"]
                inp, outp = tokens(res)
                rows.append({"task": i, "model": m, "turns": res.get("num_turns"),
                             "input_tokens": inp, "output_tokens": outp,
                             "cost_usd": res.get("total_cost_usd"), "reply": res.get("result", "")})
                print(f"\r  {i}. {TASKS[i-1]:<24} [{m}] {inp:>9,} tokens in  {outp:>6,} out", flush=True)
        if save_only:
            for r in rows:
                print(f"  {r['task']}. {TASKS[r['task']-1]:<24} [{r['model']}] {r['input_tokens']:>9,} tokens in  {r['output_tokens']:>6,} out")
        checks = check(proj)
        report(name, checks)
        results_dir.mkdir(exist_ok=True)
        save_outputs(proj, name)
        (results_dir / f"{name}.json").write_text(json.dumps({"checks": checks, "tasks": rows}, indent=2))
        results[name] = rows

    print("\nInput tokens per task")
    print(f"  {'':<24}" + "".join(f"{n.split('_')[0]:>12}" for n in results))
    for i, task in enumerate(TASKS):
        print(f"  {task:<24}" + "".join(f"{results[n][i]['input_tokens']:>12,}" for n in results))
    totals = {n: sum(r["input_tokens"] for r in results[n]) for n in results}
    costs = {n: sum(r["cost_usd"] or 0 for r in results[n]) for n in results}
    print(f"  {'Total':<24}" + "".join(f"{totals[n]:>12,}" for n in results))
    print(f"  {'Cost (API list prices)':<24}" + "".join(f"{'$' + format(costs[n], '.2f'):>12}" for n in results))
    if "A_one_chat" in results and "C_all_habits" in results:
        print(f"\nC used {totals['C_all_habits'] / totals['A_one_chat']:.0%} of A's tokens"
              f" and cost {costs['A_one_chat'] / costs['C_all_habits']:.0f}x less.")
    if "A_one_chat" in results and "B_new_sessions" in results:
        a2, b2 = results["A_one_chat"][1]["input_tokens"], results["B_new_sessions"][1]["input_tokens"]
        print(f"Same proofreading prompt: {a2:,} tokens in a long chat vs {b2:,} in a new session ({a2 / b2:.1f}x).")
    print(f"\nWhat each workflow produced (code, abstract, README, diff): {results_dir}/<workflow>/")
