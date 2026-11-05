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
window.addEventListener('load', async () => {
    const frame = document.getElementById('test-frame');
    const win = frame.contentWindow;
    const doc = frame.contentDocument;

    const nav = doc.getElementById('home-nav');
    const brandMark = nav.querySelector('.brand-mark');
    const brandText = nav.querySelector('.home-brand-text');

    // Wait for initial load protection (no-transition) to lift
    await new Promise(r => setTimeout(r, 150));

    const results = [];

    // Step 1: Default state (at top of page)
    const s1Nav = win.getComputedStyle(nav);
    const s1Text = win.getComputedStyle(brandText);
    const s1Mark = win.getComputedStyle(brandMark);

    results.push({
        step: "initial_top",
        isScrolled: nav.classList.contains('is-scrolled'),
        bg: s1Nav.backgroundColor,
        border: s1Nav.borderBottomColor,
        textOpacity: s1Text.opacity,
        textMaxWidth: s1Text.maxWidth,
        markTransform: s1Mark.transform,
        navTransition: s1Nav.transition,
        markTransition: s1Mark.transition,
        textTransition: s1Text.transition
    });

    // Step 2: Apply .is-scrolled (without transition to see final values)
    nav.style.transition = 'none';
    brandMark.style.transition = 'none';
    brandText.style.transition = 'none';
    nav.classList.add('is-scrolled');

    const s2Nav = win.getComputedStyle(nav);
    const s2Text = win.getComputedStyle(brandText);
    const s2Mark = win.getComputedStyle(brandMark);

    results.push({
        step: "scrolled_state",
        isScrolled: nav.classList.contains('is-scrolled'),
        bg: s2Nav.backgroundColor,
        border: s2Nav.borderBottomColor,
        textOpacity: s2Text.opacity,
        textMaxWidth: s2Text.maxWidth,
        markTransform: s2Mark.transform
    });

    // Step 3: Remove .is-scrolled (without transition to see restored final values)
    nav.classList.remove('is-scrolled');

    const s3Nav = win.getComputedStyle(nav);
    const s3Text = win.getComputedStyle(brandText);
    const s3Mark = win.getComputedStyle(brandMark);

    results.push({
        step: "restored_top",
        isScrolled: nav.classList.contains('is-scrolled'),
        bg: s3Nav.backgroundColor,
        border: s3Nav.borderBottomColor,
        textOpacity: s3Text.opacity,
        textMaxWidth: s3Text.maxWidth,
        markTransform: s3Mark.transform
    });

    document.getElementById('results').textContent = JSON.stringify(results);
});
</script>
</body>
</html>
"""

with open("tests/temp_nav_test.html", "w", encoding="utf-8") as f:
    f.write(harness_html)

eval_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--virtual-time-budget=2000",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/temp_nav_test.html"
]

res = subprocess.run(eval_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
match = re.search(r'<div id="results">(\[.*?\])</div>', res.stdout)

if os.path.exists("tests/temp_nav_test.html"):
    os.remove("tests/temp_nav_test.html")

if not match:
    print("[FAIL] Could not extract test results from DOM:", res.stdout[-500:])
    sys.exit(1)

data = json.loads(match.group(1))
initial = data[0]
scrolled = data[1]
restored = data[2]

# Verifications
assert initial["bg"] == scrolled["bg"] == restored["bg"], f"Navbar background color must be identical across all states, got: initial={initial['bg']}, scrolled={scrolled['bg']}"
assert "245, 243, 237" in initial["bg"], f"Expected warm ivory base in liquid glass, got: {initial['bg']}"
assert initial["border"] == scrolled["border"], f"Navbar border must be identical across all states, got: initial={initial['border']}, scrolled={scrolled['border']}"
print(f"  [PASS] Liquid glass background is identical across all states ({initial['bg']}) with zero base color difference!")

assert scrolled["isScrolled"] is True
assert scrolled["textMaxWidth"] == "0px"
assert scrolled["textOpacity"] == "0"
assert "18" in scrolled["markTransform"]
print("  [PASS] Scrolled navbar minimizes brand text and moves icon into text area")

assert restored["isScrolled"] is False
assert restored["textMaxWidth"] == "280px"
assert restored["textOpacity"] == "1"
print("  [PASS] Restored top navbar expands brand text and positions icon back at origin")

mark_t = initial.get("markTransition", "")
assert "0.2" in mark_t or "0.25" in mark_t, f"Mark transition must be snappy, got: {mark_t}"
print("  [PASS] Fast animation speeds verified (~0.25s snappy transition curves)")
