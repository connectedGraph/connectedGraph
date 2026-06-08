import os

def generate_typewriter():
    content = """<svg xmlns="http://www.w3.org/2000/svg" width="750" height="315" viewBox="0 0 750 315" fill="none">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.55"/>
    </filter>
    
    <clipPath id="clip1">
      <rect x="105" y="48" height="20" class="clip-rect-1"/>
    </clipPath>
    
    <clipPath id="clip2">
      <rect x="105" y="94" height="20" class="clip-rect-2"/>
    </clipPath>
    
    <clipPath id="clip3">
      <rect x="105" y="163" height="20" class="clip-rect-3"/>
    </clipPath>
    
    <clipPath id="clip4">
      <rect x="105" y="209" height="20" class="clip-rect-4"/>
    </clipPath>
  </defs>

  <style>
    .terminal-bg {
      fill: #1a1b26;
      stroke: #24283b;
      stroke-width: 1.5px;
    }
    .btn-red { fill: #f7768e; }
    .btn-yellow { fill: #e0af68; }
    .btn-green { fill: #9ece6a; }
    
    .title-text {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 13px;
      fill: #565f89;
      font-weight: 500;
    }
    
    .code-text {
      font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
      font-size: 14px;
      font-weight: bold;
    }
    
    .prompt {
      fill: #7dcfff;
    }
    
    .command {
      fill: #bb9af3;
    }
    
    .flag {
      fill: #ff9e64;
    }
    
    .string {
      fill: #9ece6a;
    }
    
    .output {
      font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
      font-size: 13.5px;
      fill: #a9b1d6;
    }
    
    .cursor {
      fill: #787c99;
    }
    
    /* Clip Rects CSS Animations (locks typing to CSS clock) */
    .clip-rect-1 {
      animation: type1-anim 12s infinite linear;
    }
    .clip-rect-2 {
      animation: type2-anim 12s infinite linear;
    }
    .clip-rect-3 {
      animation: type3-anim 12s infinite linear;
    }
    .clip-rect-4 {
      animation: type4-anim 12s infinite linear;
    }
    
    @keyframes type1-anim {
      0%, 4.17% { width: 0; }
      15.0%, 100% { width: 230px; }
    }
    @keyframes type2-anim {
      0%, 20.83% { width: 0; }
      29.17%, 100% { width: 105px; }
    }
    @keyframes type3-anim {
      0%, 37.5% { width: 0; }
      54.17%, 100% { width: 335px; }
    }
    @keyframes type4-anim {
      0%, 60.83% { width: 0; }
      69.17%, 100% { width: 105px; }
    }
    
    /* Unified Cursors Animations (Combines movement and visibility to prevent drift) */
    .cursor1 {
      animation: cur1-anim 12s infinite linear;
    }
    .cursor2 {
      animation: cur2-anim 12s infinite linear;
    }
    .cursor3 {
      animation: cur3-anim 12s infinite linear;
    }
    .cursor4 {
      animation: cur4-anim 12s infinite linear;
    }
    
    @keyframes cur1-anim {
      0%, 4.16% { transform: translateX(0); opacity: 0; }
      4.17% { transform: translateX(0); opacity: 1; }
      15.0% { transform: translateX(230px); opacity: 1; }
      15.5% { transform: translateX(230px); opacity: 0; }
      16.0% { transform: translateX(230px); opacity: 1; }
      16.5% { transform: translateX(230px); opacity: 0; }
      16.67%, 100% { transform: translateX(230px); opacity: 0; }
    }
    
    @keyframes cur2-anim {
      0%, 19.17% { transform: translateX(0); opacity: 0; }
      19.18%, 20.82% { transform: translateX(0); opacity: 1; }
      20.83% { transform: translateX(0); opacity: 1; }
      29.17% { transform: translateX(105px); opacity: 1; }
      29.5% { transform: translateX(105px); opacity: 0; }
      30.0% { transform: translateX(105px); opacity: 1; }
      30.5% { transform: translateX(105px); opacity: 0; }
      30.83%, 100% { transform: translateX(105px); opacity: 0; }
    }
    
    @keyframes cur3-anim {
      0%, 35.0% { transform: translateX(0); opacity: 0; }
      35.01%, 37.49% { transform: translateX(0); opacity: 1; }
      37.5% { transform: translateX(0); opacity: 1; }
      54.17% { transform: translateX(335px); opacity: 1; }
      54.5% { transform: translateX(335px); opacity: 0; }
      55.0% { transform: translateX(335px); opacity: 1; }
      55.5% { transform: translateX(335px); opacity: 0; }
      55.83%, 100% { transform: translateX(335px); opacity: 0; }
    }
    
    @keyframes cur4-anim {
      0%, 58.33% { transform: translateX(0); opacity: 0; }
      58.34%, 60.82% { transform: translateX(0); opacity: 1; }
      60.83% { transform: translateX(0); opacity: 1; }
      69.17% { transform: translateX(105px); opacity: 1; }
      72.0% { transform: translateX(105px); opacity: 0; }
      75.0% { transform: translateX(105px); opacity: 1; }
      78.0% { transform: translateX(105px); opacity: 0; }
      81.0% { transform: translateX(105px); opacity: 1; }
      84.0% { transform: translateX(105px); opacity: 0; }
      87.0% { transform: translateX(105px); opacity: 1; }
      90.0% { transform: translateX(105px); opacity: 0; }
      93.0% { transform: translateX(105px); opacity: 1; }
      96.0% { transform: translateX(105px); opacity: 0; }
      99.0%, 100% { transform: translateX(105px); opacity: 1; }
    }
    
    /* Outputs Animations */
    .op1 { animation: op1-anim 12s infinite; }
    .op2 { animation: op2-anim 12s infinite; }
    .op3 { animation: op3-anim 12s infinite; }
    .op4 { animation: op4-anim 12s infinite; }
    .op5 { animation: op5-anim 12s infinite; }
    
    .pr2 { animation: pr2-anim 12s infinite; }
    .pr3 { animation: pr3-anim 12s infinite; }
    .pr4 { animation: pr4-anim 12s infinite; }
    
    @keyframes op1-anim {
      0%, 16.67% { opacity: 0; }
      16.68%, 100% { opacity: 1; }
    }
    @keyframes pr2-anim {
      0%, 19.17% { opacity: 0; }
      19.18%, 100% { opacity: 1; }
    }
    @keyframes op2-anim {
      0%, 30.83% { opacity: 0; }
      30.84%, 100% { opacity: 1; }
    }
    @keyframes op3-anim {
      0%, 32.5% { opacity: 0; }
      32.51%, 100% { opacity: 1; }
    }
    @keyframes pr3-anim {
      0%, 35.0% { opacity: 0; }
      35.01%, 100% { opacity: 1; }
    }
    @keyframes op4-anim {
      0%, 55.83% { opacity: 0; }
      55.84%, 100% { opacity: 1; }
    }
    @keyframes pr4-anim {
      0%, 58.33% { opacity: 0; }
      58.34%, 100% { opacity: 1; }
    }
    @keyframes op5-anim {
      0%, 70.83% { opacity: 0; }
      70.84%, 100% { opacity: 1; }
    }
  </style>

  <rect x="15" y="15" width="720" height="285" rx="12" class="terminal-bg" filter="url(#shadow)"/>
  
  <!-- Window Header Buttons -->
  <circle cx="40" cy="35" r="6" class="btn-red"/>
  <circle cx="60" cy="35" r="6" class="btn-yellow"/>
  <circle cx="80" cy="35" r="6" class="btn-green"/>
  <text x="375" y="40" class="title-text" text-anchor="middle">euler@localhost:~</text>
  
  <!-- Line 1: greet command -->
  <text x="35" y="62" class="code-text prompt">euler~% </text>
  <text x="105" y="62" class="code-text command" clip-path="url(#clip1)">greet <tspan class="flag">--role</tspan> <tspan class="string">"CS Freshman"</tspan></text>
  <rect x="105" y="48" width="8" height="16" class="cursor cursor1"/>
  
  <!-- Line 2: greet output -->
  <text x="35" y="85" class="output op1">Hi, CS Freshman here! Nice to meet you. 👋</text>
  
  <!-- Line 3: show-profile command -->
  <text x="35" y="108" class="code-text prompt pr2">euler~% </text>
  <text x="105" y="108" class="code-text command" clip-path="url(#clip2)">show-profile</text>
  <rect x="105" y="94" width="8" height="16" class="cursor cursor2"/>
  
  <!-- Line 4 & 5: show-profile outputs -->
  <text x="35" y="131" class="output op2">Focus:  Full-Stack AI Applications (Vertical AIED)</text>
  <text x="35" y="154" class="output op3">Status: yolo ✨</text>
  
  <!-- Line 6: claude command -->
  <text x="35" y="177" class="code-text prompt pr3">euler~% </text>
  <text x="105" y="177" class="code-text command" clip-path="url(#clip3)">claude <tspan class="flag">--dangerously-skip-permissions</tspan></text>
  <rect x="105" y="163" width="8" height="16" class="cursor cursor3"/>
  
  <!-- Line 7: claude output -->
  <text x="35" y="200" class="output op4" fill="#bb9af3">🔓 [Danger Mode] Skipping permissions... Let's build!</text>
  
  <!-- Line 8: codex command -->
  <text x="35" y="223" class="code-text prompt pr4">euler~% </text>
  <text x="105" y="223" class="code-text command" clip-path="url(#clip4)">codex <tspan class="flag">--yolo</tspan></text>
  <rect x="105" y="209" width="8" height="16" class="cursor cursor4"/>
  
  <!-- Line 9: codex output -->
  <text x="35" y="246" class="output op5" fill="#e0af68">⚡ [YOLO Mode] Code generation full speed ahead!</text>
</svg>
"""
    with open("typewriter.svg", "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated typewriter.svg")

def generate_header(name, filename, svg_path):
    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="50" fill="none">
  <defs>
    <linearGradient id="header-grad" x1="0" y1="0" x2="200" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7aa2f7"/>
      <stop offset="100%" stop-color="#bb9af3"/>
    </linearGradient>
  </defs>
  
  <!-- Icon -->
  <g transform="translate(10, 10)">
    {svg_path}
  </g>
  
  <!-- Text -->
  <text x="45" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="19" font-weight="bold" fill="#7aa2f7" letter-spacing="0.5">{name}</text>
  
  <!-- Underline -->
  <rect x="45" y="36" width="60" height="3" rx="1.5" fill="url(#header-grad)"/>
</svg>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filename}")

def generate_social_badges():
    # Globe icon (stroke-based)
    globe_path = '<circle cx="8" cy="8" r="6.5"/><path d="M1.5 8h13M8 1.5c1.5 2 1.5 11 0 13M8 1.5c-1.5 2-1.5 11 0 13"/>'
    # Pen/Edit icon (stroke-based)
    pen_path = '<path d="M11.5 1.5a1.5 1.5 0 1 1 2 2L4.5 12.5 1.5 13.5l1-3zM10 3l3 3"/>'
    # GitHub icon (fill-based)
    github_path = '<path d="M8 .2C3.6.2 0 3.8 0 8.2c0 3.5 2.3 6.5 5.5 7.6.4.1.5-.2.5-.4v-1.4c-2.2.5-2.7-1.1-2.7-1.1-.4-.9-.9-1.2-.9-1.2-.7-.5.1-.5.1-.5.8.1 1.2.8 1.2.8.7 1.2 1.9.9 2.3.7.1-.5.3-.9.5-1.1-1.8-.2-3.6-.9-3.6-4 0-.9.3-1.6.8-2.2-.1-.2-.4-1 .1-2.1 0 0 .7-.2 2.2.8a7.8 7.8 0 0 1 4.1 0c1.5-1 2.2-.8 2.2-.8.5 1.1.2 1.9.1 2.1.5.6.8 1.3.8 2.2 0 3.1-1.9 3.8-3.7 4 .3.3.5.8.5 1.6V15c0 .2.1.5.6.4C13.7 14.7 16 11.7 16 8.2 16 3.8 12.4.2 8 .2z" fill="{color}" stroke="none"/>'
    # X icon (fill-based)
    x_path = '<path d="M1 1l5.5 7.3L1 15h2.5L9 9.5l3.5 4.5H15l-6-8L14 1h-2.5L7 6.5 3.5 1H1z" fill="{color}" stroke="none"/>'
    # Chat bubble icon (stroke-based)
    zhihu_path = '<path d="M2.5 1.5h11c.6 0 1 .4 1 1v8c0 .6-.4 1-1 1H7l-4 3v-3c-.6 0-1.1-.4-1.1-1v-8c0-.6.5-1 1.1-1z" stroke-width="1.5"/><path d="M5 4h6M5 7h4" stroke-width="1.5"/>'

    badges = [
        ("badge_website.svg", 108, globe_path, "#7dcfff", "6767.chat", False),
        ("badge_blog.svg", 72, pen_path, "#bb9af3", "Blog", False),
        ("badge_github.svg", 88, github_path, "#a9b1d6", "GitHub", True),
        ("badge_x.svg", 55, x_path, "#ffffff", "X", True),
        ("badge_zhihu.svg", 80, zhihu_path, "#7aa2f7", "Zhihu", False)
    ]

    for filename, width, icon_svg, color, label, is_fill in badges:
        if is_fill:
            icon_content = icon_svg.replace("{color}", color)
        else:
            icon_content = f'<g stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none">{icon_svg}</g>'
        
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" fill="none">
  <rect x="0.5" y="0.5" width="{width - 1}" height="27" rx="14" fill="#16161e" stroke="#24283b" stroke-width="1"/>
  <g transform="translate(8, 6)">
    {icon_content}
  </g>
  <text x="30" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="12" font-weight="600" fill="#c0caf5">{label}</text>
</svg>"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Generated {filename}")

def main():
    # Icons
    tech_path = '<path d="M16 18l6-6-6-6M8 6L2 12l6 6" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
    projects_path = '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" stroke="url(#header-grad)" stroke-width="2" stroke-linecap="round" fill="none"/><path d="M12 11l2 2-2 2" stroke="url(#header-grad)" stroke-width="2" stroke-linecap="round" fill="none"/>'
    apis_path = '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" stroke="url(#header-grad)" stroke-width="2" stroke-linecap="round" fill="none"/>'
    stats_path = '<path d="M18 20V10M12 20V4M6 20v-6" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
    roadmap_path = '<path d="M9 6h11M9 12h11M9 18h11M5 6v.01M5 12v.01M5 18v.01" stroke="url(#header-grad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
    ask_path = '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="url(#header-grad)" stroke-width="2" stroke-linecap="round" fill="none"/>'

    generate_typewriter()
    generate_header("Tech Stack", "header_tech_stack.svg", tech_path)
    generate_header("Projects", "header_projects.svg", projects_path)
    generate_header("Public APIs", "header_public_apis.svg", apis_path)
    generate_header("GitHub Stats", "header_stats.svg", stats_path)
    generate_header("Roadmap", "header_roadmap.svg", roadmap_path)
    generate_header("Ask Me", "header_ask_me.svg", ask_path)
    generate_social_badges()

if __name__ == "__main__":
    main()
