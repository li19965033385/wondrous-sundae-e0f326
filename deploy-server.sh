#!/bin/bash
# ═══════════════════════════════════════════════════════════
# AI Tools Hub - 搬瓦工服务器一键部署脚本
# 用法: 在服务器上执行:
#   curl -sL https://raw.githubusercontent.com/li19965033385/wondrous-sundae-e0f326/main/deploy-server.sh | bash
# 或者上传到服务器后: bash deploy-server.sh
# ═══════════════════════════════════════════════════════════

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🚀 AI Tools Hub - 服务器一键部署              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# 检查 root 权限
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ 请用 root 权限运行: sudo bash deploy-server.sh${NC}"
   exit 1
fi

# 配置变量
SITE_DOMAIN="${1:-localhost}"  # 如果有域名，传参: bash deploy-server.sh yourdomain.com
SITE_DIR="/var/www/aitoolshub"
NGINX_CONF="/etc/nginx/conf.d/aitoolshub.conf"

echo -e "${BLUE}[1/8] 安装系统依赖...${NC}"
yum install -y epel-release 2>/dev/null || true
yum install -y nginx git python3 python3-pip 2>/dev/null || {
    apt-get update -qq 2>/dev/null
    apt-get install -y nginx git python3 python3-pip 2>/dev/null
}
echo -e "${GREEN}  ✅ 依赖安装完成${NC}"

echo ""
echo -e "${BLUE}[2/8] 从 GitHub 拉取代码...${NC}"
rm -rf "$SITE_DIR"
git clone https://github.com/li19965033385/wondrous-sundae-e0f326.git "$SITE_DIR"
cd "$SITE_DIR"
echo -e "${GREEN}  ✅ 代码拉取完成${NC}"

echo ""
echo -e "${BLUE}[3/8] 安装 Python 依赖...${NC}"
pip3 install jinja2 2>/dev/null || pip3 install jinja2 --break-system-packages 2>/dev/null
echo -e "${GREEN}  ✅ Python 依赖安装完成${NC}"

echo ""
echo -e "${BLUE}[4/8] 生成静态网站（81篇文章 + 80张配图）...${NC}"
python3 generate_site.py
echo -e "${GREEN}  ✅ 网站生成完成${NC}"

echo ""
echo -e "${BLUE}[5/8] 配置 Nginx...${NC}"
cat > "$NGINX_CONF" << 'NGINXEOF'
server {
    listen 80;
    server_name _;
    root /var/www/aitoolshub/output;
    index index.html;

    # 静态资源缓存
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg)$ {
        expires 365d;
        add_header Cache-Control "public, immutable";
    }

    # Gzip 压缩
    gzip on;
    gzip_types text/html text/css text/javascript application/javascript image/svg+xml;
    gzip_min_length 1000;

    # SEO 友好重定向
    location = /feed {
        return 301 /rss.xml;
    }
    location = /sitemap {
        return 301 /sitemap.xml;
    }

    # 404
    error_page 404 /404.html;
    location = /404.html {
        internal;
    }
}
NGINXEOF

# 备份默认配置
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak 2>/dev/null || true

# 启动 Nginx
systemctl enable nginx 2>/dev/null || systemctl enable nginx 2>/dev/null
systemctl restart nginx 2>/dev/null || service nginx restart 2>/dev/null || {
    nginx -t && nginx 2>/dev/null
}
echo -e "${GREEN}  ✅ Nginx 配置完成${NC}"

echo ""
echo -e "${BLUE}[6/8] 配置每日自动更新...${NC}"
cat > /usr/local/bin/update-aitoolshub.sh << 'UPDATEEOF'
#!/bin/bash
cd /var/www/aitoolshub
git pull origin main 2>/dev/null || true
pip3 install jinja2 -q 2>/dev/null || pip3 install jinja2 -q --break-system-packages 2>/dev/null
python3 generate_site.py
systemctl reload nginx 2>/dev/null || service nginx reload 2>/dev/null || true
echo "✅ AI Tools Hub 更新完成: $(date)"
UPDATEEOF
chmod +x /usr/local/bin/update-aitoolshub.sh

# 添加定时任务（每天凌晨 4 点更新）
(crontab -l 2>/dev/null | grep -v update-aitoolshub; echo "0 4 * * * /usr/local/bin/update-aitoolshub.sh >> /var/log/aitoolshub-update.log 2>&1") | crontab -
echo -e "${GREEN}  ✅ 每日自动更新已配置${NC}"

echo ""
echo -e "${BLUE}[7/8] 配置防火墙...${NC}"
firewall-cmd --permanent --add-service=http 2>/dev/null || true
firewall-cmd --reload 2>/dev/null || true
echo -e "${GREEN}  ✅ 防火墙配置完成${NC}"

echo ""
echo -e "${BLUE}[8/8] 创建快捷更新命令...${NC}"
echo 'alias update-site="bash /usr/local/bin/update-aitoolshub.sh"' >> ~/.bashrc
echo -e "${GREEN}  ✅ 快捷命令已添加${NC}"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          🎉 部署完成！                          ║${NC}"
echo -e "${GREEN}╠══════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║                                                ║${NC}"
echo -e "${GREEN}║   🌐 访问地址: http://23.225.207.178           ║${NC}"
echo -e "${GREEN}║                                                ║${NC}"
echo -e "${GREEN}║   📊 81篇文章 · 399个HTML · 80张配图         ║${NC}"
echo -e "${GREEN}║                                                ║${NC}"
echo -e "${GREEN}║   📝 每日更新: bash update-aitoolshub.sh        ║${NC}"
echo -e "${GREEN}║   📝 或直接运行: update-site                    ║${NC}"
echo -e "${GREEN}║                                                ║${NC}"
echo -e "${GREEN}║   📌 域名到手后在 /etc/nginx/conf.d/aitoolshub.conf ${NC}"
echo -e "${GREEN}║       替换 server_name 和配置 SSL               ║${NC}"
echo -e "${GREEN}║                                                ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
