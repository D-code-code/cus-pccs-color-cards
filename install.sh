#!/bin/bash
# 一键安装 cus-pccs-color-cards Skill 到 Claude / Codex / 小龙虾(OpenClaw) / 通用 Agent
set -e

SKILL_NAME="cus-pccs-color-cards"
SRC="$(cd "$(dirname "$0")" && pwd)"

TARGETS=(
  "$HOME/.claude/skills/$SKILL_NAME"
  "$HOME/.codex/skills/$SKILL_NAME"
  "$HOME/.openclaw/skills/$SKILL_NAME"
  "$HOME/.openclaw/workspace/skills/$SKILL_NAME"
  "$HOME/.agents/skills/$SKILL_NAME"
)

echo "安装 Skill「$SKILL_NAME」→"
echo "  源目录: $SRC"
echo

for t in "${TARGETS[@]}"; do
  parent="$(dirname "$t")"
  mkdir -p "$parent"
  if [ -e "$t" ] || [ -L "$t" ]; then
    echo "  · 已存在，跳过: $t"
  else
    ln -s "$SRC" "$t"
    echo "  ✓ 已链接: $t"
  fi
done

echo
echo "完成。现在对 Claude / Codex / 小龙虾 说「做一张 CUS 色卡」即可触发。"
