#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AI Tools Hub - 一键部署脚本
# 在终端执行: bash deploy-final.sh
# ═══════════════════════════════════════════════════════════════

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      🚀 AI Tools Hub - 一键部署                 ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}📊 当前站点: 81篇文章 · 399个页面 · 488个文件${NC}"
echo ""

# 询问部署方式
echo "请选择部署方式:"
echo "  1) 拖拽到 Netlify Drop（最简单）"
echo "  2) 推送到 GitHub + 自动部署（推荐日更使用）"
echo ""
read -p "输入 1 或 2: " choice

if [ "$choice" = "1" ]; then
    # Netlify Drop
    echo ""
    echo -e "${BLUE}[1/2] 打包站点...${NC}"
    cd "$(dirname "$0")"
    
    # Create temp dir for clean deployment
    DEPLOY_DIR="/tmp/aitoolshub-deploy"
    rm -rf "$DEPLOY_DIR"
    cp -r output "$DEPLOY_DIR"
    
    echo -e "${GREEN}✅ 打包完成!${NC}"
    echo ""
    echo -e "${YELLOW}📂 站点已准备就绪: ${DEPLOY_DIR}${NC}"
    echo ""
    echo "════════════════════════════════════════════════════"
    echo ""
    echo "下一步:"
    echo "  1. 浏览器打开: https://app.netlify.com/drop"
    echo "  2. 把以下文件夹拖拽到页面:"
    echo ""
    echo "     ${DEPLOY_DIR}"
    echo ""
    echo "  3. 等待 10 秒完成部署"
    echo "  4. 获得临时域名后即可访问"
    echo ""
    echo "  未来日更只需:"
    echo "     python3 generate_site.py"
    echo "     然后重新拖拽 output/ 文件夹"
    echo ""
    
elif [ "$choice" = "2" ]; then
    # GitHub deploy
    echo ""
    echo -e "${BLUE}[1/4] 检查 GitHub 仓库...${NC}"
    cd "$(dirname "$0")"
    
    # Check if gh CLI is available
    if command -v gh &> /dev/null; then
        echo "✅ GitHub CLI 可用"
        # Try to create repo
        gh repo create wondrous-sundae-e0f326 --public --source=. --remote=origin --push 2>&1 || \
        gh repo create ai-tools-hub --public --source=. --remote=origin --push 2>&1 || \
        echo "请手动创建仓库"
    else
        echo "⚠️ 未安装 GitHub CLI (gh)"
        echo "请手动操作："
        echo "  1. 浏览器打开 https://github.com/new"
        echo "  2. 仓库名: wondrous-sundae-e0f326（或你喜欢的名字）"
        echo "  3. 选 Public，不要勾选任何初始化选项"
        echo "  4. 点 Create repository"
        echo ""
        echo -e "${BLUE}[2/4] 推送到 GitHub...${NC}"
        
        read -p "输入你的 GitHub 用户名: " github_user
        read -p "输入仓库名: " repo_name
        
        git remote set-url origin "https://github.com/${github_user}/${repo_name}.git"
        git push -u origin main 2>&1 || echo "⚠️ 推送失败，可能需要登录。试试: gh auth login"
        
        echo ""
        echo -e "${GREEN}✅ 推送完成!${NC}"
        echo ""
        echo "下一步:"
        echo "  1. 打开 https://vercel.com/new"
        echo "  2. 导入刚刚的 GitHub 仓库"
        echo "  3. 自动检测配置 → 部署"
        echo ""
        echo "未来日更只需:"
        echo "  ./push.sh \"今天的更新说明\""
        echo ""
    fi
else
    echo "输入无效，请重新运行脚本"
    exit 1
fi

echo -e "${GREEN}🎉 AI Tools Hub 祝你的网站流量暴涨！${NC}"
echo ""
