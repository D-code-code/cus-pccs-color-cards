"""
PCCS 扫描画像から各色チップのHEX値を抽出 v6
Precise row centers from v-column scan + calibrated column centers
"""
from PIL import Image
import numpy as np
import json, os

HUES = [
    (1,'pR'),(2,'R'),(3,'yR'),(4,'rO'),
    (5,'O'),(6,'yO'),(7,'rY'),(8,'Y'),
    (9,'gY'),(10,'YG'),(11,'yG'),(12,'G'),
    (13,'bG'),(14,'BG'),(15,'BG'),(16,'gB'),
    (17,'B'),(18,'B'),(19,'pB'),(20,'V'),
    (21,'bP'),(22,'P'),(23,'rP'),(24,'RP'),
]

SRC = '/Users/d/Desktop/PCCS_template'  # 扫描画像のフォルダ（各自の環境に合わせて変更）

# Precise row centers from v-column vertical scan (Sheet 1)
# Missing/bad rows interpolated from neighbors
ROW_CENTERS = [
    799, 1024, 1255, 1489, 1709, 1935, 2150, 2379,
    2614, 2837, 3067, 3290, 3532, 3751, 3982, 4201,
    4424, 4580, 4656, 4882, 5101, 5331, 5558, 5800,
]
# Row 12 (was 3225 with height 3) → interpolated to 3290
# Row 19 (was 4505 with height 4) → interpolated to 4580
# Row 24 extended to 5800 (slightly beyond detected 5558 to capture full chip)

COL_CENTERS = {
    'Sheet_1': [700, 1730, 2740, 3750],
    'Sheet_2': [700, 1770, 2790, 3820],
    'Sheet_3': [700, 1765, 2750, 3750],
}


def load_portrait(path):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    if w > h:
        img = img.rotate(90, expand=True)
    return img


def sample_chip(arr, cy, cx, radius):
    y0 = max(0, cy - radius)
    y1 = min(arr.shape[0], cy + radius)
    x0 = max(0, cx - radius)
    x1 = min(arr.shape[1], cx + radius)
    if y1 <= y0 or x1 <= x0:
        return '#ffffff', False

    patch = arr[y0:y1, x0:x1]
    gray = np.min(patch, axis=2)

    # Filter paper white and border black
    mask = (gray > 30) & (gray < 248)
    if mask.sum() > 15:
        r = int(np.median(patch[mask, 0]))
        g = int(np.median(patch[mask, 1]))
        b = int(np.median(patch[mask, 2]))
        return f'#{r:02x}{g:02x}{b:02x}', True
    else:
        r = int(np.median(patch[:,:,0]))
        g = int(np.median(patch[:,:,1]))
        b = int(np.median(patch[:,:,2]))
        return f'#{r:02x}{g:02x}{b:02x}', False


def extract_sheet(arr, col_centers, tones):
    n_cols = len(tones)
    n_rows = len(HUES)
    radius = 40

    colors = {}
    for ri, (hnum, hcode) in enumerate(HUES):
        row_center = ROW_CENTERS[ri]

        for ci, tone in enumerate(tones):
            col_center = col_centers[ci]
            hex_val, has = sample_chip(arr, row_center, col_center, radius)
            key = f'{tone}-{hnum}:{hcode}'
            colors[key] = {'hex': hex_val, 'has_chip': has}

    for tone in tones:
        pasted = sum(1 for k in colors if k.startswith(tone+'-') and colors[k]['has_chip'])
        print(f'  {tone}: {pasted} chips')

    return colors


def post_process(all_colors):
    # s = b
    for hnum, hcode in HUES:
        ks = f's-{hnum}:{hcode}'
        kb = f'b-{hnum}:{hcode}'
        if ks in all_colors and kb in all_colors:
            all_colors[ks]['hex'] = all_colors[kb]['hex']
            all_colors[ks]['has_chip'] = all_colors[kb]['has_chip']

    # Non-v odd → even
    non_v = ['p','lt','b','s','sf','d','dk','dp','ltg','g','dkg']
    for tone in non_v:
        for hnum, hcode in HUES:
            if hnum % 2 == 1:
                k_odd = f'{tone}-{hnum}:{hcode}'
                next_h = hnum + 1
                if next_h <= 24:
                    next_code = [h[1] for h in HUES if h[0] == next_h][0]
                    k_even = f'{tone}-{next_h}:{next_code}'
                    if k_odd in all_colors and k_even in all_colors:
                        all_colors[k_odd]['hex'] = all_colors[k_even]['hex']
                        all_colors[k_odd]['has_chip'] = all_colors[k_even]['has_chip']

    # v tone: odd → even for positions with no chip
    for hnum, hcode in HUES:
        if hnum % 2 == 1:
            k_odd = f'v-{hnum}:{hcode}'
            next_h = hnum + 1
            if next_h <= 24:
                next_code = [h[1] for h in HUES if h[0] == next_h][0]
                k_even = f'v-{next_h}:{next_code}'
                if k_odd in all_colors and k_even in all_colors:
                    if not all_colors[k_odd]['has_chip']:
                        all_colors[k_odd]['hex'] = all_colors[k_even]['hex']
                        all_colors[k_odd]['has_chip'] = True

    clean = {}
    for key, val in all_colors.items():
        clean[key] = val['hex']
    return clean


if __name__ == '__main__':
    all_colors = {}

    sheets = [
        ('Sheet_1', f'{SRC}/PCCS_Sheet_1_tones_p_lt_b_v.jpg', ['p','lt','b','v']),
        ('Sheet_2', f'{SRC}/PCCS_Sheet_2_tones_s_sf_d_dk.jpg', ['s','sf','d','dk']),
        ('Sheet_3', f'{SRC}/PCCS_Sheet_3_tones_dp_ltg_g_dkg.jpg', ['dp','ltg','g','dkg']),
    ]

    for name, path, tones in sheets:
        print(f'\n═══ {name} ═══')
        img = load_portrait(path)
        arr = np.array(img)
        centers = COL_CENTERS[name]
        colors = extract_sheet(arr, centers, tones)
        all_colors.update(colors)

    print(f'\n═══ Post-processing ═══')
    clean = post_process(all_colors)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'PCCS_HEX_data.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(clean, f, indent=2, ensure_ascii=False)

    # Summary
    white = sum(1 for v in clean.values() if v == '#ffffff')
    print(f'\nTotal: {len(clean)} | Missing: {white} | Valid: {len(clean)-white}')

    # Print all RP (hue 24) values
    print('\n=== RP (hue 24) verification ===')
    for tone in ['v','p','lt','b','s','sf','d','dk','dp','ltg','g','dkg']:
        key = f'{tone}-24:RP'
        print(f'  {key} = {clean.get(key, "N/A")}')

    print(f'\nSaved: {out}')
