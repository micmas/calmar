# CALMaR colour palette

Five colours. Everything CALMaR produces — figures, the QC dashboard,
reports, slides — draws from these and the derived steps below. The
roles are fixed so that the same colour always means the same thing
across the project.

| Name | Hex | RGB | HSL | Role |
|---|---|---|---|---|
| **Dusty Grape** | `#52489c` | 82, 72, 156 | 247°, 37 %, 45 % | Brand ink: titles, section headings, emphasis. The **person** in a workflow. |
| **Smart Blue** | `#4062bb` | 64, 98, 187 | 223°, 49 %, 49 % | Primary data colour; the **machine / model** in a workflow. Series 1. |
| **Strong Cyan** | `#59c3c3` | 89, 195, 195 | 180°, 47 %, 56 % | **Approved / canonical / verified**. Series 3. Fill only — never text. |
| **Platinum** | `#ebebeb` | 235, 235, 235 | 0°, 0 %, 92 % | Surfaces, panels, gridlines, separators. Never data. |
| **Bubblegum Pink** | `#f45b69` | 244, 91, 105 | 355°, 87 %, 66 % | **Attention**: the lesion, a rejection, a warning, the thing to look at. Series 2. |

Machine-readable copies: `calmar_palette.json` (this table plus the
derived steps) and the CSS block at the end of this file.

```
CSV      52489c,4062bb,59c3c3,ebebeb,f45b69
Hex      #52489c, #4062bb, #59c3c3, #ebebeb, #f45b69
Array    ["52489c","4062bb","59c3c3","ebebeb","f45b69"]
Object   {"Dusty Grape":"52489c","Smart Blue":"4062bb","Strong Cyan":"59c3c3","Platinum":"ebebeb","Bubblegum Pink":"f45b69"}
```

## What the validator says (and what it means in practice)

The palette was run through a colour-vision-deficiency and contrast
check (OKLab ΔE for deutan / protan / tritan simulation, WCAG contrast
against the surface). Three things to know before using it for data:

1. **Dusty Grape and Smart Blue must never be adjacent data series.**
   They are 24° apart in hue and only ΔE 7.9 apart to normal vision
   (floor is 15) and ΔE 6.3 under deutan simulation. Side by side in a
   bar chart they read as one colour. That is why Grape is *ink*
   (headings, the human actor, emphasis) and Blue is *data*. If a chart
   needs both, put text labels on the marks.
2. **Strong Cyan is 2.1 : 1 against white** — below the 3 : 1 floor for
   a mark standing alone, and far below the 4.5 : 1 needed for text.
   Rule: Cyan is a fill that always carries a visible label (a value at
   the bar end, a name beside the swatch), and Cyan text uses the
   darkened step `#1f7f7f` (4.8 : 1) instead.
3. **The safe categorical order is Blue → Pink → Cyan.** That ordering
   passes every adjacent-pair and all-pairs check (worst pair: Cyan ↔
   Pink, ΔE 12.4 deutan, 29.6 normal). Three data series is the cap;
   a fourth folds into "Other" (neutral `#bdbdbd`) or becomes a second
   panel. Grape is not a fourth series.

Text contrast on white, for reference: Grape 7.6 : 1, Blue 5.7 : 1,
Pink 3.2 : 1 (large text only — ≥ 18 px bold), Cyan 2.1 : 1 (never).

## Derived steps

Stay inside these; do not invent new tints per figure.

| Purpose | Value | Derived from |
|---|---|---|
| Body text | `#2b2b3a` | neutral, slight grape cast (13.9 : 1) |
| Secondary text | `#5a5a66` | neutral (6.8 : 1) |
| Cyan as text / icon | `#1f7f7f` | Strong Cyan darkened to 4.8 : 1 |
| Neutral data ("Other", "no value") | `#bdbdbd` | Platinum darkened so it reads as a mark |
| Page / chart surface | `#ffffff` | — |
| Panel surface | `#f7f7f7` | Platinum lightened |
| Panel border, gridlines | `#ebebeb` | Platinum |
| Strong border, axis | `#d6d6d6` | Platinum darkened |
| Blue tint (lane, highlight) | Smart Blue at 6–12 % opacity | |
| Pink tint (warning panel) | Bubblegum Pink at 8–15 % opacity | |
| Grape tint (callout) | Dusty Grape at 8–12 % opacity | |
| Highlight (annotated PDF) | any core colour at 35–40 % opacity | |

## Role map for figures and UI

| Element | Colour |
|---|---|
| Title, section label, emphasis | Dusty Grape |
| The person / reviewer / human gate | Dusty Grape (fill, white text) |
| The model / agent / automated step | Smart Blue (fill, white text) |
| Approved entry, canonical KB, "verified" | Strong Cyan (fill + label) |
| Lesion mask, rejection, warning, caveat | Bubblegum Pink |
| Panels, cards, separators, gridlines | Platinum family |
| Sequential ramp (one magnitude) | Smart Blue 100 → 700 (light → dark) |
| Diverging (two poles) | Smart Blue ↔ Bubblegum Pink with Platinum `#ebebeb` midpoint |

In the `aphasia-kb` annotated PDFs the `supports` tags map as: claim =
Smart Blue, statistics = Bubblegum Pink, sample = Strong Cyan,
limitation = Dusty Grape, method / confounders / region_definition =
neutral `#bdbdbd`.

## Dark surfaces

On a dark slide (`#1a1a24`), Pink and Cyan sit outside the comfortable
lightness band and look fluorescent. Use `#e04a58` for Pink and
`#3fa9a9` for Cyan on dark surfaces; Blue and Grape lighten to
`#5b7fd6` and `#7a6fc4`. Re-validate if you change these.

## CSS

```css
:root {
  --calmar-grape:   #52489c;
  --calmar-blue:    #4062bb;
  --calmar-cyan:    #59c3c3;
  --calmar-platinum:#ebebeb;
  --calmar-pink:    #f45b69;

  --calmar-ink:        #2b2b3a;
  --calmar-ink-2:      #5a5a66;
  --calmar-cyan-ink:   #1f7f7f;
  --calmar-neutral:    #bdbdbd;
  --calmar-surface:    #ffffff;
  --calmar-panel:      #f7f7f7;
  --calmar-line:       #ebebeb;
  --calmar-line-strong:#d6d6d6;
}
```

## Python (matplotlib / nilearn)

```python
CALMAR = {
    "grape": "#52489c", "blue": "#4062bb", "cyan": "#59c3c3",
    "platinum": "#ebebeb", "pink": "#f45b69",
}
CALMAR_SERIES = [CALMAR["blue"], CALMAR["pink"], CALMAR["cyan"]]   # max 3; validated order
import matplotlib as mpl
mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=CALMAR_SERIES)
```
