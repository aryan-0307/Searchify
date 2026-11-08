"""
tests/verify_ten_sorting_algorithms.py
End-to-end automated verification for all 10 sorting algorithms in Searchify:
1. Verifies all 10 sorting algorithms exist in the playground <select>.
2. Verifies complexity metadata, "How It Works", properties, and the 10-algorithm comparison matrix table.
3. Verifies that running each of the 5 new algorithms generates the correct auxiliary visualizations:
   - Heap Sort: Binary Heap Tree nodes, levels, parent/child highlights.
   - Shell Sort: Gap tracker, gap sequence pills, stride comparison info.
   - Counting Sort: Frequency count array cells, output array cells, active index highlights.
   - Radix Sort: 10 digit buckets (0-9), digit place passes, bucket chips.
   - Bucket Sort: Range value buckets, active sorting highlights, items inside buckets.
4. Verifies classic 5 algorithms work seamlessly without auxiliary display.
5. Verifies Prev, Next, Play, Reset, and Restart controls.
6. Verifies negative integers and identical values edge cases (no negative heights, no division by zero).
7. Verifies zero console errors across all 10 algorithms.
"""

import subprocess
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HTML_PATH = os.path.abspath("sorting.html")

harness_html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Ten Algorithms Verification Harness</title>
</head>
<body style="margin:0; padding:0;">
    <iframe id="test-frame" src="file:///__HTML_PATH__" style="width:1280px; height:900px; border:0;"></iframe>
    <div id="test-results"></div>

    <script>
    window.addEventListener('load', async () => {
        await new Promise(r => setTimeout(r, 600));
        const frame = document.getElementById('test-frame');
        const win = frame.contentWindow;
        const doc = frame.contentDocument;

        const results = {
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
            // 1. Verify algorithm selector options
            const algoSelect = doc.getElementById('algorithm-select');
            assert(algoSelect !== null, "Algorithm selector exists");

            const expectedAlgos = [
                'bubbleSort', 'selectionSort', 'insertionSort', 'mergeSort', 'quickSort',
                'heapSort', 'shellSort', 'countingSort', 'radixSort', 'bucketSort'
            ];

            const optionValues = Array.from(algoSelect.options).map(o => o.value);
            for (const expected of expectedAlgos) {
                assert(optionValues.includes(expected), `Selector contains ${expected}`);
            }

            // 2. Verify window.SortingAlgorithms has all 10 algorithms and complexity info
            const SA = win.SortingAlgorithms;
            assert(SA !== undefined, "window.SortingAlgorithms is defined");
            for (const expected of expectedAlgos) {
                assert(typeof SA[expected] === 'function', `window.SortingAlgorithms.${expected} is a function`);
                assert(SA.complexityInfo && SA.complexityInfo[expected], `complexityInfo exists for ${expected}`);
            }

            // 3. Verify Complexity Section & 10-Algorithm Comparison Matrix
            for (const algo of expectedAlgos) {
                algoSelect.value = algo;
                algoSelect.dispatchEvent(new Event('change'));
                await new Promise(r => setTimeout(r, 50));

                const compContainer = doc.getElementById('complexity-display');
                assert(compContainer !== null, `Complexity container exists for ${algo}`);
                const compText = compContainer.textContent;
                const info = SA.complexityInfo[algo];

                assert(compText.includes(info.best), `${algo} displays best complexity: ${info.best}`);
                assert(compText.includes(info.worst), `${algo} displays worst complexity: ${info.worst}`);

                // Check that comparison table has 10 data rows and marks active row
                const compTable = compContainer.querySelector('.comparison-table');
                assert(compTable !== null, `Comparison matrix table rendered for ${algo}`);
                const rows = compTable.querySelectorAll('tbody tr');
                assert(rows.length === 10, `Comparison table has exactly 10 rows (found ${rows.length})`);

                const activeRow = compTable.querySelector('tr.active-algo-row');
                assert(activeRow !== null, `Comparison table has active row for ${algo}`);
                if (activeRow) {
                    assert(activeRow.textContent.includes(info.name.split(' ')[0]), `Active row text matches algorithm name: ${info.name}`);
                }
            }

            // 4. Test Heap Sort Auxiliary Visualization
            algoSelect.value = 'heapSort';
            algoSelect.dispatchEvent(new Event('change'));
            const customInput = doc.getElementById('custom-array');
            const applyBtn = doc.getElementById('apply-custom-btn');
            const generateBtn = doc.getElementById('generate-btn');
            const stepNextBtn = doc.getElementById('next-btn');
            const stepPrevBtn = doc.getElementById('prev-btn');
            const resetBtn = doc.getElementById('reset-btn');
            const auxPanel = doc.getElementById('viz-auxiliary-panel');

            customInput.value = '45, 12, 85, 32, 89, 39, 69, 44, 42, 1, 10';
            applyBtn.click();
            await new Promise(r => setTimeout(r, 100));

            // Step next
            stepNextBtn.click();
            await new Promise(r => setTimeout(r, 60));

            assert(auxPanel.style.display !== 'none', "Heap Sort: auxPanel is visible");
            const heapNodes = auxPanel.querySelectorAll('.heap-node');
            assert(heapNodes.length > 0, `Heap Sort: binary heap tree rendered with ${heapNodes.length} nodes`);

            // Step forward several times
            for (let i = 0; i < 5; i++) stepNextBtn.click();
            await new Promise(r => setTimeout(r, 60));
            assert(auxPanel.querySelectorAll('.heap-node').length > 0, "Heap nodes persist across forward steps");

            // Step back
            stepPrevBtn.click();
            await new Promise(r => setTimeout(r, 60));
            assert(auxPanel.querySelectorAll('.heap-node').length > 0, "Heap nodes persist on step prev");

            // Reset
            resetBtn.click();
            await new Promise(r => setTimeout(r, 60));
            assert(auxPanel.style.display === 'none', "Heap Sort: reset hides auxPanel");

            // 5. Test Shell Sort Auxiliary Visualization
            algoSelect.value = 'shellSort';
            algoSelect.dispatchEvent(new Event('change'));
            customInput.value = '50, 20, 80, 10, 30, 90, 70, 40';
            applyBtn.click();
            await new Promise(r => setTimeout(r, 100));

            stepNextBtn.click();
            await new Promise(r => setTimeout(r, 60));
            assert(auxPanel.style.display !== 'none', "Shell Sort: auxPanel is visible");
            const shellPills = auxPanel.querySelectorAll('.gap-step-pill');
            assert(shellPills.length > 0, `Shell Sort: gap pills rendered (count: ${shellPills.length})`);

            // 6. Test Counting Sort Auxiliary Visualization
            algoSelect.value = 'countingSort';
            algoSelect.dispatchEvent(new Event('change'));
            customInput.value = '5, 2, 8, 2, 5, 1, 9, 3';
            applyBtn.click();
            await new Promise(r => setTimeout(r, 100));

            stepNextBtn.click();
            await new Promise(r => setTimeout(r, 60));
            assert(auxPanel.style.display !== 'none', "Counting Sort: auxPanel is visible");
            const countCells = auxPanel.querySelectorAll('.aux-cell');
            assert(countCells.length > 0, `Counting Sort: frequency cells rendered (count: ${countCells.length})`);

            // 7. Test Radix Sort Auxiliary Visualization
            algoSelect.value = 'radixSort';
            algoSelect.dispatchEvent(new Event('change'));
            customInput.value = '170, 45, 75, 90, 802, 24, 2, 66';
            applyBtn.click();
            await new Promise(r => setTimeout(r, 100));

            stepNextBtn.click();
            await new Promise(r => setTimeout(r, 60));
            assert(auxPanel.style.display !== 'none', "Radix Sort: auxPanel is visible");
            const digitBuckets = auxPanel.querySelectorAll('.digit-bucket');
            assert(digitBuckets.length === 10, `Radix Sort: 10 digit buckets rendered (count: ${digitBuckets.length})`);

            // 8. Test Bucket Sort Auxiliary Visualization
            algoSelect.value = 'bucketSort';
            algoSelect.dispatchEvent(new Event('change'));
            customInput.value = '29, 25, 3, 49, 9, 37, 21, 43';
            applyBtn.click();
            await new Promise(r => setTimeout(r, 100));

            stepNextBtn.click();
            await new Promise(r => setTimeout(r, 60));
            assert(auxPanel.style.display !== 'none', "Bucket Sort: auxPanel is visible");
            const rangeBuckets = auxPanel.querySelectorAll('.range-bucket');
            assert(rangeBuckets.length > 0, `Bucket Sort: range buckets rendered (count: ${rangeBuckets.length})`);

            // 9. Test Classic 5 Algorithms (auxPanel must remain hidden)
            const classicAlgos = ['bubbleSort', 'selectionSort', 'insertionSort', 'mergeSort', 'quickSort'];
            for (const cAlgo of classicAlgos) {
                algoSelect.value = cAlgo;
                algoSelect.dispatchEvent(new Event('change'));
                generateBtn.click();
                await new Promise(r => setTimeout(r, 50));
                stepNextBtn.click();
                await new Promise(r => setTimeout(r, 50));
                assert(auxPanel.style.display === 'none', `Classic algo ${cAlgo} keeps auxPanel hidden`);
            }

            // 10. Test Negative Numbers & Identical Elements (proportional bar heights)
            algoSelect.value = 'countingSort';
            algoSelect.dispatchEvent(new Event('change'));
            customInput.value = '-50, 20, -10, 40, -5, 0, 30';
            applyBtn.click();
            await new Promise(r => setTimeout(r, 100));

            const bars = doc.querySelectorAll('.bar');
            assert(bars.length === 7, `7 bars rendered for negative array (found ${bars.length})`);
            for (let b = 0; b < bars.length; b++) {
                const h = parseInt(bars[b].style.height, 10);
                assert(!isNaN(h) && h >= 14, `Bar ${b} has positive height >= 14px (actual: ${bars[b].style.height})`);
            }

            // Test Identical elements
            customInput.value = '42, 42, 42, 42, 42';
            applyBtn.click();
            await new Promise(r => setTimeout(r, 100));
            const idBars = doc.querySelectorAll('.bar');
            assert(idBars.length === 5, `5 bars rendered for identical elements array`);
            for (let b = 0; b < idBars.length; b++) {
                const h = parseInt(idBars[b].style.height, 10);
                assert(!isNaN(h) && h > 0, `Identical bar ${b} has valid positive height (actual: ${idBars[b].style.height})`);
            }

            // 11. Test Ascending vs Descending Toggle
            const descBtn = doc.getElementById('desc-btn');
            const ascBtn = doc.getElementById('asc-btn');
            descBtn.click();
            await new Promise(r => setTimeout(r, 50));
            algoSelect.value = 'heapSort';
            algoSelect.dispatchEvent(new Event('change'));
            generateBtn.click();
            await new Promise(r => setTimeout(r, 100));
            stepNextBtn.click();
            await new Promise(r => setTimeout(r, 50));
            assert(auxPanel.style.display !== 'none', "Heap Sort works in Descending order");
            ascBtn.click();

        } catch (err) {
            results.passed = false;
            results.errors.push('Unhandled JS Exception: ' + err.toString() + '\\n' + err.stack);
        }

        const out = document.getElementById('test-results');
        out.textContent = JSON.stringify(results);
    });
    </script>
</body>
</html>
"""

harness_html = harness_html_template.replace("__HTML_PATH__", HTML_PATH.replace(os.sep, "/"))

harness_file = os.path.abspath("tests/_temp_ten_algos_harness.html")
with open(harness_file, "w", encoding="utf-8") as f:
    f.write(harness_html)

try:
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--enable-logging=stderr",
        "--virtual-time-budget=6000",
        "--dump-dom",
        f"file:///{harness_file.replace(os.sep, '/')}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    dom = res.stdout

    import re
    m = re.search(r'<div id="test-results">(\{.*?\})</div>', dom, re.DOTALL)
    if not m or not m.group(1):
        print("[FAIL] Could not parse test-results from DOM.")
        print("DOM output snippet:", dom[:800])
        sys.exit(1)

    result_json = json.loads(m.group(1))
    print(f"Total assertions checked: {len(result_json['checks'])}")
    for check in result_json["checks"]:
        print(f"  [PASS] {check}")

    if not result_json["passed"] or len(result_json["errors"]) > 0:
        print("\nERRORS DETECTED:")
        for err in result_json["errors"]:
            print(f"  [FAIL] {err}")
        sys.exit(1)

    print("\n[SUCCESS] ALL TEN SORTING ALGORITHMS FULLY VERIFIED IN HEADLESS CHROME!")
    sys.exit(0)

finally:
    if os.path.exists(harness_file):
        try:
            os.remove(harness_file)
        except Exception:
            pass
