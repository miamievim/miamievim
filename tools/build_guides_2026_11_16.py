# -*- coding: utf-8 -*-
"""Haftalık rehber sayfaları (16 Kasım 2026 haftası): kondominyumda SIRS ve milestone denetimi; Miami'de okul bölgeleri.

Şablon: rehberler/index.html, düzen: neden-miami. Her rakam kaynağı ve tarihiyle burada tutulur.
Kullanım: python3 tools/build_guides_2026_11_16.py
"""
import html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
BASE = 'https://miamievim.com'
NOTE = 'Bu sayfa genel bilgilendirme amaçlıdır; hukuk, vergi veya finansman tavsiyesi değildir. Bir kondominyum alımında dernek belgelerini bir Florida avukatıyla birlikte inceleyin.'
NOTE_SCHOOL = 'Bu sayfa genel bilgilendirme amaçlıdır; hukuk tavsiyesi değildir. Okul atamaları, başvuru tarihleri ve kayıt şartları her yıl değişebilir; kesin bilgi için ilgili okul bölgesine başvurun. Mahalleler bu sitede okul notlarına göre sıralanmaz veya önerilmez.'


def link(u, t):
    return f'<a href="{u}" target="_blank" rel="noopener">{E(t)}</a>'


def hood(i, name):
    return f'<a href="/mahalle-raporlari/{i}/">{E(name)}</a>'


# ---------------------------------------------------------------- Rehber 1: SIRS ve milestone
CS1 = {
    'ms': ('Florida Statutes 553.899: Mandatory structural inspections for condominium and cooperative buildings (2026 sürümü)', 'https://m.flsenate.gov/Statutes/553.899'),
    'hb913': ('Florida Senate: CS/CS/HB 913 (2025) yasa özeti', 'https://flsenate.gov/Committees/BillSummaries/2025/html/913'),
    'dbpr': ('Florida DBPR: Condominiums and Cooperatives SIRS Reporting (Kasım 2026 erişimi)', 'https://www2.myfloridalicense.com/condominiums/condominiums-and-cooperatives-sirs-reporting/'),
    'ra': ('Reserve Advisors: Florida Structural Integrity Reserve Study Requirements (28 Ocak 2026 güncellemesi)', 'https://www.reserveadvisors.com/florida-structural-integrity-reserve-study-requirements'),
    'ksn': ('KSN Law: 2025 Condominium Rider and Disclosure Requirements (12 Ocak 2026)', 'https://www.ksnlaw.com/blog/florida-condo-buyers-rider-disclosure-requirements/'),
    'hm': ('Hamilton Mikes: Florida Condominium Law Changes, 2026 Session Update', 'https://hamiltonmikes.com/legislative-updates/florida-condominium-law-changes/'),
    'fnma': ('KSN Law: Fannie Mae Updates Condominium Project Guidance (7 Eylül 2026)', 'https://www.ksnlaw.com/?p=14929'),
    'oppaga': ('OPPAGA Rapor 26-04: Milestone denetimleri (Temmuz 2026)', 'https://oppaga.fl.gov/Documents/Reports/26-04.pdf'),
}


def build_sirs():
    url = BASE + '/rehberler/kondominyum-sirs-ve-milestone/'
    stats = [
        ('30 yıl', 'Milestone denetimi', 'Üç veya daha fazla yaşanabilir katlı kondominyum binaları, 30 yaşına girdikleri yılın 31 Aralık\'ına kadar denetlenir; sonra 10 yılda bir. Yerel yönetim, tuzlu suya yakınlık gibi nedenlerle bu yaşı 25\'e indirebilir. Kaynak: ' + link(CS1['ms'][1], 'Fla. Stat. 553.899') + '.'),
        ('10 yıl', 'SIRS yenileme aralığı', 'Bina yedek akçe çalışmasının (SIRS) ilki 31 Aralık 2025\'e kadar tamamlanmalıydı; sonra en az 10 yılda bir yenilenir. Kaynak: ' + link(CS1['dbpr'][1], 'Florida DBPR') + ', ' + link(CS1['ra'][1], 'Reserve Advisors') + ' (Ocak 2026).'),
        ('7 gün', 'Alıcının cayma süresi', 'Geliştirici olmayan bir satıcıdan (ikinci el) alımda alıcının cayma süresi 1 Temmuz 2025\'te 3 günden 7 güne çıktı. Kaynak: ' + link(CS1['hb913'][1], 'Florida Senate, HB 913') + '.'),
    ]
    sections = [
        ('01', 'Kısa cevap', [
            'Florida\'da 2021\'deki Surfside çöküşünden sonra çıkarılan yasalarla, üç veya daha fazla yaşanabilir katlı kondominyum binaları iki ayrı kontrolden geçer: binanın taşıyıcı sisteminin mühendis tarafından denetlendiği <strong>milestone denetimi</strong> ve binanın büyük bileşenlerinin yenileme maliyetini hesaplayıp bunun için ne kadar yedek akçe (reserve) ayrılması gerektiğini gösteren <strong>SIRS</strong> (Structural Integrity Reserve Study).',
            'Alıcı için önemi şudur: bu iki rapor, binada yakın gelecekte yapılacak onarımları ve bunların aidata veya özel aidata (special assessment) nasıl yansıyabileceğini gösterir. İkinci el bir dairede bu belgeler satıcı tarafından size verilmek zorundadır; teklif vermeden önce isteyin ve cayma süresi içinde okuyun.',
        ], ['ms', 'hb913']),
        ('02', 'Milestone denetimi nedir?', [
            '<strong>Hangi binalar:</strong> tamamen veya kısmen kondominyum ya da kooperatif olan, üç veya daha fazla yaşanabilir katlı binalar. Üç veya daha az katlı, en fazla dört aileli konutlar kapsam dışıdır.',
            '<strong>Ne zaman:</strong> bina 30 yaşına girdiği yılın 31 Aralık\'ına kadar, sonra her 10 yılda bir. Yerel yönetim, tuzlu suya yakınlık gibi çevre koşulları nedeniyle denetimi 25. yıla çekebilir; bu yüzden sahile yakın bir binada yerel belediyenin takvimini ayrıca sorun.',
            '<strong>İki aşama:</strong> birinci aşamada (phase one) lisanslı bir mühendis veya mimar binayı gözle inceler; yerel yönetimin yazılı bildiriminden sonra 180 gün içinde tamamlanır. Ciddi yapısal bozulma görülürse ikinci aşama (phase two) gerekir. İkinci aşama raporunda belirtilen onarımlara rapor alındıktan sonra 365 gün içinde başlanmalıdır; yerel yönetim daha kısa süre belirleyebilir.',
            '<strong>Daire sahiplerine bildirim:</strong> dernek, denetçinin hazırladığı özeti bulgular ne olursa olsun raporu aldıktan sonra 45 gün içinde her daire sahibine gönderir ve binada görünür bir yere asar.',
        ], ['ms']),
        ('03', 'SIRS nedir, neleri kapsar?', [
            'SIRS, derneğin bakımından sorumlu olduğu bina bileşenlerinin kalan ömrünü ve yenileme maliyetini hesaplar ve bunun için yıllık ne kadar yedek akçe ayrılacağını belirler. Florida DBPR\'ye göre kapsam: çatı, taşıyıcı sistem, yangın yalıtımı ve yangından korunma, sıhhi tesisat, elektrik, su yalıtımı ve dış cephe boyası, pencereler ve dış kapılar, ve yapısal bütünlüğü etkileyen, yenileme maliyeti $25.000\'in (veya enflasyona göre güncellenen eşiğin) üzerindeki diğer kalemler.',
            'Çalışmayı bir Reserve Specialist (RS), Professional Reserve Analyst (PRA) ya da Florida lisanslı bir mühendis veya mimar hazırlar. Dernek, çalışma tamamlandıktan sonra 45 gün içinde DBPR\'ye bildirim formu gönderir.',
            '2025\'teki HB 913 yasasıyla: SIRS\'te nakit bakiyeyi sıfırın üzerinde tutan bir asgari finansman planı (baseline) yer alır; dernekler rezervleri havuz yöntemiyle (pooling) finanse edebilir; milestone denetimini yeni tamamlamış dernekler SIRS\'i iki bütçe yılı erteleyebilir. 2026 yasama döneminde SIRS ve milestone kurallarında değişiklik yapılmadı.',
        ], ['dbpr', 'ra', 'hb913', 'hm']),
        ('04', 'Aidat ve özel aidat neden artabilir?', [
            'SIRS\'teki kalemler için ayrılması gereken yedek akçe, derneğin yıllık bütçesine ve dolayısıyla aidata yansır. Rezervleri yetersiz bir binada eksik, özel aidat, banka kredisi veya kredi limitiyle de kapatılabilir; HB 913\'e göre bunun için oy hakkının çoğunluğunun onayı gerekir.',
            'Daire sahipleri tarafından yönetilen ve son iki yılda milestone denetimini tamamlamış dernekler, 31 Aralık 2028\'e kadar kabul edilen bütçelerde, denetimde önerilen onarımları finanse etmek için rezerv katkılarını en fazla iki yıllık bütçe boyunca durdurabilir veya azaltabilir; bu da toplam oy hakkının çoğunluğuyla olur ve sonrasında yeni bir SIRS gerekir.',
            'Bu yüzden bir dairenin aylık aidatı tek başına yeterli bir gösterge değildir: yedek akçe tutarını, planlanan onarımları ve onaylanmış ya da görüşülen özel aidatları birlikte okuyun.',
        ], ['hb913']),
        ('05', 'İkinci el dairede satıcı size hangi belgeleri vermeli?', [
            'Fla. Stat. 718.503(2)(a)\'ya göre geliştirici olmayan satıcı, masrafı kendisine ait olmak üzere şu belgeleri alıcıya verir: kondominyum beyannamesi (declaration), derneğin kuruluş belgesi, iç yönetmelik ve kurallar, yıllık mali tablo ve bütçe, varsa milestone denetim özeti, en son SIRS (ya da yapılmadığına dair beyan), 1 Temmuz 2023 ve sonrasında yapılmışsa devir denetim raporu (turnover inspection) ve "Sık Sorulan Sorular ve Cevaplar" belgesi.',
            'Bu belgeler zamanında verilmezse sözleşme alıcının tercihine göre feshedilebilir hale gelir. Belgeleri aldıktan sonraki cayma süresi 2025\'ten bu yana 7 gündür.',
            'Florida Realtors\'ın 2025 kondominyum eki (Condominium Rider), alıcının ayrıca son 12 ayın yönetim kurulu toplantı tutanaklarını, sigorta poliçe özetlerini ve kapanıştan önce gelen denetim veya rezerv raporlarını istemesine imkân verir; ancak bu talepler satıcı kabul edip sözleşmeye yazılırsa geçerlidir.',
        ], ['ksn', 'hb913']),
        ('06', 'Teklif vermeden önce kendiniz neyi kontrol edebilirsiniz?', [
            '<strong>DBPR SIRS veritabanı:</strong> Florida DBPR, derneklerin bildirdiği SIRS bilgilerini herkese açık bir listede yayınlar; bilgiler dernekçe gönderildiği şekliyle gösterilir ve yalnızca tamamlanmış bildirimler yer alır.',
            '<strong>Belediyenin yapı dairesi:</strong> milestone denetiminin durumunu, ek süre (extension) verilip verilmediğini ve onarım ruhsatlarını binanın bağlı olduğu belediyeye sorabilirsiniz.',
            '<strong>Dernek tutanakları:</strong> 25 ve daha fazla daireli dernekler, son 12 ayın tutanaklarını ve kayıtlarını internet sitesinde veya uygulamada yayınlamak zorundadır. Onarım, sigorta ve özel aidat tartışmaları genellikle önce burada görünür.',
        ], ['dbpr', 'hm', 'ksn']),
        ('07', 'Konut kredisi kullanacaksanız', [
            'Fannie Mae\'nin Ağustos 2026\'da güncellenen kondominyum kurallarına göre, zorunlu yapı denetiminden geçemeyen veya kritik onarımları tamamlanmamış projelerdeki dairelere verilen krediler Fannie Mae\'ye satılamaz; belediye binayı kullanıma uygun bulsa bile onarımlar bitene kadar bu durum sürer. Fannie Mae\'nin sisteminde "Unavailable" statüsündeki projeler de aynı şekilde uygun değildir.',
            'Kredi kuruluşları artık yalnızca zorunlu denetimleri değil, son üç yılda yapılmış her türlü yapısal veya mekanik denetim raporunu inceler. Kredi onayını beklerken zaman kaybetmemek için binanın uygunluğunu kredi uzmanınıza teklif aşamasında sordurun. Nakit alımda bu kural sizi doğrudan bağlamaz, ancak ileride daireyi satarken alıcınızın kredi bulabilmesini etkileyebilir.',
        ], ['fnma']),
        ('08', 'Rakamlarla milestone denetimleri', [
            'OPPAGA\'nın Temmuz 2026 raporuna göre (DBPR\'nin 31 Mart 2026\'ya kadar aldığı verilerle) belediyeler 2024 ve 2025\'te toplam 8.736 birinci aşama ve 1.575 ikinci aşama milestone denetiminin tamamlandığını bildirdi. Denetimlerde 2024\'te 30, 2025\'te 24 bina "unsafe" (yapısal olarak riskli) veya oturulamaz bulundu; bu binalar sekiz ilçeye dağılıyor. 1.587 ek süre verildi ve bunların yaklaşık %94\'ü kıyı ilçe ve belediyelerindeydi.',
            'Bu veriler eksiktir: DBPR 2024 için yerel yönetimlerin %71\'inden, 2025 için %64\'ünden veri alabildi.',
        ], ['oppaga']),
        ('09', 'Bir sonraki adım', [
            'Kondominyum ağırlıklı bölgelerin aidat, sigorta ve bina yaşı bilgilerini mahalle raporlarında bulabilirsiniz: ' + hood('brickell', 'Brickell') + ', ' + hood('downtown-miami', 'Downtown Miami') + ', ' + hood('edgewater', 'Edgewater') + ', ' + hood('sunny-isles', 'Sunny Isles Beach') + ', ' + hood('aventura', 'Aventura') + ', ' + hood('bal-harbour', 'Bal Harbour') + ', ' + hood('surfside', 'Surfside') + ', ' + hood('hallandale', 'Hallandale Beach') + ' ve ' + hood('fort-lauderdale', 'Fort Lauderdale') + '.',
            'Milestone denetimi 30 yıl sonra başladığı için yeni binalarda henüz gündemde değildir; teslim tarihleri ve geliştiricileriyle birlikte <a href="/yeni-projeler/">yeni projeler sayfasına</a> bakabilirsiniz. Aidatın getiriye etkisini <a href="/yatirim/">yatırım sayfasındaki hesaplayıcıyla</a> görebilirsiniz.',
        ], []),
    ]
    faq = [
        ('Milestone denetimi hangi binalarda zorunlu?', 'Tamamen veya kısmen kondominyum ya da kooperatif olan, üç veya daha fazla yaşanabilir katlı binalarda. Denetim, bina 30 yaşına girdiği yılın 31 Aralık\'ına kadar ve sonra 10 yılda bir yapılır; yerel yönetim tuzlu suya yakınlık gibi nedenlerle bu yaşı 25\'e indirebilir (Fla. Stat. 553.899).'),
        ('SIRS nedir?', 'Structural Integrity Reserve Study; derneğin bakımından sorumlu olduğu çatı, taşıyıcı sistem, yangından korunma, tesisat, elektrik, su yalıtımı, pencere ve dış kapılar gibi bileşenlerin yenileme maliyetini ve bunun için ayrılacak yıllık yedek akçeyi hesaplayan çalışmadır. İlki 31 Aralık 2025\'e kadar tamamlanmalıydı; sonra en az 10 yılda bir yenilenir.'),
        ('İkinci el daire alırken SIRS ve milestone raporlarını görebilir miyim?', 'Evet. Fla. Stat. 718.503\'e göre geliştirici olmayan satıcı, varsa milestone denetim özetini ve en son SIRS\'i (ya da yapılmadığına dair beyanı) diğer dernek belgeleriyle birlikte alıcıya vermek zorundadır. Belgeler zamanında verilmezse sözleşme alıcının tercihine göre feshedilebilir. Bu bilgi hukuk tavsiyesi değildir.'),
        ('Belgeleri aldıktan sonra sözleşmeden cayabilir miyim?', 'Geliştirici olmayan bir satıcıdan alımda alıcının cayma süresi 1 Temmuz 2025\'ten bu yana 7 gündür (önceden 3 gündü). Süre ve şartlar sözleşmenize göre değişebileceği için bir avukata danışın.'),
        ('Binada milestone sorunu varsa konut kredisi alabilir miyim?', 'Zorlaşabilir. Fannie Mae\'nin Ağustos 2026 kurallarına göre zorunlu denetimden geçemeyen veya kritik onarımları tamamlanmamış projelerdeki dairelere verilen krediler Fannie Mae\'ye satılamaz; bu durum onarımlar bitene kadar sürer. Kredi uzmanınıza binanın uygunluğunu teklif aşamasında sordurun. Bu bilgi finansman tavsiyesi değildir.'),
    ]
    return dict(
        slug='kondominyum-sirs-ve-milestone', url=url, cs=CS1,
        title='Kondominyumda SIRS ve Milestone Denetimi (2026) | Aleyna Bozoklar',
        desc='Florida\'da kondominyum alırken milestone denetimi ve SIRS: hangi binalar, ne zaman, aidata etkisi, satıcının vermesi gereken belgeler ve 7 günlük cayma süresi.',
        og='Kondominyum alırken SIRS ve milestone denetimi', headline='Florida\'da kondominyum alırken SIRS ve milestone denetimi: alıcı neyi kontrol etmeli? (2026)',
        crumb='SIRS ve milestone', tab='SIRS ve milestone',
        h1='Kondominyum alırken: <em>SIRS ve milestone denetimi</em>',
        lead='Surfside sonrası yasalar bir binanın denetimini ve yedek akçesini nasıl düzenliyor, bunlar aidata nasıl yansıyor ve ikinci el bir dairede satıcı size hangi belgeleri vermek zorunda? Her kural resmi kaynağıyla.',
        date_iso='2026-11-16', date='16 Kasım 2026', stats=stats, sections=sections, faq=faq,
        sources=list(CS1.values()), cta=('/yatirim/', 'Aidatın getiriye etkisini hesaplayın'), css=[], note=NOTE)


# ---------------------------------------------------------------- Rehber 2: okul bölgeleri
CS2 = {
    'mdcps': ('Miami-Dade County Public Schools: SchoolFinder', 'https://dadeschools.finder.schoolmint.com/about-schoolfinder'),
    'zones': ('M-DCPS Okul Kurulu: Attendance Zone Recommendations 2026-2027, Final Reading (17 Haziran 2026)', 'https://pdfs.dadeschools.net/Bdarch/2026/Bd061726/agenda/ATTENDANCE-ZONE-RECOMMENDATIONS-AND-RELATED-ADMINISTRATIVE-ACTIONS-2026-2027-FINAL-READING.pdf'),
    'bcps': ('Broward County Public Schools: Find My School', 'https://www.browardschools.com/bcps-departments/strategy-innovation/demographics-enrollment-planning/find-my-school'),
    'pbc': ('School District of Palm Beach County: Controlled Open Enrollment ve Find My Zoned School', 'https://www.palmbeachschools.org/studentsparents/school-choice/controlled-open-enrollment-coe'),
    'grades': ('Florida Department of Education: 2025-2026 okul notları duyurusu (1 Temmuz 2026)', 'https://www.fldoe.org/newsroom/latest-news/commissioner-kamoutsas-celebrates-continued-success-as-performance-improves-in-the-2025-2026-school-grades.stml'),
    'packet': ('Florida Department of Education: School Grades Results Packet 2026', 'https://www.fldoe.org/file/18534/SchoolGradesResultsPacket26.pdf'),
    'wlrn': ('WLRN: South Florida okul bölgelerinin 2025-26 notları (2 Temmuz 2026)', 'https://www.wlrn.org/light/education/2026-07-02/school-district-grades-top-south-florida-public-education-officials-celebrate-a-scores'),
    'magnet': ('M-DCPS Your Choice Miami: Magnet Application Process', 'https://yourchoicemiami.org/resources/magnet-application-process'),
    'coe': ('Florida Department of Education: Controlled Open Enrollment', 'https://www.fldoe.org/schools/school-choice/other-school-choice-options/controlled-open-enrollment.stml'),
    'sufs': ('Step Up For Students: Private School Scholarships (Şubat 2026 güncellemesi)', 'https://www.stepupforstudents.org/scholarships/private-school/'),
    'entry': ('Florida Department of Education: General Provisions and Attendance', 'https://fldoe.org/schools/k-12-public-schools/sss/military-families/general-provisions-attendance.stml'),
}


def build_schools():
    url = BASE + '/rehberler/okul-bolgeleri/'
    stats = [
        ('3 bölge', 'Üç ilçe, üç okul bölgesi', 'Miami-Dade, Broward ve Palm Beach\'te devlet okulları ilçe çapında tek bir okul bölgesine bağlıdır; üçü de 2025-26\'da eyaletten A notu aldı. Kaynak: ' + link(CS2['wlrn'][1], 'WLRN') + ' (2 Temmuz 2026).'),
        ('1 Eylül', 'Anaokulu (kindergarten) yaşı', 'Okul yılının 1 Eylül\'üne kadar 5 yaşını dolduran çocuklar devlet anaokuluna kaydolabilir. Kaynak: ' + link(CS2['entry'][1], 'Florida Department of Education') + '.'),
        ('15 Ocak', 'Magnet başvurusunun son günü', 'Miami-Dade\'de magnet programlarına başvuru 1 Ekim–15 Ocak arasında yapılır; sonuçlar 15 Mart\'ta bildirilir. Kaynak: ' + link(CS2['magnet'][1], 'M-DCPS') + '.'),
    ]
    sections = [
        ('01', 'Kısa cevap', [
            'Florida\'da her ilçe kendi okul bölgesidir: Miami-Dade County Public Schools, Broward County Public Schools ve School District of Palm Beach County. Bir adres, bu bölge içinde belirli bir ilkokula, ortaokula ve liseye bağlıdır (attendance zone veya boundary). Çocuğunuz kural olarak adresinizin bağlı olduğu okula kaydolur.',
            'Bu bağlantı kalıcı değildir; okul kurulları sınırları her yıl gözden geçirir. Bu nedenle ev alırken veya kiralarken ilandaki okul bilgisine değil, okul bölgesinin resmi adres sorgulama aracına bakın ve gerekirse bölgeden yazılı teyit isteyin. Adresin bağlı olduğu okulun dışında magnet, açık kayıt, charter ve özel okul seçenekleri de vardır.',
        ], ['zones', 'coe']),
        ('02', 'Bir adresin bağlı olduğu okulu nasıl öğrenirsiniz?', [
            '<strong>Miami-Dade:</strong> ' + link(CS2['mdcps'][1], 'M-DCPS SchoolFinder') + ' aracında adresi girerek bağlı olunan okulları ve diğer seçenekleri görebilirsiniz. Okul kurulu sınır değişikliklerini her yıl karara bağlar; 2026-27 okul yılı değişiklikleri 17 Haziran 2026 toplantısında son okumayla görüşüldü.',
            '<strong>Broward:</strong> ' + link(CS2['bcps'][1], 'Find My School') + ' aracında okul yılını, sokak adresini ve posta kodunu girersiniz. Gelecek sonbahar için kayıt yapıyorsanız bir sonraki okul yılını seçin; adres sistemde görünmüyorsa bölgenin planlama birimine boundaries@browardschools.com adresinden yazabilirsiniz.',
            '<strong>Palm Beach:</strong> bölgenin sitesindeki "Find My Zoned School" haritası ve okul sınırı haritaları kullanılır (' + link(CS2['pbc'][1], 'School District of Palm Beach County') + ').',
            'Aynı apartmanın veya sokağın iki yakası farklı okullara bağlı olabilir. Sözleşme imzalamadan önce tam adresle sorgulayın.',
        ], ['mdcps', 'zones', 'bcps', 'pbc']),
        ('03', 'Okul notları nereden bakılır?', [
            'Florida Department of Education (FLDOE), her yaz devlet okullarına A\'dan F\'ye bir not verir. 2025-26 notları 1 Temmuz 2026\'da açıklandı; FLDOE\'ye göre eyalet genelinde okulların %76\'sı (2.614 okul) A veya B aldı. Okul bazında notlar FLDOE\'nin sonuç dosyasında yer alır.',
            'Not, öncelikle sınav başarısı ve ilerlemesine dayanır; program çeşitliliği, ulaşım, okul büyüklüğü veya çocuğunuzun ihtiyaçları gibi konuları göstermez. Okulu ziyaret etmek ve okul bölgesiyle doğrudan görüşmek en sağlıklı yoldur.',
        ], ['grades', 'packet']),
        ('04', 'Adresinizin okulu dışındaki seçenekler', [
            '<strong>Magnet programları:</strong> Miami-Dade\'de sanat, bilim, dil, mühendislik gibi alanlara odaklanan programlardır. Başvuru 1 Ekim–15 Ocak (gece 23.59) arasında yapılır, en fazla 5 okul seçilir (okul başına bir program). Seçim, programın kriterlerine göre bağımsız bir bilgisayar sistemiyle rastgele yapılır; seçmeler ve dil sınavları 1 Mart\'tan önce tamamlanır, sonuçlar 15 Mart\'ta e-postayla bildirilir. Dönem dışı başvurular 15 Nisan–1 Eylül arasındadır.',
            '<strong>Kontrollü açık kayıt (Controlled Open Enrollment):</strong> Florida\'da her okul bölgesi ve charter okul, kapasitesi olan okullara başka bölgelerden de başvuru kabul etmek zorundadır. Ulaşım aileye aittir; bölgede oturan öğrenciler ve askerî aileler gibi bazı gruplar öncelik alır. Başvuru tarihleri her bölgenin kendi sitesinde yayınlanır.',
            '<strong>Charter okullar:</strong> bağımsız yönetilen devlet okullarıdır ve eyaletten not alırlar; kayıt her okulun kendi başvuru takvimine göre yapılır.',
            '<strong>Özel okul bursları:</strong> Florida\'da ikamet eden ve devlet okuluna kayıt hakkı olan öğrenciler, hane gelirinden bağımsız olarak Florida Tax Credit (FTC) veya Family Empowerment Scholarship (FES-EO) bursuna başvurabilir. Step Up For Students\'a göre burs ortalama $8.000 civarındadır; öncelik sırası yenileyen öğrenciler, ardından gelir düzeyine göre belirlenir (Şubat 2026 güncellemesi).',
        ], ['magnet', 'coe', 'grades', 'sufs']),
        ('05', 'Kayıt için gerekenler', [
            '<strong>Yaş:</strong> okul yılının 1 Eylül\'üne kadar 5 yaşını dolduran çocuk anaokuluna kaydolabilir. 1 Şubat\'a kadar 6 yaşını dolduran çocuklar için okula devam zorunludur.',
            '<strong>Sağlık belgeleri:</strong> tüm aşıların tamamlandığını gösteren Florida aşı sertifikası (Florida\'daki sağlık kuruluşlarından alınır) ve okula başlamadan önceki bir yıl içinde yapılmış, hekim imzalı sağlık muayenesi belgesi. Türkiye\'den getirdiğiniz aşı kartı, Florida formuna bir sağlık kuruluşu tarafından aktarılmalıdır.',
            '<strong>Adres belgesi:</strong> okul bölgeleri, adresin bağlı olduğu okula kayıt için ikamet belgesi ister (ör. tapu veya kira sözleşmesi ve fatura). Tam liste bölgeye göre değişir; kaydı yapacağınız okul bölgesinin kayıt sayfasına bakın.',
        ], ['entry']),
        ('06', 'Ev alırken veya kiralarken pratik notlar', [
            'Taşınma tarihinizi başvuru takvimine göre planlayın: Miami-Dade\'de bir sonraki ağustos için magnet başvurusu bir önceki ekim–ocak döneminde yapılır.',
            'Okul sınırları yıllık değişebildiği için, bir evin bugün bağlı olduğu okulun ileride değişmeyeceğinin garantisi yoktur. Teyidi her zaman okul bölgesinden alın.',
            'Bu sitede mahalleler okul notlarına göre sıralanmaz veya önerilmez; mahalle raporlarında her bölge için ilgili okul bölgesinin resmi sitesine bağlantı verilir.',
        ], ['zones']),
        ('07', 'Bir sonraki adım', [
            'Her bölgenin karakterini, fiyat ve kira düzeyini ve bağlı olduğu okul bölgesinin resmi bağlantısını 121 bölgenin <a href="/mahalle-raporlari/">mahalle raporlarında</a> bulabilirsiniz; örneğin Miami-Dade\'den ' + hood('doral', 'Doral') + ' ve ' + hood('coral-gables', 'Coral Gables') + ', Broward\'dan ' + hood('weston', 'Weston') + ' ve ' + hood('fort-lauderdale', 'Fort Lauderdale') + ', Palm Beach\'ten ' + hood('boca-raton', 'Boca Raton') + ' ve ' + hood('west-palm-beach', 'West Palm Beach') + '.',
            'Hangi bölgelerin ihtiyaçlarınıza uyduğunu görmek için <a href="/mahalle-testi/">mahalle testini</a> yapabilir, kriterlerinize uyan ilanları <a href="/ilanlar/">ilan talep sayfasından</a> isteyebilirsiniz.',
        ], []),
    ]
    faq = [
        ('Miami\'de çocuğum hangi okula gider?', 'Kural olarak adresinizin bağlı olduğu (zoned) devlet okuluna. Miami-Dade\'de M-DCPS SchoolFinder, Broward\'da Find My School, Palm Beach\'te Find My Zoned School aracıyla adresinizi sorgulayabilirsiniz. Sınırlar her yıl değişebildiği için okul bölgesinden teyit alın.'),
        ('Adresimin bağlı olduğu okul dışında bir okula gidebilir mi?', 'Evet, birkaç yolla: magnet programları (Miami-Dade\'de başvuru 1 Ekim–15 Ocak), kapasitesi olan okullara kontrollü açık kayıt (ulaşım aileye ait), charter okullar ve özel okullar. Florida\'da ikamet eden öğrenciler gelirden bağımsız olarak özel okul bursuna da başvurabilir.'),
        ('Okul notlarına nereden bakabilirim?', 'Florida Department of Education her yaz devlet okullarına A–F arası not verir; 2025-26 notları 1 Temmuz 2026\'da açıklandı. Okul bazında notlar FLDOE\'nin sitesindeki sonuç dosyasında yer alır.'),
        ('Anaokuluna kayıt yaşı nedir?', 'Okul yılının 1 Eylül\'üne kadar 5 yaşını dolduran çocuklar devlet anaokuluna kaydolabilir. Kayıt için Florida aşı sertifikası ve okula başlamadan önceki bir yıl içinde yapılmış sağlık muayenesi belgesi gerekir.'),
        ('Türkiye\'den gelen bir öğrenci için ne gerekir?', 'Adres belgesi, Florida aşı sertifikası ve son bir yıl içindeki sağlık muayenesi belgesi temel şartlardır; Türkiye\'deki aşı kayıtlarının bir Florida sağlık kuruluşunca Florida formuna aktarılması gerekir. Diğer belgeler (doğum belgesi, önceki okul kayıtları gibi) okul bölgesine göre değişir; kayıt sayfasına bakın.'),
    ]
    return dict(
        slug='okul-bolgeleri', url=url, cs=CS2,
        title='Miami\'de Okul Bölgeleri Nasıl Çalışır? (2026) | Aleyna Bozoklar',
        desc='Miami-Dade, Broward ve Palm Beach\'te adresin bağlı olduğu okul nasıl öğrenilir, okul notları, magnet ve açık kayıt, özel okul bursu ve kayıt belgeleri.',
        og='Miami\'de okul bölgeleri nasıl çalışır?', headline='Miami\'de okul bölgeleri nasıl çalışır? Adres sorgulama, magnet, açık kayıt ve kayıt belgeleri (2026)',
        crumb='Okul bölgeleri', tab='Okul bölgeleri',
        h1='Miami\'de okul bölgeleri <em>nasıl çalışır?</em>',
        lead='Bir adresin bağlı olduğu okulu nasıl öğrenirsiniz, okul notlarına nereden bakarsınız, magnet ve açık kayıt başvuruları ne zaman yapılır ve kayıt için hangi belgeler gerekir? Her bilgi resmi kaynağıyla.',
        date_iso='2026-11-16', date='16 Kasım 2026', stats=stats, sections=sections, faq=faq,
        sources=list(CS2.values()), cta=('/mahalle-raporlari/', 'Mahalle raporlarına bakın'), css=[], note=NOTE_SCHOOL)


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
    guides = [build_sirs(), build_schools()]
    tabs = TABS + [('/rehberler/' + g['slug'] + '/', g['tab']) for g in guides]
    for g in guides:
        render(g, tpl, tabs)
        print('ok', g['slug'])
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'stamp_assets.py')], check=True)


if __name__ == '__main__':
    main()
