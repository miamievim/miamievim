"""Rapor JSON'larındaki tüm rakamları canlı kaynak anlık görüntülerinden yeniden üretir.

Girdi:
  tools/live/redfin_2026-10.json   Redfin "Housing Market" sayfalarından okunan değerler (Eylül 2026, son 3 ay)
  tools/live/zillow_2026-10-26.json Zillow Rental Market Trends değerleri (26 Ekim 2026 güncellemesi)
  tools/live/millage_2025.json      2025 toplam vergi oranları (resmî tablolardan)
  tools/live/areas.json             Her raporun hangi Redfin ve Zillow alanını kullandığı

Üretilen alanlar: short (ilk cümle korunur), meta, sales, rent, tax, costs[0], fiyat/kira/vergi SSS'leri,
sources (Redfin, Zillow, vergi). Diğer metinler (karakter, mekanlar, ulaşım, projeler) elle yazılır.
"""
import json, os, re, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(ROOT, 'tools', 'live')
R = json.load(open(os.path.join(LIVE, 'redfin_2026-10.json'), encoding='utf-8'))
Z = {z['u']: z for z in json.load(open(os.path.join(LIVE, 'zillow_2026-10-26.json'), encoding='utf-8'))}
T = json.load(open(os.path.join(LIVE, 'millage_2025.json'), encoding='utf-8'))
A = json.load(open(os.path.join(LIVE, 'areas.json'), encoding='utf-8'))
ST = json.load(open(os.path.join(LIVE, 'rail_stations.json'), encoding='utf-8'))
HOODS = {h['id']: h for h in json.load(open(os.path.join(ROOT, 'tools', 'hoods.json'), encoding='utf-8'))}
ALL_MILLS = sorted(v[0] for v in T.values())
MARKET_WORDS = re.compile(r'\d|satış süresi|satış sayısı|fiyatlarda|fiyat artış|fiyatta|medyan|fit kare|vergi oran|belediye oran|belediye vergi|ilan fiyat|hızlı satış|pazarlık|kiralarda yıllık|satışlar ilan|uzayan satış|kısalan satış', re.I)
KEEP = {'Belediye vergisi yok'}


def km(a, b, c, d):
    import math
    R = 6371; p = math.radians
    return 2 * R * math.asin(math.sqrt(math.sin(p(c - a) / 2) ** 2 + math.cos(p(a)) * math.cos(p(c)) * math.sin(p(d - b) / 2) ** 2))


def fix_transport(d):
    h = HOODS.get(d['id'])
    if not h:
        return
    best = min(ST, key=lambda s: km(h['lat'], h['lng'], s[2], s[3]))
    dist = km(h['lat'], h['lng'], best[2], best[3])
    label = f"{best[0]} {best[1]}"
    rep = (f"en yakın raylı sistem istasyonu {label} (sınıra çok yakın)" if dist < 1.5 else f"en yakın raylı sistem istasyonu {label} (kuş uçuşu yaklaşık {round(dist)} km)")
    for row in d['transport']:
        row[1] = re.sub(r'en yakın raylı sistem istasyonu .+? \((?:yaklaşık|kuş uçuşu yaklaşık) \d+ km\)|en yakın raylı sistem istasyonu .+? \(sınıra çok yakın\)', rep, row[1])


def market_pc(d, rf, lo):
    pros = [x for x in d['pros'] if x in KEEP or not MARKET_WORDS.search(x)]
    cons = [x for x in d['cons'] if x in KEEP or not MARKET_WORDS.search(x)]
    n = len(ALL_MILLS)
    q1, q3 = ALL_MILLS[n // 4], ALL_MILLS[(3 * n) // 4]
    if lo <= q1:
        pros.append(f"Bölgedeki düşük toplam vergi oranlarından biri ({tl(lo, 2)} mill)")
    elif lo >= q3:
        cons.append(f"Bölgedeki yüksek toplam vergi oranlarından biri ({tl(lo, 2)} mill)")
    if rf and not rf.get('thin'):
        if rf.get('stl') and 100 - rf['stl'] >= 5:
            pros.append(f"Alıcıya pazarlık payı: satışlar ilan fiyatının ortalama %{tl(100 - rf['stl'], 1)} altında kapanıyor")
        if rf.get('dom') and rf['dom'] <= 60:
            pros.append(f"Likit piyasa: medyan satış süresi {rf['dom']} gün")
        if rf.get('dom') and rf['dom'] >= 140:
            cons.append(f"Uzun satış süresi (medyan {rf['dom']} gün)")
        if rf.get('sold') is not None and rf['sold'] < 15 and not any('oynak' in c or 'az' in c.lower() and 'satış' in c.lower() for c in cons):
            cons.append('Satış sayısı az; fiyat verisi oynak')
    d['pros'], d['cons'] = pros, cons

REDFIN_ACCESS = '28 Ekim 2026 erişimi'
ZILLOW_UPDATED = '26 Ekim 2026 güncellemesi'
MONTH_TR = {'January': 'Ocak', 'February': 'Şubat', 'March': 'Mart', 'April': 'Nisan', 'May': 'Mayıs', 'June': 'Haziran',
            'July': 'Temmuz', 'August': 'Ağustos', 'September': 'Eylül', 'October': 'Ekim', 'November': 'Kasım', 'December': 'Aralık'}

TAX_SRC = {
    'Miami-Dade PA 2025': [('Miami-Dade Property Appraiser: 2025 Adopted Millage Rates', 'https://www.miamidadepa.gov/resources-pa/library/reports/millage/2025-adopted-millage-chart.pdf')],
    'Broward PA 2025': [('Broward County Property Appraiser: Millage Rates (2025)', 'https://bcpa.net/millage.asp')],
    'PAPA 2025': [('Palm Beach County Property Appraiser: 2025 Proposed Total Millage Levy', 'https://pbcpao.gov/pdf/taxroll/2025_Proposed_Total_Millage_Rates_Levy.pdf'),
                  ('Palm Beach County Property Appraiser: 2025 Final vs Proposed Millage Rates', 'https://pbcpao.gov/pdf/taxroll/2025_Final_vs_Proposed_Millage_Rates.pdf')],
}
TAX_SHORT = {'Miami-Dade PA 2025': 'Miami-Dade PA, 2025', 'Broward PA 2025': 'Broward PA, 2025', 'PAPA 2025': 'Palm Beach PA, 2025'}

# Oranın konuma göre değiştiği yerler için açıklama
TAX_RANGE_NOTE = {
    'brickell': 'Miami Downtown Development Authority (DDA) sınırları içindeki mülklerde oran 20,3778 mill, dışındakilerde 19,9878 mill.',
    'downtown-miami': 'Miami Downtown Development Authority (DDA) sınırları içindeki mülklerde oran 20,3778 mill, dışındakilerde 19,9878 mill.',
    'venetian-islands': 'Adaların Miami Beach sınırları içindeki kesiminde oran 18,7601 mill, City of Miami sınırları içindeki kesiminde 19,9878 mill.',
    'boca-raton': 'Greater Boca Raton Beach & Park District sınırları içindeki mülklerde oran 17,0029 mill, dışındakilerde 15,9229 mill.',
    'palm-beach-gardens': 'Jupiter Inlet District sınırları içindeki kesimde oran 17,9330 mill, şehrin geri kalanında 17,8608 mill.',
    'west-palm-beach': 'Downtown Development Authority (DDA) bölgesindeki mülklerde oran 21,4168 mill, şehrin geri kalanında 20,4468 mill.',
    'delray-beach': 'Downtown Development Authority (DDA) bölgesindeki mülklerde oran 19,4500 mill, şehrin geri kalanında 18,4500 mill.',
}
TAX_RANGE_GENERIC = 'Oran, şehir içindeki vergi bölgesine (taxing district) göre bu aralıkta değişir; adresinizin oranını emlak değerleme ofisinin sitesinden kontrol edebilirsiniz.'


def tl(n, dec=0):
    s = f'{n:,.{dec}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def money(n):
    return '$' + tl(round(n))


def money_short(n):
    if n >= 1_000_000:
        v = n / 1_000_000
        return '$' + (tl(v, 1) if v < 10 else tl(v, 1)).rstrip('0').rstrip(',') + ' milyon'
    return '$' + tl(round(n / 1000)) + ' bin'


def pct(v):
    if v is None:
        return ''
    if v == 0:
        return '%0'
    t = ('%g' % abs(v)).replace('.', ',')
    return ('+%' if v > 0 else '−%') + t


def label_redfin(slug):
    return slug.replace('-', ' ')


def label_zillow(u, name):
    if u.isdigit():
        return f'{u} posta kodu'
    return name


def sales_block(d, rf):
    name = d['name']
    if rf is None or rf.get('thin'):
        per = rf.get('period') if rf else None
        txt = 'Son üç ayda Redfin’de güncel medyan satış fiyatı yayımlanmıyor; satış çok nadir gerçekleşiyor.'
        if rf and rf.get('sold') is not None and rf.get('period'):
            txt = f"{MONTH_TR[rf['period'].split()[0]]} {rf['period'].split()[1]} itibarıyla {rf['sold']} satış kaydı var; tekil satışların fiyat aralığı çok geniş olduğu için medyan anlamlı değil."
        elif per:
            m, y = per.split()
            txt = f"Redfin’deki son satış verisi {MONTH_TR[m]} {y} dönemine ait; son üç ayda güncel medyan yayımlanmıyor."
        rows = [['Satış verisi', txt]]
        src = (f'<a href="{rf["url"]}" target="_blank" rel="noopener">Redfin, {label_redfin(rf["slug"])} Housing Market</a>, {REDFIN_ACCESS}.') if rf else 'Satış verisi yayımlanmıyor.'
        notes = ['Satışlar çok seyrek olduğu için fiyatlar mülke göre belirlenir. Bu tür küçük yerleşimlerde değerlendirmeyi son benzer satışlar (comparable sales) üzerinden, adres bazında yapmak gerekir.']
        return {'median': None, 'median_chg': '', 'ppsf': None, 'src_short': 'Redfin', 'rows': rows, 'src': src, 'notes': notes}

    per = rf.get('period')
    per_tr = f"{MONTH_TR[per.split()[0]]} {per.split()[1]}" if per else None
    rows = []
    med = rf.get('median')
    medtxt = (('yaklaşık ' if rf.get('median_approx') else '') + money(med)) if med else '—'
    rows.append(['Medyan satış fiyatı', medtxt + (f" <small>(yıllık {pct(rf['median_chg'])})</small>" if rf.get('median_chg') is not None else '')])
    if rf.get('ppsf'):
        p = rf['ppsf']
        rows.append(['Fit kare fiyatı', ('yaklaşık ' if rf.get('ppsf_approx') else '') + f"{money(p)} / ft² ≈ {money(p * 10.7639)} / m²" + (f" <small>(yıllık {pct(rf['ppsf_chg'])})</small>" if rf.get('ppsf_chg') is not None else '')])
    if rf.get('dom'):
        rows.append(['Medyan satış süresi', f"{rf['dom']} gün" + (f" <small>(bir yıl önce {rf['dom_ly']} gün)</small>" if rf.get('dom_ly') else '')])
    if rf.get('sold') is not None:
        lab = f"Satılan konut ({per_tr})" if rf.get('sold_month') and per_tr else 'Satılan konut (son dönem)'
        extra = []
        if rf.get('sold_ly') is not None:
            extra.append(f"bir yıl önce {rf['sold_ly']}")
        rows.append([lab, f"{rf['sold']}" + (f" <small>({', '.join(extra)})</small>" if extra else '')])
    if rf.get('stl'):
        rows.append(['Satış / ilan fiyatı oranı', '%' + tl(rf['stl'], 1)])
    elif rf.get('under_list') is not None:
        rows.append(['Satış / ilan fiyatı', f"ilan fiyatının ortalama %{tl(rf['under_list'], 1)} altında"])

    if rf.get('fmt') == 'nbhd':
        src = f'<a href="{rf["url"]}" target="_blank" rel="noopener">Redfin, {label_redfin(rf["slug"])} Housing Market</a>, {REDFIN_ACCESS} (son 3 ay; Redfin bu mahalle için yuvarlanmış değer yayımlıyor).'
    else:
        src = f'<a href="{rf["url"]}" target="_blank" rel="noopener">Redfin, {label_redfin(rf["slug"])} Housing Market</a>, {REDFIN_ACCESS} ({per_tr} itibarıyla son 3 ay verisi).'

    # Yorum: yalnızca rakamlardan çıkarılabilen gözlemler
    notes = []
    s = []
    mc, pc = rf.get('median_chg'), rf.get('ppsf_chg')
    if mc is not None:
        if abs(mc) < 1:
            s.append('Medyan satış fiyatı bir yıl öncesiyle hemen hemen aynı seviyede')
        else:
            s.append(f"Medyan satış fiyatı bir yılda {'yükseldi' if mc > 0 else 'geriledi'} ({pct(mc)})")
    if mc is not None and pc is not None and abs(mc) >= 1 and abs(pc) >= 1 and (mc > 0) != (pc > 0):
        s.append('fit kare fiyatı ise ters yönde hareket etti (' + pct(pc) + '); bu genellikle son dönemde satılan konutların büyüklük veya tip karışımının değiştiğini gösterir')
    elif pc is not None and abs(pc) >= 1:
        s.append(f"fit kare fiyatı da {'yükseldi' if pc > 0 else 'geriledi'} ({pct(pc)})")
    if s:
        notes.append('; '.join(s) + '.')
    if rf.get('dom') and rf.get('dom_ly'):
        a_, b_ = rf['dom'], rf['dom_ly']
        if abs(a_ - b_) <= 5:
            notes.append(f"Medyan satış süresi {a_} gün ile geçen yılki seviyesine yakın.")
        else:
            notes.append(f"Medyan satış süresi bir yılda {b_} günden {a_} güne {'indi; satışlar daha hızlı kapanıyor' if a_ < b_ else 'çıktı; satışlar daha uzun sürüyor'}.")
    if rf.get('stl'):
        gap = 100 - rf['stl']
        if gap >= 4:
            notes.append(f"Satışlar ortalamada ilan fiyatının %{tl(gap, 1)} altında kapanıyor; pazarlık payı belirgin.")
        elif gap >= 1.5:
            notes.append(f"Satışlar ortalamada ilan fiyatının %{tl(gap, 1)} altında kapanıyor.")
        else:
            notes.append('Satışlar ilan fiyatına çok yakın kapanıyor.')
    elif rf.get('under_list') is not None:
        notes.append(f"Satışlar ortalamada ilan fiyatının %{tl(rf['under_list'], 1)} altında kapanıyor.")
    if rf.get('sold') is not None and rf['sold'] < 15:
        notes.append('Satış sayısı az olduğu için yüzde değişimler tek tek satışlardan güçlü biçimde etkilenir; bu rakamları kesin bir eğilim olarak değil, gösterge olarak okuyun.')
    return {'median': med, 'median_approx': bool(rf.get('median_approx')), 'median_chg': (f"yıllık {pct(rf['median_chg'])}" if rf.get('median_chg') is not None else ''),
            'ppsf': rf.get('ppsf'), 'src_short': 'Redfin', 'rows': rows, 'src': src, 'notes': notes}


def rent_block(d, z, zslug):
    name = d['name']
    if not z or z.get('n', 0) < 5 or not z.get('avg'):
        n = z.get('n', 0) if z else 0
        txt = f"Zillow’da yalnızca {n} aktif kiralık ilan var; ortalama kira anlamlı değil." if z else 'Zillow bu yerleşim için kira verisi yayımlamıyor.'
        rows = [['Kira verisi', txt]]
        src = (f'<a href="https://www.zillow.com/rental-manager/market-trends/{zslug}/" target="_blank" rel="noopener">Zillow Rental Market Trends, {label_zillow(zslug, name)}</a>, {ZILLOW_UPDATED}.') if z else 'Kira verisi yayımlanmıyor.'
        return {'avg': None, 'chg': '', 'src_short': 'Zillow', 'rows': rows, 'src': src, 'notes': ['Kiralık stok çok küçük olduğu için kira, mülkün kendisine göre belirlenir; yakın yerleşimlerdeki benzer ilanlar daha iyi bir referanstır.']}
    def v(k):
        return money(z[k]) if z.get(k) else '<small>yeterli ilan yok</small>'
    rows = [['Stüdyo', v('S')], ['1 yatak odalı', v('b1')], ['2 yatak odalı', v('b2')], ['3 yatak odalı', v('b3')], ['4+ yatak odalı', v('b4')], ['Tüm konutlar (ortalama)', money(z['avg'])]]
    yoy = z.get('yoy')
    chg = 'yıllık değişim yok' if yoy == 0 else (f"yıllık {'+' if yoy > 0 else '−'}{money(abs(yoy))}" if yoy is not None else '')
    src = f'<a href="https://www.zillow.com/rental-manager/market-trends/{zslug}/" target="_blank" rel="noopener">Zillow Rental Market Trends, {label_zillow(zslug, name)}</a>, {ZILLOW_UPDATED} ({tl(z["n"])} aktif kiralık ilan).'
    notes = []
    if zslug.isdigit():
        notes.append(f"Zillow bu bölge için ayrı veri yayımlamadığından {zslug} posta kodunun ortalamaları kullanıldı; posta kodu {name} dışında komşu alanları da kapsayabilir.")
    if z['n'] < 30:
        notes.append(f"Kiralık ilan sayısı az ({z['n']} ilan); ortalamalar tek tek ilanlardan çok etkilenebilir.")
    if z.get('b4') and z['b4'] > 2.5 * z['avg']:
        notes.append('4+ yatak odalı ortalaması, az sayıdaki büyük ve lüks ev ilanından etkileniyor.')
    return {'avg': z['avg'], 'chg': chg, 'src_short': 'Zillow', 'rows': rows, 'src': src, 'notes': notes}


def tax_text(d, lo, hi):
    name = d['name']
    if hi:
        rate = f"{tl(lo, 4)}–{tl(hi, 4)} mill"
        per100 = f"${tl(lo / 10, 2)}–{tl(hi / 10, 2)}"
        ex = f"${tl(lo * 1000)}–{tl(hi * 1000)}"
        note = TAX_RANGE_NOTE.get(d['id'], TAX_RANGE_GENERIC)
    else:
        rate = f"{tl(lo, 4)} mill"
        per100 = f"${tl(lo / 10, 2)}"
        ex = f"${tl(lo * 1000)}"
        note = ''
    t = (f"{name} için 2025 toplam vergi oranı {rate}; yani her $100 vergi değeri için yıllık yaklaşık {per100}. "
         f"Örnek: vergi değeri $1.000.000 olan bir mülk için yıllık yaklaşık {ex}. " + (note + ' ' if note else '') +
         "Çöp, sokak aydınlatması gibi ek kalemler (non-ad valorem) bu tutara dahil değildir. Satın alma sonrası vergi değeri piyasa değerine yakın yeniden belirlenir; "
         "birincil konut (homestead) indirimi ve artış sınırı yalnızca sahibinin oturduğu evlerde uygulanır.")
    return t


def gen(d):
    a = A[d['id']]
    rf = R.get(a['redfin']) if a.get('redfin') else None
    zs = a.get('zillow')
    z = Z.get(zs) if zs else None
    lo, hi, tsrc = T[d['id']]
    name = d['name']

    d['sales'] = sales_block(d, rf)
    d['rent'] = rent_block(d, z, zs)
    d['tax'] = {'mills': lo, 'src_short': TAX_SHORT[tsrc]}
    if hi:
        d['tax']['mills_hi'] = hi
    d['costs'][0] = ['Emlak vergisi', tax_text(d, lo, hi)]
    fix_transport(d)
    market_pc(d, rf, lo)

    s = d['sales']
    first = d.get('lead') or re.split(r'(?<=[.!?])\s+', d['short'].strip())[0]
    d['lead'] = first
    if s.get('median'):
        mt = ('yaklaşık ' if s.get('median_approx') else '') + money_short(s['median'])
        d['short'] = f"{first} Ekim 2026 itibarıyla son 3 ayın medyan satış fiyatı {mt} (Redfin)."
    else:
        d['short'] = f"{first} Satışlar çok seyrek olduğu için güncel medyan fiyat yayımlanmıyor."
    r = d['rent']
    parts = []
    if s.get('median'):
        parts.append(f"medyan satış fiyatı {('yaklaşık ' if s.get('median_approx') else '')}{money_short(s['median'])}")
    if r.get('avg'):
        parts.append(f"ortalama kira {money(r['avg'])}")
    d['meta'] = f"{name} mahalle raporu, Ekim 2026: " + (', '.join(parts) + ', ' if parts else '') + 'emlak vergisi, sel bölgesi, ulaşım ve yeni projeler. Kaynaklı ve tarihli veriler.'

    # SSS: fiyat, kira, vergi soruları her seferinde rakamlardan üretilir
    keep = [qa for qa in d['faq'] if not re.search(r'fiyat|kira|vergi', qa[0], re.I) or re.search(r'kısa süreli|airbnb', qa[0], re.I)]
    faq = []
    if s.get('median'):
        rows = dict(s['rows'])
        per = rf.get('period') if rf else None
        when = f"{MONTH_TR[per.split()[0]]} {per.split()[1]} itibarıyla son 3 ayda" if per else 'son 3 ayda'
        a1 = f"Redfin verisine göre {when} medyan satış fiyatı {('yaklaşık ' if s.get('median_approx') else '')}{money(s['median'])}"
        if s.get('median_chg'):
            a1 += f" ({s['median_chg']})"
        if s.get('ppsf'):
            a1 += f", fit kare fiyatı {('yaklaşık ' if (rf or {}).get('ppsf_approx') else '')}{money(s['ppsf'])}"
        a1 += '.'
    else:
        a1 = 'Satışlar çok seyrek olduğu için Redfin güncel bir medyan fiyat yayımlamıyor; fiyatlar mülke göre belirlenir ve son benzer satışlarla değerlendirilir.'
    faq.append([f"{name} bölgesinde ev fiyatları ne kadar?", a1])
    if r.get('avg'):
        z_ = z
        bits = []
        if z_.get('b1'):
            bits.append(f"1 yatak odalı {money(z_['b1'])}")
        if z_.get('b2'):
            bits.append(f"2 yatak odalı {money(z_['b2'])}")
        a2 = f"Zillow'a göre (26 Ekim 2026) {'bu posta kodunda ' if zs.isdigit() else ''}ortalama kira aylık {money(r['avg'])}" + (f"; {', '.join(bits)} civarında." if bits else '.')
    else:
        a2 = ('Zillow bu yerleşim için kira verisi yayımlamıyor; kira mülke göre belirlenir.' if not z else 'Kiralık ilan sayısı çok az olduğu için güvenilir bir ortalama yok; kira mülke göre belirlenir.')
    faq.append([f"{name} bölgesinde kiralar ne kadar?", a2])
    if hi:
        a3 = f"2025 için toplam oran konuma göre {tl(lo, 4)}–{tl(hi, 4)} mill; yani yıllık vergi, vergi değerinin yaklaşık %{tl(lo / 10, 2)}–{tl(hi / 10, 2)} kadarı. Bu bilgi genel niteliktedir, vergi tavsiyesi değildir."
    else:
        a3 = f"2025 için toplam oran {tl(lo, 4)} mill; yani yıllık vergi, vergi değerinin yaklaşık %{tl(lo / 10, 2)} kadarı. Bu bilgi genel niteliktedir, vergi tavsiyesi değildir."
    faq.append([f"{name} bölgesinde emlak vergisi ne kadar?", a3])
    d['faq'] = faq + keep

    # Kaynaklar: Redfin/Zillow/vergi satırları yeniden yazılır, diğerleri korunur
    other = [x for x in d['sources'] if not re.search(r'redfin\.com|zillow\.com|rentcafe|millage|bcpa\.net|pbcpao|miamidadepa', x[1])]
    src = []
    if rf:
        src.append([f"Redfin: {label_redfin(rf['slug'])} Housing Market (Ekim 2026 erişimi)", rf['url']])
    if z or zs:
        src.append([f"Zillow: {label_zillow(zs, name)} Rental Market Trends (26 Ekim 2026)", f"https://www.zillow.com/rental-manager/market-trends/{zs}/"])
    src += [list(x) for x in TAX_SRC[tsrc]]
    d['sources'] = src + other
    return d


def main(ids=None):
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'reports', '*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if ids and d['id'] not in ids:
            continue
        gen(d)
        json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        out.append(d['id'])
    print('refreshed', len(out))


if __name__ == '__main__':
    main(sys.argv[1:] or None)
