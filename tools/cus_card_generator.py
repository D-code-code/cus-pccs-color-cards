"""
CUS 色卡生成器 — PNG 预览 + PSD 多层可编辑
Photoshop ExtendScript 驱动，每个色块独立 paint 图层，文字独立 text 图层

支持两种模式：
  GROUPS（多组）— 三原理等，多行每组独立标题
  COLORS（单组）— 单行色卡

用法：修改数据后运行
    python3 cus_card_generator.py
"""
import subprocess, os, json
from PIL import Image, ImageDraw, ImageFont

# ═══════════════════════════════════════════
# 配色数据
# ═══════════════════════════════════════════

# 多组模式：三原理 4色色卡
GROUPS = [
    {
        "title": "秩序原理",
        "subtitle": "1Y + 3YG + 5G",
        "colors": [
            ("vv-1Y",  "#fee101"),
            ("dl-1Y",  "#ab951d"),
            ("vv-3YG", "#abcd05"),
            ("dp-5G",  "#01853a"),
        ]
    },
    {
        "title": "類似性原理",
        "subtitle": "19R 同一色相",
        "colors": [
            ("pl-19R", "#fcefef"),
            ("cl-19R", "#f8c6bd"),
            ("vv-19R", "#de0144"),
            ("dp-19R", "#ad3334"),
        ]
    },
    {
        "title": "明瞭性原理",
        "subtitle": "7BG + 19R + 17RP",
        "colors": [
            ("vv-7BG",  "#009c84"),
            ("dp-7BG",  "#007855"),
            ("vv-19R",  "#de0144"),
            ("vv-17RP", "#d50080"),
        ]
    },
]

# 单组模式（GROUPS 为空列表时生效）
TITLE = "明瞭性"
SUBTITLE = "1Y + 13V + 11B"
COLORS = [
    ("vv-1Y",  "#fee101"),
    ("dl-1Y",  "#ab951d"),
    ("vv-13V", "#4c4298"),
    ("pl-11B", "#e0eaf6"),
    ("dp-11B", "#00508f"),
]

# ═══════════════════════════════════════════
# 版式参数
# ═══════════════════════════════════════════
use_groups = bool(GROUPS)
CANVAS_W = 996
BLOCK_W = 150
BLOCK_H = 200
GAP = 18
FONT_PS_NAME = "HiraginoSans-W8"
FONT_SIZE_TITLE = 24
FONT_SIZE_SUBTITLE = 16
FONT_SIZE_LABEL = 16
FONT_SIZE_HEX = 12

if use_groups:
    n = max(len(g["colors"]) for g in GROUPS)
else:
    n = len(COLORS)
total_blocks_w = n * BLOCK_W + (n - 1) * GAP
left_margin = (CANVAS_W - total_blocks_w) // 2
center_x = CANVAS_W // 2

# Multi-row layout
BLOCK_Y_OFF = 55
LABEL_Y_OFF = BLOCK_H + 18
HEX_Y_OFF   = BLOCK_H + 38
ROW_H = 350

def row_ybase(idx):
    return 40 + idx * ROW_H  # 40, 440, 840

if use_groups:
    canvas_h = row_ybase(len(GROUPS) - 1) + ROW_H
    OUTPUT_BASE = os.path.expanduser("~/Desktop/三原理_4色色卡")
else:
    BLOCK_Y = 96
    LABEL_Y = BLOCK_Y + BLOCK_H + 14
    canvas_h = LABEL_Y + 30 + 40
    OUTPUT_BASE = os.path.expanduser(f"~/Desktop/{TITLE}_色卡")


def make_png():
    img = Image.new("RGB", (CANVAS_W, canvas_h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
    ft = fl = fs = None
    if os.path.exists(font_path):
        ft = ImageFont.truetype(font_path, FONT_SIZE_TITLE)
        fl = ImageFont.truetype(font_path, FONT_SIZE_LABEL)
        fs = ImageFont.truetype(font_path, FONT_SIZE_HEX)

    if use_groups:
        for gi, grp in enumerate(GROUPS):
            yb = row_ybase(gi)
            block_top = yb + BLOCK_Y_OFF

            tw = draw.textlength(grp["title"], font=ft) if ft else len(grp["title"]) * 14
            draw.text(((CANVAS_W - tw) / 2, yb), grp["title"], fill="#000000", font=ft)

            sw = draw.textlength(grp["subtitle"], font=fl) if fl else len(grp["subtitle"]) * 10
            draw.text(((CANVAS_W - sw) / 2, yb + 28), grp["subtitle"], fill="#000000", font=fl)

            for ci, (label, hex_color) in enumerate(grp["colors"]):
                bx = left_margin + ci * (BLOCK_W + GAP)
                rgb = tuple(int(hex_color[j:j+2], 16) for j in (1, 3, 5))
                draw.rectangle([bx, block_top, bx + BLOCK_W, block_top + BLOCK_H], fill=rgb)

                lw = draw.textlength(label, font=fl) if fl else len(label) * 10
                draw.text((bx + (BLOCK_W - lw) / 2, block_top + LABEL_Y_OFF), label, fill="#000000", font=fl)

                hw = draw.textlength(hex_color, font=fs) if fs else len(hex_color) * 7
                draw.text((bx + (BLOCK_W - hw) / 2, block_top + HEX_Y_OFF), hex_color, fill="#000000", font=fs)
    else:
        tw = draw.textlength(TITLE, font=ft) if ft else len(TITLE) * 16
        draw.text(((CANVAS_W - tw) / 2, 30), TITLE, fill="#000000", font=ft)

        sw = draw.textlength(SUBTITLE, font=fl) if fl else len(SUBTITLE) * 10
        draw.text(((CANVAS_W - sw) / 2, 62), SUBTITLE, fill="#000000", font=fl)

        for i, (label, hex_color) in enumerate(COLORS):
            x = left_margin + i * (BLOCK_W + GAP)
            rgb = tuple(int(hex_color[j:j+2], 16) for j in (1, 3, 5))
            draw.rectangle([x, BLOCK_Y, x + BLOCK_W, BLOCK_Y + BLOCK_H], fill=rgb)
            lw = draw.textlength(label, font=fl) if fl else len(label) * 10
            draw.text((x + (BLOCK_W - lw) / 2, LABEL_Y), label, fill="#000000", font=fl)

    png_path = f"{OUTPUT_BASE}.png"
    img.save(png_path)
    return png_path


def make_psd():
    if use_groups:
        return _make_psd_multi()
    else:
        return _make_psd_single()


def _make_psd_single():
    block_entries = []
    for i, (label, h) in enumerate(COLORS):
        r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
        x1 = left_margin + i * (BLOCK_W + GAP)
        x2 = x1 + BLOCK_W
        y1 = BLOCK_Y
        y2 = BLOCK_Y + BLOCK_H
        block_entries.append(json.dumps({
            "label": label, "r": r, "g": g, "b": b,
            "x1": x1, "y1": y1, "x2": x2, "y2": y2
        }))

    jsx = f'''// CUS 色卡 — {TITLE}
#target photoshop
app.bringToFront();

var doc = app.documents.add({CANVAS_W}, {canvas_h}, 72, "{TITLE}_色卡", NewDocumentMode.RGB);
var white = new SolidColor();
white.rgb.red = 255; white.rgb.green = 255; white.rgb.blue = 255;
var black = new SolidColor();
black.rgb.red = 0; black.rgb.green = 0; black.rgb.blue = 0;

doc.selection.selectAll();
doc.selection.fill(white);
doc.selection.deselect();

var titleLayer = doc.artLayers.add();
titleLayer.name = "title";
titleLayer.kind = LayerKind.TEXT;
titleLayer.textItem.contents = "{TITLE}";
titleLayer.textItem.size = {FONT_SIZE_TITLE};
titleLayer.textItem.color = black;
titleLayer.textItem.position = [{center_x}, 30];
titleLayer.textItem.justification = Justification.CENTER;

var subLayer = doc.artLayers.add();
subLayer.name = "subtitle";
subLayer.kind = LayerKind.TEXT;
subLayer.textItem.contents = "{SUBTITLE}";
subLayer.textItem.size = {FONT_SIZE_LABEL};
subLayer.textItem.color = black;
subLayer.textItem.position = [{center_x}, 62];
subLayer.textItem.justification = Justification.CENTER;

var blocks = [{", ".join(block_entries)}];

for (var i = blocks.length - 1; i >= 0; i--) {{
    var b = blocks[i];

    var bl = doc.artLayers.add();
    bl.name = b.label;
    doc.selection.select([[b.x1, b.y1], [b.x2, b.y1], [b.x2, b.y2], [b.x1, b.y2]]);
    var c = new SolidColor();
    c.rgb.red = b.r; c.rgb.green = b.g; c.rgb.blue = b.b;
    doc.selection.fill(c);
    doc.selection.deselect();

    var tl = doc.artLayers.add();
    tl.name = b.label + "_label";
    tl.kind = LayerKind.TEXT;
    tl.textItem.contents = b.label;
    tl.textItem.size = {FONT_SIZE_LABEL};
    tl.textItem.color = black;
    tl.textItem.position = [b.x1 + {BLOCK_W // 2}, {LABEL_Y}];
    tl.textItem.justification = Justification.CENTER;
}}

var psdFile = new File("{OUTPUT_BASE}.psd");
var psdOpts = new PhotoshopSaveOptions();
psdOpts.layers = true;
doc.saveAs(psdFile, psdOpts, true);
doc.close(SaveOptions.DONOTSAVECHANGES);
'''

    return _run_ps_jsx(jsx)


def _make_psd_multi():
    # Build block and text instructions
    block_lines = []
    text_lines = []

    for gi, grp in enumerate(GROUPS):
        yb = row_ybase(gi)
        block_top = yb + BLOCK_Y_OFF
        label_y = block_top + LABEL_Y_OFF
        hex_y = block_top + HEX_Y_OFF

        # Text: title + subtitle
        text_lines.append(f'// ── {grp["title"]} ──')
        text_lines.append(f'var t{gi}_title = doc.artLayers.add();')
        text_lines.append(f't{gi}_title.name = "title_{gi}";')
        text_lines.append(f't{gi}_title.kind = LayerKind.TEXT;')
        text_lines.append(f't{gi}_title.textItem.contents = "{grp["title"]}";')
        text_lines.append(f't{gi}_title.textItem.size = {FONT_SIZE_TITLE};')
        text_lines.append(f't{gi}_title.textItem.color = black;')
        text_lines.append(f't{gi}_title.textItem.position = [{center_x}, {yb}];')
        text_lines.append(f't{gi}_title.textItem.justification = Justification.CENTER;')

        text_lines.append(f'var t{gi}_sub = doc.artLayers.add();')
        text_lines.append(f't{gi}_sub.name = "subtitle_{gi}";')
        text_lines.append(f't{gi}_sub.kind = LayerKind.TEXT;')
        text_lines.append(f't{gi}_sub.textItem.contents = "{grp["subtitle"]}";')
        text_lines.append(f't{gi}_sub.textItem.size = {FONT_SIZE_SUBTITLE};')
        text_lines.append(f't{gi}_sub.textItem.color = black;')
        text_lines.append(f't{gi}_sub.textItem.position = [{center_x}, {yb + 28}];')
        text_lines.append(f't{gi}_sub.textItem.justification = Justification.CENTER;')

        # Blocks + labels
        for ci, (label, h) in enumerate(grp["colors"]):
            r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
            bx = left_margin + ci * (BLOCK_W + GAP)
            cx = bx + BLOCK_W // 2

            # Block paint layer
            block_lines.append(f'// {label}')
            block_lines.append(f'var bl{gi}_{ci} = doc.artLayers.add();')
            block_lines.append(f'bl{gi}_{ci}.name = "{label}";')
            block_lines.append(f'doc.selection.select([[{bx},{block_top}],[{bx+BLOCK_W},{block_top}],[{bx+BLOCK_W},{block_top+BLOCK_H}],[{bx},{block_top+BLOCK_H}]]);')
            block_lines.append(f'var c{gi}_{ci} = new SolidColor();')
            block_lines.append(f'c{gi}_{ci}.rgb.red = {r}; c{gi}_{ci}.rgb.green = {g}; c{gi}_{ci}.rgb.blue = {b};')
            block_lines.append(f'doc.selection.fill(c{gi}_{ci});')
            block_lines.append(f'doc.selection.deselect();')

            # Label text (tone code)
            text_lines.append(f'var tl{gi}_{ci} = doc.artLayers.add();')
            text_lines.append(f'tl{gi}_{ci}.name = "{label}_label";')
            text_lines.append(f'tl{gi}_{ci}.kind = LayerKind.TEXT;')
            text_lines.append(f'tl{gi}_{ci}.textItem.contents = "{label}";')
            text_lines.append(f'tl{gi}_{ci}.textItem.size = {FONT_SIZE_LABEL};')
            text_lines.append(f'tl{gi}_{ci}.textItem.color = black;')
            text_lines.append(f'tl{gi}_{ci}.textItem.position = [{cx}, {label_y}];')
            text_lines.append(f'tl{gi}_{ci}.textItem.justification = Justification.CENTER;')

            # HEX label
            text_lines.append(f'var th{gi}_{ci} = doc.artLayers.add();')
            text_lines.append(f'th{gi}_{ci}.name = "{label}_hex";')
            text_lines.append(f'th{gi}_{ci}.kind = LayerKind.TEXT;')
            text_lines.append(f'th{gi}_{ci}.textItem.contents = "{h}";')
            text_lines.append(f'th{gi}_{ci}.textItem.size = {FONT_SIZE_HEX};')
            text_lines.append(f'th{gi}_{ci}.textItem.color = black;')
            text_lines.append(f'th{gi}_{ci}.textItem.position = [{cx}, {hex_y}];')
            text_lines.append(f'th{gi}_{ci}.textItem.justification = Justification.CENTER;')

    jsx = f'''// CUS 三原理 4色色卡 — PSD multi-row
#target photoshop
app.bringToFront();

var doc = app.documents.add({CANVAS_W}, {canvas_h}, 72, "三原理_4色色卡", NewDocumentMode.RGB);
var white = new SolidColor();
white.rgb.red = 255; white.rgb.green = 255; white.rgb.blue = 255;
var black = new SolidColor();
black.rgb.red = 0; black.rgb.green = 0; black.rgb.blue = 0;

doc.selection.selectAll();
doc.selection.fill(white);
doc.selection.deselect();

// ════ Phase 1: all blocks (bottom z-order) ════
{chr(10).join(block_lines)}

// ════ Phase 2: all text (top z-order) ════
{chr(10).join(text_lines)}

var psdFile = new File("{OUTPUT_BASE}.psd");
var psdOpts = new PhotoshopSaveOptions();
psdOpts.layers = true;
doc.saveAs(psdFile, psdOpts, true);
doc.close(SaveOptions.DONOTSAVECHANGES);
'''

    return _run_ps_jsx(jsx)


def _run_ps_jsx(jsx):
    jsx_path = f"{OUTPUT_BASE}.jsx"
    with open(jsx_path, "w", encoding="utf-8-sig") as f:
        f.write(jsx)

    applescript = f'''
    tell application "Adobe Photoshop 2026"
        activate
        do javascript file "{jsx_path}"
    end tell
    '''

    proc = subprocess.run(
        ["osascript", "-e", applescript],
        capture_output=True, text=True, timeout=120
    )

    if proc.returncode != 0:
        print(f"Photoshop error: {proc.stderr}")
        return None

    psd_path = f"{OUTPUT_BASE}.psd"
    if os.path.exists(psd_path):
        os.remove(jsx_path)
        return psd_path
    return None


if __name__ == "__main__":
    print("PNG preview…")
    png = make_png()
    print(f"  PNG: {png}")

    print("PSD (Photoshop multi-layer editable)…")
    psd = make_psd()
    if psd:
        total = sum(len(g["colors"]) for g in GROUPS) if use_groups else len(COLORS)
        texts = (3 + 3 + total * 2) if use_groups else (2 + total)
        print(f"  PSD: {psd}")
        print(f"  Layers: 1 bg + {total} blocks + {texts} text = {1 + total + texts} total")
    else:
        print("  PSD failed")

    print()
    if use_groups:
        for grp in GROUPS:
            for label, h in grp["colors"]:
                print(f"  {label}  {h}")
            print()
    else:
        for label, h in COLORS:
            print(f"  {label}  {h}")
