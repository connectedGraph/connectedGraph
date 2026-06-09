from generators import load_icon_svg, clear_collected_defs, get_collected_defs
import os, math

DEFAULT_CATEGORIES = [
    {"title": "FRONTEND", "items": [
        {"slug": "nextjs",     "label": "Next.js",    "subfolder": "code"},
        {"slug": "react",      "label": "React",      "subfolder": "code"},
        {"slug": "javascript", "label": "JavaScript", "subfolder": "code"},
        {"slug": "html5",      "label": "HTML5",      "subfolder": "code"},
        {"slug": "css3",       "label": "CSS3",       "subfolder": "code"},
    ]},
    {"title": "BACKEND & DB", "items": [
        {"slug": "nodejs",     "label": "Node.js",    "subfolder": "code"},
        {"slug": "python",     "label": "Python",     "subfolder": "code"},
        {"slug": "express",    "label": "Express",    "subfolder": "code"},
        {"slug": "pgsql",      "label": "PostgreSQL", "subfolder": "code"},
    ]},
    {"title": "AI & DEV TOOLS", "items": [
        {"slug": "claudecode",   "label": "Claude Code",  "subfolder": "devtools"},
        {"slug": "codex",        "label": "Codex",        "subfolder": "devtools"},
        {"slug": "claude-api",   "label": "Claude API",   "subfolder": "devtools"},
        {"slug": "deepseek-api", "label": "Deepseek API", "subfolder": "devtools"},
    ]},
]

# XML escape for text-content fields
def _esc(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))

def generate_tech_stack(output_dir=".", theme="dark", **kwargs):
    clear_collected_defs()

    categories = kwargs.get("categories") or DEFAULT_CATEGORIES
    # Normalise: drop empty categories
    categories = [c for c in categories if c.get("items")]
    if not categories:
        categories = DEFAULT_CATEGORIES

    if theme == "light":
        card_bg = "#f6f8fa"; card_stroke = "#d1d5db"; shadow_opacity = "0.12"
        pill_fill = "#ffffff"; pill_stroke = "#d1d5db"
        text_color = "#24292e"; title_color = "#0366d6"
        grad_start = "#0366d6"; grad_end = "#6f42c1"
    else:
        card_bg = "#1a1b26"; card_stroke = "#24283b"; shadow_opacity = "0.5"
        pill_fill = "#16161e"; pill_stroke = "#24283b"
        text_color = "#c0caf5"; title_color = "#7aa2f7"
        grad_start = "#7aa2f7"; grad_end = "#bb9af3"

    # Layout: up to 3 columns, 2 pills per row inside a column
    n_cols = min(len(categories), 3)
    if len(categories) > 3:
        # Force everything into 3 columns (truncate)
        categories = categories[:3]
        n_cols = 3

    PILL_W = 97; PILL_H = 26; PILL_GAP_X = 8; PILL_GAP_Y = 7
    COL_INNER_W = PILL_W * 2 + PILL_GAP_X       # 202
    COL_GAP = 33
    SVG_W = 750
    SIDE_PAD = (SVG_W - (n_cols * COL_INNER_W + (n_cols - 1) * COL_GAP)) / 2
    HEADER_Y = 45
    PILL_START_Y = 65

    max_rows = max(math.ceil(len(c["items"]) / 2) for c in categories)
    body_h = (PILL_H + PILL_GAP_Y) * max_rows
    SVG_H = HEADER_Y + 20 + body_h + 30
    CARD_X = 15
    CARD_W = SVG_W - 30
    CARD_Y = 15
    CARD_H = SVG_H - 30

    def pill(x, y, name, icon_svg):
        return f"""    <g transform="translate({x:.1f}, {y:.1f})">
      <rect x="0.5" y="0.5" width="{PILL_W}" height="{PILL_H - 1}" rx="13" fill="{pill_fill}" stroke="{pill_stroke}" stroke-width="1"/>
      <g transform="translate(8, 5)">
        {icon_svg}
      </g>
      <text x="28" y="17" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="10.5" font-weight="600" fill="{text_color}">{_esc(name)}</text>
    </g>"""

    def render_icon(item):
        slug = item.get("slug", "")
        sub = item.get("subfolder", "code")
        fallback = '<rect width="16" height="16" rx="3" fill="#666666"/>'
        return load_icon_svg(slug, fallback, sub, theme=theme)

    # Build columns
    col_blocks = []
    for ci, cat in enumerate(categories):
        col_x = SIDE_PAD + ci * (COL_INNER_W + COL_GAP)
        title = _esc(cat.get("title", "")[:18])
        items = cat["items"][:8]   # cap 8 per column

        # Pills
        pills_xml = []
        for idx, item in enumerate(items):
            row, col = divmod(idx, 2)
            x = col_x + col * (PILL_W + PILL_GAP_X)
            y = PILL_START_Y + row * (PILL_H + PILL_GAP_Y)
            pills_xml.append(pill(x, y, item.get("label", item.get("slug", "?")), render_icon(item)))

        # Header
        header = f"""  <text x="{col_x:.1f}" y="{HEADER_Y}" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="12" font-weight="800" fill="{title_color}" letter-spacing="1">{title}</text>
  <rect x="{col_x:.1f}" y="{HEADER_Y + 7}" width="45" height="2" rx="1" fill="url(#header-grad)"/>"""

        col_blocks.append(header + "\n" + "".join(pills_xml))

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}" fill="none">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="{shadow_opacity}"/>
    </filter>
    <linearGradient id="header-grad" x1="0" y1="0" x2="200" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{grad_start}"/>
      <stop offset="100%" stop-color="{grad_end}"/>
    </linearGradient>
    {get_collected_defs()}
  </defs>

  <rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="12" fill="{card_bg}" stroke="{card_stroke}" stroke-width="1.5" filter="url(#shadow)"/>

{chr(10).join(col_blocks)}
</svg>"""

    filepath = os.path.join(output_dir, "tech_stack.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")
