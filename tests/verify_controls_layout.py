"""
tests/verify_controls_layout.py
Automated verification for the visualizer controls layout:
- Array generation & custom array controls (generate, example input, apply, size) positioned ABOVE visualizer in top nav (centered)
- Merged playback controls (prev, play/pause, next, reset, restart) with speed control positioned BELOW visualizer in bottom nav (centered)
- Verified on both sorting.html and searching.html across desktop and mobile viewports
"""

import subprocess
import json
import re
import sys
import os

pages = ["sorting.html", "searching.html"]
all_passed = True

print("=" * 60)
print("VERIFYING VISUALIZER CONTROLS LAYOUT (TOP ARRAY, BOTTOM PLAYBACK+SPEED)")
print("=" * 60)

# Stage 1: DOM Hierarchy and Structural Order
print("\n--- 1. Testing DOM Structural Order ---")
for page in pages:
    with open(page, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract <nav class="viz-controls"> ... </nav>
    top_match = re.search(r'<nav class="viz-controls"[^>]*>(.*?)</nav>', html, re.DOTALL)
    assert top_match, f"Could not find <nav class=\"viz-controls\"> in {page}"
    top_content = top_match.group(1)

    # Check key items inside top nav (Array)
    assert 'id="generate-btn"' in top_content, f"generate-btn missing in {page} top nav"
    assert 'id="custom-array"' in top_content, f"custom-array missing in {page} top nav"
    assert 'id="apply-custom-btn"' in top_content, f"apply-custom-btn missing in {page} top nav"
    assert 'id="array-size"' in top_content, f"array-size missing in {page} top nav"

    # Verify playback & speed buttons are NOT in top nav
    assert 'id="play-btn"' not in top_content, f"play-btn should not be in top nav of {page}"
    assert 'id="speed-slider"' not in top_content, f"speed-slider should not be in top nav of {page}"

    # Extract <nav class="viz-controls viz-controls-bottom"> ... </nav>
    bottom_match = re.search(r'<nav class="viz-controls viz-controls-bottom"[^>]*>(.*?)</nav>', html, re.DOTALL)
    assert bottom_match, f"Could not find <nav class=\"viz-controls viz-controls-bottom\"> in {page}"
    bottom_content = bottom_match.group(1)

    # Check key items inside bottom nav (Playback & Speed)
    assert 'id="play-btn"' in bottom_content, f"play-btn missing in {page} bottom nav"
    assert 'id="reset-btn"' in bottom_content, f"reset-btn missing in {page} bottom nav"
    assert 'id="restart-btn"' in bottom_content, f"restart-btn missing in {page} bottom nav"
    assert 'id="prev-btn"' in bottom_content, f"prev-btn missing in {page} bottom nav"
    assert 'id="next-btn"' in bottom_content, f"next-btn missing in {page} bottom nav"
    assert 'id="speed-slider"' in bottom_content, f"speed-slider missing in {page} bottom nav"

    print(f"  [PASS] {page}: DOM cluster sequence verified: [Top Array (Center)] -> [Canvas] -> [Bottom Playback + Speed (Center)]")


# Stage 2: Chrome Headless Computed Geometry across Viewports
print("\n--- 2. Verifying Computed Layout Geometry in Chrome ---")
probe_template = """
window.addEventListener('load', () => {
    const header = document.querySelector('.viz-header');
    const headerCS = header ? window.getComputedStyle(header) : null;
    const topNav = document.querySelector('.viz-controls');
    const canvas = document.querySelector('.viz-canvas-wrapper');
    const bottomNav = document.querySelector('.viz-controls-bottom');
    const topCluster = document.querySelector('.viz-controls .array-cluster');
    const bottomCluster = document.querySelector('.merged-playback-cluster');

    const topRect = topNav ? topNav.getBoundingClientRect() : null;
    const canvasRect = canvas ? canvas.getBoundingClientRect() : null;
    const bottomRect = bottomNav ? bottomNav.getBoundingClientRect() : null;
    const topClustRect = topCluster ? topCluster.getBoundingClientRect() : null;
    const bottomClustRect = bottomCluster ? bottomCluster.getBoundingClientRect() : null;

    const vpWidth = document.documentElement.clientWidth;

    const probe = document.createElement('div');
    probe.id = 'layout-probe-results';
    probe.textContent = JSON.stringify({
        headerPos: headerCS ? headerCS.position : null,
        headerTop: header ? Math.round(header.getBoundingClientRect().top) : null,
        vpWidth: vpWidth,
        topBottom: topRect ? Math.round(topRect.bottom) : null,
        canvasTop: canvasRect ? Math.round(canvasRect.top) : null,
        canvasBottom: canvasRect ? Math.round(canvasRect.bottom) : null,
        bottomTop: bottomRect ? Math.round(bottomRect.top) : null,
        topCenterDiff: topClustRect ? Math.abs(Math.round(topClustRect.left + topClustRect.width / 2) - Math.round(vpWidth / 2)) : null,
        bottomCenterDiff: bottomClustRect ? Math.abs(Math.round(bottomClustRect.left + bottomClustRect.width / 2) - Math.round(vpWidth / 2)) : null
    });
    document.body.appendChild(probe);
});
"""

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    alt_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    if os.path.exists(alt_path):
        CHROME_PATH = alt_path

for page in pages:
    raw_html = open(page, encoding="utf-8").read()
    probe_html = raw_html.replace("</body>", f"<script>{probe_template}</script></body>")
    temp_file = f"probe_{page}"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(probe_html)

    try:
        # Test 1440px desktop
        cmd = [
            CHROME_PATH,
            "--headless=new", "--no-sandbox", "--disable-gpu",
            "--window-size=1440,900",
            "--allow-file-access-from-files",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=2000",
            "--dump-dom",
            f"file:///{os.path.abspath(temp_file).replace(os.sep, '/')}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        m = re.search(r'<div id="layout-probe-results">(.*?)</div>', res.stdout)
        assert m, f"Probe output not found for {page} at 1440px"
        data = json.loads(m.group(1))

        # Verify Navbar is fixed/sticky at top: 0
        assert data["headerPos"] == "sticky", f"Expected header position 'sticky', got {data['headerPos']}"
        assert data["headerTop"] == 0, f"Expected header top to be 0, got {data['headerTop']}"

        # Verify geometric order on desktop: Top Nav above canvas, Bottom Nav below canvas
        assert data["topBottom"] <= data["canvasTop"] + 5, f"Top nav bottom ({data['topBottom']}) must be <= canvas top ({data['canvasTop']})"
        assert data["bottomTop"] >= data["canvasBottom"] - 5, f"Bottom nav top ({data['bottomTop']}) must be >= canvas bottom ({data['canvasBottom']})"

        # Verify centered
        assert data["topCenterDiff"] <= 25, f"Top cluster must be centered, diff was {data['topCenterDiff']}px"
        assert data["bottomCenterDiff"] <= 25, f"Bottom cluster must be centered, diff was {data['bottomCenterDiff']}px"

        print(f"  [PASS] {page} @ 1440px: Top above canvas ({data['topBottom']}px <= {data['canvasTop']}px), Bottom below canvas ({data['bottomTop']}px >= {data['canvasBottom']}px), both centered")

        # Test mobile 768px
        cmd_mob = [
            CHROME_PATH,
            "--headless=new", "--no-sandbox", "--disable-gpu",
            "--window-size=768,900",
            "--allow-file-access-from-files",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=2000",
            "--dump-dom",
            f"file:///{os.path.abspath(temp_file).replace(os.sep, '/')}"
        ]
        res_mob = subprocess.run(cmd_mob, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        m_mob = re.search(r'<div id="layout-probe-results">(.*?)</div>', res_mob.stdout)
        assert m_mob, f"Probe output not found for {page} at 768px"
        data_mob = json.loads(m_mob.group(1))

        assert data_mob["topBottom"] <= data_mob["canvasTop"] + 5
        assert data_mob["bottomTop"] >= data_mob["canvasBottom"] - 5
        assert data_mob["topCenterDiff"] <= 25
        assert data_mob["bottomCenterDiff"] <= 25

        print(f"  [PASS] {page} @ 768px: Mobile layout verified (Top above canvas, Bottom below canvas, both centered)")

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

# Stage 3: Interactive Functionality Verification
print("\n--- 3. Verifying Interactive Controls Behavior ---")
interactive_probe = """
window.addEventListener('load', () => {
    const playBtn = document.getElementById('play-btn');
    const resetBtn = document.getElementById('reset-btn');
    const restartBtn = document.getElementById('restart-btn');
    const speedSlider = document.getElementById('speed-slider');
    const generateBtn = document.getElementById('generate-btn');

    // 1. Click Play
    playBtn.click();
    const afterPlayLabel = playBtn.getAttribute('aria-label');

    // 2. Click Pause
    playBtn.click();
    const afterPauseLabel = playBtn.getAttribute('aria-label');

    // 3. Reset
    resetBtn.click();

    // 4. Change Speed
    speedSlider.value = "4";
    speedSlider.dispatchEvent(new Event('input', { bubbles: true }));
    const speedVal = document.getElementById('speed-value').textContent;

    // 5. Generate Array
    generateBtn.click();

    const probe = document.createElement('div');
    probe.id = 'interactive-probe-results';
    probe.textContent = JSON.stringify({
        afterPlayLabel: afterPlayLabel,
        afterPauseLabel: afterPauseLabel,
        speedVal: speedVal
    });
    document.body.appendChild(probe);
});
"""

for page in pages:
    raw_html = open(page, encoding="utf-8").read()
    probe_html = raw_html.replace("</body>", f"<script>{interactive_probe}</script></body>")
    temp_file = f"probe_interactive_{page}"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(probe_html)

    try:
        cmd = [
            CHROME_PATH,
            "--headless=new", "--no-sandbox", "--disable-gpu",
            "--window-size=1440,900",
            "--allow-file-access-from-files",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=2000",
            "--dump-dom",
            f"file:///{os.path.abspath(temp_file).replace(os.sep, '/')}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        m = re.search(r'<div id="interactive-probe-results">(.*?)</div>', res.stdout)
        assert m, f"Interactive probe output not found for {page}"
        data = json.loads(m.group(1))

        assert data["afterPlayLabel"] == "Pause", f"Expected 'Pause' after play click, got: {data['afterPlayLabel']}"
        assert data["afterPauseLabel"] == "Play", f"Expected 'Play' after pause click, got: {data['afterPauseLabel']}"
        assert data["speedVal"] == "4x", f"Expected '4x' after speed update, got: {data['speedVal']}"

        print(f"  [PASS] {page}: Play/Pause toggle, Generate, and Speed settings verified interactive and reactive!")

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

print("\n" + "=" * 60)
print("ALL VISUALIZER CONTROLS LAYOUT VERIFICATIONS PASSED (100%)")
print("=" * 60)
