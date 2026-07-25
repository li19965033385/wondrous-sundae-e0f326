#!/usr/bin/env python3
"""
Generate the complete AI Tools Hub static website.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from content_data import ALL_ARTICLES, CATEGORIES
try:
    from generated_content import GENERATED_10000
except (ImportError, SyntaxError):
    GENERATED_10000 = []
from generator import SiteGenerator

if __name__ == "__main__":
    # Merge the editorial library and the bulk article archive. Keep the first
    # occurrence so curated articles win when a generated slug overlaps.
    articles = list({article["slug"]: article for article in reversed(ALL_ARTICLES + GENERATED_10000)}.values())
    gen = SiteGenerator(articles, CATEGORIES)
    gen.generate_all()
