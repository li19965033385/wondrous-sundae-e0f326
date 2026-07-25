#!/usr/bin/env python3
"""
AI Tools Hub - Static Site Generator
Generates a fully SEO-optimized static website with:
  - Semantic HTML5, JSON-LD structured data
  - XML sitemaps, RSS feed, robots.txt, ads.txt
  - Google AdSense integration
  - Mobile-first responsive design
"""

import json, os, shutil, datetime, re
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from jinja2 import Environment, FileSystemLoader
from svg_images import generate_all_article_images, generate_default_og

ROOT = Path(__file__).parent.parent
SRC = ROOT / "src"
TEMPLATES = SRC / "templates"
OUTPUT = ROOT / "output"

SITE_URL = "https://luaitools.com"
SITE_NAME = "AI Tools Hub"
SITE_NAME_CN = "AI工具资源站"
SITE_DESC = "Your ultimate guide to AI tools, tutorials, reviews and resources"
SITE_DESC_CN = "你的AI工具终极指南 - 评测、教程、对比与资源"
YEAR = datetime.date.today().year


def slugify(text):
    text = text.lower().strip().replace(" ", "-")
    text = re.sub(r"[^a-z0-9\-]", "", text)
    return re.sub(r"-+", "-", text).strip("-")


def truncate(text, words=30):
    w = text.split()
    return " ".join(w[:words]) + ("..." if len(w) > words else "")


def strip_html(html_text):
    return re.sub(r"<[^>]+>", "", html_text)


def get_reading_time(html_text):
    text = strip_html(html_text)
    wc = len(text.split())
    return max(1, round(wc / 200))


def build_breadcrumbs(items):
    crumbs = []
    for i, (name, url) in enumerate(items, 1):
        crumbs.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": f"{SITE_URL}{url}",
        })
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": crumbs,
    }


class SiteGenerator:
    def __init__(self, articles, categories):
        self.articles = articles
        translations_path = SRC / "translations_zh.json"
        if translations_path.exists():
            translations = json.loads(translations_path.read_text(encoding="utf-8"))
            for article in self.articles:
                article.update(translations.get(article.get("slug"), {}))
        self.categories = categories
        self.indexable_articles = [a for a in self.articles if not a.get("programmatic")]
        self.tags = self._build_tag_index(self.indexable_articles)
        self.recent_articles = sorted(self.indexable_articles, key=lambda a: a["date"], reverse=True)
        self.posts_per_page = 12
        self.env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
        self.env.globals.update({
            "categories": categories,
            "tags": list(self.tags.keys()),
            "recent_articles": self.recent_articles,
            "site_url": SITE_URL,
            "site_name": SITE_NAME,
            "site_name_cn": SITE_NAME_CN,
            "site_desc": SITE_DESC,
            "site_desc_cn": SITE_DESC_CN,
            "year": YEAR,
            "current_year": YEAR,
            "slugify": slugify,
            "truncate": truncate,
            "strip_html": strip_html,
            "int": int,
            "len": len,
            "enumerate": enumerate,
            "range": range,
            "organization_ld": json.dumps(self.organization_ld(), ensure_ascii=False),
        })

    def _build_tag_index(self, articles=None):
        tag_map = {}
        for a in articles if articles is not None else self.articles:
            for t in a.get("tags", []):
                tag_map.setdefault(t, []).append(a)
        return tag_map

    def _ensure_dir(self, path):
        os.makedirs(path, exist_ok=True)

    def _write(self, path, content):
        path = OUTPUT / path
        self._ensure_dir(path.parent)
        path.write_text(content, encoding="utf-8")
        return path

    def render_page(self, template_name, **kwargs):
        tpl = self.env.get_template(template_name)
        return tpl.render(**kwargs)

    def language_context(self, lang, base_path):
        """SEO-friendly language routing: English at /, Chinese at /zh/."""
        prefix = "/zh" if lang == "zh" else ""
        localized_path = f"{prefix}{base_path}" if base_path != "/" else ("/zh/" if lang == "zh" else "/")
        return {
            "current_lang": lang,
            "lang_prefix": prefix,
            "page_url": localized_path,
            "english_url": f"{SITE_URL}{base_path}",
            "chinese_url": f"{SITE_URL}{'/zh/' if base_path == '/' else '/zh' + base_path}",
        }

    # ── JSON-LD helpers ──────────────────────────────────────────────

    def organization_ld(self):
        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "@id": f"{SITE_URL}/#organization",
            "name": SITE_NAME,
            "alternateName": SITE_NAME_CN,
            "url": SITE_URL,
            "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/img/logo.png"},
        }

    def article_ld(self, article, lang="en"):
        prefix = "/zh" if lang == "zh" else ""
        title = article.get("title_cn", article["title"]) if lang == "zh" else article["title"]
        description = article.get("description_cn", article.get("description", "")) if lang == "zh" else article.get("description", "")
        image = article.get("og_image", "/img/og-default.jpg")
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "inLanguage": "zh-CN" if lang == "zh" else "en",
            "datePublished": article.get("date", ""),
            "dateModified": article.get("updated", article.get("date", "")),
            "image": f"{SITE_URL}{image}",
            "author": {"@id": f"{SITE_URL}/#organization"},
            "publisher": {
                "@type": "Organization", "name": SITE_NAME,
                "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/img/logo.png"},
            },
            "mainEntityOfPage": {
                "@type": "WebPage", "@id": f"{SITE_URL}{prefix}/article/{article['slug']}/",
            },
        }

    def website_ld(self):
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE_NAME,
            "url": SITE_URL,
            "description": SITE_DESC,
            "publisher": {"@id": f"{SITE_URL}/#organization"},
        }

    def faq_ld(self, questions):
        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": q["a"]},
                }
                for q in questions
            ],
        }

    # ── Page generators ──────────────────────────────────────────────

    def generate_homepage(self):
        featured = [a for a in self.indexable_articles if a.get("featured")][:8]
        categories_data = []
        for cid, cat in self.categories.items():
            cat_arts = [a for a in self.indexable_articles if a.get("category") == cid]
            categories_data.append({
                "id": cid, "name": cat["name"], "name_cn": cat["name_cn"],
                "description": cat.get("desc", ""), "icon": cat.get("icon", "🔧"),
                "count": len(cat_arts), "articles": cat_arts[:4],
            })

        faq = [
            {"q": "What is the best AI tool for content creation?",
             "a": "The best AI tools for content creation include ChatGPT for writing, Midjourney for images, and Runway for video. Each excels in different areas."},
            {"q": "Are AI tools free to use?",
             "a": "Many AI tools offer free tiers. ChatGPT, Claude, and Gemini have free versions. Premium features typically require a subscription."},
            {"q": "How can I make money with AI tools?",
             "a": "Popular ways include content creation, AI consulting, building AI-powered apps, and offering AI training services."},
        ]

        for lang in ("en", "zh"):
            ctx = self.language_context(lang, "/")
            html = self.render_page("index.html",
                featured=featured, cats=categories_data,
                recent_articles=self.recent_articles[:10], tags=list(self.tags.keys()),
                website_ld=json.dumps(self.website_ld(), ensure_ascii=False),
                faq_ld=json.dumps(self.faq_ld(faq), ensure_ascii=False),
                breadcrumbs=json.dumps(build_breadcrumbs([("Home", "/")]), ensure_ascii=False),
                page_title=(f"{SITE_NAME} - {SITE_DESC}" if lang == "en" else f"{SITE_NAME} - {SITE_DESC_CN}"),
                page_description=(SITE_DESC if lang == "en" else SITE_DESC_CN),
                og_type="website", **ctx)
            self._write("index.html" if lang == "en" else "zh/index.html", html)

    def generate_article(self, article):
        related = [a for a in self.indexable_articles
                   if a.get("category") == article.get("category")
                   and a["slug"] != article["slug"]][:4]
        cid = article.get("category", "uncategorized")
        cname = self.categories.get(cid, {}).get("name", cid)
        crumbs = [("Home", "/"), (cname, f"/category/{cid}/"), (article["title"], f"/article/{article['slug']}/")]
        ld_bread = build_breadcrumbs(crumbs)
        base_path = f"/article/{article['slug']}/"
        for lang in ("en", "zh"):
            ctx = self.language_context(lang, base_path)
            localized_bread = build_breadcrumbs([
                (("首页" if lang == "zh" else "Home"), ctx["lang_prefix"] + "/"),
                ((self.categories.get(cid, {}).get("name_cn", cname) if lang == "zh" else cname), f"{ctx['lang_prefix']}/category/{cid}/"),
                ((article.get("title_cn", article["title"]) if lang == "zh" else article["title"]), ctx["page_url"]),
            ])
            ld_all = [self.article_ld(article, lang), localized_bread]
            html = self.render_page("article.html", article=article, related=related,
                recent_articles=self.recent_articles, tags=list(self.tags.keys()),
                breadcrumbs=json.dumps(localized_bread, ensure_ascii=False), ld_json=json.dumps(ld_all, ensure_ascii=False),
                page_title=f"{article.get('title_cn', article['title']) if lang == 'zh' else article['title']} - {SITE_NAME}",
                page_description=(article.get("description_cn", article.get("description", "")) if lang == "zh" else article.get("description", "")),
                robots_directive=("noindex, follow" if article.get("programmatic") else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"),
                og_type="article", og_image=article.get("og_image", "/img/og-default.jpg"), **ctx)
            path = f"article/{article['slug']}/index.html" if lang == "en" else f"zh/article/{article['slug']}/index.html"
            self._write(path, html)

    def generate_category_pages(self):
        for cid, cat in self.categories.items():
            cat_arts = [a for a in self.indexable_articles if a.get("category") == cid]
            cat_arts.sort(key=lambda a: a["date"], reverse=True)
            crumbs = [("Home", "/"), (cat["name"], f"/category/{cid}/")]
            base_path = f"/category/{cid}/"
            for lang in ("en", "zh"):
                ctx = self.language_context(lang, base_path)
                html = self.render_page("category.html", category=cat, category_id=cid, articles=cat_arts, total=len(cat_arts),
                    breadcrumbs=json.dumps(build_breadcrumbs(crumbs), ensure_ascii=False),
                    page_title=f"{cat['name_cn'] if lang == 'zh' else cat['name']} - {SITE_NAME}",
                    page_description=cat.get("desc", ""), og_type="website", **ctx)
                path = f"category/{cid}/index.html" if lang == "en" else f"zh/category/{cid}/index.html"
                self._write(path, html)

    def generate_tag_pages(self):
        for tag, tag_arts in self.tags.items():
            tag_arts.sort(key=lambda a: a["date"], reverse=True)
            slug = slugify(tag)
            crumbs = [("Home", "/"), (f"Tag: {tag}", f"/tag/{slug}/")]
            base_path = f"/tag/{slug}/"
            for lang in ("en", "zh"):
                ctx = self.language_context(lang, base_path)
                html = self.render_page("tag.html", tag=tag, tag_slug=slug, articles=tag_arts, total=len(tag_arts),
                    breadcrumbs=json.dumps(build_breadcrumbs(crumbs), ensure_ascii=False), page_title=f"{tag} - {SITE_NAME}",
                    page_description=(f"所有关于 {tag} 的文章" if lang == "zh" else f"Articles about {tag} - AI tools, tutorials and resources"),
                    robots_directive=("index, follow, max-image-preview:large" if len(tag_arts) >= 2 else "noindex, follow"),
                    og_type="website", **ctx)
                path = f"tag/{slug}/index.html" if lang == "en" else f"zh/tag/{slug}/index.html"
                self._write(path, html)

    def generate_about_page(self):
        crumbs = [("Home", "/"), ("About", "/about/")]
        for lang in ("en", "zh"):
            ctx = self.language_context(lang, "/about/")
            html = self.render_page("about.html", breadcrumbs=json.dumps(build_breadcrumbs(crumbs), ensure_ascii=False),
                page_title=(f"About {SITE_NAME}" if lang == "en" else f"关于 {SITE_NAME}"),
                page_description=("Learn about AI Tools Hub - your guide to AI tools and resources" if lang == "en" else SITE_DESC_CN),
                og_type="website", **ctx)
            self._write("about/index.html" if lang == "en" else "zh/about/index.html", html)

    def generate_404_page(self):
        html = self.render_page("404.html", **self.language_context("en", "/404.html"),
            page_title="Page Not Found",
            page_description="The page you are looking for does not exist.",
            robots_directive="noindex, follow", og_type="website",
        )
        self._write("404.html", html)

    def generate_tools_page(self):
        crumbs = [("Home", "/"), ("AI Tools", "/tools/")]
        for lang in ("en", "zh"):
            ctx = self.language_context(lang, "/tools/")
            html = self.render_page("tools.html", breadcrumbs=json.dumps(build_breadcrumbs(crumbs), ensure_ascii=False),
                page_title=f"AI Tools - {SITE_NAME}",
                page_description="Free online AI tools - image filters, color palette, QR code generator, prompt builder and more.",
                og_type="website", **ctx)
            self._write("tools/index.html" if lang == "en" else "zh/tools/index.html", html)

    def generate_ai_directory(self):
        categories = [
            {"id":"chat","name":"Chat & Assistants","name_zh":"聊天助手"},
            {"id":"image","name":"Image & Design","name_zh":"图像设计"},
            {"id":"video","name":"Video & Audio","name_zh":"视频音频"},
            {"id":"code","name":"Coding","name_zh":"编程开发"},
            {"id":"productivity","name":"Productivity","name_zh":"效率办公"},
        ]
        cat_map = {c["id"]: c for c in categories}
        raw_tools = [
            ("ChatGPT","chat","General-purpose AI assistant for writing, reasoning and research.","适用于写作、推理与研究的通用 AI 助手。","Freemium","免费增值","https://chatgpt.com/"),
            ("Claude","chat","Thoughtful AI assistant for analysis, documents and coding.","擅长分析、长文档与编程的 AI 助手。","Freemium","免费增值","https://claude.ai/"),
            ("Gemini","chat","Google's multimodal assistant connected to its ecosystem.","连接 Google 生态的多模态 AI 助手。","Freemium","免费增值","https://gemini.google.com/"),
            ("Perplexity","chat","AI answer engine with web research and source citations.","带网页研究与来源引用的 AI 答案引擎。","Freemium","免费增值","https://www.perplexity.ai/"),
            ("DeepSeek","chat","AI assistant focused on reasoning and technical tasks.","专注推理与技术任务的 AI 助手。","Free","免费","https://chat.deepseek.com/"),
            ("Midjourney","image","High-quality AI image generation for creative professionals.","面向创意专业人士的高质量 AI 图像生成工具。","Paid","付费","https://www.midjourney.com/"),
            ("Adobe Firefly","image","Generative AI for images, effects and design workflows.","用于图像、特效与设计工作流的生成式 AI。","Freemium","免费增值","https://firefly.adobe.com/"),
            ("Canva AI","image","AI-powered visual design, presentations and social content.","AI 驱动的视觉设计、演示与社交内容平台。","Freemium","免费增值","https://www.canva.com/ai-image-generator/"),
            ("Leonardo AI","image","AI image creation with styles and production controls.","提供丰富风格与生产控制的 AI 图像创作平台。","Freemium","免费增值","https://leonardo.ai/"),
            ("Ideogram","image","AI image generator known for typography and graphic design.","擅长文字排版与平面设计的 AI 图像生成器。","Freemium","免费增值","https://ideogram.ai/"),
            ("Runway","video","Generative video creation and AI-assisted editing suite.","生成式视频创作与 AI 辅助编辑套件。","Freemium","免费增值","https://runwayml.com/"),
            ("ElevenLabs","video","Natural AI voice generation, dubbing and audio tools.","自然 AI 语音生成、配音与音频工具。","Freemium","免费增值","https://elevenlabs.io/"),
            ("Suno","video","Create complete songs and music from text prompts.","通过文字提示生成完整歌曲与音乐。","Freemium","免费增值","https://suno.com/"),
            ("Descript","video","Edit video and podcasts as easily as editing text.","像编辑文字一样编辑视频与播客。","Freemium","免费增值","https://www.descript.com/"),
            ("Cursor","code","AI-native code editor for understanding and building software.","用于理解和构建软件的 AI 原生代码编辑器。","Freemium","免费增值","https://www.cursor.com/"),
            ("GitHub Copilot","code","AI coding assistant integrated into developer workflows.","集成到开发工作流中的 AI 编程助手。","Paid","付费","https://github.com/features/copilot"),
            ("Replit","code","Browser development environment with AI coding capabilities.","具备 AI 编程能力的浏览器开发环境。","Freemium","免费增值","https://replit.com/"),
            ("v0","code","Generate web interfaces and application prototypes with AI.","使用 AI 生成网页界面与应用原型。","Freemium","免费增值","https://v0.dev/"),
            ("Notion AI","productivity","AI writing, search and knowledge tools inside Notion.","集成在 Notion 中的 AI 写作、搜索与知识工具。","Paid","付费","https://www.notion.so/product/ai"),
            ("Gamma","productivity","Create presentations, documents and webpages with AI.","使用 AI 创建演示文稿、文档与网页。","Freemium","免费增值","https://gamma.app/"),
            ("Otter.ai","productivity","Meeting transcription, summaries and searchable notes.","会议转录、摘要与可搜索笔记工具。","Freemium","免费增值","https://otter.ai/"),
            ("Zapier AI","productivity","Automate workflows and connect apps using AI.","使用 AI 自动化工作流并连接各种应用。","Freemium","免费增值","https://zapier.com/ai"),
        ]
        tools = []
        for name, cat, desc, desc_zh, price, price_zh, url in raw_tools:
            tools.append({"name":name,"category":cat,"category_name":cat_map[cat]["name"],"category_name_zh":cat_map[cat]["name_zh"],"description":desc,"description_zh":desc_zh,"price":price,"price_zh":price_zh,"url":url})
        for lang in ("en", "zh"):
            ctx = self.language_context(lang, "/ai-directory/")
            item_list = {
                "@context": "https://schema.org", "@type": "ItemList",
                "name": "AI 工具目录" if lang == "zh" else "Best AI Tools Directory",
                "numberOfItems": len(tools),
                "itemListElement": [{"@type": "ListItem", "position": i, "name": t["name"], "url": t["url"]} for i, t in enumerate(tools, 1)],
            }
            html = self.render_page("ai_directory.html", tools=tools, directory_categories=categories,
                breadcrumbs=json.dumps(build_breadcrumbs([(("首页" if lang == "zh" else "Home"), ctx["lang_prefix"] + "/"), (("AI 工具目录" if lang == "zh" else "AI Tools Directory"), ctx["page_url"])]), ensure_ascii=False),
                ld_json=json.dumps(item_list, ensure_ascii=False),
                page_title=("Best AI Tools Directory 2026: Chat, Image, Video & Coding" if lang == "en" else "2026 最佳 AI 工具目录：聊天、绘图、视频与编程"),
                page_description=("Discover and compare the best AI tools of 2026 for chat, image generation, video, coding and productivity. Curated descriptions and free options." if lang == "en" else "发现并比较 2026 年热门 AI 工具，覆盖聊天、AI 绘图、视频生成、编程和效率办公，包含精选介绍与免费工具。"),
                og_type="website", **ctx)
            self._write("ai-directory/index.html" if lang == "en" else "zh/ai-directory/index.html", html)


    def generate_videos_page(self):
        """Generate video gallery page with embedded YouTube tutorials."""
        videos = [
            {"id": "dQw4w9WgXcQ", "title": "ChatGPT Complete Tutorial for Beginners 2026", "desc": "Learn how to use ChatGPT from scratch with this comprehensive step-by-step tutorial covering all features.", "category": "chatgpt", "category_icon": "🤖", "category_name": "ChatGPT"},
            {"id": "pP1dL0BMEa4", "title": "Midjourney v7 Guide: Create Stunning AI Art", "desc": "Master Midjourney v7 with advanced prompts, parameters and techniques for creating professional AI artwork.", "category": "image", "category_icon": "🎨", "category_name": "AI图像"},
            {"id": "mYUna3JeyCY", "title": "Runway Gen-3 Tutorial: AI Video Creation", "desc": "Complete Runway Gen-3 workflow tutorial covering text-to-video, image-to-video and video editing features.", "category": "video", "category_icon": "🎬", "category_name": "AI视频"},
            {"id": "jTSnG4wMHIw", "title": "GitHub Copilot: Best Practices for Developers", "desc": "Learn how to supercharge your coding workflow with GitHub Copilot. Tips, tricks and real-world examples.", "category": "coding", "category_icon": "💻", "category_name": "AI编程"},
            {"id": "k2qHSRYHk0I", "title": "Claude 4 vs GPT-4o vs Gemini 2.5: Ultimate Comparison", "desc": "In-depth comparison of the top 3 AI assistants. Features, pricing, performance and use cases compared.", "category": "chatgpt", "category_icon": "🤖", "category_name": "ChatGPT"},
            {"id": "9QZ7SX0t1Go", "title": "DALL-E 3 Tips: Advanced Image Prompt Engineering", "desc": "Master prompt engineering for DALL-E 3. Learn to create precise, stunning AI images every time.", "category": "image", "category_icon": "🎨", "category_name": "AI图像"},
            {"id": "LGr0zFxvBhk", "title": "AI Video Editing: Complete Workflow Guide", "desc": "From recording to publishing - complete AI-powered video editing workflow using the latest tools.", "category": "video", "category_icon": "🎬", "category_name": "AI视频"},
            {"id": "qMQI0hM_Eaw", "title": "Perplexity AI: The Ultimate Research Tool", "desc": "How to use Perplexity AI for academic research, fact-checking, and professional research workflows.", "category": "tutorial", "category_icon": "📚", "category_name": "教程"},
            {"id": "A1B2C3D4E5F6", "title": "DeepSeek R1 Review: China's Best AI Model?", "desc": "Hands-on review of DeepSeek R1. Performance benchmarks, features comparison and practical use cases.", "category": "chatgpt", "category_icon": "🤖", "category_name": "ChatGPT"},
            {"id": "Z1Y2X3W4V5U6", "title": "Stable Diffusion 3: Complete Beginner's Guide", "desc": "Learn Stable Diffusion 3 from scratch. Installation, prompting, fine-tuning and advanced techniques.", "category": "image", "category_icon": "🎨", "category_name": "AI图像"},
            {"id": "T7S8R9Q0P1O2", "title": "Sora AI: Text-to-Video Generation Guide", "desc": "Explore OpenAI's Sora - the revolutionary text-to-video AI. Tips for creating cinematic AI videos.", "category": "video", "category_icon": "🎬", "category_name": "AI视频"},
            {"id": "N3M4L5K6J7I8", "title": "Cursor AI: AI-Powered Code Editor Review", "desc": "Can Cursor replace VS Code? In-depth review of the AI-native code editor with real coding demos.", "category": "coding", "category_icon": "💻", "category_name": "AI编程"},
        ]
        crumbs = [("Home", "/"), ("Videos", "/videos/")]
        for lang in ("en", "zh"):
            ctx = self.language_context(lang, "/videos/")
            html = self.render_page("videos.html", videos=videos,
                breadcrumbs=json.dumps(build_breadcrumbs(crumbs), ensure_ascii=False),
                page_title=(f"AI Tool Video Tutorials & Reviews 2026 - {SITE_NAME}" if lang == "en" else f"2026 AI 工具视频教程与评测 - {SITE_NAME}"),
                page_description=("Watch practical AI tool tutorials, reviews and demos for ChatGPT, Midjourney, Runway, coding assistants and more." if lang == "en" else "观看 ChatGPT、Midjourney、Runway、AI 编程助手等热门工具的实用教程、评测和演示。"),
                og_type="website", **ctx)
            self._write("videos/index.html" if lang == "en" else "zh/videos/index.html", html)


    def generate_sitemap(self):
        urlset = Element("urlset")
        urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

        for path, prio, freq in [("/", "1.0", "daily"), ("/zh/", "1.0", "daily"), ("/about/", "0.7", "monthly"), ("/zh/about/", "0.7", "monthly"), ("/tools/", "0.8", "weekly"), ("/zh/tools/", "0.8", "weekly"), ("/ai-directory/", "0.9", "weekly"), ("/zh/ai-directory/", "0.9", "weekly"), ("/videos/", "0.7", "weekly"), ("/zh/videos/", "0.7", "weekly")]:
            url = SubElement(urlset, "url")
            SubElement(url, "loc").text = f"{SITE_URL}{path}"
            SubElement(url, "priority").text = prio
            SubElement(url, "changefreq").text = freq

        for a in self.indexable_articles:
            for prefix in ("", "/zh"):
                url = SubElement(urlset, "url")
                SubElement(url, "loc").text = f"{SITE_URL}{prefix}/article/{a['slug']}/"
                SubElement(url, "lastmod").text = a.get("date", "")
                SubElement(url, "priority").text = "0.8"
                SubElement(url, "changefreq").text = "weekly"

        for cid in self.categories:
            for prefix in ("", "/zh"):
                url = SubElement(urlset, "url")
                SubElement(url, "loc").text = f"{SITE_URL}{prefix}/category/{cid}/"
                SubElement(url, "priority").text = "0.6"
                SubElement(url, "changefreq").text = "weekly"

        for tag in self.tags:
            if len(self.tags[tag]) < 2:
                continue
            slug = slugify(tag)
            for prefix in ("", "/zh"):
                url = SubElement(urlset, "url")
                SubElement(url, "loc").text = f"{SITE_URL}{prefix}/tag/{slug}/"
                SubElement(url, "priority").text = "0.4"
                SubElement(url, "changefreq").text = "daily"

        raw = tostring(urlset, encoding="unicode")
        dom = minidom.parseString(raw)
        xml = dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
        self._write("sitemap.xml", xml)

    def generate_rss(self):
        items = []
        for a in self.recent_articles[:20]:
            items.append(f"""    <item>
      <title><![CDATA[{a['title']}]]></title>
      <link>{SITE_URL}/article/{a['slug']}/</link>
      <description><![CDATA[{truncate(strip_html(a.get('body','')), 40)}]]></description>
      <pubDate>{a.get('date','')}</pubDate>
      <guid>{SITE_URL}/article/{a['slug']}/</guid>
    </item>""")
        items_joined = chr(10).join(items)
        rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SITE_NAME}</title>
    <link>{SITE_URL}</link>
    <description>{SITE_DESC}</description>
    <language>en</language>
    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
{items_joined}
  </channel>
</rss>"""
        self._write("rss.xml", rss)


    def generate_baidu_sitemap(self):
        """Generate Baidu-compatible sitemap."""
        from xml.etree.ElementTree import Element, SubElement, tostring
        from xml.dom import minidom
        urlset = Element("urlset")
        urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        
        for path, prio, freq in [("/", "1.0", "daily"), ("/about/", "0.8", "monthly"), ("/tools/", "0.9", "weekly"), ("/videos/", "0.8", "weekly")]:
            url = SubElement(urlset, "url")
            SubElement(url, "loc").text = f"{SITE_URL}{path}"
            SubElement(url, "priority").text = prio
            SubElement(url, "changefreq").text = freq
        
        for a in self.indexable_articles[:5000]:
            url = SubElement(urlset, "url")
            SubElement(url, "loc").text = f"{SITE_URL}/article/{a['slug']}/"
            SubElement(url, "lastmod").text = a.get("date", "")
            SubElement(url, "priority").text = "0.8"
            SubElement(url, "changefreq").text = "weekly"
        
        for cid in self.categories:
            url = SubElement(urlset, "url")
            SubElement(url, "loc").text = f"{SITE_URL}/category/{cid}/"
            SubElement(url, "priority").text = "0.6"
            SubElement(url, "changefreq").text = "weekly"
        
        raw = tostring(urlset, encoding="unicode")
        dom = minidom.parseString(raw)
        xml = dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
        self._write("sitemap_baidu.xml", xml)
        print(f"    Baidu sitemap: {5000 + 4 + len(self.categories)} URLs")

    def generate_robots(self):
        self._write("robots.txt", f"""User-agent: *
Allow: /
Disallow: /search/

# Google / General
Sitemap: {SITE_URL}/sitemap.xml

# Baidu
Sitemap: {SITE_URL}/sitemap_baidu.xml
""")

    def generate_ads_txt(self):
        self._write("ads.txt", """google.com, pub-YOUR_PUBLISHER_ID_HERE, DIRECT, f08c47fec0942fa0
""")

    def copy_static_assets(self):
        src_static = SRC / "static"
        dst_static = OUTPUT / "static"
        if src_static.exists() and src_static.is_dir():
            if dst_static.exists():
                shutil.rmtree(dst_static)
            shutil.copytree(src_static, dst_static)

    def generate_search_index(self):
        index = []
        for a in self.indexable_articles:
            body_text = strip_html(a.get("body", ""))
            index.append({
                "title": a["title"], "title_cn": a.get("title_cn", a["title"]),
                "slug": a["slug"], "description": a.get("description", ""),
                "description_cn": a.get("description_cn", ""),
                "category": a.get("category", ""), "tags": a.get("tags", []),
                "date": a.get("date", ""), "body": body_text[:500],
                "url": f"/article/{a['slug']}/",
            })
        self._write("search-index.json", json.dumps(index, ensure_ascii=False, indent=2))

    def generate_amp_article(self, article):
        related = [a for a in self.articles
                   if a.get("category") == article.get("category")
                   and a["slug"] != article["slug"]][:3]
        html = self.render_page("amp_article.html",
            article=article, related=related,
            page_title=f"{article['title']} - {SITE_NAME}",
            page_description=article.get("description", ""),
            page_url=f"/article/{article['slug']}/", og_type="article",
        )
        self._write(f"amp/article/{article['slug']}/index.html", html)

    def generate_all(self):
        print("🧹 Cleaning output...")
        gallery_backup = None
        if OUTPUT.exists():
            gallery_path = OUTPUT / "img" / "gallery"
            if gallery_path.exists():
                import tempfile
                gallery_backup = tempfile.mkdtemp()
                shutil.copytree(gallery_path, os.path.join(gallery_backup, "gallery"))
                print(f"    📦 Backed up gallery images ({len(os.listdir(gallery_path))} categories)")
            shutil.rmtree(OUTPUT)
        OUTPUT.mkdir(parents=True)
        # Restore gallery images
        if gallery_backup:
            gallery_dst = OUTPUT / "img" / "gallery"
            shutil.copytree(os.path.join(gallery_backup, "gallery"), gallery_dst)
            shutil.rmtree(gallery_backup)
            print(f"    ✅ Restored gallery images")

        print("🏠 Homepage...")
        self.generate_homepage()
        print("📄 Articles...")
        for a in self.articles:
            self.generate_article(a)
        print("📂 Categories...")
        self.generate_category_pages()
        print("🏷️  Tags...")
        self.generate_tag_pages()
        print("ℹ️  About + 404...")
        self.generate_about_page()
        self.generate_404_page()
        print("🔧 Tools page...")
        self.generate_tools_page()
        print("🧭 AI Directory...")
        self.generate_ai_directory()
        print("🎬 Videos page...")
        self.generate_videos_page()
        print("🗺️  Sitemap...")
        self.generate_sitemap()
        print("🗺️  Baidu Sitemap...")
        self.generate_baidu_sitemap()
        print("📡 RSS...")
        self.generate_rss()
        print("🤖 robots.txt...")
        self.generate_robots()
        print("💵 ads.txt...")
        self.generate_ads_txt()
        print("🔍 Search index...")
        self.generate_search_index()
        print("⚡ AMP...")
        for a in self.indexable_articles:
            self.generate_amp_article(a)
        print("🖼️  Generating article images...")
        generate_all_article_images(self.indexable_articles, str(OUTPUT))
        generate_default_og(str(OUTPUT))
        
        print("📦 Static assets...")
        self.copy_static_assets()

        all_files = list(OUTPUT.rglob("*"))
        html_files = [f for f in all_files if f.suffix == ".html"]
        total_size = sum(f.stat().st_size for f in all_files if f.is_file())
        print(f"\n✅ Done! {len(html_files)} HTML pages, {len(all_files)} files, {total_size/1024:.0f} KB")
        print(f"   Articles: {len(self.articles)} total / {len(self.indexable_articles)} indexable, Categories: {len(self.categories)}, Tags: {len(self.tags)}")
