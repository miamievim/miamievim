# -*- coding: utf-8 -*-
"""Mahalle raporlarını tools/reports/*.json dosyalarından üretir.

Kullanım: python3 tools/build_reports.py   (repo kökünden)
Her JSON dosyası bir mahalleyi tanımlar; çıktı mahalle-raporlari/<id>/index.html olur.
"""
import json, glob, os, html, re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL_SRC = os.path.join(ROOT, 'hakkimda', 'index.html')
E = html.escape
ED = json.load(open(os.path.join(ROOT, 'tools', 'edition.json'), encoding='utf-8'))
EDITION, DATE_ISO, DATE_HUMAN = ED['edition'], ED['date_iso'], ED['date_human']


def money(v):
    return '$' + f'{int(round(v)):,}'.replace(',', '.')


def nav_and_footer():
    src = open(TPL_SRC, encoding='utf-8').read()
    body_start = src[src.index('<body>'):src.index('<main id="main">')]
    body_start = body_start.replace(' aria-current="page"', '')
    body_start = body_start.replace('<a href="/mahalle-raporlari/">Mahalleler</a>', '<a href="/mahalle-raporlari/" aria-current="page">Mahalleler</a>')
    footer = src[src.index('<footer'):]
    return body_start, footer


def head(d, detail=False):
    url = f"https://miamievim.com/mahalle-raporlari/{d['id']}/" + ('detay/' if detail else '')
    title = f"{d['name']} Mahalle Raporu ({EDITION}): Fiyatlar, Kiralar, Maliyetler | Aleyna Bozoklar"
    if detail:
        title = f"{d['name']} Detaylı Mahalle Raporu · {EDITION} | Aleyna Bozoklar"
    desc = d['meta']
    faq = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d['faq']]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": f"{d['name']} Mahalle Raporu · {EDITION}", "inLanguage": "tr",
             "datePublished": DATE_ISO, "dateModified": DATE_ISO, "url": url,
             "author": {"@type": "Person", "name": "Aleyna Bozoklar", "url": "https://miamievim.com/hakkimda/"},
             "publisher": {"@type": "Organization", "name": "Miami Evim", "url": "https://miamievim.com/"},
             "about": {"@type": "Place", "name": f"{d['name']}, {d['county']} County, Florida"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": "https://miamievim.com/"},
                {"@type": "ListItem", "position": 2, "name": "Mahalle raporları", "item": "https://miamievim.com/mahalle-raporlari/"},
                {"@type": "ListItem", "position": 3, "name": d['name'], "item": url}]},
            {"@type": "FAQPage", "inLanguage": "tr", "mainEntity": faq}
        ]
    }
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{'noindex, follow' if detail else 'index, follow, max-image-preview:large'}">
<meta property="og:type" content="article">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="{E(d['name'])} Mahalle Raporu · {EDITION}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://miamievim.com/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0F0F0F">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&amp;family=Jost:wght@300;400;500&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/report.css">
{'' if detail else '<script type="application/ld+json">' + chr(10) + json.dumps(graph, ensure_ascii=False, indent=1) + chr(10) + '</script>'}
</head>
'''


def stat(label, value, note):
    return f'<div class="stat"><dt>{E(label)}</dt><dd>{value}</dd><span>{note}</span></div>'


def table(rows, head_cells):
    th = ''.join(f'<th scope="col">{E(h)}</th>' for h in head_cells)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def section(n, title, inner, sid):
    return f'''
  <section class="rsec" id="{sid}" aria-labelledby="{sid}-t">
    <div class="rnum">{n:02d}</div>
    <div class="rbody">
      <h2 id="{sid}-t">{title}</h2>
      {inner}
    </div>
  </section>'''


LOCKED = [
    ('Satış piyasası', 'Medyan fiyat, m² fiyatı, satış süresi, satış/ilan oranı ve rakamların yorumu'),
    ('Kiralar', 'Stüdyodan 3 yatak odalıya kira tablosu ve kaynak karşılaştırması'),
    ('Gizli maliyetler', 'Emlak vergisi hesabı, site aidatı (HOA), sigorta ve sel bölgesi'),
    ('Yeni projeler', 'İnşaat hâlindeki projeler, durumları ve tahmini teslim tarihleri'),
    ('Artılar ve dikkat edilecekler', 'Satın almadan veya kiralamadan önce bilmeniz gerekenler'),
]


def gate(d):
    lock = '<svg aria-hidden="true" width="12" height="14" viewBox="0 0 12 14" fill="none" stroke="currentColor" stroke-width="1.3"><rect x="1" y="6" width="10" height="7.5" rx="1"/><path d="M3.2 6V4.2a2.8 2.8 0 0 1 5.6 0V6"/></svg>'
    items = ''.join(f'<li><strong>{lock} {E(a)}</strong><span>{E(b)}</span></li>' for a, b in LOCKED)
    return f'''
  <section class="rsec rgate" id="detayli-rapor" aria-labelledby="gate-t">
    <div class="rnum">+</div>
    <div class="rbody">
      <p class="eyebrow">Ücretsiz · ad ve e-postayla</p>
      <h2 id="gate-t">Detaylı raporda neler var?</h2>
      <ul class="places locked">{items}</ul>
      <form class="form gate-inline" name="mahalle-raporu" method="POST" action="/mahalle-raporlari/{d['id']}/detay/" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="mahalle-raporu">
        <input type="hidden" name="mahalle" value="{d['id']}">
        <p class="hp"><label>Bu alanı boş bırakın <input name="bot-field"></label></p>
        <div class="row">
          <label class="field">Ad soyad<input type="text" name="ad" autocomplete="name" required></label>
          <label class="field">E-posta<input type="email" name="email" autocomplete="email" required></label>
        </div>
        <label class="consent"><input type="checkbox" name="izin" value="evet" required><span>Mahalle güncellemelerinin bana e-postayla gönderilmesini kabul ediyorum. Bilgilerim üçüncü kişilerle paylaşılmaz. <a href="/gizlilik/" style="color:inherit">Gizlilik politikası</a></span></label>
        <button class="btn" type="submit">Detaylı raporu açın</button>
      </form>
    </div>
  </section>'''


def build(d, nav, footer, detail=False):
    s, r, t = d['sales'], d['rent'], d['tax']
    m2 = s['ppsf'] * 10.7639 if s.get('ppsf') else None
    tax_pct = t['mills'] / 10
    stats = ''.join([
        stat('Medyan satış fiyatı', money(s['median']) if s.get('median') else 'Yayımlanmıyor', (f"{E(s['median_chg'])} · {E(s['src_short'])}") if s.get('median') else 'satış çok nadir'),
        stat('Metrekare fiyatı', (money(m2) + ' / m²') if m2 else '—', (f"{money(s['ppsf'])} / ft² · " + E(s['src_short'])) if m2 else E(s['src_short'])),
        stat('Ortalama kira', (money(r['avg']) + ' / ay') if r.get('avg') else 'Yetersiz veri', (f"{E(r['chg'])} · {E(r['src_short'])}") if r.get('avg') else 'kiralık ilan sayısı az'),
        stat('Emlak vergisi', (f"≈ %{tax_pct:.2f}–{t['mills_hi']/10:.2f}" if t.get('mills_hi') else f"≈ %{tax_pct:.2f}").replace('.', ','), f"vergi değerinin yıllık oranı · {E(t['src_short'])}"),
    ])
    # Tablo hücreleri güvenilir JSON kaynağından gelir; basit HTML (<strong>, <small>) içerebilir.
    sales_rows = [[k, v] for k, v in s['rows']]
    rent_rows = [[k, v] for k, v in r['rows']]
    proj_rows = [[f"<strong>{E(p[0])}</strong>", E(p[1]), E(p[2]), f'<a href="{p[3]}" target="_blank" rel="noopener">Kaynak</a>'] for p in d['projects']]
    places = ''.join(f'<li><strong>{E(a)}</strong><span>{E(b)}</span></li>' for a, b in d['places'])
    pros = ''.join(f'<li>{E(x)}</li>' for x in d['pros'])
    cons = ''.join(f'<li>{E(x)}</li>' for x in d['cons'])
    faq = ''.join(f'<details><summary>{E(q)}</summary><div class="a"><p>{E(a)}</p></div></details>' for q, a in d['faq'])
    sources = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{E(n)}</a></li>' for n, u in d['sources'])
    costs = ''.join(f'<div class="cost"><h3>{E(a)}</h3><p>{b}</p></div>' for a, b in d['costs'])
    transport = ''.join(f'<li><strong>{E(a)}</strong><span>{E(b)}</span></li>' for a, b in d['transport'])

    S = {
        'karakter': lambda n: section(n, 'Karakter ve yaşam tarzı', ''.join(f'<p>{E(p)}</p>' for p in d['character']), 'karakter'),
        'mekanlar': lambda n: section(n, 'Bilinen mekânlar ve gizli köşe', f'<ul class="places">{places}</ul>', 'mekanlar'),
        'satis': lambda n: section(n, 'Satış piyasası', table(sales_rows, ['Gösterge', 'Değer']) + f'<p class="src">Kaynak: {s["src"]}</p>' + ''.join(f'<p>{E(p)}</p>' for p in s.get('notes', [])), 'satis'),
        'kira': lambda n: section(n, 'Kiralar', table(rent_rows, ['Daire tipi', 'Ortalama aylık kira']) + f'<p class="src">Kaynak: {r["src"]}</p>' + ''.join(f'<p>{E(p)}</p>' for p in r.get('notes', [])), 'kira'),
        'maliyet': lambda n: section(n, 'Gizli maliyetler: vergi, aidat, sigorta, sel', f'<div class="costs">{costs}</div>', 'maliyet'),
        'ulasim': lambda n: section(n, 'Ulaşım ve günlük hayat', f'<ul class="places">{transport}</ul><p class="src">Mesafeler yaklaşıktır ve trafiksiz koşulları gösterir.</p>', 'ulasim'),
        'projeler': lambda n: section(n, 'Gelecek: yeni projeler', (table(proj_rows, ['Proje', 'Durum', 'Tahmini teslim', '']) if proj_rows else '') + ''.join(f'<p>{E(x)}</p>' for x in d.get('projects_notes', [])) + '<p class="src">Proje bilgileri geliştirici açıklamalarına ve basın haberlerine dayanır; teslim tarihleri değişebilir.</p>', 'projeler'),
        'artilar': lambda n: section(n, 'Artılar ve dikkat edilecekler', f'<div class="pc"><div><h3>Artılar</h3><ul>{pros}</ul></div><div><h3>Dikkat edilecekler</h3><ul>{cons}</ul></div></div>', 'artilar'),
        'sss': lambda n: section(n, 'Sık sorulan sorular', f'<div class="faq">{faq}</div>', 'sss'),
    }
    order = ['karakter', 'mekanlar', 'satis', 'kira', 'maliyet', 'ulasim', 'projeler', 'artilar', 'sss'] if detail else ['karakter', 'mekanlar', 'ulasim', 'sss']
    body = ''.join(S[k](n + 1) for n, k in enumerate(order))
    if not detail:
        body += gate(d)
    crumb_tail = (f'<a href="/mahalle-raporlari/{d["id"]}/">{E(d["name"])}</a> / <span>Detaylı rapor</span>') if detail else f'<span>{E(d["name"])}</span>'
    eyebrow = 'Detaylı mahalle raporu' if detail else 'Mahalle raporu'
    main = f'''<main id="main" class="report">
  <section class="page-hero">
    <div class="wrap">
      <nav class="crumbs" aria-label="Sayfa yolu"><a href="/">Ana sayfa</a> / <a href="/mahalle-raporlari/">Mahalle raporları</a> / {crumb_tail}</nav>
      <p class="eyebrow">{eyebrow} · {EDITION} · {E(d['county'])} County</p>
      <h1>{E(d['name'])}</h1>
      <p class="lead">{E(d['short'])}</p>
    </div>
  </section>

  <section class="statband" aria-label="Özet rakamlar">
    <div class="wrap"><dl class="stats">{stats}</dl></div>
  </section>

  <div class="wrap rwrap">
{body}
  </div>

  <section class="dark guide-band" aria-labelledby="cta-t">
    <div class="wrap">
      <div class="copy">
        <p class="eyebrow">Bir sonraki adım</p>
        <h2 id="cta-t">{E(d['name'])} size uygun mu? <em>Birlikte bakalım.</em></h2>
        <p class="lead">15 dakikalık ücretsiz görüşmede bütçenizi ve beklentilerinizi konuşalım; bu mahalledeki uygun ilanları ve binaları birlikte değerlendirelim.</p>
      </div>
      <div style="display:flex;flex-direction:column;gap:12px;flex:1 1 300px">
        <a class="btn" href="https://wa.me/13059248551?text={quote(d['wa'])}" target="_blank" rel="noopener">WhatsApp'tan yazın</a>
        <a class="btn btn-line" href="/mahalle-testi/">Mahalle testini çözün</a>
        <a class="btn btn-line" href="/mahalle-raporlari/">Diğer mahalle raporları</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      {('<h2 style="font-size:28px;margin-bottom:18px">Kaynaklar</h2><ul class="sources">' + sources + '</ul>') if detail else ''}
      <p class="src" style="margin-top:24px">Rapor tarihi: {DATE_HUMAN}. Hazırlayan: Aleyna Bozoklar, Realtor® Associate, Cervera Real Estate. Bu rapor genel bilgilendirme amaçlıdır; yatırım, hukuki veya vergi tavsiyesi değildir. Rakamlar üçüncü taraf kaynaklardan alınmıştır ve değişebilir. Mahalleler insan gruplarına göre değil, özelliklerine göre anlatılır; okul ve güvenlik bilgisi için resmi kaynaklara başvurun.</p>
    </div>
  </section>
</main>

'''
    return head(d, detail) + nav + main + footer


def all_list(reports, nav, footer):
    d = {'id': 'tum-raporlar', 'name': 'Tüm raporlar', 'county': 'Miami-Dade, Broward, Palm Beach', 'meta': f'Detaylı mahalle raporları, {EDITION}.', 'faq': []}
    h = head(d, True).replace('mahalle-raporlari/tum-raporlar/detay/', 'mahalle-raporlari/tum-raporlar/')
    h = h.replace('Tüm raporlar Detaylı Mahalle Raporu', 'Tüm Detaylı Mahalle Raporları')
    rows = ''.join(f'<li class="rrow"><div class="rmain"><span class="county">{E(r["county"])}</span><h3>{E(r["name"])}</h3></div><a class="btn btn-line" href="/mahalle-raporlari/{r["id"]}/detay/">Detaylı raporu okuyun</a></li>' for r in reports)
    main = f'''<main id="main" class="report">
  <section class="page-hero">
    <div class="wrap">
      <nav class="crumbs" aria-label="Sayfa yolu"><a href="/">Ana sayfa</a> / <a href="/mahalle-raporlari/">Mahalle raporları</a> / <span>Tüm detaylı raporlar</span></nav>
      <p class="eyebrow">Detaylı mahalle raporları · {EDITION}</p>
      <h1>Teşekkürler. <em>Tüm raporlar açık.</em></h1>
      <p class="lead">Aşağıdaki listeden istediğiniz mahallenin detaylı raporunu okuyabilirsiniz. Bu sayfayı yer imlerinize ekleyebilirsiniz.</p>
    </div>
  </section>
  <section class="section"><div class="wrap"><ol class="rlist alllist">{rows}</ol></div></section>
</main>

'''
    return h + nav + main + footer


def main():
    nav, footer = nav_and_footer()
    reports = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'reports', '*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        reports.append(d)
        out = os.path.join(ROOT, 'mahalle-raporlari', d['id'])
        os.makedirs(os.path.join(out, 'detay'), exist_ok=True)
        open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(build(d, nav, footer, False))
        open(os.path.join(out, 'detay', 'index.html'), 'w', encoding='utf-8').write(build(d, nav, footer, True))
        print('built', d['id'])
    os.makedirs(os.path.join(ROOT, 'mahalle-raporlari', 'tum-raporlar'), exist_ok=True)
    open(os.path.join(ROOT, 'mahalle-raporlari', 'tum-raporlar', 'index.html'), 'w', encoding='utf-8').write(all_list(reports, nav, footer))
    import subprocess, sys
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'stamp_assets.py')], check=True)


if __name__ == '__main__':
    main()
