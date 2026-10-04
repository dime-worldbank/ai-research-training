"""Draw the screening-strategy decision trees used in literature-session.qmd.

Each tree starts from the first LLM pass and ends in full text, exclude,
human review or an LLM rerun. Numbers are papers per 100 (fictional review).
Run: python3 trees.py  -> writes images/strategy-*.svg
"""

from pathlib import Path

BOX_W, BOX_H = 176, 58
LEAF_W = 200          # horizontal space per leaf
LEVEL_H = 158         # vertical distance between box tops
STYLE = {
    "root": ("#FFFFFF", "#1A1A1A", "#1A1A1A", "bold"),
    "q":    ("#EDEEF0", "#5A5F66", "#1A1A1A", "italic"),
    "full": ("#E6F2E6", "#2E7D32", "#1A1A1A", "normal"),
    "exc":  ("#F8E1E1", "#C0392B", "#1A1A1A", "normal"),
    "hum":  ("#FBEEDC", "#A6640C", "#1A1A1A", "normal"),
    "rer":  ("#E3F1F0", "#0F6B6B", "#0F3F3F", "bold"),
}


def N(kind, text, *children):
    return {"kind": kind, "text": text, "children": list(children)}


def E(cond, num, node):
    return (cond, num, node)


def leaves(node):
    if not node["children"]:
        return 1
    return sum(leaves(c[2]) for c in node["children"])


def layout(node, x0, depth, out, edges):
    width = leaves(node) * LEAF_W
    cx = x0 + width / 2
    y = depth * LEVEL_H
    out.append((node, cx, y))
    x = x0
    for cond, num, child in node["children"]:
        w = leaves(child) * LEAF_W
        ccx = x + w / 2
        edges.append((cx, y + BOX_H, ccx, (depth + 1) * LEVEL_H, cond, num))
        layout(child, x, depth + 1, out, edges)
        x += w
    return width


def text_lines(s):
    return s.split("\n")


def svg(tree, depth_max):
    boxes, edges = [], []
    width = layout(tree, 0, 0, boxes, edges)
    height = depth_max * LEVEL_H + BOX_H + 4
    p = [f'<svg viewBox="-4 -4 {width + 8} {height + 8}" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Lato, Helvetica, Arial, sans-serif" role="img">']
    p.append('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
             'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#4A4F57"/></marker></defs>')
    for x1, y1, x2, y2, cond, num in edges:
        ym = y1 + 18
        p.append(f'<path d="M{x1},{y1} V{ym} H{x2} V{y2 - 2}" fill="none" stroke="#4A4F57" '
                 f'stroke-width="1.6" marker-end="url(#ah)"/>')
        ty = ym + 26
        for i, line in enumerate(text_lines(cond)):
            p.append(f'<text x="{x2 + 6}" y="{ty + i * 21}" font-size="19" font-weight="700" '
                     f'fill="#1A1A1A">{line}</text>')
        nl = len(text_lines(cond))
        p.append(f'<text x="{x2 + 6}" y="{ty + nl * 21}" font-size="19" fill="#800280" '
                 f'font-weight="700">{num}</text>')
    for node, cx, y in boxes:
        fill, stroke, color, weight = STYLE[node["kind"]]
        x = cx - BOX_W / 2
        p.append(f'<rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="7" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="2"/>')
        lines = text_lines(node["text"])
        style = 'font-style="italic"' if weight == "italic" else f'font-weight="{ "700" if weight == "bold" else "400"}"'
        for i, line in enumerate(lines):
            ty = y + BOX_H / 2 + 7 + (i - (len(lines) - 1) / 2) * 21
            p.append(f'<text x="{cx}" y="{ty}" font-size="20" text-anchor="middle" fill="{color}" '
                     f'{style}>{line}</text>')
    p.append("</svg>")
    return "\n".join(p)


def first_pass(*children):
    return N("root", "LLM pass 1", E("", "", N("q", "How many Nos?", *children)))


TREES = {
    "strategy-1": (N("q", "How many Nos?",
                     E("0", "12", N("full", "Full text")),
                     E("1", "40", N("exc", "Exclude")),
                     E("2+", "48", N("exc", "Exclude"))), 1),
    "strategy-6": (N("q", "How many Nos?",
                     E("0", "12", N("full", "Full text")),
                     E("1", "40", N("hum", "Human review")),
                     E("2+", "48", N("exc", "Exclude"))), 1),
    "strategy-3": (N("q", "How many Nos?",
                     E("0", "12", N("full", "Full text")),
                     E("1", "40", N("rer", "Ask once more",
                                    E("still No", "37.2", N("exc", "Exclude")),
                                    E("flips", "2.8", N("hum", "Human review")))),
                     E("2+", "48", N("exc", "Exclude"))), 2),
    "strategy-4": (N("q", "How many Nos?",
                     E("0", "12", N("full", "Full text")),
                     E("1", "40", N("rer", "Ask up to 3×",
                                    E("No every\ntime", "33.4", N("exc", "Exclude")),
                                    E("any Yes", "6.6", N("hum", "Human review")))),
                     E("2+", "48", N("exc", "Exclude"))), 2),
    "strategy-5": (N("q", "How many Nos?",
                     E("0", "12", N("full", "Full text")),
                     E("1", "40", N("q", "Which\ncriterion?",
                                    E("easy", "10", N("rer", "Ask once more",
                                                      E("still No", "9.8", N("exc", "Exclude")),
                                                      E("flips", "0.2", N("hum", "Human")))),
                                    E("Design", "22", N("rer", "Ask up to 3×",
                                                        E("No every\ntime", "20.2", N("exc", "Exclude")),
                                                        E("any Yes", "1.8", N("hum", "Human")))),
                                    E("Outcome", "8", N("hum", "Human review")))),
                     E("2+", "48", N("exc", "Exclude"))), 3),
}


if __name__ == "__main__":
    out = Path(__file__).parent / "images"
    out.mkdir(exist_ok=True)
    for name, (tree, depth) in TREES.items():
        (out / f"{name}.svg").write_text(svg(tree, depth))
        print("wrote", name)
