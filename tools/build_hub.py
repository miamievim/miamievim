# -*- coding: utf-8 -*-
"""Mahalle listesini (tools/hoods.json) haritaya, rapor merkezine, site haritasına ve llms.txt'ye işler.

Kullanım: python3 tools/build_hub.py   (build_reports.py'den sonra)
"""
import json, os, re, html, glob, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
COUNTIES = ['Miami-Dade', 'Broward', 'Palm Beach']


def load():
    hoods = json.load(open(os.path.join(ROOT, 'tools', 'hoods.json'), encoding='utf-8'))
    live = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'tools', 'reports', '*.json'))}
    return [h for h in hoods if h['id'] in live]


def js_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


def update_map(hoods):
    p = os.path.join(ROOT, 'assets', 'map.js')
    s = open(p, encoding='utf-8').read()
    a = s.index('  var HOODS = [')
    b = s.index('];', a) + 2
    rows = ',\n'.join(f"    {{ id: {js_str(h['id'])}, name: {js_str(h['name'])}, county: {js_str(h['county'])}, lat: {h['lat']:.4f}, lng: {h['lng']:.4f}, line: {js_str(h['line'])} }}" for h in hoods)
    s = s[:a] + '  var HOODS = [\n' + rows + '\n  ];' + s[b:]
    open(p, 'w', encoding='utf-8').write(s)



LAND = [[27.6, -80.12], [26.98, -80.07], [26.94, -80.075], [26.85, -80.04], [26.75, -80.035], [26.62, -80.035], [26.47, -80.053], [26.35, -80.066], [26.26, -80.079], [26.12, -80.098], [26.0, -80.112], [25.93, -80.118], [25.905, -80.12],
    [25.905, -80.15], [25.87, -80.165], [25.83, -80.18], [25.79, -80.188], [25.76, -80.19], [25.73, -80.225], [25.70, -80.255], [25.65, -80.285],
    [25.58, -80.315], [25.50, -80.32], [25.42, -80.33], [25.30, -80.40], [24.4, -80.45], [24.4, -82.5], [27.6, -82.5]]
MB = [[25.905, -80.132], [25.84, -80.132], [25.79, -80.145], [25.763, -80.145], [25.763, -80.127], [25.80, -80.121], [25.87, -80.117], [25.905, -80.117]]
OK = [[27.20, -80.83], [27.10, -80.70], [27.00, -80.62], [26.88, -80.655], [26.80, -80.685], [26.74, -80.72], [26.73, -80.85], [26.77, -80.97], [26.95, -81.05], [27.12, -80.95]]


def locator(h):
    W, Hh = 400, 300
    span_lat = 0.8; span_lng = span_lat * 1.33 / 0.9
    lat0, lng0 = h['lat'] - span_lat / 2, h['lng'] - span_lng / 2
    def pt(la, lo): return f"{(lo - lng0) / span_lng * W:.1f},{(1 - (la - lat0) / span_lat) * Hh:.1f}"
    poly = lambda P, cls: f'<polygon class="{cls}" points="{" ".join(pt(a, b) for a, b in P)}"/>'
    x, y = pt(h['lat'], h['lng']).split(',')
    lines = ''.join(f'<line class="lc-line" x1="0" x2="{W}" y1="{pt(l, 0).split(",")[1]}" y2="{pt(l, 0).split(",")[1]}"/>' for l in (26.3220, 25.9567))
    return (f'<svg class="locmap" viewBox="0 0 {W} {Hh}" role="img" aria-label="{E(h["name"])} konum haritası">'
            f'<rect class="lc-sea" width="{W}" height="{Hh}"/>{poly(LAND, "lc-land")}{poly(MB, "lc-land")}{poly(OK, "lc-lake")}{lines}'
            f'<circle class="lc-halo" cx="{x}" cy="{y}" r="16"/><circle class="lc-dot" cx="{x}" cy="{y}" r="6"/></svg>')


def money(v):
    return '$' + f'{int(round(v)):,}'.replace(',', '.')


def card(h, imglib):
    d = json.load(open(os.path.join(ROOT, 'tools', 'reports', h['id'] + '.json'), encoding='utf-8'))
    imgs = imglib.hood(h['id'])
    def im(r, w, cls=''):
        return f'<img{(" class=" + chr(34) + cls + chr(34)) if cls else ""} src="{imglib.url(r, w if r[3] else None)}" alt="{E(h["name"])}" loading="lazy" decoding="async" width="{r[1]}" height="{r[2]}">'
    media = im(imgs[0], 500) if imgs else locator(h)
    gal = ''.join(f'<figure>{im(r, 500)}</figure>' for r in imgs[1:3])
    if imgs: gal += f'<figure class="hc-loc">{locator(h)}</figure>'
    credit = ('<p class="hc-credit">Fotoğraflar: ' + ' · '.join(f'<a href="{imglib.page(r)}" target="_blank" rel="noopener">{E(r[4])}, {E(r[5])}</a>' for r in imgs) + ', Wikimedia Commons</p>') if imgs else '<p class="hc-credit">Konum haritası şematiktir.</p>'
    s = d['sales']; rt = d['rent']; tx = d['tax']
    stats = [('Medyan satış fiyatı', (('≈ ' if s.get('median_approx') else '') + money(s['median'])) if s.get('median') else 'Yayımlanmıyor'),
             ('Ortalama kira', (money(rt['avg']) + ' / ay') if rt.get('avg') else 'Yetersiz veri'),
             ('Emlak vergisi', ('%' + f"{tx['mills'] / 10:.2f}".replace('.', ',') + (('–' + f"{tx['mills_hi'] / 10:.2f}".replace('.', ',')) if tx.get('mills_hi') else '')) + ' / yıl')]
    st = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in stats)
    return f'''
        <li class="rrow hcard" id="{h['id']}" data-live data-name="{E(h['name'].lower())}">
          <h3 class="hc-name">{E(h['name'])}</h3>
          <div class="hc-media">{media}</div>
          <details class="hc-more">
            <summary>Daha fazla bilgi</summary>
            <div class="hc-body">
              <p class="county">{E(h['county'])} County · Ekim 2026</p>
              <p class="hc-short">{E(d['short'])}</p>
              <dl class="hc-stats">{st}</dl>
              {('<div class="hc-gal">' + gal + '</div>') if gal else ''}
              {credit}
              <div class="hc-acts"><a class="btn btn-line" href="/mahalle-raporlari/{h['id']}/">Önizlemeyi açın</a><button type="button" class="btn get" data-id="{h['id']}">Detaylı rapor</button></div>
            </div>
          </details>
        </li>'''

def update_hub(hoods):
    p = os.path.join(ROOT, 'mahalle-raporlari', 'index.html')
    s = open(p, encoding='utf-8').read()
    n = len(hoods)
    # Liste: görselli kartlar (önizleme "Daha fazla bilgi" ile açılır)
    sys.path.insert(0, os.path.join(ROOT, 'tools'))
    import imglib
    blocks = []
    for c in COUNTIES:
        hs = sorted([h for h in hoods if h['county'] == c], key=lambda h: h['name'])
        if not hs: continue
        cid = c.lower().replace(' ', '-')
        items = ''.join(card(h, imglib) for h in hs)
        blocks.append(f'''
      <h3 class="rcounty" id="ilce-{cid}">{E(c)} <span>{len(hs)} bölge</span></h3>
      <ol class="rlist hgrid">{items}
      </ol>''')
    lst = ''.join(blocks)
    a = s.index('      <ol class="rlist">') if '<div class="rgroups">' not in s else s.index('      <div class="rgroups">')
    b = s.index('</ol>', a) + 5 if '<div class="rgroups">' not in s else s.index('      </div><!-- /rgroups -->') + len('      </div><!-- /rgroups -->')
    filt = f'''      <div class="rgroups">
      <div class="rfilter"><label class="sr-only" for="rf-q">Mahalle ara</label><input type="search" id="rf-q" placeholder="Mahalle veya şehir ara ({n} bölge)"><div class="rjump">''' + ''.join(
        f'<a href="#ilce-{c.lower().replace(" ", "-")}">{E(c)}</a>' for c in COUNTIES) + f'''</div></div>{lst}
      </div><!-- /rgroups -->'''
    s = s[:a] + filt + s[b:]
    # Form seçenekleri
    a = s.index('<select name="mahalle" id="gate-hood">')
    b = s.index('</select>', a)
    opts = '<option value="tumu">Tüm mahalleler</option>' + ''.join(
        f'<optgroup label="{E(c)}">' + ''.join(f'<option value="{h["id"]}">{E(h["name"])}</option>' for h in sorted([h for h in hoods if h['county'] == c], key=lambda h: h['name'])) + '</optgroup>' for c in COUNTIES)
    s = s[:a] + '<select name="mahalle" id="gate-hood">' + opts + s[b:]
    s = re.sub(r'<h2>\d+ mahalle <em>raporu</em></h2>', f'<h2>{n} bölge <em>raporu</em></h2>', s)
    s = re.sub(r'\b\d+ mahalle, aynı dokuz başlık', f'{n} bölge, aynı dokuz başlık', s)
    if 'rf-q' in s and 'id="rf-script"' not in s:
        s = s.replace('</main>', '''</main>
<script id="rf-script">
(function () {
  var q = document.getElementById('rf-q'); if (!q) return;
  q.addEventListener('input', function () {
    var v = q.value.trim().toLocaleLowerCase('tr');
    Array.prototype.forEach.call(document.querySelectorAll('.rgroups .rrow'), function (r) { r.hidden = v && r.dataset.name.indexOf(v) === -1; });
    Array.prototype.forEach.call(document.querySelectorAll('.rgroups .rlist'), function (l) { var any = l.querySelector('.rrow:not([hidden])'); l.hidden = !any; l.previousElementSibling.hidden = !any; });
  });
})();
</script>''', 1)
    open(p, 'w', encoding='utf-8').write(s)
    return n


def update_counts(n):
    # Yalnızca 2-3 basamaklı ve aralık parçası olmayan sayılar ("2–3 mahalle" gibi ifadeler korunur).
    N = r'(?<![–\-\d])\b\d{2,3}'
    common = [(N + r' mahallenin', f'{n} bölgenin'), (N + r' mahalle\b', f'{n} bölge'), (N + r' bölgenin', f'{n} bölgenin'), (N + r' bölge\b', f'{n} bölge')]
    for f, pats in [('index.html', [(N + r' mahalle, rakamlarıyla', f'{n} bölge, rakamlarıyla'), (N + r' bölge rehberi', f'{n} bölge raporu')] + common + [(r'her pazartesi yeni rapor', 'her ay güncellenen raporlar'), (r'haftalık raporlar', 'aylık güncellenen raporlar')]),
                    ('mahalle-raporlari/index.html', common),
                    ('llms.txt', common + [(r'(\d+ bölge) \([^)]*\)', r'\1')])]:
        p = os.path.join(ROOT, f)
        lines = open(p, encoding='utf-8').read().split('\n')
        out = []
        for line in lines:
            if 'mahalle-rehberi/' not in line:  # Mahalle Rehberi ayrı bir yayındır (22 mahalle); sayısına dokunulmaz
                for a, b in pats:
                    line = re.sub(a, b, line)
            out.append(line)
        open(p, 'w', encoding='utf-8').write('\n'.join(out))


def update_sitemap_llms(hoods):
    p = os.path.join(ROOT, 'sitemap.xml')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'  <url><loc>https://miamievim.com/mahalle-raporlari/[a-z0-9-]+/</loc><lastmod>[^<]+</lastmod></url>\n', '', s)
    ed = json.load(open(os.path.join(ROOT, 'tools', 'edition.json')))
    s = s.replace('</urlset>', ''.join(f'  <url><loc>https://miamievim.com/mahalle-raporlari/{h["id"]}/</loc><lastmod>{ed["date_iso"]}</lastmod></url>\n' for h in hoods) + '</urlset>')
    open(p, 'w', encoding='utf-8').write(s)
    p = os.path.join(ROOT, 'llms.txt')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'(- \[[^\]]+ mahalle raporu \([^)]*\)\]\([^)]+\)\n)+', '', s)
    lines = ''.join(f'- [{h["name"]} mahalle raporu ({ed["edition"]})](https://miamievim.com/mahalle-raporlari/{h["id"]}/)\n' for h in sorted(hoods, key=lambda h: (COUNTIES.index(h['county']), h['name'])))
    s = s.replace('Raporlar her ay güncellenir.\n', 'Raporlar her ay güncellenir.\n' + lines, 1)
    open(p, 'w', encoding='utf-8').write(s)


def main():
    hoods = load()
    update_map(hoods)
    update_counts(len(hoods))  # önce genel sayılar; ilçe başlıklarındaki sayılar update_hub'da yazılır
    n = update_hub(hoods)
    update_sitemap_llms(hoods)
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'stamp_assets.py')], check=True)
    print('hub', n)


if __name__ == '__main__':
    main()
