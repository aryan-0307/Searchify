"""
tests/verify_searchify_size_and_weight.py
Automated verification for:
1. Increased font-size of 'Searchify' text wherever it appears on the homepage (navbar and footer).
2. Increased font-weight of the primary font stack ('Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif) across all pages.
"""

import subprocess
import json
import os
import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("VERIFYING SEARCHIFY FONT SIZE & PRIMARY FONT WEIGHT")
print("=" * 60)

test_harness = """<!DOCTYPE html>
<html><body>
<iframe id="frame-home" src="../index.html" style="width:1440px; height:900px;"></iframe>
<iframe id="frame-sort" src="../sorting.html" style="width:1440px; height:900px;"></iframe>
<iframe id="frame-search" src="../searching.html" style="width:1440px; height:900px;"></iframe>
<div id="results"></div>
<script>
window.addEventListener('load', async () => {
    await new Promise(r => setTimeout(r, 600));

    const homeDoc = document.getElementById('frame-home').contentDocument;
    const homeWin = document.getElementById('frame-home').contentWindow;
    const sortDoc = document.getElementById('frame-sort').contentDocument;
    const sortWin = document.getElementById('frame-sort').contentWindow;
    const searchDoc = document.getElementById('frame-search').contentDocument;
    const searchWin = document.getElementById('frame-search').contentWindow;

    const issues = [];
    const checks = [];

    // 1. Check Searchify font size on homepage
    const brandLogo = homeDoc.querySelector('.home-brand-logo');
    if (!brandLogo) {
        issues.push("Missing .home-brand-logo on index.html");
    } else {
        const cs = homeWin.getComputedStyle(brandLogo);
        const fz = parseFloat(cs.fontSize);
        if (fz < 24) {
            issues.push(`Searchify logo font-size is too small: ${cs.fontSize} (expected >= 24px)`);
        } else {
            checks.push(`Searchify navbar brand font-size: ${cs.fontSize} (>= 24px)`);
        }
    }

    const footerBrand = homeDoc.querySelector('.footer-brand');
    if (!footerBrand) {
        issues.push("Missing .footer-brand on index.html");
    } else {
        const cs = homeWin.getComputedStyle(footerBrand);
        const fz = parseFloat(cs.fontSize);
        if (fz < 24) {
            issues.push(`Searchify footer brand font-size is too small: ${cs.fontSize} (expected >= 24px)`);
        } else {
            checks.push(`Searchify footer brand font-size: ${cs.fontSize} (>= 24px)`);
        }
    }

    // 2. Check font-weight of primary font stack (Inter / --font-primary)
    const weightTargets = [
        { doc: homeDoc, win: homeWin, sel: 'body', minWeight: 500, name: 'Home Body' },
        { doc: homeDoc, win: homeWin, sel: '.hero-description', minWeight: 500, name: 'Hero Description' },
        { doc: homeDoc, win: homeWin, sel: '.card-long-desc', minWeight: 500, name: 'Card Description' },
        { doc: sortDoc, win: sortWin, sel: 'body', minWeight: 500, name: 'Sorting Body' },
        { doc: sortDoc, win: sortWin, sel: '.viz-subtitle', minWeight: 500, name: 'Sorting Subtitle' },
        { doc: sortDoc, win: sortWin, sel: '.complexity-algo-desc', minWeight: 500, name: 'Sorting Complexity Desc' },
        { doc: searchDoc, win: searchWin, sel: 'body', minWeight: 500, name: 'Searching Body' },
        { doc: searchDoc, win: searchWin, sel: '.viz-subtitle', minWeight: 500, name: 'Searching Subtitle' },
        { doc: searchDoc, win: searchWin, sel: '.complexity-algo-desc', minWeight: 500, name: 'Searching Complexity Desc' }
    ];

    weightTargets.forEach(({ doc, win, sel, minWeight, name }) => {
        const el = doc.querySelector(sel);
        if (!el) {
            issues.push(`Element not found: ${name} (${sel})`);
            return;
        }
        const cs = win.getComputedStyle(el);
        const weight = parseInt(cs.fontWeight, 10);
        if (weight < minWeight) {
            issues.push(`${name} font-weight (${weight}) is less than expected (${minWeight})`);
        } else {
            checks.push(`${name} font-weight: ${weight} (fontFamily: ${cs.fontFamily.split(',')[0].replace(/['"]/g, '')})`);
        }
    });

    document.getElementById('results').textContent = JSON.stringify({
        passed: issues.length === 0,
        checks: checks,
        issues: issues
    });
});
</script>
</body></html>"""

temp_file = "tests/temp_searchify_weight_test.html"
with open(temp_file, "w", encoding="utf-8") as f:
    f.write(test_harness)

cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--virtual-time-budget=3000",
    "--dump-dom",
    f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{temp_file}"
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
if os.path.exists(temp_file):
    os.remove(temp_file)

m = re.search(r'<div id="results">(\{.*?\})</div>', res.stdout)
if not m:
    print("[FAIL] Could not extract test results from Chrome output")
    sys.exit(1)

data = json.loads(m.group(1))

print("\n--- Verified Checks ---")
for c in data.get("checks", []):
    print(f"  [PASS] {c}")

if data["passed"]:
    print("\n============================================================")
    print("ALL SEARCHIFY FONT SIZE & PRIMARY FONT WEIGHT CHECKS PASSED (100%)")
    print("============================================================")
else:
    print("\n--- Issues Found ---")
    for issue in data.get("issues", []):
        print(f"  [FAIL] {issue}")
    sys.exit(1)

