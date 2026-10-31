"""
PCCS 四大原理 + 15配色技法 一括PNG色卡生成
新標準: PCCS HEXデータ + PCCS類似/対照色調 + 技法互換
"""
from PIL import Image, ImageDraw, ImageFont
import json, os, datetime

# ═══════════════════
# Load PCCS data
# ═══════════════════
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, '..', 'data', 'PCCS_HEX_data.json')) as f:
    PCCS = json.load(f)

# ═══════════════════
# PCCS Hue metadata
# ═══════════════════
HUES = [(1,'pR'),(2,'R'),(3,'yR'),(4,'rO'),(5,'O'),(6,'yO'),(7,'rY'),(8,'Y'),
        (9,'gY'),(10,'YG'),(11,'yG'),(12,'G'),(13,'bG'),(14,'BG'),(15,'BG'),(16,'gB'),
        (17,'B'),(18,'B'),(19,'pB'),(20,'V'),(21,'bP'),(22,'P'),(23,'rP'),(24,'RP')]

def hue_name(n):
    for hnum, hcode in HUES:
        if hnum == n: return hcode
    return str(n)

def step(a, b):
    """歩数 (clockwise only)"""
    if a <= b: return b - a
    return (24 - a) + b

def color(tone, hnum):
    """Get HEX from PCCS data"""
    hcode = hue_name(hnum)
    key = f'{tone}-{hnum}:{hcode}'
    return PCCS.get(key, '#ffffff')

# ═══════════════════
# Card definitions
# ═══════════════════
CARDS = []

# ── 四大原理 ──

# 秩序原理: 2+2歩, 3色相  8:Y→10:YG(2)→12:G(2)
CARDS.append({
    "num": "P01", "title": "秩序原理",
    "subtitle": "2+2歩 ｜ 3色相 ｜ 8:Y → 10:YG → 12:G ｜ PCCS",
    "colors": [
        ("v-8:Y", color('v',8)),
        ("d-10:YG", color('d',10)),
        ("dp-12:G", color('dp',12)),
    ]
})

# 馴染み原理: 4+5歩, 3色相  14:BG→18:B(4)→23:rP(5)
CARDS.append({
    "num": "P02", "title": "馴染み原理",
    "subtitle": "4+5歩 ｜ 3色相 ｜ 14:BG → 18:B → 23:rP ｜ PCCS",
    "colors": [
        ("v-14:BG", color('v',14)),
        ("d-18:B", color('d',18)),
        ("dp-23:rP", color('dp',23)),
    ]
})

# 類似性原理: 0歩, 1色相  2:R 同一色相×4トーン
CARDS.append({
    "num": "P03", "title": "類似性原理",
    "subtitle": "0歩 ｜ 1色相 ｜ 2:R 同一色相 × 4トーン ｜ PCCS",
    "colors": [
        ("p-2:R", color('p',2)),
        ("lt-2:R", color('lt',2)),
        ("v-2:R", color('v',2)),
        ("dp-2:R", color('dp',2)),
    ]
})

# 明瞭性原理: 12+2歩, 3色相  8:Y→20:V(12)→22:P(2)
CARDS.append({
    "num": "P04", "title": "明瞭性原理",
    "subtitle": "12+2歩 ｜ 3色相 ｜ 8:Y → 20:V → 22:P ｜ PCCS",
    "colors": [
        ("v-8:Y", color('v',8)),
        ("d-20:V", color('d',20)),
        ("dp-22:P", color('dp',22)),
    ]
})

# ── 技法1: ドミナントカラー配色 (4亜種) ──

# 1-1. 中低彩度暖色系: 暖(2-11)×2色相(2歩) | lt, d, dk all appear
CARDS.append({
    "num": "01", "title": "中低彩度暖色系\nドミナントカラー",
    "subtitle": "暖色系×2色相(2歩) ｜ lt, d, dk すべて出現 ｜ PCCS",
    "colors": [
        ("lt-2:R", color('lt',2)),
        ("d-4:rO", color('d',4)),
        ("dk-2:R", color('dk',2)),
    ]
})

# 1-2. 高彩度暖色系: 暖×3色相(2+2歩) | b, v, dp all appear
CARDS.append({
    "num": "02", "title": "高彩度暖色系\nドミナントカラー",
    "subtitle": "暖色系×3色相(2+2歩) ｜ b, v, dp すべて出現 ｜ PCCS",
    "colors": [
        ("b-2:R", color('b',2)),
        ("v-4:rO", color('v',4)),
        ("dp-6:yO", color('dp',6)),
    ]
})

# 1-3. 中低彩度寒色系: 寒(14-19)×3色相(2+2歩) | p, d all appear
CARDS.append({
    "num": "03", "title": "中低彩度寒色系\nドミナントカラー",
    "subtitle": "寒色系×3色相(2+2歩) ｜ p, d すべて出現 ｜ PCCS",
    "colors": [
        ("p-14:BG", color('p',14)),
        ("d-16:gB", color('d',16)),
        ("d-18:B", color('d',18)),
    ]
})

# 1-4. 高彩度寒色系: 寒×3色相(1+1歩) | b, v all appear
CARDS.append({
    "num": "04", "title": "高彩度寒色系\nドミナントカラー",
    "subtitle": "寒色系×3色相(1+1歩) ｜ b, v すべて出現 ｜ PCCS",
    "colors": [
        ("b-14:BG", color('b',14)),
        ("v-15:BG", color('v',15)),
        ("b-16:gB", color('b',16)),
    ]
})

# ── 技法2: ドミナントトーン配色 (5亜種) ──

# 2-1. 亮色调: 4色相(6+4+4歩) | p/lt/b の1種統一
CARDS.append({
    "num": "05", "title": "亮色调\nドミナントトーン",
    "subtitle": "4色相(6+4+4歩) ｜ ltトーン統一 ｜ PCCS",
    "colors": [
        ("lt-4:rO", color('lt',4)),
        ("lt-10:YG", color('lt',10)),
        ("lt-14:BG", color('lt',14)),
        ("lt-18:B", color('lt',18)),
    ]
})

# 2-2. 暗色调: 4色相(6+4+8歩) | dk/dp/dkg の1種統一
CARDS.append({
    "num": "06", "title": "暗色调\nドミナントトーン",
    "subtitle": "4色相(6+4+8歩) ｜ dkトーン統一 ｜ PCCS",
    "colors": [
        ("dk-2:R", color('dk',2)),
        ("dk-8:Y", color('dk',8)),
        ("dk-12:G", color('dk',12)),
        ("dk-20:V", color('dk',20)),
    ]
})

# 2-3. 鲜色调: 4色相(6+6+6歩) | v/b/dp の1種統一
CARDS.append({
    "num": "07", "title": "鲜色调\nドミナントトーン",
    "subtitle": "4色相(6+6+6歩) ｜ vトーン統一 ｜ PCCS",
    "colors": [
        ("v-2:R", color('v',2)),
        ("v-8:Y", color('v',8)),
        ("v-14:BG", color('v',14)),
        ("v-20:V", color('v',20)),
    ]
})

# 2-4. 低彩度: 4色相(6+6+6歩) | ltg/g の1種統一
CARDS.append({
    "num": "08", "title": "低彩度\nドミナントトーン",
    "subtitle": "4色相(6+6+6歩) ｜ ltgトーン統一 ｜ PCCS",
    "colors": [
        ("ltg-2:R", color('ltg',2)),
        ("ltg-8:Y", color('ltg',8)),
        ("ltg-14:BG", color('ltg',14)),
        ("ltg-20:V", color('ltg',20)),
    ]
})

# 2-5. 中彩度: 4色相(6+4+6歩) | d/sf の1種統一
CARDS.append({
    "num": "09", "title": "中彩度\nドミナントトーン",
    "subtitle": "4色相(6+4+6歩) ｜ dトーン統一 ｜ PCCS",
    "colors": [
        ("d-2:R", color('d',2)),
        ("d-8:Y", color('d',8)),
        ("d-12:G", color('d',12)),
        ("d-18:B", color('d',18)),
    ]
})

# ── 技法3: 同一トーン配色 ──
CARDS.append({
    "num": "10", "title": "同一トーン配色",
    "subtitle": "2色 ｜ 歩数8 ｜ 同一vトーン ｜ PCCS",
    "colors": [
        ("v-2:R", color('v',2)),
        ("v-10:YG", color('v',10)),
    ]
})

# ── 技法4: 類似トーン配色 ──
# sf-ltg は隣接 (§5.4: sf ─ p, lt, b, s, d, g, ltg ... ltg ─ p, lt, sf, d, g)
CARDS.append({
    "num": "11", "title": "類似トーン配色",
    "subtitle": "2色 ｜ 歩数8 ｜ sf-ltg 類似色調 ｜ PCCS",
    "colors": [
        ("sf-2:R", color('sf',2)),
        ("ltg-10:YG", color('ltg',10)),
    ]
})

# ── 技法5: 対照色相配色 ──
# 3色相 8+1歩  2:R→10:YG(8)→11:yG(1)
CARDS.append({
    "num": "12", "title": "対照色相配色",
    "subtitle": "3色相(8+1歩) ｜ 2色相時=8〜10歩 ｜ 色相2〜3種 ｜ PCCS",
    "colors": [
        ("v-2:R", color('v',2)),
        ("lt-10:YG", color('lt',10)),
        ("b-11:yG", color('b',11)),
    ]
})

# ── 技法6: 補色色相配色 ──
# 3色相 11+1歩  2:R→13:bG(11)→14:BG(1)
CARDS.append({
    "num": "13", "title": "補色色相配色",
    "subtitle": "3色相(11+1歩) ｜ 2色相時=11〜12歩 ｜ 色相2〜3種 ｜ PCCS",
    "colors": [
        ("v-2:R", color('v',2)),
        ("lt-13:bG", color('lt',13)),
        ("b-14:BG", color('b',14)),
    ]
})

# ── 技法7: ダイアード ──
CARDS.append({
    "num": "14", "title": "ダイアード",
    "subtitle": "2色 ｜ 歩数12 ｜ トーン1〜2種 任意 ｜ PCCS",
    "colors": [
        ("v-8:Y", color('v',8)),
        ("d-20:V", color('d',20)),
    ]
})

# ── 技法8: トリコロール配色 ──
CARDS.append({
    "num": "15", "title": "トリコロール配色",
    "subtitle": "3色 ｜ v同士歩数9 + 純白W ｜ PCCS",
    "colors": [
        ("v-23:rP", color('v',23)),
        ("v-8:Y", color('v',8)),
        ("W", "#FFFFFF"),
    ]
})

# ── 技法9: ビコロール配色 ① ──
CARDS.append({
    "num": "16a", "title": "ビコロール配色\n① W+v",
    "subtitle": "2色限定 ｜ W + 任意のv 1色 ｜ PCCS",
    "colors": [
        ("W", "#FFFFFF"),
        ("v-2:R", color('v',2)),
    ]
})

# ── 技法9: ビコロール配色 ② ──
CARDS.append({
    "num": "16b", "title": "ビコロール配色\n② v同士",
    "subtitle": "2色限定 ｜ v同士 歩数±10 ｜ PCCS",
    "colors": [
        ("v-8:Y", color('v',8)),
        ("v-18:B", color('v',18)),
    ]
})

# ── 技法10: 対照トーン配色 ──
# 彩度対照: v(高彩度) × ltg(低彩度)
CARDS.append({
    "num": "17", "title": "対照トーン配色",
    "subtitle": "2色 ｜ 歩数8 ｜ v×ltg 彩度対照 ｜ PCCS",
    "colors": [
        ("v-2:R", color('v',2)),
        ("ltg-10:YG", color('ltg',10)),
    ]
})

# ── 技法11: スプリット・コンプリメンタリー ──
CARDS.append({
    "num": "18", "title": "スプリット・\nコンプリメンタリー",
    "subtitle": "3色 ｜ 歩数 2+11 (18:B→20:V→8:Y) ｜ PCCS",
    "colors": [
        ("v-18:B", color('v',18)),
        ("d-20:V", color('d',20)),
        ("b-8:Y", color('b',8)),
    ]
})

# ── 技法12: トライアド配色 ──
CARDS.append({
    "num": "19", "title": "トライアド配色",
    "subtitle": "3色限定 ｜ 8+8歩 ｜ トーン1〜3種任意 ｜ PCCS",
    "colors": [
        ("lt-8:Y", color('lt',8)),
        ("v-16:gB", color('v',16)),
        ("dp-24:RP", color('dp',24)),
    ]
})

# ── 技法13: テトラード配色 ──
CARDS.append({
    "num": "20", "title": "テトラード配色",
    "subtitle": "4色限定 ｜ 6+6+6歩 ｜ トーン1〜4種任意 ｜ PCCS",
    "colors": [
        ("v-8:Y", color('v',8)),
        ("d-14:BG", color('d',14)),
        ("b-20:V", color('b',20)),
        ("dp-2:R", color('dp',2)),
    ]
})

# ── 技法14: ペンタード配色 ──
CARDS.append({
    "num": "21", "title": "ペンタード配色",
    "subtitle": "① W+Bk+3色(8+8) ｜ 任意トーン ｜ PCCS",
    "colors": [
        ("W", "#FFFFFF"),
        ("Bk", "#000000"),
        ("lt-8:Y", color('lt',8)),
        ("b-16:gB", color('b',16)),
        ("dp-24:RP", color('dp',24)),
    ]
})

# ── 技法15: ヘクサード配色 ──
CARDS.append({
    "num": "22", "title": "ヘクサード配色",
    "subtitle": "① テトラード+W+Bk ｜ 任意トーン ｜ PCCS",
    "colors": [
        ("W", "#FFFFFF"),
        ("Bk", "#000000"),
        ("v-8:Y", color('v',8)),
        ("d-14:BG", color('d',14)),
        ("b-20:V", color('b',20)),
        ("dp-2:R", color('dp',2)),
    ]
})


# ═══════════════════
# PNG Layout
# ═══════════════════
CANVAS_W, CANVAS_H = 1200, 600
FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def gf(size):
    if os.path.exists(FONT_PATH):
        return ImageFont.truetype(FONT_PATH, size)
    return ImageFont.load_default()

def make_png(card):
    colors = card["colors"]
    n = len(colors)

    if n <= 2:   BW, BH, GAP = 200, 260, 30
    elif n <= 3: BW, BH, GAP = 170, 230, 22
    elif n == 4: BW, BH, GAP = 150, 200, 18
    elif n <= 5: BW, BH, GAP = 135, 180, 16
    else:        BW, BH, GAP = 115, 155, 14

    total_w = n * BW + (n - 1) * GAP
    left_margin = (CANVAS_W - total_w) // 2

    img = Image.new('RGB', (CANVAS_W, CANVAS_H), '#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Title
    ft = gf(26)
    title = card["title"].replace('\n', ' ')
    tw = draw.textlength(title, font=ft)
    draw.text(((CANVAS_W-tw)//2, 24), title, fill='#000000', font=ft)

    # Subtitle
    fs = gf(16)
    sub = card["subtitle"]
    sw = draw.textlength(sub, font=fs)
    draw.text(((CANVAS_W-sw)//2, 62), sub, fill='#666666', font=fs)

    # PCCS badge (右上)
    fbadge = gf(12)
    draw.text((CANVAS_W - 80, 16), 'PCCS', fill='#999999', font=fbadge)

    # Number badge
    draw.text((CANVAS_W - 50, 34), card["num"], fill='#999999', font=fbadge)

    # Color blocks
    block_top = 120
    label_y = block_top + BH + 14
    hex_y = label_y + 22

    fl = gf(16)
    fh = gf(12)

    for i, (label, hex_color) in enumerate(colors):
        x = left_margin + i * (BW + GAP)

        # Block fill
        if hex_color in ('#FFFFFF', '#ffffff'):
            r, g, b = 255, 255, 255
        elif hex_color in ('#000000', '#000000'):
            r, g, b = 0, 0, 0
        else:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)

        draw.rectangle([x, block_top, x+BW, block_top+BH], fill=(r,g,b))

        # White block border
        if hex_color == '#FFFFFF':
            draw.rectangle([x, block_top, x+BW, block_top+BH], outline='#000000', width=1)

        # Label
        lw = draw.textlength(label, font=fl)
        draw.text((x + (BW-lw)//2, label_y), label, fill='#000000', font=fl)

        # HEX
        hw = draw.textlength(hex_color, font=fh)
        draw.text((x + (BW-hw)//2, hex_y), hex_color, fill='#999999', font=fh)

    return img


if __name__ == '__main__':
    desk = os.path.expanduser('~/Desktop/AIカラーカード')
    today = datetime.date.today().strftime('%Y-%m-%d')
    out_dir = f'{desk}/{today}'
    os.makedirs(out_dir, exist_ok=True)

    ok = 0
    for card in CARDS:
        prefix = '四大原理' if card['num'].startswith('P') else '配色技法'
        title_flat = card['title'].replace('\n', ' ')
        fname = f'{out_dir}/{prefix}_{card["num"]}_{title_flat}.png'

        img = make_png(card)
        img.save(fname)
        print(f'  [{card["num"]}] {title_flat[:50]} → {fname}')
        ok += 1

    print(f'\n{ok} cards generated → {out_dir}/')
