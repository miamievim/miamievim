# -*- coding: utf-8 -*-
"""/rehberler/neden-miami/ sayfasını üretir (şablon: rehberler/index.html).

Rakamlar kaynak ve tarihleriyle birlikte burada tutulur; güncellerken kaynağı da güncelleyin.
Kullanım: python3 tools/build_why_miami.py
"""
import html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
URL = 'https://miamievim.com/rehberler/neden-miami/'
UPDATED_ISO, UPDATED = '2026-10-19', '19 Ekim 2026'

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
}


def a(k, text=None):
    t, u = SRC[k]
    return f'<a href="{u}" target="_blank" rel="noopener">{E(text or t)}</a>'


STATS = [
    ('%0', 'Eyalet gelir vergisi', f'Florida kişisel gelir vergisi almaz. Kaynak: {a("dor", "Florida Department of Revenue")}.'),
    ('55,3 milyon', 'MIA yolcusu (2025)', f'Bunun 24,9 milyonu (%45) uluslararası yolcu. Kaynak: {a("mia", "MIA Facts at a Glance")}.'),
    ('172', 'Direkt uçuş noktası', f'92 havayolu ile, Ağustos 2026 itibarıyla. Kaynak: {a("mia", "MIA Facts at a Glance")}.'),
    ('2,80 milyon', 'Miami-Dade nüfusu', f'1 Temmuz 2025 tahmini; 2020\'den bu yana %3,7 artış. Kaynak: {a("census", "U.S. Census Bureau")}.'),
]

SECTIONS = [
    ('01', 'Vergi avantajı', [
        'Florida, ABD\'de kişisel gelir vergisi almayan eyaletlerden biridir. Florida Department of Revenue\'nun ifadesiyle eyalet kişisel gelir vergisi uygulanmadığı için bireylerin eyalete gelir vergisi beyannamesi verme yükümlülüğü yoktur; şirketlerin ise beyan yükümlülükleri vardır.',
        'Bu, federal vergilerin ortadan kalktığı anlamına gelmez: ABD federal gelir vergisi, yabancı satıcılar için FIRPTA stopajı ve emlak vergisi geçerlidir. Emlak vergisi bölgeden bölgeye değişir; her bölgenin oranını <a href="/mahalle-raporlari/">mahalle raporlarında</a> bulabilirsiniz.',
    ], ['dor']),
    ('02', 'Dünyaya bağlantı', [
        'Miami Uluslararası Havalimanı (MIA) 2025\'te 55.314.661 yolcuya hizmet verdi; bunun 24.850.064\'ü (%45) uluslararası yolcuydu. Ağustos 2026 itibarıyla 92 havayolu 172 noktaya direkt sefer yapıyor.',
        'İstanbul ile Miami arasında Türk Hava Yolları\'nın direkt seferi var; 2026 tarifesinde sefer günlük ve uçuş süresi yaklaşık 12,5–13 saat.',
        'PortMiami, 1 Ekim 2024–30 Eylül 2025 mali yılında 8.564.225 kruvaziyer yolcusuyla rekor kırdı. Kara tarafında Brightline treni Eylül 2023\'ten bu yana Miami\'yi Aventura, Fort Lauderdale, Boca Raton ve West Palm Beach üzerinden yaklaşık 3,5 saatte Orlando Havalimanı\'na bağlıyor.',
    ], ['mia', 'tk', 'port', 'bl']),
    ('03', 'Büyüyen bir şehir bölgesi', [
        'ABD Nüfus Bürosu\'nun 1 Temmuz 2025 tahminine göre Miami-Dade County\'nin nüfusu 2.802.029; bu, Nisan 2020\'ye göre %3,7 artış demek. Broward ve Palm Beach ile birlikte Güney Florida, ülkenin en büyük metropol bölgelerinden birini oluşturur.',
        'Turizm de bölge ekonomisinin büyük ayaklarından biri: Greater Miami Convention & Visitors Bureau\'ya göre Temmuz 2024–Haziran 2025 döneminde Miami-Dade 28,2 milyon ziyaretçi ağırladı (yıllık %4,5 artış) ve ziyaretçi harcaması 21,3 milyar dolara ulaştı.',
    ], ['census', 'gmcvb']),
    ('04', 'Yaşam kalitesi', [
        'İklim: National Weather Service\'in 1991–2020 normallerine göre Miami Havalimanı\'nda yıllık ortalama sıcaklık yaklaşık 25°C; ocakta yaklaşık 20°C, ağustosta yaklaşık 29°C. Haziran–kasım arası kasırga sezonudur; bu yüzden sigorta ve bina yaşı satın alma kararında önemlidir.',
        'Sağlık: Miami Üniversitesi\'ne bağlı Bascom Palmer Eye Institute, U.S. News 2026 sıralamasında göz hastalıkları dalında üst üste 23. kez ülkenin 1 numarası seçildi.',
        'Kültür ve etkinlik: Art Basel Miami Beach her aralık şehri uluslararası sanat dünyasının merkezine dönüştürür. 2026 FIFA Dünya Kupası\'nda Hard Rock Stadium, üçüncülük maçı dahil yedi maça ev sahipliği yaptı.',
    ], ['nws', 'bp', 'ab', 'wc']),
    ('05', 'Emlak açısından ne anlama geliyor?', [
        'Güçlü uluslararası bağlantı, büyüyen nüfus ve yıl boyu süren talep; Miami\'yi hem oturmak hem yatırım için takip edilen bir pazar yapıyor. Yine de fiyat, kira ve maliyetler mahalleden mahalleye çok değişir: aynı bütçe iki farklı bölgede bambaşka bir aidat, sigorta ve vergi yükü anlamına gelebilir.',
        'Karar vermeden önce <a href="/mahalle-raporlari/">108 bölgenin raporlarına</a>, <a href="/yeni-projeler/">yeni projelere</a> ve <a href="/yatirim/">net getiri hesaplayıcısına</a> göz atabilirsiniz.',
    ], []),
]

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
             'dateModified': UPDATED_ISO, 'datePublished': UPDATED_ISO, 'image': 'https://miamievim.com/assets/og-image.png',
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
    stats = ''.join(f'<div class="ruled"><span class="big">{E(b)}</span><h3>{E(h)}</h3><p>{p}</p></div>' for b, h, p in STATS)
    secs = ''
    for n, h, ps, srcs in SECTIONS:
        src = (f'<p class="wm-src">Kaynak: ' + ' · '.join(a(k) for k in srcs) + '</p>') if srcs else ''
        secs += f'''
      <div class="wm-row">
        <div class="wm-h"><span class="wm-n">{n}</span><h2>{E(h)}</h2></div>
        <div class="wm-b">{''.join(f"<p>{p}</p>" for p in ps)}{src}</div>
      </div>'''
    faq = ''.join(f'<details class="faq-item"><summary>{E(q)}</summary><div class="a"><p>{E(ans)}</p></div></details>' for q, ans in FAQ)
    srclist = ''.join(f'<li>{a(k)}</li>' for k in SRC)
    main = f'''<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow"><a href="/rehberler/" style="color:inherit">Rehberler</a> · Neden Miami?</p>
      <h1>Neden <em>Miami?</em></h1>
      <p class="lead">Vergi, ulaşım, nüfus ve yaşam kalitesi: Miami\'yi oturmak ve yatırım için öne çıkaran başlıklar, her rakam kaynağı ve tarihiyle. Son güncelleme: {UPDATED}.</p>
      <nav class="subtabs" aria-label="Rehberler alt menüsü"><a href="/rehberler/">Tüm rehberler</a><a href="/rehberler/neden-miami/" aria-current="page">Neden Miami?</a></nav>
    </div>
  </section>

  <section class="section white">
    <div class="wrap">
      <div class="grid-3 wm-stats">{stats}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap wm">{secs}
    </div>
  </section>

  <section class="section bone">
    <div class="wrap">
      <div class="section-head"><div class="stack"><p class="eyebrow">Sık sorulan sorular</p><h2>Kısa <em>cevaplar</em></h2></div></div>
      <div class="faq">{faq}</div>
      <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:48px">
        <a class="btn" href="/mahalle-raporlari/">Mahalle raporlarını inceleyin</a>
        <a class="btn btn-line" href="/#iletisim">Tanışma görüşmesi planlayın</a>
      </div>
      <h3 class="wm-srch">Kaynaklar</h3>
      <ol class="wm-srcs">{srclist}</ol>
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
