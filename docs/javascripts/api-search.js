// API command palette: Ctrl+K search over domains + raw AXL, from a
// build-time generated docs/assets/api-index.json. Instant-navigation safe.
(function () {
  var index = null;
  var palette = null;
  var list = null;
  var input = null;

  function token(name) {
    return getComputedStyle(document.body).getPropertyValue(name).trim();
  }

  function siteRoot() {
    // Resolve the site root from the canonical/extra-css link, falling back
    // to the first path segment. Works for top-level and nested pages.
    var link = document.querySelector('link[rel="stylesheet"][href*="stylesheets/fonts.css"]');
    if (link) return link.href.replace(/stylesheets\/fonts\.css.*$/, '');
    var canonical = document.querySelector('link[rel="canonical"]');
    if (canonical) return canonical.href;
    var path = window.location.pathname;
    return path.slice(0, path.indexOf('/', 1) + 1) || '/';
  }

  function ensureIndex() {
    if (index) return Promise.resolve(index);
    return fetch(siteRoot() + 'assets/api-index.json')
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (data) { index = data; return data; })
      .catch(function () { index = []; return []; });
  }

  function build() {
    palette = document.createElement('div');
    palette.className = 'ab-palette';
    palette.setAttribute('role', 'dialog');
    palette.innerHTML =
      '<div class="ab-palette-box">' +
      '<input class="ab-palette-input" type="text" placeholder="Search domains and raw AXL…  (domain:components mode:write)" aria-label="API search">' +
      '<div class="ab-palette-list"></div>' +
      '</div>';
    document.body.appendChild(palette);
    input = palette.querySelector('.ab-palette-input');
    list = palette.querySelector('.ab-palette-list');
    input.addEventListener('input', render);
    input.addEventListener('keydown', onKey);
    list.addEventListener('click', function (e) {
      var row = e.target.closest('.ab-palette-row');
      if (row) go(parseInt(row.dataset.i, 10));
    });
    list.addEventListener('mousemove', function (e) {
      var row = e.target.closest('.ab-palette-row');
      if (row) { active = parseInt(row.dataset.i, 10); markActive(); }
    });
    palette.addEventListener('click', function (e) { if (e.target === palette) close(); });
  }

  function matches(entry, terms) {
    return terms.every(function (t) {
      if (t.indexOf('domain:') === 0) return entry.kind === 'domain' && entry.name.indexOf(t.slice(7)) === 0;
      if (t.indexOf('mode:') === 0) return (entry.capabilities || []).indexOf(t.slice(5)) >= 0;
      if (t.indexOf('layer:') === 0) return entry.layer === t.slice(6);
      return entry.name.toLowerCase().indexOf(t) >= 0 || (entry.summary || '').toLowerCase().indexOf(t) >= 0;
    });
  }

  function render() {
    if (!index) return;
    var q = input.value.trim().toLowerCase();
    var terms = q ? q.split(/\s+/) : [];
    var hits = index.filter(function (e) { return matches(e, terms); }).slice(0, 24);
    active = 0;
    current = hits;
    list.innerHTML = hits.map(function (e, i) {
      var caps = (e.capabilities || []).map(function (c) { return c.toUpperCase(); }).join(' · ');
      var badge = e.kind === 'domain'
        ? '<span class="ab-pk" style="color:' + token('--ab-selection') + '">DOMAIN</span>'
        : '<span class="ab-pk" style="color:' + token('--ab-raw') + '">AXL</span>';
      return '<div class="ab-palette-row" data-i="' + i + '" role="option">' + badge +
        '<span class="ab-pn">' + e.name + '</span>' +
        (caps ? '<span class="ab-pc">' + caps + '</span>' : '') +
        (e.summary ? '<span class="ab-ps">' + e.summary.slice(0, 72) + '…</span>' : '') +
        '</div>';
    }).join('') || '<div class="ab-palette-empty">no match</div>';
    markActive();
    list.scrollTop = 0;
  }

  var active = 0;
  var current = [];

  function markActive() {
    var rows = list.querySelectorAll('.ab-palette-row');
    rows.forEach(function (r, i) { r.classList.toggle('ab-active', i === active); });
    var row = rows[active];
    if (row) row.scrollIntoView({ block: 'nearest' });
  }

  function go(i) {
    var entry = current[i];
    if (!entry) return;
    var url = entry.kind === 'domain'
      ? 'reference/domain-apis.md'
      : 'guide/raw-axl.md';
    window.location.href = siteRoot() + url.replace(/\.md$/, '/') + '#' + entry.name.toLowerCase();
    close();
  }

  function onKey(e) {
    if (e.key === 'Escape') { close(); return; }
    if (e.key === 'ArrowDown') { e.preventDefault(); active = Math.min(active + 1, current.length - 1); markActive(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); active = Math.max(active - 1, 0); markActive(); }
    else if (e.key === 'Enter') { e.preventDefault(); go(active); }
  }

  function open() {
    if (!palette) build();
    palette.style.display = 'flex';
    ensureIndex().then(render);
    input.value = '';
    input.focus();
  }

  function close() {
    if (palette) palette.style.display = 'none';
  }

  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (palette && palette.style.display === 'flex') close(); else open();
    }
  });
})();
