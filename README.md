<p align="center">
  <img src="./banner-primeinc.svg" alt="primeinc" width="100%"/>
</p>

## Rebuilding the banners

```sh
pip install fonttools    # only dependency
python build_banner.py   # rebuilds banner.svg + banner-primeinc.svg
```

Custom text:
```sh
python build_banner.py --text "WHATEVER" --tagline "YOUR SUBTITLE" --out custom.svg
```

## Why things are the way they are

**Why SVG paths instead of fonts?**
GitHub's markdown renderer proxies SVGs through `camo.githubusercontent.com` which strips
`@font-face`, `@import`, and `data:` URIs for security. Embedded base64 fonts (~130KB each)
also get stripped. Converting text to `<path>` elements is the only way to guarantee the
exact font renders on GitHub. The tradeoff is you need to re-run `build_banner.py` to change text.

**Why `build_banner.py` needs TTF files?**
`fonttools` reads the glyph outlines from TTF fonts and converts them to SVG path commands.
The fonts live in `fonts/` and are NOT embedded in the output — they're only needed at build time.
Permanent Marker (graffiti style) is for the main text, Orbitron (techy/geometric) is for the tagline.

**Why not just use an image/PNG?**
SVGs with CSS animations render natively in browsers. The gradient background shifts, the text
flickers, ghost layers float, particles drift, and paint drips animate — all without JavaScript.
A PNG would be static. A GIF would be huge and lossy.

**Why `wp-gradient.html` exists separately?**
That's the full interactive version with mouse-follow glow, 3D parallax tilt, and a JS particle
system. The SVGs are a GitHub-safe subset of that. The HTML is for local use / showing off.

## Files

```
README.md              ← this file (GitHub profile page)
banner-primeinc.svg    ← active profile banner (paths, no font deps)
banner.svg             ← WP initials variant
build_banner.py        ← regenerate SVGs from any text + tagline
fonts/                 ← source TTFs (build-time only, not in output)
  PermanentMarker.ttf
  Orbitron.ttf
wp-gradient.html       ← full interactive version (HTML/CSS/JS)
```
