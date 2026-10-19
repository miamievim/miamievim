# -*- coding: utf-8 -*-
"""Yeni Projeler sayfasını tools/projects.json verisinden üretir.

Kullanım: python3 tools/build_projects.py   (repo kökünden)
Mevcut yeni-projeler/index.html dosyasının <head>, üst menü ve alt bilgi bölümleri korunur;
yalnızca <main> içeriği ve sayfa betiği yeniden yazılır.
"""
import json, os, re, html
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'yeni-projeler', 'index.html')
E = html.escape

AREAS = [
    ('brickell', 'Brickell'),
    ('downtown', 'Downtown'),
    ('edgewater', 'Edgewater · Wynwood · Midtown'),
    ('miami-beach', 'Miami Beach ve sahil'),
    ('coconut-grove', 'Coconut Grove'),
    ('coral-gables', 'Coral Gables'),
]
AREA_NAME = dict(AREAS)
CAT = {'ULTRA-LUXURY': 'Ultra lüks', 'PREMIUM': 'Premium', 'LUXURY': 'Lüks', 'SHORT-TERM RENTAL': 'Kısa süreli kiralamaya uygun'}
CAT_KEY = {'ULTRA-LUXURY': 'ultra', 'PREMIUM': 'premium', 'LUXURY': 'luks', 'SHORT-TERM RENTAL': 'kisa'}
WATER = {'beachfront': 'Okyanus cepheli', 'bayfront': 'Körfez cepheli', 'bay views': 'Körfez manzaralı', 'riverfront': 'Nehir cepheli',
         'bay and river views': 'Körfez ve nehir manzaralı', 'urban core': 'Şehir merkezinde'}
SUBLOC = [('Fisher Island', 'Fisher Island'), ('Surfside', 'Surfside'), ('Surf Club', 'Surfside'), ('Bal Harbour', 'Bal Harbour'),
          ('Sunny Isles', 'Sunny Isles Beach'), ('Bentley', 'Sunny Isles Beach'), ('South Beach', 'South Beach'), ('Raleigh', 'South Beach'),
          ('Shore Club', 'South Beach'), ('Wynwood', 'Wynwood'), ('Midtown', 'Midtown'), ('Nomad', 'Wynwood'), ('Cloud One', 'Wynwood'),
          ('Rider', 'Wynwood'), ('26 & 2', 'Wynwood'), ('LILLI', 'Edgewater'), ('Villa Miami', 'Edgewater'), ('Edition', 'Edgewater'),
          ('Cove Miami', 'Edgewater'), ('Edge House', 'Edgewater'), ('7200 Collins', 'North Beach'), ('72 Carlyle', 'North Beach'),
          ('72 Park', 'North Beach'), ('NoBe', 'North Beach'), ('Ocean Terrace', 'North Beach'), ('Mandarin Oriental', 'Brickell Key'),
          ('Faena', 'Miami River')]


def status(s):
    s = (s or '').lower().replace('constrction', 'construction')
    if 'deliver' in s: return ('teslim', 'Teslim edildi')
    if 'construction' in s: return ('insaat', 'İnşaat sürüyor')
    if 'launch' in s: return ('lansman', 'Lansman öncesi')
    if 'pre' in s and 'sale' in s: return ('onsatis', 'Ön satış')
    return ('', s.title())


def completion(c, st):
    c = (c or '').replace('Est.', '').strip()
    m = re.match(r'Q([1-4])\s*(\d{4})', c)
    if m:
        q, y = int(m.group(1)), int(m.group(2))
        label, sortv = f'Q{q} {y}', y * 10 + q
    else:
        m = re.search(r'(\d{4})', c)
        if not m: return ('Açıklanmadı', 99999, '', '')
        y = int(m.group(1)); label, sortv = str(y), y * 10 + 4
    year = y
    note = 'tarih güncelleniyor' if (st != 'teslim' and sortv < 20263) else ''
    return (label, sortv, str(year), note)


def money(n):
    return '$' + f'{int(round(n)):,}'.replace(',', '.')


def price(p):
    m = re.search(r'\$([\d,]+)\s*/\s*SF', p or '')
    if not m: return None
    return int(m.group(1).replace(',', ''))


def maint(m):
    m2 = re.search(r'\$([\d.]+)', m or '')
    if not m2: return None
    v = float(m2.group(1))
    return v if 0.5 <= v <= 5 else None


def beds(b):
    b = (b or '').strip()
    if not b or b.upper() in ('N/A', 'NA'): return ''
    b = b.replace('–', '-').replace('—', '-')
    rep = [(r'\bBedrooms?\b', 'yatak odası'), (r'\bBeds?\b', 'yatak odası'), (r'\bBR\b', 'yatak odası'), (r'\bStudios?\b', 'Stüdyo'),
           (r'\bPenthouses?\b', 'penthouse'), (r'\bplus\b', 've'), (r'\bJr\.?\s*Suite\b', 'Junior suit'), (r'\bJr\b', 'Junior'),
           (r'\bOffice\b', 'ofis'), (r'\band\b', 've'), (r'\bDen\b', 'çalışma odası'), (r'\bprivate\b', 'özel'), (r'Hotel Collection', 'otel koleksiyonu'),
           (r'Garden Estate', 'bahçe dairesi'), (r'Duplex Loft', 'dubleks loft')]
    for a, c in rep:
        b = re.sub(a, c, b, flags=re.I)
    b = re.sub(r'\s*-\s*', '–', b)
    if re.fullmatch(r'[\d–+ ]+', b): b += ' yatak odası'
    return b


MONTHS = {'january': 'Ocak', 'february': 'Şubat', 'feb': 'Şubat', 'march': 'Mart', 'april': 'Nisan', 'may': 'Mayıs', 'june': 'Haziran',
          'july': 'Temmuz', 'august': 'Ağustos', 'september': 'Eylül', 'october': 'Ekim', 'november': 'Kasım', 'december': 'Aralık'}
PHRASES = [
    (r'\(\s*est\.?[^)]*\)', ''),
    (r'\best\.?\s*', ''),
    (r'\b(commencement of )?(vertical )?pou?ting\b', 'pouring'),
    (r'\b(commenced |upon |at )?(the )?pouring of (the )?(grade floor slab)', 'zemin kat döşemesinde'),
    (r'\b(commenced |upon |at )?(the )?pouring of (the )?floor slab on which residence is located', 'dairenin bulunduğu kat dökülünce'),
    (r'\b(commenced |upon |at )?(the )?pouring of (the )?(\d+)(st|nd|rd|th)? (floor|level)', r'\4. kat dökülünce'),
    (r'\b(commencement of )?pouring (of )?(the )?(\d+)(st|nd|rd|th)? (floor|level)', r'\4. kat dökülünce'),
    (r'\b(upon |at )?(the )?pouring of (the )?rooftop( floor)?', 'çatı katı dökülünce'),
    (r'\b(at )?(the )?(\d+)(st|nd|rd|th)? (floor|level)( concrete)?( pour| amenity level)?', r'\3. katta'),
    (r'\bvertical pour\b', 'dikey inşaat başlangıcında'),
    (r'\b(at )?(the )?(amenity (deck|level)|pool deck level)', 'sosyal alan katında'),
    (r'\b(at |completion of )?(the )?podium\b', 'podyum tamamlanınca'),
    (r'\b(at )?(the )?(residence level)', 'daire katında'),
    (r'\b(at |upon )?(the )?rooftop\b', 'çatı katında'),
    (r'\b(at )?(building )?top[\s-]*off\b|\btopoff\b', 'kaba inşaat bitiminde'),
    (r'\b(at )?ground\s*breaking\b|\bground breakin\b|\bgrounbreaking\b|\bGB\b', 'temel atmada'),
    (r'\b(at )?reservation agreement\b', 'rezervasyon sözleşmesinde'), (r'\b(at )?reservation\b', 'rezervasyonda'),
    (r'\b(at |with |due at |upon )?(the )?(signing of (the )?)?(purchase )?(contract|agreement)( signing| execution)?\b|\bat signing\b|\bupon signing\b|\bsigning\b|\bPSA\b', 'sözleşmede'),
    (r'\b(remaining |balance )?(due )?(at )?closings?\b|\bbalance( due)?\b|\bremaining\b', 'teslimde'),
    (r'\b(in )?(\d+)\s*days?\s*(later|after|from|thereafter)?', r'\2 gün sonra'),
    (r'\b(in )?(\d+)\s*months?\s*(later|after|from|post|thereafter)?', r'\2 ay sonra'),
    (r'\b(\d+)\s*years?\s*(later|after|from)?', r'\1 yıl sonra'),
    (r'\bone year (after|later)\b', '1 yıl sonra'),
]
OK_WORDS = {'closing', 'veya', 'bitiminde', 'kalan', 'teslimde', 'temel', 'atmada', 'atmadan', 'kaba', 'katta', 'sonra', 'sosyal', 'alan', 'podyum', 'daire', 'dikey', 'zemin', 'rezervasyonda', 'kalan'}


def tr_text(txt):
    t = ' ' + txt + ' '
    for a, b in PHRASES:
        t = re.sub(a, b, t, flags=re.I)
    t = re.sub(r'\bor\b', 'veya', t, flags=re.I)
    for ab, trm in {'oct': 'Ekim', 'nov': 'Kasım', 'dec': 'Aralık', 'jan': 'Ocak', 'sept': 'Eylül', 'aug': 'Ağustos'}.items():
        t = re.sub(r'\b' + ab + r'\b', trm, t, flags=re.I)
    for en, trm in MONTHS.items():
        t = re.sub(r'\b' + en + r'\b', trm, t, flags=re.I)
    t = re.sub(r'\b(at|the|due|of|with|upon|on|is|now|to|after|from|thereafter|later|or|and|from contract|date|deposit|post)\b', ' ', t, flags=re.I)
    t = re.sub(r'\b(sözleşmede)\s+(\d+ (gün|ay|yıl) sonra)', r'sözleşmeden \2', t)
    t = re.sub(r'(\d+ (gün|ay|yıl) sonra)\s+sözleşmede', r'sözleşmeden \1', t)
    t = re.sub(r'(\d+ (gün|ay|yıl) sonra)\s+temel atmada', r'temel atmadan \1', t)
    t = re.sub(r'(\d+ (gün|ay|yıl) sonra)\s+(\d+(\.|st|nd|rd|th)? ?(ek )?)?', r'\1 ', t)
    t = re.sub(r'\b(\w+)( \1\b)+', r'\1', t)
    t = re.sub(r'(teslimde)( teslimde)+', r'\1', t)
    t = re.sub(r'(\d+ (gün|ay|yıl) sonra)\s*-?\s*temel atmada', r'temel atmadan \1', t)
    t = re.sub(r'(Q[1-4])-\s*', r'\1 ', t)
    t = re.sub(r'[()/]', ' ', t)
    t = re.sub(r'\s-\s|\s-$|-\s', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip(' .,;:')
    # Hâlâ İngilizce kelime kaldıysa çeviri güvenilir değildir
    leftover = [w for w in t.split() if re.fullmatch(r'[A-Za-z]{4,}', w) and w.lower() not in OK_WORDS and w not in MONTHS.values()]
    return t, not leftover


def deposit_steps(d):
    d = (d or '').strip().strip('"')
    if not d or d.upper() in ('N/A', 'NA') or '%' not in d: return []
    d = re.sub(r'(?i)\b(remaining|balance)\b', ' KALAN% ', d)
    parts = re.split(r'(\d+\s?%|KALAN%)', d)
    steps = []
    carry = None
    for i in range(1, len(parts) - 1, 2):
        pct = parts[i].replace(' ', '')
        if pct == 'KALAN%':
            pct = carry or 'Kalan'
        carry = None
        txt = parts[i + 1]
        if not re.sub(r'[^A-Za-z]', '', txt):
            carry = pct
            continue
        txt = re.sub(r'[•*|→—–]+', ' ', txt)
        txt = re.sub(r'(?<!\w)-(?!\w)', ' ', txt)
        txt = re.sub(r'\(\s*\d+\s*%?\s*\)', ' ', txt)
        txt = re.sub(r'\s+', ' ', txt).strip(' .,;:')
        if not txt: continue
        if '$' in txt: return None
        t, ok = tr_text(txt)
        t = re.sub(r'^\d+\s?%\s*', '', t)
        if not ok or not t:
            return None  # çeviri güvenilir değil; plan ayrıntısı talep üzerine paylaşılır
        steps.append((pct, t[:1].upper() + t[1:]))
    return steps


def total_dep(t):
    m = re.match(r'\s*(\d+)\s*%', t or '')
    if m: return int(m.group(1))
    m = re.match(r'\s*0?\.(\d+)', t or '')
    return None


def subloc(name, area):
    for k, v in SUBLOC:
        if k.lower() in name.lower():
            return v
    return {'brickell': 'Brickell', 'downtown': 'Downtown Miami', 'edgewater': 'Edgewater · Wynwood', 'miami-beach': 'Miami Beach',
            'coconut-grove': 'Coconut Grove', 'coral-gables': 'Coral Gables'}[area]


def slug(s):
    s = s.lower()
    for a, b in [('ç', 'c'), ('ğ', 'g'), ('ı', 'i'), ('ö', 'o'), ('ş', 's'), ('ü', 'u'), ('&', 've')]:
        s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def card(p, i):
    st_key, st_lbl = status(p['status'])
    comp, comp_sort, year, comp_note = completion(p['completion'], st_key)
    pr = price(p['price_sf'])
    mt = maint(p['maint_sf'])
    bd = beds(p['bedrooms'])
    wf = WATER.get((p['waterfront'] or '').strip().lower(), '')
    loc = subloc(p['name'], p['area'])
    units = (p['units'] or '').strip()
    units = units if units.isdigit() else ''
    steps = deposit_steps(p['deposit'])
    td = total_dep(p['deposit_total'])
    sid = slug(p['name'])
    yr_bucket = year if year in ('2025', '2026', '2027', '2028') else ('2029' if year else '')
    if year and int(year) <= 2026: yr_bucket = '2026'
    price_html = (f'<b>{money(pr)}</b><small>/ ft² · ≈ {money(pr * 10.7639)} / m²</small>') if pr else '<b class="ask">Fiyat için sorun</b>'
    rows = []
    if bd: rows.append(('Daireler', E(bd)))
    if p['developer'] and p['developer'] not in ('N/A',): rows.append(('Geliştirici', E(p['developer'].strip())))
    if p['architect'] and p['architect'] not in ('N/A', 'ma'): rows.append(('Mimar', E(p['architect'].strip().rstrip(','))))
    rows_html = ''.join(f'<div class="pj-row"><dt>{a}</dt><dd>{b}</dd></div>' for a, b in rows)
    det = []
    if td: det.append(f'<p class="pj-dep"><span>Teslim öncesi toplam depozito</span><b>%{td}</b></p>')
    if steps is None:
        det.append('<p class="pj-extra">Ayrıntılı ödeme takvimi fiyat listesiyle birlikte paylaşılır.</p>')
    elif steps:
        det.append('<ol class="pj-steps">' + ''.join(f'<li><b>{("%" + E(a.rstrip("%"))) if a[0].isdigit() else E(a)}</b><span>{E(b)}</span></li>' for a, b in steps) + '</ol>')
    extra = []
    if mt: extra.append(f'Tahmini aidat: ${str(mt).replace(".", ",")} / ft² (aylık)')
    if wf: extra.append(wf)
    if extra: det.append('<p class="pj-extra">' + ' · '.join(E(x) for x in extra) + '</p>')
    details = (f'<details class="pj-more"><summary>Ödeme planı ve detaylar</summary><div>{"".join(det)}</div></details>') if det else ''
    wa = quote(f'Merhaba Aleyna Hanım, {p["name"]} projesi için fiyat listesi ve kat planı rica ediyorum.')
    search = ' '.join([p['name'], loc, p['developer'] or '', p['architect'] or '']).lower()
    return f'''
      <article class="pj" id="{sid}" data-area="{p['area']}" data-cat="{CAT_KEY.get(p['category'], '')}" data-year="{yr_bucket}" data-status="{st_key}" data-comp="{comp_sort}" data-seg="{ {'ULTRA-LUXURY': 1, 'PREMIUM': 2, 'LUXURY': 3, 'SHORT-TERM RENTAL': 4}.get(p['category'], 5) }" data-name="{E(p['name'].lower())}" data-q="{E(search)}">
        <header class="pj-top"><span class="pj-cat">{E(CAT.get(p['category'], p['category'].title()))}</span><span class="pj-st st-{st_key}">{E(st_lbl)}</span></header>
        <h3 class="pj-name">{E(p['name'])}</h3>
        <p class="pj-loc">{E(loc)}{(' · ' + E(wf)) if wf else ''}</p>
        <div class="pj-key pj-key2">
          <div><span>Tahmini teslim</span><b>{E(comp)}</b>{('<small>' + comp_note + '</small>') if comp_note else ''}</div>
          <div><span>Daire</span><b>{units or '—'}</b></div>
        </div>
        <dl class="pj-rows">{rows_html}</dl>
        {details}
        <footer class="pj-cta">
          <button type="button" class="btn pj-ask" data-proje="{E(p['name'])}">Fiyat listesi ve kat planı</button>
          <a class="pj-wa" href="https://wa.me/13059248551?text={wa}" target="_blank" rel="noopener" aria-label="{E(p['name'])} için WhatsApp'tan yazın">WhatsApp</a>
        </footer>
      </article>'''


def build():
    data = json.load(open(os.path.join(ROOT, 'tools', 'projects.json'), encoding='utf-8'))
    ps = data['projects']
    # Teslim tarihine göre sırala (varsayılan)
    def key(p):
        st, _ = status(p['status'])
        return ({'ULTRA-LUXURY': 1, 'PREMIUM': 2, 'LUXURY': 3, 'SHORT-TERM RENTAL': 4}.get(p['category'], 5), completion(p['completion'], st)[1])
    ps = sorted(ps, key=key)
    prices = [price(p['price_sf']) for p in ps if price(p['price_sf'])]
    n_build = sum(1 for p in ps if status(p['status'])[0] == 'insaat')
    n_pre = sum(1 for p in ps if status(p['status'])[0] in ('onsatis', 'lansman'))
    cards = ''.join(card(p, i) for i, p in enumerate(ps))
    area_tabs = '<button type="button" class="pf-tab" data-area="" aria-pressed="true">Tümü <span>' + str(len(ps)) + '</span></button>' + ''.join(
        f'<button type="button" class="pf-tab" data-area="{k}" aria-pressed="false">{E(v)} <span>{sum(1 for p in ps if p["area"] == k)}</span></button>' for k, v in AREAS)
    schema = {
        "@context": "https://schema.org", "@type": "ItemList", "name": "Miami yeni projeler ve markalı rezidanslar",
        "numberOfItems": len(ps),
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p['name'], "url": f"https://miamievim.com/yeni-projeler/#{slug(p['name'])}"} for i, p in enumerate(ps)]
    }
    main = f'''<main id="main" class="projects">
  <section class="page-hero pj-hero">
    <div class="wrap">
      <p class="eyebrow">Yeni projeler · Q3 2026</p>
      <h1>Miami'nin yükselen silueti, <em>tek sayfada.</em></h1>
      <p class="lead">Brickell'den Coral Gables'a, okyanus cepheli markalı rezidanslardan kısa süreli kiralamaya uygun binalara kadar {len(ps)} proje. Teslim tarihi, ödeme planı, geliştirici ve mimar bilgisi yan yana; güncel fiyat listesi ve kat planları talep üzerine.</p>
      <div class="hero-ctas" style="margin-top:32px">
        <a class="btn" href="#projeler" style="background:var(--ivory);color:var(--ink);border-color:var(--ivory)">Projeleri inceleyin</a>
        <a class="btn btn-line" href="#proje-listesi">Size uygun listeyi isteyin</a>
      </div>
    </div>
  </section>

  <section class="statband" aria-label="Özet">
    <div class="wrap"><dl class="stats">
      <div class="stat"><dt>Proje</dt><dd>{len(ps)}</dd><span>6 bölgede</span></div>
      <div class="stat"><dt>İnşaat hâlinde</dt><dd>{n_build}</dd><span>{n_pre} proje ön satışta</span></div>
      <div class="stat"><dt>Fiyat listesi</dt><dd>Talep üzerine</dd><span>kat planlarıyla birlikte</span></div>
      <div class="stat"><dt>Kaynak</dt><dd>Q3 2026</dd><span>Cervera Development Market Study</span></div>
    </dl></div>
  </section>

  <section class="pj-section" id="projeler" aria-label="Proje listesi">
    <div class="pf" id="pf">
      <div class="wrap">
        <div class="pf-tabs" role="group" aria-label="Bölge">{area_tabs}</div>
        <div class="pf-row">
          <label class="pf-search"><span class="sr-only">Proje, geliştirici veya mimar ara</span>
            <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-4-4"></path></svg>
            <input type="search" id="pf-q" placeholder="Proje, geliştirici veya mimar">
          </label>
          <div class="pf-chips" role="group" aria-label="Segment">
            <button type="button" class="pf-chip" data-cat="ultra" aria-pressed="false">Ultra lüks</button>
            <button type="button" class="pf-chip" data-cat="premium" aria-pressed="false">Premium</button>
            <button type="button" class="pf-chip" data-cat="luks" aria-pressed="false">Lüks</button>
            <button type="button" class="pf-chip" data-cat="kisa" aria-pressed="false">Kısa süreli kiralama</button>
          </div>
          <label class="pf-sel"><span>Teslim</span><select id="pf-year"><option value="">Tümü</option><option value="2026">2026 ve öncesi</option><option value="2027">2027</option><option value="2028">2028</option><option value="2029">2029 ve sonrası</option></select></label>
          <label class="pf-sel"><span>Sırala</span><select id="pf-sort"><option value="seg">Segment</option><option value="comp">Teslim tarihi</option><option value="name">Proje adı</option></select></label>
        </div>
        <p class="pf-count" aria-live="polite"><b id="pf-n">{len(ps)}</b> proje gösteriliyor <button type="button" id="pf-reset" hidden>Filtreleri temizle</button></p>
      </div>
    </div>
    <div class="wrap">
      <div class="pj-grid" id="pj-grid">{cards}
      </div>
      <p class="pj-empty" id="pj-empty" hidden>Bu filtrelere uyan proje yok. <button type="button" id="pf-reset2">Filtreleri temizleyin</button> ya da <a href="#proje-listesi">size özel liste isteyin</a>.</p>
      <p class="pj-source">Kaynak: Cervera Real Estate, Development Market Study, Market Report Q3 2026 (Haziran 2026). Fiyat listeleri ve kat planları talep üzerine paylaşılır. Teslim tarihleri, fiyatlar ve ödeme planları geliştirici tarafından değiştirilebilir ve garanti değildir. Bu sayfa yatırım tavsiyesi değildir.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head">
        <div class="stack">
          <p class="eyebrow">Ön satışta satın alma</p>
          <h2>Broşürde yazmayanlar <em>dahil.</em></h2>
        </div>
      </div>
      <div class="grid-4">
        <div class="ruled"><span class="num">01</span><h3>Ödeme planı</h3><p>Ön satışta fiyatın genellikle %30–50'si teslimden önce, inşaat aşamalarına bağlı taksitlerle ödenir; kalan tutar teslimde (closing) ödenir veya krediyle finanse edilir.</p></div>
        <div class="ruled"><span class="num">02</span><h3>Depozito güvencesi</h3><p>Florida yasasına göre ön satış depozitoları emanet (escrow) hesabında tutulur. Sözleşmede depozitonun inşaatta kullanılıp kullanılamayacağını mutlaka kontrol edin.</p></div>
        <div class="ruled"><span class="num">03</span><h3>Geliştirici ve teslim</h3><p>Geliştiricinin tamamladığı önceki projeler, gecikme geçmişi ve sözleşmedeki teslim süresi hükümleri; tarih kayarsa haklarınız ne olur?</p></div>
        <div class="ruled"><span class="num">04</span><h3>Sahip olma maliyeti</h3><p>Aidat, sigorta, emlak vergisi ve kısa süreli kiralama kuralları. Kiralama hedefi varsa binanın kurallarını satın almadan önce yazılı olarak alın.</p></div>
      </div>
      <p class="pj-source" style="margin-top:28px">Bu bilgiler genel niteliktedir; hukuki veya finansal tavsiye değildir. Sözleşme öncesi bir Florida avukatına danışmanız önerilir.</p>
    </div>
  </section>

  <section class="dark guide-band" id="proje-listesi" aria-labelledby="proj-form-title">
    <div class="wrap">
      <div class="copy">
        <p class="eyebrow">Size uygun projeler</p>
        <h2 id="proj-form-title">Bütçenize ve bölgenize göre <em>proje listesi.</em></h2>
        <p class="lead">Bütçenizi, bölgenizi ve kullanım amacınızı (oturum, yatırım, kısa süreli kiralama) yazın; size uygun projelerin fiyat listeleri, kat planları ve ödeme planı karşılaştırmasıyla dönüş yapalım.</p>
      </div>
      <form class="form" name="yeni-proje" method="POST" action="/tesekkurler/" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="yeni-proje">
        <p class="hp"><label>Bu alanı boş bırakın <input name="bot-field"></label></p>
        <div class="row">
          <label class="field">Ad soyad<input type="text" name="ad" autocomplete="name" required></label>
          <label class="field">E-posta<input type="email" name="email" autocomplete="email" required></label>
        </div>
        <div class="row">
          <label class="field">WhatsApp (isteğe bağlı)<input type="tel" name="whatsapp" autocomplete="tel" placeholder="+90 …"></label>
          <label class="field">Bütçe<select name="butce"><option>500 bin $ altı</option><option>500 bin – 1 milyon $</option><option>1 – 3 milyon $</option><option>3 – 5 milyon $</option><option>5 milyon $ üzeri</option></select></label>
        </div>
        <div class="row">
          <label class="field">Tercih ettiğiniz bölge<select name="bolge"><option>Brickell / Downtown / Edgewater</option><option>Miami Beach / Surfside / Bal Harbour</option><option>Sunny Isles / Aventura</option><option>Coconut Grove / Coral Gables</option><option>Fort Lauderdale / Broward</option><option>Boca Raton / Palm Beach</option><option>Henüz karar vermedim</option></select></label>
          <label class="field">Amaç<select name="amac"><option>Oturum</option><option>Yatırım (uzun dönem kira)</option><option>Kısa süreli kiralama</option><option>Henüz karar vermedim</option></select></label>
        </div>
        <label class="consent"><input type="checkbox" name="izin" value="evet" required><span>Benimle e-posta, telefon veya WhatsApp üzerinden iletişime geçilmesini kabul ediyorum. <a href="/gizlilik/" style="color:inherit">Gizlilik politikası</a></span></label>
        <button class="btn" type="submit">Karşılaştırmayı gönderin</button>
      </form>
    </div>
  </section>

  <dialog class="pj-dialog" id="pj-dialog" aria-labelledby="pj-dialog-t">
    <form class="form" name="proje-talebi" method="POST" action="/tesekkurler/" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="proje-talebi">
      <input type="hidden" name="proje" id="pj-dialog-proje">
      <p class="hp"><label>Bu alanı boş bırakın <input name="bot-field"></label></p>
      <p class="eyebrow">Fiyat listesi ve kat planı</p>
      <h2 id="pj-dialog-t" class="pj-dialog-name">Proje</h2>
      <p class="pj-dialog-lead">Güncel fiyat listesi, müsait daireler, kat planları ve ödeme planı e-postanıza gelsin.</p>
      <label class="field">Ad soyad<input type="text" name="ad" autocomplete="name" required></label>
      <label class="field">E-posta<input type="email" name="email" autocomplete="email" required></label>
      <label class="field">WhatsApp (isteğe bağlı)<input type="tel" name="whatsapp" autocomplete="tel" placeholder="+90 …"></label>
      <label class="consent"><input type="checkbox" name="izin" value="evet" required><span>Benimle e-posta, telefon veya WhatsApp üzerinden iletişime geçilmesini kabul ediyorum. <a href="/gizlilik/" style="color:inherit">Gizlilik politikası</a></span></label>
      <div class="pj-dialog-actions"><button class="btn" type="submit">Gönderin</button><button class="btn btn-line" type="button" id="pj-dialog-close">Vazgeç</button></div>
    </form>
  </dialog>
</main>
<script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False)}
</script>
<script src="/assets/projects.js" defer></script>
'''
    src = open(PAGE, encoding='utf-8').read()
    a = src.index('<main id="main"')
    b = src.index('<footer class="site-footer"')
    src = src[:a] + main + src[b:]
    # Eski ld+json/projeler betiği tekrar eklenmesin
    src = re.sub(r'(<script src="/assets/projects.js" defer></script>\n)(?=[\s\S]*<script src="/assets/projects.js")', '', src)
    if '/assets/projects.css' not in src:
        src = src.replace('<link rel="stylesheet" href="/assets/site.css">', '<link rel="stylesheet" href="/assets/site.css">\n<link rel="stylesheet" href="/assets/report.css">\n<link rel="stylesheet" href="/assets/projects.css">')
    src = re.sub(r'<title>[^<]*</title>', f'<title>Miami Yeni Projeler {len(ps)} Proje: Teslim, Ödeme Planı, Kat Planı (Q3 2026) | Aleyna Bozoklar</title>', src, count=1)
    src = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="Brickell, Downtown, Edgewater, Miami Beach, Coconut Grove ve Coral Gables\'ta {len(ps)} yeni proje: tahmini teslim tarihi, ödeme planı, geliştirici ve mimar; fiyat listesi ve kat planı talep üzerine. Kaynak: Cervera Q3 2026.">', src, count=1)
    open(PAGE, 'w', encoding='utf-8').write(src)
    print('built', len(ps), 'projects')


if __name__ == '__main__':
    build()
