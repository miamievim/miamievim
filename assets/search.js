(function () {
  'use strict';
  // Ana sayfadaki ilan arama çubuğu. MLS ilanları Cervera'nın IDX arama sayfasında açılır;
  // seçilen kriterler "ev-arama" formuyla ilan uyarısı için saklanır.
  var IDX = 'https://aleynabozoklar.com/search/#!/defaultsearch:true';
  var root = document.getElementById('ev-ara');
  if (!root) return;
  var form = document.getElementById('ps-form'), q = document.getElementById('ps-q');
  var state = { mode: 'satilik', fiyat: '', yatak: '', tip: '' };

  function $all(sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }

  $all('.ps-tabs button').forEach(function (b) {
    b.addEventListener('click', function () {
      state.mode = b.getAttribute('data-mode');
      $all('.ps-tabs button').forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); });
      $all('[data-sale]').forEach(function (c) { c.textContent = c.getAttribute(state.mode === 'kiralik' ? 'data-rent' : 'data-sale'); });
    });
  });

  $all('.ps-line:not(.ps-filters) .ps-chip').forEach(function (c) {
    c.addEventListener('click', function () { q.value = c.getAttribute('data-q'); q.focus(); });
  });

  $all('.ps-group').forEach(function (g) {
    var k = g.getAttribute('data-k');
    Array.prototype.forEach.call(g.querySelectorAll('.ps-chip'), function (c) {
      c.setAttribute('aria-pressed', 'false');
      c.addEventListener('click', function () {
        var on = c.getAttribute('aria-pressed') !== 'true';
        Array.prototype.forEach.call(g.querySelectorAll('.ps-chip'), function (x) { x.setAttribute('aria-pressed', 'false'); });
        c.setAttribute('aria-pressed', on ? 'true' : 'false');
        state[k] = on ? c.textContent : '';
      });
    });
  });

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var parts = [state.mode === 'kiralik' ? 'Kiralık' : 'Satılık'];
    if (q.value.trim()) parts.push(q.value.trim());
    if (state.fiyat) parts.push(state.fiyat);
    if (state.yatak) parts.push(state.yatak + ' yatak');
    if (state.tip) parts.push(state.tip);
    var crit = document.getElementById('ps-crit');
    if (crit) crit.value = parts.join(' · ');
    window.open(IDX, '_blank', 'noopener');
    var after = document.getElementById('ps-after');
    if (after) { after.hidden = false; }
  });
})();
