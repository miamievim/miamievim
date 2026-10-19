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


def update_hub(hoods):
    p = os.path.join(ROOT, 'mahalle-raporlari', 'index.html')
    s = open(p, encoding='utf-8').read()
    n = len(hoods)
    # Liste
    blocks = []
    for c in COUNTIES:
        hs = sorted([h for h in hoods if h['county'] == c], key=lambda h: h['name'])
        if not hs: continue
        cid = c.lower().replace(' ', '-')
        items = ''.join(f'''
        <li class="rrow" id="{h['id']}" data-live data-name="{E(h['name'].lower())}">
          <div class="rmain"><span class="county">{E(c)}</span><h3>{E(h['name'])}</h3><p>{E(h['line'])}</p></div>
          <div class="racts"><a class="btn btn-line prev" href="/mahalle-raporlari/{h['id']}/">Önizleme</a><button type="button" class="btn get" data-id="{h['id']}">Detaylı rapor</button></div>
        </li>''' for h in hs)
        blocks.append(f'''
      <h3 class="rcounty" id="ilce-{cid}">{E(c)} <span>{len(hs)} bölge</span></h3>
      <ol class="rlist">{items}
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
    for f, pats in [('index.html', [(r'\b\d+ mahalle, rakamlarıyla', f'{n} bölge, rakamlarıyla'), (r'\b\d+ mahallenin', f'{n} bölgenin'), (r'\b\d+ mahalle\b', f'{n} bölge'), (r'\b\d+ bölgenin', f'{n} bölgenin'), (r'\b\d+ bölge\b', f'{n} bölge'), (r'her pazartesi yeni rapor', 'her ay güncellenen raporlar'), (r'haftalık raporlar', 'aylık güncellenen raporlar')]),
                    ('mahalle-raporlari/index.html', [(r'\b\d+ mahallenin', f'{n} bölgenin'), (r'\b\d+ mahalle\b', f'{n} bölge'), (r'\b\d+ bölgenin', f'{n} bölgenin'), (r'\b\d+ bölge\b', f'{n} bölge')]),
                    ('llms.txt', [(r'\b\d+ mahallenin', f'{n} bölgenin'), (r'\b\d+ mahalle\b', f'{n} bölge'), (r'\b\d+ bölgenin', f'{n} bölgenin'), (r'\b\d+ bölge\b', f'{n} bölge'), (r'(\d+ bölge) \([^)]*\)', r'\1')])]:
        p = os.path.join(ROOT, f)
        s = open(p, encoding='utf-8').read()
        for a, b in pats:
            s = re.sub(a, b, s)
        open(p, 'w', encoding='utf-8').write(s)


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
