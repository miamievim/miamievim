# -*- coding: utf-8 -*-
"""Wikimedia Commons görsel URL'leri ve künye bilgisi (tools/images.json)."""
import hashlib, json, os, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, 'tools', 'images.json'), encoding='utf-8'))


def url(rec, width=None):
    f, w, h, scaled = rec[0], rec[1], rec[2], rec[3]
    name = f.replace(' ', '_')
    md = hashlib.md5(name.encode('utf-8')).hexdigest()
    q = urllib.parse.quote(name)
    if scaled:
        return f'https://upload.wikimedia.org/wikipedia/commons/thumb/{md[0]}/{md[:2]}/{q}/{width or w}px-{q}'
    return f'https://upload.wikimedia.org/wikipedia/commons/{md[0]}/{md[:2]}/{q}'


def page(rec):
    return 'https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(rec[0].replace(' ', '_'))


def credit(rec):
    return f'{rec[4]} · {rec[5]} · Wikimedia Commons'


def hood(i):
    return DATA['hoods'].get(i, [])


def misc(k):
    return DATA['misc'][k]


def misc_url(k):
    return url(DATA['misc'][k], 1280)


def credits_html(recs, title='Görsel künyeleri'):
    import html as _h
    seen, items = set(), []
    for r in recs:
        if not r or r[0] in seen: continue
        seen.add(r[0])
        items.append(f'<li><a href="{page(r)}" target="_blank" rel="noopener">{_h.escape(r[0].rsplit(".",1)[0])}</a>: {_h.escape(r[4])}, {_h.escape(r[5])}</li>')
    return f'<details class="img-credits"><summary>{title}</summary><ol>' + ''.join(items) + '</ol><p>Görseller Wikimedia Commons\'tan, belirtilen özgür lisanslarla kullanılmıştır; görsellerde değişiklik yapılmamış, yalnızca boyutlandırılmıştır.</p></details>'
