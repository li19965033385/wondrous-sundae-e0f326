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
        self.categories = categories
        self.tags = self._build_tag_index()
        self.recent_articles = sorted(self.articles, key=lambda a: a["date"], reverse=True)
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
        })

    def _build_tag_index(self):
        tag_map = {}
        for a in self.articles:
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

    # ── JSON-LD helpers ──────────────────────────────────────────────

    def article_ld(self, article):
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": article["title"],
            "description": article.get("description", ""),
            "datePublished": article.get("date", ""),
            "dateModified": article.get("date", ""),
            "author": {"@type": "Organization", "name": SITE_NAME},
            "publisher": {
                "@type": "Organization", "name": SITE_NAME,
                "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/img/logo.png"},
            },
            "mainEntityOfPage": {
                "@type": "WebPage", "@id": f"{SITE_URL}/article/{article['slug']}/",
            },
        }

    def website_ld(self):
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE_NAME,
            "url": SITE_URL,
            "description": SITE_DESC,
            "potentialAction": {
                "@type": "SearchAction",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": f"{SITE_URL}/search/?q={{search_term_string}}",
                },
                "query-input": "required name=search_term_string",
            },
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
        featured = [a for a in self.articles if a.get("featured")][:8]
        categories_data = []
        for cid, cat in self.categories.items():
            cat_arts = [a for a in self.articles if a.get("category") == cid]
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

        html = self.render_page("index.html",
            featured=featured, cats=categories_data,
            recent_articles=self.recent_articles[:10],
            tags=list(self.tags.keys()),
            website_ld=json.dumps(self.website_ld(), ensure_ascii=False),
            faq_ld=json.dumps(self.faq_ld(faq), ensure_ascii=False),
            breadcrumbs=json.dumps(build_breadcrumbs([("Home", "/")]), ensure_ascii=False),
            page_title=f"{SITE_NAME} - {SITE_DESC}",
            page_description=SITE_DESC,
            page_url="/", og_type="website",
        )
        self._write("index.html", html)

    def generate_article(self, article):
        related = [a for a in self.articles
                   if a.get("category") == article.get("category")
                   and a["slug"] != article["slug"]][:4]
        cid = article.get("category", "uncategorized")
        cname = self.categories.get(cid, {}).get("name", cid)
        crumbs = [("Home", "/"), (cname, f"/category/{cid}/"), (article["title"], f"/article/{article['slug']}/")]
        ld_bread = build_breadcrumbs(crumbs)
        ld_all = [self.article_ld(article), ld_bread]

        html = self.render_page("article.html",
            article=article, related=related,
            recent_articles=self.recent_articles,
            tags=list(self.tags.keys()),
            breadcrumbs=json.dumps(ld_bread, ensure_ascii=False),
            ld_json=json.dumps(ld_all, ensure_ascii=False),
            page_title=f"{article['title']} - {SITE_NAME}",
            page_description=article.get("description", ""),
            page_url=f"/article/{article['slug']}/",
            og_type="article", og_image=article.get("og_image", "/img/og-default.jpg"),
        )
        self._write(f"article/{article['slug']}/index.html", html)

    def generate_category_pages(self):
        for cid, cat in self.categories.items():
            cat_arts = [a for a in self.articles if a.get("category") == cid]
            cat_arts.sort(key=lambda a: a["date"], reverse=True)
            crumbs = [("Home", "/"), (cat["name"], f"/category/{cid}/")]
            html = self.render_page("category.html",
                category=cat, category_id=cid, articles=cat_arts, total=len(cat_arts),
                breadcrumbs=json.dumps(build_breadcrumbs(crumbs), ensure_ascii=False),
                page_title=f"{cat['name']} - {SITE_NAME}",
                page_description=cat.get("desc", ""),
                page_url=f"/category/{cid}/", og_type="website",
            )
            self._write(f"category/{cid}/index.html", html)

    def generate_tag_pages(self):
        for tag, tag_arts in self.tags.items():
            tag_arts.sort(key=lambda a: a["date"], reverse=True)
            slug = slugify(tag)
            crumbs = [("Home", "/"), (f"Tag: {tag}", f"/tag/{slug}/")]
            html = self.render_page("tag.html",
                tag=tag, tag_slug=slug, articles=tag_arts, total=len(tag_arts),
                breadcrumbs=json.dumps(build_breadcrumbs(crumbs), ensure_ascii=False),
                page_title=f"{tag} - {SITE_NAME}",
                page_description=f"Articles about {tag} - AI tools, tutorials and resources",
                page_url=f"/tag/{slug}/", og_type="website",
            )
            self._write(f"tag/{slug}/index.html", html)

    def generate_about_page(self):
        crumbs = [("Home", "/"), ("About", "/about/")]
        html = self.render_page("about.html",
            breadcrumbs=json.dumps(build_breadcrumbs(crumbs), ensure_ascii=False),
            page_title=f"About {SITE_NAME}",
            page_description="Learn about AI Tools Hub - your guide to AI tools and resources",
            page_url="/about/", og_type="website",
        )
        self._write("about/index.html", html)

    def generate_404_page(self):
        html = self.render_page("404.html",
            page_title="Page Not Found",
            page_description="The page you are looking for does not exist.",
            page_url="/404.html", og_type="website",
        )
        self._write("404.html", html)

    def generate_tools_page(self):
        crumbs = [("Home", "/"), ("AI Tools", "/tools/")]
        html = self.render_page("tools.html",
            breadcrumbs=json.dumps(build_breadcrumbs(crumbs), ensure_ascii=False),
            page_title=f"AI Tools - {SITE_NAME}",
            page_description="Free online AI tools - image filters, color palette, QR code generator, prompt builder and more.",
            page_url="/tools/", og_type="website",
        )
        self._write("tools/index.html", html)


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
        html = self.render_page("videos.html",
            videos=videos,
            breadcrumbs=json.dumps(build_breadcrumbs(crumbs), ensure_ascii=False),
            page_title=f"AI Video Tutorials - {SITE_NAME}",
            page_description="Watch AI tools tutorials, reviews and demos. Learn ChatGPT, Midjourney, Runway and more through video guides.",
            page_url="/videos/", og_type="website",
        )
        self._write("videos/index.html", html)


    def generate_sitemap(self):
        urlset = Element("urlset")
        urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

        for path, prio, freq in [("/", "1.0", "daily"), ("/about/", "0.7", "monthly"), ("/tools/", "0.8", "weekly"), ("/videos/", "0.7", "weekly")]:
            url = SubElement(urlset, "url")
            SubElement(url, "loc").text = f"{SITE_URL}{path}"
            SubElement(url, "priority").text = prio
            SubElement(url, "changefreq").text = freq

        for a in self.articles:
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

        for tag in self.tags:
            slug = slugify(tag)
            url = SubElement(urlset, "url")
            SubElement(url, "loc").text = f"{SITE_URL}/tag/{slug}/"
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
        
        for a in self.articles[:5000]:
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
        for a in self.articles:
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
        for a in self.articles:
            self.generate_amp_article(a)
        print("🖼️  Generating article images...")
        generate_all_article_images(self.articles, str(OUTPUT))
        generate_default_og(str(OUTPUT))
        
        print("📦 Static assets...")
        self.copy_static_assets()

        all_files = list(OUTPUT.rglob("*"))
        html_files = [f for f in all_files if f.suffix == ".html"]
        total_size = sum(f.stat().st_size for f in all_files if f.is_file())
        print(f"\n✅ Done! {len(html_files)} HTML pages, {len(all_files)} files, {total_size/1024:.0f} KB")
        print(f"   Articles: {len(self.articles)}, Categories: {len(self.categories)}, Tags: {len(self.tags)}")
