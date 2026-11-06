import subprocess
import os
import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

print("============================================================")
print("VERIFYING SEMANTIC HTML5 TAGS & SEO OPTIMIZATION")
print("============================================================")

pages = ["index.html", "sorting.html", "searching.html"]
all_passed = True

semantic_tags = ["header", "nav", "main", "section", "footer"]

for page in pages:
    print(f"\n--- Checking {page} ---")
    with open(page, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. SEO Metadata Checks
    print(f"  [SEO] Checking metadata...")
    assert '<meta name="description"' in html, f"Missing meta description in {page}"
    assert '<meta name="keywords"' in html, f"Missing meta keywords in {page}"
    assert '<meta name="robots" content="index, follow"' in html, f"Missing meta robots in {page}"
    assert '<meta property="og:title"' in html, f"Missing og:title in {page}"
    assert '<meta property="og:description"' in html, f"Missing og:description in {page}"
    assert '<meta name="twitter:card"' in html, f"Missing twitter:card in {page}"
    print(f"  [PASS] All essential SEO & Open Graph meta tags present in {page}")

    # 2. Semantic Tags Presence
    print(f"  [SEMANTIC] Checking HTML5 semantic structure...")
    for tag in semantic_tags:
        opening = f"<{tag}"
        closing = f"</{tag}>"
        assert opening in html and closing in html, f"Missing semantic <{tag}> in {page}"
    
    # Specific semantic checks
    assert "<figure" in html, f"Expected <figure> in {page}"
    assert "role=\"banner\"" in html or "<header" in html, f"Expected banner landmark in {page}"
    assert "<footer" in html, f"Expected <footer> in {page}"
    
    if page == "index.html":
        assert "<article" in html, "Expected <article> tags for playground cards in index.html"
        assert "<hgroup" in html or "h1" in html, "Expected heading structure in index.html"
    elif page in ["sorting.html", "searching.html"]:
        assert "<hgroup" in html, f"Expected <hgroup> in {page}"
        assert "<nav class=\"viz-controls\"" in html, f"Expected <nav class=\"viz-controls\"> in {page}"
        assert "<article" in html, f"Expected <article> for explanation and stats in {page}"
        assert "<aside" in html, f"Expected <aside> in {page}"
        assert "viz-footer" in html, f"Expected .viz-footer in {page}"

    print(f"  [PASS] Semantic HTML5 structure (header, nav, main, section, article, figure, aside, footer) verified for {page}")

print("\n============================================================")
print("ALL SEMANTIC & SEO VERIFICATIONS COMPLETED (100% PASS)")
print("============================================================")

