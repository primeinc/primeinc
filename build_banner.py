#!/usr/bin/env python3
"""
Cyberpunk SVG banner generator.

Converts any text + tagline into an animated SVG banner with:
  - Animated gradient background (purple/indigo cycle)
  - Text rendered as vector paths (no font dependencies in output)
  - Neon glow, ghost echo layers, flicker animation
  - Paint drips, floating particles, scanlines, corner brackets

Requires: pip install fonttools

Usage:
  python build_banner.py                          # rebuild defaults
  python build_banner.py --text "HELLO"           # custom main text
  python build_banner.py --tagline "SUB TEXT"      # custom tagline
  python build_banner.py --out my-banner.svg       # custom output path
  python build_banner.py --text "WP" --out wp.svg --text "primeinc" --out pi.svg  # multiple

Examples:
  python build_banner.py
    -> Builds banner-primeinc.svg and banner.svg with current defaults

  python build_banner.py --text "ACME" --tagline "WE MAKE STUFF" --out acme.svg
    -> Single custom banner
"""
import argparse
import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MAIN_FONT = os.path.join(SCRIPT_DIR, "fonts", "PermanentMarker.ttf")
DEFAULT_TAG_FONT = os.path.join(SCRIPT_DIR, "fonts", "Orbitron.ttf")


def text_to_path_group(font_path, text, font_size, cx, cy, letter_spacing=0, attrs=""):
    """Convert a string to a centered SVG <g> element containing <path> elements."""
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    upm = font["head"].unitsPerEm
    scale = font_size / upm
    glyphset = font.getGlyphSet()

    # Measure total width
    total_width = 0
    for i, char in enumerate(text):
        glyph_name = cmap.get(ord(char))
        advance = hmtx[glyph_name][0] if glyph_name else upm // 3
        total_width += advance * scale
        if i < len(text) - 1:
            total_width += letter_spacing

    # Build path elements
    paths = []
    x = 0
    for i, char in enumerate(text):
        glyph_name = cmap.get(ord(char))
        if glyph_name:
            pen = SVGPathPen(glyphset)
            glyphset[glyph_name].draw(pen)
            d = pen.getCommands()
            if d:
                paths.append(
                    f'    <path transform="translate({x:.1f},0) '
                    f'scale({scale:.6f},-{scale:.6f})" d="{d}"/>'
                )
            advance = hmtx[glyph_name][0]
        else:
            advance = upm // 3
        x += advance * scale
        if i < len(text) - 1:
            x += letter_spacing

    x_start = cx - total_width / 2
    inner = "\n".join(paths)
    return f'  <g transform="translate({x_start:.1f},{cy})" {attrs}>\n{inner}\n  </g>', total_width


# ---------------------------------------------------------------------------
# SVG template — everything except the text layers
# ---------------------------------------------------------------------------
SVG_TEMPLATE = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 400" width="100%%">
  <defs>
    <style>
      @keyframes ghostFloat1 {
        0%%, 100%% { transform: translate(-4px, -4px) skewX(-2deg); opacity: 0.15; }
        50%%       { transform: translate(-8px, 2px) skewX(-3deg); opacity: 0.10; }
      }
      @keyframes ghostFloat2 {
        0%%, 100%% { transform: translate(4px, 4px) skewX(2deg); opacity: 0.12; }
        50%%       { transform: translate(8px, -2px) skewX(3deg); opacity: 0.08; }
      }
      @keyframes flicker {
        0%%, 19%%, 21%%, 23%%, 25%%, 54%%, 56%%, 100%% { opacity: 1; }
        20%%, 24%%, 55%% { opacity: 0.85; }
      }
      @keyframes particleDrift1 {
        0%%   { transform: translate(0,0); opacity: 0; }
        10%%  { opacity: 0.6; } 90%% { opacity: 0.6; }
        100%% { transform: translate(60px,-80px); opacity: 0; }
      }
      @keyframes particleDrift2 {
        0%%   { transform: translate(0,0); opacity: 0; }
        10%%  { opacity: 0.4; } 90%% { opacity: 0.4; }
        100%% { transform: translate(-50px,-60px); opacity: 0; }
      }
      @keyframes particleDrift3 {
        0%%   { transform: translate(0,0); opacity: 0; }
        10%%  { opacity: 0.5; } 90%% { opacity: 0.5; }
        100%% { transform: translate(40px,70px); opacity: 0; }
      }
      @keyframes particleDrift4 {
        0%%   { transform: translate(0,0); opacity: 0; }
        15%%  { opacity: 0.3; } 85%% { opacity: 0.3; }
        100%% { transform: translate(-70px,50px); opacity: 0; }
      }
      @keyframes scanScroll  { 0%% { transform: translateY(0); } 100%% { transform: translateY(8px); } }
      @keyframes tagPulse    { 0%%, 100%% { opacity: 0.5; } 50%% { opacity: 0.8; } }

      .main-text { animation: flicker 8s linear infinite; }
      .ghost1    { animation: ghostFloat1 4s ease-in-out infinite; }
      .ghost2    { animation: ghostFloat2 5s ease-in-out infinite; }
      .tagline   { animation: tagPulse 4s ease-in-out infinite; }
      .scanlines { animation: scanScroll 0.5s linear infinite; }
    </style>

    <linearGradient id="bgGrad" x1="0%%" y1="0%%" x2="100%%" y2="100%%">
      <stop offset="0%%"   style="stop-color:#0d0221"><animate attributeName="stop-color" values="#0d0221;#150050;#3f0071;#000428;#0d0221" dur="12s" repeatCount="indefinite"/></stop>
      <stop offset="50%%"  style="stop-color:#150050"><animate attributeName="stop-color" values="#150050;#610094;#004e92;#0d0221;#150050" dur="12s" repeatCount="indefinite"/></stop>
      <stop offset="100%%" style="stop-color:#000428"><animate attributeName="stop-color" values="#000428;#0d0221;#150050;#610094;#000428" dur="12s" repeatCount="indefinite"/></stop>
    </linearGradient>

    <linearGradient id="textGrad" x1="0%%" y1="0%%" x2="100%%" y2="100%%">
      <stop offset="0%%"><animate attributeName="stop-color" values="#ff00ff;#00ffff;#ffff00;#ff00ff" dur="6s" repeatCount="indefinite"/></stop>
      <stop offset="50%%"><animate attributeName="stop-color" values="#00ffff;#ff6ec7;#ff00ff;#00ffff" dur="6s" repeatCount="indefinite"/></stop>
      <stop offset="100%%"><animate attributeName="stop-color" values="#ffff00;#ff00ff;#00ffff;#ffff00" dur="6s" repeatCount="indefinite"/></stop>
    </linearGradient>

    <filter id="glow" x="-50%%" y="-50%%" width="200%%" height="200%%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="b1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="16" result="b2"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="30" result="b3"/>
      <feMerge><feMergeNode in="b3"/><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowMagenta" x="-50%%" y="-50%%" width="200%%" height="200%%">
      <feGaussianBlur stdDeviation="10"/><feColorMatrix type="matrix" values="1 0 0 0 .3 0 0 0 0 0 0 0 0 0 .3 0 0 0 1 0"/>
    </filter>
    <filter id="glowCyan" x="-50%%" y="-50%%" width="200%%" height="200%%">
      <feGaussianBlur stdDeviation="10"/><feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 .3 0 0 0 0 .3 0 0 0 1 0"/>
    </filter>

    <linearGradient id="dripMagenta" x1="0" y1="0" x2="0" y2="1"><stop offset="0%%" stop-color="#ff00ff" stop-opacity=".7"/><stop offset="100%%" stop-color="#ff00ff" stop-opacity="0"/></linearGradient>
    <linearGradient id="dripCyan"    x1="0" y1="0" x2="0" y2="1"><stop offset="0%%" stop-color="#00ffff" stop-opacity=".6"/><stop offset="100%%" stop-color="#00ffff" stop-opacity="0"/></linearGradient>
    <linearGradient id="dripYellow"  x1="0" y1="0" x2="0" y2="1"><stop offset="0%%" stop-color="#ffff00" stop-opacity=".5"/><stop offset="100%%" stop-color="#ffff00" stop-opacity="0"/></linearGradient>

    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="transparent"/><rect y="2" width="4" height="2" fill="rgba(0,0,0,.12)"/></pattern>
    <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse"><path d="M50 0L0 0 0 50" fill="none" stroke="rgba(0,255,255,.04)" stroke-width=".5"/></pattern>
  </defs>

  <rect width="900" height="400" rx="12" fill="url(#bgGrad)"/>
  <rect width="900" height="400" rx="12" fill="url(#grid)"/>
  <g class="scanlines"><rect width="900" height="420" y="-10" fill="url(#scan)"/></g>

  <circle cx="120" cy="80"  r="1.5" fill="#ff00ff" style="animation:particleDrift1 7s linear infinite"/>
  <circle cx="250" cy="320" r="1"   fill="#00ffff" style="animation:particleDrift2 9s linear infinite;animation-delay:1s"/>
  <circle cx="400" cy="60"  r="2"   fill="#ffff00" style="animation:particleDrift3 6s linear infinite;animation-delay:.5s"/>
  <circle cx="600" cy="340" r="1.5" fill="#ff6ec7" style="animation:particleDrift4 8s linear infinite;animation-delay:2s"/>
  <circle cx="750" cy="100" r="1"   fill="#00ffff" style="animation:particleDrift1 10s linear infinite;animation-delay:3s"/>
  <circle cx="800" cy="280" r="2"   fill="#ff00ff" style="animation:particleDrift2 7s linear infinite;animation-delay:4s"/>
  <circle cx="50"  cy="200" r="1.5" fill="#ffff00" style="animation:particleDrift3 9s linear infinite;animation-delay:1.5s"/>
  <circle cx="500" cy="350" r="1"   fill="#ff6ec7" style="animation:particleDrift4 6s linear infinite;animation-delay:2.5s"/>
  <circle cx="320" cy="150" r="1.8" fill="#00ffff" style="animation:particleDrift1 8s linear infinite;animation-delay:.8s"/>
  <circle cx="680" cy="200" r="1.2" fill="#ff00ff" style="animation:particleDrift2 11s linear infinite;animation-delay:3.5s"/>
  <circle cx="150" cy="300" r="1.5" fill="#ffff00" style="animation:particleDrift3 7s linear infinite;animation-delay:5s"/>
  <circle cx="850" cy="150" r="1"   fill="#00ffff" style="animation:particleDrift4 9s linear infinite;animation-delay:1.2s"/>

  <g stroke="rgba(0,255,255,.25)" stroke-width="2" fill="none">
    <path d="M30,55 L30,30 L55,30"/><path d="M870,55 L870,30 L845,30"/>
    <path d="M30,345 L30,370 L55,370"/><path d="M870,345 L870,370 L845,370"/>
  </g>

%(ghost1)s
%(ghost2)s
%(main)s
%(drips)s
%(tagline)s
</svg>
"""


def build_drips(main_width):
    ox = 450 - main_width / 2
    configs = [
        ("dripMagenta", 240, 5, "3.5s", None),
        ("dripCyan",    238, 4, "4s",   "1s"),
        ("dripYellow",  242, 5, "3s",   "2s"),
        ("dripMagenta", 236, 4, "3.8s", "0.5s"),
    ]
    parts = []
    for i, (fid, y, w, dur, begin) in enumerate(configs):
        x = ox + main_width * [0.05, 0.35, 0.65, 0.92][i]
        b = f' begin="{begin}"' if begin else ""
        parts.append(
            f'  <rect x="{x:.0f}" y="{y}" width="{w}" rx="{w/2}" fill="url(#{fid})">\n'
            f'    <animate attributeName="height" values="0;50;60;0" dur="{dur}" repeatCount="indefinite"{b}/>\n'
            f'    <animate attributeName="opacity" values=".7;.7;.4;0" dur="{dur}" repeatCount="indefinite"{b}/>\n'
            f'  </rect>'
        )
    return "\n".join(parts)


def build_banner(main_font, tag_font, text, tagline, out_path):
    ghost1, _ = text_to_path_group(
        main_font, text, 120, 450, 225, letter_spacing=6,
        attrs='class="ghost1" fill="#ff00ff" filter="url(#glowMagenta)" opacity="0.15"')
    ghost2, _ = text_to_path_group(
        main_font, text, 120, 450, 225, letter_spacing=6,
        attrs='class="ghost2" fill="#00ffff" filter="url(#glowCyan)" opacity="0.12"')
    main, mw = text_to_path_group(
        main_font, text, 120, 450, 225, letter_spacing=6,
        attrs='class="main-text" fill="url(#textGrad)" filter="url(#glow)"')
    tag, _ = text_to_path_group(
        tag_font, tagline, 14, 450, 320, letter_spacing=1,
        attrs='class="tagline" fill="rgba(0,255,255,0.6)"')

    svg = SVG_TEMPLATE % {
        "ghost1": ghost1, "ghost2": ghost2, "main": main,
        "drips": build_drips(mw), "tagline": tag,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  -> {out_path} ({os.path.getsize(out_path) // 1024}KB)")


def main():
    p = argparse.ArgumentParser(
        description="Generate cyberpunk SVG banners with text as vector paths.",
        epilog="Fonts live in ./fonts/. Outputs are GitHub-safe (no font deps).",
    )
    p.add_argument("--text", default=None, help="Main text (default: builds both 'primeinc' and 'WP')")
    p.add_argument("--tagline", default="VINCIT OMNIA VERITAS", help="Tagline below main text")
    p.add_argument("--out", default=None, help="Output SVG path")
    p.add_argument("--main-font", default=DEFAULT_MAIN_FONT, help="TTF for main text")
    p.add_argument("--tag-font", default=DEFAULT_TAG_FONT, help="TTF for tagline")
    args = p.parse_args()

    if args.text:
        out = args.out or f"banner-{args.text.lower().replace(' ', '-')}.svg"
        print(f"Building: \"{args.text}\" / \"{args.tagline}\"")
        build_banner(args.main_font, args.tag_font, args.text, args.tagline, out)
    else:
        print("Building defaults...")
        build_banner(args.main_font, args.tag_font, "primeinc", args.tagline, "banner-primeinc.svg")
        build_banner(args.main_font, args.tag_font, "WP", args.tagline, "banner.svg")

    print("Done!")


if __name__ == "__main__":
    main()
