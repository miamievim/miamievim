# -*- coding: utf-8 -*-
"""Haftalık rehber sayfalarını üretir (şablon: rehberler/index.html, düzen: neden-miami).

Her rehber GUIDES listesinde tanımlıdır; rakamlar kaynak ve tarihleriyle birlikte burada tutulur.
Mahalle karşılaştırması rakamlarını tools/reports/*.json dosyalarından (mahalle raporlarının
kaynaklı verisi) okur; raporlar güncellendiğinde bu betik yeniden çalıştırılmalıdır.
Kullanım: python3 tools/build_guides.py
"""
import html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
BASE = 'https://miamievim.com'
NOTE = 'Bu sayfa genel bilgilendirme amaçlıdır; vergi, hukuk, sigorta veya yatırım tavsiyesi değildir. Kendi durumunuz için bir vergi danışmanı, avukat veya sigorta acentesine başvurun.'


def link(u, t):
    return f'<a href="{u}" target="_blank" rel="noopener">{E(t)}</a>'


# ---------------------------------------------------------------- Rehber 1: mahalle karşılaştırması
def money(v):
    if v >= 1_000_000:
        s = f'{v / 1e6:.2f}'.rstrip('0').rstrip('.').replace('.', ',')
        return f'${s} milyon'
    return f'${round(v / 1000)} bin'


def rent(v):
    return '$' + f'{v:,.0f}'.replace(',', '.')


def mills(t):
    m = f'{t["mills"]:.4f}'.replace('.', ',')
    if t.get('mills_hi'):
        m += '–' + f'{t["mills_hi"]:.4f}'.replace('.', ',')
    return m


MONTHS = 'Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık'


def src_date(s):
    m = re.search(r'(\d{1,2} )?(' + MONTHS + r') 20\d\d', re.sub('<[^>]+>', '', s))
    return m.group(0) if m else ''


def hood_rows():
    hoods = json.load(open(os.path.join(ROOT, 'tools', 'hoods.json'), encoding='utf-8'))[:22]
    rows = {}
    for h in hoods:
        d = json.load(open(os.path.join(ROOT, 'tools', 'reports', h['id'] + '.json'), encoding='utf-8'))
        rows[h['id']] = dict(id=h['id'], name=h['name'], county=h['county'], d=d)
    return rows


GROUPS = [
    ('Yürünebilir kent merkezleri',
     ['brickell', 'edgewater', 'wynwood', 'south-beach', 'little-havana'],
     'Yürüyüş mesafesinde iş, restoran ve toplu taşıma olan bölgeler. Brickell, Downtown ve South Beach\'te konut stoku ağırlıkla kondominyum dairedir; bu yüzden aidat, binanın denetim ve yedek akçe durumu ve kısa dönem kiralama kuralları fiyat kadar belirleyicidir.'),
    ('Okyanus kıyısında kule yaşamı',
     ['sunny-isles', 'bal-harbour', 'north-beach', 'aventura', 'hallandale'],
     'Okyanus veya Intracoastal manzaralı, tam hizmetli binaların yoğun olduğu kıyı şeridi. Kıyıda sel bölgesi adrese göre değişir; sel sigortası, binanın ortak poliçesi ve bina yaşı satın alma kararının merkezindedir.'),
    ('Ağaçlı sokaklar ve müstakil evler',
     ['coral-gables', 'coconut-grove', 'pinecrest', 'key-biscayne'],
     'Bahçeli müstakil evler, yoğun bitki örtüsü ve sıkı imar kurallarıyla öne çıkan bölgeler; Key Biscayne\'de müstakil evler ile okyanus kıyısı kondominyumlar bir arada. Medyan fiyatlar bu listedeki en yüksekler arasındadır; satılan konutların büyük kısmı müstakil ev olduğunda medyan yükselir. Konut bölgelerinde günlük hayat çoğunlukla araçla geçer.'),
    ('Planlı şehirler ve site yaşamı',
     ['doral', 'weston'],
     'Göller, parklar, golf sahaları ve yönetimli sitelerle planlanmış şehirler. Site aidatı (HOA) ve site kuralları (kiralama, tadilat, araç park) teklif öncesinde incelenmelidir.'),
    ('Broward ve Palm Beach: kanallar, iskeleler ve sahil kasabaları',
     ['fort-lauderdale', 'wilton-manors', 'pompano', 'deerfield', 'hollywood', 'boca-raton'],
     'Miami\'nin kuzeyinde, derin su kanalları, tekne yaşamı ve yürünebilir sahil merkezleri olan şehirler. Emlak vergisi oranları şehirden şehre belirgin biçimde değişir; aşağıdaki tabloda karşılaştırabilirsiniz.'),
]


def build_compare():
    R = hood_rows()
    url = BASE + '/rehberler/miami-mahalle-karsilastirmasi/'
    # karşılaştırma tablosu
    order = [i for _, ids, _ in GROUPS for i in ids]
    assert sorted(order) == sorted(R), 'Gruplar 22 mahallenin tamamını kapsamalı'
    trs = ''
    for i in order:
        r = R[i]; d = r['d']
        s, rt = d['sales'], d['rent']
        trs += (f'<tr><td><a href="/mahalle-raporlari/{i}/">{E(r["name"])}</a><br><small>{E(r["county"])}</small></td>'
                f'<td>{money(s["median"])}<br><small>{E(s["src_short"])}</small></td>'
                f'<td>{rent(rt["avg"])}<br><small>{E(rt["src_short"])}, {E(src_date(rt["src"]))}</small></td>'
                f'<td>{mills(d["tax"])}<br><small>{E(d["tax"]["src_short"])}</small></td></tr>')
    table = f'''<div class="tbl"><table>
<thead><tr><th>Bölge</th><th>Medyan satış fiyatı</th><th>Ortalama kira (aylık)</th><th>Emlak vergisi (mill)</th></tr></thead>
<tbody>{trs}</tbody></table></div>'''

    def chips(ids):
        out = []
        for i in ids:
            d = R[i]['d']
            out.append(f'<a href="/mahalle-raporlari/{i}/">{E(R[i]["name"])}</a>: {E(d["short"])}')
        return out

    lo = min(R.values(), key=lambda r: r['d']['tax']['mills'])
    hi = max(R.values(), key=lambda r: r['d']['tax'].get('mills_hi') or r['d']['tax']['mills'])
    hi_m = hi['d']['tax'].get('mills_hi') or hi['d']['tax']['mills']
    tax_ex_lo = round(lo['d']['tax']['mills'] * 500)  # $500.000 vergi değeri için
    tax_ex_hi = round(hi_m * 500)
    fmt = lambda v: '$' + f'{v:,.0f}'.replace(',', '.')

    sections = []
    for n, (h, ids, intro) in enumerate(GROUPS, 1):
        ps = [intro] + chips(ids)
        sections.append((f'{n:02d}', h, ps, []))
    sections.append(('06', 'Aynı bütçe, farklı yıllık maliyet', [
        f'Emlak vergisi oranı (mill) bölgeden bölgeye değişir: 1 mill, vergi değerinin binde biridir. Bu 22 bölgede 2025 oranları {E(lo["name"])}\'te {mills(lo["d"]["tax"])} mill ile {E(hi["name"])}\'da {f"{hi_m:.4f}".replace(".", ",")} mill arasında. Vergi değeri $500.000 olan bir mülkte bu fark, yıllık yaklaşık {fmt(tax_ex_lo)} ile {fmt(tax_ex_hi)} arası bir vergi demektir (çöp, sokak aydınlatması gibi ek kalemler hariç).',
        'Medyan satış fiyatı, o dönemde satılan konutların karışımını yansıtır: küçük dairelerin çok satıldığı bir dönemde medyan düşer, büyük müstakil evlerin satıldığı bir dönemde yükselir. Bölgeleri karşılaştırırken fit kare fiyatına, satış süresine ve konut tipine de bakmak gerekir; bunlar her mahalle raporunda ayrıca verilir.',
        'Aidat, sigorta ve sel bölgesi ise binaya ve adrese göre değişir; tek bir mahalle ortalaması yanıltıcı olur. Bu kalemler için <a href="/rehberler/miami-ev-alma-maliyetleri/">ev alırken gizli maliyetler rehberine</a> bakabilirsiniz.',
    ], []))
    sections.append(('07', 'Okul ve suç verisi nereden kontrol edilir?', [
        'Okul atamaları adrese göre belirlenir ve değişebilir; okul bilgileri için ilçe okul idarelerinin resmi sayfalarına bakın: ' + link('https://www.dadeschools.net/', 'Miami-Dade County Public Schools') + ', ' + link('https://www.browardschools.com/', 'Broward County Public Schools') + ', ' + link('https://www.palmbeachschools.org/', 'School District of Palm Beach County') + '.',
        'Suç istatistikleri için resmi kaynak ' + link('https://www.fdle.state.fl.us/FSAC/Data-Statistics/UCR-Offense-Data', 'Florida Department of Law Enforcement (FDLE)') + ' verileridir. Sel bölgesini ' + link('https://msc.fema.gov/portal/search', 'FEMA haritasından') + ' adresle kontrol edebilirsiniz.',
    ], []))
    sections.append(('08', 'Bir sonraki adım', [
        'Size uyan bölgeleri daraltmak için <a href="/mahalle-testi/">9 soruluk mahalle testini</a> çözebilir, 22 mahallenin tüm başlıklarını (karakter, mekânlar, kiralar, aidat, sigorta, ulaşım, yeni projeler) tek dosyada görmek için <a href="/mahalle-rehberi/">ücretsiz Mahalle Rehberi\'ni</a> isteyebilirsiniz. Miami-Dade, Broward ve Palm Beach\'teki 108 bölgenin tamamı <a href="/mahalle-raporlari/">mahalle raporlarında</a>.',
    ], []))

    stats = [
        ('22', 'Bölge', 'Miami-Dade, Broward ve Palm Beach\'ten; mahalle raporlarının Ekim 2026 sürümü.'),
        ('5', 'Yaşam biçimi', 'Kent merkezi, okyanus kıyısı, bahçeli evler, planlı şehirler ve kuzey sahilleri.'),
        (f'{mills(lo["d"]["tax"])}–{f"{hi_m:.4f}".replace(".", ",")}', 'Emlak vergisi (mill)', 'Bu 22 bölgedeki 2025 toplam vergi oranı aralığı. Kaynak: ilçe emlak değerleme ofisleri (2025).'),
    ]
    faq = [
        ('Miami\'de hangi mahalle size uygun?', 'Önce yaşam biçiminizi belirleyin: araçsız bir kent merkezi mi, okyanus kıyısında tam hizmetli bir bina mı, bahçeli bir müstakil ev mi, planlı bir site mi? Ardından bütçenizi yalnızca fiyatla değil; aidat, emlak vergisi, sigorta ve sel bölgesiyle birlikte karşılaştırın. 9 soruluk mahalle testi ilk üç seçeneği daraltmaya yardımcı olur.'),
        ('Miami\'de emlak vergisi en düşük hangi bölgede?', f'Bu rehberdeki 22 bölge içinde 2025 toplam vergi oranı en düşük olan {lo["name"]} ({mills(lo["d"]["tax"])} mill; kaynak: {lo["d"]["tax"]["src_short"]}). Vergi tutarı oran kadar mülkün vergi değerine ve birincil konut (homestead) indirimine de bağlıdır. Bu bilgi genel niteliktedir, vergi tavsiyesi değildir.'),
        ('Araç olmadan yaşanabilecek Miami mahalleleri hangileri?', 'Mahalle raporlarına göre Brickell ve Downtown araçsız yaşamaya en uygun bölgeler arasındadır: ücretsiz Metromover, Metrorail ve Brightline istasyonları yakındır. South Beach de en yürünebilir bölgelerden biridir; Wynwood ve Design District kendi içinde yürünebilirdir.'),
        ('Okul ve suç bilgisini nereden kontrol edebilirim?', 'Okul atamaları adrese göre belirlenir; Miami-Dade, Broward ve Palm Beach ilçe okul idarelerinin resmi sitelerine bakın. Suç istatistikleri için resmi kaynak Florida Department of Law Enforcement (FDLE) verileridir.'),
    ]
    sources = [
        ('Mahalle raporları (Ekim 2026): her bölgenin satış, kira ve vergi verisi ile ayrıntılı kaynakları', BASE + '/mahalle-raporlari/'),
        ('Redfin Housing Market sayfaları (Ekim 2026 erişimi, son 3 ay verisi)', 'https://www.redfin.com/city/11458/FL/Miami/housing-market'),
        ('Zillow Rental Market Trends (Ekim 2026)', 'https://www.zillow.com/rental-manager/market-trends/miami-fl/'),
        ('RentCafe: Sunny Isles Beach ortalama kira', 'https://www.rentcafe.com/average-rent-market-trends/us/fl/sunny-isles-beach/'),
        ('Miami-Dade County Property Appraiser: 2025 vergi oranları', 'https://www.miamidadepa.gov/pa/'),
        ('Broward County Property Appraiser: 2025 vergi oranları', 'https://web.bcpa.net/'),
        ('Miami-Dade County Public Schools', 'https://www.dadeschools.net/'),
        ('Florida Department of Law Enforcement: UCR suç verisi', 'https://www.fdle.state.fl.us/FSAC/Data-Statistics/UCR-Offense-Data'),
        ('FEMA Flood Map Service Center', 'https://msc.fema.gov/portal/search'),
    ]
    return dict(
        slug='miami-mahalle-karsilastirmasi', url=url,
        title='Miami Mahalle Karşılaştırması 2026: Fiyat, Kira, Vergi | Aleyna Bozoklar',
        desc='Brickell\'den Boca Raton\'a 22 Miami mahallesi: medyan satış fiyatı, ortalama kira ve emlak vergisi oranı yan yana. Ekim 2026 verisi, kaynaklı Türkçe rehber.',
        og='Miami\'de hangi mahalle size uygun?', headline='Miami\'de hangi mahalle size uygun? 22 mahalle karşılaştırması',
        crumb='22 mahalle karşılaştırması', tab='22 mahalle',
        h1='Miami\'de hangi mahalle <em>size uygun?</em>',
        lead='Brickell\'den Boca Raton\'a 22 bölge, yaşam biçimine göre beş grupta: her bölgenin medyan satış fiyatı, ortalama kirası ve emlak vergisi oranı yan yana. Rakamlar mahalle raporlarının Ekim 2026 sürümünden, kaynaklarıyla.',
        date_iso='2026-10-26', date='26 Ekim 2026', stats=stats, sections=sections, faq=faq, sources=sources,
        extra=f'''
  <section class="section white">
    <div class="wrap">
      <div class="section-head"><div class="stack"><p class="eyebrow">Ekim 2026</p><h2>22 bölge <em>yan yana</em></h2></div></div>
      {table}
      <p class="wm-note">Medyan satış fiyatı: Redfin, Ekim 2026 erişimi (son 3 ay verisi); bazı satırlarda bölgenin çekirdek mahallesi veya şehri esas alınmıştır (alt satırda belirtilir). Ortalama kira: Zillow Rental Market Trends, Sunny Isles Beach için RentCafe (tarih alt satırda). Emlak vergisi: ilçe emlak değerleme ofislerinin 2025 toplam oranları; aralık verilen bölgelerde oran alt bölgeye göre değişir. Her rakamın ayrıntılı kaynağı ilgili mahalle raporundadır.</p>
    </div>
  </section>''',
        cta=('/mahalle-testi/', 'Mahalle testini çözün'), css=['report'])


# ---------------------------------------------------------------- Rehber 2: ev alırken gizli maliyetler
CS = {
    'dor': ('Florida Department of Revenue: Documentary Stamp Tax (GT-800014)', 'https://floridarevenue.com/forms_library/current/gt800014.pdf'),
    'int': ('Starfield & Smith: Florida doc stamp ve intangible tax özeti (4 Şubat 2026)', 'https://starfieldsmith.com/2026/02/best-practices-a-refresher-on-florida-documentary-stamp-and-nonrecurring-intangible-tax/'),
    'title': ('Florida Administrative Code 69O-186.003: Tapu sigortası tarifeleri', 'https://www.law.cornell.edu/regulations/florida/Fla-Admin-Code-Ann-R-69O-186-003'),
    'dr501': ('Florida DR-501: Homestead başvuru formu (Miami-Dade Property Appraiser)', 'https://www.miamidadepa.gov/pa/library/form/dr501.pdf'),
    'soh': ('Martin County Property Appraiser: Save Our Homes 2026 (%2,7)', 'https://www.pamartinfl.gov/images/stories/files/SOH-2026.pdf'),
    'mdpa': ('Miami-Dade Property Appraiser: Save Our Homes', 'https://www.miamidadepa.gov/pa/amendment_10.asp'),
    'tc': ('Miami-Dade Tax Collector: Erken ödeme indirimleri', 'https://mdctaxcollector.gov/discounts-for-early-payment'),
    'am3': ('Pinellas County Property Appraiser: 2026 Amendment 3 (CS/HJR 1F) SSS', 'https://www.pcpao.gov/amendment3'),
    'far': ('Florida Realtors: Oy pusulası metni yeniden yazıldı (14 Ağustos 2026)', 'https://www.floridarealtors.org/news-media/news-articles/2026/08/floridas-attorney-general-rewrites-property-tax-amendment-november'),
    'hb913': ('Florida Realtors: HB 913 kondominyum yasası (23 Haziran 2025)', 'https://floridarealtors.org/news-media/news-articles/2025/06/realtor-supported-condo-bill-becomes-law'),
    'withum': ('Withum: HB 913 ile değişenler (milestone, SIRS, yedek akçe)', 'https://www.withum.com/resources/key-changes-from-florida-house-bill-913-explained-inspections-reserves-and-more/'),
    'rider': ('Barnes Walker: FAR/BAR kondominyum eki (2025)', 'https://barneswalker.com/the-new-florida-condominium-rider-in-the-far-bar-contract/'),
    'gov': ('Florida Valilik Ofisi: Sigorta tarife indirimleri (12 Ocak 2026)', 'https://www.flgov.com/eog/news/press/2026/governor-ron-desantis-announces-major-insurance-rate-relief-floridas-reforms'),
    'flood': ('Lee County: Zorunlu sel sigortası (FEMA SFHA) bilgi notu', 'https://www.leefl.gov/dcd/Documents/FloodMapping/FEMAFloodZones/MandatoryPurchaseHandout.pdf'),
    'fema': ('FEMA Flood Map Service Center', 'https://msc.fema.gov/portal/search'),
}


def ca(k, text=None):
    t, u = CS[k]
    return link(u, text or t)


def build_costs():
    url = BASE + '/rehberler/miami-ev-alma-maliyetleri/'
    # Örnek: Miami-Dade'de $800.000'lık kondominyum (Brickell, Miami şehri 2025 oranı)
    P = 800_000
    deed = P * 1.05 / 100
    title = 100_000 * 5.75 / 1000 + (P - 100_000) * 5.00 / 1000
    loan = 480_000
    mtg_stamp = loan * 0.35 / 100
    intang = loan * 0.002
    tax = P * 19.9878 / 1000
    f = lambda v: '$' + f'{v:,.0f}'.replace(',', '.')
    ex = f'''<div class="tbl"><table>
<thead><tr><th>Kalem</th><th>Örnek tutar</th><th>Dayanak</th></tr></thead>
<tbody>
<tr><td>Tapu devri damga vergisi (doc stamps), Miami-Dade, kondominyum</td><td>{f(deed)}</td><td>$100 başına $0,60 + $0,45 ek vergi = %1,05. Kimin ödeyeceği sözleşmede belirlenir.</td></tr>
<tr><td>Tapu sigortası (sahip poliçesi)</td><td>{f(title)}</td><td>Devlet tarifesi: ilk $100.000 için binde 5,75, sonrası $1 milyona kadar binde 5. Ek teminatlar hariç.</td></tr>
<tr><td>Kredi kullanılırsa: ipotek damga vergisi ($480.000 kredi)</td><td>{f(mtg_stamp)}</td><td>$100 başına $0,35.</td></tr>
<tr><td>Kredi kullanılırsa: intangible tax ($480.000 kredi)</td><td>{f(intang)}</td><td>Kredi tutarının binde 2'si.</td></tr>
<tr><td>Yıllık emlak vergisi (homestead yok, vergi değeri = $800.000 varsayımıyla)</td><td>{f(tax)} / yıl</td><td>Miami şehri 2025 toplam oranı 19,9878 mill (Miami-Dade PA). Ek kalemler (non-ad valorem) hariç.</td></tr>
<tr><td>Aidat, konut ve sel sigortası</td><td>Binaya ve adrese göre</td><td>Bina bütçesi, SIRS ve sigorta teklifleriyle belirlenir; tahmini rakam kullanılmamalıdır.</td></tr>
</tbody></table></div>
<p class="wm-note">Örnek; Miami şehir sınırları içinde (ör. Brickell) $800.000'lık bir kondominyum ve $480.000 kredi varsayımıyla hesaplanmıştır. Avukat, kredi, ekspertiz, denetim ve kayıt ücretleri dahil değildir. Gerçek tutarlar sözleşmeye, kredi kuruluşuna ve mülke göre değişir.</p>'''

    stats = [
        ('%1,05', 'Miami-Dade doc stamps', f'Kondominyum ve müstakil ev dışı mülklerin tapu devrinde; müstakil evde %0,60, Florida\'nın geri kalanında %0,70. Kaynak: {ca("dor", "Florida Department of Revenue")}.'),
        ('$51.411', 'Homestead indirimi (2026)', f'Okul vergisi dışında; okul vergilerinde $25.000. Yalnızca 1 Ocak itibarıyla sürekli ikametgâh olan evde. Kaynak: {ca("am3", "Pinellas County PA")}.'),
        ('%2,7', 'Save Our Homes sınırı (2026)', f'Homestead evlerde yıllık vergi değeri artışı en fazla %3 veya enflasyon; 2026\'da %2,7. Kaynak: {ca("soh", "Martin County PA")}.'),
        ('3 Kasım', 'Amendment 3 oylaması', f'Homestead indirimini artıran ve yatırım mülklerinde artış sınırını %10\'dan %5\'e indiren değişiklik; %60 onay gerekir. Kaynak: {ca("am3", "Pinellas County PA")}.'),
    ]
    sections = [
        ('01', 'Kısa cevap', [
            'Miami\'de bir mülkün gerçek maliyeti ilan fiyatından ibaret değildir. Satın alırken tapu devri damga vergisi, tapu sigortası ve kredi kullanılıyorsa kredi vergileri ödenir; sonrasında her yıl emlak vergisi, aidat (HOA) ve sigorta gelir. Bu kalemler bölgeye, binaya ve mülkün birincil konut (homestead) olup olmamasına göre büyük ölçüde değişir.',
            'Aşağıda her kalemin nasıl hesaplandığı, resmi oranları ve 3 Kasım 2026\'da oylanacak emlak vergisi değişikliğinin (Amendment 3) ne anlama geldiği kaynaklarıyla anlatılıyor.',
        ], []),
        ('02', 'Kapanışta ödenenler', [
            'Tapu devri damga vergisi (documentary stamp tax): Florida genelinde satış bedelinin her $100\'ü için $0,70 (%0,70). Miami-Dade\'de oran farklıdır: tek ailelik müstakil evde $0,60, kondominyum dahil diğer mülklerde $0,60 + $0,45 ek vergi, toplam $1,05 (%1,05). Bu verginin alıcı mı satıcı mı tarafından ödeneceği satış sözleşmesinde belirlenir.',
            'Tapu sigortası (title insurance): Florida\'da tapu sigortası primleri devlet tarifesiyle belirlenir. Sahip poliçesinde ilk $100.000 için her $1.000\'e $5,75, $100.000–$1 milyon arası için $5,00, $1–5 milyon arası için $2,50 uygulanır. Ek teminatlar (endorsement) ayrıca ücretlendirilir.',
            'Kredi kullanılıyorsa: ipotek senedine $100 başına $0,35 damga vergisi ve kredi tutarının binde 2\'si oranında intangible tax eklenir. Örneğin $500.000\'lık bir kredide damga vergisi $1.750, intangible tax $1.000 olur.',
        ], ['dor', 'title', 'int']),
        ('03', 'Emlak vergisi: satın aldıktan sonra değişir', [
            'Florida\'da emlak vergisi, mülkün vergi değeri ile bölgenin toplam vergi oranının (mill) çarpımıdır; 1 mill, vergi değerinin binde biridir. Örneğin Miami şehri için 2025 toplam oranı 19,9878 mill; yani her $100 vergi değeri için yıllık yaklaşık $2. Her bölgenin oranı <a href="/mahalle-raporlari/">mahalle raporlarında</a> ve <a href="/rehberler/miami-mahalle-karsilastirmasi/">22 mahalle karşılaştırmasında</a>.',
            'Satış, vergi değerinin yeniden belirlenmesine yol açar: mülk el değiştirdiğinde önceki sahibin indirimleri ve artış sınırları sona erer, ertesi yıl vergi değeri piyasa değerine yakın yeniden belirlenir. Bu yüzden ilandaki "geçen yılın vergisi" alıcı için iyi bir rehber değildir.',
            'Birincil konut (homestead) indirimi: 1 Ocak itibarıyla mülkün sahibi olan ve orayı sürekli ikametgâhı yapan kişiler, 1 Mart\'a kadar başvurarak indirim alabilir. 2026\'da indirim okul vergileri için $25.000, diğer vergiler için toplam $51.411\'dir. Homestead evlerde yıllık vergi değeri artışı Save Our Homes kuralıyla %3 veya enflasyonla sınırlıdır; 2026\'da bu sınır %2,7. Kiraya verilen veya ikinci ev olarak kullanılan mülkler homestead alamaz; bunlarda okul dışı vergilerde yıllık %10 artış sınırı uygulanır.',
            'Ödeme: vergi faturaları kasımda gelir; kasımda ödenirse %4, aralıkta %3, ocakta %2, şubatta %1 indirim uygulanır. 1 Nisan\'dan sonra ödenmemiş vergi gecikmiş sayılır.',
        ], ['dr501', 'soh', 'mdpa', 'am3', 'tc']),
        ('04', '3 Kasım 2026: Amendment 3 ne getiriyor?', [
            'Florida seçmenleri 3 Kasım 2026 genel seçiminde emlak vergisiyle ilgili Amendment 3\'ü (CS/HJR 1F) oylayacak. Anayasa değişikliği olduğu için yürürlüğe girmesi için en az %60 onay gerekiyor. Kabul edilirse 1 Ocak 2027\'de yürürlüğe girer; etkisi ilk kez Ağustos 2027 TRIM bildirimlerinde ve Kasım 2027 vergi faturalarında görülür.',
            'Homestead evler için: okul vergilerindeki $25.000 indirim aynen kalır; okul dışı vergilerdeki indirim 2027\'de $150.000\'e, 2028\'de $250.000\'e kadar çıkar ve 2029\'dan itibaren enflasyona endekslenir. 31 Aralık 2026\'dan sonra Florida\'ya yerleşenler önce $50.000 okul dışı indirimle başlar; yüksek indirim dört yıl homestead sahipliğinden sonra uygulanır.',
            'Yatırım ve ikinci ev mülkleri (homestead olmayan) için: okul dışı vergilerde yıllık vergi değeri artış sınırı %10\'dan %5\'e iner. Okul vergileri sınırsız kalır ve bu değişiklik vergi oranlarını değil yalnızca vergi değerindeki artışı sınırlar; yani vergi tutarının mutlaka düşeceği anlamına gelmez.',
            'Oylama sonucu ve uygulama yasaları kesinleştiğinde bu bölüm güncellenecektir. Bu bilgi genel niteliktedir, vergi veya hukuk tavsiyesi değildir.',
        ], ['am3', 'far']),
        ('05', 'Aidat ve bina sağlığı: SIRS ve milestone', [
            'Florida\'da 2022\'den sonra yürürlüğe giren kondominyum yasalarıyla, üç veya daha fazla yaşanabilir katı olan binalarda iki rapor zorunlu hale geldi: bina 30 yaşına geldiğinde ve sonra her 10 yılda bir yapılan yapısal denetim (milestone inspection) ve her 10 yılda bir hazırlanan yapısal yedek akçe çalışması (SIRS). SIRS\'te belirlenen yedek akçe artık sınırlı istisnalar dışında üye oyuyla atlanamıyor; bu, bazı binalarda aidatları ve özel aidatları (special assessment) artırdı.',
            '2025\'te yürürlüğe giren HB 913 ile ilk SIRS için son tarih 31 Aralık 2025\'e uzatıldı; dernekler, onaylanmış yönetim kurulu tutanaklarının son 12 ayını web sitelerinde yayımlamak zorunda; alıcının sözleşmeden cayma süresi belgeleri teslim aldıktan sonraki 7 gün olarak düzenlendi.',
            'Teklif vermeden önce isteyin: son SIRS ve milestone raporları, yıllık bütçe ve mali tablolar, onaylanmış veya gündemdeki özel aidatlar, son 12 ayın yönetim kurulu tutanakları ve binanın sigorta poliçesi. Yatırım için alınıyorsa kiralama kuralları da bu listeye eklenmelidir; ayrıntılar <a href="/yatirim/">yatırım sayfasında</a>.',
        ], ['hb913', 'withum', 'rider']),
        ('06', 'Sigorta: konut, rüzgâr ve sel', [
            'Kondominyumda binanın dış yapısı genellikle derneğin ortak poliçesindedir; dairenin içi, eşyalar ve sorumluluk için ayrıca daire sahibi poliçesi (HO-6) alınır. Müstakil evde ise rüzgâr ve kasırga teminatı da dahil tüm yapı sahibin poliçesindedir; bina yaşı, çatı yaşı ve kasırgaya dayanıklılık önlemleri primi doğrudan etkiler.',
            'Fiyatlarda son durum: Florida Valilik Ofisi\'nin 12 Ocak 2026 açıklamasına göre devlet destekli sigorta şirketi Citizens\'ın poliçe sahipleri için eyalet geneli ortalama %8,7 tarife indirimi onaylandı. Ortalama indirim her poliçeye aynı şekilde yansımaz; teklif adres bazında alınmalıdır.',
            'Sel sigortası: FEMA\'nın yüksek riskli sel bölgelerinde (A ve V ile başlayan bölgeler) federal destekli bir konut kredisi kullanılıyorsa sel sigortası zorunludur. Kredi kullanılmasa da bu bölgelerde sel sigortası önemli bir maliyet kalemidir. Adresin sel bölgesini ' + ca('fema', 'FEMA haritasından') + ' kontrol edebilirsiniz.',
        ], ['gov', 'flood', 'fema']),
        ('07', 'Örnek hesap', ['Aşağıdaki tablo, yalnızca resmi oranı olan kalemler için bir örnek gösterir. Aidat ve sigorta binaya göre değiştiği için tahmini rakam yazılmamıştır.'], []),
    ]
    faq = [
        ('Miami\'de ev alırken kapanış masrafları ne kadar?', 'Kalemler sözleşmeye göre değişir. Resmi oranı olanlar: tapu devri damga vergisi Miami-Dade\'de müstakil evde %0,60, kondominyum dahil diğer mülklerde %1,05 (Florida geneli %0,70); tapu sigortası devlet tarifesiyle (ilk $100.000 için binde 5,75); kredi varsa ipotek damga vergisi %0,35 ve intangible tax binde 2. Bu bilgi genel niteliktedir, tavsiye değildir.'),
        ('Yabancı alıcı homestead indiriminden yararlanabilir mi?', 'Homestead indirimi, 1 Ocak itibarıyla Florida\'da sürekli ikametgâhı olan ve mülkte oturan sahiplere verilir; başvuru 1 Mart\'a kadar yapılır. Kiraya verilen veya ikinci ev olarak kullanılan mülkler bu indirimi alamaz. Kendi durumunuz için bir vergi danışmanına başvurun.'),
        ('Amendment 3 kabul edilirse yatırım mülkümün vergisi düşer mi?', 'Kendiliğinden düşmez. Değişiklik homestead olmayan mülklerde okul dışı vergilerde yıllık vergi değeri artış sınırını %10\'dan %5\'e indirir; vergi oranlarını ve okul vergilerini değiştirmez. Kabul için 3 Kasım 2026\'da en az %60 onay gerekir. Bu bilgi vergi tavsiyesi değildir.'),
        ('Kondominyum alırken hangi belgeleri istemeliyim?', 'Son SIRS ve milestone raporları, yıllık bütçe ve mali tablolar, onaylanmış veya gündemdeki özel aidatlar, son 12 ayın yönetim kurulu tutanakları ve binanın sigorta poliçesi. Florida\'da alıcının cayma süresi, belgeleri teslim aldıktan sonraki 7 gündür.'),
    ]
    return dict(
        slug='miami-ev-alma-maliyetleri', url=url,
        title='Miami\'de Ev Alırken Gizli Maliyetler (2026) | Aleyna Bozoklar',
        desc='Miami\'de ev alırken fiyata eklenenler: doc stamps, tapu sigortası, emlak vergisi ve homestead, 3 Kasım Amendment 3, SIRS, aidat ve sigorta. Resmi oranlarla.',
        og='Miami\'de ev alırken gizli maliyetler', headline='Miami\'de ev alırken gizli maliyetler: kapanış, emlak vergisi, aidat ve sigorta',
        crumb='Ev alırken gizli maliyetler', tab='Gizli maliyetler',
        h1='Ev alırken <em>gizli maliyetler</em>',
        lead='İlan fiyatının üstüne neler eklenir? Kapanış vergileri, tapu sigortası, emlak vergisi ve homestead, 3 Kasım\'daki Amendment 3 oylaması, aidat ve sigorta: her kalem resmi oranı ve kaynağıyla.',
        date_iso='2026-10-26', date='26 Ekim 2026', stats=stats, sections=sections, faq=faq,
        sources=list(CS.values()), after_sections=ex,
        cta=('/yatirim/', 'Net getiri hesaplayıcısı'), css=['report'])


# ---------------------------------------------------------------- ortak sayfa üretimi
TABS = [('/rehberler/', 'Tüm rehberler'), ('/rehberler/neden-miami/', 'Neden Miami?')]


def render(g, tpl, tabs):
    head_end = tpl.index('</head>')
    body_start = tpl[tpl.index('<body>'):tpl.index('<main id="main">')]
    footer = tpl[tpl.index('</main>') + len('</main>'):]
    head = tpl[:tpl.index('<title>')]
    links = re.findall(r'<link rel="(?:preconnect|stylesheet|icon|apple-touch-icon)"[^>]*>', tpl[:head_end])
    for c in g.get('css', []):
        links.append(f'<link rel="stylesheet" href="/assets/{c}.css">')
    srcs = g['sources']
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Article', 'headline': g['headline'], 'description': g['desc'], 'inLanguage': 'tr', 'url': g['url'],
         'mainEntityOfPage': g['url'], 'dateModified': g['date_iso'], 'datePublished': g['date_iso'],
         'image': BASE + '/assets/og-image.png',
         'author': {'@type': 'Person', '@id': BASE + '/#aleyna', 'name': 'Aleyna Bozoklar'},
         'publisher': {'@type': 'Person', '@id': BASE + '/#aleyna', 'name': 'Aleyna Bozoklar'},
         'citation': [u for _, u in srcs]},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ana sayfa', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Rehberler', 'item': BASE + '/rehberler/'},
            {'@type': 'ListItem', 'position': 3, 'name': g['crumb'], 'item': g['url']}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in g['faq']]},
    ]}
    meta = f'''<title>{E(g["title"])}</title>
<meta name="description" content="{E(g["desc"])}">
<link rel="canonical" href="{g["url"]}">
<meta property="og:type" content="article">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="{E(g["og"])}">
<meta property="og:description" content="{E(g["desc"])}">
<meta property="og:url" content="{g["url"]}">
<meta property="og:image" content="{BASE}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0F0F0F">
{chr(10).join(links)}
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
'''
    path = '/rehberler/' + g['slug'] + '/'
    cur = ' aria-current="page"'
    tabnav = ''.join(f'<a href="{u}"{cur if u == path else ""}>{E(t)}</a>' for u, t in tabs)
    stats = ''.join(f'<div class="ruled"><span class="big">{E(b)}</span><h3>{E(h)}</h3><p>{p}</p></div>' for b, h, p in g['stats'])
    keys = {u: t for t, u in srcs}
    secs = ''
    for n, h, ps, sk in g['sections']:
        src = ''
        if sk:
            src = '<p class="wm-src">Kaynak: ' + ' · '.join(ca(k) for k in sk) + '</p>'
        secs += f'''
      <div class="wm-row">
        <div class="wm-h"><span class="wm-n">{n}</span><h2>{E(h)}</h2></div>
        <div class="wm-b">{"".join(f"<p>{p}</p>" for p in ps)}{src}</div>
      </div>'''
    faq = ''.join(f'<details class="faq-item"><summary>{E(q)}</summary><div class="a"><p>{E(a)}</p></div></details>' for q, a in g['faq'])
    srclist = ''.join(f'<li>{link(u, t)}</li>' for t, u in srcs)
    after = ''
    if g.get('after_sections'):
        after = f'''
  <section class="section white">
    <div class="wrap">
      {g["after_sections"]}
    </div>
  </section>'''
    main = f'''<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow"><a href="/rehberler/" style="color:inherit">Rehberler</a> · {E(g["crumb"])}</p>
      <h1>{g["h1"]}</h1>
      <p class="lead">{E(g["lead"])} Yayın: {g["date"]}.</p>
      <nav class="subtabs" aria-label="Rehberler alt menüsü">{tabnav}</nav>
    </div>
  </section>

  <section class="section white">
    <div class="wrap">
      <div class="grid-3 wm-stats">{stats}</div>
    </div>
  </section>
{g.get("extra", "")}
  <section class="section">
    <div class="wrap wm">{secs}
    </div>
  </section>
{after}
  <section class="section bone">
    <div class="wrap">
      <div class="section-head"><div class="stack"><p class="eyebrow">Sık sorulan sorular</p><h2>Kısa <em>cevaplar</em></h2></div></div>
      <div class="faq">{faq}</div>
      <div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:48px">
        <a class="btn" href="{g["cta"][0]}">{E(g["cta"][1])}</a>
        <a class="btn btn-line" href="/#iletisim">Tanışma görüşmesi planlayın</a>
      </div>
      <h3 class="wm-srch">Kaynaklar</h3>
      <ol class="wm-srcs">{srclist}</ol>
      <p class="wm-note">{E(NOTE)}</p>
    </div>
  </section>
</main>'''
    out = head + meta + body_start + main + footer
    d = os.path.join(ROOT, 'rehberler', g['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)


def main():
    tpl = open(os.path.join(ROOT, 'rehberler', 'index.html'), encoding='utf-8').read()
    # en_caps işaretlerini şablondan temizle (yeniden uygulanacak)
    guides = [build_compare(), build_costs()]
    tabs = TABS + [('/rehberler/' + g['slug'] + '/', g['tab']) for g in guides]
    for g in guides:
        render(g, tpl, tabs)
        print('ok', g['slug'])
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'stamp_assets.py')], check=True)


if __name__ == '__main__':
    main()
