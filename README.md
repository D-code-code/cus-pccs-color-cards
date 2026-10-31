# CUS / PCCS 配色色卡 Skill（cus-pccs-color-cards）

一个「AI 行为准则」的 Skill 封装：让任何 AI（**Claude Code / Codex / 小龙虾 OpenClaw**）读完即可
**独立、正确地生成 CUS / PCCS 配色色卡（色カード）**，无需反复人工纠正。

- **CUS 体系**：24 色相 × 9 トーン = 216 色（色相环 + 全 HEX + YU/BU + 冷暖中性分类）
- **PCCS 体系**：12 トーン × 24 色相 = 288 色（+7 转换、偶奇规则、Pl≠pl、无彩色/游离色）
- **四大原理**：秩序(2+2) / 馴染み(4+5) / 類似性(0) / 明瞭性(对角线 12±2)
- **15 种配色技法**完整规格（ドミナントカラー／トーン、ダイアード、トライアド、テトラード…）
- **版式规范**：全日语 / 996px / 纯白背景 / 罫線禁止 / 纯黑文字 / ヒラギノ角ゴ Std W8
- **输出**：PNG 或 PSD（禁止 AI/Illustrator 格式），汉字不乱码（utf-8-sig BOM）

---

## 一、目录结构

```
cus-pccs-color-cards/
  SKILL.md                        # Skill 定义（规则 + 工作流，AI 先读这个）
  reference/
    CUS_Master_Reference.md       # CUS 216 色 HEX + 24 色相表 + YU/BU + 版式规范
    CUS_PCCS_制作指南.md           # 完整指南（PCCS 体系 / 15 技法全规格 / BOM / FAQ）
  data/
    PCCS_HEX_data.json            # PCCS 288 色 HEX（12 トーン × 24 色相）
    CUS24_色相環_トーンシステム_v22.png  # 视觉基准图（比对颜色·角度）
  tools/
    cus_card_generator.py         # CUS 单组/多组色卡生成（PNG + PSD）
    batch_15_techniques.py        # 15 种技法一括生成（PSD）
    gen_principles.py             # 四大原理生成（PSD）
    gen_pccs_all.py               # PCCS 四大原理 + 技法（PNG）
    gen_pccs_variants.py          # PCCS 变体（PNG）
    gen_pccs_template.py          # PCCS 扫描贴片模版（数据来源工具）
    extract_pccs.py               # PCCS 扫描图提取 HEX（数据来源工具）
  README.md / LICENSE / install.sh
```

---

## 二、安装（三大 AI 工具通用）

Skill 使用相同的 `SKILL.md` 格式，Claude / Codex / 小龙虾都能直接用。

### 一键安装（macOS / Linux）

```bash
cd cus-pccs-color-cards
./install.sh
```

`install.sh` 会把本目录软链接到 5 个位置：

| 工具 | 安装位置 | 调用方式 |
|------|---------|---------|
| Claude Code | `~/.claude/skills/cus-pccs-color-cards` | 自动触发（说关键词）或 `/cus-pccs-color-cards` |
| Codex CLI | `~/.codex/skills/cus-pccs-color-cards` | `$cus-pccs-color-cards` |
| 小龙虾 OpenClaw | `~/.openclaw/skills/`、`~/.openclaw/workspace/skills/` | `/skill cus-pccs-color-cards` |
| 通用共享 | `~/.agents/skills/cus-pccs-color-cards` | 其它兼容 Agent |

### 手动安装

直接把整个 `cus-pccs-color-cards/` 文件夹复制（或软链）到上面任一 `skills/` 目录即可。

---

## 三、使用

安装后，对 AI 说这些话即可自动触发（或手动调用）：

- 「做一张色卡」「帮我生成 CUS 色卡」「PCCS 色卡」
- 「四大原理色卡」「配色技法色卡」
- 「ドミナントカラー配色」「ドミナントトーン配色」「トーンシステム」

AI 会：
1. 先确认 **CUS 还是 PCCS**（你没指定时会问）；
2. 按四大原理 / 15 技法选色；
3. 生成符合版式规范的 PNG（任何平台）/ PSD（macOS + Photoshop）。

---

## 四、环境要求

| 项目 | 要求 |
|------|------|
| 操作系统 | macOS（PSD 生成）；PNG 生成任意平台 |
| Python | 3.x，`pip3 install Pillow` |
| Photoshop | Adobe Photoshop 2026（仅 PSD 生成需要，AppleScript 驱动） |
| 字体 | ヒラギノ角ゴ Std（macOS 自带 `/System/Library/Fonts/Hiragino Sans GB.ttc`） |

> 没装 Photoshop 也没关系——纯 Python + Pillow 就能生成标准 PNG 色卡。PSD 是多层可编辑版本。

---

## 五、开源到 GitHub

1. 在 GitHub 新建空仓库 `cus-pccs-color-cards`（**不要**勾选 README/license/.gitignore）。
2. 本地：
   ```bash
   cd cus-pccs-color-cards
   git init
   git add .
   git commit -m "Add cus-pccs-color-cards skill"
   git branch -M main
   git remote add origin https://github.com/<你的用户名>/cus-pccs-color-cards.git
   git push -u origin main
   ```

---

## 六、许可证

MIT License —— 见 `LICENSE`。欢迎 Fork、修改、商用。

---

## 七、背景

本项目源自一套「AI 行为准则」（CUS/PCCS 配色色卡制作规范），原为个人配色作业整理。
现将规则、数据、生成工具一并开源，方便在任何 AI 上复现同标准色卡。
