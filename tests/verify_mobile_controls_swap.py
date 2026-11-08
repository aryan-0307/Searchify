"""
tests/verify_mobile_controls_swap.py
Automated verification for visualizer controls placement across all viewports:
1. Across all viewports (320px to 1280px):
   - .array-cluster (Generate, Apply, Size) is strictly ABOVE the visualizer canvas.
   - .playback-cluster (merged Playback & Speed) is strictly BELOW the visualizer canvas.
   - Both clusters are horizontally centered.
2. Verified across 11 device viewports (320px to 1280px) on sorting.html and searching.html.
"""

import subprocess
import json
import re
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

viewports = [
    (320, 568, "iPhone SE 1st gen (320px)", True),
    (360, 740, "Galaxy S8/S9/S10 (360px)", True),
    (375, 667, "iPhone SE/8 (375px)", True),
    (390, 844, "iPhone 13/14/15 (390px)", True),
    (412, 915, "Galaxy S23/Pixel 7 (412px)", True),
    (430, 932, "iPhone Pro Max (430px)", True),
    (768, 1024, "iPad Portrait (768px)", True),
    (860, 1000, "Mobile Upper Boundary (860px)", True),
    (861, 1000, "Desktop Lower Boundary (861px)", False),
    (1024, 768, "Desktop 1024px", False),
    (1280, 800, "Desktop 1280px", False),
]

pages = ["sorting.html", "searching.html"]

all_passed = True
print("=" * 70)
print("VERIFYING CONTROLS POSITIONING & CENTERING ACROSS ALL VIEWPORTS")
print("=" * 70)

harness_template = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0;">
<iframe id="frame" src="../{page}" style="width: {w}px; height: {h}px; border:0; display:block;"></iframe>
<div id="results"></div>
<script>
window.addEventListener('load', async () => {{
    await new Promise(r => setTimeout(r, 400));
    const frame = document.getElementById('frame');
    const win = frame.contentWindow;
    const doc = frame.contentDocument;

    const playbackCluster = doc.querySelector('.playback-cluster');
    const arrayCluster = doc.querySelector('.array-cluster');
    const canvas = doc.querySelector('.viz-canvas-wrapper');

    const issues = [];
    const checks = [];

    if (!playbackCluster || !arrayCluster || !canvas) {{
        issues.push('Could not find .playback-cluster, .array-cluster, or .viz-canvas-wrapper');
    }} else {{
        const playRect = playbackCluster.getBoundingClientRect();
        const arrRect = arrayCluster.getBoundingClientRect();
        const canvasRect = canvas.getBoundingClientRect();

        const vpWidth = doc.documentElement.clientWidth;
        const scrollWidth = doc.documentElement.scrollWidth;

        // 1. Array cluster is ABOVE canvas
        if (arrRect.bottom > canvasRect.top + 5) {{
            issues.push(`Array cluster bottom (${{arrRect.bottom.toFixed(1)}}) is NOT above canvas top (${{canvasRect.top.toFixed(1)}})`);
        }} else {{
            checks.push(`Array cluster (bottom=${{arrRect.bottom.toFixed(1)}}) is strictly above canvas (top=${{canvasRect.top.toFixed(1)}})`);
        }}

        // 2. Playback cluster is BELOW canvas
        if (playRect.top < canvasRect.bottom - 5) {{
            issues.push(`Playback cluster top (${{playRect.top.toFixed(1)}}) is NOT below canvas bottom (${{canvasRect.bottom.toFixed(1)}})`);
        }} else {{
            checks.push(`Playback cluster (top=${{playRect.top.toFixed(1)}}) is strictly below canvas (bottom=${{canvasRect.bottom.toFixed(1)}})`);
        }}

        // 3. Array cluster is centered
        const arrCenter = arrRect.left + arrRect.width / 2;
        const arrCenterDiff = Math.abs(arrCenter - vpWidth / 2);
        if (arrCenterDiff > 25) {{
            issues.push(`Array cluster is off-center by ${{arrCenterDiff.toFixed(1)}}px (center=${{arrCenter.toFixed(1)}}, vpCenter=${{(vpWidth/2).toFixed(1)}})`);
        }} else {{
            checks.push(`Array cluster is centered (diff=${{arrCenterDiff.toFixed(1)}}px)`);
        }}

        // 4. Playback cluster is centered
        const playCenter = playRect.left + playRect.width / 2;
        const playCenterDiff = Math.abs(playCenter - vpWidth / 2);
        if (playCenterDiff > 25) {{
            issues.push(`Playback cluster is off-center by ${{playCenterDiff.toFixed(1)}}px (center=${{playCenter.toFixed(1)}}, vpCenter=${{(vpWidth/2).toFixed(1)}})`);
        }} else {{
            checks.push(`Playback cluster is centered (diff=${{playCenterDiff.toFixed(1)}}px)`);
        }}

        // 5. Zero horizontal overflow
        if (scrollWidth > vpWidth + 2) {{
            issues.push(`Horizontal overflow detected: scrollWidth=${{scrollWidth}}, vpWidth=${{vpWidth}}`);
        }} else {{
            checks.push(`Zero horizontal overflow (scrollWidth=${{scrollWidth}} <= vpWidth=${{vpWidth}})`);
        }}
    }}

    document.getElementById('results').textContent = JSON.stringify({{
        passed: issues.length === 0,
        issues: issues,
        checks: checks
    }});
}});
</script>
</body>
</html>"""

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    alt_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    if os.path.exists(alt_path):
        CHROME_PATH = alt_path

harness_file = os.path.join(os.path.dirname(__file__), "harness_controls_swap_test.html")

total_tests = 0
passed_tests = 0

for page in pages:
    print(f"\n--- Testing {page} across viewports ---")
    for w, h, name, is_mob in viewports:
        total_tests += 1
        with open(harness_file, "w", encoding="utf-8") as f:
            f.write(harness_template.format(page=page, w=w, h=h))

        cmd = [
            CHROME_PATH,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--allow-file-access-from-files",
            f"--window-size={w + 40},{h + 80}",
            "--virtual-time-budget=4000",
            "--dump-dom",
            f"file:///{os.path.abspath(harness_file).replace(os.sep, '/')}"
        ]

        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        m = re.search(r'<div id="results">(\{.*?\})</div>', res.stdout, re.DOTALL)

        if not m:
            print(f"  [FAIL] {name} ({page}): Could not extract test results JSON")
            all_passed = False
            continue

        data = json.loads(m.group(1))
        if data["passed"]:
            passed_tests += 1
            print(f"  [PASS] {name}: Array above canvas, Playback below canvas, both centered, 0 overflow")
        else:
            all_passed = False
            print(f"  [FAIL] {name}:")
            for iss in data["issues"]:
                print(f"         - {iss}")

if os.path.exists(harness_file):
    os.remove(harness_file)

print("\n" + "=" * 70)
if all_passed:
    print(f"ALL CONTROLS POSITIONING TESTS PASSED ({passed_tests}/{total_tests})")
    print("Array cluster above visualizer, Merged Playback cluster below visualizer, both centered!")
    print("=" * 70)
else:
    print(f"SOME TESTS FAILED ({passed_tests}/{total_tests})")
    print("=" * 70)
    sys.exit(1)
