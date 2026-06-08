import os

def generate_typewriter(output_dir=".", theme="dark"):
    if theme == "light":
        term_bg = "#f6f8fa"
        term_stroke = "#d1d5db"
        shadow_opacity = "0.15"
        title_color = "#6a737d"
        prompt_color = "#005cc5"
        command_color = "#6f42c1"
        flag_color = "#e36209"
        string_color = "#22863a"
        output_color = "#24292e"
        cursor_color = "#586069"
        danger_op_color = "#6f42c1"
        yolo_op_color = "#d73a49"
    else:
        term_bg = "#1a1b26"
        term_stroke = "#24283b"
        shadow_opacity = "0.55"
        title_color = "#565f89"
        prompt_color = "#7dcfff"
        command_color = "#bb9af3"
        flag_color = "#ff9e64"
        string_color = "#9ece6a"
        output_color = "#a9b1d6"
        cursor_color = "#787c99"
        danger_op_color = "#bb9af3"
        yolo_op_color = "#f7768e"

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="750" height="315" viewBox="0 0 750 315" fill="none">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="{shadow_opacity}"/>
    </filter>
    <clipPath id="terminal-clip">
      <rect x="16" y="16" width="718" height="283" rx="11"/>
    </clipPath>
  </defs>

  <style>
    .terminal-bg {{
      fill: {term_bg};
      stroke: {term_stroke};
      stroke-width: 1.5px;
    }}
    .btn-red {{ fill: #f7768e; }}
    .btn-yellow {{ fill: #e0af68; }}
    .btn-green {{ fill: #9ece6a; }}
    
    .title-text {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 13px;
      fill: {title_color};
      font-weight: 500;
    }}
    
    .code-text {{
      font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
      font-size: 14px;
      font-weight: bold;
    }}
    
    .prompt {{
      fill: {prompt_color};
    }}
    
    .command {{
      fill: {command_color};
    }}
    
    .flag {{
      fill: {flag_color};
    }}
    
    .string {{
      fill: {string_color};
    }}
    
    .output {{
      font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
      font-size: 13.5px;
      fill: {output_color};
    }}
    
    .cursor {{
      fill: {cursor_color};
    }}
    
    /* Sliding Mask Rects (locked to cursor keyframes) */
    .mask-rect-1 {{
      animation: mask1-anim 12s infinite linear;
    }}
    .mask-rect-2 {{
      animation: mask2-anim 12s infinite linear;
    }}
    .mask-rect-3 {{
      animation: mask3-anim 12s infinite linear;
    }}
    .mask-rect-4 {{
      animation: mask4-anim 12s infinite linear;
    }}
    
    @keyframes mask1-anim {{
      0%, 4.17% {{ transform: translateX(0); }}
      15.0%, 100% {{ transform: translateX(230px); }}
    }}
    @keyframes mask2-anim {{
      0%, 20.83% {{ transform: translateX(0); }}
      29.17%, 100% {{ transform: translateX(105px); }}
    }}
    @keyframes mask3-anim {{
      0%, 37.5% {{ transform: translateX(0); }}
      54.17%, 100% {{ transform: translateX(335px); }}
    }}
    @keyframes mask4-anim {{
      0%, 60.83% {{ transform: translateX(0); }}
      69.17%, 100% {{ transform: translateX(105px); }}
    }}
    
    /* Unified Cursors Animations (Combines movement and visibility to prevent drift) */
    .cursor1 {{
      animation: cur1-anim 12s infinite linear;
    }}
    .cursor2 {{
      animation: cur2-anim 12s infinite linear;
    }}
    .cursor3 {{
      animation: cur3-anim 12s infinite linear;
    }}
    .cursor4 {{
      animation: cur4-anim 12s infinite linear;
    }}
    
    @keyframes cur1-anim {{
      0%, 4.16% {{ transform: translateX(0); opacity: 0; }}
      4.17% {{ transform: translateX(0); opacity: 1; }}
      15.0% {{ transform: translateX(230px); opacity: 1; }}
      15.5% {{ transform: translateX(230px); opacity: 0; }}
      16.0% {{ transform: translateX(230px); opacity: 1; }}
      16.5% {{ transform: translateX(230px); opacity: 0; }}
      16.67%, 100% {{ transform: translateX(230px); opacity: 0; }}
    }}
    
    @keyframes cur2-anim {{
      0%, 19.17% {{ transform: translateX(0); opacity: 0; }}
      19.18%, 20.82% {{ transform: translateX(0); opacity: 1; }}
      20.83% {{ transform: translateX(0); opacity: 1; }}
      29.17% {{ transform: translateX(105px); opacity: 1; }}
      29.5% {{ transform: translateX(105px); opacity: 0; }}
      30.0% {{ transform: translateX(105px); opacity: 1; }}
      30.5% {{ transform: translateX(105px); opacity: 0; }}
      30.83%, 100% {{ transform: translateX(105px); opacity: 0; }}
    }}
    
    @keyframes cur3-anim {{
      0%, 35.0% {{ transform: translateX(0); opacity: 0; }}
      35.01%, 37.49% {{ transform: translateX(0); opacity: 1; }}
      37.5% {{ transform: translateX(0); opacity: 1; }}
      54.17% {{ transform: translateX(335px); opacity: 1; }}
      54.5% {{ transform: translateX(335px); opacity: 0; }}
      55.0% {{ transform: translateX(335px); opacity: 1; }}
      55.5% {{ transform: translateX(335px); opacity: 0; }}
      55.83%, 100% {{ transform: translateX(335px); opacity: 0; }}
    }}
    
    @keyframes cur4-anim {{
      0%, 58.33% {{ transform: translateX(0); opacity: 0; }}
      58.34%, 60.82% {{ transform: translateX(0); opacity: 1; }}
      60.83% {{ transform: translateX(0); opacity: 1; }}
      69.17% {{ transform: translateX(105px); opacity: 1; }}
      72.0% {{ transform: translateX(105px); opacity: 0; }}
      75.0% {{ transform: translateX(105px); opacity: 1; }}
      78.0% {{ transform: translateX(105px); opacity: 0; }}
      81.0% {{ transform: translateX(105px); opacity: 1; }}
      84.0% {{ transform: translateX(105px); opacity: 0; }}
      87.0% {{ transform: translateX(105px); opacity: 1; }}
      90.0% {{ transform: translateX(105px); opacity: 0; }}
      93.0% {{ transform: translateX(105px); opacity: 1; }}
      96.0% {{ transform: translateX(105px); opacity: 0; }}
      99.0%, 100% {{ transform: translateX(105px); opacity: 1; }}
    }}
    
    /* Outputs Animations */
    .op1 {{ animation: op1-anim 12s infinite; }}
    .op2 {{ animation: op2-anim 12s infinite; }}
    .op3 {{ animation: op3-anim 12s infinite; }}
    .op4 {{ animation: op4-anim 12s infinite; }}
    .op5 {{ animation: op5-anim 12s infinite; }}
    
    .pr2 {{ animation: pr2-anim 12s infinite; }}
    .pr3 {{ animation: pr3-anim 12s infinite; }}
    .pr4 {{ animation: pr4-anim 12s infinite; }}
    
    @keyframes op1-anim {{
      0%, 16.67% {{ opacity: 0; }}
      16.68%, 100% {{ opacity: 1; }}
    }}
    @keyframes pr2-anim {{
      0%, 19.17% {{ opacity: 0; }}
      19.18%, 100% {{ opacity: 1; }}
    }}
    @keyframes op2-anim {{
      0%, 30.83% {{ opacity: 0; }}
      30.84%, 100% {{ opacity: 1; }}
    }}
    @keyframes op3-anim {{
      0%, 32.5% {{ opacity: 0; }}
      32.51%, 100% {{ opacity: 1; }}
    }}
    @keyframes pr3-anim {{
      0%, 35.0% {{ opacity: 0; }}
      35.01%, 100% {{ opacity: 1; }}
    }}
    @keyframes op4-anim {{
      0%, 55.83% {{ opacity: 0; }}
      55.84%, 100% {{ opacity: 1; }}
    }}
    @keyframes pr4-anim {{
      0%, 58.33% {{ opacity: 0; }}
      58.34%, 100% {{ opacity: 1; }}
    }}
    @keyframes op5-anim {{
      0%, 70.83% {{ opacity: 0; }}
      70.84%, 100% {{ opacity: 1; }}
    }}
  </style>

  <rect x="15" y="15" width="720" height="285" rx="12" class="terminal-bg" filter="url(#shadow)"/>
  
  <!-- Window Header Buttons -->
  <circle cx="40" cy="35" r="6" class="btn-red"/>
  <circle cx="60" cy="35" r="6" class="btn-yellow"/>
  <circle cx="80" cy="35" r="6" class="btn-green"/>
  <text x="375" y="40" class="title-text" text-anchor="middle">euler@localhost:~</text>
  
  <g clip-path="url(#terminal-clip)">
    <!-- Line 1: greet command -->
    <text x="35" y="62" class="code-text prompt">euler~% </text>
  <text x="105" y="62" class="code-text command">greet <tspan class="flag">--role</tspan> <tspan class="string">"CS Freshman"</tspan></text>
  <rect x="105" y="48" width="230" height="20" fill="{term_bg}" class="mask-rect-1"/>
  <rect x="105" y="48" width="8" height="16" class="cursor cursor1"/>
  
  <!-- Line 2: greet output -->
  <text x="35" y="85" class="output op1">Hi, CS Freshman here! Nice to meet you. 👋</text>
  
  <!-- Line 3: show-profile command -->
  <text x="35" y="108" class="code-text prompt pr2">euler~% </text>
  <text x="105" y="108" class="code-text command">show-profile</text>
  <rect x="105" y="94" width="105" height="20" fill="{term_bg}" class="mask-rect-2"/>
  <rect x="105" y="94" width="8" height="16" class="cursor cursor2"/>
  
  <!-- Line 4 & 5: show-profile outputs -->
  <text x="35" y="131" class="output op2">Focus:  Full-Stack AI Applications (Vertical AIED)</text>
  <text x="35" y="154" class="output op3">Status: yolo</text>
  
  <!-- Line 6: claude command -->
  <text x="35" y="177" class="code-text prompt pr3">euler~% </text>
  <text x="105" y="177" class="code-text command">claude <tspan class="flag">--dangerously-skip-permissions</tspan></text>
  <rect x="105" y="163" width="335" height="20" fill="{term_bg}" class="mask-rect-3"/>
  <rect x="105" y="163" width="8" height="16" class="cursor cursor3"/>
  
  <!-- Line 7: claude output -->
  <text x="35" y="200" class="output op4" fill="{danger_op_color}">[Danger Mode] Skipping permissions... Let\'s build!</text>
  
  <!-- Line 8: codex command -->
  <text x="35" y="223" class="code-text prompt pr4">euler~% </text>
  <text x="105" y="223" class="code-text command">codex <tspan class="flag">--yolo</tspan></text>
  <rect x="105" y="209" width="105" height="20" fill="{term_bg}" class="mask-rect-4"/>
  <rect x="105" y="209" width="8" height="16" class="cursor cursor4"/>
  
    <!-- Line 9: codex output -->
    <text x="35" y="246" class="output op5" fill="{yolo_op_color}">[YOLO Mode] Code generation full speed ahead!</text>
  </g>
</svg>
"""
    filepath = os.path.join(output_dir, "typewriter.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")
