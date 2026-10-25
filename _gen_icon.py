import os
from PIL import Image

SRC = r'C:\vnchoicedouble\icon-512.png'
RES = r'C:\vnchoicedouble\android-app\android\app\src\main\res'
logo = Image.open(SRC).convert('RGBA')
info = []
dens = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}

for d, f in dens.items():
    # full icon fills the canvas (source is a complete red square logo)
    c108 = int(round(108 * f))
    fg = logo.resize((c108, c108), Image.LANCZOS)
    fg.save(os.path.join(RES, 'mipmap-%s' % d, 'ic_launcher_foreground.png'))

    c48 = int(round(48 * f))
    leg = logo.resize((c48, c48), Image.LANCZOS)
    leg.save(os.path.join(RES, 'mipmap-%s' % d, 'ic_launcher.png'))
    leg.save(os.path.join(RES, 'mipmap-%s' % d, 'ic_launcher_round.png'))
    info.append('%s -> fg %dx%d legacy %dx%d' % (d, c108, c108, c48, c48))

info.append('DONE')
with open(r'C:\vnchoicedouble\_icon_info.txt', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(info))
print('\n'.join(info))
