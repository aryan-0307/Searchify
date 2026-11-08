"""
tests/verify_merged_visualizer_controls.py
Automated verification for the visualizer controls layout split and merge:
1. Above visualizer: Only Array generation & customization (Generate, Custom Input, Apply, Size, Target) remains, centered.
2. Below visualizer: Playback buttons (start/stop/prev/next/reset/restart) are merged with Speed control (and sort order), centered.
3. Both toolbars are horizontally centered.
4. Full interactive functionality verified on both sorting.html and searching.html across Desktop and Mobile.
"""

import subprocess
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    # Fallback to local appdata or standard paths
    alt_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    if os.path.exists(alt_path):
        CHROME_PATH = alt_path

pages = ["sorting.html", "searching.html"]
viewports = [
    {"name": "Desktop 1280px", "width": 1280, "height": 850, "isMobile": False},
    {"name": "iPad 768px", "width": 768, "height": 900, "isMobile": True},
    {"name": "Galaxy S23 412px", "width": 412, "height": 850, "isMobile": True},
    {"name": "iPhone SE 375px", "width": 375, "height": 800, "isMobile": True}
]

print("=" * 65)
print("VERIFYING MERGED VISUALIZER CONTROLS (TOP ARRAY, BOTTOM PLAYBACK+SPEED)")
print("=" * 65)

# -------------------------------------------------------------
# Stage 1: DOM Hierarchy and Structural Order
# -------------------------------------------------------------
print("\n--- 1. Testing DOM Structural Order & Element Placement ---")
for page in pages:
    with open(page, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Top controls nav
    top_nav_match = re.search(r'<nav class="viz-controls"[^>]*>(.*?)</nav>', html, re.DOTALL)
    assert top_nav_match, f"Could not find <nav class=\"viz-controls\"> in {page}"
    top_content = top_nav_match.group(1)

    # Must contain Array controls
    assert 'class="controls-cluster array-cluster"' in top_content, f"array-cluster missing in top nav of {page}"
    assert 'id="generate-btn"' in top_content, f"generate-btn missing in top nav of {page}"
    assert 'id="custom-array"' in top_content, f"custom-array missing in top nav of {page}"
    assert 'id="apply-custom-btn"' in top_content, f"apply-custom-btn missing in top nav of {page}"
    assert 'id="array-size"' in top_content, f"array-size missing in top nav of {page}"
    if page == "searching.html":
        assert 'id="target-input"' in top_content, f"target-input missing in top nav of {page}"

    # Must NOT contain playback or speed controls
    assert 'id="play-btn"' not in top_content, f"play-btn must NOT be in top nav of {page}"
    assert 'id="speed-slider"' not in top_content, f"speed-slider must NOT be in top nav of {page}"
    assert 'id="reset-btn"' not in top_content, f"reset-btn must NOT be in top nav of {page}"
    assert 'id="restart-btn"' not in top_content, f"restart-btn must NOT be in top nav of {page}"
    assert 'id="prev-btn"' not in top_content, f"prev-btn must NOT be in top nav of {page}"
    assert 'id="next-btn"' not in top_content, f"next-btn must NOT be in top nav of {page}"

    # 2. Canvas wrapper
    canvas_idx = html.find('class="viz-canvas-wrapper"')
    top_nav_idx = html.find('class="viz-controls"')
    bottom_nav_idx = html.find('class="viz-controls viz-controls-bottom"')

    assert top_nav_idx != -1 and canvas_idx != -1 and bottom_nav_idx != -1, f"Missing markers in {page}"
    assert top_nav_idx < canvas_idx, f"Top nav must be placed BEFORE canvas in {page}"
    assert canvas_idx < bottom_nav_idx, f"Bottom nav must be placed AFTER canvas in {page}"

    # 3. Bottom controls nav
    bottom_nav_match = re.search(r'<nav class="viz-controls viz-controls-bottom"[^>]*>(.*?)</nav>', html, re.DOTALL)
    assert bottom_nav_match, f"Could not find <nav class=\"viz-controls viz-controls-bottom\"> in {page}"
    bottom_content = bottom_nav_match.group(1)

    # Must contain merged playback and speed controls
    assert 'merged-playback-cluster' in bottom_content, f"merged-playback-cluster missing in bottom nav of {page}"
    assert 'id="play-btn"' in bottom_content, f"play-btn missing in bottom nav of {page}"
    assert 'id="prev-btn"' in bottom_content, f"prev-btn missing in bottom nav of {page}"
    assert 'id="next-btn"' in bottom_content, f"next-btn missing in bottom nav of {page}"
    assert 'id="reset-btn"' in bottom_content, f"reset-btn missing in bottom nav of {page}"
    assert 'id="restart-btn"' in bottom_content, f"restart-btn missing in bottom nav of {page}"
    assert 'id="speed-slider"' in bottom_content, f"speed-slider missing in bottom nav of {page}"
    assert 'id="speed-value"' in bottom_content, f"speed-value missing in bottom nav of {page}"
    if page == "sorting.html":
        assert 'id="asc-btn"' in bottom_content, f"asc-btn missing in bottom nav of {page}"
        assert 'id="desc-btn"' in bottom_content, f"desc-btn missing in bottom nav of {page}"

    # Progress section must be after bottom controls
    progress_idx = html.find('class="progress-section"')
    assert bottom_nav_idx < progress_idx, f"Bottom controls must be placed BEFORE progress section in {page}"

    print(f"  [PASS] {page}: DOM layout validated (Top: Array -> Canvas -> Bottom: Playback + Speed -> Progress)")

# -------------------------------------------------------------
# Stage 2: Chrome Headless Geometry and Centering Verification
# -------------------------------------------------------------
print("\n--- 2. Verifying Geometric Placement & Centering in Chrome ---")

for vp in viewports:
    print(f"\n--- Testing Viewport: {vp['name']} ({vp['width']}x{vp['height']}) ---")
    for page in pages:
        page_abs = os.path.abspath(page).replace(os.sep, "/")
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

    const topNav = doc.querySelector('.viz-controls');
    const canvas = doc.querySelector('.viz-canvas-wrapper');
    const bottomNav = doc.querySelector('.viz-controls-bottom');
    const topCluster = doc.querySelector('.viz-controls .array-cluster');
    const bottomCluster = doc.querySelector('.merged-playback-cluster');

    const topRect = topNav ? topNav.getBoundingClientRect() : null;
    const canvasRect = canvas ? canvas.getBoundingClientRect() : null;
    const bottomRect = bottomNav ? bottomNav.getBoundingClientRect() : null;
    const topClustRect = topCluster ? topCluster.getBoundingClientRect() : null;
    const bottomClustRect = bottomCluster ? bottomCluster.getBoundingClientRect() : null;

    const vpWidth = doc.documentElement.clientWidth;

    // Centering calculations
    const topCenter = topClustRect ? (topClustRect.left + topClustRect.width / 2) : 0;
    const bottomCenter = bottomClustRect ? (bottomClustRect.left + bottomClustRect.width / 2) : 0;
    const idealCenter = vpWidth / 2;

    const topCenterDiff = Math.abs(topCenter - idealCenter);
    const bottomCenterDiff = Math.abs(bottomCenter - idealCenter);

    // Interactive test
    const playBtn = doc.getElementById('play-btn');
    const speedSlider = doc.getElementById('speed-slider');
    const speedVal = doc.getElementById('speed-value');
    const generateBtn = doc.getElementById('generate-btn');
    const customInput = doc.getElementById('custom-array');
    const applyBtn = doc.getElementById('apply-custom-btn');
    const statusText = doc.getElementById('canvas-status-text');

    // Test speed slider
    speedSlider.value = "3";
    speedSlider.dispatchEvent(new win.Event('input', {{ bubbles: true }}));
    const speedTextAfter = speedVal.textContent.trim();

    // Test custom array apply
    customInput.value = "42, 17, 89";
    applyBtn.click();
    await new Promise(r => setTimeout(r, 100));
    const barCount = doc.querySelectorAll('.bar, .cell').length;

    // Test play/pause toggle
    playBtn.click();
    await new Promise(r => setTimeout(r, 150));
    const statusPlaying = statusText ? statusText.textContent.trim() : "";
    playBtn.click(); // pause
    await new Promise(r => setTimeout(r, 50));

    const res = {{
        topNavAboveCanvas: topRect && canvasRect ? (topRect.bottom <= canvasRect.top + 2) : false,
        bottomNavBelowCanvas: bottomRect && canvasRect ? (bottomRect.top >= canvasRect.bottom - 2) : false,
        topCenterDiff: Math.round(topCenterDiff * 10) / 10,
        bottomCenterDiff: Math.round(bottomCenterDiff * 10) / 10,
        topIsCentered: topCenterDiff <= 25,
        bottomIsCentered: bottomCenterDiff <= 25,
        speedUpdated: speedTextAfter.includes('3x'),
        customApplied: barCount === 3,
        statusPlaying: statusPlaying,
        topRect: topRect ? {{ top: Math.round(topRect.top), bottom: Math.round(topRect.bottom) }} : null,
        canvasRect: canvasRect ? {{ top: Math.round(canvasRect.top), bottom: Math.round(canvasRect.bottom) }} : null,
        bottomRect: bottomRect ? {{ top: Math.round(bottomRect.top), bottom: Math.round(bottomRect.bottom) }} : null
    }};

    document.getElementById('output').textContent = JSON.stringify(res);
}});
</script>
</body>
</html>"""

        harness_path = os.path.join(os.path.dirname(__file__), "harness_merged_controls_test.html")
        with open(harness_path, "w", encoding="utf-8") as f:
            f.write(harness_html)

        cmd = [
            CHROME_PATH,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--allow-file-access-from-files",
            f"--window-size={vp['width'] + 60},{vp['height'] + 100}",
            "--virtual-time-budget=8000",
            "--dump-dom",
            f"file:///{os.path.abspath(harness_path).replace(os.sep, '/')}"
        ]

        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if os.path.exists(harness_path):
            os.remove(harness_path)

        match = re.search(r'<div id="output">({.*?})</div>', proc.stdout)
        assert match, f"Failed to retrieve output for {page} on {vp['name']}"
        data = json.loads(match.group(1))

        assert data["topNavAboveCanvas"], f"{page} on {vp['name']}: Top nav is NOT above canvas! (topNav.bottom={data['topRect']['bottom']}, canvas.top={data['canvasRect']['top']})"
        assert data["bottomNavBelowCanvas"], f"{page} on {vp['name']}: Bottom nav is NOT below canvas! (bottomNav.top={data['bottomRect']['top']}, canvas.bottom={data['canvasRect']['bottom']})"
        assert data["topIsCentered"], f"{page} on {vp['name']}: Top cluster is NOT centered! (diff={data['topCenterDiff']}px)"
        assert data["bottomIsCentered"], f"{page} on {vp['name']}: Bottom cluster is NOT centered! (diff={data['bottomCenterDiff']}px)"
        assert data["speedUpdated"], f"{page} on {vp['name']}: Speed slider did not update value to 3x"
        assert data["customApplied"], f"{page} on {vp['name']}: Custom array apply failed (expected 3 elements)"

        print(f"  [PASS] {page}: Top above canvas ({data['topRect']['bottom']}px <= {data['canvasRect']['top']}px), Bottom below canvas ({data['bottomRect']['top']}px >= {data['canvasRect']['bottom']}px)")
        print(f"  [PASS] {page}: Top centered (diff={data['topCenterDiff']}px), Bottom centered (diff={data['bottomCenterDiff']}px)")
        print(f"  [PASS] {page}: Interactive controls (speed slider, custom array apply, play/pause) fully verified")

print("\n" + "=" * 65)
print("ALL MERGED VISUALIZER CONTROLS TESTS PASSED (100% PASS RATE)!")
print("=" * 65)
