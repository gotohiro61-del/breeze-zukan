# -*- coding: utf-8 -*-
import base64, os

base = r'C:\Users\Administrator\GitHub\BREEZE'
imgdir = os.path.join(base, 'images')

with open(os.path.join(base, 'index.html'), encoding='utf-8') as f:
    html = f.read()

def datauri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {'.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp'}.get(ext,'application/octet-stream')
    with open(path, 'rb') as fp:
        b64 = base64.b64encode(fp.read()).decode('ascii')
    return 'data:%s;base64,%s' % (mime, b64)

files = [f for f in os.listdir(imgdir) if f.lower().endswith(('.jpg','.jpeg','.png','.webp'))]
imgmap = {f: datauri(os.path.join(imgdir, f)) for f in files}

# 1) hero background in CSS
old_hero = "url('images/hero.webp')"
assert old_hero in html, "hero css not found"
html = html.replace(old_hero, "url('%s')" % imgmap['hero.webp'])

# 2) inject IMGDATA map right after BOOK_URL
anchor = 'const BOOK_URL = "https://breeze-camp.com/";'
assert anchor in html, "BOOK_URL anchor not found"
entries = ','.join('"%s":"%s"' % (k, v) for k, v in imgmap.items())
html = html.replace(anchor, anchor + '\nconst IMGDATA = {' + entries + '};')

# 3) point the <img> src at the inlined data
old_img = '<img src="images/${it.img}" alt="${it.title}の様子" loading="lazy" onerror="${FALLBACK}">'
assert old_img in html, "img tag not found"
new_img = '<img src="${IMGDATA[it.img]||(\'images/\'+it.img)}" alt="${it.title}の様子" loading="lazy" onerror="${FALLBACK}">'
html = html.replace(old_img, new_img)

out = os.path.join(base, 'BREEZE-zukan.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print('images inlined:', len(imgmap))
print('output:', out)
print('size MB:', round(os.path.getsize(out)/1048576, 2))
print('remaining images/ refs in img src:', html.count('src="images/'))
