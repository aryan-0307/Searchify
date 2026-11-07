import subprocess
import json
import re
import os
import sys

viewports = [
    (320, 568, "iPhone SE 1st gen (320px)"),
    (360, 740, "Galaxy S8/S9/S10 compact (360px)"),
    (375, 667, "iPhone SE / 8 (375px)"),
    (390, 844, "iPhone 13 / 14 / 15 / 16 (390px)"),
    (412, 915, "Samsung Galaxy S23 / Pixel 7 (412px)"),
    (430, 932, "iPhone 14/15/16 Pro Max (430px)")
]

pages = ["searching.html", "sorting.html"]

all_passed = True
print("============================================================")
print("VERIFYING MOBILE VISUALIZER ARRAY INDEX VISIBILITY")
print("============================================================")

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

    const isSearching = '{page}' === 'searching.html';

    if (isSearching) {{
        const cells = Array.from(doc.querySelectorAll('.cell'));
        const issues = [];

        cells.forEach((cell, i) => {{
            const cellR = cell.getBoundingClientRect();
            const idxEl = cell.querySelector('.cell-index');
            if (!idxEl) {{
                issues.push(`Cell ${{i}} has no .cell-index element`);
                return;
            }}
            const idxR = idxEl.getBoundingClientRect();

            // Check if index extends beyond canvas bottom
            if (idxR.bottom > areaRect.bottom + 1) {{
                issues.push(`Cell ${{i}} index extends beyond canvas bottom (idxBottom=${{idxR.bottom}}, areaBottom=${{areaRect.bottom}})`);
            }}

            // Check if index overlaps another cell below it in the same column
            cells.forEach((otherCell, j) => {{
                if (i !== j) {{
                    const otherR = otherCell.getBoundingClientRect();
                    const horizOverlap = Math.max(idxR.left, otherR.left) < Math.min(idxR.right, otherR.right);
                    // other cell is vertically below cell in the same column
                    if (horizOverlap && otherR.top >= cellR.bottom - 2) {{
                        if (idxR.bottom > otherR.top) {{
                            issues.push(`Cell ${{i}} index overlaps Cell ${{j}} (idxBottom=${{idxR.bottom}}, nextCellTop=${{otherR.top}})`);
                        }}
                    }}
                }}
            }});
        }});

        document.getElementById('results').textContent = JSON.stringify({{
            page: '{page}',
            totalCells: cells.length,
            issues: issues,
            passed: issues.length === 0 && cells.length > 0
        }});
    }} else {{
        const bars = Array.from(doc.querySelectorAll('.bar'));
        const issues = [];

        bars.forEach((bar, i) => {{
            const barR = bar.getBoundingClientRect();
            const idxEl = bar.querySelector('.bar-index');
            if (!idxEl) {{
                issues.push(`Bar ${{i}} has no .bar-index element`);
                return;
            }}
            const idxR = idxEl.getBoundingClientRect();

            // Check if index extends beyond canvas bottom
            if (idxR.bottom > areaRect.bottom + 1) {{
                issues.push(`Bar ${{i}} index extends beyond canvas bottom (idxBottom=${{idxR.bottom}}, areaBottom=${{areaRect.bottom}})`);
            }}
            if (idxR.height < 6) {{
                issues.push(`Bar ${{i}} index has invalid height: ${{idxR.height}}`);
            }}
        }});

        document.getElementById('results').textContent = JSON.stringify({{
            page: '{page}',
            totalBars: bars.length,
            issues: issues,
            passed: issues.length === 0 && bars.length > 0
        }});
    }}
}});
</script>
</body>
</html>
"""

for page in pages:
    print(f"\n--- Testing {page} across mobile viewports ---")
    for w, h, device_name in viewports:
        harness = harness_template.format(page=page, w=w, h=h)
        temp_file = f"tests/temp_mob_idx_{w}_{page}"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(harness)

        cmd = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--allow-file-access-from-files",
            "--virtual-time-budget=3000",
            f"--window-size={w+50},{h+100}",
            "--dump-dom",
            f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{temp_file}"
        ]

        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        if os.path.exists(temp_file):
            os.remove(temp_file)

        match = re.search(r'<div id="results">(\{.*?\})</div>', res.stdout)
        if not match:
            print(f"  [FAIL] {device_name}: Could not extract results")
            all_passed = False
            continue

        data = json.loads(match.group(1))
        if data["passed"]:
            total = data.get("totalCells") or data.get("totalBars")
            print(f"  [PASS] {device_name}: All {total} indices fully visible without clipping or overlap")
        else:
            print(f"  [FAIL] {device_name}: {data['issues']}")
            all_passed = False

if not all_passed:
    sys.exit(1)

print("\n============================================================")
print("ALL MOBILE INDEX VISIBILITY VERIFICATIONS PASSED (100%)")
print("============================================================")
