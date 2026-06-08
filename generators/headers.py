def generate_header(name, filename, svg_path, output_dir=".", theme="dark"):
    import os
    if theme == "light":
        grad_start = "#0366d6"
        grad_end = "#6f42c1"
        text_color = "#0366d6"
    else:
        grad_start = "#7aa2f7"
        grad_end = "#bb9af3"
        text_color = "#7aa2f7"

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="50" fill="none">
  <defs>
    <linearGradient id="header-grad" x1="0" y1="0" x2="200" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{grad_start}"/>
      <stop offset="100%" stop-color="{grad_end}"/>
    </linearGradient>
  </defs>
  
  <!-- Icon -->
  <g transform="translate(10, 10)">
    {svg_path}
  </g>
  
  <!-- Text -->
  <text x="45" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="19" font-weight="bold" fill="{text_color}" letter-spacing="0.5">{name}</text>
  
  <!-- Underline -->
  <rect x="45" y="36" width="60" height="3" rx="1.5" fill="url(#header-grad)"/>
</svg>
"""
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")
