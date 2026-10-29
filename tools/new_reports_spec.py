# -*- coding: utf-8 -*-
"""Ayrılan ve yeni eklenen mahalle raporlarının elle yazılmış metinleri.

Rakam içeren alanlar (satış, kira, vergi, kısa özet, SSS fiyat/kira/vergi) refresh_numbers.py ile canlı verilerden üretilir.
Kullanım: python3 tools/new_reports_spec.py  → tools/reports/<id>.json dosyalarını yazar.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEMA = '<a href="https://msc.fema.gov/portal/search" target="_blank" rel="noopener">FEMA haritasından</a>'
HOA = ("Aidat binadan binaya ve siteden siteye çok değişir; tek bir mahalle ortalaması yanıltıcı olur. 2022 sonrası Florida yasaları gereği kondominyumlarda "
       "<strong>yapısal yedek akçe çalışması (SIRS)</strong> ve <strong>milestone denetimi</strong> zorunludur. Teklif vermeden önce bu raporları, bütçeyi ve planlanan özel aidatları (special assessment) mutlaka isteyin.")
SCHOOLS = {
    'Miami-Dade': '<a href="https://www.dadeschools.net/" target="_blank" rel="noopener">Miami-Dade County Public Schools</a>',
    'Broward': '<a href="https://www.browardschools.com/" target="_blank" rel="noopener">Broward County Public Schools</a>',
}
FDLE = '<a href="https://www.fdle.state.fl.us/FSAC/Data-Statistics/UCR-Offense-Data" target="_blank" rel="noopener">Florida Department of Law Enforcement (FDLE)</a>'
CBB_AUG = 'https://www.condoblackbook.com/blog/august-2026-miami-dade-luxury-preconstruction-condo-updates'
CBB_SEP = 'https://www.condoblackbook.com/blog/september-2026-miami-dade-luxury-preconstruction-condo-updates'
CBB_OCT = 'https://www.condoblackbook.com/blog/october-2026-miami-dade-luxury-preconstruction-condo-updates'
PDF = '/yeni-projeler/'
PDF_SRC = ['Cervera Real Estate: Development Market Study, Q3 2026 (Haziran 2026); proje listesi Yeni Projeler sayfasında', '/yeni-projeler/']
GENERIC_PJ = 'Bu raporda yalnızca kaynağı belirtilebilen kondominyum ve konut projeleri listelenir. Bölgedeki diğer yeni projeleri ve fiyat listelerini görüşmede birlikte değerlendirebiliriz.'


def flood(txt):
    return (txt + " Konut ve sel sigortası Güney Florida'da önemli bir yıllık kalemdir; teklif vermeden önce adres bazında teklif alın. "
            f"Sel bölgesini {FEMA} adresle kontrol edebilirsiniz.")


def schools(county):
    return (f"Okul bölgeleri ve okul bilgileri için {SCHOOLS[county]}, suç istatistikleri için {FDLE} resmi kaynaklarına başvurun. "
            "Okul atamaları adrese göre belirlenir ve değişebilir.")


S = []

S.append(dict(
    id='pinecrest', name='Pinecrest', county='Miami-Dade', lat=25.6651, lng=-80.3080,
    line='Geniş arsalar ve bahçeli müstakil evler.',
    lead='Geniş parseller, yoğun tropikal bitki örtüsü ve sakin sokaklarla bahçeli müstakil ev yaşamı.',
    character=[
        "Pinecrest, 1996'da belediye olarak kurulmuş, geniş parsellere oturan müstakil evlerden oluşan yeşil bir köy (Village of Pinecrest). Sokakların çoğunda ağaç gölgesi, bahçeler ve havuzlu evler hâkimdir; ticari alanlar ağırlıkla US-1 (South Dixie Highway) boyunca toplanır.",
        "İmar yapısı düşük yoğunluklu müstakil konutu esas alır; apartman ve kondominyum stoku çok sınırlıdır. Doğu kesimi Old Cutler Road boyunca Biscayne Körfezi'ne yaklaşır; bu bölgede büyük arsalar ve su kenarı evler bulunur.",
        "Kuzeyinde South Miami ve Coral Gables, batısında Kendall, güneyinde Palmetto Bay yer alır; Dadeland alışveriş bölgesi ve Metrorail istasyonları kısa sürüş mesafesindedir.",
    ],
    places=[
        ['Pinecrest Gardens', 'Eski Parrot Jungle arazisinde, dev banyan ağaçları ve göletleriyle belediye bahçesi; konser ve etkinlik alanı.'],
        ['Dadeland Mall', 'Kuzeybatıda, bölgenin en büyük alışveriş merkezlerinden biri; Metrorail ile bağlantılı.'],
        ['Old Cutler Road', 'Banyan ağaçlarıyla gölgelenen, bisiklet ve yürüyüş için tarihî yol.'],
        ['The Underline', 'Metrorail hattının altında, Dadeland\'dan Brickell\'e uzanan yürüyüş ve bisiklet yolu (bölümler hâlinde açılıyor).'],
        ['Gizli köşe: Pinecrest Farmers Market', 'Pazar sabahları Pinecrest Gardens\'ta kurulan üretici pazarı.'],
    ],
    flood=flood("Körfeze yakın doğu kesimleri yüksek riskli bölgelerdedir (AE); US-1'in batısındaki iç kesimlerde risk adres bazında değişir."),
    transport=[
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 20 km · 25 dakika'],
        ['Brickell', 'yaklaşık 18 km · 25 dakika'],
        ['Coral Gables (Miracle Mile)', 'yaklaşık 9 km · 15 dakika'],
        ['Toplu taşıma', 'Metrobus hatları; US-1 boyunca Metrorail Dadeland North ve Dadeland South istasyonları.'],
        ['Günlük hayat', 'Büyük ölçüde araca bağımlı; alışveriş ve hizmetler US-1 ve Dadeland çevresinde.'],
    ],
    projects=[], projects_notes=["Pinecrest'in imar yapısı düşük yoğunluklu müstakil konutu esas alır; bölgede büyük ölçekli kondominyum projesi takip etmiyoruz. Yeni inşa müstakil ev seçeneklerini görüşmede birlikte değerlendirebiliriz."],
    pros=['Geniş parseller, bahçe ve havuz imkânı', 'Yoğun ağaç dokusu ve sakin konut sokakları', 'Dadeland, Coral Gables ve Metrorail\'e yakınlık'],
    cons=['Giriş eşiği yüksek; müstakil ev ağırlıklı pahalı stok', 'Kiralık stok sınırlı', 'US-1 üzerinde yoğun trafik', 'Körfeze yakın kesimlerde sel sigortası maliyeti'],
    faq=[["Pinecrest ile South Miami arasındaki fark nedir?", "Pinecrest geniş parselli, sakin ve araç odaklı bir köydür. South Miami daha kompakt, yürünebilir bir merkeze (Sunset Drive) ve Metrorail istasyonuna sahiptir. İki şehrin güncel fiyatlarını ayrı raporlarda bulabilirsiniz."]],
    sources=[],
))

S.append(dict(
    id='south-miami', name='South Miami', county='Miami-Dade', lat=25.7076, lng=-80.2934,
    line='Sunset Drive çevresinde yürünebilir merkez ve Metrorail.',
    lead='Sunset Drive çevresindeki yürünebilir merkezi, Metrorail istasyonu ve ağaçlı konut sokaklarıyla Coral Gables\'ın güney komşusu.',
    character=[
        "South Miami, Coral Gables ile Pinecrest arasında, 1920'lerde belediye olan küçük bir şehir. Sunset Drive ve Red Road kesişimi çevresindeki şehir merkezi restoranlar, kafeler ve dükkânlarla yürünebilir bir yapıdadır.",
        "Konut stoku ağırlıkla müstakil evlerden oluşur; merkeze yakın kesimlerde townhouse ve kondominyumlar da bulunur. University of Miami'nin Coral Gables kampüsü şehrin hemen kuzeydoğusundadır.",
        "Metrorail South Miami istasyonu şehri Brickell ve Downtown'a raylı sistemle bağlar; US-1 boyunca uzanan The Underline yürüyüş ve bisiklet yolu da bu hattı izler.",
    ],
    places=[
        ['Sunset Drive', 'Restoran, kafe ve butiklerin sıralandığı yürünebilir şehir merkezi.'],
        ['The Shops at Sunset Place', 'Merkezdeki açık hava alışveriş ve eğlence alanı.'],
        ['University of Miami', 'Kuzeydoğuda, kampüs etkinlikleri ve Lowe Art Museum.'],
        ['Metrorail South Miami istasyonu', 'Brickell ve Downtown\'a doğrudan raylı bağlantı.'],
        ['Gizli köşe: Fuchs Park', 'Ağaçlar arasında küçük ve sakin bir mahalle parkı.'],
    ],
    flood=flood("İç kesimde yer alan şehirde risk adres bazında değişir; alçak kesimlerde sel bölgesini mutlaka kontrol edin."),
    transport=[
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 15 km · 20–25 dakika'],
        ['Brickell', 'yaklaşık 14 km · 20 dakika; Metrorail ile de ulaşılabilir'],
        ['Coral Gables (Miracle Mile)', 'yaklaşık 5 km · 10 dakika'],
        ['Toplu taşıma', 'Metrorail South Miami istasyonu ve Metrobus hatları.'],
        ['Günlük hayat', 'Şehir merkezi yürünebilir; konut sokaklarında araç gerekir.'],
    ],
    projects=[], projects_notes=[GENERIC_PJ],
    pros=['Yürünebilir şehir merkezi ve Metrorail istasyonu', 'University of Miami ve Coral Gables\'a yakınlık', 'Ağaçlı konut sokakları'],
    cons=['Kiralık stok sınırlı', 'US-1 ve Sunset Drive\'da yoğun trafik', 'Eski evlerde yenileme ve sigorta maliyeti'],
    faq=[["South Miami ile Pinecrest arasındaki fark nedir?", "South Miami daha kompakt ve yürünebilir bir merkeze ve Metrorail istasyonuna sahiptir. Pinecrest daha geniş parselli, sakin ve araç odaklı bir köydür."]],
    sources=[],
))

S.append(dict(
    id='wynwood', name='Wynwood', county='Miami-Dade', lat=25.8010, lng=-80.1990,
    line='Duvar resimleri, galeriler ve yeni kiralık binalar.',
    lead='Dev duvar resimleri, galeriler, restoranlar ve bira fabrikalarıyla Miami\'nin en hızlı dönüşen bölgesi.',
    character=[
        "Wynwood, Downtown Miami'nin kuzeyinde, eski depo ve tekstil atölyelerinin 2000'lerden itibaren sanat galerilerine, restoranlara, bira fabrikalarına ve ofislere dönüştüğü bir bölgedir. Duvarları dev muralların kapladığı sokaklar, bölgeyi Miami'nin en çok fotoğraflanan yerlerinden biri yaptı.",
        "Wynwood Walls açık hava sergisi bölgenin simgesidir; galeriler, tasarım ajansları ve atölye tipi mekânlar hâlâ yaygındır. Doğusunda Edgewater, kuzeyinde Midtown ve Design District yer alır.",
        "Konut stoku yeni orta yükseklikte kiralık binalar ile butik kondominyumlardan oluşur; imar değişiklikleri sonrası bölgede çok sayıda yeni proje yükseliyor.",
    ],
    places=[
        ['Wynwood Walls', 'Dünyanın dört bir yanından sokak sanatçılarının eserlerini sergileyen açık hava galerisi.'],
        ['NW 2nd Avenue', 'Galeriler, restoranlar ve dükkânlarla bölgenin ana aksı.'],
        ['Wynwood Marketplace ve bira fabrikaları', 'Hafta sonu canlı müzik ve yerel üreticiler.'],
        ['Rubell Museum', 'Batıda, Allapattah\'ta, Kuzey Amerika\'nın büyük özel çağdaş sanat koleksiyonlarından biri.'],
        ['Gizli köşe: Ayın ikinci cumartesisi Art Walk', 'Galerilerin akşam saatlerinde açık kaldığı sanat yürüyüşü.'],
    ],
    flood=flood("Kıyıdan içeride yer alan bölgede risk Edgewater ve Brickell'e göre genellikle daha düşüktür; ancak alçak sokaklarda yağış kaynaklı su birikmesi görülebilir ve risk adres bazında değişir."),
    transport=[
        ['Brickell', 'yaklaşık 6 km · 10–15 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 11 km · 15 dakika'],
        ['Miami Beach', 'yaklaşık 10 km · 15–20 dakika'],
        ['Toplu taşıma', 'Ücretsiz Miami Trolley hatları, Metrobus ve Citi Bike; Downtown\'daki MiamiCentral\'dan Brightline.'],
        ['Günlük hayat', 'Bölge kendi içinde yürünebilir; Downtown ve plajlara araç veya trolley gerekir.'],
    ],
    projects=[
        ['The Rider at Wynwood', 'Kaba inşaat tamamlandı (Eylül 2026)', '2027 ikinci yarı', CBB_OCT],
        ['Twenty Sixth & 2nd Wynwood Residences', 'Dikey inşaatın ilk aşaması', '2028 2. çeyrek', CBB_AUG],
        ['WOMA', 'Satışlar başladı; temel atma 2027', '2029 sonu', CBB_OCT],
        ['Frida Kahlo Wynwood Residences', '244 daire, 8 kat; ön satış', '2029', PDF],
    ],
    projects_notes=[],
    pros=['Sanat, gastronomi ve gece hayatının bir arada olduğu canlı çevre', 'Brickell, havalimanı ve Miami Beach\'e yakın merkezi konum', 'Yapım aşamasında çok sayıda yeni proje'],
    cons=['Gece hayatı ve etkinliklere bağlı gürültü', 'Yeni arzla birlikte kira ve satış rekabeti artabilir', 'Satış sayısı az; fiyat verisi oynak'],
    faq=[["Wynwood yatırım için uygun mu?", "Bölge hızla dönüşüyor ve kira talebi güçlü; ancak yeni arz, satış verisinin azlığı ve Miami şehri vergi oranı net getiriyi etkiler. Kararı net getiri hesabıyla vermek gerekir. Bu bilgi yatırım tavsiyesi değildir."]],
    sources=[['CondoBlackBook: Ağustos ve Ekim 2026 proje güncellemeleri', CBB_OCT], PDF_SRC],
))

S.append(dict(
    id='design-district', name='Design District', county='Miami-Dade', lat=25.8130, lng=-80.1930,
    line='Lüks markalar, tasarım ve çağdaş sanat.',
    lead='Lüks moda markaları, mimari açıdan dikkat çekici binalar ve ücretsiz müzeleriyle Miami\'nin tasarım ve alışveriş bölgesi.',
    character=[
        "Miami Design District, Wynwood ve Midtown'un kuzeyinde, NE 38th Street ile NE 42nd Street arasında yoğunlaşan bir bölgedir. Son on beş yılda lüks moda markalarının mağazaları, tasarım showroom'ları ve kamusal sanat eserleriyle uluslararası bir alışveriş adresine dönüştü.",
        "Bölge, Aralık ayındaki Art Basel Miami Beach haftasında Design Miami fuarı ve galeri etkinlikleriyle şehrin sanat takviminin merkezlerinden biridir. ICA Miami ve de la Cruz Collection gibi müzeler ücretsiz ziyaret edilebilir.",
        "Konut stoku sınırlıdır; bölgenin büyük kısmı ticari kullanımdadır. Konut seçenekleri çevredeki Buena Vista ve Little Haiti'nin müstakil ev sokakları ile yeni markalı projelerden oluşur.",
    ],
    places=[
        ['Palm Court', 'Lüks mağazalarla çevrili, Buckminster Fuller kubbesinin bulunduğu meydan.'],
        ['ICA Miami', 'Ücretsiz giriş sunan çağdaş sanat müzesi.'],
        ['de la Cruz Collection', 'Ücretsiz ziyaret edilebilen özel çağdaş sanat koleksiyonu.'],
        ['NE 40th Street', 'Mağazalar, restoranlar ve tasarım showroom\'ları.'],
        ['Gizli köşe: Buena Vista', 'Hemen kuzeyinde, 1920\'lerden kalma evleri ve sakin sokaklarıyla tarihî mahalle.'],
    ],
    flood=flood("Kıyıdan içeride yer alan bölgede risk Edgewater'a göre genellikle daha düşüktür; ancak risk adres bazında değişir."),
    transport=[
        ['Brickell', 'yaklaşık 7 km · 15 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 12 km · 15–20 dakika'],
        ['Miami Beach', 'yaklaşık 10 km · 15–20 dakika'],
        ['Toplu taşıma', 'Ücretsiz Miami Trolley hatları ve Metrobus; Downtown\'daki MiamiCentral\'dan Brightline.'],
        ['Günlük hayat', 'Bölge kendi içinde yürünebilir; çevre mahallelere araç gerekir.'],
    ],
    projects=[
        ['Kempinski Residences, Design District', 'Satış ofisi açık; temel atma Şubat 2027', '2029 4. çeyrek', CBB_AUG],
        ["Fouquet's Hotel & Residences", 'Ön satış', '2030', CBB_AUG],
    ],
    projects_notes=[],
    pros=['Lüks alışveriş, tasarım ve ücretsiz müzeler', 'Wynwood, Midtown ve Upper East Side\'a yürüme veya kısa sürüş mesafesi', 'Markalı yeni konut projeleri'],
    cons=['Konut stoku çok sınırlı; satış verisi yayımlanmıyor', 'Etkinlik dönemlerinde yoğunluk ve otopark sıkıntısı', 'Fiyatlar proje ve binaya göre çok değişir'],
    faq=[["Design District'te hangi projeler var?", "Kempinski Residences (2029 4. çeyrek) ve Fouquet's Hotel & Residences (2030) öne çıkan markalı projelerdir. Teslim tarihleri geliştirici açıklamalarına dayanır ve değişebilir."]],
    sources=[['CondoBlackBook: Ağustos 2026 Miami-Dade proje güncellemesi', CBB_AUG]],
))

S.append(dict(
    id='edgewater', name='Edgewater', county='Miami-Dade', lat=25.7990, lng=-80.1880,
    line='Biscayne Körfezi boyunca yükselen yeni nesil kuleler.',
    lead='Biscayne Körfezi boyunca yükselen yeni nesil kondominyum kuleleri ve körfez kıyısı parklarıyla Downtown\'un kuzey komşusu.',
    character=[
        "Edgewater, Downtown Miami'nin kuzeyinde, Biscayne Boulevard ile Biscayne Körfezi arasında uzanan bir mahalle. Son on yılda körfez kıyısında yükselen yüksek katlı kondominyumlar bölgenin silüetini ve karakterini değiştirdi.",
        "Batısında Wynwood ve Midtown, güneyinde Arsht Center ve Downtown yer alır. Margaret Pace Park çevresi körfez kıyısında yürüyüş ve spor için mahallenin buluşma noktasıdır; mahalle Downtown'a göre daha sakin ve konut ağırlıklıdır.",
        "Konut stoku neredeyse tamamen yüksek katlı dairelerden oluşur; teslim edilen ve inşa hâlindeki projelerle arz belirgin şekilde artıyor.",
    ],
    places=[
        ['Margaret Pace Park', 'Körfez kıyısında spor sahaları ve yürüyüş yolu.'],
        ['Adrienne Arsht Center', 'Güney ucunda opera, bale ve konser salonu.'],
        ['Biscayne Boulevard', 'Restoranlar ve günlük ihtiyaç için marketler.'],
        ['Wynwood ve Midtown', 'Batıda galeriler, restoranlar ve alışveriş.'],
        ['Gizli köşe: Körfez kıyısı gün batımı', 'Margaret Pace Park\'tan Venetian Adaları\'na bakan manzara.'],
    ],
    flood=flood("Körfez kıyısındaki kesimler yüksek riskli bölgelerdedir (AE). Yüksek katlı binalarda sel sigortası çoğunlukla binanın ortak poliçesindedir; dairenin iç kısmı için ayrıca poliçe gerekir."),
    transport=[
        ['Brickell', 'yaklaşık 5 km · 10–15 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 12 km · 15–20 dakika'],
        ['Fort Lauderdale Havalimanı (FLL)', 'yaklaşık 40 km · 35–40 dakika'],
        ['Toplu taşıma', 'Metrobus ve ücretsiz Miami Trolley hatları; güneyde Metromover (Omni) ve MiamiCentral (Brightline, Metrorail).'],
        ['Günlük hayat', 'Biscayne Boulevard çevresinde yürüme mesafesinde market ve restoranlar.'],
    ],
    projects=[
        ['Villa Miami', "İnşaat sürüyor; kaba inşaatın Ekim 2026'da tamamlanması bekleniyor", '2027 sonu', CBB_OCT],
        ['The Cove Residences', "İnşaat Mart 2026'da başladı", '2028', CBB_AUG],
        ['Edge House', 'İnşaat sürüyor', '2028 sonu', CBB_OCT],
        ['EDITION Residences Edgewater', 'Eylül 2026 uzlaşmasıyla yeniden yolunda; temel atma 2026 sonu', '2029', CBB_OCT],
        ['LILLI Miami Edgewater', 'Onaylı; temel atma 2026 sonu', '2029', CBB_AUG],
    ],
    projects_notes=[],
    pros=['Körfez manzaralı yeni nesil binalar', 'Wynwood, Design District ve Downtown\'a yakınlık', 'Körfez kıyısı parkı ve kültür merkezleri'],
    cons=['Yüksek yeni arz; kira ve yeniden satışta rekabet', 'Kıyı bölgesi sel riski ve sigorta maliyeti', 'Biscayne Boulevard\'da yoğun trafik'],
    faq=[["Edgewater'da hangi yeni projeler var?", "Villa Miami (2027 sonu), The Cove (2028), Edge House (2028 sonu), EDITION Residences ve LILLI (2029) başlıca projelerdir. Teslim tarihleri değişebilir."]],
    sources=[['CondoBlackBook: Ağustos ve Ekim 2026 proje güncellemeleri', CBB_OCT]],
))

S.append(dict(
    id='downtown-miami', name='Downtown Miami', county='Miami-Dade', lat=25.7743, lng=-80.1937,
    line='Müzeler, Kaseya Center ve MiamiCentral istasyonu.',
    lead='Müzeleri, körfez kıyısı parkları, Kaseya Center ve MiamiCentral istasyonuyla şehrin idari ve kültürel merkezi.',
    character=[
        "Downtown Miami, Brickell'in kuzeyinde, Miami Nehri ile Arsht Center arasında uzanan şehir merkezidir. Belediye ve ilçe binaları, adliyeler ve şirket merkezleri burada toplanır; Biscayne Boulevard boyunca Bayfront Park, Pérez Art Museum Miami (PAMM), Frost Bilim Müzesi ve Kaseya Center yan yana dizilir.",
        "MiamiCentral istasyonu Brightline ile Fort Lauderdale, West Palm Beach ve Orlando'ya, Tri-Rail ile banliyölere bağlantı sağlar; ücretsiz Metromover şehir merkezini Brickell ve Omni'ye bağlar. Miami Worldcenter bölgenin en büyük karma kullanımlı projesidir.",
        "Konut stoku büyük ölçüde yüksek katlı kondominyumlardan oluşur; çok sayıda yeni markalı proje inşaat veya ön satış aşamasındadır.",
    ],
    places=[
        ['Pérez Art Museum Miami (PAMM)', 'Körfez kıyısında, asma bahçeli çağdaş sanat müzesi.'],
        ['Frost Science Museum', 'Akvaryumu ve planetaryumuyla bilim müzesi.'],
        ['Bayfront Park', 'Konserler ve etkinlikler için körfez kıyısı park.'],
        ['Kaseya Center', 'Miami Heat maçları ve konserler.'],
        ['Gizli köşe: Miami Riverwalk', 'Nehir ağzı boyunca, teknelerin geçişini izleyebileceğiniz yürüyüş yolu.'],
    ],
    flood=flood("Körfez ve nehir kıyısındaki kesimler yüksek riskli bölgelerdedir (AE/VE). Yüksek katlı binalarda sel sigortası çoğunlukla binanın ortak poliçesindedir; dairenin iç kısmı için ayrıca poliçe gerekir."),
    transport=[
        ['Brickell', 'yaklaşık 2 km · 5–10 dakika; Metromover ile de ulaşılabilir'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 12 km · 15–20 dakika'],
        ['Fort Lauderdale Havalimanı (FLL)', 'yaklaşık 45 km · 35–45 dakika; Brightline ile Fort Lauderdale istasyonuna yaklaşık 30 dakika'],
        ['Toplu taşıma', 'Ücretsiz Metromover, Metrorail, Tri-Rail ve Brightline (MiamiCentral), Metrobus.'],
        ['Günlük hayat', 'Araçsız yaşanabilir; market, restoran ve hizmetler yürüme mesafesinde.'],
    ],
    projects=[
        ['Waldorf Astoria Residences Miami', 'İnşaat sürüyor', '2028 2. çeyrek', CBB_SEP],
    ],
    projects_notes=["Cervera Real Estate'in Q3 2026 pazar raporu Downtown Miami'de 15 yeni projeyi takip ediyor; tamamını kat, teslim tarihi ve ödeme planıyla Yeni Projeler sayfamızda görebilirsiniz."],
    pros=['Metromover, Metrorail, Tri-Rail ve Brightline ile en güçlü toplu taşıma', 'Müzeler, parklar ve körfez manzarası', 'Araçsız yaşanabilir yoğun şehir merkezi'],
    cons=['Yüksek yeni arz; kira ve yeniden satışta rekabet', 'Kıyı bölgesi sel riski ve sigorta maliyeti', 'Etkinlik günlerinde yoğunluk ve gürültü'],
    faq=[],
    sources=[['CondoBlackBook: Eylül 2026 Miami-Dade proje güncellemesi', CBB_SEP], PDF_SRC],
))

S.append(dict(
    id='north-beach', name='North Beach', county='Miami-Dade', lat=25.8640, lng=-80.1215,
    line='Miami Beach\'in daha sakin ve mahalle dokusundaki kuzeyi.',
    lead='Okyanus kıyısı parkları, MiMo mimarisi ve Normandy Isles\'ıyla Miami Beach\'in daha sakin ve mahalle dokusundaki kuzey ucu.',
    character=[
        "North Beach, Miami Beach şehrinin en kuzey kesimidir; güneyde yaklaşık 63. cadde ve Indian Creek Drive'dan kuzeyde 87th Terrace'a kadar uzanır. Normandy Isles, Biscayne Point ve North Shore gibi mahalleleri kapsar.",
        "1950–60'lardan kalma MiMo (Miami Modern) tarzı alçak binalar ve North Shore Open Space Park gibi okyanus kıyısı parklar bölgenin karakterini belirler. Collins Avenue boyunca okyanusa doğrudan çıkışı olan kuleler ve oteller, batıda ise kanallara açılan müstakil evler bulunur.",
        "South Beach'e göre turist yoğunluğu daha azdır; son yıllarda Ocean Terrace ve 72nd Street çevresindeki yeni projelerle bölge yenileniyor.",
    ],
    places=[
        ['North Beach Oceanside Park', 'Okyanus kıyısında geniş yeşil alan ve yürüyüş yolları.'],
        ['North Beach Bandshell', 'Okyanus kıyısında açık hava konser alanı; düzenli ücretsiz etkinlikler.'],
        ['Normandy Isles', 'Fransız esintili sokak adlarıyla ada mahallesi ve çeşmeli meydanı.'],
        ['Miami Beach Beachwalk', 'Okyanus boyunca güneye uzanan yürüyüş ve bisiklet yolu.'],
        ['Gizli köşe: Ocean Terrace', 'Okyanusa bakan tarihî MiMo cepheli kısa cadde.'],
    ],
    flood=flood("Bariyer adası üzerindeki bölgenin büyük kısmı yüksek riskli kıyı bölgelerindedir (AE/VE)."),
    transport=[
        ['Brickell / Downtown', 'yaklaşık 17 km · 25 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 22 km · 25–30 dakika'],
        ['Fort Lauderdale Havalimanı (FLL)', 'yaklaşık 35 km · 35 dakika'],
        ['Toplu taşıma', 'Ücretsiz Miami Beach Trolley hatları ve Metrobus.'],
        ['Günlük hayat', 'Collins ve Harding caddeleri çevresi yürünebilir; ana karaya araçla 15–25 dakika.'],
    ],
    projects=[
        ['7200 Collins', 'İnşaat sürüyor; inşaat kredisi sağlandı', '2027 sonu', CBB_AUG],
        ['72 Carlyle', '134 daire, 20 kat; ön satış', '2028 4. çeyrek', PDF],
        ['Ocean Terrace', '52 daire, 20 kat; ön satış', '2029', PDF],
        ['NoBe Parc', '222 daire, 14 kat; ön lansman', '2029 1. çeyrek', PDF],
        ['Kolter / BH Group kulesi', '17 katlı kule önerisi; izleme listesinde', 'Açıklanmadı', CBB_AUG],
    ],
    projects_notes=[],
    pros=['South Beach\'e göre daha sakin okyanus yaşamı', 'Geniş kumsallar ve okyanus kıyısı parkları', 'Yeni projelerle yenilenen stok'],
    cons=['Kıyı bölgesi sel riski ve sigorta maliyeti', 'Eski binalarda SIRS ve milestone kaynaklı özel aidat riski', 'Miami Beach\'te sıkı kısa süreli kiralama kuralları', 'Ana karaya ulaşımda köprü trafiği'],
    faq=[["North Beach ile Mid-Beach farkı nedir?", "Mid-Beach büyük oteller, Indian Creek kıyısındaki konutlar ve okyanus cepheli kulelerle daha lüks bir segmentte; North Beach daha mahalle dokusunda ve yeni projelerle dönüşüyor. İki bölgenin güncel fiyatlarını ayrı raporlarda bulabilirsiniz."]],
    sources=[['CondoBlackBook: Ağustos 2026 Miami-Dade proje güncellemesi', CBB_AUG], PDF_SRC],
))

S.append(dict(
    id='mid-beach', name='Mid-Beach', county='Miami-Dade', lat=25.8250, lng=-80.1225,
    line='Tarihî oteller ve Indian Creek kıyısı.',
    lead='Fontainebleau ve Eden Roc gibi tarihî otelleri, Indian Creek kıyısındaki konutları ve okyanus cepheli kuleleriyle Miami Beach\'in orta kesimi.',
    character=[
        "Mid-Beach, Miami Beach şehrinin orta kesimidir; güneyde 23. cadde ve Indian Creek'ten kuzeyde yaklaşık 63. caddeye kadar uzanır. Oceanfront, Bayshore ve Nautilus gibi mahalleleri kapsar.",
        "Collins Avenue boyunca Fontainebleau ve Eden Roc gibi 1950'lerin simge otelleri ile okyanus cepheli kondominyumlar dizilir. Indian Creek kanalının batısında ise Nautilus ve La Gorce çevresinde geniş arsalı müstakil evler ve Miami Beach Golf Club bulunur.",
        "South Beach'e göre daha sakin, North Beach'e göre daha lüks bir segmenttedir; Miami Beach Beachwalk yolu bölgeyi güneye bağlar.",
    ],
    places=[
        ['Fontainebleau Miami Beach', '1954 yapımı simge otel; restoranları ve gece hayatıyla.'],
        ['Indian Creek kanalı', 'Collins Avenue boyunca palmiyeli kanal kıyısı.'],
        ['Miami Beach Golf Club', 'Bayshore bölgesinde şehrin golf sahası.'],
        ['Miami Beach Beachwalk', 'Okyanus boyunca kilometrelerce uzanan yürüyüş ve bisiklet yolu.'],
        ['Gizli köşe: Pinetree Park', 'Indian Creek kıyısında sakin, gölgeli mahalle parkı.'],
    ],
    flood=flood("Bariyer adası üzerindeki bölgenin büyük kısmı yüksek riskli kıyı bölgelerindedir (AE/VE)."),
    transport=[
        ['Brickell / Downtown', 'yaklaşık 13 km · 20 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 20 km · 25 dakika'],
        ['Fort Lauderdale Havalimanı (FLL)', 'yaklaşık 40 km · 40 dakika'],
        ['Toplu taşıma', 'Ücretsiz Miami Beach Trolley hatları ve Metrobus.'],
        ['Günlük hayat', 'Collins Avenue çevresi yürünebilir; ana karaya Julia Tuttle veya 79th Street Causeway ile.'],
    ],
    projects=[
        ['The Perigon Miami Beach', '82 daire, 15 kat; inşaat sürüyor', '2027 2. çeyrek', PDF],
    ],
    projects_notes=[],
    pros=['Okyanus cepheli yaşam ve tarihî oteller', 'Indian Creek ve golf sahası çevresinde müstakil ev seçenekleri', 'South Beach\'e göre daha sakin'],
    cons=['Kıyı bölgesi sel riski ve sigorta maliyeti', 'Eski binalarda SIRS ve milestone kaynaklı özel aidat riski', 'Miami Beach\'te sıkı kısa süreli kiralama kuralları'],
    faq=[["Mid-Beach ile North Beach farkı nedir?", "Mid-Beach büyük oteller, Indian Creek kıyısındaki konutlar ve okyanus cepheli kulelerle daha lüks bir segmentte; North Beach daha mahalle dokusunda ve yeni projelerle dönüşüyor."]],
    sources=[PDF_SRC],
))

S.append(dict(
    id='bal-harbour', name='Bal Harbour', county='Miami-Dade', lat=25.8915, lng=-80.1270,
    line='Okyanus cepheli kuleler ve Bal Harbour Shops.',
    lead='Okyanus cepheli lüks kondominyumları ve dünyaca bilinen Bal Harbour Shops ile Miami Beach adasının kuzey ucundaki küçük belediye.',
    character=[
        "Bal Harbour, Miami Beach adasının kuzey ucunda, Haulover Inlet'in hemen güneyinde yer alan küçük bir köy (Village of Bal Harbour). Okyanus boyunca uzanan lüks kondominyumlar ve oteller ile Collins Avenue'nun batısındaki kapılı müstakil ev bölgesinden oluşur.",
        "Bal Harbour Shops açık hava lüks alışveriş merkezi köyün simgesidir. Okyanus boyunca uzanan yürüyüş yolu ve yürünebilir ölçeği köyün sakin karakterini tamamlar; batısında Bay Harbor Islands, güneyinde Surfside yer alır.",
    ],
    places=[
        ['Bal Harbour Shops', 'Açık hava lüks alışveriş merkezi.'],
        ['Bal Harbour Beach Path', 'Okyanus boyunca uzanan yürüyüş ve koşu yolu.'],
        ['Haulover Park', 'Hemen kuzeyde, geniş kumsalı ve marinasıyla büyük park.'],
        ['Bay Harbor Islands', 'Batıda, Kane Concourse\'taki restoranlar ve kafeler.'],
        ['Gizli köşe: Haulover Sandbar', 'Haulover Inlet içinde, hafta sonları teknelerin demirlediği sığ kum adası.'],
    ],
    flood=flood("Bariyer adası üzerindeki köyün tamamına yakını yüksek riskli kıyı bölgelerindedir (AE/VE)."),
    transport=[
        ['Fort Lauderdale Havalimanı (FLL)', 'yaklaşık 30 km · 30 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 25 km · 30 dakika'],
        ['Brickell', 'yaklaşık 22 km · 30 dakika'],
        ['Toplu taşıma', 'Köy shuttle servisi ve Metrobus; ada dışı ulaşım için araç gerekir.'],
        ['Günlük hayat', 'Collins Avenue ve Bal Harbour Shops çevresi yürünebilir.'],
    ],
    projects=[['Rivage Bal Harbour', 'Satışlar sürüyor', '2027 sonu', CBB_AUG]],
    projects_notes=[],
    pros=['Okyanus cepheli sakin yaşam ve lüks alışveriş', 'Haulover, Aventura ve FLL havalimanına yakınlık', 'Yürünebilir küçük köy ölçeği'],
    cons=['Kıyı bölgesi sel riski ve yüksek sigorta maliyeti', 'Eski binalarda SIRS ve milestone kaynaklı özel aidat riski', 'Küçük piyasa: fiyat verisi oynak'],
    faq=[],
    sources=[['CondoBlackBook: Ağustos 2026 Miami-Dade proje güncellemesi', CBB_AUG]],
))

S.append(dict(
    id='surfside', name='Surfside', county='Miami-Dade', lat=25.8784, lng=-80.1256,
    line='Harding Avenue çevresinde küçük kasaba merkezi.',
    lead='Harding Avenue çevresindeki küçük merkezi, okyanus cepheli butik projeleri ve müstakil ev sokaklarıyla Bal Harbour\'un güney komşusu.',
    character=[
        "Surfside, Miami Beach ile Bal Harbour arasında, okyanus kıyısında yer alan küçük bir kasaba. Harding Avenue çevresindeki kafeler, restoranlar ve dükkânlar kasabaya mahalle ölçeğinde bir merkez kazandırır.",
        "Okyanus cephesinde butik kondominyumlar ve oteller, Collins ve Harding caddelerinin batısında ise müstakil ev sokakları bulunur. Kasabanın yeni toplum merkezi ve yüzme tesisi okyanus kıyısındadır.",
        "2021'deki Champlain Towers South çöküşü sonrası Florida'da kondominyum denetim ve yedek akçe yasaları sıkılaştırıldı; kasabada yeni projeler ve kapsamlı bina yenilemeleri bu dönemin ardından hızlandı.",
    ],
    places=[
        ['Harding Avenue', 'Kafe ve restoranlarla küçük kasaba merkezi.'],
        ['Surfside Community Center', 'Okyanus kıyısında yüzme havuzu ve etkinlik alanı.'],
        ['Bal Harbour Shops', 'Kuzeyde, birkaç dakika mesafede lüks alışveriş.'],
        ['Okyanus kıyısı yürüyüş yolu', 'Kumsala paralel sakin rota.'],
        ['Gizli köşe: 96th Street Park', 'Kasabanın batısında tenis kortları ve oyun alanlarıyla mahalle parkı.'],
    ],
    flood=flood("Bariyer adası üzerindeki kasabanın tamamına yakını yüksek riskli kıyı bölgelerindedir (AE/VE)."),
    transport=[
        ['Fort Lauderdale Havalimanı (FLL)', 'yaklaşık 30 km · 30 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 23 km · 30 dakika'],
        ['Brickell', 'yaklaşık 20 km · 30 dakika'],
        ['Toplu taşıma', 'Kasaba shuttle servisi ve Metrobus; ada dışı ulaşım için araç gerekir.'],
        ['Günlük hayat', 'Harding Avenue çevresi yürünebilir; plaj birkaç blok mesafede.'],
    ],
    projects=[
        ['Surf Row Residences', 'İnşaat sürüyor; %50 ön satış', '2027', CBB_SEP],
        ['Ocean House Surfside', '25 daire, 12 kat; inşaat sürüyor', '2027 3. çeyrek', PDF],
        ['The Delmore', '37 daire, 12 kat; ön satış', '2029 3. çeyrek', PDF],
        ['Seaway The Surf Club', '34 daire, 11 kat; teslim edildi', '2026 1. çeyrek', PDF],
    ],
    projects_notes=[],
    pros=['Yürünebilir kasaba merkezi ve okyanusa yakınlık', 'Butik ölçekli yeni okyanus cepheli projeler', 'Bal Harbour ve Miami Beach\'e kısa mesafe'],
    cons=['Kıyı bölgesi sel riski ve yüksek sigorta maliyeti', 'Eski binalarda SIRS ve milestone kaynaklı özel aidat riski', 'Küçük piyasa: fiyat verisi oynak'],
    faq=[["Surfside'da bina güvenliğini nasıl kontrol ederim?", "Florida yasası kondominyumlarda milestone denetimi ve yapısal yedek akçe çalışması (SIRS) şartı getiriyor. Teklif öncesinde bu raporları, bina bütçesini ve planlanan özel aidatları yazılı olarak isteyin."]],
    sources=[['CondoBlackBook: Eylül 2026 Miami-Dade proje güncellemesi', CBB_SEP], PDF_SRC],
))

S.append(dict(
    id='pompano', name='Pompano Beach', county='Broward', lat=26.2379, lng=-80.1248,
    line='Yenilenen sahil şeridi, iskele ve markalı yeni kuleler.',
    lead='Yenilenen sahil şeridi, okyanusa uzanan balıkçı iskelesi ve markalı yeni kuleleriyle dönüşen bir kıyı şehri.',
    character=[
        "Pompano Beach, Fort Lauderdale ile Deerfield Beach arasında, okyanustan Florida Turnpike'a uzanan geniş bir şehir. Yenilenen sahil şeridi, okyanusa uzanan balıkçı iskelesi, amfitiyatro ve kültür merkeziyle dönüşüm geçiriyor.",
        "Sahil boyunca markalı yeni kuleler yükselirken Intracoastal'ın batısında kanal kenarı evler, iç kesimlerde ise daha uygun fiyatlı müstakil ev ve kondominyum seçenekleri bulunur. Kuzeydoğusunda Lighthouse Point ve Hillsboro Inlet yer alır.",
    ],
    places=[
        ['Pompano Beach Fishing Pier', 'Okyanusa uzanan iskele ve çevresindeki restoranlar.'],
        ['Pompano Beach Boardwalk', 'Yenilenen sahil yürüyüş yolu ve parkı.'],
        ['Pompano Beach Amphitheater', 'Açık hava konser alanı.'],
        ['Hillsboro Inlet', 'Kuzeyde, teknelerin okyanusa açıldığı geçit.'],
        ['Gizli köşe: Pompano Beach Cultural Center', 'Konserler, sergiler ve kütüphane bir arada.'],
    ],
    flood=flood("Kanal kenarı ve sahil kesimleri yüksek riskli bölgelerdedir (AE/VE). Kanal kenarı evlerde deniz duvarı (seawall) ve iskele durumunu ekspertize dahil edin."),
    transport=[
        ['Fort Lauderdale Havalimanı (FLL)', 'yaklaşık 20 km · 20 dakika'],
        ['Boca Raton', 'yaklaşık 15 km · 15–20 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 60 km · 50 dakika'],
        ['Toplu taşıma', 'Tri-Rail Pompano Beach istasyonu ve Broward County Transit; Brightline için Fort Lauderdale veya Boca Raton istasyonu.'],
        ['Günlük hayat', 'Sahil şeridi yürünebilir; diğer bölgelerde araç gerekir.'],
    ],
    projects=[['Waldorf Astoria Residences Pompano Beach', "92 daire, 28 kat; kaba inşaat tamamlandı, %85'in üzerinde satış", '2027 yazı', 'https://floridayimby.com/?p=39690']],
    projects_notes=[],
    pros=['Yenilenen sahil şeridi ve yeni markalı projeler', 'Miami\'ye göre daha uygun giriş fiyatları', 'Tri-Rail ve I-95 bağlantısı'],
    cons=['Kanal kenarı evlerde deniz duvarı ve sigorta maliyeti', 'Eski kondominyumlarda özel aidat riski', 'Miami\'ye uzak (yaklaşık 50 dakika)'],
    faq=[],
    sources=[['Florida YIMBY: Waldorf Astoria Residences Pompano Beach (Mayıs 2026)', 'https://floridayimby.com/?p=39690']],
))

S.append(dict(
    id='lighthouse-point', name='Lighthouse Point', county='Broward', lat=26.2756, lng=-80.0873,
    line='Derin su kanalları ve tekne sahipleri için evler.',
    lead='Intracoastal\'a açılan derin su kanalları ve özel iskeleli evleriyle tekne sahiplerinin tercih ettiği küçük bir şehir.',
    character=[
        "Lighthouse Point, Pompano Beach ile Deerfield Beach arasında, Intracoastal Waterway'in batı kıyısında yer alan küçük bir şehir. Adını Hillsboro Inlet'teki tarihî deniz fenerinden alır.",
        "Konut stoku ağırlıkla kanallara cepheli müstakil evlerden oluşur; evlerin önemli bir kısmında özel iskele bulunur ve Hillsboro Inlet üzerinden okyanusa çıkış birkaç dakikadır. Federal Highway boyunca restoranlar ve dükkânlar sıralanır.",
    ],
    places=[
        ['Hillsboro Inlet', 'Teknelerin okyanusa açıldığı geçit; balıkçı tekneleri ve yat kulüpleri.'],
        ['Dan Witt Park', 'Şehrin tenis ve spor tesisleri.'],
        ['Pompano Beach Fishing Pier', 'Güneyde okyanusa uzanan iskele.'],
        ['Deerfield Beach', 'Kuzeyde plaj ve yürüyüş yolu.'],
        ['Gizli köşe: Hillsboro Inlet Lighthouse', '1907 tarihli deniz feneri; koruma derneğinin düzenlediği turlarla ziyaret edilebilir.'],
    ],
    flood=flood("Kanal kenarındaki evlerin büyük kısmı yüksek riskli bölgelerdedir (AE). Deniz duvarı (seawall), iskele ve köprü yüksekliği kısıtlarını ekspertize dahil edin."),
    transport=[
        ['Fort Lauderdale Havalimanı (FLL)', 'yaklaşık 25 km · 25 dakika'],
        ['Boca Raton', 'yaklaşık 12 km · 15 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 65 km · 55 dakika'],
        ['Toplu taşıma', 'Broward County Transit otobüs hatları; Tri-Rail Pompano Beach ve Deerfield Beach istasyonları.'],
        ['Günlük hayat', 'Günlük ihtiyaçlar Federal Highway boyunca; araç gerekir.'],
    ],
    projects=[], projects_notes=[GENERIC_PJ],
    pros=['Derin su kanalları ve okyanusa hızlı çıkış', 'Özel iskeleli müstakil evler', 'Sakin ve konut ağırlıklı şehir'],
    cons=['Kanal kenarı evlerde deniz duvarı ve sigorta maliyeti', 'Kiralık stok sınırlı', 'Miami\'ye uzak (yaklaşık 1 saat)'],
    faq=[["Lighthouse Point tekne sahipleri için neden tercih ediliyor?", "Şehrin kanalları derin sudur ve Hillsboro Inlet üzerinden okyanusa çıkış kısa sürer; evlerin önemli bir kısmında özel iskele bulunur. Satın almadan önce iskele, deniz duvarı ve köprü yüksekliği kısıtlarını kontrol edin."]],
    sources=[],
))

S.append(dict(
    id='allapattah', name='Allapattah', county='Miami-Dade', lat=25.8150, lng=-80.2240,
    line='Rubell Museum, Jackson ve Metrorail istasyonları.',
    lead='Rubell Museum, Jackson Memorial Hastanesi\'ne komşu sağlık bölgesi ve üç Metrorail istasyonuyla Wynwood\'un batı komşusu.',
    character=[
        "Allapattah, Miami şehri sınırları içinde, Wynwood'un batısında ve Miami Nehri'nin kuzeyinde yer alan bir mahalle. Güney ucunda Jackson Memorial Hastanesi ve UHealth tesislerinin bulunduğu sağlık bölgesi (Health District) yer alır.",
        "Rubell Museum, Kuzey Amerika'nın büyük özel çağdaş sanat koleksiyonlarından birini eski bir sanayi binasında sergiler; çevresindeki depolar galerilere ve atölyelere dönüşüyor. NW 17th Avenue çevresi Dominik ve Latin Amerika esintili dükkân ve restoranlarıyla bilinir.",
        "Konut stoku tek katlı müstakil evler, dubleksler ve küçük apartmanlardan oluşur; Metrorail istasyonlarının çevresinde yeni kiralık bina projeleri artıyor.",
    ],
    places=[
        ['Rubell Museum', 'Eski bir sanayi binasında çağdaş sanat koleksiyonu.'],
        ['Jackson Memorial Hastanesi', 'Güneyde, bölgenin büyük hastane ve tıp merkezi.'],
        ['NW 17th Avenue', 'Restoranlar, pazarlar ve dükkânlarla mahallenin ticari aksı.'],
        ['Wynwood', 'Doğuda galeriler, restoranlar ve gece hayatı.'],
        ['Gizli köşe: Allapattah\'ın meyve ve sebze pazarları', 'NW 20th Street çevresinde toptan ve perakende pazarlar.'],
    ],
    flood=flood("Miami Nehri ve kanallara yakın güney kesimlerde risk daha yüksektir; iç kesimlerde risk adres bazında değişir."),
    transport=[
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 6 km · 10–15 dakika'],
        ['Brickell', 'yaklaşık 7 km · 15 dakika'],
        ['Downtown Miami', 'yaklaşık 5 km · 10 dakika'],
        ['Toplu taşıma', 'Metrorail Allapattah, Santa Clara ve UHealth–Jackson istasyonları; Metrobus hatları.'],
        ['Günlük hayat', 'Ana caddeler çevresinde market ve hizmetler; Metrorail ile şehir merkezine araçsız ulaşım.'],
    ],
    projects=[], projects_notes=[GENERIC_PJ],
    pros=['Üç Metrorail istasyonu ve şehir merkezine yakınlık', 'Havalimanına ve sağlık bölgesine kısa mesafe', 'Wynwood\'a göre daha uygun giriş fiyatları'],
    cons=['Eski evlerde yenileme ve sigorta maliyeti', 'Mahalleden mahalleye belirgin fark', 'Ana caddelerde trafik'],
    faq=[],
    sources=[],
))

S.append(dict(
    id='little-haiti', name='Little Haiti', county='Miami-Dade', lat=25.8300, lng=-80.1960,
    line='Karayip kültürü, galeriler ve Little Haiti Cultural Complex.',
    lead='Little Haiti Cultural Complex, renkli duvar resimleri ve bağımsız galerileriyle Design District\'in kuzey komşusu.',
    character=[
        "Little Haiti, Miami şehri sınırları içinde, Design District'in kuzeyinde, yaklaşık NE 54th Street ile NE 79th Street arasında uzanan bir mahalle. Haiti ve Karayip kültürünün izlerini taşıyan restoranlar, pazarlar ve duvar resimleri mahallenin karakterini oluşturur.",
        "Little Haiti Cultural Complex Afro-Karayip sanatı, dans ve tiyatro etkinliklerine ev sahipliği yapar; yanındaki Caribbean Marketplace yerel ürünlerin satıldığı kapalı pazardır. Son yıllarda küçük bağımsız galeriler, plak dükkânları ve müzik mekânları bölgeye ilgi çekiyor.",
        "Konut stoku ağırlıkla tek katlı müstakil evler, dubleksler ve küçük apartmanlardan oluşur; Design District ve Upper East Side'a yakınlık bölgeyi dönüşüm baskısı altına sokuyor.",
    ],
    places=[
        ['Little Haiti Cultural Complex', 'Sanat galerisi, tiyatro ve etkinlik alanı.'],
        ['Caribbean Marketplace', 'Yerel el sanatları ve ürünlerin satıldığı kapalı pazar.'],
        ['NE 2nd Avenue', 'Restoranlar, dükkânlar ve duvar resimleriyle ana cadde.'],
        ['Design District', 'Güneyde lüks alışveriş ve müzeler.'],
        ['Gizli köşe: Sounds of Little Haiti', 'Kültür merkezinde düzenlenen ücretsiz müzik etkinlikleri.'],
    ],
    flood=flood("Little River kıyısına yakın kesimlerde risk daha yüksektir; iç kesimlerde risk adres bazında değişir."),
    transport=[
        ['Brickell', 'yaklaşık 9 km · 15–20 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 12 km · 20 dakika'],
        ['Design District', 'yaklaşık 2 km · 5 dakika'],
        ['Toplu taşıma', 'Metrobus ve ücretsiz Miami Trolley hatları.'],
        ['Günlük hayat', 'Ana caddeler çevresinde market ve hizmetler; günlük hayat için çoğunlukla araç gerekir.'],
    ],
    projects=[], projects_notes=[GENERIC_PJ],
    pros=['Güçlü kültürel kimlik ve sanat sahnesi', 'Design District ve Upper East Side\'a yakınlık', 'Çevresine göre daha uygun giriş fiyatları'],
    cons=['Eski evlerde yenileme ve sigorta maliyeti', 'Satış sayısı az; fiyat verisi oynak', 'Mahalleden mahalleye belirgin fark'],
    faq=[],
    sources=[],
))

S.append(dict(
    id='midtown', name='Midtown', county='Miami-Dade', lat=25.8075, lng=-80.1930,
    line='Yürünebilir alışveriş ve kondominyum blokları.',
    lead='Yürünebilir alışveriş caddeleri ve yeni nesil kondominyumlarıyla Wynwood ile Design District arasındaki planlı bölge.',
    character=[
        "Midtown Miami, Wynwood ile Design District arasında, eski Florida East Coast demiryolu depo alanında 2000'lerde planlanan karma kullanımlı bir bölge. Mağazalar, restoranlar ve market zincirleri yürünebilir sokaklar boyunca kondominyum bloklarının zemin katlarında yer alır.",
        "Konut stoku modern kondominyumlar ve çok katlı townhouse'lardan oluşur; bölgenin kenarlarında eklektik tarzda tarihî müstakil evler de bulunur. Doğusunda Edgewater ve körfez, batısında Wynwood'un galerileri yer alır.",
    ],
    places=[
        ['The Shops at Midtown Miami', 'Market, mağaza ve restoranlarla bölgenin alışveriş alanı.'],
        ['Midtown Boulevard', 'Kafe ve restoranlarla yürünebilir ana cadde.'],
        ['Wynwood', 'Batıda galeriler ve sokak sanatı.'],
        ['Design District', 'Kuzeyde lüks alışveriş ve müzeler.'],
        ['Gizli köşe: Buena Vista Avenue', 'Bölgenin kuzeyinde tarihî evlerle sakin bir yürüyüş rotası.'],
    ],
    flood=flood("Kıyıdan içeride yer alan bölgede risk Edgewater'a göre genellikle daha düşüktür; ancak risk adres bazında değişir."),
    transport=[
        ['Brickell', 'yaklaşık 6 km · 10–15 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 11 km · 15 dakika'],
        ['Miami Beach', 'yaklaşık 10 km · 15–20 dakika'],
        ['Toplu taşıma', 'Ücretsiz Miami Trolley hatları ve Metrobus; Downtown\'daki MiamiCentral\'dan Brightline.'],
        ['Günlük hayat', 'Market, restoran ve hizmetler yürüme mesafesinde.'],
    ],
    projects=[['Midtown Park', '288 daire, 27 kat; ön satış', '2028', PDF]],
    projects_notes=[],
    pros=['Yürünebilir alışveriş ve günlük hizmetler', 'Wynwood, Design District ve Edgewater\'a yakınlık', 'Görece yeni kondominyum stoku'],
    cons=['Yeni arzla birlikte kira ve satış rekabeti', 'Eski binalarda SIRS ve özel aidat riski', 'Yoğun trafik ve otopark sıkıntısı'],
    faq=[],
    sources=[PDF_SRC],
))

S.append(dict(
    id='morningside', name='Morningside', county='Miami-Dade', lat=25.8290, lng=-80.1830,
    line='Körfez kıyısında tarihî Akdeniz tarzı evler.',
    lead='Körfez kıyısındaki Akdeniz tarzı tarihî evleri ve ağaçlı sokaklarıyla Upper East Side\'ın en bilinen mahallesi.',
    character=[
        "Morningside, Miami şehri sınırları içinde, Upper East Side bölgesinde, Biscayne Boulevard ile Biscayne Körfezi arasında yer alan tarihî bir konut mahallesi. Mahalle, 1920'lerden kalma Akdeniz Canlanması (Mediterranean Revival) evleri ve korunan sokak dokusuyla tarihî bölge statüsündedir.",
        "Konut stoku tamamen müstakil evlerden oluşur; körfez kıyısındaki evlerin bir kısmı su cephelidir. Mahallenin doğusundaki Morningside Park, körfez manzaralı yürüyüş yolları, havuzu ve tekne rampasıyla sosyal hayatın merkezidir.",
    ],
    places=[
        ['Morningside Park', 'Körfez kıyısında havuzlu ve tekne rampalı mahalle parkı.'],
        ['MiMo Biscayne Boulevard', 'Batıda restoranlar ve butik oteller.'],
        ['Legion Park', 'Güneyde körfez kıyısında hafta sonu pazarı.'],
        ['Design District', 'Güneybatıda lüks alışveriş ve müzeler.'],
        ['Gizli köşe: Morningside sokakları', 'Tarihî evler ve banyan ağaçlarıyla sakin bir yürüyüş rotası.'],
    ],
    flood=flood("Körfez kıyısındaki evler yüksek riskli bölgelerdedir (AE); iç sokaklarda risk adres bazında değişir."),
    transport=[
        ['Brickell', 'yaklaşık 10 km · 15–20 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 15 km · 20 dakika'],
        ['Design District', 'yaklaşık 3 km · 5–10 dakika'],
        ['Toplu taşıma', 'Biscayne Boulevard üzerinde Metrobus hatları.'],
        ['Günlük hayat', 'Mahalle içi sakin; restoranlar ve hizmetler Biscayne Boulevard boyunca.'],
    ],
    projects=[], projects_notes=["Tarihî bölge statüsündeki mahallede yeni yapılaşma sınırlıdır; arz büyük ölçüde mevcut evlerin el değiştirmesiyle sağlanır."],
    pros=['Korunan tarihî doku ve körfez kıyısı park', 'Design District ve Miami Beach\'e yakınlık', 'Tamamen konut ağırlıklı sakin mahalle'],
    cons=['Satış sayısı çok az; fiyat verisi oynak', 'Tarihî bölge kuralları nedeniyle tadilat izinleri detaylıdır', 'Körfeze yakın evlerde sel sigortası maliyeti'],
    faq=[],
    sources=[],
))

S.append(dict(
    id='venetian-islands', name='Venetian Islands', county='Miami-Dade', lat=25.7905, lng=-80.1600,
    line='Venetian Causeway üzerinde körfez ortasında adalar.',
    lead='Venetian Causeway ile birbirine bağlanan, Downtown ile Miami Beach arasında Biscayne Körfezi\'nin ortasındaki altı yapay ada.',
    character=[
        "Venetian Islands, Biscayne Körfezi'nde, batıdan doğuya Biscayne Island, San Marco, San Marino, Di Lido, Rivo Alto ve Belle Isle'dan oluşan altı yapay adanın adıdır. Adalar, 1920'lerde inşa edilen Venetian Causeway ile hem Downtown Miami'ye hem Miami Beach'e bağlanır.",
        "Biscayne Island ve San Marco Island City of Miami, diğer dört ada Miami Beach sınırları içindedir. Konut stoku ağırlıkla su cepheli müstakil evlerden oluşur; Belle Isle ve batı adalarında kondominyumlar da bulunur.",
        "Venetian Causeway araçlar için ücretlidir ve yürüyüş ile bisiklet için Miami'nin en sevilen rotalarından biridir.",
    ],
    places=[
        ['Venetian Causeway', 'Adaları birbirine bağlayan, yürüyüş ve bisiklet için manzaralı köprü yolu.'],
        ['Belle Isle Park', 'Doğu ucundaki adada küçük mahalle parkı.'],
        ['Lincoln Road', 'Doğuda, köprünün Miami Beach ucunda alışveriş caddesi.'],
        ['Margaret Pace Park', 'Batıda, Edgewater\'da körfez kıyısı park.'],
        ['Gizli köşe: Gün doğumunda causeway', 'Downtown silüetine ve körfeze bakan sabah yürüyüşü.'],
    ],
    flood=flood("Körfez ortasındaki adaların tamamı yüksek riskli kıyı bölgelerindedir (AE)."),
    transport=[
        ['Downtown Miami', 'yaklaşık 4 km · 10 dakika'],
        ['South Beach (Lincoln Road)', 'yaklaşık 2 km · 5 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 16 km · 20–25 dakika'],
        ['Toplu taşıma', 'Toplu taşıma sınırlı; Venetian Causeway yürüyüş ve bisiklet yoluyla Downtown ve Miami Beach\'e bağlanır.'],
        ['Günlük hayat', 'Adalar tamamen konut amaçlıdır; günlük ihtiyaçlar için South Beach veya Edgewater kullanılır.'],
    ],
    projects=[], projects_notes=["Adalarda yeni yapı alanı çok sınırlıdır; arz büyük ölçüde mevcut evlerin el değiştirmesi ve yeniden inşasıyla sağlanır."],
    pros=['Su cepheli evler ve tekne erişimi', 'Downtown ile South Beach arasında merkezi konum', 'Ticari trafiği olmayan sakin adalar'],
    cons=['Kıyı bölgesi sel riski ve yüksek sigorta maliyeti', 'Causeway ücretli ve tek ulaşım yolu', 'Satış sayısı az; fiyatlar mülke göre çok değişir'],
    faq=[],
    sources=[],
))

S.append(dict(
    id='sofi', name='SoFi (South of Fifth)', county='Miami-Dade', lat=25.7700, lng=-80.1340,
    line='South Beach\'in en güneyindeki prestijli küçük bölge.',
    lead='South Pointe Park, okyanus cepheli lüks kuleleri ve köklü restoranlarıyla South Beach\'in en güneyindeki küçük ve prestijli bölge.',
    character=[
        "SoFi (South of Fifth), Miami Beach'in güney ucunda, 5. caddenin güneyinde kalan küçük bölgedir. Ocean Drive, Washington Avenue ve South Pointe Drive'ın güney kesimleri bu bölgededir.",
        "Okyanus cepheli ultra lüks kondominyum kuleleri, penthouse'lar ve orta yükseklikte binalar; Joe's Stone Crab gibi köklü restoranlarla yan yanadır. South Pointe Park, Government Cut kanalından geçen gemileri izleyebileceğiniz park ve iskelesiyle bölgenin simgesidir.",
        "South Beach'in kalabalık kesimlerine göre daha sakin bir yaşam sunar; Lincoln Road ve Art Deco bölgesi yürüme veya kısa bisiklet mesafesindedir.",
    ],
    places=[
        ['South Pointe Park', 'Adanın güney ucunda, gemilerin geçişini izleyebileceğiniz park ve iskele.'],
        ["Joe's Stone Crab", '1913\'ten beri hizmet veren köklü restoran.'],
        ['South Pointe Drive', 'Restoran ve kafelerle sakin cadde.'],
        ['Ocean Drive', 'Kuzeyde Art Deco cepheleri ve okyanus kıyısı.'],
        ['Gizli köşe: Gün batımında South Pointe iskelesi', 'Fisher Island ve Downtown silüetine bakan manzara.'],
    ],
    flood=flood("Bariyer adası üzerindeki bölgenin tamamı yüksek riskli kıyı bölgelerindedir (AE/VE)."),
    transport=[
        ['Brickell / Downtown', 'yaklaşık 10 km · 15–20 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 20 km · 25 dakika'],
        ['Fort Lauderdale Havalimanı (FLL)', 'yaklaşık 45 km · 45 dakika'],
        ['Toplu taşıma', 'Ücretsiz Miami Beach Trolley hatları ve Metrobus.'],
        ['Günlük hayat', 'Bölge yürünebilir; market ve restoranlar yakın.'],
    ],
    projects=[], projects_notes=[GENERIC_PJ],
    pros=['Okyanus cepheli lüks yaşam ve South Pointe Park', 'South Beach\'in kalabalığından uzak ama yürüme mesafesinde', 'Köklü restoranlar ve marina'],
    cons=['Çok yüksek giriş fiyatı', 'Kıyı bölgesi sel riski ve sigorta maliyeti', 'Miami Beach\'te sıkı kısa süreli kiralama kuralları'],
    faq=[],
    sources=[],
))

S.append(dict(
    id='hollywood-beach', name='Hollywood Beach', county='Broward', lat=26.0130, lng=-80.1190,
    line='Broadwalk, okyanus kıyısı ve "Old Florida" havası.',
    lead='Yaklaşık 4 km\'lik Broadwalk\'u, okyanus kıyısı restoranları ve "Old Florida" havasıyla Hollywood\'un sahil kesimi.',
    character=[
        "Hollywood Beach, Hollywood şehrinin okyanus ile Intracoastal Waterway arasındaki sahil kesimidir. Okyanus boyunca uzanan Broadwalk; restoranlar, kafeler ve bisiklet yoluyla bölgenin simgesidir.",
        "Alçak katlı eski binalar ve küçük oteller, \"Old Florida\" havasını korur; Margaritaville Hollywood Beach Resort ve The Diplomat gibi büyük oteller ile okyanus cepheli kondominyumlar ise bölgenin daha yeni yüzüdür. Konut stoku ağırlıkla kondominyumlardan oluşur.",
    ],
    places=[
        ['Hollywood Beach Broadwalk', 'Okyanus boyunca restoran, kafe ve bisiklet yoluyla uzanan yürüyüş yolu.'],
        ['Margaritaville Hollywood Beach Resort', 'Broadwalk üzerinde otel, restoranlar ve etkinlikler.'],
        ['Charnow Park', 'Broadwalk\'ta oyun alanı ve su parkı.'],
        ['Anne Kolb Nature Center', 'Batıda mangrovlar arasında kano rotaları ve seyir kulesi.'],
        ['Gizli köşe: Broadwalk\'ta gün doğumu', 'Kalabalık başlamadan okyanus kıyısında sabah yürüyüşü.'],
    ],
    flood=flood("Bariyer adası üzerindeki bölgenin tamamına yakını yüksek riskli kıyı bölgelerindedir (AE/VE)."),
    transport=[
        ['Fort Lauderdale Havalimanı (FLL)', 'yaklaşık 10 km · 15 dakika'],
        ['Miami Uluslararası Havalimanı (MIA)', 'yaklaşık 35 km · 35 dakika'],
        ['Aventura', 'yaklaşık 12 km · 15 dakika'],
        ['Toplu taşıma', 'Hollywood Trolley ve Broward County Transit; Tri-Rail Hollywood istasyonu ana karada.'],
        ['Günlük hayat', 'Broadwalk çevresi yürünebilir; büyük alışveriş için ana karaya araçla.'],
    ],
    projects=[], projects_notes=["Hollywood genelindeki yeni projeler (Icon Beach Waterfront Residences dahil) Hollywood raporunda listelenir."],
    pros=['Güney Florida\'nın en yaşanabilir plaj şeritlerinden biri', 'FLL havalimanına 15 dakika', 'Miami Beach\'e göre daha uygun fiyatlar'],
    cons=['Kıyı bölgesi sel riski ve sigorta maliyeti', 'Eski kondominyumlarda özel aidat riski', 'Sezon döneminde kalabalık ve otopark sıkıntısı'],
    faq=[],
    sources=[],
))

# Orijinal raporlardan korunacak alanlar (yalnızca bu id'ler önceden birleşik kayıttı)
PREV = {'pinecrest', 'wynwood', 'edgewater', 'north-beach', 'bal-harbour', 'pompano'}


def build():
    hoods = json.load(open(os.path.join(ROOT, 'tools', 'hoods.json'), encoding='utf-8'))
    hmap = {h['id']: h for h in hoods}
    for s in S:
        d = {
            'id': s['id'], 'name': s['name'], 'county': s['county'],
            'meta': '', 'short': s['lead'], 'lead': s['lead'],
            'sales': {}, 'rent': {}, 'tax': {},
            'character': s['character'], 'places': s['places'],
            'costs': [['Emlak vergisi', ''], ['Site aidatı (HOA)', HOA], ['Sigorta ve sel bölgesi', s['flood']], ['Okul ve güvenlik verisi', schools(s['county'])]],
            'transport': s['transport'], 'projects': s['projects'], 'projects_notes': s['projects_notes'],
            'pros': s['pros'], 'cons': s['cons'], 'faq': s['faq'],
            'sources': s['sources'] + [['FEMA Flood Map Service Center', 'https://msc.fema.gov/portal/search']],
            'wa': f"Merhaba Aleyna Hanım, {s['name']} raporunu okudum. Bu bölge hakkında görüşmek istiyorum.",
        }
        json.dump(d, open(os.path.join(ROOT, 'tools', 'reports', s['id'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        h = {'id': s['id'], 'name': s['name'], 'county': s['county'], 'lat': s['lat'], 'lng': s['lng'], 'line': s['line']}
        if s['id'] in hmap:
            hmap[s['id']].update(h)
        else:
            hoods.append(h)
            hmap[s['id']] = h
    json.dump(hoods, open(os.path.join(ROOT, 'tools', 'hoods.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', len(S), 'reports; hoods', len(hoods))


if __name__ == '__main__':
    build()
