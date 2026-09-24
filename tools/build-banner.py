# -*- coding: utf-8 -*-
"""Profile banner generator. Text is outlined with Pretendard so it renders
identically everywhere -- an <img>-embedded SVG cannot load a webfont."""
import io, math, os, random, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb

FONT_SRC = sys.argv[1]
OUT_DIR  = sys.argv[2]
W, H, PAD = 1280, 210, 68
NAME, EYEBROW = "Kyubum Jang", "QA ENGINEER"
GROUND = 178.0
RX = 1074.0

_cache = {}
def _inst(weight):
    if weight in _cache: return _cache[weight]
    f = TTFont(FONT_SRC)
    f = instancer.instantiateVariableFont(f, {"wght": weight}, inplace=True)
    f.flavor = None          # loaded from woff2; save() would re-compress and hb can't parse it
    b = io.BytesIO(); f.save(b); data = b.getvalue()
    face = hb.Face(data); hbf = hb.Font(face)
    assert face.upem == f["head"].unitsPerEm, "hb face upem %s != %s" % (face.upem, f["head"].unitsPerEm)
    _cache[weight] = (f, hbf, f["head"].unitsPerEm, f.getGlyphOrder(), f.getGlyphSet())
    return _cache[weight]

def text_path(text, weight, size, x, y, tracking=0.0, fill="#000"):
    """tracking in px; (x,y) is the left baseline point."""
    tt, hbf, upem, order, gs = _inst(weight)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbf, buf)                       # real GSUB/GPOS -> correct kerning
    s = size / float(upem)
    tr_u = tracking / s
    cur, cmds = 0.0, []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = SVGPathPen(gs)
        gs[order[info.codepoint]].draw(
            TransformPen(pen, (1, 0, 0, 1, cur + pos.x_offset, pos.y_offset)))
        d = pen.getCommands()
        if d: cmds.append(d)
        cur += pos.x_advance + tr_u
    width = (cur - tr_u) * s
    g = ('  <g fill="%s" transform="translate(%.2f %.2f) scale(%.6f %.6f)">\n'
         '    <path d="%s"/>\n  </g>' % (fill, x, y, s, -s, " ".join(cmds)))
    return g, width

def tree(P):
    rnd = random.Random(23)
    segs, tips = [], []
    def grow(x, y, ang, ln, depth, wd):
        x2 = x + math.sin(ang) * ln
        y2 = y - math.cos(ang) * ln
        bow = ln * rnd.uniform(-0.17, 0.17)
        segs.append((x, y, (x+x2)/2 + math.cos(ang)*bow, (y+y2)/2 + math.sin(ang)*bow,
                     x2, y2, wd, depth))
        if depth == 0:
            tips.append((x2, y2)); return
        spread = 0.38 + rnd.uniform(-0.05, 0.13)
        lean = rnd.uniform(-0.10, 0.10)
        for sgn in (-1, 1):
            grow(x2, y2, ang + sgn*spread + lean + rnd.uniform(-0.13, 0.13),
                 ln * rnd.uniform(0.70, 0.81), depth-1, max(wd*0.63, 0.85))
        if depth in (3, 4) and rnd.random() < 0.5:
            grow(x2, y2, ang + lean + rnd.uniform(-0.12, 0.12),
                 ln*0.60, depth-2, max(wd*0.5, 0.85))
    grow(RX, GROUND, 0.035, 50.0, 5, 8.2)

    o = ['  <ellipse cx="%.0f" cy="78" rx="120" ry="76" fill="url(#haze)"/>' % (RX+6),
         '  <g fill="none" stroke="%s" stroke-linecap="round">' % P["leaf"]]
    for x1,y1,cx,cy,x2,y2,wd,d in sorted(segs, key=lambda s: -s[7]):
        o.append('    <path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" stroke-width="%.2f" opacity="%.3f"/>'
                 % (x1,y1,cx,cy,x2,y2,wd, P["limb0"] + (5-d)*0.052))
    o.append('  </g>')

    # spread the pick across the whole crown, not just the topmost twigs,
    # otherwise the dots line up along the skyline and read as bulbs.
    # greedy min-distance over a shuffled pool: no clumping, but not evenly
    # spaced either -- even spacing is what makes them read as a string of lights
    rf = random.Random(9)
    pool = sorted(tips, key=lambda t: t[1])[:46]
    rf.shuffle(pool)
    picks, MIN = [], 15.0
    for tx, ty in pool:
        if all((tx - px) ** 2 + (ty - py) ** 2 >= MIN * MIN for px, py in picks):
            picks.append((tx, ty))
        if len(picks) == 11:
            break
    picks.sort(key=lambda t: t[1])          # draw far/high fruit first

    for tx, ty in picks:
        fx = tx + rf.uniform(-1.6, 1.6)
        fy = ty + rf.uniform(4.2, 7.0)          # fruit hangs below the twig it grew on
        r  = rf.uniform(3.3, 4.4)
        o.append('  <path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" '
                 'stroke-width="1.1" stroke-linecap="round" opacity="0.70"/>'
                 % (tx, ty, tx, (ty+fy)/2, fx, fy-r+0.6, P["leaf"]))
        o.append('  <circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.13"/>'
                 % (fx, fy, r*1.75, P["fruit"]))
        o.append('  <circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="1.15"/>'
                 % (fx, fy, r, P["fruit"], P["case"]))
    return "\n".join(o)

def build(P, name):
    eyebrow, _ = text_path(EYEBROW, 600, 13, PAD, 82, tracking=4.6, fill=P["eyebrow"])
    title,  tw = text_path(NAME,    700, 56, PAD, 140, tracking=-0.9, fill=P["name"])
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s, %s">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>
    </linearGradient>
    <radialGradient id="haze">
      <stop offset="0" stop-color="%s" stop-opacity="%.2f"/>
      <stop offset="1" stop-color="%s" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rule" gradientUnits="userSpaceOnUse" x1="%d" y1="0" x2="%d" y2="0">
      <stop offset="0" stop-color="%s" stop-opacity="0"/>
      <stop offset="0.42" stop-color="%s" stop-opacity="%.2f"/>
      <stop offset="0.82" stop-color="%s" stop-opacity="%.2f"/>
      <stop offset="1" stop-color="%s" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="%d" height="%d" rx="12" fill="url(#bg)"/>
%s
  <line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="url(#rule)" stroke-width="1.25"/>
%s
%s
</svg>
""" % (W,H,W,H, NAME, EYEBROW,
       P["bg1"], P["bg2"],
       P["leaf"], P["haze"], P["leaf"],
       PAD, W-PAD, P["rule"], P["rule"], P["ruleA"], P["rule"], P["ruleB"], P["rule"],
       W, H, tree(P), PAD, GROUND, W-PAD, GROUND, eyebrow, title)
    p = os.path.join(OUT_DIR, name)
    io.open(p, "w", encoding="utf-8", newline="\n").write(svg)
    print("  %-18s %6d bytes   title width %.1fpx" % (name, os.path.getsize(p), tw))

# palette lifted straight from ai-qc-platform/frontend/src/app/globals.css
DARK = dict(bg1="#020617", bg2="#0F172A",            # --bg-base -> --bg-surface (dark)
            leaf="#10B981", haze=0.11, fruit="#F87171", case="#0A1020",
            name="#F8FAFC", eyebrow="#94A3B8",
            rule="#334155", ruleA=0.55, ruleB=0.80, limb0=0.46)
LIGHT = dict(bg1="#F8FAFC", bg2="#EDF2F7",           # --neutral-50 -> elevated
            leaf="#059669", haze=0.06, fruit="#DC2626", case="#F4F8FB",
            name="#0F172A", eyebrow="#475569",
            rule="#94A3B8", ruleA=0.50, ruleB=0.72, limb0=0.50)
build(DARK,  "banner-dark.svg")
build(LIGHT, "banner-light.svg")
