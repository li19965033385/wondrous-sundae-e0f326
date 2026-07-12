#!/usr/bin/env python3
"""
Generate the complete AI Tools Hub static website.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from content_data import ALL_ARTICLES, CATEGORIES
from generator import SiteGenerator

if __name__ == "__main__":
    gen = SiteGenerator(ALL_ARTICLES, CATEGORIES)
    gen.generate_all()
