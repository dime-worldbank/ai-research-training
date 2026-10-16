"""Duplicate a slide in a python-pptx Presentation, correctly.

python-pptx has no built-in "duplicate slide" method. The obvious approach
-- add a new slide on the same layout, then copy each shape across -- drops
two things silently:

1. The slide-level background fill (<p:bg>). It lives as a sibling of the
   shape tree (<p:spTree>) under <p:cSld>, not inside it, so a shape-by-shape
   copy never touches it. The duplicate renders with no background fill even
   though every shape copied correctly -- e.g. duplicating this skill's navy
   section-divider slide (slide index 1 in template.pptx) silently produces
   a slide with a plain white background and (if the title text is styled
   white-on-navy, as the divider's is) invisible white-on-white text. This
   is not a hypothetical: it's the actual bug that motivated this file.
2. Image relationships. A copied picture shape's XML still points at the
   *source* slide's relationship ID (r:embed="rIdN") -- the destination
   slide has its own, unrelated relationship list, so the copied picture
   either fails to resolve or (worse) silently resolves to whatever
   unrelated part happens to occupy that same rId in the new slide.

Use `duplicate_slide(prs, index)` when building a deck from this skill's
starter slides (e.g. "duplicate the closest starter slide for each new
slide" in format-conventions.md) instead of hand-rolling shape copies.

Usage:
    from pptx import Presentation
    from duplicate_slide import duplicate_slide

    prs = Presentation("template.pptx")
    new_slide = duplicate_slide(prs, 2)   # duplicates slide index 2
    prs.save("output.pptx")
"""
import copy

from pptx.oxml.ns import qn
from pptx.opc.constants import RELATIONSHIP_TYPE as RT


def duplicate_slide(prs, index):
    """Duplicate the slide at `index` (0-based) in `prs` and append the copy
    at the end of the deck. Returns the new Slide object.

    Preserves the slide-level background fill and re-links any image
    relationships so copied pictures still resolve correctly.
    """
    source = prs.slides[index]
    dest = prs.slides.add_slide(source.slide_layout)

    # The new slide's layout auto-populates placeholder shapes (title,
    # body, etc.) -- remove them before deep-copying the source's own shape
    # tree, or the duplicate ends up with both sets.
    for shape in list(dest.shapes):
        shape._element.getparent().remove(shape._element)

    # Map source relationship IDs to newly created destination relationship
    # IDs for any image parts referenced by copied shapes, so r:embed
    # attributes can be rewritten to point at valid relationships in the
    # destination slide rather than the source's.
    rId_map = {}

    def remap_image_rels(element):
        for blip in element.iter(qn("a:blip")):
            old_rId = blip.get(qn("r:embed"))
            if not old_rId:
                continue
            if old_rId not in rId_map:
                image_part = source.part.related_part(old_rId)
                rId_map[old_rId] = dest.part.relate_to(image_part, RT.IMAGE)
            blip.set(qn("r:embed"), rId_map[old_rId])

    for shape in source.shapes:
        new_el = copy.deepcopy(shape._element)
        remap_image_rels(new_el)
        dest.shapes._spTree.append(new_el)

    # Copy the slide-level background (<p:bg>) -- see module docstring for
    # why this needs to be handled separately from the shape copy above.
    # <p:bg> must be the first child of <p:cSld>, immediately before
    # <p:spTree>, per the OOXML schema.
    source_cSld = source._element.find(qn("p:cSld"))
    source_bg = source_cSld.find(qn("p:bg"))
    if source_bg is not None:
        dest_cSld = dest._element.find(qn("p:cSld"))
        dest_cSld.insert(0, copy.deepcopy(source_bg))

    return dest


if __name__ == "__main__":
    import sys
    from pptx import Presentation

    if len(sys.argv) != 4:
        print("Usage: python3 duplicate_slide.py <input.pptx> <slide-index> <output.pptx>")
        sys.exit(1)

    in_path, index, out_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    prs = Presentation(in_path)
    duplicate_slide(prs, index)
    prs.save(out_path)
    print(f"Duplicated slide {index} of {in_path}; saved to {out_path}")
