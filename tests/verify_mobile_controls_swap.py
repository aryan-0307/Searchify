"""
tests/verify_mobile_controls_swap.py
Automated verification for toolbar controls order:
1. On mobile viewports (<= 860px):
   - .array-cluster appears BEFORE .playback-cluster (arrayRect.top < playbackRect.top).
   - .playback-cluster appears BEFORE .settings-cluster (playbackRect.top < settingsRect.top).
   - CSS order is: .array-cluster (1), .playback-cluster (2), .settings-cluster (3).
2. On desktop viewports (> 860px):
   - Desktop layout is preserved: .playback-cluster is on the left, .array-cluster in the center, .settings-cluster on the right.
   - playbackRect.left < arrayRect.left < settingsRect.left.
   - CSS order remains default (0).
3. Verified across mobile (320px to 860px) and desktop (861px to 1280px) on sorting.html and searching.html.
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
print("VERIFYING CONTROLS CLUSTER SWAP (ARRAY vs PLAYBACK) ON MOBILE")
print("=" * 70)

harness_template = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0;">
<iframe id="frame" src="../{page}" style="width: {w}px; height: {h}px; border:0; display:block;"></iframe>
<div id="results"></div>
<script>
window.addEventListener('load', async () => {{
    await new Promise(r => setTimeout(r, 600));
    const frame = document.getElementById('frame');
    const doc = frame.contentDocument;
    const win = frame.contentWindow;

    const playbackCluster = doc.querySelector('.playback-cluster');
    const arrayCluster = doc.querySelector('.array-cluster');
    const settingsCluster = doc.querySelector('.settings-cluster');

    const issues = [];
    const checks = [];

    if (!playbackCluster || !arrayCluster || !settingsCluster) {{
        issues.push('Could not find all 3 control clusters (.playback-cluster, .array-cluster, .settings-cluster)');
    }} else {{
        const playRect = playbackCluster.getBoundingClientRect();
        const arrRect = arrayCluster.getBoundingClientRect();
        const setRect = settingsCluster.getBoundingClientRect();

        const playStyle = win.getComputedStyle(playbackCluster);
        const arrStyle = win.getComputedStyle(arrayCluster);
        const setStyle = win.getComputedStyle(settingsCluster);

        const isMobile = {is_mobile};

        if (isMobile) {{
            // Mobile: Array cluster must appear ABOVE playback cluster
            if (arrRect.top >= playRect.top) {{
                issues.push(`Mobile swap failed: Array cluster top (${{arrRect.top.toFixed(1)}}) is NOT above Playback cluster top (${{playRect.top.toFixed(1)}})`);
            }} else {{
                checks.push(`Array cluster (top=${{arrRect.top.toFixed(1)}}) is strictly above Playback cluster (top=${{playRect.top.toFixed(1)}})`);
            }}

            if (playRect.top >= setRect.top) {{
                issues.push(`Mobile order failed: Playback cluster top (${{playRect.top.toFixed(1)}}) is NOT above Settings cluster top (${{setRect.top.toFixed(1)}})`);
            }} else {{
                checks.push(`Playback cluster (top=${{playRect.top.toFixed(1)}}) is strictly above Settings cluster (top=${{setRect.top.toFixed(1)}})`);
            }}

            // Check CSS order properties
            if (arrStyle.order !== '1') {{
                issues.push(`Array cluster CSS order should be '1', got '${{arrStyle.order}}'`);
            }}
            if (playStyle.order !== '2') {{
                issues.push(`Playback cluster CSS order should be '2', got '${{playStyle.order}}'`);
            }}
            if (setStyle.order !== '3') {{
                issues.push(`Settings cluster CSS order should be '3', got '${{setStyle.order}}'`);
            }}
            if (arrStyle.order === '1' && playStyle.order === '2' && setStyle.order === '3') {{
                checks.push("CSS flex orders match expected (array:1, playback:2, settings:3)");
            }}
        }} else {{
            // Desktop: Playback precedes Array, Array precedes Settings
            // When items are on the same row, left should be strictly less.
            // When items wrap onto subsequent rows, earlier item has lower top.
            const sameRowPlayArr = Math.abs(playRect.top - arrRect.top) < 15;
            if (sameRowPlayArr) {{
                if (playRect.left >= arrRect.left) {{
                    issues.push(`Desktop same-row: Playback left (${{playRect.left.toFixed(1)}}) should be to the left of Array left (${{arrRect.left.toFixed(1)}})`);
                }} else {{
                    checks.push(`Desktop same-row: Playback is to the left of Array`);
                }}
            }} else {{
                if (playRect.top >= arrRect.top) {{
                    issues.push(`Desktop wrapped: Playback top (${{playRect.top.toFixed(1)}}) should be above Array top (${{arrRect.top.toFixed(1)}})`);
                }} else {{
                    checks.push(`Desktop wrapped: Playback (row 1, top=${{playRect.top.toFixed(1)}}) precedes Array (row 2, top=${{arrRect.top.toFixed(1)}})`);
                }}
            }}

            const sameRowArrSet = Math.abs(arrRect.top - setRect.top) < 15;
            if (sameRowArrSet) {{
                if (arrRect.left >= setRect.left) {{
                    issues.push(`Desktop same-row: Array left (${{arrRect.left.toFixed(1)}}) should be to the left of Settings left (${{setRect.left.toFixed(1)}})`);
                }} else {{
                    checks.push(`Desktop same-row: Array is to the left of Settings`);
                }}
            }} else {{
                if (arrRect.top >= setRect.top) {{
                    issues.push(`Desktop wrapped: Array top (${{arrRect.top.toFixed(1)}}) should be above Settings top (${{setRect.top.toFixed(1)}})`);
                }} else {{
                    checks.push(`Desktop wrapped: Array (top=${{arrRect.top.toFixed(1)}}) precedes Settings (top=${{setRect.top.toFixed(1)}})`);
                }}
            }}

            if (playStyle.order !== '0' || arrStyle.order !== '0' || setStyle.order !== '0') {{
                issues.push(`Desktop CSS orders should be default '0', got play=${{playStyle.order}}, arr=${{arrStyle.order}}, set=${{setStyle.order}}`);
            }} else {{
                checks.push("Desktop CSS orders default to '0' (DOM order)");
            }}
        }}
    }}

    document.getElementById('results').textContent = JSON.stringify({{
        page: '{page}',
        viewport: '{name}',
        width: {w},
        height: {h},
        isMobile: {is_mobile},
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

harness_file = os.path.join(os.path.dirname(__file__), "harness_controls_swap_test.html")

total_tests = 0
passed_tests = 0

for page in pages:
    print(f"\n--- Testing Page: {page} ---")
    for w, h, name, is_mobile in viewports:
        total_tests += 1
        harness_content = harness_template.format(
            page=page,
            w=w,
            h=h,
            name=name,
            is_mobile="true" if is_mobile else "false"
        )
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
            "--virtual-time-budget=2000",
            "--dump-dom",
            file_url
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=20)
            dom = res.stdout
            match = re.search(r'<div id="results">(\{.*?\})</div>', dom, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                if data["passed"]:
                    passed_tests += 1
                    mode_label = "[MOBILE]" if is_mobile else "[DESKTOP]"
                    print(f"  [PASS] {mode_label} {name}: {data['checks'][0]}")
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

print("\n" + "=" * 70)
if all_passed:
    print(f"ALL CONTROLS SWAP TESTS PASSED ({passed_tests}/{total_tests})")
    print("Mobile swapped positions verified (Array cluster first, Playback cluster second). Desktop untouched.")
else:
    print(f"SOME TESTS FAILED ({passed_tests}/{total_tests} passed)")
    sys.exit(1)

