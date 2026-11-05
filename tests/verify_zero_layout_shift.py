import subprocess
import json
import os
import re
import sys

harness_html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<iframe id="test-frame" src="../index.html" style="width: 1200px; height: 800px; border: 0;"></iframe>
<div id="results"></div>
<script>
window.addEventListener('load', () => {
    const frame = document.getElementById('test-frame');
    const win = frame.contentWindow;
    const doc = frame.contentDocument;

    const nav = doc.getElementById('home-nav');
    const hero = doc.querySelector('.home-hero');

    const results = [];

    // 1. Initial State Measurement
    const h1Nav = nav.getBoundingClientRect().height;
    const topHero1 = hero.getBoundingClientRect().top;
    const padNav1 = win.getComputedStyle(nav).paddingTop;

    // 2. Add is-scrolled (simulate scrolling down)
    nav.classList.add('is-scrolled');
    const h2Nav = nav.getBoundingClientRect().height;
    const topHero2 = hero.getBoundingClientRect().top;
    const padNav2 = win.getComputedStyle(nav).paddingTop;

    // 3. Remove is-scrolled (simulate scrolling up)
    nav.classList.remove('is-scrolled');
    const h3Nav = nav.getBoundingClientRect().height;
    const topHero3 = hero.getBoundingClientRect().top;
    const padNav3 = win.getComputedStyle(nav).paddingTop;

    results.push({
        h1Nav, h2Nav, h3Nav,
        topHero1, topHero2, topHero3,
        padNav1, padNav2, padNav3,
        heightDelta: Math.abs(h2Nav - h1Nav),
        heroDelta: Math.abs(topHero2 - topHero1)
    });

    document.getElementById('results').textContent = JSON.stringify(results);
});
</script>
</body>
</html>
"""

with open("tests/temp_shift_test.html", "w", encoding="utf-8") as f:
    f.write(harness_html)

eval_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/temp_shift_test.html"
]

res = subprocess.run(eval_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
match = re.search(r'<div id="results">(\[.*?\])</div>', res.stdout)

if os.path.exists("tests/temp_shift_test.html"):
    os.remove("tests/temp_shift_test.html")

if not match:
    print("[FAIL] Could not extract layout shift results:", res.stdout[-500:])
    sys.exit(1)

data = json.loads(match.group(1))[0]
print(f"Navbar height default: {data['h1Nav']}px, scrolled: {data['h2Nav']}px, restored: {data['h3Nav']}px")
print(f"Hero top position default: {data['topHero1']}px, scrolled: {data['topHero2']}px, restored: {data['topHero3']}px")
print(f"Height delta: {data['heightDelta']}px | Hero delta: {data['heroDelta']}px")

assert data["heightDelta"] == 0, f"Expected 0px height shift, got {data['heightDelta']}px"
assert data["heroDelta"] == 0, f"Expected 0px hero displacement, got {data['heroDelta']}px"
print("  [PASS] Zero layout shift verified (Navbar height and hero position remain 100% constant)!")

