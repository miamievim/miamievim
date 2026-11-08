# -*- coding: utf-8 -*-
"""Haftalık rehber sayfaları (9 Kasım 2026 haftası): FEMA sel bölgeleri ve sel sigortası; Amendment 3 sonrası emlak vergisi.

Şablon: rehberler/index.html, düzen: neden-miami. Her rakam kaynağı ve tarihiyle burada tutulur.
Kullanım: python3 tools/build_guides_2026_11_09.py
"""
import html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
BASE = 'https://miamievim.com'
NOTE = 'Bu sayfa genel bilgilendirme amaçlıdır; vergi, hukuk, sigorta veya finansman tavsiyesi değildir. Kendi durumunuz için bir vergi danışmanı, sigorta acentesi veya avukata başvurun.'


def link(u, t):
    return f'<a href="{u}" target="_blank" rel="noopener">{E(t)}</a>'


def hood(i, name):
    return f'<a href="/mahalle-raporlari/{i}/">{E(name)}</a>'


def src(u, t):
    return link(u, t)


# ---------------------------------------------------------------- Rehber 1: sel bölgeleri ve sel sigortası
CS1 = {
    'zones': ('FEMA: Flood Zones (bölge tanımları)', 'https://fema.gov/flood-zones'),
    'msc': ('FEMA Flood Map Service Center (adres sorgulama)', 'https://msc.fema.gov/portal/search'),
    'mdc': ('Miami-Dade County: sel bölgesi, kot belgesi ve CRS bilgileri (Kasım 2026 erişimi)', 'https://www.miamidade.gov/environment/insurance-agents.asp'),
    'nfip': ('FEMA NFIP: Why Do I Need Flood Insurance? (F-002, Eylül 2024)', 'https://agents.floodsmart.gov/sites/default/files/media/document/2025-08/FEMA_NFIP_TEXT-ONLY_fema_nfip-why-do-i-need_brochure_20251.pdf'),
    'rr2': ('FEMA: Understanding Risk Rating 2.0 (Temmuz 2025)', 'https://agents.floodsmart.gov/sites/default/files/media/document/2025-08/fema-understanding-risk-rating-2.0-fact-sheet-2025.pdf'),
    'citizens': ('Citizens Property Insurance: New Flood Requirements (4 Aralık 2023)', 'https://www.citizensfla.com/-/new-flood-requirements-begin-january-1'),
    'disc': ('Florida Realtors: Florida Expands Flood Disclosures (30 Eylül 2025)', 'https://www.floridarealtors.org/news-media/news-articles/2025/09/florida-expands-flood-disclosures'),
    'auth': ('Legis1: National Flood Insurance Program Faces Dec. 11 Funding Deadline (7 Ekim 2026)', 'https://legis1.com/news/nfip-reauthorization-faces-december-deadline-with'),
}


def build_flood():
    url = BASE + '/rehberler/sel-bolgeleri-ve-sel-sigortasi/'
    stats = [
        ('$250.000', 'NFIP bina teminatı üst sınırı', 'Müstakil ev ve kondominyum dairede bina için; eşya için ayrıca en fazla $100.000. Kaynak: ' + link(CS1['nfip'][1], 'FEMA') + ' (Eylül 2024).'),
        ('30 gün', 'Bekleme süresi', 'NFIP poliçesi genellikle satın alındıktan 30 gün sonra başlar; konut kredisiyle kapanışta alınan poliçede bekleme yoktur. Kaynak: ' + link(CS1['nfip'][1], 'FEMA') + '.'),
        ('1 Ocak 2027', 'Citizens sel şartı', 'Citizens\'tan rüzgâr teminatlı konut poliçesi olanların kalan grubu için ayrı sel sigortası zorunlu hale geliyor; kondominyum daire sahibi poliçeleri hariç. Kaynak: ' + link(CS1['citizens'][1], 'Citizens') + '.'),
    ]
    sections = [
        ('01', 'Kısa cevap', [
            'Miami\'de bir evin sel riski, FEMA\'nın sel haritasındaki bölgesiyle (flood zone) başlar. Yüksek riskli bölgedeki bir mülkü federal denetimli bir bankanın kredisiyle alıyorsanız sel sigortası zorunludur; nakit alımda yasal zorunluluk yoktur, ancak standart konut sigortası selden doğan hasarı genellikle karşılamaz.',
            'Teklif vermeden önce üç şeyi kontrol edin: adresin FEMA sel bölgesi, binanın kot belgesi (elevation certificate) ve satıcının sel beyanı. Sel sigortası teklifini denetim süresi içinde alın; prim, aynı bölgede bile binadan binaya farklıdır.',
        ], []),
        ('02', 'Sel bölgeleri ne anlama gelir?', [
            '<strong>Yüksek riskli bölgeler (Special Flood Hazard Area):</strong> herhangi bir yılda %1 ihtimalle su basması beklenen alanlar ("100 yıllık sel"). Haritada A ile başlayan bölgeler (A, AE, AH, AO) ve V ile başlayan bölgeler (V, VE) bu gruptadır. V bölgeleri kıyı şeridindeki, dalga etkisinin de hesaba katıldığı alanlardır.',
            '<strong>Orta riskli bölgeler (B ve gölgeli X):</strong> 100 yıllık sel sınırı ile yıllık %0,2 ihtimalli ("500 yıllık") sel sınırı arasında kalan alanlar.',
            '<strong>Düşük riskli bölgeler (C ve gölgesiz X):</strong> 500 yıllık sel kotunun üzerinde kalan alanlar. Düşük risk sıfır risk demek değildir: FEMA\'ya göre 2013–2023 arasında NFIP hasar taleplerinin üçte biri, güncel yüksek riskli bölgelerin dışından geldi.',
        ], ['zones', 'nfip']),
        ('03', 'Bir adresin sel bölgesini nasıl öğrenirsiniz?', [
            'Her adres için ' + link(CS1['msc'][1], 'FEMA Flood Map Service Center') + ' üzerinden haritayı açabilirsiniz; bu araç Miami-Dade, Broward ve Palm Beach\'in tamamında geçerlidir.',
            'Miami-Dade\'de ilçenin Flood Zone GIS haritası ve sel bölgesi danışma hattı (305-372-6466) da kullanılabilir. 1995\'ten sonra yapılmış binaların kot belgesi ilçenin kot belgesi arama uygulamasında bulunabilir; 1995 öncesi ve esaslı tadilat görmemiş binalarda belge için lisanslı bir harita mühendisi (surveyor) gerekebilir.',
            'Kot belgesi, binanın zemin katının taban sel kotuna (base flood elevation) göre yüksekliğini gösterir ve sel sigortası priminde doğrudan etkilidir. İlan sayfasında yazan sel bölgesini değil, resmi haritayı esas alın.',
        ], ['msc', 'mdc']),
        ('04', 'Sel sigortası ne zaman zorunlu?', [
            '<strong>Kredili alım:</strong> yüksek riskli bölgedeki bir mülk için federal denetimli bir kuruluştan konut kredisi kullanıyorsanız sel sigortası zorunludur; kredi kuruluşu bunu kapanıştan önce size bildirir.',
            '<strong>Citizens poliçesi olan evler:</strong> Florida\'nın devlet destekli sigortacısı Citizens, rüzgâr teminatlı konut poliçelerinde ayrı bir sel poliçesini kademeli olarak şart koştu: önce yüksek riskli bölgedekiler (1 Temmuz 2023), ardından bina yeniden yapım maliyetine göre $600.000 (2024), $500.000 (2025) ve $400.000 (2026) üzeri yapılar; kalan konutlar için şart 1 Ocak 2027\'de başlıyor. Şart, sel bölgesinden bağımsızdır. NFIP ya da yetkili bir özel şirketin sel poliçesi kabul edilir; kondominyum daire sahibi poliçeleri bu şartın dışındadır.',
            '<strong>Nakit alım:</strong> yasal zorunluluk yoktur. Karar verirken standart konut poliçesinin selden doğan hasarı genellikle karşılamadığını ve düşük riskli bölgelerden de hasar talebi geldiğini göz önünde bulundurun.',
        ], ['nfip', 'citizens']),
        ('05', 'Sel sigortası primi nasıl belirlenir?', [
            'NFIP 2021\'den bu yana primleri "Risk Rating 2.0" yöntemiyle binaya özel hesaplar: mülkün ne sıklıkla su bastığı, sel türü (yağış, fırtına kabarması, kıyı erozyonu), su kaynağına uzaklık, ilk katın yüksekliği ve yeniden yapım maliyeti. Bu yüzden aynı sokaktaki iki evin primi farklı olabilir.',
            'Mevcut poliçelerde prim artışları kademeli uygulanır; FEMA\'ya göre artışların çoğu yıllık %18 ile sınırlıdır ve prim tam risk fiyatına ulaşana kadar artar. İndirimler ise yenilemede hemen uygulanır.',
            'Belediyelerin sel önleme çalışmaları NFIP primlerine indirim olarak yansır (Community Rating System). Miami-Dade\'in belediye sınırları dışındaki bölgeleri (unincorporated) Class 3 topluluktur ve primlerde %35\'e varan indirim alır (Miami-Dade County, Kasım 2026 erişimi). Belediye sınırları içindeki şehirlerin sınıfı farklıdır; teklif alırken acenteye sorun.',
        ], ['rr2', 'mdc']),
        ('06', 'Kondominyum dairede sel sigortası', [
            'Dairede bina yapısının sel sigortası genellikle derneğin (association) ana poliçesindedir. Teklif vermeden önce dernek belgeleri arasında bu poliçenin olup olmadığını, teminat tutarını ve muafiyetini (deductible) sorun; ana poliçenin yetersiz kaldığı hasarlar özel aidat (special assessment) olarak daire sahiplerine yansıyabilir.',
            'Daire sahibi kendi eşyası için ayrı sel poliçesi alabilir. NFIP, kondominyum dairede bina için en fazla $250.000, eşya için en fazla $100.000 teminat verir.',
            'Bina sağlığı, SIRS ve milestone raporları için <a href="/yatirim/">yatırım sayfasındaki bina sağlığı bölümüne</a> bakın.',
        ], ['nfip']),
        ('07', 'Satıcının sel beyanı', [
            'Florida\'da 1 Ekim 2025\'ten bu yana konut satıcıları alıcıya üç konuda yazılı beyan verir: mülk için yapılmış sel hasarı sigorta talepleri, sel hasarının onarımı için alınan her türlü yardım (yalnızca federal yardım değil) ve satıcının sahipliği süresince mülke zarar veren her sel olayı (Fla. Stat. 689.302).',
            'Kiralamada da benzer kural vardır: 1 yıl veya daha uzun kira sözleşmelerinde ev sahibi aynı beyanı sözleşmeden ayrı bir belgeyle verir (Fla. Stat. 83.512). Beyan verilmemişse ve kiracı ciddi sel hasarına uğrarsa, kiracı sözleşmeyi feshedip peşin ödediği kirayı geri isteyebilir.',
        ], ['disc']),
        ('08', 'Kapanış tarihi için bir not: NFIP\'in yetki süresi', [
            'NFIP, Kongre\'nin kısa süreli uzatmalarıyla çalışır. Ekim 2026 itibarıyla programın yetkisi 11 Aralık 2026\'da sona eriyor; uzatılmazsa NFIP yeni poliçe düzenleme yetkisini kaybeder. Aralık ortası veya sonrasına kapanış planlıyorsanız sel poliçesini erken bağlamayı ve özel sel sigortası tekliflerini de değerlendirin.',
            'Bu tarih Kongre kararıyla değişebilir; kapanıştan önce acentenize güncel durumu sorun.',
        ], ['auth']),
        ('09', 'Bir sonraki adım', [
            'Kıyıya yakın bölgelerin karakterini, sigorta ve sel bölgesi bilgilerini mahalle raporlarında bulabilirsiniz: ' + hood('south-beach', 'South Beach') + ', ' + hood('mid-beach', 'Mid-Beach') + ', ' + hood('north-beach', 'North Beach') + ', ' + hood('surfside', 'Surfside') + ', ' + hood('bal-harbour', 'Bal Harbour') + ', ' + hood('sunny-isles', 'Sunny Isles Beach') + ', ' + hood('key-biscayne', 'Key Biscayne') + ', ' + hood('hollywood-beach', 'Hollywood Beach') + ' ve ' + hood('fort-lauderdale', 'Fort Lauderdale') + '. Körfez kıyısındaki kent merkezleri için ' + hood('brickell', 'Brickell') + ', ' + hood('edgewater', 'Edgewater') + ' ve ' + hood('coconut-grove', 'Coconut Grove') + ' raporlarına bakın.',
            'Bütçenizi ve kriterlerinizi paylaşırsanız güncel MLS ilanları, sel bölgesi bilgisiyle birlikte <a href="/ilanlar/">ilan talep sayfasından</a> size gönderilir.',
        ], []),
    ]
    faq = [
        ('Miami\'de sel sigortası zorunlu mu?', 'Yüksek riskli FEMA sel bölgesindeki (A veya V ile başlayan bölgeler) bir mülkü federal denetimli bir kuruluşun konut kredisiyle alıyorsanız zorunludur. Citizens\'tan rüzgâr teminatlı konut poliçesi olanlar için de ayrı sel poliçesi kademeli olarak şart; kalan konutlarda şart 1 Ocak 2027\'de başlıyor. Nakit alımda yasal zorunluluk yoktur. Bu bilgi sigorta tavsiyesi değildir.'),
        ('Bir evin sel bölgesini nereden öğrenebilirim?', 'FEMA Flood Map Service Center (msc.fema.gov) üzerinden adresle sorgulayabilirsiniz. Miami-Dade\'de ilçenin Flood Zone GIS haritası ve 305-372-6466 numaralı danışma hattı da kullanılabilir; 1995 sonrası binaların kot belgesi ilçenin arama uygulamasında bulunur.'),
        ('X bölgesindeki bir eve sel sigortası gerekir mi?', 'Yasal olarak genellikle gerekmez, ancak X bölgesi düşük veya orta risk anlamına gelir, risksiz anlamına gelmez. FEMA\'ya göre 2013–2023 arasında NFIP hasar taleplerinin üçte biri güncel yüksek riskli bölgelerin dışından geldi. Citizens poliçesi olan evlerde ise şart sel bölgesinden bağımsızdır.'),
        ('Sel sigortası hemen başlar mı?', 'NFIP poliçesi genellikle satın alındıktan 30 gün sonra başlar. Konut kredisiyle kapanışta alınan poliçede bekleme süresi uygulanmaz. Özel sel sigortalarının bekleme süresi şirkete göre değişir.'),
        ('Kondominyum dairede sel sigortasını kim yapar?', 'Bina yapısı genellikle derneğin ana poliçesindedir. Daire sahibi kendi eşyası ve gerekirse dairenin iç kısmı için ayrı poliçe alabilir; NFIP dairede bina için en fazla $250.000, eşya için en fazla $100.000 teminat verir. Satın almadan önce derneğin sel poliçesini ve muafiyetini isteyin.'),
    ]
    return dict(
        slug='sel-bolgeleri-ve-sel-sigortasi', url=url, cs=CS1,
        title='Miami\'de Sel Bölgeleri ve Sel Sigortası (2026) | Aleyna Bozoklar',
        desc='FEMA sel bölgeleri (AE, VE, X), sel sigortası ne zaman zorunlu, Citizens 2027 şartı, prim nasıl belirlenir, satıcının sel beyanı. Resmi kaynaklarla.',
        og='Miami\'de sel bölgeleri ve sel sigortası', headline='Sahil kenarında ev almak: FEMA sel bölgeleri ve sel sigortası (2026)',
        crumb='Sel bölgeleri ve sigorta', tab='Sel ve sigorta',
        h1='Sahil kenarında ev almak: <em>sel bölgeleri ve sigorta</em>',
        lead='Bir adresin sel bölgesini nasıl öğrenirsiniz, sel sigortası ne zaman zorunludur, prim neye göre belirlenir ve satıcı neyi beyan etmek zorundadır? Her kural resmi kaynağıyla.',
        date_iso='2026-11-09', date='9 Kasım 2026', stats=stats, sections=sections, faq=faq,
        sources=list(CS1.values()), cta=('/ilanlar/', 'İlan listesi isteyin'), css=[])


# ---------------------------------------------------------------- Rehber 2: Amendment 3 sonrası emlak vergisi
CS2 = {
    'nbc': ('NBC 6 South Florida: Florida Amendment 3 passes (3–4 Kasım 2026)', 'https://www.nbcmiami.com/elections/florida-amendment-3-election-result-homeowners/3880204/'),
    'faq': ('Manatee County Property Appraiser: Proposed 2026 Florida Property Tax Amendment FAQ', 'https://www.manateepao.gov/data/downloads/Proposed 2026 Florida Property Tax Amendment FAQ.pdf'),
    'fac': ('Florida Association of Counties: HJR 1F Joint Resolution Backgrounder (Haziran 2026)', 'https://www.fl-counties.com/wp-content/uploads/2026/06/HJR-1F-Joint-Resolution-Backgrounder.pdf'),
    'chamber': ('Florida Chamber of Commerce: Florida\'s 2026 Property Tax Amendment 3', 'https://www.flchamber.com/amendment3'),
    'req': ('Miami-Dade Property Appraiser: Exemption Requirements (v. 2/2026)', 'https://www.miamidade.gov/resources-pa/library/guidelines/exemption-requirements.pdf'),
    'file': ('Miami-Dade Property Appraiser: Homestead başvurusu ve son tarih', 'https://www.miamidade.gov/pa/exemptions_homestead_filing.asp'),
}


def build_amend3():
    url = BASE + '/rehberler/amendment-3-emlak-vergisi/'
    stats = [
        ('%62', 'Evet oyu', 'Amendment 3, 3 Kasım 2026 seçiminde %62,01 evet oyuyla kabul edildi; anayasa değişikliği için %60 gerekiyordu. Kaynak: ' + link(CS2['nbc'][1], 'NBC 6') + ' (4 Kasım 2026, oyların %99\'u sayılmışken).'),
        ('$150.000', 'Homestead indirimi, 2027', 'Okul dışı vergilerde; 2028\'de $250.000\'e çıkıyor, 2029\'dan itibaren enflasyona göre artıyor. Okul vergilerindeki $25.000 değişmiyor. Kaynak: ' + link(CS2['faq'][1], 'Manatee PAO') + '.'),
        ('%10 → %5', 'Yatırım mülklerinde artış sınırı', 'Homestead olmayan mülklerde okul dışı vergilerde yıllık vergi değeri artış sınırı 2027\'den itibaren %5. Kaynak: ' + link(CS2['chamber'][1], 'Florida Chamber') + '.'),
    ]
    sections = [
        ('01', 'Kısa cevap', [
            'Florida seçmenleri 3 Kasım 2026\'da emlak vergisiyle ilgili anayasa değişikliği Amendment 3\'ü kabul etti. Değişiklik 1 Ocak 2027\'de yürürlüğe giriyor; etkisi ilk kez Ağustos 2027\'deki TRIM bildirimlerinde ve Kasım 2027 vergi faturalarında görülecek.',
            'En büyük değişiklik birincil konutta (homestead) oturan sahipler için: okul dışı vergilerdeki indirim 2027\'de $150.000\'e, 2028\'de $250.000\'e çıkıyor. Kiraya verilen ve ikinci ev olarak kullanılan mülklerde ise yıllık vergi değeri artış sınırı %10\'dan %5\'e iniyor.',
            'Kritik tarih 31 Aralık 2026: bu tarihe kadar Florida\'da sürekli ikamet edenler yüksek indirimden yararlanabilir; 1 Ocak 2027 ve sonrasında Florida\'ya yerleşenler için bekleme süresi var.',
        ], ['nbc', 'faq']),
        ('02', 'Homestead sahipleri için ne değişiyor?', [
            'Bugün (2026) homestead indirimi toplam $51.411\'dir: ilk $25.000 tüm vergilerde, ikinci dilim yalnızca okul dışı vergilerde uygulanır. 2027\'den itibaren okul dışı vergilerde indirim $150.000, 2028\'de $250.000 olur; okul vergilerinde yalnızca ilk $25.000 muaf kalmaya devam eder. Bu yüzden çoğu ev sahibi okul vergisi ödemeye devam edecek.',
            'Basit bir örnek (yalnızca yöntemi göstermek için): vergi değeri (assessed value) $400.000 olan bir homestead evde okul dışı vergiler bugün yaklaşık $348.589 üzerinden hesaplanır; 2027\'de bu tutar $250.000\'e, 2028\'de $150.000\'e iner. Okul vergileri her iki yılda da $375.000 üzerinden hesaplanır. Gerçek tasarruf; vergi oranlarına (millage), mevcut diğer indirimlere ve uygulama yasasına göre değişir.',
            'Değişiklik vergi oranlarını kendiliğinden düşürmez; belediyeler ve ilçeler oranları, harçları ve vergi dışı aidatları (non-ad valorem) değiştirebilir. Yasama meclisinin ileride indirimi daha da artırma ve okul dışı homestead vergisini kademeli kaldırma takvimini yasayla belirlemesi gerekiyor.',
        ], ['faq', 'fac']),
        ('03', '31 Aralık 2026 neden önemli?', [
            '31 Aralık 2026 itibarıyla Florida\'da sürekli ikamet eden kişiler, diğer şartları sağladıklarında yüksek indirimden yararlanır. Bu tarihe kadar Florida ikametini kurup evi daha sonra alanlar da homestead başvurusu yaptıklarında yüksek indirime hak kazanır.',
            '1 Ocak 2027 veya sonrasında Florida\'ya yerleşenler başlangıçta okul dışı vergilerde $50.000 indirim alır (2028\'den itibaren enflasyona göre artar). Florida homestead indirimini dört yıl sürdürdükten sonra, beşinci yılın 1 Ocak\'ından itibaren yüksek indirime geçerler. Florida Chamber\'a göre ilçe ve belediyeler üçte iki oyla bu süreyi kısaltabilir.',
            'Homestead için, 1 Ocak itibarıyla mülkün sahibi olmak ve orayı sürekli ikametgâh olarak kullanmak gerekir; başvurunun son günü 1 Mart\'tır. Miami-Dade Property Appraiser\'a göre başvuran ABD vatandaşı veya ABD\'de kalıcı oturma izni sahibi (permanent resident) olmalı ve Florida\'da ikamet etmelidir. ABD dışında yaşayan yabancı alıcılar homestead indiriminden yararlanamaz.',
        ], ['faq', 'chamber', 'req', 'file']),
        ('04', 'Yatırım mülkü ve ikinci ev sahipleri için', [
            'Kiraya verilen veya ikinci ev olarak kullanılan konutlar homestead indirimi almaz. Bu mülklerde okul dışı vergilerde yıllık vergi değeri artış sınırı 2027\'den itibaren %10 yerine %5 olacak; bu, piyasa değeri hızlı arttığında verginin daha yavaş artması anlamına gelir.',
            'Sınır okul vergilerinde uygulanmaz; okul vergileri piyasa değerine (just value) göre hesaplanmaya devam eder. Değişiklik vergi oranlarını doğrudan düşürmez.',
            'Satın aldığınızda mülkün vergi değeri yeniden belirlenir; bu nedenle ilandaki "geçen yılın vergisi" alıcı için güvenilir bir gösterge değildir. Net getiri hesabı için <a href="/yatirim/">yatırım sayfasındaki hesaplayıcıyı</a> kullanabilirsiniz.',
        ], ['chamber', 'faq']),
        ('05', 'Neler değişmiyor?', [
            'Save Our Homes sınırı (homestead evlerde yıllık vergi değeri artışı en fazla %3 veya enflasyon, hangisi düşükse) aynen kalıyor. Save Our Homes avantajının yeni eve taşınması (portability) değişmiyor.',
            'Dul, yaşlı, gazi ve engelli indirimleri değişmiyor. Homestead indirimi vergi dışı aidatları (çöp, yağmur suyu gibi non-ad valorem kalemler) düşürmez.',
        ], ['faq']),
        ('06', 'Henüz belli olmayanlar', [
            'Başvuru ve uygulama ayrıntıları uygulama yasasıyla belirlenecek; Manatee County Property Appraiser\'ın SSS belgesi, mevcut homestead sahiplerinin yeniden başvurması gerekip gerekmediğine dair bir hüküm içermiyor. Kesin tasarruf tutarı da yerel vergi oranları belli olmadan hesaplanamıyor.',
            'İlçe ve belediyelerin vergi gelirinin hangi alanlarda kullanılabileceği de değişiklikle sınırlandı (kamu güvenliği, eğitim, altyapı, doğal kaynaklar, borç ödemeleri, emeklilik yükümlülükleri, yönetim giderleri). Yerel bütçelerin buna nasıl uyum sağlayacağı 2027 bütçe döneminde netleşecek.',
        ], ['faq', 'fac']),
        ('07', 'Bir sonraki adım', [
            'Bölgelerin vergi oranlarını (millage), aidat ve sigorta bilgilerini 121 bölgenin <a href="/mahalle-raporlari/">mahalle raporlarında</a> karşılaştırabilirsiniz; örneğin ' + hood('coral-gables', 'Coral Gables') + ', ' + hood('pinecrest', 'Pinecrest') + ', ' + hood('miami-shores', 'Miami Shores') + ', ' + hood('weston', 'Weston') + ' ve ' + hood('boca-raton', 'Boca Raton') + ' müstakil ev ağırlıklı bölgelerdir; ' + hood('brickell', 'Brickell') + ' ve ' + hood('sunny-isles', 'Sunny Isles Beach') + ' kondominyum ağırlıklıdır.',
            'Satın alma takviminizi bu tarihlere göre planlamak için <a href="/#iletisim">bir tanışma görüşmesi</a> isteyebilirsiniz.',
        ], []),
    ]
    faq = [
        ('Amendment 3 kabul edildi mi?', 'Evet. Florida seçmenleri 3 Kasım 2026\'da Amendment 3\'ü %62,01 evet oyuyla kabul etti (NBC 6, oyların %99\'u sayılmışken); kabul için %60 gerekiyordu. Değişiklik 1 Ocak 2027\'de yürürlüğe giriyor.'),
        ('Amendment 3 ile homestead indirimi ne kadar oluyor?', 'Okul dışı vergilerde 2027\'de $150.000, 2028\'de $250.000; 2029\'dan itibaren enflasyona göre artıyor. Okul vergilerinde yalnızca ilk $25.000 muaf kalıyor. 1 Ocak 2027 ve sonrasında Florida\'ya yerleşenler önce $50.000 ile başlıyor. Bu bilgi vergi tavsiyesi değildir.'),
        ('Emlak vergisindeki değişiklik ne zaman faturaya yansıyacak?', 'Değişiklik 1 Ocak 2027\'de yürürlüğe giriyor; etkisi ilk kez Ağustos 2027 TRIM bildirimlerinde ve Kasım 2027\'de gönderilen vergi faturalarında görülecek.'),
        ('Kiraya verdiğim dairenin vergisi düşecek mi?', 'Kendiliğinden düşmez. Homestead olmayan mülklerde okul dışı vergilerde yıllık vergi değeri artış sınırı 2027\'den itibaren %10 yerine %5 olur; bu, değer arttığında verginin daha yavaş artması demektir. Okul vergileri sınırsız kalır ve vergi oranları yerel yönetimlerce belirlenmeye devam eder. Bu bilgi vergi tavsiyesi değildir.'),
        ('Yabancı alıcı Amendment 3\'ten yararlanabilir mi?', 'Homestead indirimi, 1 Ocak itibarıyla mülkte sürekli ikamet eden, ABD vatandaşı veya kalıcı oturma izni sahibi ve Florida\'da ikamet eden sahiplere verilir. ABD dışında yaşayan yabancı alıcılar homestead indirimi alamaz; kiraya verilen veya ikinci ev olarak kullanılan mülklerde yalnızca %5 artış sınırından yararlanılır.'),
    ]
    return dict(
        slug='amendment-3-emlak-vergisi', url=url, cs=CS2,
        title='Amendment 3 Kabul Edildi: Florida Emlak Vergisinde 2027 | Aleyna Bozoklar',
        desc='Amendment 3 (%62 evet): homestead indirimi 2027\'de $150.000, 2028\'de $250.000; yatırım mülklerinde %5 sınırı; 31 Aralık 2026 tarihi. Resmi kaynaklı.',
        og='Amendment 3 kabul edildi: emlak vergisinde ne değişiyor?', headline='Amendment 3 kabul edildi: Miami\'de emlak vergisinde 2027\'den itibaren ne değişiyor?',
        crumb='Amendment 3 ve emlak vergisi', tab='Amendment 3',
        h1='Amendment 3 kabul edildi: <em>emlak vergisinde ne değişiyor?</em>',
        lead='Florida\'da 3 Kasım 2026\'da kabul edilen emlak vergisi değişikliği; homestead sahipleri, yeni gelenler ve yatırımcılar için ne anlama geliyor, ne zaman faturaya yansıyacak? Her kural resmi kaynağıyla.',
        date_iso='2026-11-09', date='9 Kasım 2026', stats=stats, sections=sections, faq=faq,
        sources=list(CS2.values()), cta=('/yatirim/', 'Net getiriyi hesaplayın'), css=[])


# ---------------------------------------------------------------- ortak sayfa üretimi
TABS = [('/rehberler/', 'Tüm rehberler'), ('/rehberler/neden-miami/', 'Neden Miami?')]


def render(g, tpl, tabs):
    head_end = tpl.index('</head>')
    body_start = tpl[tpl.index('<body>'):tpl.index('<main id="main">')]
    footer = tpl[tpl.index('</main>') + len('</main>'):]
    head = tpl[:tpl.index('<title>')]
    links = re.findall(r'<link (?:rel="(?:preconnect|stylesheet|icon|apple-touch-icon)"|href="https://fonts\.googleapis\.com)[^>]*>', tpl[:head_end])
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
            src = '<p class="wm-src">Kaynak: ' + ' · '.join(link(g['cs'][k][1], g['cs'][k][0]) for k in sk) + '</p>'
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
    guides = [build_flood(), build_amend3()]
    tabs = TABS + [('/rehberler/' + g['slug'] + '/', g['tab']) for g in guides]
    for g in guides:
        render(g, tpl, tabs)
        print('ok', g['slug'])
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'stamp_assets.py')], check=True)


if __name__ == '__main__':
    main()
