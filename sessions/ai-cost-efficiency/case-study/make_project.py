"""Build a mock impact-evaluation project (fictional Cash Plus RCT) for the token case study."""
import csv
import random
import sys
from pathlib import Path

root = Path(sys.argv[1])
random.seed(42)

def w(path, text):
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)

# --- data -------------------------------------------------------------------
villages = [f"V{i:03d}" for i in range(1, 61)]
treated = set(random.sample(villages, 30))
rows = []
for i in range(1, 1201):
    v = random.choice(villages)
    rows.append({
        "hhid": f"HH{i:05d}",
        "village_id": v,
        "treatment": int(v in treated),
        "hh_size": random.randint(1, 11),
        "head_female": int(random.random() < 0.38),
        "head_age": random.randint(18, 80),
        "head_educ_yrs": random.randint(0, 14),
        "consumption_pc": round(random.lognormvariate(7.2, 0.6), 2),
        "food_insecure": int(random.random() < 0.46),
        "n_children_u5": random.randint(0, 4),
        "livestock_tlu": round(random.expovariate(1.2), 2),
        "dist_market_km": round(random.uniform(0.5, 25), 1),
    })
for name in ["baseline_hh.csv"]:
    p = root / "data/raw" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=rows[0].keys())
        wr.writeheader()
        wr.writerows(rows)
end = root / "data/raw/endline_hh.csv"
with end.open("w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["hhid", "consumption_pc_el", "food_insecure_el", "child_haz_el"])
    for r in rows:
        bump = 1.12 if r["treatment"] else 1.0
        wr.writerow([r["hhid"], round(r["consumption_pc"] * bump * random.uniform(0.85, 1.2), 2),
                     int(random.random() < (0.36 if r["treatment"] else 0.45)),
                     round(random.gauss(-1.4 + 0.15 * r["treatment"], 1.1), 2)])

# --- code -------------------------------------------------------------------
w("code/00_main.R", """# Main script: runs the full Cash Plus pipeline in order
# Set the project root before running
root <- here::here()
source(file.path(root, "code", "01_clean.R"))
source(file.path(root, "code", "02_balance.R"))
source(file.path(root, "code", "03_analysis.R"))
""")
w("code/01_clean.R", """# Clean baseline and endline household data
library(dplyr)
root <- here::here()
bl <- read.csv(file.path(root, "data", "raw", "baseline_hh.csv"))
el <- read.csv(file.path(root, "data", "raw", "endline_hh.csv"))

bl <- bl %>%
  mutate(log_cons = log(consumption_pc),
         large_hh = as.integer(hh_size >= 7))

hh <- left_join(bl, el, by = "hhid")
dir.create(file.path(root, "data", "clean"), showWarnings = FALSE, recursive = TRUE)
saveRDS(hh, file.path(root, "data", "clean", "hh_panel.rds"))
""")
w("code/02_balance.R", """# Balance table: baseline characteristics by treatment arm
library(dplyr)
root <- here::here()
hh <- readRDS(file.path(root, "data", "clean", "hh_panel.rds"))

balance_vars <- c("hh_size", "head_female", "head_age", "head_educ",
                  "consumption", "food_insecure", "n_children_u5",
                  "livestock_tlu", "dist_market_km")

balance <- lapply(balance_vars, function(v) {
  t <- t.test(hh[[v]] ~ hh$treat)
  data.frame(variable = v,
             control = mean(hh[[v]][hh$treat == 0]),
             treatment = mean(hh[[v]][hh$treat == 1]),
             p_value = t$p.value)
})
balance <- do.call(rbind, balance)
dir.create(file.path(root, "output"), showWarnings = FALSE)
write.csv(balance, file.path(root, "output", "balance_table.csv"), row.names = FALSE)
""")
w("code/03_analysis.R", """# Main ITT estimates, standard errors clustered by village
library(dplyr)
library(fixest)
root <- here::here()
hh <- readRDS(file.path(root, "data", "clean", "hh_panel.rds"))

m1 <- feols(log(consumption_pc_el) ~ treatment + log_cons, cluster = ~village_id, data = hh)
m2 <- feols(food_insecure_el ~ treatment + food_insecure, cluster = ~village_id, data = hh)
m3 <- feols(child_haz_el ~ treatment, cluster = ~village_id, data = hh)
etable(m1, m2, m3, file = file.path(root, "output", "itt_table.tex"))
""")

# --- documents (long, mostly irrelevant to the tasks) ------------------------
outcomes = ["household consumption per capita", "food insecurity", "child height-for-age",
            "livestock holdings", "female decision-making", "school enrollment",
            "health expenditure", "savings", "debt", "labor supply"]
pap = ["# Cash Plus: Pre-Analysis Plan\n",
       "Registered with the AEA RCT Registry. Version 3.\n"]
for k, o in enumerate(outcomes, 1):
    pap.append(f"\n## {k}. Outcome family: {o}\n")
    for j in range(6):
        pap.append(
            f"Hypothesis H{k}.{j+1}: Households assigned to the cash plus arm will show a "
            f"change in {o} relative to the control arm at endline. We measure {o} using the "
            f"household survey module {k}{chr(65+j)}, administered to the primary respondent. "
            f"The primary specification regresses the endline outcome on treatment assignment, "
            f"the baseline value of the outcome, and strata fixed effects, with standard errors "
            f"clustered at the village level, the unit of randomization. We will adjust for "
            f"multiple hypothesis testing within the {o} family using sharpened q-values. "
            f"Heterogeneity will be examined by female headship, baseline poverty, and distance "
            f"to the nearest market. Attrition will be tested by regressing an indicator of "
            f"non-response on treatment, and Lee bounds will be reported if differential.\n")
w("docs/pre_analysis_plan.md", "".join(pap))

notes = ["# Field notes, 2025 data collection\n"]
for d in range(1, 41):
    v = random.choice(villages)
    notes.append(
        f"\n## Day {d}: village {v}\n"
        f"Team arrived at {random.randint(7,9)}:{random.choice(['00','15','30','45'])}. "
        f"Completed {random.randint(18,32)} household interviews out of the target. "
        f"Two respondents were away at the market and will be revisited. The enumerator "
        f"supervisor re-checked consumption module answers for three households where totals "
        f"looked implausible. Tablets synced at the end of the day without errors. Community "
        f"leader raised questions about the timing of the next transfer, which were referred "
        f"to the implementing partner. Road conditions were {random.choice(['good','muddy','poor'])}.\n")
w("docs/field_notes_2025.md", "".join(notes))

for ver in (1, 2):
    w(f"docs/old_drafts/paper_v{ver}.md",
      f"# Cash Plus paper, draft {ver}\n\n" +
      "".join(f"\n## Section {s}\n" + ("This draft section discusses the context, design and "
              "preliminary results of the Cash Plus evaluation in rural Kenya. " * 25) + "\n"
              for s in range(1, 9)))

w("paper/abstract.md", """# Abstract

We evaluate a cash plus program in rural Kenya that combine unconditional cash transfers with
nutrition coaching for househods with children under five. Using a cluster randomized trial
across 60 villages and 1,200 households, we find that the program increase household
consumption per capita by 12 percent and reduces food insecurity by 9 percentage points one
year after the first transfer. Effects on child height-for-age are positive but imprecise.
Impacts are larger for female-headed househods and for househods further from markets, wich
suggests that the coaching component matter most where access to diverse food are limited.
""")

w("README.md", "# Cash Plus RCT\n\nTODO\n")
w(".here", "")  # makes here::here() resolve to the project folder
print("built", root)
