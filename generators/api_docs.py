import os

def generate_api_docs(output_dir=".", theme="dark"):
    if theme == "light":
        card_bg = "#f6f8fa"
        card_stroke = "#d1d5db"
        shadow_opacity = "0.12"
        title_color = "#24292e"
        desc_color = "#586069"
        icon_color = "#0366d6"
        icon_bg = "#e1ecf8"
        btn_bg = "#ffffff"
        btn_stroke = "#0366d6"
        btn_text = "#0366d6"
    else:
        card_bg = "#1a1b26"
        card_stroke = "#24283b"
        shadow_opacity = "0.5"
        title_color = "#c0caf5"
        desc_color = "#a9b1d6"
        icon_color = "#7dcfff"
        icon_bg = "#16161e"
        btn_bg = "#16161e"
        btn_stroke = "#7aa2f7"
        btn_text = "#7dcfff"

    # API Document Icon (book with code chevron)
    icon_path = f"""
    <rect x="0" y="0" width="40" height="40" rx="10" fill="{icon_bg}"/>
    <g transform="translate(10, 10)" stroke="{icon_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
      <path d="M9 7l3 3-3 3"/>
    </g>
    """

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="750" height="110" viewBox="0 0 750 110" fill="none">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="{shadow_opacity}"/>
    </filter>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="720" height="80" rx="12" fill="{card_bg}" stroke="{card_stroke}" stroke-width="1.5" filter="url(#shadow)"/>

  <!-- Icon & Text Group -->
  <g transform="translate(35, 35)">
    {icon_path}
  </g>

  <!-- Left Text -->
  <text x="90" y="52" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="14" font-weight="bold" fill="{title_color}">Interactive API Documentation</text>
  <text x="90" y="70" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="11" fill="{desc_color}">Explore endpoints, schemas, parameters, and live try-outs</text>

  <!-- Right CTA Button -->
  <g transform="translate(525, 38)">
    <rect x="0" y="0" width="190" height="34" rx="17" fill="{btn_bg}" stroke="{btn_stroke}" stroke-width="1.5"/>
    <text x="95" y="21" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="11.5" font-weight="bold" fill="{btn_text}" text-anchor="middle">Explore API Docs ↗</text>
  </g>
</svg>
"""

    filepath = os.path.join(output_dir, "api_docs.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")
