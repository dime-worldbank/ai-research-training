"""Builds a compact, brand-colored stacked horizontal bar chart of who attended
the bootcamp (by VPU and by seniority), replacing two mismatched pie charts."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

HERE = Path(__file__).parent
MONTSERRAT_BOLD = fm.FontProperties(fname=str(HERE / "fonts" / "Montserrat-ExtraBold-static.ttf"))
LATO = fm.FontProperties(fname=str(HERE / "fonts" / "Lato-Regular.ttf"))
LATO_BOLD = fm.FontProperties(fname=str(HERE / "fonts" / "Lato-Bold.ttf"))

INK = "#1a1a1a"
GREY = "#6b6b6b"

# monochrome purple scale (largest -> smallest), neutral grey for the catch-all
PURPLES = ["#530153", "#800280", "#A64FA6", "#C9A0C9", "#E4CBE4"]
OTHER_GREY = "#C9C9C9"

fig, axes = plt.subplots(2, 1, figsize=(6.85, 2.05), dpi=300)
fig.patch.set_alpha(0)

# (label, pct, color, level) -- level 1 sits just under the bar, level 2 is
# dropped lower with a leader line so narrow neighbouring segments don't collide.
vpu = [
    ("DEC", 48, PURPLES[0], 1),
    ("People", 8, PURPLES[1], 1),
    ("East Asia\n& Pacific", 6, PURPLES[2], 2),
    ("Planet", 6, PURPLES[3], 1),
    ("Prosperity", 6, PURPLES[4], 2),
    ("14 other VPUs", 26, OTHER_GREY, 1),
]
title = [
    ("Senior", 29, PURPLES[0], 1),
    ("Economist / Specialist", 29, PURPLES[1], 1),
    ("Extended Term", 16, PURPLES[2], 1),
    ("STC", 11, PURPLES[3], 1),
    ("Other", 14, OTHER_GREY, 1),
]
bar_rows = [("Participants by VPU", vpu), ("Participants by seniority", title)]

for ax, (row_title, data) in zip(axes, bar_rows):
    ax.axis("off")
    ax.set_facecolor("none")
    ax.set_xlim(0, 100)
    ax.text(0, 0.62, row_title, fontproperties=MONTSERRAT_BOLD, fontsize=10.5,
            color="#530153", ha="left", va="bottom")
    bar_h, left = 0.7, 0
    for label, pct, color, level in data:
        ax.barh(0, pct, left=left, height=bar_h, color=color,
                edgecolor="white", linewidth=1.4, zorder=2)
        cx = left + pct / 2
        wide = pct >= 9
        if wide:
            ax.text(cx, 0, f"{pct}%", ha="center", va="center", fontproperties=LATO_BOLD,
                    fontsize=9.5, color="white" if color != OTHER_GREY else INK, zorder=3)
        text = label if wide else f"{label}\n{pct}%"
        y = -0.52 if level == 1 else -0.95
        if level == 2:
            ax.plot([cx, cx], [-bar_h / 2, y + 0.12], color="#9a9a9a", linewidth=0.6, zorder=1)
        ax.text(cx, y, text, ha="center", va="top", fontproperties=LATO, fontsize=8,
                color=INK, linespacing=1.15)
        left += pct
    ax.set_ylim(-1.75, 1.05)

plt.subplots_adjust(hspace=0.2, left=0.005, right=0.995, top=0.97, bottom=0.01)
out = HERE / "images" / "chart-attendance.png"
fig.savefig(out, transparent=True, bbox_inches="tight", pad_inches=0.04)
print("saved", out)
