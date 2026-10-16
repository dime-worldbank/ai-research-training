"""Builds the "what participants gained" chart: share of respondents who agree /
strongly agree with each end-of-course confidence statement."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from pathlib import Path

HERE = Path(__file__).parent
CSV = HERE.parent / "data" / "AI-Enabled Research Bootcamp Feedback Survey.csv"
MONTSERRAT = fm.FontProperties(fname=str(HERE / "fonts" / "Montserrat-ExtraBold-static.ttf"))
LATO = fm.FontProperties(fname=str(HERE / "fonts" / "Lato-Regular.ttf"))
LATO_BOLD = fm.FontProperties(fname=str(HERE / "fonts" / "Lato-Bold.ttf"))

INK, GREY = "#1a1a1a", "#6b6b6b"
STRONG, AGREE = "#530153", "#B974B9"

STATEMENTS = [
    ("I understand WBG ethics and governance\nrequirements for AI use", "ethics and governance"),
    ("I know how to check and verify\nAI outputs before using them", "check and verify"),
    ("I feel confident directing an AI agent\non a research task", "confident directing"),
    ("I understand the cost and efficiency\ntrade-offs of using AI agents", "cost and efficiency"),
]

df = pd.read_csv(CSV)
df = df[df["Id"].notna()]

rows = []
for label, key in STATEMENTS:
    col = next(c for c in df.columns if key in c)
    s = df[col].dropna()
    n = len(s)
    rows.append((label, (s == "Strongly agree").sum() / n * 100, (s == "Agree").sum() / n * 100, n))
    print(key, n, rows[-1][1:3])

rows.sort(key=lambda r: r[1] + r[2])

fig, ax = plt.subplots(figsize=(7.2, 2.45), dpi=300)
fig.patch.set_alpha(0)
ax.set_facecolor("none")
for i, (label, strong, agree, n) in enumerate(rows):
    ax.barh(i, strong, color=STRONG, height=0.62, edgecolor="white", linewidth=1.2)
    ax.barh(i, agree, left=strong, color=AGREE, height=0.62, edgecolor="white", linewidth=1.2)
    ax.text(strong / 2, i, f"{strong:.0f}%", ha="center", va="center",
            fontproperties=LATO_BOLD, fontsize=8, color="white")
    ax.text(strong + agree / 2, i, f"{agree:.0f}%", ha="center", va="center",
            fontproperties=LATO_BOLD, fontsize=8, color=INK)
    ax.text(strong + agree + 1.5, i, f"{strong + agree:.0f}%", ha="left", va="center",
            fontproperties=MONTSERRAT, fontsize=10, color=STRONG)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows])
for t in ax.get_yticklabels():
    t.set_fontproperties(LATO)
    t.set_fontsize(8.3)
    t.set_color(INK)
ax.set_xlim(0, 100)
ax.set_xticks([])
for sp in ax.spines.values():
    sp.set_visible(False)
ax.tick_params(left=False)
# legend
ax.scatter([0], [len(rows) - 0.25 + 0.55], marker="s", s=45, color=STRONG, clip_on=False)
ax.text(2.2, len(rows) - 0.25 + 0.55, "Strongly agree", fontproperties=LATO, fontsize=8, va="center", color=GREY)
ax.scatter([24], [len(rows) - 0.25 + 0.55], marker="s", s=45, color=AGREE, clip_on=False)
ax.text(26.2, len(rows) - 0.25 + 0.55, "Agree", fontproperties=LATO, fontsize=8, va="center", color=GREY)
ax.set_ylim(-0.5, len(rows) + 0.5)
plt.subplots_adjust(left=0.36, right=0.98, top=0.9, bottom=0.02)
out = HERE / "images" / "chart-gains.png"
fig.savefig(out, transparent=True, bbox_inches="tight", pad_inches=0.05)
print("saved", out)
