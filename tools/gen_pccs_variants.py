"""
PCCS 配色技法 追加バリエーション — 全12トーン + 多様な色相を活用
"""
from PIL import Image, ImageDraw, ImageFont
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, '..', 'data', 'PCCS_HEX_data.json')) as f:
    PCCS = json.load(f)

HUES = {1:'pR',2:'R',3:'yR',4:'rO',5:'O',6:'yO',7:'rY',8:'Y',
        9:'gY',10:'YG',11:'yG',12:'G',13:'bG',14:'BG',15:'BG',16:'gB',
        17:'B',18:'B',19:'pB',20:'V',21:'bP',22:'P',23:'rP',24:'RP'}

def c(tone, hnum):
    return PCCS.get(f'{tone}-{hnum}:{HUES[hnum]}', '#ffffff')

CARDS = []

# ══════════════════════════════════
# 同一トーン配色 — 全 12 トーン各 1 枚
# ══════════════════════════════════
same_tone_variants = [
    # tone, hue_a, hue_b, step_size
    ('p',  2, 10, 8, 'pトーン統一'),
    ('lt', 4, 12, 8, 'ltトーン統一'),
    ('b',  6, 14, 8, 'bトーン統一'),
    ('s',  8, 16, 8, 'sトーン統一 (=b同色)'),
    ('sf', 10,18, 8, 'sfトーン統一'),
    ('d',  12,20, 8, 'dトーン統一'),
    ('dk', 14,22, 8, 'dkトーン統一'),
    ('dp', 16,24, 8, 'dpトーン統一'),
    ('ltg',2, 10, 8, 'ltgトーン統一'),
    ('g',  4, 12, 8, 'gトーン統一'),
    ('dkg',6, 14, 8, 'dkgトーン統一'),
    ('v',  20,4,  8, 'vトーン統一 (追加)'),
]
for tone, a, b, step_n, desc in same_tone_variants:
    CARDS.append({
        "num": f"10{tone}", "title": "同一トーン配色",
        "subtitle": f"2色 ｜ 歩数{step_n} ｜ 同一{desc} ｜ PCCS",
        "colors": [
            (f'{tone}-{a}:{HUES[a]}', c(tone,a)),
            (f'{tone}-{b}:{HUES[b]}', c(tone,b)),
        ]
    })

# ══════════════════════════════════
# 類似トーン配色 — 多様な隣接ペア
# ══════════════════════════════════
similar_variants = [
    ('b','v',  2, 10, 8, 'b-v 隣接'),
    ('lt','b', 4, 12, 8, 'lt-b 隣接'),
    ('s','d',  6, 14, 8, 's-d 隣接'),
    ('sf','g', 8, 16, 8, 'sf-g 隣接'),
    ('d','dk', 10,18, 8, 'd-dk 隣接'),
    ('v','dp', 12,20, 8, 'v-dp 隣接'),
    ('p','lt', 14,22, 8, 'p-lt 隣接'),
    ('g','dkg',16,24, 8, 'g-dkg 隣接'),
    ('ltg','d',2, 10, 8, 'ltg-d 隣接'),
    ('s','sf', 20,4,  8, 's-sf 隣接'),
]
for t1, t2, a, b, step_n, desc in similar_variants:
    CARDS.append({
        "num": "11v", "title": "類似トーン配色",
        "subtitle": f"2色 ｜ 歩数{step_n} ｜ {desc} ｜ PCCS",
        "colors": [
            (f'{t1}-{a}:{HUES[a]}', c(t1,a)),
            (f'{t2}-{b}:{HUES[b]}', c(t2,b)),
        ]
    })

# ══════════════════════════════════
# ダイアード — 多様なトーンペア
# ══════════════════════════════════
diad_variants = [
    ('sf','dkg', 8, 20, 'sf + dkg'),
    ('p','dp',   2, 14, 'p + dp (双対照)'),
    ('lt','dk',  4, 16, 'lt + dk'),
    ('g','dkg',  6, 18, 'g + dkg'),
    ('s','dp',   10,22, 's + dp'),
    ('b','dkg',  12,24, 'b + dkg (双対照)'),
]
for t1, t2, a, b, desc in diad_variants:
    CARDS.append({
        "num": "14v", "title": "ダイアード",
        "subtitle": f"2色 ｜ 歩数12 ｜ {desc} ｜ PCCS",
        "colors": [
            (f'{t1}-{a}:{HUES[a]}', c(t1,a)),
            (f'{t2}-{b}:{HUES[b]}', c(t2,b)),
        ]
    })

# ══════════════════════════════════
# 対照トーン配色 — 多様な対照
# ══════════════════════════════════
contrast_variants = [
    ('p','dp', 2, 14, 6, 'p×dp 双対照'),
    ('b','dkg',4, 22, 6, 'b×dkg 双対照'),
    ('lt','dk',6, 20, 6, 'lt×dk 明度対照'),
    ('v','ltg',8, 2,  6, 'v×ltg 彩度対照'),
    ('b','dk', 10,24, 6, 'b×dk 明度対照'),
    ('p','dk', 12,2,  6, 'p×dk 明度対照'),
]
for t1, t2, a, b, step_n, desc in contrast_variants:
    CARDS.append({
        "num": "17v", "title": "対照トーン配色",
        "subtitle": f"2色 ｜ 歩数{step_n} ｜ {desc} ｜ PCCS",
        "colors": [
            (f'{t1}-{a}:{HUES[a]}', c(t1,a)),
            (f'{t2}-{b}:{HUES[b]}', c(t2,b)),
        ]
    })

# ══════════════════════════════════
# ビコロール — 追加の vv ペア
# ══════════════════════════════════
bicol_variants = [
    (2, 12, 10), (4, 14, 10), (6, 16, 10), (10, 20, 10), (12, 22, 10),
    (1, 11, 10), (3, 13, 10), (5, 15, 10), (7, 17, 10), (9, 19, 10),
    (14, 24, 10), (16, 2, 10), (18, 4, 10), (20, 6, 10), (22, 8, 10), (24, 10, 10),
]
for a, b, step_n in bicol_variants:
    CARDS.append({
        "num": "16v", "title": "ビコロール配色\n② v同士",
        "subtitle": f"2色限定 ｜ v同士 歩数±10 (v-{a}:{HUES[a]} + v-{b}:{HUES[b]}) ｜ PCCS",
        "colors": [
            (f'v-{a}:{HUES[a]}', c('v',a)),
            (f'v-{b}:{HUES[b]}', c('v',b)),
        ]
    })

# ══════════════════════════════════
# トライアド — sf, g, dkg, s 混在
# ══════════════════════════════════
triad_variants = [
    (['sf-8:Y','g-16:gB','dkg-24:RP'], [c('sf',8),c('g',16),c('dkg',24)], 'sf+g+dkg 8+8歩'),
    (['p-2:R','s-10:YG','dk-18:B'], [c('p',2),c('s',10),c('dk',18)], 'p+s+dk 8+8歩'),
    (['ltg-4:rO','d-12:G','dp-20:V'], [c('ltg',4),c('d',12),c('dp',20)], 'ltg+d+dp 8+8歩'),
]
for labels, hexes, desc in triad_variants:
    CARDS.append({
        "num": "19v", "title": "トライアド配色",
        "subtitle": f"3色限定 ｜ 8+8歩 ｜ {desc} ｜ PCCS",
        "colors": list(zip(labels, hexes)),
    })

# ══════════════════════════════════
# テトラード — g, sf, ltg, dkg 混在
# ══════════════════════════════════
tetra_variants = [
    (['g-8:Y','sf-14:BG','dkg-20:V','s-2:R'], [c('g',8),c('sf',14),c('dkg',20),c('s',2)], 'g+sf+dkg+s 6+6+6歩'),
    (['ltg-4:rO','d-10:YG','dk-16:gB','dp-22:P'], [c('ltg',4),c('d',10),c('dk',16),c('dp',22)], 'ltg+d+dk+dp 6+6+6歩'),
]
for labels, hexes, desc in tetra_variants:
    CARDS.append({
        "num": "20v", "title": "テトラード配色",
        "subtitle": f"4色限定 ｜ 6+6+6歩 ｜ {desc} ｜ PCCS",
        "colors": list(zip(labels, hexes)),
    })

# ══════════════════════════════════
# ペンタード — sf, g, ltg 混在
# ══════════════════════════════════
CARDS.append({
    "num": "21v", "title": "ペンタード配色",
    "subtitle": "① W+Bk+sf(8+8) ｜ sf+g+dkg 混在 ｜ PCCS",
    "colors": [
        ("W", "#FFFFFF"), ("Bk", "#000000"),
        ("sf-8:Y", c('sf',8)), ("g-16:gB", c('g',16)), ("dkg-24:RP", c('dkg',24)),
    ]
})

# ══════════════════════════════════
# ヘクサード — 多様トーン
# ══════════════════════════════════
CARDS.append({
    "num": "22v", "title": "ヘクサード配色",
    "subtitle": "① テトラード+W+Bk ｜ p+lt+d+dk 混在 ｜ PCCS",
    "colors": [
        ("W", "#FFFFFF"), ("Bk", "#000000"),
        ("p-8:Y", c('p',8)), ("lt-14:BG", c('lt',14)),
        ("d-20:V", c('d',20)), ("dk-2:R", c('dk',2)),
    ]
})

# ══════════════════════════════════
# ドミナントトーン 追加トーン
# ══════════════════════════════════
CARDS.append({
    "num": "05v", "title": "亮色调\nドミナントトーン",
    "subtitle": "4色相(6+4+4歩) ｜ pトーン統一 ｜ PCCS",
    "colors": [
        ("p-4:rO", c('p',4)), ("p-10:YG", c('p',10)),
        ("p-14:BG", c('p',14)), ("p-18:B", c('p',18)),
    ]
})
CARDS.append({
    "num": "06v", "title": "暗色调\nドミナントトーン",
    "subtitle": "4色相(6+4+8歩) ｜ dkgトーン統一 ｜ PCCS",
    "colors": [
        ("dkg-2:R", c('dkg',2)), ("dkg-8:Y", c('dkg',8)),
        ("dkg-12:G", c('dkg',12)), ("dkg-20:V", c('dkg',20)),
    ]
})
CARDS.append({
    "num": "07v", "title": "鲜色调\nドミナントトーン",
    "subtitle": "4色相(6+6+6歩) ｜ sトーン統一 (=b同色) ｜ PCCS",
    "colors": [
        ("s-2:R", c('s',2)), ("s-8:Y", c('s',8)),
        ("s-14:BG", c('s',14)), ("s-20:V", c('s',20)),
    ]
})
CARDS.append({
    "num": "08v", "title": "低彩度\nドミナントトーン",
    "subtitle": "4色相(6+6+6歩) ｜ gトーン統一 ｜ PCCS",
    "colors": [
        ("g-2:R", c('g',2)), ("g-8:Y", c('g',8)),
        ("g-14:BG", c('g',14)), ("g-20:V", c('g',20)),
    ]
})
CARDS.append({
    "num": "09v", "title": "中彩度\nドミナントトーン",
    "subtitle": "4色相(6+4+6歩) ｜ sfトーン統一 ｜ PCCS",
    "colors": [
        ("sf-2:R", c('sf',2)), ("sf-8:Y", c('sf',8)),
        ("sf-12:G", c('sf',12)), ("sf-18:B", c('sf',18)),
    ]
})


# ═══════════════════
# PNG Generator
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

    ft = gf(24)
    title = card["title"].replace('\n', ' ')
    tw = draw.textlength(title, font=ft)
    draw.text(((CANVAS_W-tw)//2, 20), title, fill='#000000', font=ft)

    fs = gf(15)
    sw = draw.textlength(card["subtitle"], font=fs)
    draw.text(((CANVAS_W-sw)//2, 56), card["subtitle"], fill='#666666', font=fs)

    fb = gf(11)
    draw.text((CANVAS_W - 75, 12), 'PCCS', fill='#999999', font=fb)
    draw.text((CANVAS_W - 45, 28), card["num"], fill='#999999', font=fb)

    fl = gf(15)
    fh = gf(11)
    bt = 110
    ly = bt + BH + 12
    hy = ly + 20

    for i, (label, hex_color) in enumerate(colors):
        x = left_margin + i * (BW + GAP)
        if hex_color in ('#FFFFFF', '#ffffff'):
            r, g, b = 255, 255, 255
        elif hex_color in ('#000000', '#000000'):
            r, g, b = 0, 0, 0
        else:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
        draw.rectangle([x, bt, x+BW, bt+BH], fill=(r,g,b))
        if hex_color == '#FFFFFF':
            draw.rectangle([x, bt, x+BW, bt+BH], outline='#000000', width=1)
        lw = draw.textlength(label, font=fl)
        draw.text((x + (BW-lw)//2, ly), label, fill='#000000', font=fl)
        hw = draw.textlength(hex_color, font=fh)
        draw.text((x + (BW-hw)//2, hy), hex_color, fill='#999999', font=fh)
    return img


if __name__ == '__main__':
    desk = os.path.expanduser('~/Desktop/AIカラーカード')
    today = datetime.date.today().strftime('%Y-%m-%d')
    out_dir = f'{desk}/{today}'
    os.makedirs(out_dir, exist_ok=True)

    ok = 0
    for card in CARDS:
        prefix = '配色技法'
        title_flat = card['title'].replace('\n', ' ')
        fname = f'{out_dir}/{prefix}_{card["num"]}_{title_flat}.png'
        img = make_png(card)
        img.save(fname)
        ok += 1

    print(f'{ok} variant cards → {out_dir}/')
