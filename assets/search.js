(function () {
  'use strict';
  // Ana sayfadaki ilan arama çubuğu: kriterleri /ilanlar/ sayfasına taşır.
  // (MLS IDX bağlantısı kurulduğunda bu sayfa gerçek ilan sonuçlarını gösterecek.)
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
    var p = new URLSearchParams();
    p.set('islem', state.mode);
    if (q.value.trim()) p.set('q', q.value.trim());
    if (state.fiyat) p.set('fiyat', state.fiyat);
    if (state.yatak) p.set('yatak', state.yatak);
    if (state.tip) p.set('tip', state.tip);
    location.href = '/ilanlar/?' + p.toString();
  });
})();
