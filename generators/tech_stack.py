def generate_tech_stack():
    # Icons for tech stack
    nextjs_icon = '<path d="M1 15V1M1 1L15 15M15 15V1" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    react_icon = '<circle cx="8" cy="8" r="1.5" fill="#61dafb"/><ellipse cx="8" cy="8" rx="7.5" ry="2.5" stroke="#61dafb" stroke-width="1.2" fill="none" transform="rotate(30 8 8)"/><ellipse cx="8" cy="8" rx="7.5" ry="2.5" stroke="#61dafb" stroke-width="1.2" fill="none" transform="rotate(90 8 8)"/><ellipse cx="8" cy="8" rx="7.5" ry="2.5" stroke="#61dafb" stroke-width="1.2" fill="none" transform="rotate(150 8 8)"/>'
    js_icon = '<rect x="0" y="0" width="16" height="16" rx="2" fill="#f7df1e"/><text x="3" y="12" font-family="-apple-system, sans-serif" font-size="9" font-weight="900" fill="#000000">JS</text>'
    html5_icon = '<path d="M2 1l1.2 11 4.8 1.8 4.8-1.8L14 1H2z" fill="#e34f26"/><path d="M8 2.2v10.3l3.8-1.4.7-7.5H8z" fill="#f06529"/><path d="M5 4.5h6l-.3 3H8v1.5h1.2l-.2 1.5-2.2.8-2.2-.8-.1-1.5H3.1l.2 2.8 4.7 1.7 4.7-1.7.5-5.2H8V4.5z" fill="#ffffff"/>'
    css3_icon = '<path d="M2 1l1.2 11 4.8 1.8 4.8-1.8L14 1H2z" fill="#1572b6"/><path d="M8 2.2v10.3l3.8-1.4.7-7.5H8z" fill="#33a9dc"/><path d="M5 4.5h6l-.3 3H8v1.5h1.2l-.2 1.5-2.2.8-2.2-.8-.1-1.5H3.1l.2 2.8 4.7 1.7 4.7-1.7.5-5.2H8V4.5z" fill="#ffffff"/>'
    nodejs_icon = '<path d="M8 1L1.5 4.8v7.5L8 16l6.5-3.7V4.8L8 1z" stroke="#339933" stroke-width="1.8" stroke-linejoin="round" fill="none"/>'
    python_icon = """<g transform="scale(0.14545) translate(-0.21, 0.077)">
      <linearGradient id="python_grad1" gradientUnits="userSpaceOnUse" x1="63.8159" y1="56.6829" x2="118.4934" y2="1.8225" gradientTransform="matrix(1 0 0 -1 -53.2974 66.4321)">
        <stop offset="0" style="stop-color:#387EB8"/>
        <stop offset="1" style="stop-color:#366994"/>
      </linearGradient>
      <path fill="url(#python_grad1)" d="M55.023-0.077c-25.971,0-26.25,10.081-26.25,12.156c0,3.148,0,12.594,0,12.594h26.75v3.781 c0,0-27.852,0-37.375,0c-7.949,0-17.938,4.833-17.938,26.25c0,19.673,7.792,27.281,15.656,27.281c2.335,0,9.344,0,9.344,0 s0-9.765,0-13.125c0-5.491,2.721-15.656,15.406-15.656c15.91,0,19.971,0,26.531,0c3.902,0,14.906-1.696,14.906-14.406 c0-13.452,0-17.89,0-24.219C82.054,11.426,81.515-0.077,55.023-0.077z M40.273,8.392c2.662,0,4.813,2.15,4.813,4.813 c0,2.661-2.151,4.813-4.813,4.813s-4.813-2.151-4.813-4.813C35.46,10.542,37.611,8.392,40.273,8.392z"/>
      <linearGradient id="python_grad2" gradientUnits="userSpaceOnUse" x1="97.0444" y1="21.6321" x2="155.6665" y2="-34.5308" gradientTransform="matrix(1 0 0 -1 -53.2974 66.4321)">
        <stop offset="0" style="stop-color:#FFE052"/>
        <stop offset="1" style="stop-color:#FFC331"/>
      </linearGradient>
      <path fill="url(#python_grad2)" d="M55.397,109.923c25.959,0,26.282-10.271,26.282-12.156c0-3.148,0-12.594,0-12.594H54.897v-3.781 c0,0,28.032,0,37.375,0c8.009,0,17.938-4.954,17.938-26.25c0-23.322-10.538-27.281-15.656-27.281c-2.336,0-9.344,0-9.344,0 s0,10.216,0,13.125c0,5.491-2.631,15.656-15.406,15.656c-15.91,0-19.476,0-26.532,0c-3.892,0-14.906,1.896-14.906,14.406 c0,14.475,0,18.265,0,24.219C28.366,100.497,31.562,109.923,55.397,109.923z M70.148,101.454c-2.662,0-4.813-2.151-4.813-4.813 s2.15-4.813,4.813-4.813c2.661,0,4.813,2.151,4.813,4.813S72.809,101.454,70.148,101.454z"/>
    </g>"""
    express_icon = '<text x="1" y="13" font-family="-apple-system, sans-serif" font-size="11" font-weight="900" fill="#a9b1d6">EX</text>'
    postgresql_icon = '<path d="M14 6c0-2.5-2-4.5-4.5-4.5S5 3.5 5 6c0 1.5.5 3 1.5 4L5 13.5l3.5-1.5c1 .5 2 .8 3 .8h1v3H9v1h4.5c1.4 0 2.5-1.1 2.5-2.5V6z" fill="#316192"/>'
    claude_icon = '<circle cx="8" cy="8" r="7" stroke="#d97757" stroke-width="1.8" fill="none"/><circle cx="8" cy="8" r="3" fill="#d97757"/>'
    codex_icon = '<g transform="scale(0.6667)"><path clip-rule="evenodd" fill-rule="evenodd" d="M8.086.457a6.105 6.105 0 013.046-.415c1.333.153 2.521.72 3.564 1.7a.117.117 0 00.107.029c1.408-.346 2.762-.224 4.061.366l.063.03.154.076c1.357.703 2.33 1.77 2.918 3.198.278.679.418 1.388.421 2.126a5.655 5.655 0 01-.18 1.631.167.167 0 00.04.155 5.982 5.982 0 011.578 2.891c.385 1.901-.01 3.615-1.183 5.14l-.182.22a6.063 6.063 0 01-2.934 1.851.162.162 0 00-.108.102c-.255.736-.511 1.364-.987 1.992-1.199 1.582-2.962 2.462-4.948 2.451-1.583-.008-2.986-.587-4.21-1.736a.145.145 0 00-.14-.032c-.518.167-1.04.191-1.604.185a5.924 5.924 0 01-2.595-.622 6.058 6.058 0 01-2.146-1.781c-.203-.269-.404-.522-.551-.821a7.74 7.74 0 01-.495-1.283 6.11 6.11 0 01-.017-3.064.166.166 0 00.008-.074.115.115 0 00-.037-.064 5.958 5.958 0 01-1.38-2.202 5.196 5.196 0 01-.333-1.589 6.915 6.915 0 01.188-2.132c.45-1.484 1.309-2.648 2.577-3.493.282-.188.55-.334.802-.438.286-.12.573-.22.861-.304a.129.129 0 00.087-.087A6.016 6.016 0 015.635 2.31C6.315 1.464 7.132.846 8.086.457zm-.804 7.85a.848.848 0 00-1.473.842l1.694 2.965-1.688 2.848a.849.849 0 001.46.864l1.94-3.272a.849.849 0 00.007-.854l-1.94-3.393zm5.446 6.24a.849.849 0 000 1.695h4.848a.849.849 0 000-1.696h-4.848z" fill="#9ece6a"/></g>'
    claudecode_icon = """<g transform="scale(0.66667)">
      <path clip-rule="evenodd" d="M20.998 10.949H24v3.102h-3v3.028h-1.487V20H18v-2.921h-1.487V20H15v-2.921H9V20H7.488v-2.921H6V20H4.487v-2.921H3V14.05H0V10.95h3V5h17.998v5.949zM6 10.949h1.488V8.102H6v2.847zm10.51 0H18V8.102h-1.49v2.847z" fill="#D97757" fill-rule="evenodd"/>
    </g>"""

    # Helper function to generate a tech pill
    def pill(x, y, name, icon):
        return f"""    <g transform="translate({x}, {y})">
      <rect x="0.5" y="0.5" width="97" height="25" rx="13" fill="#16161e" stroke="#24283b" stroke-width="1"/>
      <g transform="translate(8, 5)">
        {icon}
      </g>
      <text x="28" y="17" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="10.5" font-weight="600" fill="#c0caf5">{name}</text>
    </g>"""

    # Columns definitions
    # Frontend: Next.js, React, JavaScript, HTML5, CSS3
    fe_pills = [
        pill(35, 65, "Next.js", nextjs_icon),
        pill(140, 65, "React", react_icon),
        pill(35, 98, "JavaScript", js_icon),
        pill(140, 98, "HTML5", html5_icon),
        pill(35, 131, "CSS3", css3_icon)
    ]

    # Backend: Node.js, Python, Express, PostgreSQL
    be_pills = [
        pill(270, 65, "Node.js", nodejs_icon),
        pill(375, 65, "Python", python_icon),
        pill(270, 98, "Express", express_icon),
        pill(375, 98, "PostgreSQL", postgresql_icon)
    ]

    # AI & Tools: Claude, Codex, Claude Code
    ai_pills = [
        pill(505, 65, "Claude API", claude_icon),
        pill(610, 65, "Codex", codex_icon),
        pill(505, 98, "Claude Code", claudecode_icon)
    ]

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="750" height="185" viewBox="0 0 750 185" fill="none">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
    <linearGradient id="header-grad" x1="0" y1="0" x2="200" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7aa2f7"/>
      <stop offset="100%" stop-color="#bb9af3"/>
    </linearGradient>
  </defs>

  <!-- Background Card -->
  <rect x="15" y="15" width="720" height="155" rx="12" fill="#1a1b26" stroke="#24283b" stroke-width="1.5" filter="url(#shadow)"/>

  <!-- Column 1: Frontend -->
  <text x="35" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="12" font-weight="800" fill="#7aa2f7" letter-spacing="1">FRONTEND</text>
  <rect x="35" y="52" width="45" height="2" rx="1" fill="url(#header-grad)"/>
  {"".join(fe_pills)}

  <!-- Column 2: Backend & DB -->
  <text x="270" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="12" font-weight="800" fill="#7aa2f7" letter-spacing="1">BACKEND &amp; DB</text>
  <rect x="270" y="52" width="45" height="2" rx="1" fill="url(#header-grad)"/>
  {"".join(be_pills)}

  <!-- Column 3: AI & Tools -->
  <text x="505" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="12" font-weight="800" fill="#7aa2f7" letter-spacing="1">AI &amp; DEV TOOLS</text>
  <rect x="505" y="52" width="45" height="2" rx="1" fill="url(#header-grad)"/>
  {"".join(ai_pills)}
</svg>"""

    with open("tech_stack.svg", "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated tech_stack.svg")
