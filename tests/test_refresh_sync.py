import subprocess
import json
import os
import re
import sys

# Test 1: Loading at a hash anchor (simulating opening or refreshing at #playgrounds)
cmd_hash = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/index.html#playgrounds"
]

res_hash = subprocess.run(cmd_hash, capture_output=True, text=True, encoding="utf-8", errors="ignore")
dom_hash = res_hash.stdout

match_nav = re.search(r'<header[^>]+id="home-nav"[^>]*>', dom_hash)
if match_nav:
    nav_tag = match_nav.group(0)
    print("Nav tag with hash #playgrounds:", nav_tag)
    assert "is-scrolled" in nav_tag, f"Expected is-scrolled class on direct deep link, got: {nav_tag}"
    print("  [PASS] Hash link immediately renders with .is-scrolled!")
else:
    print("[FAIL] Could not find home-nav in DOM")
    sys.exit(1)

# Test 2: In-browser test checking initial paint state vs after load
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

    // Wait 200ms for safety timeout to have unlocked transitions
    await new Promise(r => setTimeout(r, 200));

    const results = {
        noTransitionRemoved: !nav.classList.contains('no-transition'),
        brandMarkTransition: win.getComputedStyle(nav.querySelector('.brand-mark')).transition
    };

    document.getElementById('results').textContent = JSON.stringify(results);
});
</script>
</body>
</html>
"""

with open("tests/temp_refresh_test.html", "w", encoding="utf-8") as f:
    f.write(harness_html)

eval_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--virtual-time-budget=2000",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/temp_refresh_test.html"
]

res = subprocess.run(eval_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
match = re.search(r'<div id="results">(\{.*?\})</div>', res.stdout)

if os.path.exists("tests/temp_refresh_test.html"):
    os.remove("tests/temp_refresh_test.html")

if match:
    data = json.loads(match.group(1))
    print("Transition unlock result:", data)
    assert data["noTransitionRemoved"] is True, "no-transition class should be removed after load"
    assert "0.25s" in data["brandMarkTransition"] or "0.2" in data["brandMarkTransition"]
    print("  [PASS] Transitions correctly unlocked for subsequent user scroll gestures!")
else:
    print("[FAIL] Could not get transition unlock result:", res.stdout[-500:])
    sys.exit(1)
