# Mahalle raporlarının aylık yenilenmesi

Raporlar her ay yenilenir. Kaynak verisi `tools/reports/<id>.json` dosyalarında, sayfalar `tools/build_reports.py` ile üretilir. Yayın kuralı değişmez: önce `taslak` dalı ve önizleme, Aleyna Bozoklar "onaylıyorum" dedikten sonra `main`.

## Adımlar

1. `tools/edition.json` içinde `edition` (ör. "Kasım 2026"), `date_iso` ve `date_human` alanlarını güncelleyin.
2. Her mahalle için verileri yenileyin ve JSON'daki rakamları, kaynak tarihlerini ve rakamlara bağlı yorum cümlelerini (`notes`, `short`, `meta`, `faq`, `pros`, `cons`) birlikte güncelleyin:
   - **Satış:** JSON'daki `sources` listesinde yer alan Redfin "Housing Market" sayfaları. WebFetch eski önbellek döndürebilir; URL'nin sonuna `?v=<yılay>` ekleyin (ör. `?v=202611`) ve sayfanın veri ayını mutlaka kontrol edin.
   - **Kira:** Zillow Rental Market Trends sayfaları (`https://www.zillow.com/rental-manager/market-trends/<şehir-veya-zip>/?v=<yılay>`). "Last updated" tarihi bir aydan eskiyse kullanmayın; RentCafe'ye geçin ve kaynakta belirtin.
   - **Vergi:** Millage oranları yılda bir (ekim–kasım) değişir. Yeni yılın oranları yayımlanınca Miami-Dade PA, Broward PA (`https://bcpa.net/millage.asp`) ve Boca Raton kaynaklarından güncelleyin.
   - **Projeler:** CondoBlackBook'un aylık Miami-Dade ve Broward/Palm Beach güncellemeleri, Florida YIMBY ve Commercial Observer. Teslim edilen projeleri "Tamamlandı" yapın, yenilerini ekleyin.
3. Kaynağı ve ayı belirtilmeyen hiçbir rakam yazılmaz. Veri bulunamazsa önceki ayın rakamı "güncellenemedi" notuyla bırakılır ve Aleyna'ya bildirilir.
4. `python3 tools/build_reports.py` çalıştırın (CSS/JS sürüm parametrelerini `tools/stamp_assets.py` otomatik günceller); `sitemap.xml` içindeki rapor `lastmod` tarihlerini güncelleyin.
5. `taslak` dalına commit edip push edin. Aleyna'ya kısa bir özet gönderin: en çok değişen 3–5 rakam, güncellenemeyen veriler ve onay isteği.
6. "onaylıyorum" gelince `taslak` → `main` fast-forward merge ve push. Netlify otomatik yayınlar.

## Kurallar

- Fair Housing: mahalleler insan gruplarına göre değil, özelliklerine göre anlatılır.
- Vergi, hukuk ve yatırım içeriklerinde "tavsiye değildir" notu korunur.
- Dil Türkçe, "siz" hitabı; birinci tekil şahıs kullanılmaz.
