/* ═══════════════════════════════════════════
   README Builder — App Logic
   ═══════════════════════════════════════════ */

// ── State ──────────────────────────────────────────────────────────────────────
const state = {
  component: 'typewriter',
  previewTheme: 'dark',   // which single theme the toggle shows (unused — we show both)
  params: {
    typewriter: { animation_duration: 12 },
    avatar:     { ring_color_1: '#7aa2f7', ring_color_2: '#bb9af3', ring_color_3: '#7dcfff', pulse_duration: 4 },
    thinking:   { sweep_color: '#22d3ee', spin_duration: 2.4 },
  }
};

// ── DOM refs ────────────────────────────────────────────────────────────────────
const $  = id => document.getElementById(id);
const $$ = sel => document.querySelectorAll(sel);

const darkPreview   = $('darkPreview');
const lightPreview  = $('lightPreview');
const previewLabel  = $('previewLabel');
const buildLog      = $('buildLog');
const buildLogBody  = $('buildLogBody');
const buildModal    = $('buildModal');
const modalMsg      = $('modalMsg');

// ── Labels ─────────────────────────────────────────────────────────────────────
const COMPONENT_LABELS = {
  typewriter:          'Terminal Animation',
  avatar:              'Avatar',
  thinking:            'Thinking UI',
  api_docs:            'API Docs Card',
  footer:              'Footer',
  ask_me_badge:        'Ask Me Badge',
  header_tech_stack:   'Header · Tech Stack',
  header_projects:     'Header · Projects',
  header_public_apis:  'Header · Public APIs',
  header_stats:        'Header · GitHub Stats',
  header_roadmap:      'Header · Roadmap',
  header_ask_me:       'Header · Ask Me',
};

// ── Sidebar navigation ─────────────────────────────────────────────────────────
document.querySelectorAll('.nav-item').forEach(btn => {
  btn.addEventListener('click', () => {
    $$('.nav-item').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.component = btn.dataset.component;
    previewLabel.textContent = COMPONENT_LABELS[state.component] || state.component;
    showControls(state.component);
    requestPreview();
  });
});

function showControls(component) {
  // Hide all
  $$('[id^="ctrl-"]').forEach(el => el.classList.add('hidden'));

  if (component === 'typewriter') {
    $('ctrl-typewriter').classList.remove('hidden');
  } else if (component === 'avatar') {
    $('ctrl-avatar').classList.remove('hidden');
  } else if (component === 'thinking') {
    $('ctrl-thinking').classList.remove('hidden');
  } else {
    $('ctrl-generic').classList.remove('hidden');
  }
}

// ── Slider wiring ──────────────────────────────────────────────────────────────
function wireSlider(sliderId, valId, stateKey, paramKey, suffix = 's', decimals = 0) {
  const slider = $(sliderId);
  const valEl  = $(valId);
  if (!slider) return;

  slider.addEventListener('input', () => {
    const v = parseFloat(slider.value);
    valEl.textContent = decimals ? `${v.toFixed(decimals)}${suffix}` : `${v}${suffix}`;
    state.params[stateKey][paramKey] = v;
  });
}

wireSlider('tw-duration', 'tw-duration-val', 'typewriter', 'animation_duration', 's');
wireSlider('av-pulse',    'av-pulse-val',    'avatar',     'pulse_duration',     's', 1);

// Thinking spin slider
const thSpin    = $('th-spin');
const thSpinVal = $('th-spin-val');
if (thSpin) {
  thSpin.addEventListener('input', () => {
    const v = parseFloat(thSpin.value);
    thSpinVal.textContent = `${v.toFixed(1)}s`;
    state.params.thinking.spin_duration = v;
  });
}

// ── Color pickers ───────────────────────────────────────────────────────────────
['av-ring1', 'av-ring2', 'av-ring3'].forEach((id, i) => {
  const el = $(id);
  if (!el) return;
  el.addEventListener('input', () => {
    state.params.avatar[`ring_color_${i + 1}`] = el.value;
  });
});

const thSweep = $('th-sweep');
if (thSweep) {
  thSweep.addEventListener('input', () => {
    state.params.thinking.sweep_color = thSweep.value;
  });
}

// ── Speed preset chips (terminal) ───────────────────────────────────────────────
$$('.chip[data-target]').forEach(chip => {
  chip.addEventListener('click', () => {
    const targetId = chip.dataset.target;
    const val      = parseFloat(chip.dataset.val);
    const slider   = $(targetId);
    if (!slider) return;

    slider.value = val;
    slider.dispatchEvent(new Event('input'));

    // Update active chip
    const siblings = $$(`.chip[data-target="${targetId}"]`);
    siblings.forEach(s => s.classList.remove('active'));
    chip.classList.add('active');
  });
});

// ── Color chips (thinking sweep) ────────────────────────────────────────────────
$$('.chip[data-color]').forEach(chip => {
  chip.addEventListener('click', () => {
    const pickerId = chip.dataset.picker;
    const color    = chip.dataset.color;
    const picker   = $(pickerId);
    if (picker) {
      picker.value = color;
      picker.dispatchEvent(new Event('input'));
    }
    const siblings = $$(`.chip[data-picker="${pickerId}"]`);
    siblings.forEach(s => s.classList.remove('active'));
    chip.classList.add('active');
  });
});

// ── Avatar preset chips ─────────────────────────────────────────────────────────
$$('.chip-preset').forEach(chip => {
  chip.addEventListener('click', () => {
    const r1 = chip.dataset.r1;
    const r2 = chip.dataset.r2;
    const r3 = chip.dataset.r3;

    // Update color pickers
    const setCol = (id, val) => {
      const el = $(id);
      if (el) { el.value = val; el.dispatchEvent(new Event('input')); }
    };
    setCol('av-ring1', r1);
    setCol('av-ring2', r2);
    setCol('av-ring3', r3);

    $$('.chip-preset').forEach(s => s.classList.remove('active'));
    chip.classList.add('active');
  });
});

// ── Preview ─────────────────────────────────────────────────────────────────────
function setPreviewLoading(container) {
  container.innerHTML = `<div class="preview-placeholder"><div class="spinner"></div><span>Generating…</span></div>`;
}

function setPreviewSvg(container, dataUri) {
  container.innerHTML = `<img src="${dataUri}" alt="preview" draggable="false"/>`;
}

function setPreviewError(container, msg) {
  container.innerHTML = `<div class="preview-placeholder" style="color:#f7768e">⚠ ${msg}</div>`;
}

async function fetchPreview(theme) {
  const container = theme === 'dark' ? darkPreview : lightPreview;
  setPreviewLoading(container);

  const compParams = buildComponentParams(state.component);

  try {
    const res = await fetch('/api/preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ component: state.component, theme, params: compParams })
    });
    const data = await res.json();
    if (data.error) {
      setPreviewError(container, data.error);
    } else {
      setPreviewSvg(container, data.svg);
    }
  } catch (e) {
    setPreviewError(container, e.message);
  }
}

function buildComponentParams(component) {
  if (component === 'typewriter') return state.params.typewriter;
  if (component === 'avatar')     return state.params.avatar;
  if (component === 'thinking')   return state.params.thinking;
  return {};
}

function requestPreview() {
  fetchPreview('dark');
  fetchPreview('light');
}

// ── Preview button ──────────────────────────────────────────────────────────────
$('previewBtn').addEventListener('click', requestPreview);

// ── Refresh button ──────────────────────────────────────────────────────────────
$('refreshPreviewBtn').addEventListener('click', () => {
  const btn = $('refreshPreviewBtn');
  btn.classList.add('spin');
  setTimeout(() => btn.classList.remove('spin'), 650);
  requestPreview();
});

// ── Build Component ─────────────────────────────────────────────────────────────
$('buildComponentBtn').addEventListener('click', async () => {
  const btn = $('buildComponentBtn');
  btn.disabled = true;
  btn.textContent = 'Building…';

  const compParams = buildComponentParams(state.component);

  for (const theme of ['dark', 'light']) {
    await fetch('/api/preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        component: state.component,
        theme,
        params: compParams,
        write_to_project: true
      })
    });
  }

  btn.disabled = false;
  btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg> Build Component`;

  // Refresh preview
  requestPreview();
  showLog([`✅ Built ${COMPONENT_LABELS[state.component]} (dark + light)`]);
});

// ── Build All ───────────────────────────────────────────────────────────────────
$('buildAllBtn').addEventListener('click', async () => {
  const btn = $('buildAllBtn');
  btn.classList.add('loading');
  btn.innerHTML = `<div class="spinner" style="width:14px;height:14px;border-width:2px;border-top-color:#1a1b26;border-color:rgba(26,27,38,0.3);"></div> Building…`;

  try {
    const res = await fetch('/api/build-all', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ params: state.params })
    });
    const data = await res.json();

    modalMsg.textContent = data.results.join('\n');
    buildModal.style.display = 'flex';
    showLog(data.results);
    requestPreview();
  } catch (e) {
    alert('Build failed: ' + e.message);
  } finally {
    btn.classList.remove('loading');
    btn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg> Build All`;
  }
});

// ── Build log ───────────────────────────────────────────────────────────────────
function showLog(lines) {
  buildLog.style.display = 'block';
  buildLogBody.innerHTML = lines.map(l => `<div>${l}</div>`).join('');
}

$('buildLogClose').addEventListener('click', () => {
  buildLog.style.display = 'none';
});

// ── Modal close ─────────────────────────────────────────────────────────────────
$('modalClose').addEventListener('click', () => {
  buildModal.style.display = 'none';
});
buildModal.addEventListener('click', e => {
  if (e.target === buildModal) buildModal.style.display = 'none';
});

// ── Init ────────────────────────────────────────────────────────────────────────
showControls('typewriter');
requestPreview();
