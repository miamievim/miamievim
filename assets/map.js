(function () {
  'use strict';

  var HOODS = [
    { id: 'coral-gables', name: 'Coral Gables', county: 'Miami-Dade', lat: 25.7215, lng: -80.2684, line: 'Ağaçlıklı sokaklar, yürünebilir bir merkez ve Akdeniz tarzı evler.' },
    { id: 'coconut-grove', name: 'Coconut Grove', county: 'Miami-Dade', lat: 25.7280, lng: -80.2430, line: 'Miami’nin en eski mahallesi: marinalar, körfez parkları ve köy sakinliği.' },
    { id: 'pinecrest', name: 'South Miami & Pinecrest', county: 'Miami-Dade', lat: 25.6680, lng: -80.3020, line: 'Geniş arsalar ve bahçeli müstakil evler.' },
    { id: 'key-biscayne', name: 'Key Biscayne', county: 'Miami-Dade', lat: 25.6930, lng: -80.1626, line: 'Şehir merkezine tek bir köprüyle bağlı ada hayatı.' },
    { id: 'south-beach', name: 'South Beach', county: 'Miami-Dade', lat: 25.7826, lng: -80.1341, line: 'Art Deco binalar, plaj ve Ocean Drive’ın enerjisi.' },
    { id: 'wynwood', name: 'Wynwood & Design District', county: 'Miami-Dade', lat: 25.8060, lng: -80.1960, line: 'Duvar resimleri, galeriler ve lüks butikler.' },
    { id: 'brickell', name: 'Brickell', county: 'Miami-Dade', lat: 25.7617, lng: -80.1918, line: 'Miami’nin finans merkezi; arabasız yaşamın gerçekten mümkün olduğu yer.' },
    { id: 'edgewater', name: 'Downtown & Edgewater', county: 'Miami-Dade', lat: 25.7930, lng: -80.1880, line: 'Biscayne Körfezi’nde en hızlı değişen silüet.' },
    { id: 'little-havana', name: 'Little Havana', county: 'Miami-Dade', lat: 25.7656, lng: -80.2190, line: 'Calle Ocho ve Miami’nin Latin kalbi.' },
    { id: 'doral', name: 'Doral', county: 'Miami-Dade', lat: 25.8195, lng: -80.3553, line: 'Yeni yapılar, golf sahaları ve havalimanına hızlı erişim.' },
    { id: 'north-beach', name: 'Mid-Beach & North Beach', county: 'Miami-Dade', lat: 25.8450, lng: -80.1205, line: 'Miami Beach’in daha sakin yüzü.' },
    { id: 'bal-harbour', name: 'Surfside & Bal Harbour', county: 'Miami-Dade', lat: 25.8840, lng: -80.1220, line: 'Sakin sahil sokakları ve Bal Harbour Shops.' },
    { id: 'sunny-isles', name: 'Sunny Isles Beach', county: 'Miami-Dade', lat: 25.9420, lng: -80.1220, line: 'Okyanus kıyısında kuleler ve markalı rezidanslar.' },
    { id: 'aventura', name: 'Aventura', county: 'Miami-Dade', lat: 25.9480, lng: -80.1400, line: 'Alışveriş, marinalar ve Intracoastal kıyısında yüksek katlı yaşam.' },
    { id: 'hallandale', name: 'Hallandale Beach', county: 'Broward', lat: 25.9812, lng: -80.1484, line: 'Miami’ye yakın, Broward fiyatlarında.' },
    { id: 'hollywood', name: 'Hollywood', county: 'Broward', lat: 26.0112, lng: -80.1300, line: 'Broadwalk boyunca bisikletle sahil hayatı.' },
    { id: 'weston', name: 'Weston', county: 'Broward', lat: 26.1004, lng: -80.3998, line: 'Göller, geniş evler ve sakin sokaklarla planlı bir şehir.' },
    { id: 'fort-lauderdale', name: 'Fort Lauderdale', county: 'Broward', lat: 26.1194, lng: -80.1300, line: 'Las Olas, Victoria Park ve kanal kenarında yaşam.' },
    { id: 'wilton-manors', name: 'Wilton Manors', county: 'Broward', lat: 26.1604, lng: -80.1389, line: 'Fort Lauderdale’e dakikalar mesafede renkli, küçük bir şehir.' },
    { id: 'pompano', name: 'Lighthouse Point & Pompano', county: 'Broward', lat: 26.2600, lng: -80.0990, line: 'Derin su kanalları ve tekne sahipleri için tasarlanmış evler.' },
    { id: 'deerfield', name: 'Deerfield Beach', county: 'Broward', lat: 26.3184, lng: -80.0998, line: 'İki büyük şehrin arasında sahil kasabası hissi.' },
    { id: 'boca-raton', name: 'Boca Raton', county: 'Palm Beach', lat: 26.3587, lng: -80.0900, line: 'Golf sahaları, plajlar ve bakımlı bir şehir merkezi.' },
    { id: 'pembroke-pines', name: 'Pembroke Pines', county: 'Broward', lat: 26.0128, lng: -80.3382, line: 'Göller etrafında planlı siteler ve geniş müstakil evler.' },
    { id: 'miramar', name: 'Miramar', county: 'Broward', lat: 25.9773, lng: -80.2722, line: 'Kurumsal ofisler, yeni siteler ve Miami\'ye kısa mesafe.' },
    { id: 'davie', name: 'Davie', county: 'Broward', lat: 26.0629, lng: -80.2331, line: 'At çiftlikleri, geniş arsalar ve üniversite kampüsleri.' },
    { id: 'plantation', name: 'Plantation', county: 'Broward', lat: 26.1276, lng: -80.2331, line: 'Ağaçlı sokaklar, kanallar ve olgun müstakil ev mahalleleri.' },
    { id: 'sunrise', name: 'Sunrise', county: 'Broward', lat: 26.1570, lng: -80.2864, line: 'Sawgrass Mills, hokey arenası ve uygun fiyatlı kondominyumlar.' },
    { id: 'coral-springs', name: 'Coral Springs', county: 'Broward', lat: 26.2712, lng: -80.2706, line: 'Planlı şehir: parklar, spor tesisleri ve bakımlı mahalleler.' },
    { id: 'coconut-creek', name: 'Coconut Creek', county: 'Broward', lat: 26.2517, lng: -80.1789, line: 'Yeşil alanlar, kelebek bahçesi ve uygun fiyatlı siteler.' },
    { id: 'cooper-city', name: 'Cooper City', county: 'Broward', lat: 26.0573, lng: -80.2717, line: 'Küçük, sakin ve müstakil ev ağırlıklı bir banliyö.' },
    { id: 'margate', name: 'Margate', county: 'Broward', lat: 26.2445, lng: -80.2064, line: 'Uygun fiyatlı villa ve kondominyum siteleri.' },
    { id: 'parkland', name: 'Parkland', county: 'Broward', lat: 26.3101, lng: -80.2373, line: 'Geniş arsalar, yeni lüks siteler ve doğa alanları.' },
    { id: 'tamarac', name: 'Tamarac', county: 'Broward', lat: 26.2129, lng: -80.2498, line: 'Golf çevresi siteler ve uygun fiyatlı villalar.' },
    { id: 'dania-beach', name: 'Dania Beach', county: 'Broward', lat: 26.0523, lng: -80.1439, line: 'Broward\'ın en eski şehri: plaj, iskele ve havalimanına komşu.' },
    { id: 'hillsboro-beach', name: 'Hillsboro Beach', county: 'Broward', lat: 26.2909, lng: -80.0783, line: 'Okyanus ile Intracoastal arasında dar, sakin bir sahil şeridi.' },
    { id: 'lauderdale-by-the-sea', name: 'Lauderdale-by-the-Sea', county: 'Broward', lat: 26.1920, lng: -80.0965, line: 'Alçak katlı yapılar, iskele ve kıyıdan dalış.' },
    { id: 'lauderdale-lakes', name: 'Lauderdale Lakes', county: 'Broward', lat: 26.1665, lng: -80.2084, line: 'Göllerle çevrili, uygun fiyatlı merkezi bir şehir.' },
    { id: 'lauderhill', name: 'Lauderhill', county: 'Broward', lat: 26.1404, lng: -80.2134, line: 'Kriket stadyumu, sanat merkezi ve uygun fiyatlı konut.' },
    { id: 'north-lauderdale', name: 'North Lauderdale', county: 'Broward', lat: 26.2173, lng: -80.2259, line: 'Küçük, konut ağırlıklı ve uygun fiyatlı.' },
    { id: 'oakland-park', name: 'Oakland Park', county: 'Broward', lat: 26.1723, lng: -80.1320, line: 'Mutfak bölgesi, bira fabrikaları ve plaja yakın konum.' },
    { id: 'pembroke-park', name: 'Pembroke Park', county: 'Broward', lat: 25.9887, lng: -80.1747, line: 'Küçük, ticari ağırlıklı ve Hallandale\'e komşu.' },
    { id: 'sea-ranch-lakes', name: 'Sea Ranch Lakes', county: 'Broward', lat: 26.2001, lng: -80.0966, line: 'Okyanus kıyısında kapılı küçük bir köy.' },
    { id: 'southwest-ranches', name: 'Southwest Ranches', county: 'Broward', lat: 26.0587, lng: -80.3373, line: 'Büyük arsalı çiftlik evleri ve binicilik.' },
    { id: 'west-park', name: 'West Park', county: 'Broward', lat: 25.9845, lng: -80.1987, line: 'Küçük, konut ağırlıklı ve Miami-Dade sınırında.' },
    { id: 'north-miami', name: 'North Miami', county: 'Miami-Dade', lat: 25.8901, lng: -80.1867, line: 'Çağdaş sanat müzesi, körfez kıyısı ve gelişen karma projeler.' },
    { id: 'north-miami-beach', name: 'North Miami Beach', county: 'Miami-Dade', lat: 25.9331, lng: -80.1625, line: 'Tarihî manastır, Intracoastal kıyısı ve uygun fiyatlı kondominyumlar.' },
    { id: 'miami-shores', name: 'Miami Shores', county: 'Miami-Dade', lat: 25.8631, lng: -80.1928, line: 'Ağaçlı sokaklar, tarihî evler ve küçük bir köy merkezi.' },
    { id: 'bay-harbor-islands', name: 'Bay Harbor Islands', county: 'Miami-Dade', lat: 25.8876, lng: -80.1311, line: 'Körfezde iki ada: butik binalar ve yürünebilir bir merkez.' },
    { id: 'miami-gardens', name: 'Miami Gardens', county: 'Miami-Dade', lat: 25.9420, lng: -80.2456, line: 'Hard Rock Stadium, üniversiteler ve müstakil ev mahalleleri.' },
    { id: 'north-bay-village', name: 'North Bay Village', county: 'Miami-Dade', lat: 25.8463, lng: -80.1541, line: '79th Street Causeway üzerinde üç ada ve körfez manzarası.' },
    { id: 'biscayne-park', name: 'Biscayne Park', county: 'Miami-Dade', lat: 25.8823, lng: -80.1809, line: 'Ağaç gölgesinde müstakil evlerden oluşan küçük bir köy.' },
    { id: 'el-portal', name: 'El Portal', county: 'Miami-Dade', lat: 25.8554, lng: -80.1934, line: 'Little River kıyısında küçük, tarihî bir köy.' },
    { id: 'florida-city', name: 'Florida City', county: 'Miami-Dade', lat: 25.4479, lng: -80.4795, line: 'Everglades ve Keys yolunun başlangıcı; uygun fiyatlı yeni evler.' },
    { id: 'golden-beach', name: 'Golden Beach', county: 'Miami-Dade', lat: 25.9654, lng: -80.1203, line: 'Okyanus cepheli malikâneler ve özel plaj.' },
    { id: 'opa-locka', name: 'Opa-locka', county: 'Miami-Dade', lat: 25.9023, lng: -80.2503, line: 'Mağribi mimarisiyle tarihî bir şehir; uygun fiyatlı konut.' },
    { id: 'sweetwater', name: 'Sweetwater', county: 'Miami-Dade', lat: 25.7631, lng: -80.3731, line: 'FIU kampüsü ve Dolphin Mall\'a komşu küçük bir şehir.' },
    { id: 'virginia-gardens', name: 'Virginia Gardens', county: 'Miami-Dade', lat: 25.8101, lng: -80.3017, line: 'Havalimanına komşu küçük bir köy.' },
    { id: 'west-miami', name: 'West Miami', county: 'Miami-Dade', lat: 25.7587, lng: -80.2970, line: 'Coral Gables\'a komşu, müstakil evlerden oluşan küçük bir şehir.' },
    { id: 'medley', name: 'Medley', county: 'Miami-Dade', lat: 25.8406, lng: -80.3265, line: 'Sanayi ve lojistik ağırlıklı, çok az konutlu bir kasaba.' },
    { id: 'indian-creek', name: 'Indian Creek', county: 'Miami-Dade', lat: 25.8762, lng: -80.1351, line: 'Körfezde özel bir ada: birkaç düzine malikâne ve golf kulübü.' },
    { id: 'fisher-island', name: 'Fisher Island', county: 'Miami-Dade', lat: 25.7605, lng: -80.1428, line: 'Yalnızca feribotla ulaşılan özel ada.' },
    { id: 'upper-east-side', name: 'Upper East Side', county: 'Miami-Dade', lat: 25.8300, lng: -80.1840, line: 'MiMo mimarisi, tarihî körfez mahalleleri ve restoranlar.' },
    { id: 'hialeah', name: 'Hialeah', county: 'Miami-Dade', lat: 25.8576, lng: -80.2781, line: 'Florida\'nın en kalabalık şehirlerinden biri; tarihî hipodrom.' },
    { id: 'miami-lakes', name: 'Miami Lakes', county: 'Miami-Dade', lat: 25.9087, lng: -80.3087, line: 'Göller etrafında planlanmış, bakımlı bir kasaba.' },
    { id: 'miami-springs', name: 'Miami Springs', county: 'Miami-Dade', lat: 25.8223, lng: -80.2895, line: 'Pueblo tarzı tarihî evler ve havalimanına komşu golf sahası.' },
    { id: 'cutler-bay', name: 'Cutler Bay', county: 'Miami-Dade', lat: 25.5808, lng: -80.3468, line: 'Körfez kıyısı, marina ve uygun fiyatlı müstakil evler.' },
    { id: 'hialeah-gardens', name: 'Hialeah Gardens', county: 'Miami-Dade', lat: 25.8651, lng: -80.3245, line: 'Hialeah\'ın batısında, sakin ve konut ağırlıklı.' },
    { id: 'palmetto-bay', name: 'Palmetto Bay', county: 'Miami-Dade', lat: 25.6217, lng: -80.3248, line: 'Geniş arsalar, körfez kıyısında tarihî malikâneler.' },
    { id: 'kendall', name: 'Kendall', county: 'Miami-Dade', lat: 25.6793, lng: -80.3173, line: 'Dadeland, hastaneler ve geniş banliyö mahalleleri.' },
    { id: 'homestead', name: 'Homestead', county: 'Miami-Dade', lat: 25.4687, lng: -80.4776, line: 'İki ulusal parkın kapısı; uygun fiyatlı yeni evler.' },
    { id: 'west-palm-beach', name: 'West Palm Beach', county: 'Palm Beach', lat: 26.7153, lng: -80.0534, line: 'Intracoastal kıyısında şehir merkezi, Brightline ve kültür odakları.' },
    { id: 'palm-beach', name: 'Palm Beach', county: 'Palm Beach', lat: 26.7056, lng: -80.0364, line: 'Worth Avenue, okyanus kıyısı malikâneler ve tarihî oteller.' },
    { id: 'palm-beach-gardens', name: 'Palm Beach Gardens', county: 'Palm Beach', lat: 26.8234, lng: -80.1387, line: 'Golf toplulukları, Gardens Mall ve planlı siteler.' },
    { id: 'jupiter', name: 'Jupiter', county: 'Palm Beach', lat: 26.9342, lng: -80.0942, line: 'Deniz feneri, Loxahatchee Nehri ve tekne kültürü.' },
    { id: 'delray-beach', name: 'Delray Beach', county: 'Palm Beach', lat: 26.4615, lng: -80.0728, line: 'Atlantic Avenue, plaj ve canlı bir kasaba merkezi.' },
    { id: 'boynton-beach', name: 'Boynton Beach', county: 'Palm Beach', lat: 26.5318, lng: -80.0905, line: 'Marina, Intracoastal kıyısı ve geniş banliyö siteleri.' },
    { id: 'wellington', name: 'Wellington', county: 'Palm Beach', lat: 26.6618, lng: -80.2684, line: 'Binicilik, polo ve geniş arsalı evler.' },
    { id: 'lake-worth-beach', name: 'Lake Worth Beach', county: 'Palm Beach', lat: 26.6168, lng: -80.0684, line: 'Sanatçı kasabası, tarihî evler ve okyanus kıyısı casino.' },
    { id: 'royal-palm-beach', name: 'Royal Palm Beach', county: 'Palm Beach', lat: 26.7084, lng: -80.2306, line: 'Göller, parklar ve müstakil evlerden oluşan sakin bir köy.' },
    { id: 'greenacres', name: 'Greenacres', county: 'Palm Beach', lat: 26.6276, lng: -80.1354, line: 'Uygun fiyatlı kondominyumlar ve merkezi konum.' },
    { id: 'riviera-beach', name: 'Riviera Beach', county: 'Palm Beach', lat: 26.7753, lng: -80.0581, line: 'Singer Island, Port of Palm Beach ve marinalar.' },
    { id: 'north-palm-beach', name: 'North Palm Beach', county: 'Palm Beach', lat: 26.8176, lng: -80.0820, line: 'Kanal evleri, country club ve sakin bir köy.' },
    { id: 'tequesta', name: 'Tequesta', county: 'Palm Beach', lat: 26.9634, lng: -80.1000, line: 'Loxahatchee Nehri kıyısında küçük bir köy.' },
    { id: 'juno-beach', name: 'Juno Beach', county: 'Palm Beach', lat: 26.8798, lng: -80.0534, line: 'İskele, kaplumbağa merkezi ve okyanus kıyısı kondominyumlar.' },
    { id: 'highland-beach', name: 'Highland Beach', county: 'Palm Beach', lat: 26.3995, lng: -80.0656, line: 'Okyanus ile Intracoastal arasında ince bir kondominyum şeridi.' },
    { id: 'lantana', name: 'Lantana', county: 'Palm Beach', lat: 26.5867, lng: -80.0517, line: 'Intracoastal kıyısında küçük bir kasaba ve halk plajı.' },
    { id: 'lake-park', name: 'Lake Park', county: 'Palm Beach', lat: 26.8000, lng: -80.0664, line: 'Marina, Park Avenue ve küçük bir kasaba merkezi.' },
    { id: 'palm-springs', name: 'Palm Springs', county: 'Palm Beach', lat: 26.6359, lng: -80.0961, line: 'Merkezi konumda uygun fiyatlı bir köy.' },
    { id: 'belle-glade', name: 'Belle Glade', county: 'Palm Beach', lat: 26.6845, lng: -80.6676, line: 'Okeechobee Gölü kıyısında tarım şehri.' },
    { id: 'pahokee', name: 'Pahokee', county: 'Palm Beach', lat: 26.8201, lng: -80.6653, line: 'Okeechobee Gölü kıyısında küçük bir kasaba ve marina.' },
    { id: 'ocean-ridge', name: 'Ocean Ridge', county: 'Palm Beach', lat: 26.5270, lng: -80.0484, line: 'Okyanus ile Intracoastal arasında sakin bir ada kasabası.' },
    { id: 'gulf-stream', name: 'Gulf Stream', county: 'Palm Beach', lat: 26.4887, lng: -80.0598, line: 'Mizner mimarisi ve golf kulübüyle küçük bir kıyı kasabası.' },
    { id: 'hypoluxo', name: 'Hypoluxo', county: 'Palm Beach', lat: 26.5662, lng: -80.0534, line: 'Intracoastal kıyısında küçük bir kasaba.' },
    { id: 'manalapan', name: 'Manalapan', county: 'Palm Beach', lat: 26.5687, lng: -80.0412, line: 'Okyanustan Intracoastal\'a uzanan malikâneler.' },
    { id: 'south-palm-beach', name: 'South Palm Beach', county: 'Palm Beach', lat: 26.5887, lng: -80.0387, line: 'A1A boyunca okyanus kıyısı kondominyumlar.' },
    { id: 'palm-beach-shores', name: 'Palm Beach Shores', county: 'Palm Beach', lat: 26.7787, lng: -80.0356, line: 'Singer Island\'ın güney ucunda küçük bir kasaba.' },
    { id: 'lake-clarke-shores', name: 'Lake Clarke Shores', county: 'Palm Beach', lat: 26.6454, lng: -80.0759, line: 'Lake Osborne kıyısında müstakil evlerden oluşan bir kasaba.' },
    { id: 'westlake', name: 'Westlake', county: 'Palm Beach', lat: 26.7480, lng: -80.3200, line: 'Sıfırdan kurulan yeni bir şehir ve yeni evler.' },
    { id: 'loxahatchee-groves', name: 'Loxahatchee Groves', county: 'Palm Beach', lat: 26.6837, lng: -80.2800, line: 'Geniş arsalar, çiftlikler ve kırsal yaşam.' },
    { id: 'atlantis', name: 'Atlantis', county: 'Palm Beach', lat: 26.5934, lng: -80.1009, line: 'Golf sahası etrafında kurulmuş küçük bir şehir.' },
    { id: 'jupiter-inlet-colony', name: 'Jupiter Inlet Colony', county: 'Palm Beach', lat: 26.9473, lng: -80.0745, line: 'Jupiter Inlet\'in güneyinde çok küçük bir kıyı kasabası.' },
    { id: 'haverhill', name: 'Haverhill', county: 'Palm Beach', lat: 26.6912, lng: -80.1206, line: 'West Palm Beach\'in batısında geniş arsalı küçük bir kasaba.' },
    { id: 'mangonia-park', name: 'Mangonia Park', county: 'Palm Beach', lat: 26.7600, lng: -80.0740, line: 'Tri-Rail istasyonu ve sanayi alanlarıyla küçük bir kasaba.' },
    { id: 'briny-breezes', name: 'Briny Breezes', county: 'Palm Beach', lat: 26.5076, lng: -80.0509, line: 'Okyanus kıyısında mobil ev topluluğu olan bir kasaba.' },
    { id: 'south-bay', name: 'South Bay', county: 'Palm Beach', lat: 26.6637, lng: -80.7162, line: 'Okeechobee Gölü\'nün güneyinde küçük bir tarım şehri.' },
    { id: 'golf', name: 'Golf', county: 'Palm Beach', lat: 26.5040, lng: -80.1070, line: 'Golf kulübü etrafında kurulmuş çok küçük bir köy.' },
    { id: 'cloud-lake', name: 'Cloud Lake', county: 'Palm Beach', lat: 26.6762, lng: -80.0739, line: 'Belediye vergisi olmayan çok küçük bir kasaba.' },
    { id: 'glen-ridge', name: 'Glen Ridge', county: 'Palm Beach', lat: 26.6720, lng: -80.0723, line: 'Belediye vergisi olmayan çok küçük bir kasaba.' }
  ];

  // Approximate county lines (east-west) and extents for the overlay.
  var PB_BR = 26.3220;   // Palm Beach / Broward
  var BR_MD = 25.9567;   // Broward / Miami-Dade (County Line Rd)
  var WEST = -80.90, EAST_LAND = -80.06, EAST = -79.90;
  var COUNTY_BOUNDS = {
    'Palm Beach': [[-80.72, 26.30], [-80.02, 26.98]],
    'Broward': [[-80.46, 25.94], [-80.05, 26.34]],
    'Miami-Dade': [[-80.52, 25.42], [-80.08, 25.98]],
    'All': [[-80.72, 25.42], [-79.98, 26.98]]
  };

  var state = { selected: 'brickell', county: 'All' };
  var map = null;
  var markers = {};
  var countyLabels = {};

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function byId(id) { for (var i = 0; i < HOODS.length; i++) { if (HOODS[i].id === id) return HOODS[i]; } return null; }

  function renderCard(h) {
    var card = $('#hood-card');
    if (!card) return;
    $('.county', card).textContent = h.county; $('.county', card).setAttribute('lang', 'en');
    $('h3', card).textContent = h.name;
    $('p', card).textContent = h.line;
    var r = document.getElementById('card-report'); if (r) r.href = '/mahalle-raporlari/' + h.id + '/';
    var sr = document.getElementById('card-search'); if (sr) sr.href = '/ilanlar/?q=' + encodeURIComponent(h.name);
  }

  function updateMarkers() {
    HOODS.forEach(function (h) {
      var el = markers[h.id] && markers[h.id].getElement();
      if (!el) return;
      el.classList.toggle('on', h.id === state.selected);
      el.classList.toggle('dim', state.county !== 'All' && h.county !== state.county);
      el.setAttribute('aria-pressed', h.id === state.selected ? 'true' : 'false');
    });
    $all('.chip[data-hood]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-hood') === state.selected ? 'true' : 'false');
    });
    $all('.counties button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-county') === state.county ? 'true' : 'false');
    });
    Object.keys(countyLabels).forEach(function (c) {
      countyLabels[c].getElement().classList.toggle('on', c === state.county);
    });
    if (map && map.getLayer('county-shade')) {
      map.setPaintProperty('county-shade', 'fill-opacity', [
        'case', ['any', ['==', state.county, 'All'], ['==', ['get', 'county'], state.county]], 0, 0.55
      ]);
    }
  }

  function select(id, fly) {
    var h = byId(id);
    if (!h) return;
    state.selected = id;
    renderCard(h);
    updateMarkers();
    if (map && fly !== false) {
      var wide = window.matchMedia('(min-width: 901px)').matches;
      map.flyTo({ center: [h.lng, h.lat], zoom: Math.max(map.getZoom(), 12), offset: wide ? [-150, 0] : [0, 0], speed: 1.2 });
    }
  }

  function setCounty(c) {
    state.county = c;
    updateMarkers();
    if (svgEl) { fitSvg(COUNTY_BOUNDS[c]); return; }
    if (map) {
      var wide = window.matchMedia('(min-width: 901px)').matches;
      map.fitBounds(COUNTY_BOUNDS[c], { padding: wide ? { top: 140, bottom: 110, left: 60, right: 440 } : 30, duration: 1100 });
    }
  }

  function countyGeo() {
    function box(name, s, n) {
      return { type: 'Feature', properties: { county: name }, geometry: { type: 'Polygon', coordinates: [[[WEST, s], [EAST, s], [EAST, n], [WEST, n], [WEST, s]]] } };
    }
    return {
      shade: { type: 'FeatureCollection', features: [box('Palm Beach', PB_BR, 27.0), box('Broward', BR_MD, PB_BR), box('Miami-Dade', 25.0, BR_MD)] },
      lines: { type: 'FeatureCollection', features: [
        { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: [[WEST, PB_BR], [EAST_LAND, PB_BR]] } },
        { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: [[WEST, BR_MD], [-80.115, BR_MD]] } }
      ] }
    };
  }


  // ---- Şematik yedek harita (MapLibre veya harita karoları yüklenemezse) ----
  var SVGNS = 'http://www.w3.org/2000/svg';
  var K = Math.cos(26 * Math.PI / 180);
  function px(lng) { return (lng + 80.55) * K * 1000; }
  function py(lat) { return (26.47 - lat) * 1000; }
  function pts(arr) { return arr.map(function (p) { return px(p[1]).toFixed(1) + ',' + py(p[0]).toFixed(1); }).join(' '); }
  var svgEl = null;
  var LAND = [[27.6, -80.12], [26.98, -80.07], [26.94, -80.075], [26.85, -80.04], [26.75, -80.035], [26.62, -80.035], [26.47, -80.053], [26.35, -80.066], [26.26, -80.079], [26.12, -80.098], [26.0, -80.112], [25.93, -80.118], [25.905, -80.12],
    [25.905, -80.15], [25.87, -80.165], [25.83, -80.18], [25.79, -80.188], [25.76, -80.19], [25.73, -80.225], [25.70, -80.255], [25.65, -80.285],
    [25.58, -80.315], [25.50, -80.32], [25.42, -80.33], [25.30, -80.40], [24.4, -80.45], [24.4, -82.5], [27.6, -82.5]];
  var MIAMI_BEACH = [[25.905, -80.132], [25.84, -80.132], [25.79, -80.145], [25.763, -80.145], [25.763, -80.127], [25.80, -80.121], [25.87, -80.117], [25.905, -80.117]];
  var OKEECHOBEE = [[27.20, -80.83], [27.10, -80.70], [27.00, -80.62], [26.88, -80.655], [26.80, -80.685], [26.74, -80.72], [26.73, -80.85], [26.77, -80.97], [26.95, -81.05], [27.12, -80.95]];
  var KEY_BISCAYNE = [[25.738, -80.168], [25.70, -80.172], [25.663, -80.162], [25.668, -80.150], [25.72, -80.153]];

  function el(tag, attrs, parent) {
    var e = document.createElementNS(SVGNS, tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(e);
    return e;
  }

  var svgBounds = null;
  function freeArea(W) {
    if (W <= 900) return { l: 16, r: 16, t: 250, b: 30 };
    if (W <= 1180) return { l: 40, r: 460, t: 230, b: 110 };
    return { l: 590, r: 470, t: 50, b: 50 };
  }
  function fitSvg(bounds) {
    if (!svgEl) return;
    svgBounds = bounds || svgBounds;
    var host = $('#map'), W = host.clientWidth || 1, H = host.clientHeight || 1, f = freeArea(W);
    var bx = px(svgBounds[0][0]), bw = px(svgBounds[1][0]) - bx, by = py(svgBounds[1][1]), bh = py(svgBounds[0][1]) - by;
    var fw = Math.max(W - f.l - f.r, 120), fh = Math.max(H - f.t - f.b, 120);
    var sc = Math.min(fw / bw, fh / bh);
    var vx = bx - (f.l + (fw - bw * sc) / 2) / sc, vy = by - (f.t + (fh - bh * sc) / 2) / sc;
    svgEl.setAttribute('viewBox', vx.toFixed(1) + ' ' + vy.toFixed(1) + ' ' + (W / sc).toFixed(1) + ' ' + (H / sc).toFixed(1));
    svgEl.style.setProperty('--sv', (1 / sc).toFixed(3));
    Array.prototype.forEach.call(svgEl.querySelectorAll('.sv-left'), function (t) { t.setAttribute('x', (bx + 4 / sc).toFixed(1)); });
    sizeLabels();
  }

  var labels = [];
  function sizeLabels() {
    labels.forEach(function (l) {
      var bb; try { bb = l[0].getBBox(); } catch (e) { return; }
      var padX = bb.height * 0.5, gap = bb.height * 0.9;
      var x = l[2] ? -(bb.width + gap + padX) : gap + padX;
      l[0].setAttribute('x', x); l[0].setAttribute('y', 0);
      l[1].setAttribute('x', x - padX); l[1].setAttribute('y', -bb.height * 0.75);
      l[1].setAttribute('width', bb.width + 2 * padX); l[1].setAttribute('height', bb.height * 1.5);
    });
  }
  window.addEventListener('resize', function () { if (svgEl) { fitSvg(); sizeLabels(); } });

  function renderSchematic() {
    labels = [];
    var host = $('#map'), shell = $('.map-shell');
    if (!host) return;
    markers = {}; countyLabels = {};
    host.innerHTML = '';
    if (shell) { shell.classList.remove('no-map'); shell.classList.add('schematic'); }
    svgEl = el('svg', { 'class': 'schematic-map', role: 'img', 'aria-label': 'Güney Florida mahalle haritası (şematik)', preserveAspectRatio: 'none' }, host);
    el('rect', { x: -2000, y: -2000, width: 6000, height: 6000, 'class': 'sv-sea' }, svgEl);
    el('polygon', { points: pts(LAND), 'class': 'sv-land' }, svgEl);
    el('polygon', { points: pts(MIAMI_BEACH), 'class': 'sv-land' }, svgEl);
    el('polygon', { points: pts(KEY_BISCAYNE), 'class': 'sv-land' }, svgEl);
    el('polygon', { points: pts(OKEECHOBEE), 'class': 'sv-lake' }, svgEl);
    [PB_BR, BR_MD].forEach(function (lat) {
      el('line', { x1: px(-80.56), x2: px(-80.10), y1: py(lat), y2: py(lat), 'class': 'sv-county-line' }, svgEl);
    });
    [['Palm Beach', 26.60], ['Broward', 26.20], ['Miami-Dade', 25.90]].forEach(function (c) {
      var t = el('text', { x: px(-80.53), y: py(c[1]), 'class': 'sv-county sv-left' }, svgEl);
      t.textContent = c[0]; t.setAttribute('lang', 'en');
      countyLabels[c[0]] = { getElement: function () { return t; } };
    });
    el('text', { x: px(-80.02), y: py(26.05), 'class': 'sv-ocean' }, svgEl).textContent = 'Atlantik';
    HOODS.forEach(function (h) {
      var g = el('g', { 'class': 'sv-hood', tabindex: '0', role: 'button', 'aria-label': h.name, transform: 'translate(' + px(h.lng).toFixed(1) + ',' + py(h.lat).toFixed(1) + ')' }, svgEl);
      el('circle', { r: 1, 'class': 'sv-hit' }, g);
      el('circle', { r: 1, 'class': 'sv-dot' }, g);
      var right = h.lng > -80.2;
      var bg = el('rect', { 'class': 'sv-lbl-bg' }, g);
      var t = el('text', { 'class': 'sv-lbl', 'dominant-baseline': 'central' }, g);
      t.textContent = h.name; t.setAttribute('lang', 'en');
      labels.push([t, bg, right]);
      function go() { select(h.id); }
      g.addEventListener('click', go);
      g.addEventListener('keydown', function (ev) { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); go(); } });
      markers[h.id] = { getElement: function () { return g; } };
    });
    sizeLabels();
    var note = document.createElement('p');
    note.className = 'schematic-note';
    note.textContent = 'Şematik görünüm';
    host.appendChild(note);
    fitSvg(COUNTY_BOUNDS[state.county === 'All' ? 'Miami-Dade' : state.county]);
    updateMarkers();
  }

  function initMap() {
    // Önce her ortamda çalışan şematik harita çizilir; gerçek harita yalnızca
    // başarıyla yüklendiğinde onun yerine geçer. Böylece harita hiçbir zaman boş kalmaz.
    var shell = $('.map-shell'), host = $('#map');
    if (!host || !shell) return;
    renderSchematic();
    if (!window.maplibregl) return;
    try { if (maplibregl.supported && !maplibregl.supported()) return; } catch (e) {}
    var glEl = document.createElement('div');
    glEl.className = 'gl-layer';
    glEl.setAttribute('aria-hidden', 'true');
    host.parentNode.insertBefore(glEl, host.nextSibling);
    var gl;
    try {
      gl = new maplibregl.Map({
        container: glEl,
        style: 'https://tiles.openfreemap.org/styles/dark',
        bounds: COUNTY_BOUNDS['Miami-Dade'],
        fitBoundsOptions: { padding: window.matchMedia('(min-width: 901px)').matches ? { top: 140, bottom: 110, left: 60, right: 440 } : 20 },
        cooperativeGestures: true,
        attributionControl: { compact: true },
        maxZoom: 16,
        minZoom: 7
      });
    } catch (e) {
      glEl.parentNode.removeChild(glEl);
      return;
    }
    gl.on('error', function () {});
    gl.on('load', function () {
      try {
        var g = countyGeo();
        gl.addSource('county-shade', { type: 'geojson', data: g.shade });
        gl.addLayer({ id: 'county-shade', type: 'fill', source: 'county-shade', paint: { 'fill-color': '#000000', 'fill-opacity': 0 } });
        gl.addSource('county-lines', { type: 'geojson', data: g.lines });
        gl.addLayer({ id: 'county-lines', type: 'line', source: 'county-lines', paint: { 'line-color': '#8A8378', 'line-width': 1.4, 'line-dasharray': [4, 3] } });
        gl.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-right');
      } catch (e) { return; }
      // Şematik haritayı kaldır, gerçek haritaya geç.
      host.innerHTML = ''; svgEl = null; labels = []; markers = {}; countyLabels = {};
      shell.classList.remove('schematic'); shell.classList.add('gl-ready');
      glEl.removeAttribute('aria-hidden');
      glEl.setAttribute('role', 'region');
      glEl.setAttribute('aria-label', 'Güney Florida mahalle haritası');
      map = gl;
      [['Palm Beach', 26.345], ['Broward', 25.985], ['Miami-Dade', 25.930]].forEach(function (c) {
        var el = document.createElement('div');
        el.className = 'county-label';
        el.textContent = c[0]; el.setAttribute('lang', 'en');
        countyLabels[c[0]] = new maplibregl.Marker({ element: el, anchor: 'left' }).setLngLat([-80.62, c[1]]).addTo(map);
      });
      HOODS.forEach(function (h) {
        var el = document.createElement('button');
        el.type = 'button';
        el.className = 'hood-marker';
        el.setAttribute('aria-label', h.name);
        el.innerHTML = '<span class="dot" aria-hidden="true"></span><span class="lbl"></span>';
        el.querySelector('.lbl').textContent = h.name; el.querySelector('.lbl').setAttribute('lang', 'en');
        el.addEventListener('click', function (ev) { ev.stopPropagation(); select(h.id); });
        markers[h.id] = new maplibregl.Marker({ element: el, anchor: 'left', offset: [-22, 0] }).setLngLat([h.lng, h.lat]).addTo(map);
      });
      if (state.county !== 'All') setCounty(state.county);
      updateMarkers();
    });
  }

  function initControls() {
    $all('.chip[data-hood], .hood-index button[data-hood]').forEach(function (b) {
      b.addEventListener('click', function () {
        select(b.getAttribute('data-hood'));
        if (b.closest('.hood-index')) { $('.map-shell').scrollIntoView({ behavior: 'smooth', block: 'start' }); }
      });
    });
    $all('.counties button').forEach(function (b) {
      b.addEventListener('click', function () { setCounty(b.getAttribute('data-county')); });
    });
    var form = $('#map-search');
    if (form) {
      form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        var q = ($('input', form).value || '').trim().toLocaleLowerCase('tr');
        if (!q) return;
        var hit = HOODS.filter(function (h) { return h.name.toLocaleLowerCase('tr').indexOf(q) !== -1; })[0];
        if (hit) { select(hit.id); return; }
        location.href = '/ilanlar/?q=' + encodeURIComponent(($('input', form).value || '').trim());
      });
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    renderCard(byId(state.selected));
    initControls();
    initMap();
  });
})();
