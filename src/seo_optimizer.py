#!/usr/bin/env python3
"""AI Tools Hub - SEO Auto-Optimizer
======================================
Daily/Weekly script to maintain SEO freshness:
1. Refresh article dates to keep content fresh
2. Optimize titles with trending keywords
3. Add internal links between related articles
4. Refresh sitemap
5. Ping search engines

Usage:
  python3 src/seo_optimizer.py                  # Run full optimization
  python3 src/seo_optimizer.py --dates-only     # Only refresh dates
  python3 src/seo_optimizer.py --ping-only      # Only ping search engines

Schedule via crontab:
  0 3 * * * cd /path/to/project && python3 src/seo_optimizer.py >> logs/seo.log 2>&1
"""
import os, sys, datetime, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))

SITE_URL = "https://luaitools.com"
SEARCH_ENGINES = {
    "google": f"https://www.google.com/ping?sitemap={SITE_URL}/sitemap.xml",
    "bing": f"https://www.bing.com/ping?sitemap={SITE_URL}/sitemap.xml",
    "baidu": f"https://www.baidu.com/s?wd={SITE_URL}",
}

def refresh_dates():
    """Preserve truthful publication dates; freshness is updated with real edits only."""
    print("  ✅ Publication dates preserved (no artificial freshness changes)")

def optimize_titles():
    """Avoid mechanically adding trend terms that are not supported by page content."""
    print("  ✅ Titles preserved (keyword stuffing disabled)")

def regenerate_site():
    """Regenerate the static site."""
    print("  🔄 Regenerating site...")
    result = subprocess.run(
        [sys.executable, os.path.join(ROOT, 'generate_site.py')],
        capture_output=True, text=True, cwd=ROOT
    )
    if result.returncode == 0:
        # Extract stats from output
        for line in result.stdout.split('\n'):
            if 'Done' in line or 'HTML' in line:
                print(f"  ✅ {line.strip()}")
    else:
        print(f"  ❌ Generation failed: {result.stderr[:200]}")

def ping_search_engines():
    """Notify search engines of updates."""
    import urllib.request
    print("  📡 Pinging search engines...")
    for name, url in SEARCH_ENGINES.items():
        try:
            resp = urllib.request.urlopen(url, timeout=10)
            print(f"    ✅ {name}: {resp.status}")
        except Exception as e:
            print(f"    ⚠️  {name}: {str(e)[:50]}")

def check_seo_issues():
    """Scan for common SEO issues."""
    issues = []
    
    # Check sitemap
    sitemap_path = os.path.join(ROOT, 'output', 'sitemap.xml')
    if os.path.exists(sitemap_path):
        with open(sitemap_path) as f:
            urls = f.read().count('<loc>')
        print(f"  📊 Sitemap: {urls} URLs")
    else:
        issues.append("❌ Sitemap not found")
    
    # Check robots.txt
    robots_path = os.path.join(ROOT, 'output', 'robots.txt')
    if os.path.exists(robots_path):
        with open(robots_path) as f:
            content = f.read()
        if SITE_URL in content:
            print(f"  ✅ robots.txt OK")
    else:
        issues.append("❌ robots.txt not found")
    
    # Check homepage
    index_path = os.path.join(ROOT, 'output', 'index.html')
    if os.path.exists(index_path):
        with open(index_path) as f:
            content = f.read()
        checks = {
            "has_title": "<title>" in content,
            "has_desc": 'meta name="description"' in content,
            "has_canonical": 'rel="canonical"' in content,
            "has_og": 'og:title' in content,
            "has_hreflang": 'hreflang' in content,
            "has_schema": 'schema.org' in content,
        }
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check}")
            if not result:
                issues.append(f"❌ {check} missing")
    
    # Check article pages
    article_dir = os.path.join(ROOT, 'output', 'article')
    if os.path.exists(article_dir):
        articles = os.listdir(article_dir)
        print(f"  📊 Article pages: {len(articles)}")
    
    if issues:
        print(f"\n  ⚠️  Issues found:")
        for issue in issues:
            print(f"    {issue}")
    else:
        print(f"\n  ✅ No issues found!")
    
    return len(issues) == 0

def main():
    print(f"\n{'='*50}")
    print(f"  🔍 AI Tools Hub - SEO Optimizer")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if args and "dates-only" in args[0]:
        print("📅 Refreshing article dates...")
        refresh_dates()
    
    if args and "titles-only" in args[0]:
        print("\n📝 Optimizing titles...")
        optimize_titles()
    
    if not args:
        print("\n🔄 Regenerating optimized site...")
        regenerate_site()

    if not args or "check-only" in args[0]:
        print("\n🔍 Checking SEO issues...")
        check_seo_issues()
    
    if args and "ping-only" in args[0]:
        print("\n📡 Pinging search engines...")
        ping_search_engines()
    
    print(f"\n{'='*50}")
    print(f"  ✅ SEO optimization complete!")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
