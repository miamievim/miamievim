(function () {
  'use strict';
  var grid = document.getElementById('pj-grid');
  if (!grid) return;
  var cards = Array.prototype.slice.call(grid.querySelectorAll('.pj'));
  var st = { area: '', cats: [], year: '', q: '', sort: 'seg' };
  var $ = function (id) { return document.getElementById(id); };

  function apply() {
    var n = 0;
    cards.forEach(function (c) {
      var ok = (!st.area || c.dataset.area === st.area) &&
        (!st.cats.length || st.cats.indexOf(c.dataset.cat) !== -1) &&
        (!st.year || c.dataset.year === st.year) &&
        (!st.q || c.dataset.q.indexOf(st.q) !== -1);
      c.hidden = !ok; if (ok) n++;
    });
    var sorted = cards.slice().sort(function (a, b) {
      if (st.sort === 'name') return a.dataset.name.localeCompare(b.dataset.name, 'tr');
      if (st.sort === 'comp') return (+a.dataset.comp) - (+b.dataset.comp);
      return (+a.dataset.seg) - (+b.dataset.seg) || (+a.dataset.comp) - (+b.dataset.comp);
    });
    sorted.forEach(function (c) { grid.appendChild(c); });
    $('pf-n').textContent = n;
    $('pj-empty').hidden = n !== 0;
    $('pf-reset').hidden = !(st.area || st.cats.length || st.year || st.q);
  }

  Array.prototype.forEach.call(document.querySelectorAll('.pf-tab'), function (b, _, all) {
    b.addEventListener('click', function () {
      st.area = b.dataset.area;
      Array.prototype.forEach.call(document.querySelectorAll('.pf-tab'), function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      apply();
    });
  });
  Array.prototype.forEach.call(document.querySelectorAll('.pf-chip'), function (b) {
    b.addEventListener('click', function () {
      var on = b.getAttribute('aria-pressed') !== 'true';
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var k = b.dataset.cat;
      st.cats = st.cats.filter(function (x) { return x !== k; });
      if (on) st.cats.push(k);
      apply();
    });
  });
  $('pf-year').addEventListener('change', function (e) { st.year = e.target.value; apply(); });
  $('pf-sort').addEventListener('change', function (e) { st.sort = e.target.value; apply(); });
  $('pf-q').addEventListener('input', function (e) { st.q = e.target.value.trim().toLocaleLowerCase('tr'); apply(); });
  function reset() {
    st = { area: '', cats: [], year: '', q: '', sort: st.sort };
    $('pf-q').value = ''; $('pf-year').value = '';
    Array.prototype.forEach.call(document.querySelectorAll('.pf-tab'), function (x) { x.setAttribute('aria-pressed', x.dataset.area === '' ? 'true' : 'false'); });
    Array.prototype.forEach.call(document.querySelectorAll('.pf-chip'), function (x) { x.setAttribute('aria-pressed', 'false'); });
    apply();
  }
  $('pf-reset').addEventListener('click', reset);
  $('pf-reset2').addEventListener('click', reset);

  // Bölge bağlantısıyla gelindiyse (ör. /yeni-projeler/#bolge-brickell) filtreyi uygula
  var h = (location.hash || '').replace('#bolge-', '');
  if (h && h !== location.hash) {
    var t = document.querySelector('.pf-tab[data-area="' + h + '"]'); if (t) t.click();
  }

  var dlg = $('pj-dialog');
  Array.prototype.forEach.call(document.querySelectorAll('.pj-ask'), function (b) {
    b.addEventListener('click', function () {
      var name = b.dataset.proje;
      $('pj-dialog-proje').value = name;
      dlg.querySelector('.pj-dialog-name').textContent = name;
      if (dlg.showModal) dlg.showModal(); else { location.hash = 'proje-listesi'; }
    });
  });
  $('pj-dialog-close').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
})();
