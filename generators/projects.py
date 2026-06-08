def generate_projects():
    projects = [
        {
            "name": "Zhihu Immersive Reader",
            "url": "https://6767.chat/zhihu-immersive-reader/",
            "status": "Live",
            "status_bg": "#132f22",
            "status_fg": "#22c55e",
            "desc": "Immersive reading script for Zhihu, featuring ad-blocking, AI summaries, and Markdown exports."
        },
        {
            "name": "Sanguosha Voice & Lines",
            "url": "https://6767.chat/sgs",
            "status": "Live",
            "status_bg": "#132f22",
            "status_fg": "#22c55e",
            "desc": "Interactive quote library for Sanguosha game, featuring dialogue search, audio playback, and admin panel."
        },
        {
            "name": "AIED DuoGrow SaaS",
            "url": "https://github.com/connectedGraph/AIED-DuoGrow-SaaS",
            "status": "Build",
            "status_bg": "#352311",
            "status_fg": "#e0af68",
            "desc": "Lightweight English learning web app with parent-child feedback loops and AI grading."
        },
        {
            "name": "BrightlyPk",
            "url": "https://github.com/connectedGraph/BrightlyPk",
            "status": "Lab",
            "status_bg": "#24183d",
            "status_fg": "#bb9af3",
            "desc": "Node.js + WebSocket powered real-time multiplayer trivia competition platform."
        },
        {
            "name": "Deepseek Unofficial API",
            "url": "https://github.com/connectedGraph/Deepseek-unofficial-API",
            "status": "Lab",
            "status_bg": "#24183d",
            "status_fg": "#bb9af3",
            "desc": "Node.js library wrapper for Deepseek Expert Mode."
        }
    ]

    rows_html = ""
    for idx, p in enumerate(projects):
        row_y = 50 + idx * 42
        
        # Draw separator line between rows (except after the last one)
        sep_line = ""
        if idx < len(projects) - 1:
            sep_y = row_y + 21
            sep_line = f'<line x1="35" y1="{sep_y}" x2="715" y2="{sep_y}" stroke="#24283b" stroke-width="1"/>'
            
        rows_html += f"""    <!-- Row {idx}: {p['name']} -->
    <g transform="translate(0, 0)">
      <!-- Folder Icon -->
      <g transform="translate(35, {row_y - 12})" stroke="#7aa2f7" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <path d="M2 4a2 2 0 0 1 2-2h4l2 2h6a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4z"/>
      </g>
      
      <!-- Project Name -->
      <text x="62" y="{row_y + 1}" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="13.5" font-weight="bold" fill="#7dcfff">{p['name']}</text>
      
      <!-- Status Badge -->
      <rect x="245" y="{row_y - 11}" width="48" height="17" rx="8.5" fill="{p['status_bg']}"/>
      <text x="269" y="{row_y + 1}" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="9.5" font-weight="800" fill="{p['status_fg']}" text-anchor="middle">{p['status']}</text>
      
      <!-- Description -->
      <text x="305" y="{row_y + 1}" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="12" fill="#a9b1d6">{p['desc']}</text>
    </g>
    {sep_line}
"""

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="750" height="277" viewBox="0 0 750 277" fill="none">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="720" height="247" rx="12" fill="#1a1b26" stroke="#24283b" stroke-width="1.5" filter="url(#shadow)"/>

{rows_html}</svg>
"""

    with open("projects.svg", "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated projects.svg")
