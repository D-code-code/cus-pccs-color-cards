"""
PCCS 色卡扫描用 A3 贴色块模版 v2
3枚構成（各4トーン×24色相）+ 無彩色
貼付エリア: 10mm × 10mm
300 DPI, A3 portrait (297×420mm)
"""
from PIL import Image, ImageDraw, ImageFont
import os

DPI = 300
MM = DPI / 25.4

W_PX = int(297 * MM)   # 3508
H_PX = int(420 * MM)   # 4961

MARGIN = int(15 * MM)        # 15mm
TITLE_H = int(22 * MM)       # title area
FOOTER_H = int(10 * MM)      # bottom footer

GRID_X = MARGIN
GRID_Y = MARGIN + TITLE_H
GRID_W = W_PX - 2 * MARGIN
GRID_H = H_PX - GRID_Y - MARGIN - FOOTER_H

# 3 sheets × 4 tones
TONES_ALL = ['p','lt','b','v','s','sf','d','dk','dp','ltg','g','dkg']
SHEET_TONES = [TONES_ALL[i:i+4] for i in range(0, 12, 4)]

# 24 PCCS hues (PCCS ordering 1-24)
HUES = [
    (1,'pR','紫赤'),(2,'R','赤'),(3,'yR','赤(黄)'),(4,'rO','赤橙'),
    (5,'O','橙'),(6,'yO','黄橙'),(7,'rY','黄(赤)'),(8,'Y','黄'),
    (9,'gY','黄(緑)'),(10,'YG','黄緑'),(11,'yG','黄緑(黄)'),(12,'G','緑'),
    (13,'bG','緑(青)'),(14,'BG','青緑'),(15,'BG','青緑'),(16,'gB','緑青'),
    (17,'B','青'),(18,'B','青'),(19,'pB','紫青'),(20,'V','青紫'),
    (21,'bP','青紫(紫)'),(22,'P','紫'),(23,'rP','赤紫'),(24,'RP','赤紫(赤)'),
]

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def gf(size):
    if os.path.exists(FONT_PATH):
        return ImageFont.truetype(FONT_PATH, size)
    return ImageFont.load_default()


def draw_regmarks(draw, l, t, r, b):
    L = int(5 * MM)
    for (cx, cy) in [(l,t), (r,t), (l,b), (r,b)]:
        draw.line([(cx-L,cy),(cx+L,cy)], fill='#888888', width=2)
        draw.line([(cx,cy-L),(cx,cy+L)], fill='#888888', width=2)


def gen_sheet(idx, tones):
    img = Image.new('RGB', (W_PX, H_PX), '#FFFFFF')
    draw = ImageDraw.Draw(img)

    N_COLS = len(tones)  # 4
    N_ROWS = len(HUES)   # 24
    COL_W = GRID_W // N_COLS
    ROW_H = GRID_H // N_ROWS

    CHIP = int(10 * MM)  # 10mm × 10mm

    # Title
    ft = gf(26)
    title = f'PCCS 色卡スキャン用テンプレート  Sheet {idx+1}/3'
    tw = draw.textlength(title, font=ft)
    draw.text(((W_PX-tw)/2, int(4*MM)), title, fill='#000000', font=ft)

    # Subtitle
    fs = gf(14)
    tone_str = ' / '.join(tones)
    sub = f'トーン: {tone_str}'
    sw = draw.textlength(sub, font=fs)
    draw.text(((W_PX-sw)/2, int(4*MM)+32), sub, fill='#666666', font=fs)

    # Registration marks on grid corners
    draw_regmarks(draw, GRID_X, GRID_Y, GRID_X+GRID_W, GRID_Y+GRID_H)

    # Column headers (tone)
    fh = gf(15)
    for ci, tone in enumerate(tones):
        cx = GRID_X + ci * COL_W + COL_W // 2
        tw2 = draw.textlength(tone, font=fh)
        draw.text((cx-tw2/2, GRID_Y - int(6*MM)),
                 tone, fill='#333333', font=fh)

    # Row labels (hue # on left margin)
    frow = gf(10)
    for ri, (hnum, hcode, _) in enumerate(HUES):
        y_mid = GRID_Y + ri * ROW_H + ROW_H // 2
        lbl = f'{hnum}'
        draw.text((GRID_X - int(10*MM), y_mid-6), lbl, fill='#999999', font=frow)

    # Cells
    fcell = gf(12)
    fname = gf(9)

    for ri, (hnum, hcode, hname) in enumerate(HUES):
        y0 = GRID_Y + ri * ROW_H
        y1 = y0 + ROW_H
        y_mid = y0 + ROW_H // 2

        # Hue name on left margin
        draw.text((GRID_X - int(10*MM), y_mid + 6), hcode, fill='#aaaaaa', font=fname)

        for ci, tone in enumerate(tones):
            x0 = GRID_X + ci * COL_W
            x1 = x0 + COL_W

            # Cell border
            draw.rectangle([x0, y0, x1, y1], outline='#dddddd', width=1)

            # Chip area — 10mm × 10mm, centered vertically, right of label
            label_w = int(22 * MM)  # label area on left
            chip_x0 = x0 + label_w
            chip_x1 = chip_x0 + CHIP
            chip_y0 = y_mid - CHIP // 2
            chip_y1 = y_mid + CHIP // 2

            # Chip border (thick black)
            draw.rectangle([chip_x0, chip_y0, chip_x1, chip_y1],
                          outline='#000000', width=2)

            # For non-v tones, odd hues → show duplicate hint
            is_odd = hnum % 2 == 1
            is_v = (tone == 'v')
            if is_odd and not is_v:
                dup_hue = hnum + 1
                dup_code = [h[1] for h in HUES if h[0] == dup_hue][0]
                # Gray out the chip area to indicate "don't paste here"
                draw.rectangle([chip_x0+2, chip_y0+2, chip_x1-2, chip_y1-2],
                              fill='#f0f0f0')
                fdup = gf(11)
                dup_text = f'={dup_hue}'
                tw3 = draw.textlength(dup_text, font=fdup)
                draw.text((chip_x0 + (CHIP-tw3)/2, chip_y0 + (CHIP-14)/2),
                         dup_text, fill='#999999', font=fdup)

            # Tone-hue label (left of chip)
            label = f'{tone}-{hnum}:{hcode}'
            lbl_y = y_mid - 10
            draw.text((x0 + int(1.5*MM), lbl_y), label, fill='#000000', font=fcell)

            # Hue name below label
            draw.text((x0 + int(1.5*MM), lbl_y + 16), hname, fill='#888888', font=fname)

            # Tone code inside chip area (faint, as guide)
            fchip = gf(8)
            draw.text((chip_x0 + 3, chip_y1 + 1), tone, fill='#cccccc', font=fchip)

    # Footer
    ff = gf(11)
    footer = f'Sheet {idx+1}/3  |  A3 300dpi  |  貼付枠 10×10mm  |  色チップを黒枠内に貼付'
    fw2 = draw.textlength(footer, font=ff)
    draw.text(((W_PX-fw2)/2, H_PX - MARGIN - int(2*MM)),
             footer, fill='#999999', font=ff)

    return img


def gen_achromatic():
    W2, H2 = int(100*MM), int(70*MM)
    img = Image.new('RGB', (W2, H2), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    ft = gf(18)
    draw.text((int(5*MM), int(3*MM)), 'PCCS 無彩色', fill='#000000', font=ft)

    CHIP = int(10 * MM)
    GAP = int(6 * MM)
    fc = gf(13)

    achro = [('W','純白'),('Bk','純黒'),('Gy','灰色')]
    for i, (code, name) in enumerate(achro):
        x0 = int(5*MM) + i*(CHIP+GAP)
        y0 = int(14*MM)
        draw.rectangle([x0, y0, x0+CHIP, y0+CHIP], outline='#000000', width=2)
        draw.text((x0, y0+CHIP+int(1*MM)), f'{code}\n{name}', fill='#000000', font=fc)

    return img


if __name__ == '__main__':
    desk = os.path.expanduser('~/Desktop')
    outdir = f'{desk}/PCCS_template'
    os.makedirs(outdir, exist_ok=True)

    for si, tones in enumerate(SHEET_TONES):
        img = gen_sheet(si, tones)
        path = f'{outdir}/PCCS_Sheet_{si+1}_tones_{"_".join(tones)}.png'
        img.save(path, dpi=(DPI, DPI))
        print(f'Saved: {path} ({img.width}×{img.height}px)')

    img_a = gen_achromatic()
    path_a = f'{outdir}/PCCS_Sheet_4_achromatic.png'
    img_a.save(path_a, dpi=(DPI, DPI))
    print(f'Saved: {path_a} ({img_a.width}×{img_a.height}px)')

    print(f'\nDone. {outdir}/ に4枚出力。A3 (1-3) + 任意サイズ (4) で印刷。')
