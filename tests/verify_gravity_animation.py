import subprocess
import json
import re
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

print("============================================================")
print("VERIFYING GRAVITY DROP & REVERSE GRAVITY LAUNCH PHYSICS")
print("============================================================")

all_passed = True

# 1. Static CSS Physics Rule Verification
print("\n--- 1. Verifying CSS Gravity Keyframes & Reverse Physics ---")
with open("css/visualizer.css", "r", encoding="utf-8") as f:
    css_content = f.read()

# Forward gravity fall (Adding elements)
assert "@keyframes gravity-fall" in css_content, "Missing @keyframes gravity-fall"
assert "translateY(-140px)" in css_content or "translateY(-160px)" in css_content, "gravity-fall must drop from height"
assert "scaleY(0.82)" in css_content or "scaleY(0.84)" in css_content or "scaleY(0.85)" in css_content, "gravity-fall must include elastic ground compression"
assert "scaleX(1.12)" in css_content or "scaleX(1.10)" in css_content, "gravity-fall must include elastic squash bulge"
assert "transform-origin: bottom center" in css_content, "Must anchor transform-origin at bottom center"
assert ".bar.drop-in" in css_content, "Missing .bar.drop-in selector"
assert ".cell.drop-in" in css_content, "Missing .cell.drop-in selector"

# Reverse gravity launch (Decreasing elements)
assert "@keyframes gravity-launch" in css_content, "Missing @keyframes gravity-launch"
assert ".bar-launching" in css_content, "Missing .bar-launching selector"
assert ".cell-launching" in css_content, "Missing .cell-launching selector"
assert "prefers-reduced-motion" in css_content, "Must support prefers-reduced-motion accessibility"
print("  [PASS] Forward and Reverse CSS keyframes, elastic ground compression, and launch physics verified!")


# 2. Headless Chrome Runtime Physics & Live Sliding Test
print("\n--- 2. Verifying Runtime Gravity Drop & Reverse Launch in Chrome ---")

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

    // 3. Slide down from 19 to 8 bars (inspect launching bars in reverse physics)
    sortSlider.value = 8;
    sortSlider.dispatchEvent(new sortWin.Event('input', { bubbles: true }));
    const launchingBars = sortArea.querySelectorAll('.bar-launching');
    const remainingBars = sortArea.querySelectorAll('.bar');
    let launchAnim = '';
    if (launchingBars.length > 0) {
        launchAnim = sortWin.getComputedStyle(launchingBars[0]).animationName;
    }

    results.sorting.decreasedCount = remainingBars.length;
    results.sorting.launchingCount = launchingBars.length;
    results.sorting.launchAnimation = launchAnim;

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

    // 3. Slide down to 6 cells (inspect launching cells in reverse physics)
    searchSlider.value = 6;
    searchSlider.dispatchEvent(new searchWin.Event('input', { bubbles: true }));
    const launchingCells = searchArea.querySelectorAll('.cell-launching');
    const remainingCells = searchArea.querySelectorAll('.cell');
    let cellLaunchAnim = '';
    if (launchingCells.length > 0) {
        cellLaunchAnim = searchWin.getComputedStyle(launchingCells[0]).animationName;
    }

    results.searching.decreasedCount = remainingCells.length;
    results.searching.launchingCount = launchingCells.length;
    results.searching.launchAnimation = cellLaunchAnim;

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

print(f"  After sliding down (8): {sort_res['decreasedCount']} remaining bars, {sort_res['launchingCount']} launching bars, launchAnimation: '{sort_res['launchAnimation']}'")
assert sort_res["decreasedCount"] == 8, f"Expected 8 bars, got {sort_res['decreasedCount']}"
assert sort_res["launchingCount"] == 11, f"Expected 11 launching bars (19 - 8), got {sort_res['launchingCount']}"
assert "gravity-launch" in sort_res["launchAnimation"], f"Expected gravity-launch animation, got {sort_res['launchAnimation']}"
assert "/" in sort_res["stepDisplay"], "Sorting playback must run on resized array"
print(f"  [PASS] Removed bars catapult into the sky following reverse gravity physics!")

# Assertions for searching
print(f"\nSearching Visualizer:")
print(f"  Initial cells: {search_res['initCount']}")
print(f"  After sliding up (+3): {search_res['newCount']}, hasDropIn: {search_res['hasDropInClass']}, animation: {search_res['animationName']}")
assert search_res["newCount"] == search_res["initCount"] + 3, f"Expected {search_res['initCount'] + 3} cells, got {search_res['newCount']}"
assert search_res["hasDropInClass"] is True, "Newly added cell must have 'drop-in' class"
assert "gravity-fall" in search_res["animationName"], f"Expected gravity-fall animation, got {search_res['animationName']}"
print(f"  [PASS] Newly added cells drop from height with gravity-fall physics animation!")

print(f"  After sliding down (6): {search_res['decreasedCount']} remaining cells, {search_res['launchingCount']} launching cells, launchAnimation: '{search_res['launchAnimation']}'")
assert search_res["decreasedCount"] == 6, f"Expected 6 cells, got {search_res['decreasedCount']}"
assert search_res["launchingCount"] == 12, f"Expected 12 launching cells (18 - 6), got {search_res['launchingCount']}"
assert "gravity-launch" in search_res["launchAnimation"], f"Expected gravity-launch animation, got {search_res['launchAnimation']}"
assert "/" in search_res["stepDisplay"], "Searching playback must run on resized array"
print(f"  [PASS] Removed cells catapult into the sky following reverse gravity physics!")

print("\n============================================================")
print("ALL GRAVITY & REVERSE PHYSICS VERIFICATIONS PASSED (100%)")
print("============================================================")
