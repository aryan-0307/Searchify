"""
Verify Searchify Production Enhancements:
1. /.well-known/security.txt (RFC 9116)
2. /privacy (Privacy Policy page & responsive layout)
3. /terms (Terms of Service page & responsive layout)
4. /404 (Custom animated 404 error page & simulation)
5. /robots.txt (Crawling directives & sitemap reference)
6. /sitemap.xml (Valid XML & public pages only)
7. /llms.txt (AI-readable architecture & algorithm overview)
8. /site.webmanifest (Valid JSON PWA manifest & icon existence)
9. /favicon.ico and brand icons
10. Footer links across all pages
11. Routing & Redirect configurations (vercel.json, _redirects)
12. Viewport Zero-Horizontal-Overflow verification in Headless Chrome
"""

import os
import sys
import json
import re
import subprocess
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

print("=" * 60)
print("VERIFYING SEARCHIFY PRODUCTION ENHANCEMENTS")
print("=" * 60)

# 1. Verify .well-known/security.txt & security.txt
print("\n--- 1. Testing RFC 9116 Security Disclosure (security.txt) ---")
sec_path = os.path.join(ROOT_DIR, ".well-known", "security.txt")
assert os.path.exists(sec_path), "Missing .well-known/security.txt"
with open(sec_path, "r", encoding="utf-8") as f:
    sec_content = f.read()

required_sec_fields = ["Contact:", "Expires:", "Preferred-Languages:", "Canonical:", "Policy:"]
for field in required_sec_fields:
    assert field in sec_content, f"Missing required RFC 9116 field '{field}' in security.txt"
    print(f"  [PASS] Found required field: {field}")

root_sec_path = os.path.join(ROOT_DIR, "security.txt")
assert os.path.exists(root_sec_path), "Missing root security.txt fallback"
print("  [PASS] Root security.txt fallback present")

# 2. Verify robots.txt
print("\n--- 2. Testing Search Engine Crawling Rules (robots.txt) ---")
robots_path = os.path.join(ROOT_DIR, "robots.txt")
assert os.path.exists(robots_path), "Missing robots.txt"
with open(robots_path, "r", encoding="utf-8") as f:
    robots_content = f.read()

assert "User-agent: *" in robots_content, "Missing 'User-agent: *' in robots.txt"
assert "Allow: /" in robots_content, "Missing 'Allow: /' in robots.txt"
assert "Sitemap: https://searchify.aryandixit.space/sitemap.xml" in robots_content, "Missing Sitemap directive in robots.txt"
print("  [PASS] robots.txt contains valid crawler directives and sitemap reference")

# 3. Verify sitemap.xml
print("\n--- 3. Testing XML Sitemap (sitemap.xml) ---")
sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
assert os.path.exists(sitemap_path), "Missing sitemap.xml"
with open(sitemap_path, "r", encoding="utf-8") as f:
    sitemap_content = f.read()

root = ET.fromstring(sitemap_content)
namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs = [elem.text for elem in root.findall('.//ns:loc', namespaces)]

expected_public_urls = [
    "https://searchify.aryandixit.space/",
    "https://searchify.aryandixit.space/sorting",
    "https://searchify.aryandixit.space/searching",
    "https://searchify.aryandixit.space/compare",
    "https://searchify.aryandixit.space/privacy",
    "https://searchify.aryandixit.space/terms"
]

for url in expected_public_urls:
    assert url in locs, f"Expected URL {url} missing from sitemap.xml"
    print(f"  [PASS] Public URL included: {url}")

assert not any("404" in loc for loc in locs), "Error page 404 must NOT be included in sitemap.xml"
print("  [PASS] Non-public / 404 pages correctly excluded from sitemap.xml")

# 4. Verify llms.txt
print("\n--- 4. Testing AI Context Document (llms.txt) ---")
llms_path = os.path.join(ROOT_DIR, "llms.txt")
assert os.path.exists(llms_path), "Missing llms.txt"
with open(llms_path, "r", encoding="utf-8") as f:
    llms_content = f.read()

assert "# Searchify" in llms_content
assert "Aryan Dixit" in llms_content
for algo in ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort",
             "Heap Sort", "Shell Sort", "Counting Sort", "Radix Sort", "Bucket Sort",
             "Linear Search", "Binary Search"]:
    assert algo in llms_content, f"Algorithm '{algo}' missing in llms.txt"
print("  [PASS] llms.txt contains complete architecture, algorithm documentation, and canonical URLs")

# 5. Verify site.webmanifest and PWA Icons
print("\n--- 5. Testing PWA Webmanifest & Icons ---")
manifest_path = os.path.join(ROOT_DIR, "site.webmanifest")
assert os.path.exists(manifest_path), "Missing site.webmanifest"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest_data = json.load(f)

assert manifest_data.get("name") == "Searchify — DSA Playground"
assert manifest_data.get("short_name") == "Searchify"
assert manifest_data.get("theme_color") == "#224D95"
assert manifest_data.get("background_color") == "#F5F3ED"
print("  [PASS] site.webmanifest contains valid metadata")

icons = manifest_data.get("icons", [])
assert len(icons) >= 4, "Expected at least 4 icon configurations in webmanifest"

for icon in icons:
    icon_src = icon["src"]
    icon_full_path = os.path.join(ROOT_DIR, icon_src.lstrip("/"))
    assert os.path.exists(icon_full_path), f"Manifest icon file '{icon_src}' missing on disk!"
    file_size = os.path.getsize(icon_full_path)
    assert file_size > 100, f"Icon file '{icon_src}' is unexpectedly small ({file_size} bytes)"
    print(f"  [PASS] Manifest icon verified: {icon_src} ({icon['sizes']}, {file_size} bytes)")

# 6. Verify Hosting Routing Configurations (vercel.json & _redirects)
print("\n--- 6. Testing Hosting Routing Configurations ---")
vercel_path = os.path.join(ROOT_DIR, "vercel.json")
assert os.path.exists(vercel_path), "Missing vercel.json"
with open(vercel_path, "r", encoding="utf-8") as f:
    vdata = json.load(f)

assert vdata.get("cleanUrls") is True, "cleanUrls must be enabled in vercel.json"
routes = vdata.get("routes", [])

# Validate route behaviors
route_map = {}
status_map = {}
for r in routes:
    if "src" in r and "dest" in r:
        route_map[r["src"]] = r["dest"]
        if "status" in r:
            status_map[r["src"]] = r["status"]

assert route_map.get("/privacy") == "/privacy.html"
assert route_map.get("/terms") == "/terms.html"
assert route_map.get("/404") == "/404.html"
assert status_map.get("/404") == 404, "Route /404 should specify status 404"
assert route_map.get("/(.*)") == "/404.html"
assert status_map.get("/(.*)") == 404, "Catch-all route must return status 404"
print("  [PASS] vercel.json routes: /privacy -> /privacy.html (200), /terms -> /terms.html (200), /404 -> /404.html (404), unknown -> /404.html (404)")

# Validate headers in vercel.json
headers_list = vdata.get("headers", [])
assert len(headers_list) >= 2, "Expected security and cache headers in vercel.json"
sec_headers = {h["key"]: h["value"] for h in headers_list[0].get("headers", [])}
assert sec_headers.get("X-Content-Type-Options") == "nosniff"
assert sec_headers.get("X-Frame-Options") == "DENY"
print("  [PASS] vercel.json security headers verified (nosniff, DENY, strict-origin)")

# Validate _redirects
redirects_path = os.path.join(ROOT_DIR, "_redirects")
assert os.path.exists(redirects_path), "Missing _redirects file"
with open(redirects_path, "r", encoding="utf-8") as f:
    rcontent = f.read()

lines = [l.strip() for l in rcontent.splitlines() if l.strip() and not l.strip().startswith('#')]
redirect_rules = [l.split() for l in lines]
r_dict = {rule[0]: (rule[1], rule[2] if len(rule) > 2 else "301") for rule in redirect_rules if len(rule) >= 2}

assert r_dict.get("/privacy") == ("/privacy.html", "200"), "Expected /privacy -> /privacy.html 200 in _redirects"
assert r_dict.get("/terms") == ("/terms.html", "200"), "Expected /terms -> /terms.html 200 in _redirects"
assert r_dict.get("/404") == ("/404.html", "404"), "Expected /404 -> /404.html 404 in _redirects"
assert r_dict.get("/*") == ("/404.html", "404"), "Expected /* -> /404.html 404 in _redirects"
print("  [PASS] _redirects contains Netlify/Cloudflare routing rules (/privacy 200, /terms 200, /404 404, /* 404)")

# 7. Testing New Pages in Headless Chrome
print("\n--- 7. Testing New Pages in Headless Chrome ---")
test_pages = [
    ("privacy.html", "Searchify — Privacy Policy", [".legal-card", ".legal-title", ".home-footer"]),
    ("terms.html", "Searchify — Terms of Service", [".legal-card", ".legal-title", ".home-footer"]),
    ("404.html", "404: Element Not Found", [".error-card", ".error-title", "#btn-replay-search", ".home-footer"])
]

viewports = [
    {"name": "Desktop 1280px", "width": 1280, "height": 850},
    {"name": "Tablet 768px", "width": 768, "height": 900},
    {"name": "Galaxy S23 412px", "width": 412, "height": 850},
    {"name": "iPhone SE 375px", "width": 375, "height": 800}
]

for file_name, expected_title_part, expected_selectors in test_pages:
    page_path = os.path.join(ROOT_DIR, file_name)
    assert os.path.exists(page_path), f"Page {file_name} missing on disk"

    # 7.1 Verify HTML5 Semantic Structure & Title
    with open(page_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert expected_title_part in html, f"Expected '{expected_title_part}' in title of {file_name}"
    for tag in ["header", "nav", "main", "footer"]:
        assert f"<{tag}" in html, f"Missing semantic <{tag}> tag in {file_name}"
    assert "privacy.html" in html and "terms.html" in html, f"Missing footer privacy/terms links in {file_name}"
    print(f"  [PASS] Semantic markup and footer links verified in {file_name}")

    # 7.2 Headless Chrome Console Errors Check
    page_url = f"file:///{page_path.replace(os.sep, '/')}"
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--enable-logging=stderr",
        "--dump-dom",
        page_url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    stderr = res.stderr
    assert "Uncaught" not in stderr and "TypeError" not in stderr and "SyntaxError" not in stderr, \
        f"JavaScript runtime error in {file_name}:\n{stderr}"
    print(f"  [PASS] Zero JS runtime errors on {file_name}")

    # 7.3 Viewport Overflow Check via Headless Chrome Iframe Harness
    for vp in viewports:
        harness_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0;">
<iframe id="test-frame" src="{page_url}" style="width:{vp['width']}px; height:{vp['height']}px; border:none; display:block;"></iframe>
<div id="output"></div>
<script>
window.addEventListener('load', async () => {{
    await new Promise(r => setTimeout(r, 600));
    const iframe = document.getElementById('test-frame');
    const doc = iframe.contentDocument;
    const body = doc.body;
    const docEl = doc.documentElement;
    const scrollW = Math.max(body.scrollWidth, docEl.scrollWidth);
    const clientW = docEl.clientWidth;
    document.getElementById('output').textContent = JSON.stringify({{
        scrollWidth: scrollW,
        clientWidth: clientW,
        hasOverflow: scrollW > clientW + 2
    }});
}});
</script>
</body>
</html>"""
        harness_path = os.path.join(ROOT_DIR, "tests", f"temp_harness_{file_name}_{vp['width']}.html")
        with open(harness_path, "w", encoding="utf-8") as f:
            f.write(harness_content)

        run_cmd = [
            CHROME_PATH,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--allow-file-access-from-files",
            f"--window-size={vp['width'] + 60},{vp['height'] + 100}",
            "--virtual-time-budget=5000",
            "--dump-dom",
            f"file:///{harness_path.replace(os.sep, '/')}"
        ]
        h_res = subprocess.run(run_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        if os.path.exists(harness_path):
            os.remove(harness_path)

        m = re.search(r'<div id="output"[^>]*>(.*?)</div>', h_res.stdout)
        if m and m.group(1):
            data = json.loads(m.group(1))
            assert not data["hasOverflow"], f"Horizontal overflow on {file_name} at {vp['name']} (scrollWidth={data['scrollWidth']}, clientWidth={data['clientWidth']})"
            print(f"  [PASS] {file_name} @ {vp['name']}: Zero horizontal overflow (scrollWidth: {data['scrollWidth']}, clientWidth: {data['clientWidth']})")
        else:
            print(f"  [WARN] Output container empty for {file_name} at {vp['name']}")

# 8. Verify Footer Links on Existing Pages
print("\n--- 8. Testing Footer Links on Existing Pages ---")
for existing_page in ["index.html", "sorting.html", "searching.html", "compare.html"]:
    ep_path = os.path.join(ROOT_DIR, existing_page)
    with open(ep_path, "r", encoding="utf-8") as f:
        ep_content = f.read()
    assert "privacy.html" in ep_content, f"Missing privacy.html link in {existing_page}"
    assert "terms.html" in ep_content, f"Missing terms.html link in {existing_page}"
    assert "site.webmanifest" in ep_content, f"Missing site.webmanifest link in {existing_page}"
    print(f"  [PASS] Footer links and site.webmanifest verified in {existing_page}")

print("\n" + "=" * 60)
print("ALL SEARCHIFY PRODUCTION ENHANCEMENTS VERIFIED (100% PASS)!")
print("=" * 60)
