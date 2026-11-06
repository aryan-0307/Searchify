import subprocess
import json
import re
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

print("============================================================")
print("VERIFYING GRAVITY DROP & NATURAL BOUNCE PHYSICS")
print("============================================================")

all_passed = True

# 1. Static CSS Physics Rule Verification
print("\n--- 1. Verifying CSS Gravity Keyframes & Transform-Origin ---")
with open("css/visualizer.css", "r", encoding="utf-8") as f:
    css_content = f.read()

assert "@keyframes gravity-fall" in css_content, "Missing @keyframes gravity-fall"
assert "translateY(-140px)" in css_content or "translateY(-160px)" in css_content, "gravity-fall must drop from height"
assert "scaleY(0.82)" in css_content or "scaleY(0.84)" in css_content or "scaleY(0.85)" in css_content, "gravity-fall must include elastic ground compression"
assert "scaleX(1.12)" in css_content or "scaleX(1.10)" in css_content, "gravity-fall must include elastic squash bulge"
assert "transform-origin: bottom center" in css_content, "Must anchor transform-origin at bottom center"
assert ".bar.drop-in" in css_content, "Missing .bar.drop-in selector"
assert ".cell.drop-in" in css_content, "Missing .cell.drop-in selector"
assert "prefers-reduced-motion" in css_content, "Must support prefers-reduced-motion accessibility"
print("  [PASS] CSS keyframes, elastic ground compression, and transform-origin verified!")


# 2. Headless Chrome Runtime Physics & Live Sliding Test
print("\n--- 2. Verifying Runtime Gravity Drop & Live Sliding in Chrome ---")

test_html_content = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<iframe id="sort-frame" src="../sorting.html" style="width: 1200px; height: 800px; border: 0;"></iframe>
<iframe id="search-frame" src="../searching.html" style="width: 1200px; height: 800px; border: 0;"></iframe>
<div id="results"></div>

<script>
window.addEventListener('load', async () => {
    await new Promise(r => setTimeout(r, 200));

    const results = {};

    // --- SORTING VISUALIZER ---
    const sortWin = document.getElementById('sort-frame').contentWindow;
    const sortDoc = document.getElementById('sort-frame').contentDocument;
    const sortSlider = sortDoc.getElementById('array-size');
    const sortArea = sortDoc.getElementById('visualization-area');

    // 1. Initial bars
    const initBars = sortArea.querySelectorAll('.bar');
    const initCount = initBars.length;

    // 2. Slide up to add 4 bars
    sortSlider.value = initCount + 4;
    sortSlider.dispatchEvent(new sortWin.Event('input', { bubbles: true }));

    // Check immediately for new bars having .drop-in and animation-name
    const barsAfterInc = sortArea.querySelectorAll('.bar');
    const newBar = barsAfterInc[barsAfterInc.length - 1];
    const newBarComputed = sortWin.getComputedStyle(newBar);

    results.sorting = {
        initCount: initCount,
        newCount: barsAfterInc.length,
        hasDropInClass: newBar.classList.contains('drop-in'),
        animationName: newBarComputed.animationName,
        transformOrigin: newBarComputed.transformOrigin
    };

    // 3. Slide down to 8 bars
    sortSlider.value = 8;
    sortSlider.dispatchEvent(new sortWin.Event('input', { bubbles: true }));
    const barsAfterDec = sortArea.querySelectorAll('.bar');
    results.sorting.decreasedCount = barsAfterDec.length;

    // 4. Test Playback after sliding
    sortDoc.getElementById('play-btn').click();
    await new Promise(r => setTimeout(r, 120));
    results.sorting.stepDisplay = sortDoc.getElementById('step-display').textContent.trim();


    // --- SEARCHING VISUALIZER ---
    const searchWin = document.getElementById('search-frame').contentWindow;
    const searchDoc = document.getElementById('search-frame').contentDocument;
    const searchSlider = searchDoc.getElementById('array-size');
    const searchArea = searchDoc.getElementById('visualization-area');

    // 1. Initial cells
    const initCells = searchArea.querySelectorAll('.cell');
    const initCellCount = initCells.length;

    // 2. Slide up to add 3 cells
    searchSlider.value = initCellCount + 3;
    searchSlider.dispatchEvent(new searchWin.Event('input', { bubbles: true }));

    const cellsAfterInc = searchArea.querySelectorAll('.cell');
    const newCell = cellsAfterInc[cellsAfterInc.length - 1];
    const newCellComputed = searchWin.getComputedStyle(newCell);

    results.searching = {
        initCount: initCellCount,
        newCount: cellsAfterInc.length,
        hasDropInClass: newCell.classList.contains('drop-in'),
        animationName: newCellComputed.animationName,
        transformOrigin: newCellComputed.transformOrigin
    };

    // 3. Slide down to 6 cells
    searchSlider.value = 6;
    searchSlider.dispatchEvent(new searchWin.Event('input', { bubbles: true }));
    const cellsAfterDec = searchArea.querySelectorAll('.cell');
    results.searching.decreasedCount = cellsAfterDec.length;

    // 4. Test Playback after sliding
    searchDoc.getElementById('play-btn').click();
    await new Promise(r => setTimeout(r, 120));
    results.searching.stepDisplay = searchDoc.getElementById('step-display').textContent.trim();

    document.getElementById('results').textContent = JSON.stringify(results);
});
</script>
</body>
</html>
"""

temp_file = "tests/temp_test_gravity.html"
with open(temp_file, "w", encoding="utf-8") as f:
    f.write(test_html_content)

chrome_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=5000",
    "--dump-dom",
    "file:///" + os.path.abspath(temp_file).replace("\\", "/")
]

res = subprocess.run(chrome_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
if os.path.exists(temp_file):
    os.remove(temp_file)

dom = res.stdout
match = re.search(r'<div id="results"[^>]*>(.*?)</div>', dom)
if not match or not match.group(1).strip():
    print("[FAIL] Could not extract gravity runtime results from test DOM.")
    sys.exit(1)

data = json.loads(match.group(1))
sort_res = data["sorting"]
search_res = data["searching"]

# Assertions for sorting
print(f"Sorting Visualizer:")
print(f"  Initial bars: {sort_res['initCount']}")
print(f"  After sliding up (+4): {sort_res['newCount']}, hasDropIn: {sort_res['hasDropInClass']}, animation: {sort_res['animationName']}")
assert sort_res["newCount"] == sort_res["initCount"] + 4, f"Expected {sort_res['initCount'] + 4} bars, got {sort_res['newCount']}"
assert sort_res["hasDropInClass"] is True, "Newly added bar must have 'drop-in' class"
assert "gravity-fall" in sort_res["animationName"], f"Expected gravity-fall animation, got {sort_res['animationName']}"
print(f"  [PASS] Newly added bars drop from height with gravity-fall physics animation!")

print(f"  After sliding down (8): {sort_res['decreasedCount']} bars, step playback: '{sort_res['stepDisplay']}'")
assert sort_res["decreasedCount"] == 8, f"Expected 8 bars, got {sort_res['decreasedCount']}"
assert "/" in sort_res["stepDisplay"], "Sorting playback must run on resized array"
print(f"  [PASS] Sorting live removal and playback smoothly synchronized!")

# Assertions for searching
print(f"\nSearching Visualizer:")
print(f"  Initial cells: {search_res['initCount']}")
print(f"  After sliding up (+3): {search_res['newCount']}, hasDropIn: {search_res['hasDropInClass']}, animation: {search_res['animationName']}")
assert search_res["newCount"] == search_res["initCount"] + 3, f"Expected {search_res['initCount'] + 3} cells, got {search_res['newCount']}"
assert search_res["hasDropInClass"] is True, "Newly added cell must have 'drop-in' class"
assert "gravity-fall" in search_res["animationName"], f"Expected gravity-fall animation, got {search_res['animationName']}"
print(f"  [PASS] Newly added cells drop from height with gravity-fall physics animation!")

print(f"  After sliding down (6): {search_res['decreasedCount']} cells, step playback: '{search_res['stepDisplay']}'")
assert search_res["decreasedCount"] == 6, f"Expected 6 cells, got {search_res['decreasedCount']}"
assert "/" in search_res["stepDisplay"], "Searching playback must run on resized array"
print(f"  [PASS] Searching live removal and playback smoothly synchronized!")

print("\n============================================================")
print("ALL GRAVITY PHYSICS VERIFICATIONS PASSED (100%)")
print("============================================================")

