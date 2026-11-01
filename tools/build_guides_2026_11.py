# -*- coding: utf-8 -*-
"""Haftalık rehber sayfaları (2 Kasım 2026 haftası): yabancı alıcı süreci ve proje aşamasından daire almak.

Şablon: rehberler/index.html, düzen: neden-miami. Her rakam kaynağı ve tarihiyle burada tutulur;
yeni proje istatistikleri tools/projects.json'dan (Cervera Development Market Study, Q3 2026) hesaplanır.
Kullanım: python3 tools/build_guides_2026_11.py
"""
import html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
BASE = 'https://miamievim.com'
NOTE = 'Bu sayfa genel bilgilendirme amaçlıdır; vergi, hukuk, göçmenlik veya finansman tavsiyesi değildir. Kendi durumunuz için bir vergi danışmanı veya avukata başvurun.'


def link(u, t):
    return f'<a href="{u}" target="_blank" rel="noopener">{E(t)}</a>'


def hood(i, name):
    return f'<a href="/mahalle-raporlari/{i}/">{E(name)}</a>'


# ---------------------------------------------------------------- Rehber 1: yabancı olarak ev almak
CS1 = {
    'sb264': ('Florida Senatosu: CS/CS/SB 264 yasa özeti (Ch. 2023-33)', 'https://www.flsenate.gov/Committees/BillSummaries/2023/html/264'),
    'resale': ('Fla. Stat. 718.503: kondominyum satışında belge teslimi ve cayma hakkı (2026)', 'https://www.flsenate.gov/Laws/Statutes/2026/718.503'),
    'fincen': ('Davis Wright Tremaine: FinCEN Residential Real Estate Rule on Hold (27 Mayıs 2026)', 'https://www.dwt.com/insights/2026/05/fincen-residential-real-estate-rule-on-hold'),
    'rent': ('IRS: Nonresident aliens, real property located in the U.S.', 'https://www.irs.gov/individuals/international-taxpayers/nonresident-aliens-real-property-located-in-the-us'),
    'itin': ('IRS: Individual Taxpayer Identification Number (ITIN)', 'https://www.irs.gov/individuals/individual-taxpayer-identification-number'),
    'firpta': ('IRS: FIRPTA withholding', 'https://www.irs.gov/individuals/international-taxpayers/firpta-withholding'),
    'estate': ('IRS: Some nonresidents with U.S. assets must file estate tax returns', 'https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-us-assets-must-file-estate-tax-returns'),
    'treaty': ('ABD Dışişleri Bakanlığı: Treaty Countries (E-1/E-2 anlaşma ülkeleri)', 'https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/fees/treaty.html'),
    'e2': ('ABD Dışişleri Bakanlığı: Treaty Trader & Treaty Investor (E) vizeleri', 'https://travel.state.gov/content/travel/en/us-visas/employment/treaty-trader-investor-visa-e.html'),
    'uscis': ('USCIS: E-2 Treaty Investors', 'https://www.uscis.gov/working-in-the-united-states/temporary-workers/e-2-treaty-investors'),
    'fema': ('FEMA Flood Map Service Center', 'https://msc.fema.gov/portal/search'),
}


def build_foreign():
    url = BASE + '/rehberler/yabanci-olarak-ev-almak/'
    stats = [
        ('7', 'Kısıtlı ülke (SB 264)', 'Çin, Rusya, İran, Kuzey Kore, Küba, Venezuela (Maduro yönetimi) ve Suriye. Türkiye listede yer almıyor. Kaynak: <a href="https://www.flsenate.gov/Committees/BillSummaries/2023/html/264" target="_blank" rel="noopener">Florida Senatosu</a> (2023).'),
        ('%15', 'FIRPTA kesintisi', 'Yabancı uyruklu satıcıda alıcının satış bedelinden kestiği genel oran; konut istisnaları $300.000 ve $1 milyon eşiklerine bağlıdır. Kaynak: <a href="https://www.irs.gov/individuals/international-taxpayers/firpta-withholding" target="_blank" rel="noopener">IRS</a> (Kasım 2026 erişimi).'),
        ('$60.000', 'Veraset beyan eşiği', 'ABD\'de yerleşik olmayan yabancıların ABD\'deki varlıkları vefat anında bu tutarı aşarsa Form 706-NA verilir; ABD\'deki gayrimenkul bu varlıklara dahildir. Kaynak: <a href="https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-us-assets-must-file-estate-tax-returns" target="_blank" rel="noopener">IRS</a>.'),
    ]
    sections = [
        ('01', 'Kısa cevap', [
            'Evet, Türkiye vatandaşı olarak Florida\'da konut satın alabilirsiniz. ABD vatandaşlığı, yeşil kart veya oturma izni gerekmez; satın alma nakitle ya da yabancı uyruklu alıcılara kredi veren bir kuruluşla yapılabilir.',
            'Florida\'nın 2023\'te çıkardığı SB 264 yasası yalnızca yedi "endişe duyulan ülke" ile bağlantılı kişi ve kurumlara kısıt getirir: Çin, Rusya, İran, Kuzey Kore, Küba, Venezuela\'daki Maduro yönetimi ve Suriye. Türkiye bu listede değildir.',
            'Konut satın almak tek başına ABD vizesi veya oturma izni sağlamaz. Süreç; bütçe ve finansman, bölge seçimi, teklif ve sözleşme, denetim ve kapanış, ardından vergi yükümlülükleri olarak ilerler.',
        ], ['sb264']),
        ('02', 'Adım 1: Bütçe ve finansman', [
            'Teklif verirken satıcı, ödeme gücünüzü gösteren bir belge ister: nakit alımda banka hesabı veya fon kanıtı (proof of funds), kredili alımda kredi kuruluşunun ön onay mektubu.',
            'Yabancı uyruklu alıcılara verilen konut kredilerinde (foreign national mortgage) peşinat oranı, faiz ve istenen belgeler kredi kuruluşuna göre değişir; ABD kredi geçmişi yerine yurt dışındaki gelir ve banka kayıtları incelenir. Bu konu takvimdeki ayrı bir rehberde (21 Aralık) ayrıntılı anlatılacak.',
            'Bütçeye yalnızca fiyatı değil, kapanış masraflarını, aidatı, emlak vergisini ve sigortayı da ekleyin. Net getiriyi hesaplamak için <a href="/yatirim/">yatırım sayfasındaki hesaplayıcıyı</a> kullanabilirsiniz.',
        ], []),
        ('03', 'Adım 2: Bölge ve mülk tipi', [
            'Miami\'de yabancı alıcıların incelediği konutların büyük kısmı kondominyum dairedir. Dairede binanın kiralama kuralları (en kısa kira süresi, yılda kaç kez kiralanabileceği), aidat, binanın denetim ve yedek akçe durumu fiyat kadar önemlidir. Müstakil evde ise sel bölgesi, sigorta ve bakım masrafı öne çıkar.',
            'Yürünebilir, toplu taşımaya yakın bir kent merkezi için ' + hood('brickell', 'Brickell') + ', ' + hood('downtown-miami', 'Downtown Miami') + ' ve ' + hood('edgewater', 'Edgewater') + '; okyanus kıyısında tam hizmetli binalar için ' + hood('sunny-isles', 'Sunny Isles Beach') + ' ve ' + hood('surfside', 'Surfside') + '; bahçeli müstakil evler ve ağaçlı sokaklar için ' + hood('coral-gables', 'Coral Gables') + ' ve ' + hood('coconut-grove', 'Coconut Grove') + ' raporlarına bakabilirsiniz. Her raporda fiyat, kira, aidat, sigorta ve sel bölgesi kaynağıyla verilir.',
            'Henüz inşaat aşamasındaki bir daireyi düşünüyorsanız süreç farklıdır; <a href="/rehberler/proje-asamasindan-daire-almak/">proje aşamasından daire alma rehberine</a> ve <a href="/yeni-projeler/">yeni projeler listesine</a> bakın.',
        ], []),
        ('04', 'Adım 3: Teklif ve satış sözleşmesi', [
            'Teklif yazılı bir satış sözleşmesiyle verilir. Sözleşmede fiyat, emanet hesabına (escrow) yatırılacak depozito ve tarihi, denetim süresi, varsa kredi şartı ve kapanış tarihi yer alır. Depozito, kapanışa kadar tapu şirketinin veya avukatın emanet hesabında tutulur.',
            'İkinci el bir kondominyum dairede satıcının dernek belgelerini (yönetmelik, bütçe, tutanaklar ve benzeri) vermesi istenebilir; sözleşmede bu hak kullanılırsa alıcı, belgeleri aldıktan sonra hafta sonu ve resmi tatiller hariç 7 gün içinde yazılı bildirimle sözleşmeyi feshedebilir (Fla. Stat. 718.503(2)). Bu süreyi belgeleri gerçekten okumak için kullanın.',
        ], ['resale']),
        ('05', 'Adım 4: Denetim, sigorta ve kapanış', [
            'Denetim süresinde lisanslı bir denetçiyle evin veya dairenin durumu incelenir; aynı dönemde konut ve gerekirse sel sigortası teklifi alınır. Adresin sel bölgesini ' + link('https://msc.fema.gov/portal/search', 'FEMA haritasından') + ' kontrol edebilirsiniz.',
            'Kapanışı genellikle bir tapu şirketi veya gayrimenkul avukatı yürütür: tapu araştırması, tapu sigortası, ödemelerin dağıtımı ve tapunun kaydı. Kapanış belgeleri çoğu durumda uzaktan imzalanabilir; yöntemi (vekâletname, konsoloslukta onay veya uzaktan noter) tapu şirketiyle önceden netleştirin.',
            'Para transferinde dolandırıcılığa dikkat edin: banka bilgilerini yalnızca e-postaya güvenerek değil, tapu şirketini bildiğiniz bir numaradan arayarak teyit edin. Hesap bilgilerinin son anda "değiştiğini" söyleyen bir mesaj uyarı işaretidir.',
            'Mülkü bir şirket (LLC) veya tröst üzerinden nakitle almak için FinCEN\'in getirdiği yeni bildirim kuralı 1 Mart 2026\'da başlayacaktı; 19 Mart 2026\'da bir federal mahkeme kuralı iptal etti ve FinCEN 11 Mayıs 2026\'da itiraz etti. Mayıs 2026 itibarıyla bu bildirim zorunlu değildir; itiraz sonucunda değişebilir.',
        ], ['fema', 'fincen']),
        ('06', 'Sahip olduktan sonra: kira geliri ve vergiler', [
            'Emlak vergisi her yıl ödenir. Birincil konut (homestead) indirimi yalnızca Florida\'da sürekli ikamet eden ve mülkte oturan sahiplere verilir; kiraya verilen veya ikinci ev olarak kullanılan mülkler bu indirimi alamaz.',
            'ABD\'de yerleşik olmayan yabancıların ABD\'deki gayrimenkulden elde ettiği kira geliri, bir ticari faaliyetle bağlantılı değilse %30 (veya vergi anlaşmasındaki daha düşük oran) ile vergilendirilir. Mülk sahibi, IRC 871(d) kapsamında bu geliri net esasa göre beyan etmeyi seçebilir; bu durumda giderler düşülür ve kademeli oranlar uygulanır. Seçim Form 1040-NR\'a eklenen bir beyanla yapılır.',
            'ABD vergi beyannamesi vermek için sosyal güvenlik numarası yoksa bireysel vergi kimlik numarası (ITIN) alınır.',
        ], ['rent', 'itin']),
        ('07', 'Satarken ve veraset: FIRPTA ve Form 706-NA', [
            'Yabancı uyruklu bir satıcı ABD\'deki gayrimenkulünü sattığında, alıcı satış bedelinin genellikle %15\'ini kesip IRS\'e yatırır (FIRPTA). Satış bedeli $300.000 veya altındaysa ve alıcı evi konut olarak kullanacaksa kesinti uygulanmayabilir; $300.000 ile $1 milyon arasında daha düşük oran uygulanabilir. Kesilen tutar gerçek vergiden fazlaysa fark beyanname ile geri alınır.',
            'ABD\'de yerleşik olmayan bir yabancı vefat ettiğinde ABD\'deki varlıklarının değeri $60.000\'i aşarsa veraset vergisi beyannamesi (Form 706-NA) verilmesi gerekir; ABD\'deki gayrimenkul bu varlıklara dahildir. Bazı ülkelerle yapılmış veraset vergisi anlaşmaları daha avantajlı kurallar getirebilir. Mülkün kimin veya hangi yapının adına alınacağı bu nedenle baştan, bir vergi danışmanıyla planlanmalıdır.',
        ], ['firpta', 'estate']),
        ('08', 'Vize ve oturma izni', [
            'Konut sahibi olmak ABD\'de kalma veya çalışma hakkı vermez. Türkiye, 18 Mayıs 1990\'dan bu yana E-2 (anlaşmalı yatırımcı) vizesi kapsamındaki ülkeler arasındadır; ancak E-2, mal veya hizmet üreten, gerçek ve faal bir ticari işletmeye yapılan esaslı bir yatırım ister. Banka hesabında bekleyen, geri çekilebilir fonlar yatırım sayılmaz.',
            'Kiraya verilen bir daire veya kendi kullanımınız için alınan bir ev, tek başına bu şartı karşılamaz. Vize seçenekleri için bir göçmenlik avukatına danışın.',
        ], ['treaty', 'e2', 'uscis']),
        ('09', 'Bir sonraki adım', [
            'Bütçenizi ve kriterlerinizi paylaşırsanız güncel MLS ilanları <a href="/ilanlar/">ilan talep sayfasından</a> size gönderilir. Bölgeleri karşılaştırmak için <a href="/mahalle-testi/">mahalle testini</a> çözebilir veya Miami-Dade, Broward ve Palm Beach\'teki 121 bölgenin <a href="/mahalle-raporlari/">mahalle raporlarına</a> bakabilirsiniz.',
        ], []),
    ]
    faq = [
        ('Türk vatandaşı Miami\'de ev alabilir mi?', 'Evet. Florida\'da yabancıların konut almasını genel olarak yasaklayan bir kural yoktur; vatandaşlık veya oturma izni gerekmez. 2023 tarihli SB 264 yasası yalnızca Çin, Rusya, İran, Kuzey Kore, Küba, Venezuela (Maduro yönetimi) ve Suriye ile bağlantılı kişi ve kurumlara kısıt getirir; Türkiye bu listede değildir. Bu bilgi hukuki tavsiye değildir.'),
        ('Miami\'de ev almak oturma izni veya vize sağlar mı?', 'Hayır. Konut sahibi olmak ABD\'de kalma veya çalışma hakkı vermez. Türkiye E-2 anlaşmalı yatırımcı vizesi kapsamındadır, ancak bu vize gerçek ve faal bir ticari işletmeye yapılan esaslı yatırım ister; konut alımı tek başına yeterli değildir. Bir göçmenlik avukatına danışın.'),
        ('Yabancı biri Miami\'deki evini satarken ne kadar vergi kesilir?', 'FIRPTA kapsamında alıcı, satış bedelinin genellikle %15\'ini kesip IRS\'e yatırır. $300.000 ve altındaki, alıcının konut olarak kullanacağı satışlarda kesinti uygulanmayabilir; $300.000 ile $1 milyon arasında daha düşük oran uygulanabilir. Fazla kesilen tutar beyannameyle geri alınır. Bu bilgi vergi tavsiyesi değildir.'),
        ('Yabancı alıcının kira geliri ABD\'de vergilendirilir mi?', 'Evet. ABD\'de yerleşik olmayan yabancıların kira geliri, ticari faaliyetle bağlantılı değilse %30 (veya anlaşmadaki daha düşük oran) ile vergilendirilir. IRC 871(d) seçimiyle net esasa geçilebilir; giderler düşülür ve kademeli oranlar uygulanır. Bu bilgi vergi tavsiyesi değildir.'),
    ]
    return dict(
        slug='yabanci-olarak-ev-almak', url=url, cs=CS1,
        title='Yabancı Olarak Miami\'de Ev Almak (2026): Adım Adım | Aleyna Bozoklar',
        desc='Türkiye vatandaşı olarak Florida\'da ev almak: SB 264, teklif, emanet, kapanış, kira vergisi, FIRPTA, veraset ve vize. Resmi kaynaklarla adım adım.',
        og='Yabancı olarak Miami\'de ev almak', headline='Yabancı olarak Miami\'de ev almak: adım adım süreç (2026)',
        crumb='Yabancı olarak ev almak', tab='Yabancı alıcı',
        h1='Yabancı olarak <em>Miami\'de ev almak</em>',
        lead='Türkiye vatandaşı olarak Florida\'da konut alabilir misiniz, hangi adımlar izlenir, sahip olduktan ve satarken hangi vergiler doğar? Her kural resmi kaynağıyla.',
        date_iso='2026-11-02', date='2 Kasım 2026', stats=stats, sections=sections, faq=faq,
        sources=list(CS1.values()), cta=('/ilanlar/', 'İlan listesi isteyin'), css=[])


# ---------------------------------------------------------------- Rehber 2: proje aşamasından daire almak
CS2 = {
    'escrow': ('Fla. Stat. 718.202: geliştirici satışlarında depozitoların emanette tutulması (2026)', 'https://m.flsenate.gov/Statutes/718.202'),
    'cancel': ('Fla. Stat. 718.503: geliştiriciden alımda 15 günlük cayma hakkı (2026)', 'https://www.flsenate.gov/Laws/Statutes/2026/718.503'),
    'check': ('MIAMI REALTORS®: New Construction Condominium Due Diligence Checklist, 21+ daireli binalar (Şubat 2026)', 'https://www.miamirealtors.com/wp-content/uploads/bsk-pdf-manager/2026/02/New-Construction-Condominium-Due-Diligence-Checklist-Condominiums-with-21-or-More-Residential-Units.pdf'),
    'cervera': ('Cervera Real Estate, Development Market Study, Q3 2026 (miamievim.com yeni projeler sayfası)', BASE + '/yeni-projeler/'),
}


def project_stats():
    p = json.load(open(os.path.join(ROOT, 'tools', 'projects.json'), encoding='utf-8'))['projects']
    tot = [int(m.group(1)) for m in (re.match(r'(\d+)%', x['deposit_total'].strip()) for x in p) if m]
    st = [x['status'].lower().replace('-', ' ').replace('constrction', 'construction') for x in p]
    return dict(n=len(p), n_tot=len(tot), n_4050=sum(1 for a in tot if a in (40, 50)),
                uc=sum(1 for s in st if s == 'under construction'), pre=sum(1 for s in st if s == 'pre sales'))


def build_precon():
    url = BASE + '/rehberler/proje-asamasindan-daire-almak/'
    ps = project_stats()
    stats = [
        ('15 gün', 'Yasal cayma hakkı', 'Geliştiriciden alımda sözleşmeyi imzalayıp yasal belgelerin tamamını aldıktan sonra; bu haktan feragat edilemez. Kaynak: <a href="https://www.flsenate.gov/Laws/Statutes/2026/718.503" target="_blank" rel="noopener">Fla. Stat. 718.503</a> (2026).'),
        ('%10', 'Emanet eşiği', 'Satış bedelinin %10\'una kadar depozito emanette; fazlası ayrı bir özel emanet hesabında tutulur ve yalnızca sözleşme izin verirse inşaatta kullanılır. Kaynak: <a href="https://m.flsenate.gov/Statutes/718.202" target="_blank" rel="noopener">Fla. Stat. 718.202</a> (2026).'),
        (f'{ps["n_4050"]} / {ps["n_tot"]}', 'Teslim öncesi %40–%50', f'Toplam depozito bilgisi olan {ps["n_tot"]} Miami projesinin {ps["n_4050"]}\'inde teslim öncesi toplam depozito %40 veya %50. Kaynak: Cervera Development Market Study, Q3 2026.'),
    ]
    sections = [
        ('01', 'Kısa cevap', [
            'Proje aşamasından (pre-construction) daire alırken fiyatın bir kısmını inşaat süresince taksitlerle depozito olarak ödersiniz; kalan tutar bina tamamlanıp kapanış yapıldığında ödenir. Florida\'da bu depozitoların nasıl tutulacağı ve alıcının cayma hakkı kondominyum yasasıyla (Florida Statutes, Bölüm 718) düzenlenir.',
            'Üç kural öne çıkar: satış bedelinin %10\'una kadar depozito emanette bekler; %10\'un üstü ancak sözleşmede açıkça yazıyorsa inşaat giderleri için kullanılabilir; alıcı, sözleşmeyi imzalayıp yasal belgelerin tamamını aldıktan sonraki 15 gün içinde yazılı bildirimle sözleşmeden vazgeçebilir ve depozitosunu geri alır.',
        ], ['escrow', 'cancel']),
        ('02', 'Süreç adım adım', [
            'Rezervasyon: Bazı projeler sözleşmeden önce rezervasyon depozitosu alır. Yasaya göre rezervasyon depozitosu yazılı talep üzerine tamamen iade edilir; sözleşme imzalandıktan sonra satış depozitosu kurallarına tabi olur.',
            'Sözleşme ve belgeler: Geliştirici sözleşmeyle birlikte tanıtım belgesini (prospectus veya offering circular) ve eklerini (yönetmelik, tahmini bütçe, kat planları, emanet sözleşmesi) teslim eder. 15 günlük süre, imza ve bu belgelerin tamamının teslimi gerçekleştikten sonra başlar.',
            'Depozito takvimi: Taksitler genellikle sözleşmede, temel atmada ve kaba inşaatın bitiminde (top-off) ödenir. İnşaat bitince iskân izni (certificate of occupancy) alınır; kapanışta kalan bakiye nakit veya kredi ile ödenir ve tapu devredilir.',
        ], ['escrow', 'cancel']),
        ('03', 'Depozitonuz nerede durur?', [
            'Bina tamamlanmadan yapılan satışlarda depozitolar bir emanet (escrow) hesabına yatırılır; emanet acentesinin kim olduğu sözleşmede ve tanıtım belgesinde yazar ve talep ederseniz size makbuz verilir.',
            'Satış bedelinin %10\'unu aşan ödemeler ayrı bir özel emanet hesabında tutulur. Sözleşme izin veriyorsa ve inşaat başlamışsa geliştirici bu fazlayı yıkım, saha hazırlığı, izin ve etki harçları ile mimarlık ve mühendislik gibi fiili inşaat giderleri için çekebilir. Bu durumda sözleşmede, imzanızın üstünde kalın harflerle "MAY BE USED FOR CONSTRUCTION PURPOSES BY THE DEVELOPER" ifadesi bulunmak zorundadır.',
            'Çekilen paralar satış komisyonu, maaş, reklam, pazarlama, kredi maliyeti, avukat, muhasebe veya sigorta giderleri için kullanılamaz. Alıcı sözleşmeyi usulüne uygun feshederse parasını faiziyle geri alır; alıcı temerrüde düşerse emanetteki tutar geliştiriciye geçer.',
        ], ['escrow']),
        ('04', 'Cayma hakkı ve sözleşme değişiklikleri', [
            'Geliştiriciden alımda sözleşme, imzadan ve yasal belgelerin tamamının tesliminden sonraki 15 gün içinde alıcının yazılı bildirimiyle feshedilebilir. Bu hak sözleşmede belirgin harflerle yazılmak zorundadır ve bu haktan feragat ettiren hükümler geçersizdir.',
            'Geliştirici daha sonra teklifi alıcının aleyhine önemli ölçüde değiştiren bir değişiklik gönderirse, alıcının bu değişikliği aldıktan sonra yeniden 15 gün cayma hakkı doğar. Ancak bütçedeki olağan maliyet artışları "önemli aleyhe değişiklik" sayılmaz. Cayma hakkı kapanışla sona erer.',
        ], ['cancel']),
        ('05', 'İmzadan önce hangi belgeleri incelemeli?', [
            'MIAMI REALTORS®\'ın yeni inşaat kondominyum kontrol listesi şu başlıkları öne çıkarır: emanet acentesi ve emanet sözleşmesi; en az 12 aylık tahmini işletme bütçesi ve daire başına aidat tablosu (bütçe "iyi niyetli tahmin" olarak verilir); kapanış masrafları; yapısal bütünlük yedek akçe etüdü (SIRS) veya henüz yapılmadığına dair açıklama; geliştiricinin yönetimde kalacağı süre; bir yıldan uzun yönetim sözleşmeleri.',
            'Ayrıca satış, kiralama ve devir kısıtlarını (en kısa kira süresi, yılda kaç kez kiralanabileceği), evcil hayvan gibi kullanım kurallarını, tahmini tamamlanma tarihini, mülkiyet türünü (tam mülkiyet veya kiralık arsa) ve geliştiricinin deneyimini kontrol edin. Projelerin kiralama kuralları <a href="/yeni-projeler/">yeni projeler sayfasında</a> listelenir.',
        ], ['check']),
        ('06', 'Miami\'de ödeme planları nasıl görünüyor?', [
            f'Cervera Development Market Study\'nin Q3 2026 sürümünde Brickell, Downtown, Edgewater, Miami Beach, Coconut Grove ve Coral Gables\'ta {ps["n"]} proje yer alıyor: {ps["uc"]} projede inşaat sürüyor, {ps["pre"]} proje ön satışta. Toplam depozito bilgisi olan {ps["n_tot"]} projenin {ps["n_4050"]}\'inde teslim öncesi ödenen toplam depozito satış bedelinin %40\'ı veya %50\'si; kalan %50–%60 kapanışta ödenir.',
            'Sık görülen bir plan: sözleşmede %20, temel atmada %10, kaba inşaatın bitiminde %10 ve teslimde kalan %60. Taksit sayısı ve zamanlaması projeden projeye değişir; her projenin planı <a href="/yeni-projeler/">yeni projeler listesinde</a> verilir.',
            'Projelerin yoğunlaştığı bölgeleri karşılaştırmak için ' + hood('brickell', 'Brickell') + ', ' + hood('downtown-miami', 'Downtown Miami') + ', ' + hood('edgewater', 'Edgewater') + ', ' + hood('south-beach', 'South Beach') + ', ' + hood('surfside', 'Surfside') + ' ve ' + hood('coconut-grove', 'Coconut Grove') + ' mahalle raporlarına bakabilirsiniz.',
        ], ['cervera']),
        ('07', 'Riskler ve dikkat edilecekler', [
            'Teslim tarihi: Tanıtım belgesindeki tamamlanma tarihi tahminidir; gecikme hâlinde haklarınızı sözleşmedeki ilgili maddeler belirler. Kapanış: Kalan bakiyeyi kredi ile ödeyecekseniz kredi, teslim yaklaşırken o günkü faiz ve ekspertiz değerine göre verilir; ekspertiz değeri sözleşme fiyatının altında kalırsa farkı nakit tamamlamanız gerekebilir.',
            'Devir (assignment): Sözleşmeyi kapanıştan önce başkasına devretme hakkı birçok projede kısıtlanır veya geliştiricinin onayına bağlanır; bu konuyu imzadan önce sorun. Aidat: Bütçe tahmindir; bina teslim edilip dernek yönetimi el değiştirdiğinde aidat değişebilir.',
            'Yabancı alıcıysanız vergi ve yapı (şahsen veya şirket üzerinden alım) sorularını baştan planlayın; ayrıntılar için <a href="/rehberler/yabanci-olarak-ev-almak/">yabancı olarak ev alma rehberine</a> bakın.',
        ], []),
        ('08', 'Bir sonraki adım', [
            f'{ps["n"]} projenin tahmini teslim tarihi, ödeme planı, geliştiricisi ve kiralama kuralı <a href="/yeni-projeler/">yeni projeler sayfasında</a>; fiyat listesi ve kat planı talep üzerine gönderilir. Kira getirisini önceden hesaplamak için <a href="/yatirim/">net getiri hesaplayıcısını</a> kullanabilirsiniz.',
        ], []),
    ]
    faq = [
        ('Proje aşamasında ödediğim depozito nasıl korunur?', 'Florida yasasına göre geliştirici satışlarında depozitolar emanet hesabında tutulur. Satış bedelinin %10\'una kadarı kapanışa kadar emanette kalır; %10\'un üstü ayrı bir özel emanet hesabına yatırılır ve yalnızca sözleşmede açıkça izin verilmişse fiili inşaat giderleri için kullanılabilir; reklam, komisyon veya maaş için kullanılamaz (Fla. Stat. 718.202). Bu bilgi hukuki tavsiye değildir.'),
        ('Proje aşamasından aldığım daireden vazgeçebilir miyim?', 'Sözleşmeyi imzalayıp yasal belgelerin tamamını aldıktan sonraki 15 gün içinde yazılı bildirimle vazgeçebilir ve depozitonuzu geri alabilirsiniz; bu haktan feragat edilemez. Geliştirici sonradan teklifi aleyhinize önemli ölçüde değiştirirse yeniden 15 gün hakkınız olur. Bu süreler dışında vazgeçmek depozitonun kaybına yol açabilir (Fla. Stat. 718.503).'),
        ('Miami\'de yeni projelerde depozito oranı ne kadar?', f'Cervera Development Market Study Q3 2026 verisine göre toplam depozito bilgisi olan {ps["n_tot"]} projenin {ps["n_4050"]}\'inde teslim öncesi toplam depozito %40 veya %50; kalan tutar kapanışta ödenir. Sık görülen takvim: sözleşmede %20, temel atmada %10, kaba inşaat bitiminde %10.'),
        ('Yabancı olarak proje aşamasından daire alabilir miyim?', 'Evet; yabancı alıcılar Miami\'deki yeni projelerden daire alabilir. Kalan bakiyeyi kredi ile ödeyecekseniz kredi teslim zamanındaki faiz ve ekspertiz değerine göre verilir; vergi ve mülkiyet yapısını baştan bir danışmanla planlayın. Bu bilgi finansman veya vergi tavsiyesi değildir.'),
    ]
    return dict(
        slug='proje-asamasindan-daire-almak', url=url, cs=CS2,
        title='Proje Aşamasından Daire Almak: Depozito ve Cayma Hakkı | Aleyna Bozoklar',
        desc='Miami\'de proje aşamasından daire alırken depozito nasıl korunur, 15 günlük cayma hakkı nedir, ödeme planları nasıldır? Florida yasası ve Q3 2026 verisi.',
        og='Proje aşamasından daire almak', headline='Proje aşamasından daire almak: depozito, emanet hesabı ve cayma hakkı',
        crumb='Proje aşamasından daire almak', tab='Proje aşamasından',
        h1='Proje aşamasından <em>daire almak</em>',
        lead='Miami\'de inşaatı süren bir projeden daire alırken depozitolarınız nerede tutulur, ne zaman vazgeçebilirsiniz, imzadan önce hangi belgeleri incelemelisiniz? Florida yasası ve 83 projenin ödeme planı verisiyle.',
        date_iso='2026-11-02', date='2 Kasım 2026', stats=stats, sections=sections, faq=faq,
        sources=list(CS2.values()), cta=('/yeni-projeler/', 'Yeni projeleri inceleyin'), css=[])


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
    guides = [build_foreign(), build_precon()]
    tabs = TABS + [('/rehberler/' + g['slug'] + '/', g['tab']) for g in guides]
    for g in guides:
        render(g, tpl, tabs)
        print('ok', g['slug'])
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'stamp_assets.py')], check=True)


if __name__ == '__main__':
    main()
