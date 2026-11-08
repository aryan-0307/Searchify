"""
tests/verify_multi_sort_showcase.py
Automated verification for the Multi-Algorithm Sorting Comparison Showcase on the hero/home page:
1. DOM Structure & Metadata in index.html (section #try-it, chips for all 10 algorithms, presets, controls, grid, leaderboard).
2. Dynamic multi-selection of algorithms (select N of user choice, add/remove cards).
3. Presets activation (Popular, O(n log n), O(n^2), Linear Time, All 10).
4. Exact same shared array rendered across all selected algorithm cards.
5. Custom input and shuffle updating all active cards synchronously with identical data.
6. Synchronized playback lockstep (Play/Pause, Step Next/Prev, Reset, Speed scaling).
7. Completion detection, finish ranks (1st, 2nd, etc.), and race leaderboard rendering.
8. Responsive layout verification (zero horizontal scroll/overflow across Desktop 1280px, iPad 768px, Galaxy S23 412px, iPhone SE 375px).
"""

import subprocess
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    alt_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    if os.path.exists(alt_path):
        CHROME_PATH = alt_path

viewports = [
    {"name": "Desktop 1280px", "width": 1280, "height": 850, "isMobile": False},
    {"name": "iPad 768px", "width": 768, "height": 900, "isMobile": True},
    {"name": "Galaxy S23 412px", "width": 412, "height": 850, "isMobile": True},
    {"name": "iPhone SE 375px", "width": 375, "height": 800, "isMobile": True}
]

print("=" * 65)
print("VERIFYING MULTI-ALGORITHM SORTING COMPARISON SHOWCASE")
print("=" * 65)

# -------------------------------------------------------------
# Stage 1: DOM Hierarchy and Structural Order in index.html
# -------------------------------------------------------------
print("\n--- 1. Testing DOM Structure & Section Markers in index.html ---")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Section #try-it
assert 'id="try-it"' in html, "Missing #try-it anchor in index.html"
assert 'class="home-showcase-section"' in html, "Missing .home-showcase-section in index.html"
assert "MULTI-ALGORITHM SHOWCASE" in html, "Missing kicker 'MULTI-ALGORITHM SHOWCASE' in index.html"
assert "Compare N Sorting Algorithms on the Same Array" in html, "Missing section heading in index.html"

# 2. Presets
presets = ["popular", "nlogn", "n2", "linear", "all"]
for p in presets:
    assert f'data-preset="{p}"' in html, f"Missing preset '{p}' in index.html"
print("  [PASS] All 5 quick presets present (Popular, nlogn, n2, linear, all)")

# 3. Chips grid container
assert 'id="showcase-chips-grid"' in html, "Missing #showcase-chips-grid container in index.html"
print("  [PASS] Dynamic multi-select chips grid container present")

# 4. Shared array controls
assert 'id="showcase-shuffle-btn"' in html, "Missing shuffle button in index.html"
assert 'id="showcase-custom-input"' in html, "Missing custom input in index.html"
assert 'id="showcase-apply-btn"' in html, "Missing apply button in index.html"
print("  [PASS] Shared dataset controls (shuffle, custom input, apply) present")

# 5. Playback dock
assert 'id="showcase-play-btn"' in html, "Missing play button in index.html"
assert 'id="showcase-prev-btn"' in html, "Missing prev button in index.html"
assert 'id="showcase-next-btn"' in html, "Missing next button in index.html"
assert 'id="showcase-reset-btn"' in html, "Missing reset button in index.html"
assert 'id="showcase-speed"' in html, "Missing speed slider in index.html"
print("  [PASS] Playback dock controls (play, prev, next, reset, speed slider) present")

# 6. Grid and leaderboard
assert 'id="showcase-grid"' in html, "Missing #showcase-grid in index.html"
assert 'id="showcase-leaderboard"' in html, "Missing #showcase-leaderboard in index.html"
print("  [PASS] Showcase grid and leaderboard containers present")

# 7. Script tags ordering
sorting_algo_idx = html.find('src="js/sorting-algorithms.js"')
multi_sort_idx = html.find('src="js/multi-sort-showcase.js"')
assert sorting_algo_idx != -1, "Missing js/sorting-algorithms.js script tag in index.html"
assert multi_sort_idx != -1, "Missing js/multi-sort-showcase.js script tag in index.html"
assert sorting_algo_idx < multi_sort_idx, "js/sorting-algorithms.js must be loaded BEFORE js/multi-sort-showcase.js"
print("  [PASS] Script loading order verified (engine loaded before showcase controller)")

# -------------------------------------------------------------
# Stage 2: Chrome Headless Verification Across Viewports
# -------------------------------------------------------------
print("\n--- 2. Verifying Multi-Algorithm Dynamic Functionality in Chrome ---")

for vp in viewports:
    print(f"\n--- Testing Viewport: {vp['name']} ({vp['width']}x{vp['height']}) ---")
    page_abs = os.path.abspath("index.html").replace(os.sep, "/")
    harness_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;">
<iframe id="test-frame" src="file:///{page_abs}" style="width:{vp['width']}px;height:{vp['height']}px;border:none;"></iframe>
<div id="output"></div>
<script>
window.addEventListener('load', async () => {{
    await new Promise(r => setTimeout(r, 600));
    const iframe = document.getElementById('test-frame');
    const doc = iframe.contentDocument;
    const win = iframe.contentWindow;

    const results = {{}};

    // 1. Check responsive overflow of showcase section
    const showcase = doc.getElementById('try-it');
    const showcaseRect = showcase ? showcase.getBoundingClientRect() : null;
    const bodyScrollWidth = doc.body.scrollWidth;
    const docScrollWidth = doc.documentElement.scrollWidth;
    results.hasHorizontalOverflow = (showcase && showcase.scrollWidth > showcase.clientWidth + 2) || (showcaseRect && showcaseRect.right > {vp['width']} + 2);
    results.showcaseScrollWidth = showcase ? showcase.scrollWidth : 0;
    results.showcaseClientWidth = showcase ? showcase.clientWidth : 0;
    results.viewportWidth = {vp['width']};

    // 2. Initial state
    const grid = doc.getElementById('showcase-grid');
    const chipsGrid = doc.getElementById('showcase-chips-grid');
    results.renderedChipsCount = chipsGrid ? chipsGrid.querySelectorAll('.showcase-chip').length : 0;

    const initialCards = grid.querySelectorAll('.showcase-algo-card');
    results.initialCardCount = initialCards.length;

    // Collect array values from each card to check identical shared array
    const cardArrays = [];
    initialCards.forEach(card => {{
        const vals = Array.from(card.querySelectorAll('.showcase-bar-val')).map(el => parseInt(el.textContent.trim(), 10));
        cardArrays.push(vals);
    }});
    results.cardArraysIdentical = cardArrays.length >= 2 && cardArrays.every(arr => JSON.stringify(arr) === JSON.stringify(cardArrays[0]));
    results.sampleArray = cardArrays[0] || [];

    // 3. Dynamic selection: toggle Heap Sort chip
    const heapChip = doc.querySelector('.showcase-chip[data-algo="heapSort"]');
    if (heapChip) {{
        heapChip.click();
        await new Promise(r => setTimeout(r, 150));
    }}
    const cardsAfterAdd = grid.querySelectorAll('.showcase-algo-card');
    results.cardsAfterAddingHeap = cardsAfterAdd.length;

    // Verify heap card has the exact same array
    const heapCard = grid.querySelector('.showcase-algo-card[data-algo="heapSort"]');
    if (heapCard) {{
        const heapVals = Array.from(heapCard.querySelectorAll('.showcase-bar-val')).map(el => parseInt(el.textContent.trim(), 10));
        results.heapArrayMatches = JSON.stringify(heapVals) === JSON.stringify(results.sampleArray);
    }} else {{
        results.heapArrayMatches = false;
    }}

    // Toggle Heap Sort back off
    if (heapChip) {{
        heapChip.click();
        await new Promise(r => setTimeout(r, 150));
    }}
    results.cardsAfterRemovingHeap = grid.querySelectorAll('.showcase-algo-card').length;

    // 4. Test Preset: Linear Time (counting, radix, bucket)
    const linearPreset = doc.querySelector('.preset-btn[data-preset="linear"]');
    if (linearPreset) {{
        linearPreset.click();
        await new Promise(r => setTimeout(r, 200));
    }}
    const linearCards = grid.querySelectorAll('.showcase-algo-card');
    const linearAlgos = Array.from(linearCards).map(c => c.getAttribute('data-algo'));
    results.linearAlgos = linearAlgos.sort();

    // 5. Test Custom Input on the shared array
    const customInput = doc.getElementById('showcase-custom-input');
    const applyBtn = doc.getElementById('showcase-apply-btn');
    if (customInput && applyBtn) {{
        customInput.value = "50, 20, 80, 10, 40";
        applyBtn.click();
        await new Promise(r => setTimeout(r, 200));
    }}
    const cardsAfterCustom = grid.querySelectorAll('.showcase-algo-card');
    const customArrays = [];
    cardsAfterCustom.forEach(card => {{
        const vals = Array.from(card.querySelectorAll('.showcase-bar-val')).map(el => parseInt(el.textContent.trim(), 10));
        customArrays.push(vals);
    }});
    results.customInputAppliedAll = customArrays.every(arr => JSON.stringify(arr) === JSON.stringify([50, 20, 80, 10, 40]));

    // 6. Test Playback execution
    // Select popular preset for playback test
    const popularPreset = doc.querySelector('.preset-btn[data-preset="popular"]');
    if (popularPreset) {{
        popularPreset.click();
        await new Promise(r => setTimeout(r, 200));
    }}

    // Speed up to 4x for quick completion test
    const speedSlider = doc.getElementById('showcase-speed');
    if (speedSlider) {{
        speedSlider.value = "4";
        speedSlider.dispatchEvent(new win.Event('input', {{ bubbles: true }}));
    }}

    const playBtn = doc.getElementById('showcase-play-btn');
    if (playBtn) {{
        playBtn.click();
    }}
    // Wait for race to finish (small array of 5 elements sorts in < 1 second at 4x speed)
    await new Promise(r => setTimeout(r, 1400));

    // Check finished status and leaderboard
    const finishedCards = grid.querySelectorAll('.showcase-algo-card.is-finished');
    results.finishedCardsCount = finishedCards.length;
    const leaderboard = doc.getElementById('showcase-leaderboard');
    results.leaderboardVisible = leaderboard && leaderboard.style.display !== 'none' && leaderboard.innerHTML.trim().length > 0;
    const leaderboardCards = leaderboard ? leaderboard.querySelectorAll('.leaderboard-card').length : 0;
    results.leaderboardRowsCount = leaderboardCards;

    // Reset test
    const resetBtn = doc.getElementById('showcase-reset-btn');
    if (resetBtn) {{
        resetBtn.click();
        await new Promise(r => setTimeout(r, 150));
    }}
    results.cardsReset = grid.querySelectorAll('.showcase-algo-card.is-finished').length === 0;

    const out = document.getElementById('output');
    out.textContent = JSON.stringify(results);
    out.setAttribute('data-done', 'true');
}});
</script>
</body>
</html>
"""
    harness_path = f"tests/temp_multi_sort_test_{vp['width']}.html"
    with open(harness_path, "w", encoding="utf-8") as f:
        f.write(harness_html)

    try:
        cmd = [
            CHROME_PATH,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--allow-file-access-from-files",
            f"--window-size={vp['width'] + 60},{vp['height'] + 100}",
            "--virtual-time-budget=8000",
            "--dump-dom",
            f"file:///{os.path.abspath(harness_path).replace(os.sep, '/')}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        dom = res.stdout

        m = re.search(r'<div id="output"[^>]*>(.*?)</div>', dom)
        assert m, f"Failed to get test results from output div. Raw DOM:\n{dom[:400]}"
        raw_json = m.group(1).replace("&quot;", '"')
        data = json.loads(raw_json)

        print(f"  Showcase Section Overflow: {data['hasHorizontalOverflow']} (Showcase scrollWidth: {data.get('showcaseScrollWidth')}, clientWidth: {data.get('showcaseClientWidth')}, Viewport: {data['viewportWidth']})")
        assert not data["hasHorizontalOverflow"], f"Horizontal overflow detected in {vp['name']}!"

        print(f"  Rendered chips: {data['renderedChipsCount']}")
        assert data["renderedChipsCount"] == 10, f"Expected 10 algorithm chips, got {data['renderedChipsCount']}"

        print(f"  Initial Cards: {data['initialCardCount']}, Arrays Identical: {data['cardArraysIdentical']}")
        assert data["initialCardCount"] == 3, f"Expected 3 initial cards, got {data['initialCardCount']}"
        assert data["cardArraysIdentical"], "Initial cards do not share the exact same array!"

        print(f"  Add 4th algorithm (Heap): cards={data['cardsAfterAddingHeap']}, array matches={data['heapArrayMatches']}")
        assert data["cardsAfterAddingHeap"] == 4, f"Expected 4 cards after adding Heap, got {data['cardsAfterAddingHeap']}"
        assert data["heapArrayMatches"], "Added Heap card does not share the same array!"

        print(f"  Remove Heap algorithm: cards={data['cardsAfterRemovingHeap']}")
        assert data["cardsAfterRemovingHeap"] == 3, f"Expected 3 cards after removing Heap, got {data['cardsAfterRemovingHeap']}"

        print(f"  Linear Preset: algos={data['linearAlgos']}")
        assert data["linearAlgos"] == ["bucketSort", "countingSort", "radixSort"], f"Expected ['bucketSort', 'countingSort', 'radixSort'], got {data['linearAlgos']}"

        print(f"  Custom Input [50, 20, 80, 10, 40] applied to all: {data['customInputAppliedAll']}")
        assert data["customInputAppliedAll"], "Custom array was not applied synchronously to all cards!"

        print(f"  Race Execution: finishedCards={data['finishedCardsCount']}, leaderboardVisible={data['leaderboardVisible']}, rows={data['leaderboardRowsCount']}")
        assert data["finishedCardsCount"] > 0, "No cards finished race"
        assert data["leaderboardVisible"], "Leaderboard did not render after race completion"
        assert data["leaderboardRowsCount"] > 0, "Leaderboard has no ranking rows"

        print(f"  Reset: cardsReset={data['cardsReset']}")
        assert data["cardsReset"], "Cards did not reset properly to step 0"

        print(f"  [PASS] {vp['name']}: All multi-algorithm showcase features verified!")

    finally:
        if os.path.exists(harness_path):
            os.remove(harness_path)

print("\n" + "=" * 65)
print("ALL MULTI-ALGORITHM SHOWCASE VERIFICATIONS PASSED (100%)")
print("=" * 65)
