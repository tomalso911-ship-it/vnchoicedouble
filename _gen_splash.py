import os, glob
from PIL import Image, ImageDraw, ImageFont

SRC = r'C:\vnchoicedouble\icon-512.png'
RES = r'C:\vnchoicedouble\android-app\android\app\src\main\res'
RED = (211, 47, 47, 255)  # #D32F2F
NAME = 'ChoiceVN'
VER = '2026.10.25-V1'
LINE = '%s  ·  %s' % (NAME, VER)

FONT = r'C:\Windows\Fonts\arial.ttf'
def get_font(sz):
    try:
        return ImageFont.truetype(FONT, sz)
    except Exception:
        return ImageFont.load_default()

# 抽取白色字标（亮部留白，红底变透明）
logo = Image.open(SRC).convert('RGBA')
W, H = logo.size
lpx = logo.load()
white = Image.new('RGBA', (W, H), (0, 0, 0, 0))
wpx = white.load()
for y in range(H):
    for x in range(W):
        r, g, b, a = lpx[x, y]
        if a <= 10:
            continue
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        if lum > 150:
            wpx[x, y] = (255, 255, 255, 255)

paths = glob.glob(os.path.join(RES, 'drawable', 'splash.png')) + \
        glob.glob(os.path.join(RES, 'drawable-*', 'splash.png'))
info = []
for p in sorted(set(paths)):
    im = Image.open(p).convert('RGBA')
    sw, sh = im.size
    bg = Image.new('RGBA', (sw, sh), RED)
    # logo 偏上居中
    s = int(min(sw, sh) * 0.40)
    wl = white.copy()
    wl.thumbnail((s, s), Image.LANCZOS)
    lx = (sw - wl.width) // 2
    ly = int(sh * 0.33) - wl.height // 2
    if ly < 0:
        ly = 0
    bg.paste(wl, (lx, ly), wl)
    # 一行标语/版本号（白字，居中，自动缩小避免超宽）
    d = ImageDraw.Draw(bg)
    fs = max(14, int(min(sw, sh) * 0.05))
    f = get_font(fs)
    while True:
        bb = d.textbbox((0, 0), LINE, font=f)
        if (bb[2] - bb[0]) <= sw * 0.92 or fs <= 14:
            break
        fs -= 2
        f = get_font(fs)
    d.text((sw / 2, int(sh * 0.63)), LINE, fill=(255, 255, 255, 255), font=f, anchor='mm')
    bg.convert('RGB').save(p)
    info.append('%s %dx%d' % (os.path.relpath(p, RES), sw, sh))

info.append('DONE count=%d' % len(info))
open(r'C:\vnchoicedouble\_splash_info.txt', 'w', encoding='utf-8').write('\n'.join(info))
print('\n'.join(info))
