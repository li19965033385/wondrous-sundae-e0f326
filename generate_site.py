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
    # Keep the bulk archive online for existing links, but distinguish it from
    # human-edited content so low-value pages do not dilute search quality.
    merged = {}
    for article in GENERATED_10000:
        item = dict(article)
        item["programmatic"] = True
        merged[item["slug"]] = item
    for article in ALL_ARTICLES:
        item = dict(article)
        item["programmatic"] = False
        merged[item["slug"]] = item
    articles = list(merged.values())
    gen = SiteGenerator(articles, CATEGORIES)
    gen.generate_all()
