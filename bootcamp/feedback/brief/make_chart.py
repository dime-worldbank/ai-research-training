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

vpu = [
    ("DEC", 48, PURPLES[0]),
    ("People", 8, PURPLES[1]),
    ("East Asia & Pacific", 6, PURPLES[2]),
    ("Planet", 6, PURPLES[3]),
    ("Prosperity", 6, PURPLES[4]),
    ("14 other VPUs", 26, OTHER_GREY),
]

title = [
    ("Senior", 29, PURPLES[0]),
    ("Economist / Specialist", 29, PURPLES[1]),
    ("Extended Term", 16, PURPLES[2]),
    ("Consultant", 11, PURPLES[3]),
    ("Lead, Analyst, Program Assistant, other", 14, OTHER_GREY),
]

fig, axes = plt.subplots(2, 1, figsize=(7.0, 2.0), dpi=300)
fig.patch.set_alpha(0)

bar_rows = [("Participants by VPU", vpu), ("Participants by seniority", title)]

for ax, (row_title, data) in zip(axes, bar_rows):
    ax.axis("off")
    ax.set_facecolor("none")
    ax.set_xlim(0, 100)

    ax.text(0, 1.22, row_title, fontproperties=MONTSERRAT_BOLD, fontsize=11.5,
             color="#530153", ha="left", va="bottom")

    left = 0
    bar_h = 0.6
    bar_y = 0
    for label, pct, color in data:
        ax.barh(bar_y, pct, left=left, height=bar_h, color=color,
                edgecolor="white", linewidth=1.4, zorder=2)
        cx = left + pct / 2
        if pct >= 9:
            txt_color = "white" if color != OTHER_GREY else INK
            ax.text(cx, bar_y, f"{pct}%", ha="center", va="center",
                     fontproperties=LATO_BOLD, fontsize=10, color=txt_color, zorder=3)
        left += pct

    # legend row under each bar: swatch + label + %
    legend_top = -0.72
    row_h = 0.5
    col_w = 100 / 3
    for i, (label, pct, color) in enumerate(data):
        col = i % 3
        rrow = i // 3
        gx = col * col_w
        gy = legend_top - rrow * row_h
        ax.scatter([gx], [gy], marker="s", s=80, color=color,
                   edgecolor="white", linewidth=0.6, zorder=3, clip_on=False)
        ax.text(gx + 2.6, gy, f"{label} ({pct}%)", ha="left", va="center",
                 fontproperties=LATO, fontsize=8.6, color=INK, clip_on=False)

    n_legend_rows = -(-len(data) // 3)
    ax.set_ylim(legend_top - (n_legend_rows - 1) * row_h - 0.35, 1.5)

plt.subplots_adjust(hspace=0.5, left=0.01, right=0.99, top=0.97, bottom=0.03)
out = HERE / "images" / "chart-attendance.png"
fig.savefig(out, transparent=True, bbox_inches="tight", pad_inches=0.08)
print("saved", out)
