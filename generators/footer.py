import os

def generate_footer(output_dir=".", theme="dark"):
    if theme == "light":
        bg         = "#f6f8fa"
        stroke     = "#d1d5db"
        heart_col  = "#e06c75"
        name_col   = "#0366d6"
        text_col   = "#586069"
        dot_col    = "#d1d5db"
        link_col   = "#0366d6"
        glow       = "rgba(224,108,117,0.15)"
    else:
        bg         = "#1a1b26"
        stroke     = "#24283b"
        heart_col  = "#f7768e"
        name_col   = "#7aa2f7"
        text_col   = "#a9b1d6"
        dot_col    = "#3b4261"
        link_col   = "#7dcfff"
        glow       = "rgba(247,118,142,0.18)"

    # Heart icon path (16×16 viewBox)
    heart_icon = f'<path d="M8 14s-6-3.8-6-8a4 4 0 0 1 6-3.44A4 4 0 0 1 14 6c0 4.2-6 8-6 8z" fill="{heart_col}" stroke="none"/>'

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="750" height="52" viewBox="0 0 750 52" fill="none">
  <defs>
    <radialGradient id="heart-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{glow}"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
    <filter id="subtle-shadow" x="-2%" y="-5%" width="104%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000000" flood-opacity="{"0.08" if theme == "light" else "0.35"}"/>
    </filter>
  </defs>

  <!-- Card background -->
  <rect x="1" y="1" width="748" height="50" rx="10"
        fill="{bg}" stroke="{stroke}" stroke-width="1" filter="url(#subtle-shadow)"/>

  <!-- Subtle top divider line accent -->
  <line x1="40" y1="1" x2="710" y2="1" stroke="{heart_col}" stroke-width="1.5" stroke-opacity="0.35"/>

  <!-- Heart glow halo -->
  <ellipse cx="375" cy="26" rx="28" ry="18" fill="url(#heart-glow)"/>

  <!-- "Built with" -->
  <text x="233" y="31"
        font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif"
        font-size="13" font-weight="500" fill="{text_col}" text-anchor="middle">Built with</text>

  <!-- Heart icon centred -->
  <g transform="translate(259, 18) scale(0.9375)">
    {heart_icon}
  </g>

  <!-- "by" -->
  <text x="286" y="31"
        font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif"
        font-size="13" font-weight="500" fill="{text_col}">by</text>

  <!-- Author name -->
  <text x="305" y="31"
        font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif"
        font-size="13" font-weight="700" fill="{name_col}">Euler Rap</text>

  <!-- (connectedGraph) -->
  <text x="385" y="31"
        font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif"
        font-size="12" font-weight="400" fill="{text_col}">(connectedGraph)</text>

  <!-- Bullet separator -->
  <circle cx="487" cy="26" r="2.5" fill="{dot_col}"/>

  <!-- Link -->
  <text x="499" y="31"
        font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif"
        font-size="13" font-weight="600" fill="{link_col}">6767.chat</text>

  <!-- Underline for link -->
  <line x1="499" y1="33" x2="551" y2="33" stroke="{link_col}" stroke-width="1" stroke-opacity="0.5"/>
</svg>"""

    filepath = os.path.join(output_dir, "footer.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")
