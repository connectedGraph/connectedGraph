import os

def generate_thinking_header(output_dir=".", theme="dark"):
    spinner_symbols = ['✻', '✺', '✹', '✸', '✶', '✶', '✦', '✶', '✶', '✸', '✹', '✺']
    words = [
        'Cogitating',
        'Pondering',
        'Contemplating',
        'Deliberating',
        'Architecting',
        'Synthesizing',
        'Orchestrating',
        'Composing',
        'Brewing',
        'Whisking',
        'Caramelizing',
        'Marinating',
        'Seasoning',
        'Crystallizing',
        'Transmuting',
        'Conjuring',
        'Finagling',
        'Vibing'
    ]

    if theme == "light":
        text_color = "#24292e"
        spin_color = "#005cc5"
        sweep_gradient = "linear-gradient(90deg, #005cc5 0%, #005cc5 38%, #c8e1ff 50%, #005cc5 62%, #005cc5 100%)"
    else:
        text_color = "#c9d1d9"
        spin_color = "#22d3ee"
        sweep_gradient = "linear-gradient(90deg, #22d3ee 0%, #22d3ee 38%, #e3fbff 50%, #22d3ee 62%, #22d3ee 100%)"

    # Generate 18 rows. Each row has its own spinner and verb.
    rows_html = ""
    for idx, word in enumerate(words):
        row_delay = (idx - len(words)) * 2
        
        # Generate spinner spans for this row
        spinner_spans = ""
        for s_idx, char in enumerate(spinner_symbols):
            s_delay = (s_idx - len(spinner_symbols)) * 0.2
            spinner_spans += f'            <span class="cc-spin" style="animation-delay: {s_delay:.1f}s;">{char}</span>\n'
            
        rows_html += f"""          <div class="cc-row" style="animation-delay: {row_delay}s;">
            <span class="cc-spin-container">
{spinner_spans}            </span>
            <span class="cc-label">
              <span class="cc-verb">{word}</span>
              <span class="cc-dots">…</span>
            </span>
          </div>\n"""

    content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="300" height="35" viewBox="0 0 300 35" fill="none">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <style>
        .cc-container {{
          display: flex;
          justify-content: center;
          align-items: center;
          width: 100%;
          height: 100%;
        }}
        .cc {{
          font-family: "Cascadia Code", "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace;
          color: {text_color};
          font-size: 14px;
          line-height: 1.55;
          user-select: none;
        }}
        .cc-row-container {{
          display: grid;
          grid-template-columns: 1fr;
          width: 100%;
          justify-items: center;
          align-items: center;
        }}
        .cc-row {{
          grid-area: 1 / 1;
          display: inline-flex;
          align-items: center;
          gap: 8px;
          opacity: 0;
          visibility: hidden;
          animation: word-step 36s infinite linear;
        }}
        .cc-spin-container {{
          display: inline-grid;
          grid-template-columns: 1fr;
          align-items: center;
          justify-items: center;
          width: 1.3em;
          height: 1.55em;
          position: relative;
          flex: 0 0 auto;
        }}
        .cc-spin {{
          grid-area: 1 / 1;
          color: {spin_color};
          font-weight: 700;
          line-height: 1;
          opacity: 0;
          visibility: hidden;
          animation: spin-step 2.4s infinite linear;
        }}
        .cc-label {{
          white-space: nowrap;
          display: inline-flex;
          align-items: center;
        }}
        .cc-verb {{
          background: {sweep_gradient};
          background-size: 220% 100%;
          -webkit-background-clip: text;
          background-clip: text;
          -webkit-text-fill-color: transparent;
          color: {spin_color};
          animation: cc-sweep 2.4s linear infinite;
        }}
        .cc-dots {{
          color: {text_color};
          margin-left: 2px;
        }}
        @keyframes cc-sweep {{
          0% {{ background-position: 130% 0; }}
          100% {{ background-position: -30% 0; }}
        }}
        @keyframes spin-step {{
          0%, 8.333% {{ opacity: 1; visibility: visible; }}
          8.334%, 100% {{ opacity: 0; visibility: hidden; }}
        }}
        @keyframes word-step {{
          0%, 5.555% {{ opacity: 1; visibility: visible; }}
          5.556%, 100% {{ opacity: 0; visibility: hidden; }}
        }}
      </style>
      <div class="cc cc-container">
        <div class="cc-row-container">
{rows_html}        </div>
      </div>
    </div>
  </foreignObject>
</svg>
"""
    filepath = os.path.join(output_dir, "thinking_header.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath} ({theme})")
