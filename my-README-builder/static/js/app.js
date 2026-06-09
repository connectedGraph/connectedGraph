/* README Builder — frontend logic (rebuilt) */

// ── State ──────────────────────────────────────────────────────────────────────
const DEFAULT_TS_CATS = [
  {title: 'FRONTEND', items: [
    {slug: 'nextjs', label: 'Next.js', subfolder: 'code'},
    {slug: 'react',  label: 'React',   subfolder: 'code'},
    {slug: 'javascript', label: 'JavaScript', subfolder: 'code'},
    {slug: 'html5',  label: 'HTML5',   subfolder: 'code'},
    {slug: 'css3',   label: 'CSS3',    subfolder: 'code'},
  ]},
  {title: 'BACKEND & DB', items: [
    {slug: 'nodejs',  label: 'Node.js',    subfolder: 'code'},
    {slug: 'python',  label: 'Python',     subfolder: 'code'},
    {slug: 'express', label: 'Express',    subfolder: 'code'},
    {slug: 'pgsql',   label: 'PostgreSQL', subfolder: 'code'},
  ]},
  {title: 'AI & DEV TOOLS', items: [
    {slug: 'claudecode',   label: 'Claude Code',  subfolder: 'devtools'},
    {slug: 'codex',        label: 'Codex',        subfolder: 'devtools'},
    {slug: 'claude-api',   label: 'Claude API',   subfolder: 'devtools'},
    {slug: 'deepseek-api', label: 'Deepseek API', subfolder: 'devtools'},
  ]},
];

const DEFAULT_PROJECTS = [
  {name: 'Zhihu Immersive Reader', url: 'https://6767.chat/zhihu-immersive-reader/', status: 'Live',
   desc: 'Immersive reading script for Zhihu, featuring ad-blocking, AI summaries, and Markdown exports.'},
  {name: 'Sanguosha Voice & Lines', url: 'https://6767.chat/sgs', status: 'Live',
   desc: 'Interactive quote library for Sanguosha game, featuring dialogue search, audio playback, and admin panel.'},
  {name: 'AIED DuoGrow SaaS', url: 'https://github.com/connectedGraph/AIED-DuoGrow-SaaS', status: 'Build',
   desc: 'Lightweight English learning web app with parent-child feedback loops and AI grading.'},
];

const state = {
  component: 'overview',
  previewMode: 'both',                  // both | dark | light
  params: {
    typewriter: {animation_duration: 12},
    avatar:     {ring_color_1: '#7aa2f7', ring_color_2: '#bb9af3', ring_color_3: '#7dcfff', pulse_duration: 4},
    thinking:   {sweep_color: '#22d3ee', spin_duration: 2.4},
    tech_stack: {categories: deepClone(DEFAULT_TS_CATS)},
    projects:   {projects: deepClone(DEFAULT_PROJECTS)},
  },
  iconManifest: [],                     // [{slug, label, subfolder, color}]
};

const COMPONENT_LABELS = {
  overview:            'Overview',
  typewriter:          'Terminal Animation',
  avatar:              'Avatar',
  thinking:            'Thinking UI',
  tech_stack:          'Tech Stack',
  projects:            'Projects',
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

const OVERVIEW_GROUPS = [
  {label: 'Hero', items: ['typewriter', 'avatar', 'thinking']},
  {label: 'Sections', items: ['tech_stack', 'projects', 'api_docs', 'ask_me_badge', 'footer']},
  {label: 'Headers', items: ['header_tech_stack', 'header_projects', 'header_public_apis',
                             'header_stats', 'header_roadmap', 'header_ask_me']},
];

// ── DOM helpers ────────────────────────────────────────────────────────────────
const $  = id => document.getElementById(id);
const $$ = sel => document.querySelectorAll(sel);
function deepClone(o) { return JSON.parse(JSON.stringify(o)); }
function debounce(fn, ms = 350) {
  let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}

// ── Sidebar nav ────────────────────────────────────────────────────────────────
function bindNav() {
  $$('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      $$('.nav-item').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const comp = btn.dataset.component;
      state.component = comp;
      $('previewLabel').textContent = COMPONENT_LABELS[comp] || comp;
      showControls(comp);
      switchView(comp);
    });
  });
}

function showControls(component) {
  $$('[id^="ctrl-"]').forEach(el => el.classList.add('hidden'));

  const map = {
    overview:   'ctrl-overview',
    typewriter: 'ctrl-typewriter',
    avatar:     'ctrl-avatar',
    thinking:   'ctrl-thinking',
    tech_stack: 'ctrl-tech_stack',
    projects:   'ctrl-projects',
  };
  const id = map[component] || 'ctrl-generic';
  const el = $(id);
  if (el) el.classList.remove('hidden');

  // Hide action buttons on Overview
  $('ctrlActions').style.display = (component === 'overview') ? 'none' : '';
}

function switchView(component) {
  const isOverview = (component === 'overview');
  $('previewDual').classList.toggle('hidden', isOverview);
  $('overviewGallery').classList.toggle('hidden', !isOverview);
  $('refreshPreviewBtn').style.display = isOverview ? 'none' : '';
  $('bothTag').textContent = isOverview ? 'Build All to populate' : modeTag();
  if (isOverview) {
    loadOverview();
  } else {
    requestPreview();
  }
}

function modeTag() {
  if (state.previewMode === 'both')  return 'Both themes';
  if (state.previewMode === 'dark')  return 'Dark only';
  return 'Light only';
}

// ── Preview mode segmented control ─────────────────────────────────────────────
$$('#previewModeSeg .seg-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    $$('#previewModeSeg .seg-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.previewMode = btn.dataset.mode;
    applyPreviewMode();
  });
});

function applyPreviewMode() {
  const dual = $('previewDual');
  dual.classList.remove('mode-dark', 'mode-light');
  if (state.previewMode !== 'both') dual.classList.add(`mode-${state.previewMode}`);

  // Overview cards
  $$('#overviewGrid .ov-pair-wrap').forEach(w => {
    w.classList.remove('mode-dark', 'mode-light');
    if (state.previewMode !== 'both') w.classList.add(`mode-${state.previewMode}`);
  });

  $('bothTag').textContent = (state.component === 'overview') ? 'Build All to populate' : modeTag();
}

// ── Slider wiring ──────────────────────────────────────────────────────────────
function wireSlider(sliderId, valId, paramKey, key, suffix = 's', decimals = 0) {
  const slider = $(sliderId);
  const valEl  = $(valId);
  if (!slider) return;
  slider.addEventListener('input', () => {
    const v = parseFloat(slider.value);
    valEl.textContent = decimals ? `${v.toFixed(decimals)}${suffix}` : `${v}${suffix}`;
    state.params[paramKey][key] = v;
    debouncedPreview();
  });
}
wireSlider('tw-duration', 'tw-duration-val', 'typewriter', 'animation_duration', 's');
wireSlider('av-pulse',    'av-pulse-val',    'avatar',     'pulse_duration',     's', 1);

const thSpin = $('th-spin');
if (thSpin) {
  thSpin.addEventListener('input', () => {
    const v = parseFloat(thSpin.value);
    $('th-spin-val').textContent = `${v.toFixed(1)}s`;
    state.params.thinking.spin_duration = v;
    debouncedPreview();
  });
}

// ── Color pickers ──────────────────────────────────────────────────────────────
['av-ring1', 'av-ring2', 'av-ring3'].forEach((id, i) => {
  const el = $(id);
  if (!el) return;
  el.addEventListener('input', () => {
    state.params.avatar[`ring_color_${i + 1}`] = el.value;
    debouncedPreview();
  });
});

const thSweep = $('th-sweep');
if (thSweep) {
  thSweep.addEventListener('input', () => {
    state.params.thinking.sweep_color = thSweep.value;
    debouncedPreview();
  });
}

// ── Preset chips ───────────────────────────────────────────────────────────────
$$('.chip[data-target]').forEach(chip => {
  chip.addEventListener('click', () => {
    const targetId = chip.dataset.target;
    const slider   = $(targetId);
    if (!slider) return;
    slider.value = chip.dataset.val;
    slider.dispatchEvent(new Event('input'));
    $$(`.chip[data-target="${targetId}"]`).forEach(s => s.classList.remove('active'));
    chip.classList.add('active');
  });
});
$$('.chip[data-color]').forEach(chip => {
  chip.addEventListener('click', () => {
    const pickerId = chip.dataset.picker;
    const picker   = $(pickerId);
    if (picker) {
      picker.value = chip.dataset.color;
      picker.dispatchEvent(new Event('input'));
    }
    $$(`.chip[data-picker="${pickerId}"]`).forEach(s => s.classList.remove('active'));
    chip.classList.add('active');
  });
});
$$('.chip-preset').forEach(chip => {
  chip.addEventListener('click', () => {
    const set = (id, v) => {
      const el = $(id);
      if (el) { el.value = v; el.dispatchEvent(new Event('input')); }
    };
    set('av-ring1', chip.dataset.r1);
    set('av-ring2', chip.dataset.r2);
    set('av-ring3', chip.dataset.r3);
    $$('.chip-preset').forEach(s => s.classList.remove('active'));
    chip.classList.add('active');
  });
});

// ── Single-component preview ───────────────────────────────────────────────────
function setLoading(c) {
  c.innerHTML = `<div class="preview-placeholder"><div class="spinner"></div><span>Generating...</span></div>`;
}
function setSvg(c, dataUri) {
  c.innerHTML = `<img src="${dataUri}" alt="preview" draggable="false"/>`;
}
function setError(c, msg) {
  c.innerHTML = `<div class="preview-placeholder" style="color:#f7768e">! ${escapeHtml(msg)}</div>`;
}
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
}

function paramsForCurrentComponent() {
  return state.params[state.component] || {};
}

async function fetchPreview(theme) {
  if (state.component === 'overview') return;
  const container = theme === 'dark' ? $('darkPreview') : $('lightPreview');
  if (!container) return;
  setLoading(container);
  try {
    const res = await fetch('/api/preview', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        component: state.component,
        theme,
        params: paramsForCurrentComponent(),
      }),
    });
    const data = await res.json();
    if (data.error) setError(container, data.error);
    else setSvg(container, data.svg);
  } catch (e) {
    setError(container, e.message);
  }
}

function requestPreview() {
  fetchPreview('dark');
  fetchPreview('light');
}
const debouncedPreview = debounce(requestPreview, 320);

$('previewBtn').addEventListener('click', requestPreview);
$('refreshPreviewBtn').addEventListener('click', () => {
  const btn = $('refreshPreviewBtn');
  btn.classList.add('spin');
  setTimeout(() => btn.classList.remove('spin'), 650);
  if (state.component === 'overview') loadOverview();
  else requestPreview();
});

// ── Build Component ────────────────────────────────────────────────────────────
$('buildComponentBtn').addEventListener('click', async () => {
  if (state.component === 'overview') return;
  const btn = $('buildComponentBtn');
  btn.disabled = true;
  const original = btn.innerHTML;
  btn.textContent = 'Building...';
  for (const theme of ['dark', 'light']) {
    await fetch('/api/preview', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        component: state.component,
        theme,
        params: paramsForCurrentComponent(),
        write_to_project: true,
      }),
    });
  }
  btn.disabled = false;
  btn.innerHTML = original;
  requestPreview();
  showLog([`OK Built ${COMPONENT_LABELS[state.component]} (dark + light)`]);
});

// ── Build All ──────────────────────────────────────────────────────────────────
async function runBuildAll() {
  const btn = $('buildAllBtn');
  btn.classList.add('loading');
  const original = btn.innerHTML;
  btn.innerHTML = `<div class="spinner" style="width:14px;height:14px;border-width:2px;border-top-color:#1a1b26;border-color:rgba(26,27,38,0.3);"></div> Building...`;

  try {
    const res = await fetch('/api/build-all', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({params: state.params}),
    });
    const data = await res.json();
    if (data && data.results) {
      $('modalMsg').textContent = data.results.join('\n');
      $('buildModal').classList.remove('hidden');
      showLog(data.results);
    }
    if (state.component === 'overview') loadOverview();
    else requestPreview();
  } catch (e) {
    alert('Build failed: ' + e.message);
  } finally {
    btn.classList.remove('loading');
    btn.innerHTML = original;
  }
}
$('buildAllBtn').addEventListener('click', runBuildAll);

// ── Build log ──────────────────────────────────────────────────────────────────
function showLog(lines) {
  $('buildLog').style.display = 'block';
  $('buildLogBody').innerHTML = lines.map(l => `<div>${escapeHtml(l)}</div>`).join('');
}
$('buildLogClose').addEventListener('click', () => { $('buildLog').style.display = 'none'; });

// ── Modal ──────────────────────────────────────────────────────────────────────
$('modalClose').addEventListener('click', () => $('buildModal').classList.add('hidden'));
$('modalGoOverview').addEventListener('click', () => {
  $('buildModal').classList.add('hidden');
  document.querySelector('.nav-overview').click();
});
$('buildModal').addEventListener('click', e => {
  if (e.target === $('buildModal')) $('buildModal').classList.add('hidden');
});
$('overviewBuildAll').addEventListener('click', runBuildAll);

// ── Overview gallery ───────────────────────────────────────────────────────────
async function loadOverview() {
  const empty = $('overviewEmpty');
  const grid  = $('overviewGrid');
  grid.innerHTML = '';
  empty.classList.remove('hidden');
  grid.classList.add('hidden');
  try {
    const res  = await fetch('/api/all-previews');
    const data = await res.json();
    const dark  = data.dark  || {};
    const light = data.light || {};

    let nonEmpty = false;
    OVERVIEW_GROUPS.forEach(group => {
      const groupHtml = [];
      group.items.forEach(key => {
        if (!dark[key] && !light[key]) return;
        nonEmpty = true;
        groupHtml.push(`
          <div class="ov-pair-wrap ${state.previewMode !== 'both' ? 'mode-' + state.previewMode : ''}">
            <div class="ov-pair">
              <div class="ov-name">${escapeHtml(COMPONENT_LABELS[key] || key)}</div>
              <div class="ov-cell dark">${dark[key]  ? `<img src="${dark[key]}"  alt=""/>` : '<span style="color:#565f89;font-size:11px">no dark output</span>'}</div>
              <div class="ov-cell light">${light[key] ? `<img src="${light[key]}" alt=""/>` : '<span style="color:#565f89;font-size:11px">no light output</span>'}</div>
            </div>
          </div>`);
      });
      if (groupHtml.length) {
        grid.insertAdjacentHTML('beforeend', `<div class="ov-section-label">${group.label}</div>${groupHtml.join('')}`);
      }
    });

    // Badges
    const dBadges = (dark.badges  || []);
    const lBadges = (light.badges || []);
    if (dBadges.length || lBadges.length) {
      nonEmpty = true;
      grid.insertAdjacentHTML('beforeend', `<div class="ov-section-label">Social Badges</div>`);
      grid.insertAdjacentHTML('beforeend', `
        <div class="ov-pair-wrap ${state.previewMode !== 'both' ? 'mode-' + state.previewMode : ''}">
          <div class="ov-pair">
            <div class="ov-name">Badges</div>
            <div class="ov-cell dark"><div class="ov-badges">${dBadges.map(b => `<img src="${b.svg}" alt="${escapeHtml(b.name)}"/>`).join('')}</div></div>
            <div class="ov-cell light"><div class="ov-badges">${lBadges.map(b => `<img src="${b.svg}" alt="${escapeHtml(b.name)}"/>`).join('')}</div></div>
          </div>
        </div>`);
    }

    if (nonEmpty) {
      empty.classList.add('hidden');
      grid.classList.remove('hidden');
    }
  } catch (e) {
    console.error(e);
  }
}

// ── Tech Stack editor ──────────────────────────────────────────────────────────
function renderTsEditor() {
  const root = $('tsCats');
  root.innerHTML = '';
  state.params.tech_stack.categories.forEach((cat, ci) => {
    const card = document.createElement('div');
    card.className = 'ts-cat';
    card.innerHTML = `
      <div class="ts-cat-head">
        <input class="ts-cat-title" value="${escapeHtml(cat.title)}" maxlength="20" data-ci="${ci}"/>
        <button class="btn-tiny" data-action="remove-cat" data-ci="${ci}">Remove</button>
      </div>
      <div class="ts-items" data-ci="${ci}">
        ${cat.items.map((it, ii) => tsPillHtml(ci, ii, it)).join('')}
      </div>
      <button class="btn-tiny add" data-action="pick-icons" data-ci="${ci}">+ Icons</button>
    `;
    root.appendChild(card);
  });
  // Wire title edits
  root.querySelectorAll('.ts-cat-title').forEach(inp => {
    inp.addEventListener('input', () => {
      const ci = parseInt(inp.dataset.ci, 10);
      state.params.tech_stack.categories[ci].title = inp.value;
      debouncedPreview();
    });
  });
  // Wire actions
  root.querySelectorAll('[data-action]').forEach(btn => {
    btn.addEventListener('click', () => {
      const ci = parseInt(btn.dataset.ci, 10);
      const action = btn.dataset.action;
      if (action === 'remove-cat') {
        state.params.tech_stack.categories.splice(ci, 1);
        renderTsEditor();
        debouncedPreview();
      } else if (action === 'pick-icons') {
        openIconPicker({
          mode: 'multi',
          selected: state.params.tech_stack.categories[ci].items.map(it => it.slug),
          onConfirm: (slugs) => {
            const byMan = Object.fromEntries(state.iconManifest.map(m => [m.slug, m]));
            state.params.tech_stack.categories[ci].items = slugs.map(s => {
              const m = byMan[s];
              return m
                ? {slug: m.slug, label: m.label, subfolder: m.subfolder}
                : {slug: s, label: s, subfolder: 'code'};
            });
            renderTsEditor();
            debouncedPreview();
          }
        });
      }
    });
  });
  // Wire pill remove
  root.querySelectorAll('.ts-pill .x').forEach(x => {
    x.addEventListener('click', () => {
      const ci = parseInt(x.dataset.ci, 10);
      const ii = parseInt(x.dataset.ii, 10);
      state.params.tech_stack.categories[ci].items.splice(ii, 1);
      renderTsEditor();
      debouncedPreview();
    });
  });
}
function tsPillHtml(ci, ii, item) {
  const url = `/static/icon/${item.subfolder}/${item.slug}.svg`;
  return `
    <span class="ts-pill" title="${escapeHtml(item.slug)}">
      <img src="${url}" onerror="this.style.display='none'"/>
      ${escapeHtml(item.label)}
      <button class="x" data-ci="${ci}" data-ii="${ii}" title="remove">x</button>
    </span>`;
}
$('tsAddCat').addEventListener('click', () => {
  if (state.params.tech_stack.categories.length >= 3) {
    alert('Maximum 3 columns');
    return;
  }
  state.params.tech_stack.categories.push({title: 'NEW', items: []});
  renderTsEditor();
  debouncedPreview();
});

// ── Projects editor ────────────────────────────────────────────────────────────
function renderProjEditor() {
  const root = $('projList');
  root.innerHTML = '';
  state.params.projects.projects.forEach((p, idx) => {
    const card = document.createElement('div');
    card.className = 'proj-item';
    card.innerHTML = `
      <input class="text-input" data-idx="${idx}" data-key="name" value="${escapeHtml(p.name||'')}" placeholder="Project name"/>
      <div class="proj-row">
        <input class="text-input" data-idx="${idx}" data-key="url" value="${escapeHtml(p.url||'')}" placeholder="https://..."/>
        <select class="select-input" data-idx="${idx}" data-key="status">
          ${['Live','Build','Lab','Wip','Idea'].map(s =>
            `<option value="${s}" ${p.status===s?'selected':''}>${s}</option>`).join('')}
        </select>
      </div>
      <textarea class="textarea-input" data-idx="${idx}" data-key="desc" placeholder="One-line description">${escapeHtml(p.desc||'')}</textarea>
      <button class="btn-tiny" data-idx="${idx}" data-action="remove-proj" style="align-self:flex-end;">Remove</button>
    `;
    root.appendChild(card);
  });
  root.querySelectorAll('[data-key]').forEach(el => {
    const evt = el.tagName === 'SELECT' ? 'change' : 'input';
    el.addEventListener(evt, () => {
      const idx = parseInt(el.dataset.idx, 10);
      const key = el.dataset.key;
      state.params.projects.projects[idx][key] = el.value;
      debouncedPreview();
    });
  });
  root.querySelectorAll('[data-action="remove-proj"]').forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = parseInt(btn.dataset.idx, 10);
      state.params.projects.projects.splice(idx, 1);
      renderProjEditor();
      debouncedPreview();
    });
  });
}
$('projAdd').addEventListener('click', () => {
  state.params.projects.projects.push({name: 'New project', url: '', status: 'Lab', desc: ''});
  renderProjEditor();
  debouncedPreview();
});

// ── Icon Picker ────────────────────────────────────────────────────────────────
const iconPickerCtx = {selected: new Set(), onConfirm: null, folder: 'all'};

function openIconPicker({mode = 'multi', selected = [], onConfirm}) {
  iconPickerCtx.selected = new Set(selected);
  iconPickerCtx.onConfirm = onConfirm;
  iconPickerCtx.folder = 'all';
  $('iconSearch').value = '';
  renderIconFolders();
  renderIconGrid('');
  $('iconPicker').classList.remove('hidden');
}
function closeIconPicker() { $('iconPicker').classList.add('hidden'); }

function renderIconFolders() {
  const folders = Array.from(new Set(state.iconManifest.map(i => i.subfolder))).sort();
  const root = $('iconFolders');
  root.innerHTML = '';
  ['all', ...folders].forEach(f => {
    const c = document.createElement('button');
    c.className = 'chip' + (iconPickerCtx.folder === f ? ' active' : '');
    c.textContent = f === 'all' ? 'All' : f;
    c.addEventListener('click', () => {
      iconPickerCtx.folder = f;
      renderIconFolders();
      renderIconGrid($('iconSearch').value);
    });
    root.appendChild(c);
  });
}
function renderIconGrid(query) {
  const grid = $('iconGrid');
  grid.innerHTML = '';
  const q = (query || '').toLowerCase().trim();
  const list = state.iconManifest.filter(i => {
    if (iconPickerCtx.folder !== 'all' && i.subfolder !== iconPickerCtx.folder) return false;
    if (q && !i.label.toLowerCase().includes(q) && !i.slug.toLowerCase().includes(q)) return false;
    return true;
  });
  list.forEach(i => {
    const cell = document.createElement('div');
    cell.className = 'icon-cell' + (iconPickerCtx.selected.has(i.slug) ? ' picked' : '');
    cell.innerHTML = `
      <img src="/static/icon/${i.subfolder}/${i.slug}.svg" alt="" onerror="this.style.opacity=0.2"/>
      <span>${escapeHtml(i.label)}</span>
    `;
    cell.addEventListener('click', () => {
      if (iconPickerCtx.selected.has(i.slug)) iconPickerCtx.selected.delete(i.slug);
      else iconPickerCtx.selected.add(i.slug);
      cell.classList.toggle('picked');
    });
    grid.appendChild(cell);
  });
  if (!list.length) {
    grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:30px;color:#565f89;font-size:12px;">No icons match.</div>`;
  }
}

$('iconSearch').addEventListener('input', e => renderIconGrid(e.target.value));
$('iconPickerClose').addEventListener('click', closeIconPicker);
$('iconPickerDone').addEventListener('click', () => {
  if (iconPickerCtx.onConfirm) iconPickerCtx.onConfirm(Array.from(iconPickerCtx.selected));
  closeIconPicker();
});
$('iconPicker').addEventListener('click', e => {
  if (e.target === $('iconPicker')) closeIconPicker();
});

// ── Bootstrap ──────────────────────────────────────────────────────────────────
async function loadIconManifest() {
  try {
    const res = await fetch('/api/icons');
    state.iconManifest = await res.json();
  } catch (e) {
    console.warn('Could not load icon manifest:', e);
    state.iconManifest = [];
  }
}

(async function init() {
  bindNav();
  await loadIconManifest();
  renderTsEditor();
  renderProjEditor();
  showControls('overview');
  switchView('overview');
})();
