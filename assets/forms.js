/* Netlify formları: gönderimi arka planda yapar, ardından formun o anki action adresine gider.
   Neden: Aynı adı taşıyan formlarda (ör. her mahallenin "mahalle-raporu" formu) Netlify,
   gönderimden sonra yayın sırasında kaydettiği tek bir başarı sayfasına yönlendirir; bu da
   ziyaretçiyi başka bir mahallenin raporuna götürebilir. */
(function () {
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || f.tagName !== 'FORM' || f.getAttribute('data-netlify') !== 'true' || e.defaultPrevented) return;
    if (typeof window.fetch !== 'function' || typeof window.URLSearchParams !== 'function') return; // eski tarayıcı: normal gönderim
    e.preventDefault();
    var target = f.getAttribute('action') || '/tesekkurler/';
    var btn = f.querySelector('button[type="submit"], button:not([type])');
    if (btn) { btn.disabled = true; }
    var data = new FormData(f);
    if (!data.get('form-name') && f.getAttribute('name')) data.append('form-name', f.getAttribute('name'));
    var body = new URLSearchParams(data).toString();
    var post = function (url) { return fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body }).then(function (r) { if (!r.ok) throw new Error(r.status); }); };
    // Ziyaretçi her durumda formun kendi adresine gider; Netlify'ın kayıtlı başarı sayfasına asla düşmez.
    post('/')
      .catch(function () { return post(target).catch(function () {}); })
      .then(function () { window.location.assign(target); });
  });
})();
