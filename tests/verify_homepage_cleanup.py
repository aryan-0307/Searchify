import subprocess
import os
import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("VERIFYING HOMEPAGE HERO CLEANUP (NO STRAY DUPLICATES)")
print("=" * 60)

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Verify no orphan code line or code-card-foot outside hero-code-card
lines_04 = re.findall(r'<div class="hero-code-line"><small>04</small><code>\s*// repeat &amp; improve</code></div>', html)
mini_bars = re.findall(r'<div class="hero-mini-bars"', html)
card_foot = re.findall(r'<div class="code-card-foot"', html)

print(f"  Count of line 04: {len(lines_04)} (expected <= 1 inside hero-code-card)")
print(f"  Count of hero-mini-bars: {len(mini_bars)} (expected <= 1 inside hero-code-card)")
print(f"  Count of code-card-foot: {len(card_foot)} (expected <= 1 inside hero-code-card)")

assert len(lines_04) <= 1, f"Found {len(lines_04)} occurrences of line 04 (expected at most 1)"
assert len(mini_bars) <= 1, f"Found {len(mini_bars)} occurrences of hero-mini-bars (expected at most 1)"
assert len(card_foot) <= 1, f"Found {len(card_foot)} occurrences of code-card-foot (expected at most 1)"

# 2. Check DOM structure via Headless Chrome
script_html = """<!DOCTYPE html>
<html><body>
<iframe id="f" src="../index.html" style="width:1440px;height:1200px;"></iframe>
<script>
var f = document.getElementById("f");
f.onload = function() {
    var doc = f.contentDocument;
    var container = doc.querySelector(".home-container");
    var strayChildren = [];
    Array.from(container.children).forEach(function(el) {
        if (el.classList.contains("hero-code-line") || 
            el.classList.contains("hero-mini-bars") || 
            el.classList.contains("code-card-foot") ||
            el.classList.contains("floating-chip") ||
            el.classList.contains("hero-sparkle")) {
            strayChildren.push(el.className);
        }
    });
    var stats = doc.querySelector(".home-stats");
    var hero = doc.querySelector(".home-hero");
    
    var validSequence = (hero.nextElementSibling === stats);
    
    var res = {
        strayCount: strayChildren.length,
        strayClasses: strayChildren,
        validSequence: validSequence
    };
    
    var pre = document.createElement("pre");
    pre.id = "result";
    pre.textContent = JSON.stringify(res);
    document.body.appendChild(pre);
};
</script>
</body></html>"""

with open("tests/temp_hero_cleanup_test.html", "w", encoding="utf-8") as f:
    f.write(script_html)

cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--virtual-time-budget=2000",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/temp_hero_cleanup_test.html"
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
if os.path.exists("tests/temp_hero_cleanup_test.html"):
    os.remove("tests/temp_hero_cleanup_test.html")

assert '<pre id="result">' in res.stdout, "Failed to get DOM result from Headless Chrome"
import json
data = json.loads(res.stdout.split('<pre id="result">')[1].split("</pre>")[0])

assert data["strayCount"] == 0, f"Found stray children in home-container: {data['strayClasses']}"
assert data["validSequence"] is True, "Expected .home-stats to be immediate next sibling of .home-hero"

print("  [PASS] Zero stray children in .home-container")
print("  [PASS] .home-stats immediately follows .home-hero with no leaking elements")
print("\n" + "=" * 60)
print("ALL HERO CLEANUP VERIFICATIONS PASSED (100%)")
print("=" * 60)

