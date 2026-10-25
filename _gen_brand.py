import os, glob
from PIL import Image, ImageDraw, ImageFont

MASTER = r'C:\vnchoicedouble\_logo_full.png'
RES = r'C:\vnchoicedouble\android-app\android\app\src\main\res'
WHITE = (255, 255, 255)
NAVY = (27, 42, 74)
LINE = 'ChoiceVN   \u00b7   2026.10.25-V1'
FONT = r'C:\Windows\Fonts\arialbd.ttf'

def font(sz):
    try:
        return ImageFont.truetype(FONT, sz)
    except Exception:
        return ImageFont.load_default()

logo = Image.open(MASTER).convert('RGB')
LW, LH = logo.size
RATIO = LW / LH

def fit_logo(tw):
    th = max(1, int(round(tw / RATIO)))
    return logo.resize((tw, th), Image.LANCZOS)

info = []

# ---------- 启动图标 ----------
dens = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}
for d, f in dens.items():
    c108 = int(round(108 * f))
    fg = Image.new('RGBA', (c108, c108), (255, 255, 255, 255))
    lg = fit_logo(int(round(0.84 * c108)))
    fg.paste(lg, ((c108 - lg.width) // 2, (c108 - lg.height) // 2))
    fg.save(os.path.join(RES, 'mipmap-%s' % d, 'ic_launcher_foreground.png'))

    c48 = int(round(48 * f))
    leg = Image.new('RGBA', (c48, c48), (255, 255, 255, 255))
    lg2 = fit_logo(int(round(0.86 * c48)))
    leg.paste(lg2, ((c48 - lg2.width) // 2, (c48 - lg2.height) // 2))
    leg.save(os.path.join(RES, 'mipmap-%s' % d, 'ic_launcher.png'))
    leg.save(os.path.join(RES, 'mipmap-%s' % d, 'ic_launcher_round.png'))
    info.append('icon %s fg %d legacy %d' % (d, c108, c48))

# ---------- 闪屏 ----------
paths = glob.glob(os.path.join(RES, 'drawable', 'splash.png')) + \
        glob.glob(os.path.join(RES, 'drawable-*', 'splash.png'))
for p in sorted(set(paths)):
    im = Image.open(p)
    sw, sh = im.size
    bg = Image.new('RGB', (sw, sh), WHITE)

    tw = int(sw * 0.80)
    th = int(round(tw / RATIO))
    maxh = int(sh * 0.45)
    if th > maxh:
        th = maxh
        tw = int(round(th * RATIO))
    lg = fit_logo(tw)
    lx = (sw - lg.width) // 2
    ly = int(sh * 0.40) - lg.height // 2
    if ly < int(sh * 0.03):
        ly = int(sh * 0.03)
    bg.paste(lg, (lx, ly))

    # 版本号/标语行（藏蓝）
    d = ImageDraw.Draw(bg)
    ty = ly + lg.height + int(sh * 0.07)
    if ty > int(sh * 0.92):
        ty = int(sh * 0.92)
    fs = max(12, int(min(sw, sh) * 0.045))
    fnt = font(fs)
    while True:
        bb = d.textbbox((0, 0), LINE, font=fnt)
        if (bb[2] - bb[0]) <= sw * 0.90 or fs <= 12:
            break
        fs -= 2
        fnt = font(fs)
    d.text((sw // 2, ty), LINE, fill=NAVY, font=fnt, anchor='mm')

    bg.save(p)
    info.append('splash %s %dx%d' % (os.path.relpath(p, RES), sw, sh))

open(r'C:\vnchoicedouble\_brand_info.txt', 'w', encoding='utf-8').write('\n'.join(info))
print('\n'.join(info))
