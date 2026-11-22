# -*- coding: utf-8 -*-
"""Haftalık rehber sayfaları (23 Kasım 2026 haftası): Miami'de kısa dönem kiralama (Airbnb) kuralları; kira getirisi nasıl hesaplanır.

Şablon: rehberler/index.html, düzen: neden-miami. Her rakam kaynağı ve tarihiyle burada tutulur.
Kullanım: python3 tools/build_guides_2026_11_23.py
"""
import html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
BASE = 'https://miamievim.com'
NOTE = 'Bu sayfa genel bilgilendirme amaçlıdır; hukuk, vergi veya yatırım tavsiyesi değildir. Kısa dönem kiralama kuralları ve vergi oranları değişebilir; bir mülkü kiraya vermeden önce ilgili belediyeye, kondominyum derneğine ve bir vergi danışmanına veya Florida avukatına başvurun.'
NOTE_YIELD = 'Bu sayfa genel bilgilendirme amaçlıdır; yatırım, vergi veya finansman tavsiyesi değildir. Getiri garanti edilmez. Vergi ve yapılandırma kararları için bir vergi danışmanına veya avukata başvurun.'


def link(u, t):
    return f'<a href="{u}" target="_blank" rel="noopener">{E(t)}</a>'


def hood(i, name):
    return f'<a href="/mahalle-raporlari/{i}/">{E(name)}</a>'


# Ortak kaynaklar (Kasım 2026 erişimi)
S = {
    'dbpr': ('Florida DBPR: Vacation Rental licensing guide (Kasım 2026 erişimi)', 'https://www2.myfloridalicense.com/hotels-restaurants/licensing/vrtsp-guide/'),
    'fs212': ('Florida Statutes 212.03: Transient rentals tax (2025 sürümü)', 'https://www.flsenate.gov/Laws/Statutes/2025/0212.03'),
    'tdt': ('Florida Department of Revenue: DR-15TDT, Local Option Transient Rental Tax Rates (R. 03/25)', 'https://www.floridarevenue.com/Forms_library/current/dr15tdt.pdf'),
    'dss': ('Florida Department of Revenue: DR-15DSS, Discretionary Sales Surtax, Calendar Year 2026', 'https://floridarevenue.com/Forms_library/current/dr15dss_26.pdf'),
    'mb': ('City of Miami Beach: Vacation / Short Term Rentals', 'https://www.miamibeachfl.gov/?p=28205'),
    'mbsafe': ('City of Miami Beach: Practice Safe Renting', 'https://apps.miamibeachfl.gov/practicesaferenting'),
    'miami': ('City of Miami: Short Term Rental Info (Zoning FAQs)', 'https://miami.gov/Planning-Zoning-Land-Use/Zoning-FAQs/Short-Term-Rental-Info'),
    'miamiproc': ('City of Miami: How to Convert to a Short-Term Rental/Lodging', 'https://www.miami.gov/Permits-Construction/Short-Term-RentalLodging-Procedures'),
    'mdc': ('Miami-Dade County: Residential Short-Term Vacation Rentals (Sec. 33-28)', 'https://miamidade.gov/building/standards/residential-short-term-vacation-rentals.asp'),
    'condo': ('Florida Statutes 718.110(13): kiralama haklarını kısıtlayan beyanname değişiklikleri', 'https://www.flsenate.gov/Laws/Statutes/2005/718.110'),
    'irs': ('IRS: Nonresident aliens, real property located in the U.S. (23 Temmuz 2026 güncellemesi)', 'https://www.irs.gov/individuals/international-taxpayers/nonresident-aliens-real-property-located-in-the-u-s'),
    'firpta': ('IRS: FIRPTA Withholding', 'https://www.irs.gov/individuals/international-taxpayers/firpta-withholding'),
    'pto': ('Florida Department of Revenue: PTO Bulletin 26-21, Constitutional Amendment 3 (5 Kasım 2026)', 'https://floridarevenue.com/property/Documents/PTO_BUL_26-21.pdf'),
    'pa': ('Miami-Dade Property Appraiser: Property Value Cap', 'https://miamidade.gov/pa/property_value_cap.asp'),
}


def pick(*keys):
    return {k: S[k] for k in keys}


# ---------------------------------------------------------------- Rehber 1: kısa dönem kiralama
CS1 = pick('dbpr', 'mb', 'mbsafe', 'miami', 'miamiproc', 'mdc', 'condo', 'fs212', 'tdt', 'dss', 'irs')


def build_str():
    url = BASE + '/rehberler/kisa-donem-kiralama-kurallari/'
    stats = [
        ('30 gün', 'Eyalet lisansının eşiği', 'Bir konutun tamamını bir takvim yılında üçten fazla kez, 30 günden kısa sürelerle kiraya veriyorsanız Florida DBPR\'den tatil kiralaması (vacation rental) lisansı gerekir. Kaynak: ' + link(CS1['dbpr'][1], 'Florida DBPR') + '.'),
        ('6 ay + 1 gün', 'Miami Beach\'te kısa dönemin tanımı', 'Miami Beach, 6 ay ve 1 günden kısa kiralamaları kısa dönem sayar; tüm müstakil evlerde ve bazı imar bölgelerindeki birçok apartmanda yasaktır. Kaynak: ' + link(CS1['mb'][1], 'City of Miami Beach') + '.'),
        ('%13', 'Miami-Dade\'de konaklama vergisi', 'Eyalet satış vergisi %6, Miami-Dade ilçe ek vergisi %1 ve ilçenin yerel konaklama vergisi %6. Miami Beach\'te yerel oran %7, Surfside ve Bal Harbour\'da %4. Kaynak: ' + link(CS1['tdt'][1], 'DR-15TDT') + ', ' + link(CS1['dss'][1], 'DR-15DSS 2026') + '.'),
    ]
    sections = [
        ('01', 'Kısa cevap', [
            'Miami\'de bir daireyi veya evi Airbnb gibi platformlarda kısa dönem kiraya verebilmek için üç ayrı katmanın aynı anda izin vermesi gerekir: <strong>eyalet</strong> (Florida DBPR lisansı ve konaklama vergisi kaydı), <strong>şehir</strong> (mülkün bulunduğu belediyenin imar kuralları ve iş ruhsatı) ve <strong>bina</strong> (kondominyum beyannamesi ve dernek kuralları). Biri bile izin vermiyorsa kısa dönem kiralama yapılamaz.',
            'Bu yüzden yatırım amacıyla mülk alırken soru "bu daire Airbnb\'ye verilebilir mi?" değil, "bu adres, bu imar bölgesi ve bu binanın yönetmeliği hangi kiralama süresine izin veriyor?" olmalıdır. Cevabı teklif vermeden önce yazılı olarak alın.',
        ], ['dbpr', 'mb', 'miami']),
        ('02', 'Eyalet katmanı: Florida DBPR lisansı', [
            '<strong>Kimin lisansa ihtiyacı var:</strong> bir konutun tamamını bir takvim yılında üçten fazla kez, 30 günden (veya bir takvim ayından) kısa sürelerle kiraya veren ya da düzenli olarak bu şekilde kiralandığını ilan eden mülk sahipleri.',
            '<strong>İki lisans türü:</strong> kondominyum veya kooperatif dairesi için "Vacation Rental – Condominium"; müstakil ev, townhouse veya dört ve daha az birimli bir yapıdaki birim için "Vacation Rental – Dwelling".',
            '<strong>Ücretler:</strong> yeni başvuruda $50 başvuru ücreti, $10 HEP ücreti ve lisans ücreti; tek birim için lisans ücreti tam yıl $170, yarım yıl $90. Miami-Dade\'de lisans her yıl 1 Ekim\'de yenilenir.',
            '<strong>Ek şartlar:</strong> üç ve daha fazla katlı binalarda (balkonlar kondominyum ortak alanı değilse) üç yılda bir balkon denetim belgesi; bazı kondominyum binalarında yangın sprinkleri; lisansın mülkte görünür biçimde bulundurulması.',
        ], ['dbpr']),
        ('03', 'Miami Beach: en sıkı kurallar', [
            'Miami Beach, 6 ay ve 1 günden kısa kiralamaları kısa dönem sayar. Şehrin açıklamasına göre bu kiralamalar <strong>tüm müstakil evlerde</strong> ve belirli imar bölgelerindeki <strong>birçok apartman binasında yasaktır</strong> (Şehir Kanunu Sec. 142-1111 ve 142-905(b)).',
            'İzin verilen bölgelerde mülk sahibinin şehirden kısa dönem kiralama iş vergisi makbuzu (Vacation/Short-Term Rental Business Tax Receipt) ve bir resort tax (konaklama vergisi) hesabı alması gerekir. Bu iki belgenin numarası her ilanda ve her reklamda gösterilmelidir (Sec. 102-386).',
            'Yasak bir yerde kısa dönem kiralama yapıldığında şehir, kiracıların tahliye edileceğini ve mülk sahibine para cezası kesileceğini belirtiyor. Bir adresin hangi imar bölgesinde olduğunu ve kısa dönem kiralamaya açık olup olmadığını satın almadan önce şehrin planlama dairesine sorun.',
        ], ['mb', 'mbsafe']),
        ('04', 'City of Miami: Brickell, Downtown, Edgewater ve diğerleri', [
            'City of Miami\'de kısa dönem kiralama bir konaklama (lodging) kullanımı sayılır. Konaklamanın hangi bölgelerde serbest olduğu Miami 21 imar kanununun 4. madde, 3. tablosunda yer alır. Şehrin açıklamasına göre T3 ve T4-R bölgelerindeki müstakil evler ve iki aileli evler (duplex) kısa dönem kiralamaya uygun değildir.',
            'Konaklamanın serbest olduğu bir bölgede bile mevcut bir daireyi kısa dönem kiralamaya açmak bir dönüşüm sürecidir: geçerli iskân belgesi (Certificate of Occupancy) ve kullanım belgesi (Certificate of Use), şehrin değerlendirme formu, kondominyum veya site derneğinin imzaladığı bir işletme yönetim planı, yapı ruhsatı ve denetimler, DBPR konaklama lisansı, konaklama için yeni kullanım belgesi ve iş vergisi makbuzu (BTR). Kullanım belgesi ve BTR her yıl yenilenir.',
            'Bu nedenle City of Miami\'de "kısa dönem kiralamaya uygun" olarak pazarlanan binalar genellikle bu izinleri bina düzeyinde almış olan binalardır. Bir dairede bu süreci tek başına yürütmek mümkün olsa da dernek imzası olmadan ilerlemez.',
        ], ['miami', 'miamiproc']),
        ('05', 'Diğer belediyeler ve ilçe bölgeleri', [
            'Miami-Dade\'nin belediyeye bağlı olmayan (unincorporated) bölgelerinde, bir konutun tamamının veya bir bölümünün 30 günden ya da bir takvim ayından kısa sürelerle kiraya verilmesi ilçe kanununun 33-28. bölümüne tabidir; kondominyum ve apartman daireleri de bu tanıma girer.',
            'Mülk bir belediyenin sınırları içindeyse (örneğin Sunny Isles Beach, Aventura, Surfside, Bal Harbour, Coral Gables, Doral) kuralları o belediye belirler; ilçe de bu durumda doğrudan belediyeye başvurulmasını istiyor. Broward ve Palm Beach\'te de her şehrin kendi kayıt ve imar kuralları vardır.',
        ], ['mdc']),
        ('06', 'Bina katmanı: kondominyum beyannamesi', [
            'Şehir izin verse bile kondominyum beyannamesi (declaration) ve dernek kuralları kiralamayı yasaklayabilir veya en kısa kira süresi, yıllık kiralama sayısı, ilk yıl kiraya verme yasağı, kiracı onayı ve kayıt ücreti gibi sınırlar koyabilir. Bunlar binadan binaya değişir.',
            'Fla. Stat. 718.110(13)\'e göre kiralama haklarını kısıtlayan bir beyanname değişikliği, değişikliği onaylayan daire sahiplerini ve değişiklik yürürlüğe girdikten sonra daire satın alanları bağlar. Yani bir daireyi satın aldığınızda, o tarihte geçerli olan kısıtlamalar size de uygulanır. Satıcının vermesi gereken dernek belgelerinde kiralama bölümünü teklif aşamasında okuyun ve kısa dönem kiralama planınız varsa bunu bir Florida avukatına teyit ettirin.',
            'Yeni projelerde kiralama kuralları geliştiricinin hazırladığı beyannamede yazar; <a href="/yeni-projeler/">yeni projeler sayfasında</a> kısa süreli kiralamaya uygun olarak işaretlenen projeleri ayrıca görebilirsiniz.',
        ], ['condo']),
        ('07', 'Kısa dönem kiralamada vergiler', [
            '<strong>Konaklama vergileri:</strong> 6 aydan kısa kiralamalar Florida\'da konaklama (transient rental) vergisine tabidir: kira bedeli üzerinden %6 eyalet satış vergisi, ilçe ek satış vergisi (discretionary sales surtax) ve ilçenin yerel konaklama vergisi. Miami-Dade\'de ek vergi %1, yerel konaklama vergisi ilçenin büyük bölümünde %6, Miami Beach\'te %7, Surfside ve Bal Harbour\'da %4. Broward\'da ek vergi %1 ve yerel konaklama vergisi %6; Palm Beach\'te 1 Ocak 2026\'dan itibaren ek vergi %0,5 ve yerel konaklama vergisi %6.',
            'Bu üç ilçede yerel konaklama vergisi ilçeye ödenir; eyalet vergisi ve ek vergi ise Florida Department of Revenue\'ya DR-15 beyannamesiyle beyan edilir. Bazı platformlar bu vergilerin bir kısmını sizin adınıza tahsil eder; hangilerini tahsil ettiğini kendi hesabınızda kontrol edin.',
            '<strong>Uzun dönem kiralama:</strong> 6 aydan uzun, yazılı ve gerçek bir kira sözleşmesiyle sürekli ikamet amacıyla yapılan kiralamalar bu konaklama vergisine tabi değildir (Fla. Stat. 212.03).',
            '<strong>Gelir vergisi:</strong> ABD\'de yerleşik olmayan yabancıların ABD\'deki mülkten elde ettiği kira geliri, bir ticari faaliyetle bağlantılı değilse brüt tutar üzerinden %30 (veya vergi anlaşmasındaki daha düşük oran) ile vergilenir. Mülk sahibi IRC 871(d) seçimiyle bu geliri ticari faaliyet geliri sayabilir; o durumda giderler düşülür ve net gelir kademeli oranlarla vergilenir. Seçim için ödeyiciye W-8ECI formu verilir ve her yıl 1040-NR beyannamesi verilir.',
        ], ['fs212', 'tdt', 'dss', 'irs']),
        ('08', 'Satın almadan önce kontrol listesi', [
            '1. Adresin bağlı olduğu belediye ve imar bölgesi kısa dönem konaklamaya izin veriyor mu? (Belediyenin planlama dairesine yazılı soru.)',
            '2. Kondominyum beyannamesi ve kuralları en kısa kira süresi, yıllık kiralama sayısı ve ilk yıl kiralama hakkında ne diyor?',
            '3. Bina veya daire için hangi belgeler gerekiyor: DBPR lisansı, şehir iş vergisi makbuzu, kullanım belgesi, konaklama vergisi kayıtları?',
            '4. Konaklama vergileri, platform komisyonu, temizlik, mobilya ve boş günler düşüldükten sonra net getiri nedir? Bunu <a href="/rehberler/kira-getirisi-hesaplama/">kira getirisi rehberindeki</a> yöntemle ve <a href="/yatirim/">yatırım hesaplayıcısıyla</a> uzun dönem kiralamayla karşılaştırın.',
        ], []),
        ('09', 'Bir sonraki adım', [
            'Kondominyum ağırlıklı bölgelerin aidat, sigorta ve kira bilgilerini mahalle raporlarında bulabilirsiniz: ' + hood('south-beach', 'South Beach') + ', ' + hood('mid-beach', 'Mid-Beach') + ', ' + hood('north-beach', 'North Beach') + ', ' + hood('brickell', 'Brickell') + ', ' + hood('downtown-miami', 'Downtown Miami') + ', ' + hood('edgewater', 'Edgewater') + ', ' + hood('sunny-isles', 'Sunny Isles Beach') + ', ' + hood('hollywood-beach', 'Hollywood Beach') + ' ve ' + hood('fort-lauderdale', 'Fort Lauderdale') + '. Raporlar bir binanın kısa dönem kiralamaya açık olup olmadığını göstermez; bu her adres için ayrıca kontrol edilir.',
        ], []),
    ]
    faq = [
        ('Miami\'de her daire Airbnb\'ye verilebilir mi?', 'Hayır. Kısa dönem kiralama için eyalet lisansı, belediyenin imar izni ve binanın kondominyum beyannamesinin aynı anda izin vermesi gerekir. Miami Beach\'te 6 ay ve 1 günden kısa kiralamalar tüm müstakil evlerde ve belirli bölgelerdeki birçok apartmanda yasaktır; City of Miami\'de konaklama yalnızca Miami 21\'in izin verdiği bölgelerde ve gerekli belgelerle yapılabilir.'),
        ('Florida\'da tatil kiralaması lisansı ne zaman gerekir?', 'Bir konutun tamamını bir takvim yılında üçten fazla kez, 30 günden veya bir takvim ayından kısa sürelerle kiraya veriyorsanız ya da böyle kiralandığını ilan ediyorsanız Florida DBPR\'den lisans gerekir. Tek birim için lisans ücreti tam yıl $170\'dir; yeni başvuruda $50 başvuru ve $10 HEP ücreti eklenir (DBPR, Kasım 2026).'),
        ('Miami\'de kısa dönem kiralamada ne kadar vergi ödenir?', 'Miami-Dade\'nin büyük bölümünde kira bedeli üzerinden %6 eyalet satış vergisi, %1 ilçe ek vergisi ve %6 yerel konaklama vergisi, toplam %13. Miami Beach\'te yerel oran %7, Surfside ve Bal Harbour\'da %4 (Florida Department of Revenue, DR-15TDT ve DR-15DSS 2026). Gelir vergisi bunlardan ayrıdır. Bu bilgi vergi tavsiyesi değildir.'),
        ('Kondominyum derneği kiralamayı yasaklayabilir mi?', 'Evet. Kondominyum beyannamesi ve dernek kuralları kiralamayı yasaklayabilir veya en kısa kira süresi, yıllık kiralama sayısı gibi sınırlar koyabilir. Fla. Stat. 718.110(13)\'e göre kiralama haklarını kısıtlayan bir değişiklik, onu onaylayan sahipleri ve değişiklikten sonra satın alanları bağlar. Bu bilgi hukuk tavsiyesi değildir.'),
        ('6 aydan uzun kiralamada konaklama vergisi var mı?', 'Hayır. Florida\'da 6 aydan uzun, yazılı ve gerçek bir kira sözleşmesiyle sürekli ikamet amacıyla yapılan kiralamalar konaklama vergisine tabi değildir (Fla. Stat. 212.03). Kira gelirinin gelir vergisi ise ayrıca değerlendirilir.'),
    ]
    return dict(
        slug='kisa-donem-kiralama-kurallari', url=url, cs=CS1,
        title='Miami\'de Kısa Dönem Kiralama (Airbnb) Kuralları (2026) | Aleyna Bozoklar',
        desc='Miami ve Miami Beach\'te Airbnb kuralları: Florida DBPR lisansı, belediye imar izinleri, kondominyum beyannamesi, %13\'e varan konaklama vergileri ve satın almadan önce kontrol listesi.',
        og='Miami\'de kısa dönem kiralama (Airbnb) kuralları', headline='Miami\'de kısa dönem kiralama (Airbnb) kuralları: eyalet lisansı, belediye izni, bina yönetmeliği ve vergiler (2026)',
        crumb='Kısa dönem kiralama', tab='Kısa dönem kiralama',
        h1='Miami\'de kısa dönem kiralama: <em>Airbnb kuralları</em>',
        lead='Bir daireyi Airbnb\'ye vermek için eyalet, şehir ve bina katmanlarının üçünün de izin vermesi gerekir. Miami Beach ve City of Miami kuralları, kondominyum beyannamesi ve konaklama vergileri; her kural resmi kaynağıyla.',
        date_iso='2026-11-23', date='23 Kasım 2026', stats=stats, sections=sections, faq=faq,
        sources=list(CS1.values()), cta=('/yatirim/', 'Net getirinizi hesaplayın'), css=[], note=NOTE)


# ---------------------------------------------------------------- Rehber 2: kira getirisi
CS2 = pick('pa', 'pto', 'fs212', 'tdt', 'dss', 'irs', 'firpta')


def build_yield():
    url = BASE + '/rehberler/kira-getirisi-hesaplama/'
    stats = [
        ('3 ölçü', 'Brüt, net ve nakit getirisi', 'Brüt getiri ilandaki kiraya, net getiri giderler düşüldükten sonra kalana, nakit getirisi ise krediyle alımda cebinizden çıkan paraya bakar. Hesaplama yöntemleri aşağıda.'),
        ('%10 → %5', 'Emlak vergisi değer artışı sınırı', 'Homestead olmayan (yatırım) mülklerde vergi değerinin yıllık artış sınırı, 3 Kasım 2026\'da kabul edilen Amendment 3 ile 2027 vergi listesinden itibaren %10\'dan %5\'e iniyor. Kaynak: ' + link(CS2['pto'][1], 'Florida DOR, PTO 26-21') + ' (5 Kasım 2026).'),
        ('%30', 'Yabancıların brüt kira vergisi', 'ABD\'de yerleşik olmayan yabancıların kira geliri, IRC 871(d) seçimi yapılmazsa brüt tutar üzerinden %30 (veya anlaşmadaki daha düşük oran) ile vergilenir. Kaynak: ' + link(CS2['irs'][1], 'IRS') + ' (Temmuz 2026).'),
    ]
    sections = [
        ('01', 'Kısa cevap', [
            'İlanlarda yazan getiri çoğunlukla <strong>brüt getiridir</strong>: yıllık kiranın satın alma fiyatına oranı. Yatırım kararını belirleyen ise <strong>net getiridir</strong>: aidat, emlak vergisi, sigorta, yönetim, bakım ve boş kalınan aylar düşüldükten sonra kalan gelirin toplam alım maliyetine oranı. Krediyle alıyorsanız buna bir üçüncü ölçü eklenir: <strong>nakit getirisi</strong> (cash-on-cash).',
            'Miami\'de özellikle kondominyum dairelerinde aidat ve sigorta önemli kalemler olduğu için iki dairenin brüt getirisi aynı olsa bile net getirileri çok farklı çıkabilir. Karşılaştırmayı her zaman net getiriyle yapın.',
        ], []),
        ('02', 'Brüt getiri', [
            '<strong>Formül:</strong> brüt getiri = yıllık kira ÷ satın alma fiyatı × 100.',
            'Yıllık kira, aylık kiranın 12 ile çarpımıdır; boş aylar ve giderler hesaba katılmaz. Bu yüzden brüt getiri yalnızca ilk eleme için kullanılır: bir bölgede veya binada kiraların fiyata göre yüksek mi düşük mü olduğunu hızlıca gösterir, ama elinize geçecek parayı göstermez.',
        ], []),
        ('03', 'Net getiri (net işletme geliri)', [
            '<strong>Formül:</strong> net getiri = (tahsil edilen yıllık kira − yıllık işletme giderleri) ÷ toplam alım maliyeti × 100.',
            '<strong>Tahsil edilen kira:</strong> yıllık kiradan boş kalınan aylar düşülür. Uzun dönem kiralamada bu, kiracı değişimleri arasındaki süredir; kısa dönem kiralamada doluluk oranı belirleyicidir.',
            '<strong>İşletme giderleri:</strong> aylık aidat (HOA) ve onaylanmış özel aidatlar, emlak vergisi, konut ve gerekiyorsa sel sigortası, yönetim ücreti, bakım ve onarım. Kısa dönem kiralamada buna konaklama vergileri (kiracıdan tahsil edilip devlete ödenir), platform komisyonu, temizlik, mobilya ve faturalar eklenir.',
            '<strong>Toplam alım maliyeti:</strong> satın alma fiyatına kapanış masrafları (tapu sigortası, kayıt ücretleri, avukat ve denetim ücretleri) ve kiraya hazırlık için yapılan harcamalar eklenir.',
            'Kredi faizi ve anapara ödemeleri net getiriye dahil edilmez; böylece mülkün kendi getirisi finansman yönteminden bağımsız olarak ölçülür. Bu oran sektörde cap rate olarak da anılır.',
        ], []),
        ('04', 'Nakit getirisi (krediyle alımda)', [
            '<strong>Formül:</strong> nakit getirisi = (net işletme geliri − yıllık kredi ödemeleri) ÷ cebinizden çıkan toplam nakit × 100.',
            'Cebinizden çıkan nakit; peşinat, kapanış masrafları ve kiraya hazırlık harcamalarıdır. Kredi faizi net getirinin üzerindeyse kredi nakit getirisini düşürür; altındaysa yükseltir. Yabancı uyruklulara verilen (foreign national) kredilerde peşinat ve faiz şartları bankaya göre değiştiği için bu hesabı bankanın yazılı teklifiyle yapın.',
        ], []),
        ('05', 'Emlak vergisini doğru tahmin etmek', [
            'Yatırım mülkleri homestead indiriminden yararlanamaz. Miami-Dade Emlak Değerleme Dairesine göre homestead olmayan mülklerde vergi değerinin yıllık artışı (okul vergileri hariç) %10 ile sınırlıdır ve mülk el değiştirdiğinde bu sınırın başlangıç yılı sıfırlanır. Yani satın aldıktan sonraki yıl vergi değeri yeniden belirlenir; önceki sahibin vergi faturası size rehber olmaz.',
            '3 Kasım 2026\'da kabul edilen Amendment 3, homestead olmayan mülklerde yıllık artış sınırını %10\'dan %5\'e indiriyor. Değişiklik 1 Ocak 2027\'de yürürlüğe giriyor ve ilk kez 2027 vergi listesine uygulanıyor. Sınır mevcut vergi değerinin artışını sınırlar; satın alma sonrası yeniden değerlemeyi engellemez.',
            'Tahmin için satın alma fiyatına yakın bir vergi değeri ve bölgenin güncel vergi oranıyla hesap yapın; mahalle raporlarında her bölgenin vergi bilgisi kaynağıyla yer alır.',
        ], ['pa', 'pto']),
        ('06', 'Kira gelirinin vergileri', [
            '<strong>Eyalet:</strong> Florida\'da kişisel eyalet gelir vergisi yoktur (bkz. <a href="/rehberler/neden-miami/">Neden Miami?</a>). Kira gelirinde federal vergi ve, kısa dönem kiralamada, konaklama vergileri söz konusudur.',
            '<strong>Uzun ve kısa dönem farkı:</strong> 6 aydan uzun, yazılı ve gerçek bir kira sözleşmesiyle yapılan kiralamalar konaklama vergisine tabi değildir. 6 aydan kısa kiralamalarda Miami-Dade\'nin büyük bölümünde %6 eyalet, %1 ilçe ek vergisi ve %6 yerel konaklama vergisi uygulanır (Miami Beach\'te yerel oran %7, Surfside ve Bal Harbour\'da %4). Ayrıntılar <a href="/rehberler/kisa-donem-kiralama-kurallari/">kısa dönem kiralama rehberinde</a>.',
            '<strong>Federal gelir vergisi (yabancılar):</strong> ABD\'de yerleşik olmayan yabancıların kira geliri, IRC 871(d) seçimi yapılmazsa brüt kira üzerinden %30 (veya vergi anlaşmasındaki daha düşük oran) ile vergilenir. Seçim yapılırsa aidat, vergi, sigorta, yönetim ve amortisman gibi giderler düşülür ve net gelir kademeli oranlarla vergilenir. Seçim için ödeyiciye W-8ECI verilir ve her yıl 1040-NR beyannamesi verilir. IRS\'e göre beyanname asıl son tarihten itibaren 16 ay içinde verilmezse giderler düşülemez. Net getiri hesabınızı, hangi yöntemin uygulanacağını bir vergi danışmanıyla netleştirdikten sonra vergi sonrası olarak da yapın.',
        ], ['fs212', 'tdt', 'dss', 'irs']),
        ('07', 'Çıkışı baştan hesaba katın: FIRPTA', [
            'Toplam getiri yalnızca kira gelirinden oluşmaz; satıştaki değer artışı ve satış masrafları da sonucu belirler. Yabancı uyruklu bir satıcı ABD\'deki gayrimenkulünü sattığında alıcı, kural olarak satış bedelinin %15\'ini kesip IRS\'e yatırır (FIRPTA). Bu bir kesintidir, nihai vergi değildir; fazla kesilen tutar beyannameyle geri istenebilir. Satış yılındaki nakit akışınızı planlarken bu kesintiyi hesaba katın.',
        ], ['firpta']),
        ('08', 'Sık yapılan hatalar', [
            '<strong>Önceki sahibin vergi faturasını kullanmak:</strong> homestead indirimli veya uzun süredir sınırlı artışla gelen bir vergi tutarı, satın almadan sonra belirgin biçimde artabilir.',
            '<strong>Boş ayları ve bakım payını sıfır almak:</strong> kiracı değişimi, boya, cihaz yenileme ve kısa dönem kiralamada sezon farkı her yıl gelir kaybı yaratır.',
            '<strong>Özel aidatları atlamak:</strong> binanın yapısal denetim ve yedek akçe (SIRS) durumu gelecekteki özel aidatları belirler; dernek belgelerinde onaylanmış veya görüşülen özel aidatları hesaba katın.',
            '<strong>Kısa dönem kiralama izni olmadan kısa dönem kirası varsaymak:</strong> bina veya belediye izin vermiyorsa hesap uzun dönem kirasıyla yapılmalıdır.',
            '<strong>Brüt getiriyle karşılaştırmak:</strong> aidatı yüksek yeni bir bina ile aidatı düşük eski bir bina brüt getiride aynı, net getiride farklı görünebilir.',
        ], []),
        ('09', 'Bir sonraki adım', [
            'Kendi rakamlarınızla net getiriyi <a href="/yatirim/">yatırım sayfasındaki hesaplayıcıda</a> görebilirsiniz. Bölgelerin kira, aidat, vergi ve sigorta bilgileri mahalle raporlarında kaynaklarıyla yer alır: ' + hood('brickell', 'Brickell') + ', ' + hood('edgewater', 'Edgewater') + ', ' + hood('downtown-miami', 'Downtown Miami') + ', ' + hood('doral', 'Doral') + ', ' + hood('aventura', 'Aventura') + ', ' + hood('fort-lauderdale', 'Fort Lauderdale') + ' ve ' + hood('west-palm-beach', 'West Palm Beach') + '. Proje aşamasındaki dairelerin teslim tarihleri ve ödeme planları <a href="/yeni-projeler/">yeni projeler sayfasında</a>.',
        ], []),
    ]
    faq = [
        ('Brüt getiri ile net getiri arasındaki fark nedir?', 'Brüt getiri yıllık kiranın satın alma fiyatına oranıdır. Net getiri ise boş aylar, aidat, emlak vergisi, sigorta, yönetim ve bakım düşüldükten sonra kalan gelirin toplam alım maliyetine (fiyat ve kapanış masrafları) oranıdır. Yatırım kararı için net getiri kullanılır.'),
        ('Kira getirisi hesabına kredi faizi dahil edilir mi?', 'Net getiri (cap rate) hesabına dahil edilmez; mülkün getirisi finansmandan bağımsız ölçülür. Krediyle alımda ayrıca nakit getirisi hesaplanır: net işletme gelirinden yıllık kredi ödemeleri düşülür ve sonuç cebinizden çıkan toplam nakde bölünür.'),
        ('Satın aldıktan sonra emlak vergisi değişir mi?', 'Evet. Mülk el değiştirdiğinde vergi değeri yeniden belirlenir ve homestead olmayan mülklerdeki artış sınırının başlangıç yılı sıfırlanır (Miami-Dade Property Appraiser). Amendment 3 ile bu sınır 2027 vergi listesinden itibaren %10\'dan %5\'e iniyor (Florida DOR, 5 Kasım 2026).'),
        ('Yabancı olarak kira gelirine ne kadar vergi öderim?', 'IRS\'e göre ABD\'de yerleşik olmayan yabancıların kira geliri, ticari faaliyet geliri sayılmazsa brüt tutar üzerinden %30 (veya vergi anlaşmasındaki daha düşük oran) ile vergilenir. IRC 871(d) seçimiyle giderler düşülür ve net gelir kademeli oranlarla vergilenir. Florida\'da eyalet gelir vergisi yoktur. Bu bilgi vergi tavsiyesi değildir.'),
        ('Uzun dönem kirada konaklama vergisi ödenir mi?', 'Hayır. Florida\'da 6 aydan uzun, yazılı ve gerçek bir kira sözleşmesiyle sürekli ikamet amacıyla yapılan kiralamalar konaklama vergisine tabi değildir (Fla. Stat. 212.03). 6 aydan kısa kiralamalarda Miami-Dade\'nin büyük bölümünde toplam %13 konaklama vergisi uygulanır.'),
    ]
    return dict(
        slug='kira-getirisi-hesaplama', url=url, cs=CS2,
        title='Kira Getirisi Nasıl Hesaplanır? Brüt ve Net Getiri (2026) | Aleyna Bozoklar',
        desc='Miami\'de kira getirisi hesaplama: brüt getiri, net getiri (cap rate) ve nakit getirisi formülleri, emlak vergisi tahmini, Amendment 3, yabancıların kira vergisi ve FIRPTA.',
        og='Kira getirisi nasıl hesaplanır? Brüt ve net getiri', headline='Kira getirisi nasıl hesaplanır? Miami\'de brüt getiri, net getiri ve nakit getirisi (2026)',
        crumb='Kira getirisi', tab='Kira getirisi',
        h1='Kira getirisi nasıl hesaplanır? <em>Brüt ve net getiri</em>',
        lead='İlandaki getiri ile elinize geçen getiri neden farklıdır? Brüt getiri, net getiri ve nakit getirisinin formülleri, Miami\'de giderlerin doğru tahmini, kira gelirinin vergileri ve satıştaki FIRPTA kesintisi; her kural resmi kaynağıyla.',
        date_iso='2026-11-23', date='23 Kasım 2026', stats=stats, sections=sections, faq=faq,
        sources=list(CS2.values()), cta=('/yatirim/', 'Net getirinizi hesaplayın'), css=[], note=NOTE_YIELD)


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
      <p class="wm-note">{E(g.get('note', NOTE))}</p>
    </div>
  </section>
</main>'''
    out = head + meta + body_start + main + footer
    d = os.path.join(ROOT, 'rehberler', g['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)




def main():
    tpl = open(os.path.join(ROOT, 'rehberler', 'index.html'), encoding='utf-8').read()
    guides = [build_str(), build_yield()]
    tabs = TABS + [('/rehberler/' + g['slug'] + '/', g['tab']) for g in guides]
    for g in guides:
        render(g, tpl, tabs)
        print('ok', g['slug'])
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'stamp_assets.py')], check=True)


if __name__ == '__main__':
    main()
