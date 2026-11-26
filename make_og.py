#!/usr/bin/env python3
"""make_og.py — og.png 1200x630 for RIND by Block Island Charcuterie demo host.
Lane painter pattern (honey-bistro lineage, forked via deannas-wine-bar). Header-line
width guards live: tracked mono lines measured and asserted before save (jeyas lesson:
shorten the line, never shrink tracking below 4). Palette = the site's cheese-wax system.
Text facts press-verified only (Newsday / GreaterLongIsland / Hoodline, Oct 2026)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "public", "og.png")

W, H = 1200, 630
INK = (36, 28, 20)       # --ink roast brown
ROAST = (58, 44, 29)     # --roast
RIND = (192, 90, 44)     # --rind paprika wax
RIND_DK = (143, 60, 24)  # --rind-dk
GOLD = (223, 164, 67)    # --gold
SAGE = (93, 107, 69)     # --sage wax
BONE = (246, 240, 226)   # --bone
SOFT = (234, 223, 190)   # --soft
MAROON = (124, 47, 35)   # salumi

def F(size, bold=False, italic=False):
    cands = []
    if bold:
        cands += ["/System/Library/Fonts/Supplemental/Iowan Old Style Bold.ttf",
                  "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"]
    elif italic:
        cands += ["/System/Library/Fonts/Supplemental/Iowan Old Style Italic.ttf",
                  "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"]
    cands += ["/System/Library/Fonts/Supplemental/Iowan Old Style Roman.ttf",
              "/System/Library/Fonts/Supplemental/Times New Roman.ttf"]
    for c in cands:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except OSError:
                continue
    return ImageFont.load_default()

def MONO(size):
    for c in ["/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Monaco.ttf"]:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except OSError:
                continue
    return ImageFont.load_default()

def tracked_width(draw, text, font, tracking):
    total = 0
    for ch in text:
        total += draw.textlength(ch, font=font) + tracking
    return total - tracking

def draw_tracked(draw, x, y, text, font, tracking, fill):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=font, fill=fill)
        cx += draw.textlength(ch, font=font) + tracking
    return cx

img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# outer wax frame: rind top bar + gold hairline inner frame
d.rectangle([0, 0, W - 1, 7], fill=RIND)
d.rectangle([0, H - 4, W - 1, H - 1], fill=GOLD)
d.rectangle([26, 26, W - 27, H - 27], outline=(96, 74, 50), width=2)

TEXT_W = 740  # left column budget (graphic occupies the right ~380px)

# top kicker line
y = 62
kw = tracked_width(d, "BUILD-YOUR-OWN CHARCUTERIE", MONO(21), 9)
assert kw <= TEXT_W, "og guard: kicker too wide (%d)" % kw
draw_tracked(d, 64, y, "BUILD-YOUR-OWN CHARCUTERIE", MONO(21), 9, GOLD)

# giant RIND wordmark
f_mark = F(196, bold=True)
tw = tracked_width(d, "RIND", f_mark, 18)
assert tw <= TEXT_W, "og guard: RIND too wide (%d)" % tw
y = 108
draw_tracked(d, 62, y, "RIND", f_mark, 18, BONE)
# rind-orange underline bar beneath the wordmark
d.rectangle([64, y + 212, 64 + tw, y + 222], fill=RIND)

# parent-brand italic line
f_sub = F(38, italic=True)
sub = "by Block Island Charcuterie"
assert d.textlength(sub, font=f_sub) <= TEXT_W, "og guard: sub line"
d.text((64, y + 240), sub, font=f_sub, fill=SOFT)

# feature lines (mono, tracked — measured guards)
f_line = MONO(23)
lines = [
    ("CUT CHEESE  ·  CURED MEATS", 7, BONE),
    ("HOLIDAY BOARDS  &  GRAZING TABLES", 7, GOLD),
]
y2 = 430
for text, trk, col in lines:
    wpx = tracked_width(d, text, f_line, trk)
    assert wpx <= TEXT_W, "og guard: line too wide (%d): %r" % (wpx, text)
    draw_tracked(d, 64, y2, text, f_line, trk, col)
    y2 += 44

# foot lines — stacked two rows, each guarded against the left column budget
f_foot = MONO(16)
foot1 = "OPENING AROUND THANKSGIVING 2026  ·  NORTHPORT NY"
foot2 = "THE THOMPSON BUILDING  ·  24 WOODBINE AVE"
w1 = tracked_width(d, foot1, f_foot, 4)
w2 = tracked_width(d, foot2, f_foot, 4)
assert w1 <= TEXT_W and w2 <= TEXT_W, "og guard: foot lines (%d, %d)" % (w1, w2)
draw_tracked(d, 64, 534, foot1, f_foot, 4, RIND)
draw_tracked(d, 64, 562, foot2, f_foot, 4, SOFT)

# ---- right graphic: flat grazing board (same shapes language as the hero SVG) ----
BX, BY = 812, 96
d.rounded_rectangle([BX, BY, BX + 330, BY + 420], 22, fill=ROAST)
d.rounded_rectangle([BX + 12, BY + 12, BX + 318, BY + 408], 16, fill=(201, 162, 107))
# cheese wheel with rind ring + wedge cut
d.ellipse([BX + 34, BY + 42, BX + 158, BY + 166], fill=BONE, outline=RIND, width=10)
d.pieslice([BX + 34, BY + 42, BX + 158, BY + 166], -60, 0, fill=GOLD, outline=RIND, width=10)
# salami coins
for (ox, oy, r, col) in [(200, 60, 33, MAROON), (252, 104, 33, RIND_DK), (216, 142, 33, (163, 74, 34))]:
    d.ellipse([BX + ox - r, BY + oy - r, BX + ox + r, BY + oy + r], fill=col, outline=(95, 32, 24), width=5)
# crackers
d.rounded_rectangle([BX + 42, BY + 250, BX + 92, BY + 300], 8, fill=(231, 212, 172), outline=(185, 153, 62), width=4)
d.rounded_rectangle([BX + 98, BY + 268, BX + 148, BY + 318], 8, fill=(234, 223, 190), outline=(185, 153, 62), width=4)
# olives + leaf + grape cluster
d.ellipse([BX + 186, BY + 262, BX + 208, BY + 284], fill=SAGE)
d.ellipse([BX + 214, BY + 276, BX + 236, BY + 298], fill=(80, 96, 60))
d.polygon([(BX + 248, BY + 246), (BX + 300, BY + 232), (BX + 288, BY + 262)], fill=SAGE)
for (gx, gy) in [(258, 306), (282, 314), (270, 332)]:
    d.ellipse([BX + gx - 12, BY + gy - 12, BX + gx + 12, BY + gy + 12], fill=(109, 75, 138))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, "PNG")
print("wrote", OUT)
