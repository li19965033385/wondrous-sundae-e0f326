# 🤖 AI Tools Hub - AI工具资源站

**AI工具评测、教程、对比与资源 — 中英双语内容网站**

一个完整的 SEO 优化静态网站，50 篇深度文章覆盖 AI 聊天机器人、图像生成、视频、编程、效率工具等热门赛道。

---

## 🚀 快速部署（选一个即可）

### 方案 A：Netlify Drop（最简单，无需注册 GitHub）

这是**最推荐的方式**，只需 3 步：

1. 打开 [https://app.netlify.com/drop](https://app.netlify.com/drop)
2. 把项目中的 **`output/`** 文件夹拖拽到浏览器页面
3. 几秒钟后你就获得 `https://xxx-xxx-xxx.netlify.app/` 域名

**👇 绑定自定义域名：**
- Netlify Dashboard → Domain Settings → Add Custom Domain
- 输入你的域名，按提示在 DNS 管理添加 CNAME 记录

### 方案 B：Vercel（通过 GitHub）

1. 在 [github.com](https://github.com) 创建新仓库
2. 在本地项目根目录执行：
```bash
git init
git add .
git commit -m "🎉 Initial commit - AI Tools Hub"
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```
3. 打开 [vercel.com/new](https://vercel.com/new)，导入刚刚的 GitHub 仓库
4. Vercel 会自动识别 `vercel.json`，构建并部署
5. 自动获得 `https://你的项目名.vercel.app/` 域名

**👇 绑定自定义域名：**
Vercel Dashboard → Domains → 输入你的域名 → 按提示配置 DNS

### 方案 C：Cloudflare Pages

1. 同样先推送到 GitHub 仓库
2. 打开 [pages.cloudflare.com](https://pages.cloudflare.com)
3. 连接 GitHub 仓库
4. 构建设置：
   - **构建命令:** `python3 generate_site.py`
   - **输出目录:** `output`
5. 部署完成！Cloudflare 自动提供 CDN 加速

---

## 📋 部署前配置

### 1. 替换 Google AdSense ID

搜索 `YOUR_PUBLISHER_ID_HERE` 替换为你的真实 AdSense ID：

- `src/templates/base.html`
- `output/index.html`
- `output/article/*/index.html`
- `output/ads.txt`

### 2. 替换域名

编辑 `src/generator.py` 中的 `SITE_URL` 变量：

```python
SITE_URL = "https://你的域名.com"
```

改完后重新生成：
```bash
python3 generate_site.py
```

### 3. 重新生成网站
```bash
python3 generate_site.py
```

---

## 🏗️ 本地开发

### 预览网站
```bash
python3 -m http.server 8000 -d output
# 打开 http://localhost:8000
```

### 添加新文章
1. 编辑 `src/content_data.py`
2. 在 `ALL_ARTICLES` 列表中添加新文章字典
3. 运行 `python3 generate_site.py` 重新生成

### 修改样式/功能
- 样式: `src/static/css/style.css`
- 模板: `src/templates/` 目录下的 Jinja2 文件
- 脚本: `src/static/js/` 目录

---

## 📊 站点结构

```
├── src/                     # 源代码
│   ├── generator.py         # 静态站点生成器
│   ├── content_data.py      # 50篇内容数据
│   ├── templates/           # Jinja2 模板
│   └── static/              # CSS、JS 等静态资源
├── output/                  # 生成后的站点（可直接部署）
│   ├── index.html           # 首页
│   ├── article/             # 50篇文章目录
│   ├── category/            # 10个分类目录
│   ├── tag/                 # 141个标签目录
│   ├── amp/                 # AMP 加速版本
│   ├── sitemap.xml          # 站点地图 (406 URLs)
│   ├── rss.xml              # RSS 订阅
│   ├── robots.txt           # 搜索引擎指引
│   ├── ads.txt              # Google AdSense
│   └── search-index.json    # 搜索索引
├── vercel.json              # Vercel 配置
└── netlify.toml             # Netlify 配置
```

---

## 🔍 SEO 技术栈

| 特性 | 说明 |
|------|------|
| JSON-LD 结构化数据 | Article, WebSite, BreadcrumbList, FAQPage |
| Open Graph | Facebook/LinkedIn 分享优化 |
| Twitter Cards | Twitter 分享卡片 |
| 语义化 HTML5 | `<article>`, `<nav>`, `<aside>`, `<main>` |
| 规范标题层级 | H1 → H2 → H3 |
| Canonical URL | 防重复内容 |
| XML Sitemap | 406个URL |
| AMP 版本 | Google 移动搜索加速 |
| 响应式设计 | 移动优先 + 暗色主题 |
| 搜索功能 | 客户端即时全文搜索 |

---

## ⚡ 日常维护

```bash
# 1. 修改内容或模板
# 2. 重新生成
python3 generate_site.py
# 3. 本地预览
python3 -m http.server 8000 -d output
# 4. 推送到 GitHub（Vercel/Netlify 会自动部署）
git add .
git commit -m "更新内容"
git push
```

---

## 📝 许可

© 2025 AI Tools Hub. All rights reserved.
