# -*- coding: utf-8 -*-
"""/rehberler/neden-miami/ sayfasını üretir (şablon: rehberler/index.html).

Rakamlar kaynak ve tarihleriyle birlikte burada tutulur; güncellerken kaynağı da güncelleyin.
Kullanım: python3 tools/build_why_miami.py
"""
import html, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
URL = 'https://miamievim.com/rehberler/neden-miami/'
UPDATED_ISO, UPDATED = '2026-10-28', '28 Ekim 2026'

SRC = {
    'dor': ('Florida Department of Revenue: Kişisel gelir vergisi beyannamesi', 'https://floridarevenue.com/faq/Pages/FAQDetails.aspx?FAQID=1466'),
    'mia': ('Miami International Airport: Facts at a Glance (Ağustos 2026)', 'https://www.miami-airport.com/library/pdfdoc/Facts%20at%20a%20Glance/Facts-at-a-Glance_2026.pdf'),
    'tk': ('FlightMapper: TK 77 İstanbul–Miami tarifesi (2026)', 'https://info.flightmapper.net/flight/Turkish_Airlines_TK_77'),
    'port': ('CruiseHive: PortMiami 2025 mali yılı yolcu rekoru (2 Aralık 2025)', 'https://www.cruisehive.com/portmiami-cruise-passenger-numbers-hit-unprecedented-levels/193632'),
    'bl': ('Wikipedia: Brightline (Miami–Orlando hattı ve duraklar)', 'https://en.wikipedia.org/wiki/Brightline'),
    'census': ('U.S. Census Bureau: QuickFacts, Miami-Dade County (V2025)', 'https://www.census.gov/quickfacts/miamidadecountyflorida'),
    'gmcvb': ('Greater Miami Convention & Visitors Bureau: 2025 yıllık toplantı açıklaması (6 Kasım 2025)', 'https://www.gmcvb.com/press/miami-press-releases/2025-spotlights-and-2026-outlook'),
    'nws': ('National Weather Service Miami: Günlük iklim normalleri 1991–2020, MIA', 'https://www.weather.gov/media/mfl/climate/Daily%20Normals%20(1991-2020)%20-%20MIA.pdf'),
    'bp': ('Ophthalmology Times: U.S. News 2026 göz hastanesi sıralaması (4 Ağustos 2026)', 'https://www.ophthalmologytimes.com/view/us-news-reveals-top-ranked-hospitals-for-eye-care-in-2026'),
    'wc': ('Yahoo News: Miami 2026 Dünya Kupası maçları', 'https://news.yahoo.com/miami-host-2026-world-cup-215722837.html'),
    'ab': ('Art Basel: Miami Beach', 'https://www.artbasel.com/miami-beach'),
    'ft': ('Florida Trend: A region golden with global business (7 Kasım 2019)', 'https://www.floridatrend.com/article/28235/a-region-golden-with-global-business'),
    'gdp': ('Wikipedia: ABD metropol alanlarının GSYH listesi (2024, BEA ilçe verileri)', 'https://en.wikipedia.org/wiki/List_of_United_States_metropolitan_areas_by_GDP'),
}


def a(k, text=None):
    t, u = SRC[k]
    return f'<a href="{u}" target="_blank" rel="noopener">{E(text or t)}</a>'


ICON = {
 'pct': '<path d="M5 19 19 5"/><circle cx="7" cy="7" r="2.2"/><circle cx="17" cy="17" r="2.2"/>',
 'bank': '<path d="M3 10h18L12 4 3 10zM5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>',
 'globe': '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.6 2.6 2.6 14.4 0 17M12 3.5c-2.6 2.6-2.6 14.4 0 17"/>',
 'chart': '<path d="M4 20V4M4 20h16M8 16v-4M12 16V8M16 16v-6"/>',
 'plane': '<path d="M21 15.5 13.5 11V5.5a1.5 1.5 0 0 0-3 0V11L3 15.5v2l7.5-2.3V19l-2 1.5v1.5l3.5-1 3.5 1v-1.5l-2-1.5v-3.8l7.5 2.3z"/>',
 'route': '<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.5"/>',
 'ship': '<path d="M3 17c2 2 4 2 6 0 2 2 4 2 6 0 2 2 4 2 6 0M5 14l1-5h12l1 5M8 9V6h8v3M12 3v3"/>',
 'train': '<rect x="6" y="3" width="12" height="13" rx="3"/><path d="M6 10h12M9 20l-2 2M15 20l2 2M9 13h.01M15 13h.01"/>',
 'heart': '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
 'art': '<circle cx="12" cy="12" r="8.5"/><circle cx="8.5" cy="10" r="1"/><circle cx="12" cy="7.5" r="1"/><circle cx="15.5" cy="10" r="1"/><path d="M12 20.5c-1.5 0-2-1.5-1-2.5s0-2.5-1.5-2.5"/>',
 'ball': '<circle cx="12" cy="12" r="8.5"/><path d="m12 7 3.5 2.5-1.3 4h-4.4l-1.3-4z"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/>',
 'people': '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.4"/><path d="M3.5 19c.6-3.3 2.8-5 5.5-5s4.9 1.7 5.5 5M14.5 14.6c2.6-.6 5 .9 5.8 4.4"/>',
 'trend': '<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>',
 'bag': '<rect x="4" y="7" width="16" height="13" rx="2"/><path d="M9 7V5a3 3 0 0 1 6 0v2"/>',
 'wallet': '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M16 14.5h2"/>',
}


def icon(k):
    return f'<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>'


INTRO = [
    'Florida, ABD\'de kişisel gelir vergisi almayan eyaletlerden biridir; bu, Miami\'yi hem yaşamak hem yatırım yapmak için düşünen alıcılar açısından en çok konuşulan avantajlardan biri. ' + a('dor', 'Florida Department of Revenue') + ' bunu açıkça belirtir.',
    'Miami, uluslararası bir iş ve finans merkezinin kozmopolit temposunu, yıl boyu güneşli bir sahil şehrinin rahatlığıyla birleştirir. Aşağıda bu tabloyu oluşturan başlıkları, her rakamın kaynağı ve tarihiyle bulabilirsiniz.',
]

# (no, başlık, [görseller], [(ikon, başlık, metin, kaynak anahtarları)])
SECTIONS = [
    ('01', 'Gelişen bir iş ve finans merkezi', [('misc', 'downtown'), ('hood', 'brickell', 0), ('misc', 'knight')], [
        ('pct', 'Eyalet gelir vergisi yok', 'Florida kişisel gelir vergisi almaz; ABD federal gelir vergisi ve emlak vergisi ise geçerlidir.', ['dor']),
        ('bank', 'Uluslararası bankacılık', 'Güney Florida, ABD\'nin ikinci büyük uluslararası bankacılık merkezi olarak anılır (2019).', ['ft']),
        ('globe', '1.400\'den fazla çok uluslu şirket', 'Üç ilçeden oluşan bölgede faaliyet gösteren çok uluslu şirket sayısı; Latin Amerika\'ya açılan bir kapı (2019).', ['ft']),
        ('chart', 'Yaklaşık 575 milyar dolarlık ekonomi', 'Miami–Fort Lauderdale–West Palm Beach metropol alanının 2024 GSYH\'si; ABD\'de 12. sırada.', ['gdp']),
    ]),
    ('02', 'Dünyaya bağlantı', [('misc', 'mia'), ('misc', 'port'), ('misc', 'brightline')], [
        ('plane', 'Miami Uluslararası Havalimanı', '2025\'te 55,3 milyon yolcu, bunların %45\'i uluslararası; Ağustos 2026 itibarıyla 92 havayolu ile 172 noktaya direkt uçuş.', ['mia']),
        ('route', 'İstanbul\'a direkt sefer', 'Türk Hava Yolları İstanbul–Miami arasında günlük direkt sefer yapıyor; uçuş yaklaşık 12,5–13 saat (2026 tarifesi).', ['tk']),
        ('ship', 'PortMiami', '1 Ekim 2024–30 Eylül 2025 mali yılında 8.564.225 kruvaziyer yolcusuyla rekor.', ['port']),
        ('train', 'Brightline', 'Eylül 2023\'ten bu yana Miami\'yi Aventura, Fort Lauderdale, Boca Raton ve West Palm Beach üzerinden yaklaşık 3,5 saatte Orlando\'ya bağlıyor.', ['bl']),
    ]),
    ('03', 'Dünya standartlarında yaşam', [('misc', 'pamm'), ('misc', 'southbeach'), ('misc', 'um')], [
        ('heart', 'Sağlık', 'Miami Üniversitesi\'ne bağlı Bascom Palmer Eye Institute, U.S. News 2026 sıralamasında göz hastalıklarında üst üste 23. kez ABD\'nin 1 numarası.', ['bp']),
        ('art', 'Sanat ve kültür', 'Art Basel Miami Beach her aralık şehri uluslararası sanat dünyasının buluşma noktasına dönüştürür.', ['ab']),
        ('ball', 'Spor', '2026 FIFA Dünya Kupası\'nda Hard Rock Stadium, üçüncülük maçı dahil yedi maça ev sahipliği yaptı.', ['wc']),
        ('sun', 'İklim', 'Yıllık ortalama sıcaklık yaklaşık 25°C; ocakta yaklaşık 20°C, ağustosta yaklaşık 29°C (1991–2020 normalleri). Haziran–kasım arası kasırga sezonudur.', ['nws']),
    ]),
    ('04', 'Büyüyen bir şehir', [('misc', 'skyline4'), ('misc', 'bay')], [
        ('people', '2,80 milyon kişi', 'Miami-Dade County\'nin 1 Temmuz 2025 nüfus tahmini: 2.802.029.', ['census']),
        ('trend', '%3,7 büyüme', 'Nisan 2020\'den Temmuz 2025\'e Miami-Dade nüfus artışı.', ['census']),
        ('bag', '28,2 milyon ziyaretçi', 'Temmuz 2024–Haziran 2025 döneminde Miami-Dade\'i ziyaret edenler (yıllık %4,5 artış).', ['gmcvb']),
        ('wallet', '21,3 milyar dolar harcama', 'Aynı dönemde ziyaretçilerin bölgede yaptığı toplam harcama.', ['gmcvb']),
    ]),
]
VALUE = ('05', 'Emlak açısından ne anlama geliyor?', [('hood', 'sunny-isles', 0), ('hood', 'coral-gables', 1), ('hood', 'fort-lauderdale', 0)])


FAQ = [
    ('Miami\'de gelir vergisi var mı?', 'Florida eyaleti kişisel gelir vergisi almaz (Florida Department of Revenue). Ancak ABD federal gelir vergisi, emlak vergisi ve yabancı satıcılar için FIRPTA stopajı geçerlidir. Bu bilgi genel niteliktedir, vergi tavsiyesi değildir.'),
    ('İstanbul\'dan Miami\'ye direkt uçuş var mı?', 'Evet. Türk Hava Yolları İstanbul–Miami arasında direkt sefer yapıyor; 2026 tarifesinde sefer günlük ve uçuş süresi yaklaşık 12,5–13 saat.'),
    ('Miami-Dade\'in nüfusu ne kadar?', 'ABD Nüfus Bürosu\'nun 1 Temmuz 2025 tahminine göre 2.802.029; Nisan 2020\'ye göre %3,7 artış.'),
]


def main():
    tpl = open(os.path.join(ROOT, 'rehberler', 'index.html'), encoding='utf-8').read()
    head_end = tpl.index('</head>')
    body_start = tpl[tpl.index('<body>'):tpl.index('<main id="main">')]
    footer = tpl[tpl.index('</main>') + len('</main>'):]
    title = 'Neden Miami? Vergi, Ulaşım, Nüfus ve Yaşam (2026) | Aleyna Bozoklar'
    desc = 'Miami neden tercih ediliyor? Florida\'da eyalet gelir vergisi yok, MIA\'dan 172 noktaya direkt uçuş, İstanbul\'a günlük sefer ve büyüyen nüfus. Kaynaklı ve tarihli Türkçe rehber.'
    head = tpl[:tpl.index('<title>')]
    css_links = re.findall(r'<link rel="(?:preconnect|stylesheet|icon|apple-touch-icon)"[^>]*>', tpl[:head_end])
    ld = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'Article', 'headline': 'Neden Miami? Vergi, ulaşım, nüfus ve yaşam', 'inLanguage': 'tr', 'url': URL,
             'dateModified': UPDATED_ISO, 'datePublished': UPDATED_ISO, 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Miami_skyline_from_the_ocean.jpg/1280px-Miami_skyline_from_the_ocean.jpg',
             'author': {'@type': 'Person', '@id': 'https://miamievim.com/#aleyna', 'name': 'Aleyna Bozoklar'},
             'publisher': {'@type': 'Person', '@id': 'https://miamievim.com/#aleyna', 'name': 'Aleyna Bozoklar'},
             'citation': [u for _, u in SRC.values()]},
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Ana sayfa', 'item': 'https://miamievim.com/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Rehberler', 'item': 'https://miamievim.com/rehberler/'},
                {'@type': 'ListItem', 'position': 3, 'name': 'Neden Miami?', 'item': URL}]},
            {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ans}} for q, ans in FAQ]},
        ]}
    meta = f'''<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="Neden Miami?">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://miamievim.com/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0F0F0F">
{chr(10).join(css_links)}
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
'''
    import imglib
    def pic(spec, w=960):
        rec = imglib.misc(spec[1]) if spec[0] == 'misc' else imglib.hood(spec[1])[spec[2]]
        used.append(rec)
        u = imglib.url(rec, w if rec[3] else None)
        return f'<figure><img src="{u}" alt="" loading="lazy" decoding="async" width="{rec[1]}" height="{rec[2]}"></figure>'
    used = []
    hero_rec = imglib.misc('hero'); used.append(hero_rec)
    secs = ''
    for n, h, pics, feats in SECTIONS:
        fh = ''.join(f'<div class="wm-f">{icon(ic)}<h3>{E(t)}</h3><p>{E(txt)}</p><p class="wm-fsrc">Kaynak: {" · ".join(a(k) for k in ks)}</p></div>' for ic, t, txt, ks in feats)
        secs += f'''
  <section class="wm-sec">
    <div class="wrap">
      <p class="wm-num">{n}</p>
      <h2 class="wm-title">{E(h)}</h2>
      <div class="wm-strip wm-strip-{len(pics)}">{''.join(pic(x) for x in pics)}</div>
      <div class="wm-feats">{fh}</div>
    </div>
  </section>'''
    vn, vh, vpics = VALUE
    secs += f'''
  <section class="wm-sec">
    <div class="wrap">
      <p class="wm-num">{vn}</p>
      <h2 class="wm-title">{E(vh)}</h2>
      <div class="wm-strip wm-strip-3">{''.join(pic(x) for x in vpics)}</div>
      <div class="wm-value">
        <p>Güçlü uluslararası bağlantı, büyüyen nüfus ve yıl boyu süren talep, Miami\'yi hem oturmak hem yatırım için takip edilen bir pazar yapıyor. Yine de fiyat, kira ve maliyetler mahalleden mahalleye çok değişir: aynı bütçe iki farklı bölgede bambaşka bir aidat, sigorta ve vergi yükü anlamına gelebilir.</p>
        <div class="wm-links"><a class="btn" href="/mahalle-raporlari/">108 bölgenin raporları</a><a class="btn btn-line" href="/yeni-projeler/">Yeni projeler</a><a class="btn btn-line" href="/yatirim/">Net getiri hesaplayıcısı</a></div>
      </div>
    </div>
  </section>'''
    faq = ''.join(f'<details class="faq-item"><summary>{E(q)}</summary><div class="a"><p>{E(ans)}</p></div></details>' for q, ans in FAQ)
    srclist = ''.join(f'<li>{a(k)}</li>' for k in SRC)
    intro = ''.join(f'<p>{x}</p>' for x in INTRO)
    main = f'''<main id="main">
  <section class="wm-hero" style="background-image:linear-gradient(rgba(10,10,10,.28),rgba(10,10,10,.55)),url('{imglib.url(hero_rec, 1280)}')">
    <div class="wrap">
      <p class="eyebrow"><a href="/rehberler/">Rehberler</a> · Neden Miami?</p>
      <h1>Neden <em>Miami?</em></h1>
      <nav class="subtabs" aria-label="Rehberler alt menüsü"><a href="/rehberler/">Tüm rehberler</a><a href="/rehberler/neden-miami/" aria-current="page">Neden Miami?</a></nav>
    </div>
  </section>

  <section class="wm-intro">
    <div class="wrap">{intro}<p class="wm-upd">Son güncelleme: {UPDATED}</p></div>
  </section>
{secs}

  <section class="section bone">
    <div class="wrap">
      <div class="section-head"><div class="stack"><p class="eyebrow">Sık sorulan sorular</p><h2>Kısa <em>cevaplar</em></h2></div></div>
      <div class="faq">{faq}</div>
      <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:48px">
        <a class="btn" href="/mahalle-testi/">Size uygun mahalleyi bulun</a>
        <a class="btn btn-line" href="/#iletisim">Tanışma görüşmesi planlayın</a>
      </div>
      <h3 class="wm-srch">Kaynaklar</h3>
      <ol class="wm-srcs">{srclist}</ol>
      {imglib.credits_html(used)}
      <p class="wm-note">Bu sayfa genel bilgilendirme amaçlıdır; vergi, hukuk veya yatırım tavsiyesi değildir. Kendi durumunuz için bir vergi danışmanı veya avukata başvurun.</p>
    </div>
  </section>
</main>'''
    out = head + meta + body_start.replace('<a href="/rehberler/">Rehberler</a>', '<a href="/rehberler/" aria-current="page">Rehberler</a>') + main + footer
    d = os.path.join(ROOT, 'rehberler', 'neden-miami')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'stamp_assets.py')], check=True)
    print('neden-miami ok')


if __name__ == '__main__':
    main()
