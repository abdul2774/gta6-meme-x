#!/usr/bin/env python3
"""Build "THE WAITING RECEIPT" meme for make.fun gta6-meme-x-01.

Original itemized-receipt style meme: a fan's bill of GTA 6 grievances,
paid by their AI agent via make.fun. Rendered with PIL at 2x supersample
and downscaled to 1280x1120 for smoothness.
"""
import os
import urllib.request

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SS = 2  # supersample factor
W, H = 1280 * SS, 1120 * SS

ASSET_DIR = "/tmp/receipt-assets"
GHOST_URL = "https://make.fun/press/mark-1024.png"
TW_BASE = "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/{}.png"

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme-receipt.png")


def S(v):
    return int(v * SS)


def font(path, size):
    return ImageFont.truetype(path, S(size))


def get_asset(name, url):
    path = os.path.join(ASSET_DIR, name)
    if not os.path.exists(path):
        os.makedirs(ASSET_DIR, exist_ok=True)
        urllib.request.urlretrieve(url, path)
    return Image.open(path).convert("RGBA")


def twemoji(codepoint):
    return get_asset(f"tw-{codepoint}.png", TW_BASE.format(codepoint))


def paste_emoji(base, codepoint, cx, cy, size):
    """Paste a twemoji centred at (cx, cy) with the given final-scale size."""
    img = twemoji(codepoint)
    s = S(size)
    img = img.resize((s, s), Image.LANCZOS)
    base.alpha_composite(img, (S(cx) - s // 2, S(cy) - s // 2))


def v_gradient(w, h, stops):
    """Vertical gradient through (pos, (r,g,b)) stops."""
    grad = Image.new("RGB", (1, h))
    px = []
    for y in range(h):
        t = y / max(h - 1, 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                f = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                px.append(tuple(round(c0[k] + (c1[k] - c0[k]) * f) for k in range(3)))
                break
        else:
            px.append(stops[-1][1])
    grad.putdata(px)
    return grad.resize((w, h))


def text_w(draw, txt, fnt):
    return draw.textlength(txt, font=fnt)


def main():
    # ---------- background ----------
    bg = v_gradient(W, H, [
        (0.0, (30, 11, 61)),      # deep purple
        (0.42, (123, 30, 110)),   # purple-magenta
        (0.68, (214, 51, 108)),   # magenta-pink
        (1.0, (255, 154, 61)),    # warm orange
    ]).convert("RGBA")

    # ---------- card shadow + body ----------
    card_x0, card_y0, card_x1, card_y1 = S(70), S(56), S(1210), S(1064)
    radius = S(36)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([card_x0, card_y0 + S(14), card_x1, card_y1 + S(14)],
                         radius=radius, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(S(16)))
    bg.alpha_composite(shadow)

    d = ImageDraw.Draw(bg)
    d.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=radius,
                        fill=(255, 253, 248, 255))
    pad = S(46)
    inner_l, inner_r = card_x0 + pad, card_x1 - pad

    # ---------- header band (black) ----------
    hdr_h = S(118)
    hdr = Image.new("RGBA", (card_x1 - card_x0, hdr_h), (17, 17, 17, 255))
    # round only the top corners: paste, then square off the bottom via mask
    mask = Image.new("L", hdr.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, hdr.size[0], hdr.size[1] + radius], radius=radius, fill=255)
    bg.paste(hdr, (card_x0, card_y0), mask)
    d = ImageDraw.Draw(bg)

    paste_emoji(bg, "1f9fe", 70 + 62, 56 + 59, 66)  # receipt icon
    sub_f = font(FONT_BOLD, 23)
    tx = card_x0 + S(112)
    # Title: "JASON <broken-heart twemoji> LUCIA RECEIPT", auto-fit to one line.
    title_left, title_right = "JASON", "LUCIA RECEIPT"
    title_size = 53
    heart_pad = 12  # final-scale px on each side of the heart
    while title_size > 20:
        title_f = font(FONT_BOLD, title_size)
        lw = text_w(d, title_left, title_f)
        rw = text_w(d, title_right, title_f)
        total_w = lw + S(heart_pad) + S(title_size) + S(heart_pad) + rw
        if tx + total_w <= inner_r:
            break
        title_size -= 1
    title_y = card_y0 + S(16)
    d.text((tx, title_y), title_left, font=title_f, fill=(255, 255, 255))
    heart_cx = (tx + lw + S(heart_pad) + S(title_size) // 2) // SS
    paste_emoji(bg, "1f494", heart_cx, (title_y // SS) + title_size // 2 + 2, title_size)
    d.text((tx + lw + S(heart_pad) + S(title_size) + S(heart_pad), title_y),
           title_right, font=title_f, fill=(255, 255, 255))
    d.text((tx, card_y0 + S(80)), "GRAND THEFT AUTO VI · FAN ACCOUNT STATEMENT",
           font=sub_f, fill=(255, 216, 61))

    # ---------- meta lines ----------
    meta_f = font(FONT_BOLD, 22)
    meta_y = card_y0 + hdr_h + S(18)
    d.text((inner_l, meta_y), "ISSUED TO: EVERY GTA FAN", font=meta_f, fill=(90, 90, 90))
    right_txt = "ACCOUNT OPEN SINCE: SEP 17, 2013"
    d.text((inner_r - text_w(d, right_txt, meta_f), meta_y), right_txt,
           font=meta_f, fill=(90, 90, 90))

    # ---------- itemized lines ----------
    items = [
        ("Waiting for a sequel", "13 YEARS", "1f480"),
        ("Delay #1: Fall 2025 \u2192 May 2026", "6 MONTHS", "1f624"),
        ("Delay #2: May 2026 \u2192 Nov 19, 2026", "6 MORE", "1f62d"),
        ("Download size (SSD sold separately)", "200 GB", "1faa6"),
        ("Day-one patch", "ANOTHER 40 GB", "1fae0"),
        ("Launch price", "$80", "1f4b8"),
        ("PC version at launch", "NOT INCLUDED", "1f6ab"),
        ("Sick days burned for launch week", "3 (WORTH IT)", "1f912"),
    ]
    lab_f = font(FONT_REG, 29)
    val_f = font(FONT_BOLD, 30)
    items_top = meta_y + S(52)
    row_h = S(49)
    emoji_size = 36
    emoji_cx = (inner_r // SS) - 20  # final-scale centre x of emoji column
    val_right = inner_r - S(emoji_size + 22)  # values end before emoji column

    def draw_row(cy, label, value, cps):
        """One itemized line: label, dotted leader, bold value, trailing emoji(s)."""
        n = len(cps)
        block_w = n * emoji_size + (n - 1) * 6
        block_right = inner_r - S(2)
        v_right = block_right - S(block_w + 20)
        baseline = cy + S(6)
        d.text((inner_l, baseline), label, font=lab_f, fill=(25, 25, 25))
        vw = text_w(d, value, val_f)
        d.text((v_right - vw, baseline), value, font=val_f, fill=(25, 25, 25))
        # dotted leader between label and value
        lab_end = inner_l + text_w(d, label, lab_f) + S(12)
        dot_y = baseline + S(24)
        x = lab_end
        while x < v_right - vw - S(14):
            d.ellipse([x, dot_y, x + S(3.4), dot_y + S(3.4)], fill=(150, 150, 150))
            x += S(11)
        for j, cp in enumerate(cps):
            cx = (block_right - S(block_w)) // SS + j * (emoji_size + 6) + emoji_size // 2
            paste_emoji(bg, cp, cx, (cy // SS) + 24, emoji_size)

    for i, (label, value, cp) in enumerate(items):
        draw_row(items_top + i * row_h, label, value, [cp])

    # ---------- Jason & Lucia section ----------
    jl_items = [
        ("Lucia's prison sentence", "DONE. WE'RE STILL WAITING", ["1f494"]),
        ("Jason & Lucia surviving the ending", "PLEASE SURVIVE", ["1f64f", "1f494"]),
    ]
    jl_head_y = items_top + len(items) * row_h + S(16)
    jl_head_f = font(FONT_BOLD, 25)
    jl_head_txt = "JASON & LUCIA"
    d.text((inner_l, jl_head_y), jl_head_txt, font=jl_head_f, fill=(207, 18, 128))
    jw = text_w(d, jl_head_txt, jl_head_f)
    paste_emoji(bg, "1f494", (inner_l + jw) // SS + 24, (jl_head_y // SS) + 15, 30)
    jl_top = jl_head_y + S(44)
    for i, (label, value, cps) in enumerate(jl_items):
        draw_row(jl_top + i * row_h, label, value, cps)

    # ---------- divider + total ----------
    div_y = jl_top + len(jl_items) * row_h + S(10)
    d.line([inner_l, div_y, inner_r, div_y], fill=(30, 30, 30), width=S(3))
    total_txt = "TOTAL DUE: ONE GAME + ONE HAPPY ENDING FOR JASON & LUCIA"
    total_size = 36
    total_f = font(FONT_BOLD, total_size)
    while total_size > 20 and text_w(d, total_txt, total_f) > (inner_r - inner_l) - S(64):
        total_size -= 1
        total_f = font(FONT_BOLD, total_size)
    total_y = div_y + S(20)
    d.text((inner_l, total_y), total_txt, font=total_f, fill=(17, 17, 17))
    tw = text_w(d, total_txt, total_f)
    paste_emoji(bg, "1f494", (inner_l + tw) // SS + 30, (total_y // SS) + total_size // 2 + 4, 36)

    # ---------- red stamp ----------
    stamp_txt = "PAID · NOV 19, 2026"
    stamp_f = font(FONT_BOLD, 30)
    tmp = Image.new("RGBA", (S(400), S(130)), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    twd = td.textlength(stamp_txt, font=stamp_f)
    bw, bh = twd + S(34), S(58)
    bx, by = (tmp.width - bw) // 2, (tmp.height - bh) // 2
    red = (210, 31, 43, 215)
    td.rounded_rectangle([bx, by, bx + bw, by + bh], radius=S(9), outline=red, width=S(5))
    td.rounded_rectangle([bx + S(6), by + S(6), bx + bw - S(6), by + bh - S(6)],
                         radius=S(6), outline=red, width=S(2))
    td.text((bx + (bw - twd) / 2, by + S(10)), stamp_txt, font=stamp_f, fill=red)
    stamp = tmp.rotate(9, resample=Image.BICUBIC, expand=True)
    # centred over the dotted leaders of rows 2-3, clear of the values
    bg.alpha_composite(stamp, (S(578), items_top + S(14)))

    # ---------- magenta bottom band ----------
    band_h = S(168)
    band_y0 = card_y1 - band_h
    band = Image.new("RGBA", (card_x1 - card_x0, band_h), (207, 18, 128, 255))
    mask = Image.new("L", band.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, -radius, band.size[0], band.size[1]], radius=radius, fill=255)
    bg.paste(band, (card_x0, band_y0), mask)
    d = ImageDraw.Draw(bg)

    ghost = get_asset("ghost.png", GHOST_URL)
    gs = S(150)
    ghost_img = ghost.resize((gs, gs), Image.LANCZOS)
    bg.alpha_composite(ghost_img, (card_x0 + S(30), band_y0 + (band_h - gs) // 2))
    d = ImageDraw.Draw(bg)

    gx = card_x0 + S(200)
    big_f = font(FONT_BOLD, 41)
    small_f = font(FONT_REG, 26)
    d.text((gx, band_y0 + S(30)), "MY AI AGENT PAID THIS BILL", font=big_f,
           fill=(255, 255, 255))
    small_txt = "it earns real money on make.fun while I wait"
    d.text((gx, band_y0 + S(94)), small_txt, font=small_f, fill=(255, 255, 255))
    sw = text_w(d, small_txt, small_f)
    paste_emoji(bg, "1f4b0", (gx + sw) // SS + 24, (band_y0 // SS) + 84 + 14, 30)

    # ---------- save ----------
    out = bg.convert("RGB").resize((1280, 1120), Image.LANCZOS)
    out.save(OUT, "PNG")
    print("saved", OUT, out.size)


if __name__ == "__main__":
    main()
