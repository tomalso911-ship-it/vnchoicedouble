import zipfile, io
from PIL import Image

APK = r'C:\vnchoicedouble\android-app\android\app\build\outputs\apk\debug\ChoiceVN-2026.10.25-V1.apk'
z = zipfile.ZipFile(APK)


def check(name, label):
    im = Image.open(io.BytesIO(z.read(name))).convert('RGB')
    W, H = im.size
    px = im.load()
    red = navy = 0
    for y in range(0, H, 4):
        for x in range(0, W, 4):
            r, g, b = px[x, y]
            if r > 170 and g < 90 and b < 70:
                red += 1
            if r < 70 and g < 80 and 50 < b < 130:
                navy += 1
    print('%s %dx%d red=%d navy=%d' % (label, W, H, red, navy))


icons = [n for n in z.namelist() if n.endswith('ic_launcher.png')]
print('icon entries:', icons)
for n in icons:
    check(n, 'ICON')

sps = [n for n in z.namelist() if n.endswith('splash.png')]
print('splash count:', len(sps))
for n in sps:
    check(n, 'SPLASH')
