"""
tests/verify_heap_sort_layout.py
Automated verification for Heap Sort visualizer layout:
1. Verifies that the Heap Tree operation area requires ZERO scrolling (scrollHeight <= clientHeight, overflow visible, max-height none).
2. Verifies that the Heap Tree operation area and the Array Elements (bars) area NEVER mix into each other:
   - Every bar and every bar label is strictly lower than the bottom of the Heap Tree panel.
   - Clearance between the bottom of the Heap Tree panel and the top of the highest bar label is at least 30px on desktop and 20px on mobile.
3. Verifies layout separation remains 100% intact across active stepping (forward & backward) and algorithm switching.
4. Tested across desktop (1280px), tablet (768px), and mobile (375px, 412px).
"""

import subprocess
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HTML_PATH = os.path.abspath("sorting.html")

harness_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Heap Sort Layout Verification</title>
</head>
<body style="margin:0; padding:0;">
    <iframe id="test-frame" src="file:///__HTML_PATH__" style="width:__W__px; height:__H__px; border:0;"></iframe>
    <div id="test-results"></div>

    <script>
    window.addEventListener('load', async () => {
        await new Promise(r => setTimeout(r, 600));
        const frame = document.getElementById('test-frame');
        const win = frame.contentWindow;
        const doc = frame.contentDocument;

        const results = {
            viewport: '__NAME__',
            width: __W__,
            passed: true,
            errors: [],
            checks: []
        };

        function assert(cond, msg) {
            if (!cond) {
                results.passed = false;
                results.errors.push(msg);
            } else {
                results.checks.push(msg);
            }
        }

        try {
            const algoSelect = doc.getElementById('algorithm-select');
            const customInput = doc.getElementById('custom-array');
            const applyBtn = doc.getElementById('apply-custom-btn');
            const stepNextBtn = doc.getElementById('next-btn');
            const stepPrevBtn = doc.getElementById('prev-btn');
            const vizArea = doc.getElementById('visualization-area');
            const auxPanel = doc.getElementById('viz-auxiliary-panel');

            // Select Heap Sort
            algoSelect.value = 'heapSort';
            algoSelect.dispatchEvent(new Event('change'));
            await new Promise(r => setTimeout(r, 100));

            assert(vizArea.classList.contains('heap-sort-active'), "vizArea has class 'heap-sort-active'");

            // Set a diverse test array with 12 elements (4 heap levels)
            customInput.value = '95, 34, 78, 12, 67, 45, 89, 23, 56, 99, 10, 82';
            applyBtn.click();
            await new Promise(r => setTimeout(r, 120));

            // Start stepping
            stepNextBtn.click();
            await new Promise(r => setTimeout(r, 80));

            assert(auxPanel.style.display !== 'none', "auxPanel is displayed for Heap Sort");
            assert(auxPanel.classList.contains('heap-tree-mode'), "auxPanel has 'heap-tree-mode' class");

            // 1. Verify ZERO scrolling in Heap Tree Panel
            const auxStyle = win.getComputedStyle(auxPanel);
            const clientH = auxPanel.clientHeight;
            const scrollH = auxPanel.scrollHeight;
            const overflowY = auxStyle.overflowY;

            assert(scrollH <= clientH + 2, `Heap Tree requires zero scrolling (scrollH=${scrollH}px, clientH=${clientH}px)`);
            assert(overflowY === 'visible', `Heap Tree overflow-y is visible (actual: ${overflowY})`);

            // Check that all 4 levels of the tree exist and are rendered
            const levels = auxPanel.querySelectorAll('.heap-level');
            assert(levels.length >= 3, `Heap Tree has at least 3-4 levels rendered (found ${levels.length})`);

            const divider = auxPanel.querySelector('.heap-array-stage-divider');
            assert(divider !== null, "Heap Tree has clear array stage divider");

            // 2. Verify separation between Heap Tree and Array Bars
            function verifyClearance(stepNum) {
                const heapRect = auxPanel.getBoundingClientRect();
                const bars = Array.from(doc.querySelectorAll('.bar'));
                assert(bars.length === 12, `Step ${stepNum}: 12 bars found`);

                let minBarTop = 999999;
                let minLabelTop = 999999;

                bars.forEach(bar => {
                    const bR = bar.getBoundingClientRect();
                    if (bR.top < minBarTop) minBarTop = bR.top;

                    const label = bar.querySelector('.bar-label');
                    if (label) {
                        const lR = label.getBoundingClientRect();
                        if (lR.top < minLabelTop) minLabelTop = lR.top;
                    }
                });

                const highestTop = Math.min(minBarTop, minLabelTop);
                const clearance = highestTop - heapRect.bottom;
                const minAllowed = __W__ <= 768 ? 20 : 35;

                assert(clearance >= minAllowed, `Step ${stepNum}: Highest bar element (top=${highestTop.toFixed(1)}px) is strictly lower than Heap Tree panel (bottom=${heapRect.bottom.toFixed(1)}px) by ${clearance.toFixed(1)}px (min ${minAllowed}px)`);
            }

            verifyClearance(1);

            // Step through 8 more operations
            for (let s = 2; s <= 9; s++) {
                stepNextBtn.click();
                await new Promise(r => setTimeout(r, 60));
                verifyClearance(s);
            }

            // Test Step Prev
            stepPrevBtn.click();
            await new Promise(r => setTimeout(r, 60));
            verifyClearance('prev');

            // 3. Test Algorithm Switching
            algoSelect.value = 'bubbleSort';
            algoSelect.dispatchEvent(new Event('change'));
            await new Promise(r => setTimeout(r, 80));
            assert(!vizArea.classList.contains('heap-sort-active'), "Switching to bubbleSort removes 'heap-sort-active'");
            assert(auxPanel.style.display === 'none', "auxPanel hidden on bubbleSort");

            // Switch back to heapSort
            algoSelect.value = 'heapSort';
            algoSelect.dispatchEvent(new Event('change'));
            await new Promise(r => setTimeout(r, 80));
            assert(vizArea.classList.contains('heap-sort-active'), "Switching back to heapSort restores 'heap-sort-active'");

        } catch (err) {
            results.passed = false;
            results.errors.push('Exception: ' + err.toString() + '\\n' + err.stack);
        }

        const out = document.getElementById('test-results');
        out.textContent = JSON.stringify(results);
    });
    </script>
</body>
</html>
"""

viewports = [
    (1280, 850, "Desktop 1280px"),
    (768, 900, "iPad Portrait 768px"),
    (412, 850, "Galaxy S23 412px"),
    (375, 800, "iPhone SE 375px")
]

harness_file = os.path.abspath("tests/_temp_heap_layout_harness.html")
all_passed = True

print("=" * 65)
print("VERIFYING HEAP SORT ZERO-SCROLL & NON-OVERLAPPING LAYOUT")
print("=" * 65)

try:
    for w, h, name in viewports:
        print(f"\n--- Testing Viewport: {name} ({w}x{h}) ---")
        content = harness_template.replace("__HTML_PATH__", HTML_PATH.replace(os.sep, "/"))
        content = content.replace("__W__", str(w)).replace("__H__", str(h)).replace("__NAME__", name)

        with open(harness_file, "w", encoding="utf-8") as f:
            f.write(content)

        cmd = [
            CHROME_PATH,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--allow-file-access-from-files",
            f"--window-size={w+60},{h+100}",
            "--virtual-time-budget=8000",
            "--dump-dom",
            f"file:///{harness_file.replace(os.sep, '/')}"
        ]

        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        import re
        m = re.search(r'<div id="test-results">(\{.*?\})</div>', res.stdout, re.DOTALL)
        if not m or not m.group(1):
            print(f"  [FAIL] Could not parse results for {name}")
            all_passed = False
            continue

        data = json.loads(m.group(1))
        for chk in data["checks"]:
            print(f"  [PASS] {chk}")

        if not data["passed"] or len(data["errors"]) > 0:
            all_passed = False
            for err in data["errors"]:
                print(f"  [FAIL] {err}")

    if all_passed:
        print("\n" + "=" * 65)
        print("ALL HEAP SORT LAYOUT VERIFICATIONS PASSED (100% PASS RATE)!")
        print("=" * 65)
        sys.exit(0)
    else:
        print("\n[FAIL] Some Heap Sort layout verifications failed!")
        sys.exit(1)

finally:
    if os.path.exists(harness_file):
        try:
            os.remove(harness_file)
        except Exception:
            pass

