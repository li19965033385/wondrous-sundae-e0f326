#!/bin/bash
# ═══════════════════════════════════════════════════════════
# AI Tools Hub - 一键推送部署脚本
# 用法: ./push.sh "新增了XX文章的更新说明"
# ═══════════════════════════════════════════════════════════

set -e

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 AI Tools Hub - 部署流水线${NC}"
echo ""

# 1. 生成站点
echo -e "${BLUE}[1/4] 生成站点...${NC}"
python3 generate_site.py
echo ""

# 2. Git 添加
echo -e "${BLUE}[2/4] 添加到 Git...${NC}"
git add -A
echo ""

# 3. Git 提交
COMMIT_MSG="${1:-每日内容更新}"
echo -e "${BLUE}[3/4] 提交: $COMMIT_MSG${NC}"
git commit -m "$COMMIT_MSG"
echo ""

# 4. Git 推送
echo -e "${BLUE}[4/4] 推送到 GitHub...${NC}"
git push

echo ""
echo -e "${GREEN}✅ 部署完成！ Vercel/Netlify 正在自动构建中...${NC}"
echo -e "${GREEN}   等待 1-2 分钟即可看到更新${NC}"
