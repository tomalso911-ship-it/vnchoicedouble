# -*- coding: utf-8 -*-
"""生成 PWA / APK 需要的 PNG 图标（品牌红 + 白色漏缝地板条）。
用法：python make_pwa_icons.py
产物：icon-192.png / icon-512.png / icon-512-maskable.png / apple-touch-icon.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
RED = (211, 47, 47, 255)      # #D32F2F（与顶栏/标题一致）
WHITE = (255, 255, 255, 255)

FONT_CANDIDATES = [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


def _font(size):
    for p in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _draw(size, maskable=False, radius_ratio=0.18):
    """画一张 size×size 的图标；maskable=True 时满底、内容缩进 20% 安全区。"""
    S = 1024                                   # 先在高分辨率画，再缩放（边缘平滑）
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if maskable:
        d.rectangle([0, 0, S, S], fill=RED)    # maskable 必须满底，不能被裁出白角
        pad = int(S * 0.16)                    # Android 圆形遮罩安全区
    else:
        r = int(S * radius_ratio)
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=r, fill=RED)
        pad = int(S * 0.10)

    inner = S - pad * 2
    # 文字 CS
    f = _font(int(inner * 0.40))
    d.text((S / 2, pad + inner * 0.36), "CS", font=f, fill=WHITE, anchor="mm")
    # 4 条漏缝地板（白色圆角横条）
    bar_h = int(inner * 0.055)
    gap = int(inner * 0.045)
    x0 = pad + int(inner * 0.16)
    x1 = pad + inner - int(inner * 0.16)
    y = pad + int(inner * 0.68)
    for _ in range(4):
        d.rounded_rectangle([x0, y, x1, y + bar_h], radius=bar_h // 2, fill=WHITE)
        y += bar_h + gap
    return img.resize((size, size), Image.LANCZOS)


def main():
    for name, size, maskable in [
        ("icon-512.png", 512, False),
        ("icon-192.png", 192, False),
        ("icon-512-maskable.png", 512, True),
        ("apple-touch-icon.png", 180, False),
    ]:
        path = os.path.join(BASE, name)
        _draw(size, maskable=maskable).save(path, "PNG", optimize=True)
        print("OK", name, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
