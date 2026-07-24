# DECDI Branding

Use this reference whenever creating, improving, or reviewing a DECDI-branded
presentation.

This file defines the branding decisions the skill should apply. Technical
implementation details for Quarto, Beamer, and PowerPoint belong in
`format-conventions.md`.

## Source

This reference was prepared using the
[DECDI Branding Guide](https://www.canva.com/design/DAG_uu89IfA/9M6MXACvYKjn4wmVqjc5Lg/view?utm_content=DAG_uu89IfA&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hf98aceecdd#16).

The guide is the authoritative source for DECDI typography, colors, and logo
usage. If the guide changes or conflicts with this reference, follow the
current guide and update the bundled branding assets accordingly.

## Typography

Use:

- **Montserrat Bold** for titles and headings.
- **Lato** for body text and subheadings.

Maintain a clear visual hierarchy:

- Use the largest type for presentation and section titles.
- Use a consistent heading size across content slides.
- Keep body text large enough to read in presentation view.
- Avoid using multiple unrelated font families in the same deck.

If Montserrat or Lato is unavailable in the selected output format, report the
font substitution rather than assuming the result is visually equivalent.

## Overall colors

Use the overall DECDI palette for decks that are not associated with a specific
Impact Lab or program.

| Name | Hex | Typical use |
|---|---|---|
| Navy | `#002A4F` | Primary headings and section backgrounds |
| Blue dark | `#1C618C` | Secondary emphasis and chart series |
| Blue mid | `#2599CD` | Links, highlights, and chart series |
| Blue light | `#2AACE2` | Supporting chart series |
| Cyan | `#01ADEF` | Accents and highlighted values |

Default to navy and the blue palette. Do not introduce unrelated colors unless
the content requires a clearly explained exception.

## Program colors

Use program colors only when:

- The deck is explicitly associated with that program.
- A figure compares DECDI programs.
- The user requests program-specific branding.

The official base colors are:

| Program | Base color |
|---|---|
| People Impact Lab | `#991D38` |
| Prosperity Impact Lab | `#FFC20D` |
| Infrastructure & Digital Impact Lab | `#047D70` |
| eMBeD | `#F78D28` |
| Analytics | `#800280` |

The following dark and light values are derived for data visualization. They
are useful for ordered values within one program but are not verified official
brand colors.

| Program | Dark, derived | Light, derived |
|---|---|---|
| People Impact Lab | `#631324` | `#C78392` |
| Prosperity Impact Lab | `#A67E08` | `#FFDD7A` |
| Infrastructure & Digital Impact Lab | `#035149` | `#75B8B0` |
| eMBeD | `#A15C1A` | `#FBC089` |
| Analytics | `#530153` | `#B974B9` |

Use:

- Program base colors for categorical comparisons across programs.
- A program's dark, base, and light colors for ordered values within that
  program.
- The overall DECDI palette for general research results.

## Color and contrast

- Maintain sufficient contrast between text and backgrounds.
- Use white text on navy or other dark backgrounds.
- Do not use yellow or other light colors for small text on white backgrounds.
- Do not rely on color alone to distinguish groups or findings.
- Combine color with direct labels, symbols, line styles, or patterns where
  needed.
- Check colors in the rendered deck, not only in the source file.

## Logo selection and use

Use the plain DEC logo by default.

| Context | Logo |
|---|---|
| Standard DECDI deck on a light background | `COLOR_WB_DEC.png` |
| Dark background | `WHITE_WB_DEC.png` |
| Grayscale or black-and-white output | `BLACK_WB_DEC.png` |
| Explicitly LEADS-branded deck | Matching `WB_DEC_LEADS` variant |
| WBG-only material | WBG horizontal logo, when requested |

LEADS and WBG-only variants should not replace the standard DEC logo unless
the deck's purpose requires them.

Do not:

- Stretch or distort a logo.
- Crop the logo.
- Recolor the logo.
- Rotate the logo.
- Recreate the logo with text or other graphics.
- Crowd the logo with text, figures, or other elements.
- Shrink the logo to solve a crowded layout.

Preserve the original aspect ratio and use an existing approved variant.

## Logo placement

The current presentation convention is:

- Show the logo on the title slide.
- Show the logo on the closing or thank-you slide.
- Do not show the logo on ordinary content slides.
- Do not show the logo on section-divider slides.
- Position the logo at the top-right.
- Keep placement and scale consistent between the title and closing slides.

Apply this convention consistently across Quarto, Beamer, and PowerPoint.

If the user requests a different placement, treat it as an explicit branding
change and apply it consistently throughout the deck.

See `format-conventions.md` for how each output format implements the placement.

## Updating the brand

When branding changes:

1. Update `branding/colors.yml`.
2. Update the approved files in `branding/logos/`.
3. Synchronize the copies bundled with Quarto, Beamer, and PowerPoint.
4. Rebuild example decks in all supported formats.
5. Visually inspect colors, fonts, logo variants, placement, and contrast.
6. Update this reference if the approved rules changed.

The paths above are relative to the skill folder. The format-specific folders
under `assets/` must remain complete and usable after being copied into a
user's project.

## Branding review check

Before delivering or approving a deck, confirm that:

- Montserrat and Lato are used where supported.
- Colors come from the approved palette.
- Program colors are used only when appropriate.
- The correct DEC, LEADS, or WBG logo is used.
- The correct logo variant is used for the background.
- Logo placement follows the title-and-closing-slide convention.
- Logos are not stretched, cropped, recolored, or crowded.
- Text and visual contrast are sufficient.
- No outdated or conflicting institutional branding remains.
