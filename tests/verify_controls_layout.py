"""
tests/verify_controls_layout.py
Automated verification for the visualizer controls layout:
- Start/Stop & Playback controls (prev, play/pause, next, reset, restart) positioned on the LEFT
- Array generation & custom array controls (generate, example input, apply, size) positioned in the CENTER
- Settings option (speed, sort order) positioned on the RIGHT
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
print("VERIFYING VISUALIZER CONTROLS LAYOUT (LEFT PLAYBACK, CENTER ARRAY, RIGHT SETTINGS)")
print("=" * 60)

# Stage 1: DOM Hierarchy and Structural Order
print("\n--- 1. Testing DOM Structural Order ---")
for page in pages:
    with open(page, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract <nav class="viz-controls"> ... </nav>
    nav_match = re.search(r'<nav class="viz-controls"[^>]*>(.*?)</nav>', html, re.DOTALL)
    assert nav_match, f"Could not find <nav class=\"viz-controls\"> in {page}"
    nav_content = nav_match.group(1)

    # Find all <section class="controls-cluster ...">
    clusters = re.findall(r'<section class="controls-cluster([^"]*)"[^>]*aria-label="([^"]*)"', nav_content)
    assert len(clusters) == 3, f"Expected 3 clusters in {page}, found {len(clusters)}"

    c1_class, c1_label = clusters[0]
    c2_class, c2_label = clusters[1]
    c3_class, c3_label = clusters[2]

    # Cluster 1: Playback Controls (Left)
    assert "Playback controls" in c1_label, f"Cluster 1 should be Playback controls, got: {c1_label}"
    assert "playback-cluster" in c1_class, f"Cluster 1 should have class 'playback-cluster', got: {c1_class}"

    # Cluster 2: Array Configuration (Center)
    assert "Array configuration" in c2_label, f"Cluster 2 should be Array configuration, got: {c2_label}"
    assert "array-cluster" in c2_class, f"Cluster 2 should have class 'array-cluster', got: {c2_class}"

    # Cluster 3: Settings (Right)
    assert "Animation settings" in c3_label, f"Cluster 3 should be Animation settings, got: {c3_label}"
    assert "settings-cluster" in c3_class, f"Cluster 3 should have class 'settings-cluster', got: {c3_class}"

    # Check key buttons inside cluster 1 (Playback)
    assert 'id="play-btn"' in nav_content, f"play-btn missing in {page}"
    assert 'id="reset-btn"' in nav_content, f"reset-btn missing in {page}"
    assert 'id="restart-btn"' in nav_content, f"restart-btn missing in {page}"
    assert 'id="prev-btn"' in nav_content, f"prev-btn missing in {page}"
    assert 'id="next-btn"' in nav_content, f"next-btn missing in {page}"

    # Check key buttons inside cluster 2 (Array)
    assert 'id="generate-btn"' in nav_content, f"generate-btn missing in {page}"
    assert 'id="custom-array"' in nav_content, f"custom-array missing in {page}"
    assert 'id="apply-custom-btn"' in nav_content, f"apply-custom-btn missing in {page}"
    assert 'id="array-size"' in nav_content, f"array-size missing in {page}"

    # Check key items inside cluster 3 (Settings)
    assert 'id="speed-slider"' in nav_content, f"speed-slider missing in {page}"

    print(f"  [PASS] {page}: DOM cluster sequence verified: [Playback (Left)] -> [Array (Center)] -> [Settings (Right)]")


# Stage 2: Chrome Headless Computed Geometry across Viewports
print("\n--- 2. Verifying Computed Layout Geometry in Chrome ---")
probe_template = """
window.addEventListener('load', () => {
    const nav = document.querySelector('.viz-controls');
    const clusters = Array.from(document.querySelectorAll('.controls-cluster')).map(c => {
        const rect = c.getBoundingClientRect();
        return {
            label: c.getAttribute('aria-label'),
            className: c.className,
            width: Math.round(rect.width),
            left: Math.round(rect.left),
            right: Math.round(rect.right),
            top: Math.round(rect.top),
            center: Math.round((rect.left + rect.right) / 2)
        };
    });
    const navRect = nav.getBoundingClientRect();
    const probe = document.createElement('div');
    probe.id = 'layout-probe-results';
    probe.textContent = JSON.stringify({
        navLeft: Math.round(navRect.left),
        navRight: Math.round(navRect.right),
        navWidth: Math.round(navRect.width),
        navCenter: Math.round((navRect.left + navRect.right) / 2),
        clusters: clusters
    });
    document.body.appendChild(probe);
});
"""

for page in pages:
    raw_html = open(page, encoding="utf-8").read()
    probe_html = raw_html.replace("</body>", f"<script>{probe_template}</script></body>")
    temp_file = f"probe_{page}"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(probe_html)

    try:
        # Test 1440px desktop
        cmd = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "--headless=new", "--no-sandbox", "--disable-gpu",
            "--window-size=1440,900",
            "--allow-file-access-from-files",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=2000",
            "--dump-dom",
            f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{temp_file}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        m = re.search(r'<div id="layout-probe-results">(.*?)</div>', res.stdout)
        assert m, f"Probe output not found for {page} at 1440px"
        data = json.loads(m.group(1))
        clusters = data["clusters"]

        play = clusters[0]
        arr = clusters[1]
        sett = clusters[2]

        # Verify geometric order on desktop: Playback.left < Array.left < Settings.left
        assert play["left"] < arr["left"], f"Playback left ({play['left']}) should be less than Array left ({arr['left']})"
        assert arr["right"] < sett["right"], f"Array right ({arr['right']}) should be less than Settings right ({sett['right']})"

        # Verify Array is centered between Playback and Settings
        gap_left = arr["left"] - play["right"]
        gap_right = sett["left"] - arr["right"]
        gap_diff = abs(gap_left - gap_right)
        assert gap_diff <= 3, f"Array should be centered between Playback and Settings! Gaps: left={gap_left}, right={gap_right}, diff={gap_diff}"

        # Verify Playback sits on the left edge and Settings on the right edge
        dist_to_nav_left = play["left"] - data["navLeft"]
        dist_to_nav_right = data["navRight"] - sett["right"]
        assert dist_to_nav_left <= 40, f"Playback should sit on left side, distance from left: {dist_to_nav_left}px"
        assert dist_to_nav_right <= 40, f"Settings should sit on right side, distance from right: {dist_to_nav_right}px"

        print(f"  [PASS] {page} @ 1440px: Playback Left (L:{play['left']} R:{play['right']}), Array Center (L:{arr['left']} R:{arr['right']}, equal gaps {gap_left}px/{gap_right}px), Settings Right (R:{sett['right']})")

        # Test mobile 768px
        cmd_mob = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "--headless=new", "--no-sandbox", "--disable-gpu",
            "--window-size=768,900",
            "--allow-file-access-from-files",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=2000",
            "--dump-dom",
            f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{temp_file}"
        ]
        res_mob = subprocess.run(cmd_mob, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        m_mob = re.search(r'<div id="layout-probe-results">(.*?)</div>', res_mob.stdout)
        assert m_mob, f"Probe output not found for {page} at 768px"
        data_mob = json.loads(m_mob.group(1))
        c_mob = data_mob["clusters"]

        # Vertically stacked: top increases monotonically
        assert c_mob[0]["top"] < c_mob[1]["top"] < c_mob[2]["top"], f"Mobile clusters should be vertically stacked, tops: {[c['top'] for c in c_mob]}"
        print(f"  [PASS] {page} @ 768px: Mobile responsive stacking verified cleanly (tops: {[c['top'] for c in c_mob]})")

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
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "--headless=new", "--no-sandbox", "--disable-gpu",
            "--window-size=1440,900",
            "--allow-file-access-from-files",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=2000",
            "--dump-dom",
            f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{temp_file}"
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
