import os

def generate_ask_me_badge(output_dir=".", theme="dark"):
    if theme == "light":
        bg           = "#ffffff"
        stroke       = "#d1d5db"
        pill_bg      = "#f3f0ff"
        pill_stroke  = "#7c3aed"
        icon_color   = "#7c3aed"
        label_color  = "#6d28d9"
        arrow_color  = "#7c3aed"
        url_color    = "#0366d6"
        shadow_op    = "0.08"
    else:
        bg           = "#1a1b26"
        stroke       = "#24283b"
        pill_bg      = "#1e1a2e"
        pill_stroke  = "#9d7ee8"
        icon_color   = "#bb9af3"
        label_color  = "#c0caf5"
        arrow_color  = "#9d7ee8"
        url_color    = "#7dcfff"
        shadow_op    = "0.4"

    # Robot / Claude icon (simplified face outline, 20×20)
    robot_icon = f"""
    <rect x="2" y="5" width="16" height="11" rx="3" stroke="{icon_color}" stroke-width="1.6" fill="none"/>
    <circle cx="7.5" cy="10.5" r="1.5" fill="{icon_color}"/>
    <circle cx="12.5" cy="10.5" r="1.5" fill="{icon_color}"/>
    <path d="M7.5 13.5 Q10 15 12.5 13.5" stroke="{icon_color}" stroke-width="1.4" stroke-linecap="round" fill="none"/>
    <line x1="10" y1="2" x2="10" y2="5" stroke="{icon_color}" stroke-width="1.6" stroke-linecap="round"/>
    <circle cx="10" cy="1.5" r="1" fill="{icon_color}"/>
    <line x1="0" y1="9" x2="2" y2="9" stroke="{icon_color}" stroke-width="1.4" stroke-linecap="round"/>
    <line x1="18" y1="9" x2="20" y2="9" stroke="{icon_color}" stroke-width="1.4" stroke-linecap="round"/>"""

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="340" height="52" viewBox="0 0 340 52" fill="none">
  <defs>
    <filter id="badge-shadow" x="-3%" y="-5%" width="106%" height="130%">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#000000" flood-opacity="{shadow_op}"/>
    </filter>
    <linearGradient id="pill-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{"#7c3aed" if theme == "light" else "#6e40c9"}"/>
      <stop offset="100%" stop-color="{"#9d7ee8" if theme == "light" else "#9d7ee8"}"/>
    </linearGradient>
  </defs>

  <!-- Outer card -->
  <rect x="1" y="1" width="338" height="50" rx="12"
        fill="{bg}" stroke="{stroke}" stroke-width="1" filter="url(#badge-shadow)"/>

  <!-- Coloured pill / CTA area -->
  <rect x="12" y="10" width="316" height="32" rx="16"
        fill="{pill_bg}" stroke="{pill_stroke}" stroke-width="1.5"/>

  <!-- Robot icon -->
  <g transform="translate(22, 16)">
    {robot_icon}
  </g>

  <!-- "🤖 Ask Me via Claude" label -->
  <text x="53" y="30"
        font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif"
        font-size="13" font-weight="700" fill="{label_color}">Ask Me via Claude</text>

  <!-- Separator -->
  <line x1="197" y1="18" x2="197" y2="34" stroke="{pill_stroke}" stroke-width="1" stroke-opacity="0.4"/>

  <!-- URL text -->
  <text x="210" y="30"
        font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif"
        font-size="11.5" font-weight="600" fill="{url_color}">6767.chat/#about</text>

  <!-- Arrow -->
  <text x="313" y="30"
        font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif"
        font-size="13" font-weight="700" fill="{arrow_color}">↗</text>
</svg>"""

    filepath = os.path.join(output_dir, "ask_me_badge.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")
