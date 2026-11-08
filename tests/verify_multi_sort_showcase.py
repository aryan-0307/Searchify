"""
tests/verify_multi_sort_showcase.py
Automated verification for the Multi-Algorithm Sorting Comparison Showcase:
1. DOM Structure & Minimalist Content in index.html:
   - Card 03 (.compare-card) in .home-cards with <figure class="mini-viz compare-mini-viz"> (visuals like searching and sorting).
   - Card 03 links to compare.html.
   - Minimalist preview section #try-it (.home-showcase-minimal, .showcase-feature-viz with multi-track preview).
   - Launch CTA button linking to compare.html.
   - Verifies heavy visualization grid (#showcase-grid) is NOT on index.html.
2. Dedicated Comparison Laboratory in compare.html:
   - Full interactive visualization with 10 algorithm chips, 5 presets, shared array controls.
   - Playback dock (play/pause, step backward/forward, reset, speed slider) with no 'Start' text.
   - Live simultaneous tracks (#showcase-grid) and leaderboard (#showcase-leaderboard).
   - Script loading order (sorting engine before showcase controller).
3. Chrome Headless Dynamic Execution Across Viewports:
   - Verified on compare.html across Desktop 1280px, iPad 768px, Galaxy S23 412px, iPhone SE 375px.
   - Zero horizontal overflow on compare.html and index.html across all viewports.
   - Dynamic algorithm selection, shared array updates, custom input, synchronized playback, and leaderboard race results.
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
# Stage 1: DOM Hierarchy in index.html (Minimalist Content & Hero Visuals)
# -------------------------------------------------------------
print("\n--- 1. Testing Minimalist Hero Content & Card Visuals in index.html ---")
with open("index.html", "r", encoding="utf-8") as f:
    html_home = f.read()

# 1. Card 03 in .home-cards with compare-mini-viz
assert 'compare-card' in html_home, "Missing .compare-card in index.html .home-cards"
assert 'compare-mini-viz' in html_home, "Missing .compare-mini-viz in index.html"
assert 'mini-race-tracks' in html_home, "Missing .mini-race-tracks inside compare-mini-viz"
assert 'href="compare.html"' in html_home, "Missing link to compare.html on index.html"
print("  [PASS] Card 03 (Comparison) with mini-race visual present in index.html")

# 2. Section #try-it has minimalist showcase preview
assert 'id="try-it"' in html_home, "Missing #try-it anchor in index.html"
assert 'home-showcase-minimal' in html_home, "Missing .home-showcase-minimal class in index.html"
assert 'showcase-feature-viz' in html_home, "Missing .showcase-feature-viz preview in index.html"
assert 'showcase-launch-btn' in html_home, "Missing launch CTA button in index.html"
assert "MULTI-ALGORITHM SHOWCASE" in html_home, "Missing kicker 'MULTI-ALGORITHM SHOWCASE' in index.html"
assert "Compare N Sorting Algorithms on the Same Array" in html_home, "Missing heading in index.html"
print("  [PASS] Minimalist preview section #try-it with feature viz and launch CTA present in index.html")

# 3. Heavy visualizer grid is NOT on index.html
assert 'id="showcase-grid"' not in html_home, "#showcase-grid should NOT be on index.html (it belongs in compare.html)"
assert 'js/multi-sort-showcase.js' not in html_home, "multi-sort-showcase.js should NOT be loaded on index.html"
print("  [PASS] Heavy visualizer grid and script correctly excluded from hero page")

# -------------------------------------------------------------
# Stage 2: DOM Hierarchy in compare.html (Actual Interactive Visualization)
# -------------------------------------------------------------
print("\n--- 2. Testing Dedicated Visualization Laboratory in compare.html ---")
with open("compare.html", "r", encoding="utf-8") as f:
    html_compare = f.read()

# 1. Section #try-it
assert 'id="try-it"' in html_compare, "Missing #try-it anchor in compare.html"
assert 'class="home-showcase-section' in html_compare, "Missing .home-showcase-section in compare.html"
assert "MULTI-ALGORITHM SHOWCASE" in html_compare, "Missing kicker 'MULTI-ALGORITHM SHOWCASE' in compare.html"
assert "Compare N Sorting Algorithms on the Same Array" in html_compare, "Missing section heading in compare.html"

# 2. Presets
presets = ["popular", "nlogn", "n2", "linear", "all"]
for p in presets:
    assert f'data-preset="{p}"' in html_compare, f"Missing preset '{p}' in compare.html"
print("  [PASS] All 5 quick presets present (Popular, nlogn, n2, linear, all) in compare.html")

# 3. Chips grid container
assert 'id="showcase-chips-grid"' in html_compare, "Missing #showcase-chips-grid container in compare.html"
print("  [PASS] Dynamic multi-select chips grid container present in compare.html")

# 4. Shared array controls
assert 'id="showcase-shuffle-btn"' in html_compare, "Missing shuffle button in compare.html"
assert 'id="showcase-custom-input"' in html_compare, "Missing custom input in compare.html"
assert 'id="showcase-apply-btn"' in html_compare, "Missing apply button in compare.html"
print("  [PASS] Shared dataset controls (shuffle, custom input, apply) present in compare.html")

# 5. Playback dock
assert 'id="showcase-play-btn"' in html_compare, "Missing play button in compare.html"
assert 'Start Race' not in html_compare, "'Start Race' text should be removed from the play button in compare.html"
assert 'id="showcase-prev-btn"' in html_compare, "Missing prev button in compare.html"
assert 'id="showcase-next-btn"' in html_compare, "Missing next button in compare.html"
assert 'id="showcase-reset-btn"' in html_compare, "Missing reset button in compare.html"
assert 'id="showcase-speed"' in html_compare, "Missing speed slider in compare.html"
print("  [PASS] Playback dock controls (play/pause, prev, next, reset, speed slider) present without 'Start' text")

# 6. Grid and leaderboard
assert 'id="showcase-grid"' in html_compare, "Missing #showcase-grid in compare.html"
assert 'id="showcase-leaderboard"' in html_compare, "Missing #showcase-leaderboard in compare.html"
print("  [PASS] Showcase grid and leaderboard containers present in compare.html")

# 7. Script tags ordering
sorting_algo_idx = html_compare.find('src="js/sorting-algorithms.js"')
multi_sort_idx = html_compare.find('src="js/multi-sort-showcase.js"')
assert sorting_algo_idx != -1, "Missing js/sorting-algorithms.js script tag in compare.html"
assert multi_sort_idx != -1, "Missing js/multi-sort-showcase.js script tag in compare.html"
assert sorting_algo_idx < multi_sort_idx, "js/sorting-algorithms.js must be loaded BEFORE js/multi-sort-showcase.js in compare.html"
print("  [PASS] Script loading order verified on compare.html")

# -------------------------------------------------------------
# Stage 3: Chrome Headless Verification on compare.html Across Viewports
# -------------------------------------------------------------
print("\n--- 3. Verifying Multi-Algorithm Dynamic Functionality on compare.html ---")

for vp in viewports:
    print(f"\n--- Testing compare.html Viewport: {vp['name']} ({vp['width']}x{vp['height']}) ---")
    page_abs = os.path.abspath("compare.html").replace(os.sep, "/")
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
    results.playBtnHasStartText = playBtn ? /Start/i.test(playBtn.textContent) : false;
    results.playBtnIconBefore = playBtn ? playBtn.textContent.trim() : "";
    if (playBtn) {{
        playBtn.click();
    }}
    // Wait for race to finish
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

        print(f"  Play Button: hasStartText={data['playBtnHasStartText']}, iconBefore={data['playBtnIconBefore']}")
        assert not data["playBtnHasStartText"], "Play button still contains 'Start' text!"
        assert "▶" in data["playBtnIconBefore"], f"Play button icon expected '▶', got '{data['playBtnIconBefore']}'"

        print(f"  Race Execution: finishedCards={data['finishedCardsCount']}, leaderboardVisible={data['leaderboardVisible']}, rows={data['leaderboardRowsCount']}")
        assert data["finishedCardsCount"] > 0, "No cards finished race"
        assert data["leaderboardVisible"], "Leaderboard did not render after race completion"
        assert data["leaderboardRowsCount"] > 0, "Leaderboard has no ranking rows"

        print(f"  Reset: cardsReset={data['cardsReset']}")
        assert data["cardsReset"], "Cards did not reset properly to step 0"

        print(f"  [PASS] {vp['name']}: All multi-algorithm showcase features verified on compare.html!")

    finally:
        if os.path.exists(harness_path):
            os.remove(harness_path)

# -------------------------------------------------------------
# Stage 4: Verify index.html Zero-Overflow Across Mobile and Desktop
# -------------------------------------------------------------
print("\n--- 4. Verifying index.html Minimal Hero Zero-Overflow in Chrome ---")
for vp in viewports:
    page_abs = os.path.abspath("index.html").replace(os.sep, "/")
    harness_html = f"""<!DOCTYPE html>
<html><body style="margin:0;padding:0;">
<iframe id="test-frame" src="file:///{page_abs}" style="width:{vp['width']}px;height:{vp['height']}px;border:none;"></iframe>
<div id="output"></div>
<script>
window.addEventListener('load', async () => {{
    await new Promise(r => setTimeout(r, 400));
    const iframe = document.getElementById('test-frame');
    const doc = iframe.contentDocument;
    const showcase = doc.getElementById('try-it');
    const overflow = doc.documentElement.scrollWidth > {vp['width']} + 2;
    document.getElementById('output').textContent = JSON.stringify({{ overflow, scrollWidth: doc.documentElement.scrollWidth }});
}});
</script></body></html>"""
    harness_path = f"tests/temp_index_test_{vp['width']}.html"
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
            "--virtual-time-budget=4000",
            "--dump-dom",
            f"file:///{os.path.abspath(harness_path).replace(os.sep, '/')}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        m = re.search(r'<div id="output"[^>]*>(.*?)</div>', res.stdout)
        assert m, "Failed to inspect index.html output"
        data = json.loads(m.group(1).replace("&quot;", '"'))
        assert not data["overflow"], f"Horizontal overflow detected on index.html at {vp['name']} (scrollWidth={data['scrollWidth']})"
        print(f"  [PASS] index.html {vp['name']} scrollWidth: {data['scrollWidth']} (0 overflow)")
    finally:
        if os.path.exists(harness_path):
            os.remove(harness_path)

print("\n" + "=" * 65)
print("ALL MULTI-ALGORITHM SHOWCASE VERIFICATIONS PASSED (100%)")
print("=" * 65)
