"""
tests/verify_mobile_visualizer_clearance.py
Automated verification for mobile visualizer layout:
1. .color-legend and #canvas-status-pill never overlap or occupy each other's space.
2. #canvas-status-pill floats in its own clean, empty area.
3. The highest element of the array (tallest bar + bar-label in sorting; cells in searching)
   is strictly and comfortably lower than both the status pill and the color legend.
4. Verified across mobile viewports (320px to 768px) and desktop (1280px).
"""

import subprocess
import json
import re
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

viewports = [
    (320, 568, "iPhone SE 1st gen (320px)"),
    (360, 740, "Galaxy S8/S9/S10 (360px)"),
    (375, 667, "iPhone SE/8 (375px)"),
    (390, 844, "iPhone 13/14/15 (390px)"),
    (412, 915, "Galaxy S23/Pixel 7 (412px)"),
    (430, 932, "iPhone Pro Max (430px)"),
    (768, 1024, "iPad Portrait (768px)"),
    (1280, 800, "Desktop (1280px)")
]

pages = ["sorting.html", "searching.html"]

all_passed = True
print("=" * 65)
print("VERIFYING MOBILE VISUALIZER CLEARANCE & NON-OVERLAPPING STATUS")
print("=" * 65)

harness_template = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0;">
<iframe id="frame" src="../{page}" style="width: {w}px; height: {h}px; border:0; display:block;"></iframe>
<div id="results"></div>
<script>
window.addEventListener('load', async () => {{
    await new Promise(r => setTimeout(r, 1000));
    const frame = document.getElementById('frame');
    const doc = frame.contentDocument;
    const win = frame.contentWindow;

    const area = doc.getElementById('visualization-area');
    const areaRect = area.getBoundingClientRect();
    const legend = doc.querySelector('.color-legend');
    const pill = doc.getElementById('canvas-status-pill');

    const issues = [];
    const checks = [];

    if (!legend) {{
        issues.push("Missing .color-legend");
    }}
    if (!pill) {{
        issues.push("Missing #canvas-status-pill");
    }}

    if (legend && pill) {{
        const legR = legend.getBoundingClientRect();
        const pillR = pill.getBoundingClientRect();

        // 1. Check mutual exclusion / non-overlap between legend and pill
        const xOverlap = Math.max(legR.left, pillR.left) < Math.min(legR.right, pillR.right);
        const yOverlap = Math.max(legR.top, pillR.top) < Math.min(legR.bottom, pillR.bottom);
        const boxesOverlap = xOverlap && yOverlap;

        if (boxesOverlap) {{
            issues.push(`Collision detected: .color-legend and #canvas-status-pill overlap! Leg bottom=${{legR.bottom}}, Pill top=${{pillR.top}}, Leg right=${{legR.right}}, Pill left=${{pillR.left}}`);
        }} else {{
            checks.push("Legend and Status Pill are completely non-overlapping");
        }}

        const isMobile = {w} <= 768;

        if (isMobile) {{
            // On mobile, legend should be on top and pill below it
            if (pillR.top < legR.bottom - 1) {{
                issues.push(`On mobile, status pill top (${{pillR.top}}) should be below legend bottom (${{legR.bottom}})`);
            }} else {{
                const gap = pillR.top - legR.bottom;
                checks.push(`Status pill is positioned cleanly below legend with gap: ${{gap.toFixed(1)}}px`);
            }}
        }}

        // 2. Check that the highest element of the array is strictly lower than both legend and status pill
        const isSorting = '{page}' === 'sorting.html';
        let highestTop = 999999;
        let highestElDescription = "none";

        if (isSorting) {{
            const bars = Array.from(doc.querySelectorAll('.bar'));
            if (bars.length === 0) {{
                issues.push("No bars found in sorting visualizer");
            }} else {{
                bars.forEach((bar, idx) => {{
                    const barR = bar.getBoundingClientRect();
                    const label = bar.querySelector('.bar-label');
                    const labelR = label ? label.getBoundingClientRect() : null;
                    const effectiveTop = labelR ? labelR.top : barR.top;

                    if (effectiveTop < highestTop) {{
                        highestTop = effectiveTop;
                        highestElDescription = label ? `bar-label for bar ${{idx}} (val ${{label.textContent}})` : `bar ${{idx}}`;
                    }}
                }});
            }}
        }} else {{
            // Searching visualizer
            const cells = Array.from(doc.querySelectorAll('.cell'));
            const targetDisplay = doc.querySelector('.search-target-display');
            if (targetDisplay) {{
                const tdR = targetDisplay.getBoundingClientRect();
                if (tdR.top < highestTop) {{
                    highestTop = tdR.top;
                    highestElDescription = "search-target-display";
                }}
            }}
            cells.forEach((cell, idx) => {{
                const cellR = cell.getBoundingClientRect();
                if (cellR.top < highestTop) {{
                    highestTop = cellR.top;
                    highestElDescription = `cell ${{idx}}`;
                }}
            }});
        }}

        if (highestTop < 999999) {{
            const clearanceBelowPill = highestTop - pillR.bottom;
            const clearanceBelowLegend = highestTop - legR.bottom;

            if (clearanceBelowPill <= 0) {{
                issues.push(`Array highest element (${{highestElDescription}} at top=${{highestTop.toFixed(1)}}) collides with or is higher than status pill (bottom=${{pillR.bottom.toFixed(1)}})`);
            }} else {{
                checks.push(`Highest array element (${{highestElDescription}}) is strictly lower than status pill by ${{clearanceBelowPill.toFixed(1)}}px`);
            }}

            if (clearanceBelowLegend <= 0) {{
                issues.push(`Array highest element (${{highestElDescription}} at top=${{highestTop.toFixed(1)}}) collides with or is higher than color legend (bottom=${{legR.bottom.toFixed(1)}})`);
            }} else {{
                checks.push(`Highest array element (${{highestElDescription}}) is strictly lower than color legend by ${{clearanceBelowLegend.toFixed(1)}}px`);
            }}
        }}
    }}

    document.getElementById('results').textContent = JSON.stringify({{
        page: '{page}',
        viewport: '{name}',
        width: {w},
        height: {h},
        passed: issues.length === 0,
        checks: checks,
        issues: issues
    }});
}});
</script>
</body>
</html>
"""

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

harness_file = os.path.join(os.path.dirname(__file__), "harness_clearance_test.html")

total_tests = 0
passed_tests = 0

for page in pages:
    print(f"\n--- Testing Page: {page} ---")
    for w, h, name in viewports:
        total_tests += 1
        harness_content = harness_template.format(page=page, w=w, h=h, name=name)
        with open(harness_file, "w", encoding="utf-8") as f:
            f.write(harness_content)

        file_url = "file:///" + os.path.abspath(harness_file).replace("\\", "/")
        cmd = [
            chrome_path,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--allow-file-access-from-files",
            f"--window-size={w+60},{h+120}",
            "--virtual-time-budget=3000",
            "--dump-dom",
            file_url
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=12)
            dom = res.stdout
            match = re.search(r'<div id="results">(\{.*?\})</div>', dom, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                if data["passed"]:
                    passed_tests += 1
                    print(f"  [PASS] {name}: {data['checks'][-1]} (All {len(data['checks'])} checks OK)")
                else:
                    all_passed = False
                    print(f"  [FAIL] {name}:")
                    for iss in data["issues"]:
                        print(f"         - {iss}")
            else:
                all_passed = False
                print(f"  [FAIL] {name}: Could not extract test results from Chrome output")
        except Exception as e:
            all_passed = False
            print(f"  [ERROR] {name}: {e}")

if os.path.exists(harness_file):
    try:
        os.remove(harness_file)
    except:
        pass

print("\n" + "=" * 65)
if all_passed:
    print(f"ALL CLEARANCE TESTS PASSED ({passed_tests}/{total_tests})")
    print("Zero collisions detected; highest elements strictly lower than status options!")
else:
    print(f"SOME TESTS FAILED ({passed_tests}/{total_tests} passed)")
    sys.exit(1)

