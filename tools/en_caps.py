# -*- coding: utf-8 -*-
"""İngilizce özel adları <span lang="en"> ile işaretler.

Sayfa dili Türkçe (lang="tr") olduğu için CSS büyük harf dönüşümü (text-transform: uppercase)
İngilizce kelimelerdeki "i" harfini "İ" yapar (MİAMİ). İngilizce kelimeler lang="en" ile
işaretlenince tarayıcı doğru büyük harfi kullanır (MIAMI). Yalnızca içinde küçük "i" olan
İngilizce kelimeler işaretlenir; Türkçe ekler (Miami'de) dışarıda kalır.

Kullanım: python3 tools/en_caps.py  (stamp_assets.py tarafından otomatik çağrılır)
"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXTRA = """Miami Miami-Dade Florida Brightline Tri-Rail Metrorail Metromover Trolley Brickell Wynwood Design District
Biscayne Fisher Island Islands Isles Inlet Village City Springs Gardens Pines Hialeah Pinecrest Midtown Edgewater Little Havana
Realtor Realtors International Specialist Portfolio Housing Opportunity Equal Zillow Redfin Instagram LinkedIn Airbnb
Wellington Jupiter Riviera Delray Manalapan Highland Briny Breezes Atlantis Haverhill Mangonia Hypoluxo Juno Tequesta
Lighthouse Pointe Point Hills Heights Ridge Sailfish Collins Lincoln Coconut Grove Gables Virginia Indian Creek
Kravis Norton Flagler Clematis Mizner Mills Sawgrass Fontainebleau Faena Aventura Mall Shops Fair Wilton Manors
Plantation Sunrise Tamarac Margate Hillsboro Dania Parkland Opa-locka Medley Sweetwater Kendall Doral Palmetto
FIU University Institute Living Haute Elle English Français Leading Premium Companies Luxury Wildlife Wildlife Preserve Nature Natural Pier Marina Stadium District Cervera PortMiami Kaseya Pérez Frost Bascom Palmer Basel Bayfront Baptist""".split()


def words():
    ws = set(EXTRA)
    names = [h['name'] for h in json.load(open(os.path.join(ROOT, 'tools', 'hoods.json'), encoding='utf-8'))]
    pj = os.path.join(ROOT, 'tools', 'projects.json')
    if os.path.exists(pj):
        for p in json.load(open(pj, encoding='utf-8')).get('projects', []):
            names += [p.get('name') or '', p.get('developer') or '', p.get('area') or '']
    for n in names:
        for w in re.split(r"[\s&/(),.;:+]+", n):
            if w and re.fullmatch(r"[A-Za-z][A-Za-z'\-]*", w):
                ws.add(w)
    # Yalnızca küçük "i" içerenler sorun yaratır; Türkçe kelimelerle çakışmasın diye büyük harfle başlayanlar
    return sorted({w.strip("'-") for w in ws if 'i' in w and w[0].isupper()}, key=len, reverse=True)


TOKEN = re.compile(r'(<(script|style|select|textarea|title|svg)\b.*?</\2>)|(<[^>]*>)([^<]+)(?=<)', re.S | re.I)


def process(html, pat):
    i = html.find('<body')
    if i < 0:
        return html
    def rep(m):
        if m.group(1):
            return m.group(1)
        tag, text = m.group(3), m.group(4)
        if 'lang="en"' in tag or tag.startswith('<script') or tag.startswith('<style'):
            return tag + text
        new = pat.sub(r'<span lang="en">\1</span>', text)
        if new != text and not tag.startswith('<span class="ent"'):
            # Metnin tamamı tek bir öğe olarak kalsın (flex kapsayıcılarda kelimeler ayrı kutulara bölünmesin)
            new = '<span class="ent">' + new + '</span>'
        return tag + new
    return html[:i] + TOKEN.sub(rep, html[i:])


def main():
    ws = words()
    # Zaten işaretli olanları atla: hemen öncesinde lang="en"> olmayan kelimeler
    pat = re.compile(r'(?<![\w-])(' + '|'.join(re.escape(w) for w in ws) + r')(?![\w-])')
    n = 0
    for h in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        if '/tools/' in h or '/node_modules/' in h:
            continue
        s = open(h, encoding='utf-8').read()
        t = process(s, pat)
        if t != s:
            open(h, 'w', encoding='utf-8').write(t); n += 1
    print('en_caps', n, 'files')


if __name__ == '__main__':
    main()
