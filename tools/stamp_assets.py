# -*- coding: utf-8 -*-
"""CSS/JS bağlantılarına içerik özetine dayalı sürüm ekler (?v=...).

/assets/* tarayıcıda 7 gün önbelleğe alındığı için, dosya değiştiğinde
ziyaretçinin eski sürümü görmemesi bu sürüm parametresiyle sağlanır.
Kullanım: python3 tools/stamp_assets.py  (her derlemeden sonra)
"""
import glob, hashlib, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ver(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()[:8]


def main():
    vers = {}
    for f in glob.glob(os.path.join(ROOT, 'assets', '*.css')) + glob.glob(os.path.join(ROOT, 'assets', '*.js')):
        vers['/assets/' + os.path.basename(f)] = ver(f)
    n = 0
    for h in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        if '/tools/' in h or '/node_modules/' in h:
            continue
        s = open(h, encoding='utf-8').read()
        if 'data-netlify="true"' in s and '/assets/forms.js' not in s:
            s = s.replace('</body>', '<script src="/assets/forms.js" defer></script>\n</body>', 1)
            open(h, 'w', encoding='utf-8').write(s)
        t = re.sub(r'(/assets/[\w.-]+\.(?:css|js))(\?v=[0-9a-f]+)?', lambda m: m.group(1) + ('?v=' + vers[m.group(1)] if m.group(1) in vers else ''), s)
        if t != s:
            open(h, 'w', encoding='utf-8').write(t); n += 1
    print('stamped', n, 'files')
    import importlib.util
    spec = importlib.util.spec_from_file_location('en_caps', os.path.join(ROOT, 'tools', 'en_caps.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.main()


if __name__ == '__main__':
    main()
