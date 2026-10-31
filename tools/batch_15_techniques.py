"""
CUS 配色技法 15種 一括色卡生成
各技法に適合する色を厳選し、PSD色卡を生成
"""
import subprocess, os, json, datetime

# ══════════════════════════════════
# Full CUS 216-color lookup
# ══════════════════════════════════
CUS = {
    # hue: {tone: hex}
    1:  {"pl":"#fef8ea","cl":"#fff3c3","bt":"#fde013","vv":"#fee101","dl":"#ab951d","lg":"#b9ad7b","td":"#403726","dk":"#6e5d25","dp":"#948d00"},
    2:  {"pl":"#f9f8e2","cl":"#faf4b9","bt":"#dfdc3e","vv":"#f3e900","dl":"#909d3a","lg":"#afb07c","td":"#3a3e30","dk":"#505f29","dp":"#8d9c10"},
    3:  {"pl":"#f4f7da","cl":"#f5f5af","bt":"#c1d969","vv":"#abcd05","dl":"#74a556","lg":"#a5b37e","td":"#33443a","dk":"#31612d","dp":"#86ab20"},
    4:  {"pl":"#eaf4e3","cl":"#d8ecc3","bt":"#b4d68b","vv":"#80bf3c","dl":"#4d974f","lg":"#9ab090","td":"#21403c","dk":"#226332","dp":"#44982d"},
    5:  {"pl":"#e1f2ec","cl":"#bce2d7","bt":"#a6d4ad","vv":"#009a54","dl":"#268948","lg":"#8fada1","td":"#0f3c3f","dk":"#126537","dp":"#01853a"},
    6:  {"pl":"#daf0eb","cl":"#b0dcd6","bt":"#96d0b6","vv":"#009f5c","dl":"#248a5e","lg":"#82a9a1","td":"#153e40","dk":"#0a6040","dp":"#007e48"},
    7:  {"pl":"#d4edea","cl":"#a3d7d5","bt":"#85cbc0","vv":"#009c84","dl":"#218b75","lg":"#74a5a1","td":"#1b4142","dk":"#025c4a","dp":"#007855"},
    8:  {"pl":"#d3edf0","cl":"#a1d7dc","bt":"#53c1c8","vv":"#00a2ae","dl":"#388e85","lg":"#7aa6ac","td":"#104450","dk":"#025656","dp":"#006f68"},
    9:  {"pl":"#d2edf6","cl":"#9fd7e4","bt":"#21b7cf","vv":"#01a0ca","dl":"#4e9295","lg":"#81a6b6","td":"#06475d","dk":"#014f63","dp":"#00667c"},
    10: {"pl":"#d9ecf6","cl":"#acdaec","bt":"#3fb7dc","vv":"#0096dc","dl":"#508ca1","lg":"#829fb2","td":"#084259","dk":"#014a6c","dp":"#005b86"},
    11: {"pl":"#e0eaf6","cl":"#badcf5","bt":"#5db7e8","vv":"#0075c2","dl":"#5286ad","lg":"#8398ad","td":"#0a3c55","dk":"#014574","dp":"#00508f"},
    12: {"pl":"#e7ebf6","cl":"#c6d4ee","bt":"#74a5d8","vv":"#025baa","dl":"#5977a3","lg":"#7e8ba2","td":"#102e47","dk":"#254374","dp":"#24478f"},
    13: {"pl":"#eeecf7","cl":"#d2cce6","bt":"#8c93c9","vv":"#4c4298","dl":"#606899","lg":"#7a7e97","td":"#162039","dk":"#494174","dp":"#473e8f"},
    14: {"pl":"#f3eef8","cl":"#dcd0e7","bt":"#988dc3","vv":"#633d98","dl":"#6e6288","lg":"#807b91","td":"#221e38","dk":"#56426f","dp":"#553782"},
    15: {"pl":"#f8f1f8","cl":"#e7d4e8","bt":"#a587bd","vv":"#920784","dl":"#7d5c77","lg":"#87788b","td":"#2d1d37","dk":"#62446a","dp":"#633075"},
    16: {"pl":"#f9eff6","cl":"#eaccda","bt":"#cc92c0","vv":"#b40985","dl":"#925f77","lg":"#927a84","td":"#362438","dk":"#683a58","dp":"#762468"},
    17: {"pl":"#faedf4","cl":"#eec5cd","bt":"#f29ec2","vv":"#d50080","dl":"#a76277","lg":"#9d7d7e","td":"#402b3a","dk":"#6f2f47","dp":"#8a175a"},
    18: {"pl":"#fbeef2","cl":"#f3c6c5","bt":"#f29db4","vv":"#e40072","dl":"#b06470","lg":"#aa8e90","td":"#512834","dk":"#742a38","dp":"#9c2547"},
    19: {"pl":"#fcefef","cl":"#f8c6bd","bt":"#f29ca7","vv":"#de0144","dl":"#ba6568","lg":"#b6a0a3","td":"#62252d","dk":"#792429","dp":"#ad3334"},
    20: {"pl":"#fceeea","cl":"#f8c6b4","bt":"#f29c8f","vv":"#e70f38","dl":"#c47052","lg":"#c4aeb0","td":"#6a241f","dk":"#862a24","dp":"#b64024"},
    21: {"pl":"#fdede4","cl":"#f8c5aa","bt":"#f39b77","vv":"#e7340c","dl":"#cd7c3d","lg":"#d1bbbd","td":"#732211","dk":"#92311e","dp":"#bf4c15"},
    22: {"pl":"#feefe1","cl":"#facfb0","bt":"#f5a470","vv":"#ea5e03","dl":"#c47a36","lg":"#d1baae","td":"#54241e","dk":"#924224","dp":"#ba5410"},
    23: {"pl":"#fef1de","cl":"#fbd9b6","bt":"#f7ae69","vv":"#f39801","dl":"#bc782f","lg":"#d1b99f","td":"#35262b","dk":"#935429","dp":"#b45d0a"},
    24: {"pl":"#fef4e4","cl":"#fde6bc","bt":"#fac73e","vv":"#faca02","dl":"#b48626","lg":"#c5b38d","td":"#3a2e28","dk":"#805827","dp":"#a47505"},
}

def hue_name(n):
    names = {1:"1Y",2:"2Y",3:"3YG",4:"4YG",5:"5G",6:"6G",7:"7BG",8:"8BG",
             9:"9GB",10:"10GB",11:"11B",12:"12B",13:"13V",14:"14V",15:"15P",
             16:"16P",17:"17RP",18:"18RP",19:"19R",20:"20R",21:"21RO",
             22:"22RO",23:"23YO",24:"24YO"}
    return names.get(n, str(n))

# ══════════════════════════════════
# 15 Techniques — color selections
# ══════════════════════════════════
TECHNIQUES = []

# 1. 中低彩度暖色系ドミナントカラー
TECHNIQUES.append({
    "num": "01", "title": "中低彩度暖色系\nドミナントカラー",
    "subtitle": "暖色系×2色相(2歩) ｜ cl, dl, dk すべて出現",
    "colors": [
        ("cl-19R", CUS[19]["cl"]),
        ("dl-21RO", CUS[21]["dl"]),
        ("dk-19R", CUS[19]["dk"]),
    ]
})

# 2. 高彩度暖色系ドミナントカラー
TECHNIQUES.append({
    "num": "02", "title": "高彩度暖色系\nドミナントカラー",
    "subtitle": "暖色系×3色相(2+2歩) ｜ bt, vv, dp すべて出現",
    "colors": [
        ("bt-19R", CUS[19]["bt"]),
        ("vv-21RO", CUS[21]["vv"]),
        ("dp-23YO", CUS[23]["dp"]),
    ]
})

# 3. 中低彩度寒色系ドミナントカラー
TECHNIQUES.append({
    "num": "03", "title": "中低彩度寒色系\nドミナントカラー",
    "subtitle": "寒色系×3色相(2+2歩) ｜ pl, dl すべて出現",
    "colors": [
        ("pl-12B", CUS[12]["pl"]),
        ("dl-10GB", CUS[10]["dl"]),
        ("dl-8BG", CUS[8]["dl"]),
    ]
})

# 4. 高彩度寒色系ドミナントカラー
TECHNIQUES.append({
    "num": "04", "title": "高彩度寒色系\nドミナントカラー",
    "subtitle": "寒色系×3色相(1+1歩) ｜ bt, vv すべて出現",
    "colors": [
        ("bt-12B", CUS[12]["bt"]),
        ("vv-11B", CUS[11]["vv"]),
        ("bt-10GB", CUS[10]["bt"]),
    ]
})

# 5. 亮色调ドミナントトーン
TECHNIQUES.append({
    "num": "05", "title": "亮色调\nドミナントトーン",
    "subtitle": "4色相(6+4+4歩) ｜ btトーン統一",
    "colors": [
        ("bt-22RO", CUS[22]["bt"]),
        ("bt-4YG", CUS[4]["bt"]),
        ("bt-8BG", CUS[8]["bt"]),
        ("bt-12B", CUS[12]["bt"]),
    ]
})

# 6. 暗色调ドミナントトーン
TECHNIQUES.append({
    "num": "06", "title": "暗色调\nドミナントトーン",
    "subtitle": "4色相(6+4+8歩) ｜ dkトーン統一",
    "colors": [
        ("dk-14V", CUS[14]["dk"]),
        ("dk-20R", CUS[20]["dk"]),
        ("dk-24YO", CUS[24]["dk"]),
        ("dk-8BG", CUS[8]["dk"]),
    ]
})

# 7. 鲜色调ドミナントトーン
TECHNIQUES.append({
    "num": "07", "title": "鲜色调\nドミナントトーン",
    "subtitle": "4色相(6+6+6歩) ｜ vvトーン統一",
    "colors": [
        ("vv-20R", CUS[20]["vv"]),
        ("vv-2Y", CUS[2]["vv"]),
        ("vv-8BG", CUS[8]["vv"]),
        ("vv-14V", CUS[14]["vv"]),
    ]
})

# 8. 低彩度ドミナントトーン
TECHNIQUES.append({
    "num": "08", "title": "低彩度\nドミナントトーン",
    "subtitle": "4色相(6+6+6歩) ｜ lgまたはtdトーン統一",
    "colors": [
        ("lg-20R", CUS[20]["lg"]),
        ("lg-2Y", CUS[2]["lg"]),
        ("lg-8BG", CUS[8]["lg"]),
        ("lg-14V", CUS[14]["lg"]),
    ]
})

# 9. 中彩度ドミナントトーン
TECHNIQUES.append({
    "num": "09", "title": "中彩度\nドミナントトーン",
    "subtitle": "4色相(6+4+6歩) ｜ dlトーン統一",
    "colors": [
        ("dl-2Y", CUS[2]["dl"]),
        ("dl-8BG", CUS[8]["dl"]),
        ("dl-12B", CUS[12]["dl"]),
        ("dl-18RP", CUS[18]["dl"]),
    ]
})

# 10. 同一トーン配色
TECHNIQUES.append({
    "num": "10", "title": "同一トーン配色",
    "subtitle": "2色 ｜ 歩数6 ｜ 同一トーン（任意）",
    "colors": [
        ("dl-1Y", CUS[1]["dl"]),
        ("dl-7BG", CUS[7]["dl"]),
    ]
})

# 11. 類似トーン配色
TECHNIQUES.append({
    "num": "11", "title": "類似トーン配色",
    "subtitle": "2色 ｜ 歩数4 ｜ cl-bt 類似色調",
    "colors": [
        ("cl-19R", CUS[19]["cl"]),
        ("bt-23YO", CUS[23]["bt"]),
    ]
})

# 12. 対照色相配色
TECHNIQUES.append({
    "num": "12", "title": "対照色相配色",
    "subtitle": "3色相(8+1歩) ｜ 2色相時=8〜10歩 ｜ 色相2〜3種",
    "colors": [
        ("vv-19R", CUS[19]["vv"]),
        ("cl-3YG", CUS[3]["cl"]),
        ("bt-4YG", CUS[4]["bt"]),
    ]
})

# 13. 補色色相配色
TECHNIQUES.append({
    "num": "13", "title": "補色色相配色",
    "subtitle": "3色相(11+1歩) ｜ 2色相時=11〜12歩 ｜ 色相2〜3種",
    "colors": [
        ("bt-19R", CUS[19]["bt"]),
        ("cl-6G", CUS[6]["cl"]),
        ("dp-7BG", CUS[7]["dp"]),
    ]
})

# 14. ダイアード
TECHNIQUES.append({
    "num": "14", "title": "ダイアード",
    "subtitle": "2色 ｜ 歩数12 ｜ トーン1〜2種 任意",
    "colors": [
        ("vv-1Y", CUS[1]["vv"]),
        ("dl-13V", CUS[13]["dl"]),
    ]
})

# 15. トリコロール配色
TECHNIQUES.append({
    "num": "15", "title": "トリコロール配色",
    "subtitle": "3色 ｜ vv同士歩数9 + 純白W",
    "colors": [
        ("vv-16P", CUS[16]["vv"]),
        ("vv-1Y", CUS[1]["vv"]),
        ("W", "#FFFFFF"),
    ]
})

# 16a. ビコロール配色 ① W+vv
TECHNIQUES.append({
    "num": "16a", "title": "ビコロール配色\n① W+vv",
    "subtitle": "2色限定 ｜ W + 任意のvv 1色",
    "colors": [
        ("W", "#FFFFFF"),
        ("vv-19R", CUS[19]["vv"]),
    ]
})

# 16b. ビコロール配色 ② vv同士
TECHNIQUES.append({
    "num": "16b", "title": "ビコロール配色\n② vv同士",
    "subtitle": "2色限定 ｜ vv同士 歩数±10",
    "colors": [
        ("vv-20R", CUS[20]["vv"]),
        ("vv-10GB", CUS[10]["vv"]),
    ]
})

# 17. 対照トーン配色
TECHNIQUES.append({
    "num": "17", "title": "対照トーン配色",
    "subtitle": "2色 ｜ 歩数6 ｜ pl×dp 双对照",
    "colors": [
        ("pl-13V", CUS[13]["pl"]),
        ("dp-19R", CUS[19]["dp"]),
    ]
})

# 18. スプリット・コンプリメンタリー
TECHNIQUES.append({
    "num": "18", "title": "スプリット・\nコンプリメンタリー",
    "subtitle": "3色 ｜ 歩数 2+11 (12B→14V→1Y)",
    "colors": [
        ("vv-12B", CUS[12]["vv"]),
        ("dl-14V", CUS[14]["dl"]),
        ("bt-1Y", CUS[1]["bt"]),
    ]
})

# 19. トライアド配色
TECHNIQUES.append({
    "num": "19", "title": "トライアド配色",
    "subtitle": "3色限定 ｜ ① 8+8歩 ｜ ② 4+10歩 ｜ トーン1〜3種任意",
    "colors": [
        ("cl-1Y", CUS[1]["cl"]),
        ("vv-9GB", CUS[9]["vv"]),
        ("dp-17RP", CUS[17]["dp"]),
    ]
})

# 20. テトラード配色
TECHNIQUES.append({
    "num": "20", "title": "テトラード配色",
    "subtitle": "4色限定 ｜ ① 6+6+6歩 ｜ ② 4+8+4歩 ｜ トーン1〜4種任意",
    "colors": [
        ("vv-1Y", CUS[1]["vv"]),
        ("dl-7BG", CUS[7]["dl"]),
        ("bt-13V", CUS[13]["bt"]),
        ("dp-19R", CUS[19]["dp"]),
    ]
})

# 21. ペンタード配色
TECHNIQUES.append({
    "num": "21", "title": "ペンタード配色",
    "subtitle": "① W+Bk+3色(8+8) ｜ ② 5+5+4+5歩 5色 ｜ 任意トーン",
    "colors": [
        ("W", "#FFFFFF"),
        ("Bk", "#000000"),
        ("cl-1Y", CUS[1]["cl"]),
        ("bt-9GB", CUS[9]["bt"]),
        ("dp-17RP", CUS[17]["dp"]),
    ]
})

# 22. ヘクサード配色
TECHNIQUES.append({
    "num": "22", "title": "ヘクサード配色",
    "subtitle": "① テトラード+W+Bk ｜ ② 4+4+4+4+4歩 6色 ｜ 任意トーン",
    "colors": [
        ("W", "#FFFFFF"),
        ("Bk", "#000000"),
        ("vv-1Y", CUS[1]["vv"]),
        ("dl-7BG", CUS[7]["dl"]),
        ("bt-13V", CUS[13]["bt"]),
        ("dp-19R", CUS[19]["dp"]),
    ]
})

# ══════════════════════════════════
# Layout params
# ══════════════════════════════════
CANVAS_W = 996
FONT_PS = "HiraginoSans-W8"
FONT_T = 20
FONT_ST = 13
FONT_L = 14
FONT_H = 11

def make_jsx(tech, idx):
    """Generate ExtendScript for one technique card"""
    colors = tech["colors"]
    n = len(colors)

    # Adaptive block size
    if n <= 3:
        BW, BH, GAP = 150, 200, 18
    elif n <= 4:
        BW, BH, GAP = 130, 180, 16
    elif n <= 5:
        BW, BH, GAP = 120, 160, 14
    else:
        BW, BH, GAP = 100, 140, 12

    total_w = n * BW + (n - 1) * GAP
    left_margin = (CANVAS_W - total_w) // 2
    center_x = CANVAS_W // 2

    BLOCK_Y = 130
    LABEL_Y = BLOCK_Y + BH + 12
    HEX_Y = LABEL_Y + 20
    canvas_h = HEX_Y + 40

    block_entries = []
    for i, (label, h) in enumerate(colors):
        if h in ("#FFFFFF", "#ffffff"):
            r, g, b = 255, 255, 255
        elif h in ("#000000", "#000000"):
            r, g, b = 0, 0, 0
        else:
            r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
        x1 = left_margin + i * (BW + GAP)
        x2 = x1 + BW
        y1 = BLOCK_Y
        y2 = BLOCK_Y + BH
        block_entries.append(json.dumps({
            "label": label, "hex": h,
            "r": r, "g": g, "b": b,
            "x1": x1, "y1": y1, "x2": x2, "y2": y2
        }))

    safe_title = tech["title"].replace("\n", " ").replace('"', '\\"')
    safe_sub = tech["subtitle"].replace('"', '\\"')
    desk = os.path.expanduser("~/Desktop/AIカラーカード")
    today = datetime.date.today().strftime("%Y-%m-%d")
    os.makedirs(f"{desk}/{today}", exist_ok=True)
    filename = f"{desk}/{today}/配色技法_{tech['num']}_{safe_title.split(chr(10))[0]}"

    jsx = f'''// CUS Technique {tech["num"]}: {safe_title}
#target photoshop
app.bringToFront();

var doc = app.documents.add({CANVAS_W}, {canvas_h}, 72, "技法{tech['num']}", NewDocumentMode.RGB);
var white = new SolidColor();
white.rgb.red = 255; white.rgb.green = 255; white.rgb.blue = 255;
var black = new SolidColor();
black.rgb.red = 0; black.rgb.green = 0; black.rgb.blue = 0;
var lgray = new SolidColor();
lgray.rgb.red = 170; lgray.rgb.green = 170; lgray.rgb.blue = 170;

doc.selection.selectAll();
doc.selection.fill(white);
doc.selection.deselect();

// Title
var t_title = doc.artLayers.add();
t_title.name = "title";
t_title.kind = LayerKind.TEXT;
t_title.textItem.contents = "{safe_title}";
t_title.textItem.size = {FONT_T};
t_title.textItem.color = black;
t_title.textItem.position = [{center_x}, 24];
t_title.textItem.justification = Justification.CENTER;

// Subtitle
var t_sub = doc.artLayers.add();
t_sub.name = "subtitle";
t_sub.kind = LayerKind.TEXT;
t_sub.textItem.contents = "{safe_sub}";
t_sub.textItem.size = {FONT_ST};
t_sub.textItem.color = lgray;
t_sub.textItem.position = [{center_x}, 80];
t_sub.textItem.justification = Justification.CENTER;

// Number badge
var t_num = doc.artLayers.add();
t_num.name = "num";
t_num.kind = LayerKind.TEXT;
t_num.textItem.contents = "{tech['num']}";
t_num.textItem.size = 11;
t_num.textItem.color = lgray;
t_num.textItem.position = [{CANVAS_W - 40}, 16];
t_num.textItem.justification = Justification.CENTER;

var blocks = [{", ".join(block_entries)}];

for (var i = blocks.length - 1; i >= 0; i--) {{
    var b = blocks[i];
    var bl = doc.artLayers.add();
    bl.name = b.label;
    doc.selection.select([[b.x1, b.y1], [b.x2, b.y1], [b.x2, b.y2], [b.x1, b.y2]]);
    var c = new SolidColor();
    c.rgb.red = b.r; c.rgb.green = b.g; c.rgb.blue = b.b;
    doc.selection.fill(c);
    if (b.r == 255 && b.g == 255 && b.b == 255) {{
        doc.selection.stroke(black, 0.25, StrokeLocation.INSIDE, ColorBlendMode.NORMAL, 100, false);
    }}
    doc.selection.deselect();

    var tl = doc.artLayers.add();
    tl.name = b.label + "_label";
    tl.kind = LayerKind.TEXT;
    tl.textItem.contents = b.label;
    tl.textItem.size = {FONT_L};
    tl.textItem.color = black;
    tl.textItem.position = [b.x1 + {BW // 2}, {LABEL_Y}];
    tl.textItem.justification = Justification.CENTER;

    var th = doc.artLayers.add();
    th.name = b.label + "_hex";
    th.kind = LayerKind.TEXT;
    th.textItem.contents = b.hex;
    th.textItem.size = {FONT_H};
    th.textItem.color = lgray;
    th.textItem.position = [b.x1 + {BW // 2}, {HEX_Y}];
    th.textItem.justification = Justification.CENTER;
}}

var psdFile = new File("{filename}.psd");
var psdOpts = new PhotoshopSaveOptions();
psdOpts.layers = true;
doc.saveAs(psdFile, psdOpts, true);
doc.close(SaveOptions.DONOTSAVECHANGES);
'''
    return jsx, filename


def run_ps(jsx, filename):
    jsx_path = f"{filename}.jsx"
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
        return f"ERROR: {proc.stderr[:200]}"

    psd_path = f"{filename}.psd"
    if os.path.exists(psd_path):
        os.remove(jsx_path)
        return f"OK: {psd_path}"
    return "FAILED: no output"


if __name__ == "__main__":
    print(f"Generating {len(TECHNIQUES)} technique cards...\n")

    success = 0
    for i, tech in enumerate(TECHNIQUES):
        jsx, fname = make_jsx(tech, i)
        label = tech["title"].replace("\n", " ")
        print(f"[{tech['num']}] {label[:50]}...", end=" ", flush=True)
        result = run_ps(jsx, fname)
        print(result)
        if result.startswith("OK"):
            success += 1

    print(f"\n{success}/{len(TECHNIQUES)} cards generated.")
