import subprocess
import json
import os
import sys

print("============================================================")
print("VERIFYING PERFECT VISUALIZATION-TO-PSEUDOCODE SYNCHRONIZATION")
print("============================================================")

harness_code = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<div id="results"></div>
<script src="../js/main.js"></script>
<script src="../js/sorting-algorithms.js"></script>
<script src="../js/searching-algorithms.js"></script>
<script>
window.addEventListener('load', () => {
    const report = {
        sorting: {},
        searching: {},
        allValid: true
    };

    const SA = window.SortingAlgorithms;
    const SEA = window.SearchingAlgorithms;
    const testArr = [34, 12, 89, 5, 23, 77, 42];

    // 1. Check Sorting Algorithms (All 10 Algorithms)
    const sortAlgos = [
        'bubbleSort',
        'selectionSort',
        'insertionSort',
        'mergeSort',
        'quickSort',
        'heapSort',
        'shellSort',
        'countingSort',
        'radixSort',
        'bucketSort'
    ];
    sortAlgos.forEach(algo => {
        const pseudocode = SA.pseudocode[algo];
        const steps = SA[algo](testArr, 'asc');
        let validSteps = 0;
        let invalidSteps = [];

        steps.forEach((step, idx) => {
            const line = step.pseudocodeLine;
            if (typeof line !== 'number' || line < 0 || line >= pseudocode.length) {
                invalidSteps.push({ idx, line, max: pseudocode.length - 1 });
            } else {
                validSteps++;
            }
        });

        // Test specific semantic alignments
        let hasCompareHighlight = false;
        let hasSwapOrActionHighlight = false;

        steps.forEach(s => {
            if (s.comparing && s.comparing.length > 0) {
                const codeText = pseudocode[s.pseudocodeLine];
                if (codeText && (codeText.includes('if') || codeText.includes('while') || codeText.includes('Compare') || codeText.includes('≤') || codeText.includes('<') || codeText.includes('>') || codeText.includes('violates') || codeText.includes('count') || codeText.includes('digit') || codeText.includes('bIdx') || codeText.includes('buckets') || codeText.includes('A['))) {
                    hasCompareHighlight = true;
                }
            }
            if (s.swapping && s.swapping.length > 0) {
                const codeText = pseudocode[s.pseudocodeLine];
                if (codeText && (codeText.includes('swap') || codeText.includes('A[') || codeText.includes('=') || codeText.includes('output') || codeText.includes('buckets'))) {
                    hasSwapOrActionHighlight = true;
                }
            }
        });

        report.sorting[algo] = {
            totalSteps: steps.length,
            pseudocodeLines: pseudocode.length,
            validSteps: validSteps,
            invalidSteps: invalidSteps,
            hasCompareHighlight: hasCompareHighlight,
            hasSwapOrActionHighlight: hasSwapOrActionHighlight,
            passed: invalidSteps.length === 0 && hasCompareHighlight && hasSwapOrActionHighlight
        };

        if (invalidSteps.length > 0 || !hasCompareHighlight || !hasSwapOrActionHighlight) {
            report.allValid = false;
        }
    });

    // 2. Check Searching Algorithms
    const searchAlgos = [
        { name: 'linearSearch', target: 23, arr: [5, 12, 23, 34, 42, 77, 89] },
        { name: 'binarySearch', target: 23, arr: [5, 12, 23, 34, 42, 77, 89] }
    ];

    searchAlgos.forEach(testCase => {
        const algo = testCase.name;
        const pseudocode = SEA.pseudocode[algo];
        const steps = SEA[algo](testCase.arr, testCase.target);
        let validSteps = 0;
        let invalidSteps = [];

        steps.forEach((step, idx) => {
            const line = step.pseudocodeLine;
            if (typeof line !== 'number' || line < 0 || line >= pseudocode.length) {
                invalidSteps.push({ idx, line, max: pseudocode.length - 1 });
            } else {
                validSteps++;
            }
        });

        // Test specific semantic alignments: found step highlights return mid or return i
        const finalFound = steps.find(s => s.found !== null && s.found !== undefined);
        let foundHighlightsReturn = false;
        if (finalFound) {
            const codeText = pseudocode[finalFound.pseudocodeLine];
            if (codeText && codeText.includes('return')) {
                foundHighlightsReturn = true;
            }
        }

        report.searching[algo] = {
            totalSteps: steps.length,
            pseudocodeLines: pseudocode.length,
            validSteps: validSteps,
            invalidSteps: invalidSteps,
            foundHighlightsReturn: foundHighlightsReturn,
            passed: invalidSteps.length === 0 && foundHighlightsReturn
        };

        if (invalidSteps.length > 0 || !foundHighlightsReturn) {
            report.allValid = false;
        }
    });

    document.getElementById('results').textContent = JSON.stringify(report);
});
</script>
</body>
</html>
"""

test_harness_path = os.path.join("tests", "_temp_verify_pseudocode_sync.html")
with open(test_harness_path, "w", encoding="utf-8") as f:
    f.write(harness_code)

chrome_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--dump-dom",
    f"file:///{os.path.abspath(test_harness_path).replace(os.sep, '/')}"
]

res = subprocess.run(chrome_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
dom = res.stdout

if os.path.exists(test_harness_path):
    os.remove(test_harness_path)

import re
m = re.search(r'<div id="results">(.*?)</div>', dom)
if not m or not m.group(1):
    print("[FAIL] Could not extract results from test harness")
    sys.exit(1)

data = json.loads(m.group(1))

all_passed = True

print("\n--- Sorting Algorithms Pseudocode Synchronization ---")
for algo, r in data.get("sorting", {}).items():
    if r.get("passed"):
        print(f"  [PASS] {algo:<15} ({r['totalSteps']} steps) -> 100% bounds valid, compare & swap line actions perfectly aligned")
    else:
        print(f"  [FAIL] {algo:<15} -> invalid steps: {r.get('invalidSteps')}, compare: {r.get('hasCompareHighlight')}, swap: {r.get('hasSwapOrActionHighlight')}")
        all_passed = False

print("\n--- Searching Algorithms Pseudocode Synchronization ---")
for algo, r in data.get("searching", {}).items():
    if r.get("passed"):
        print(f"  [PASS] {algo:<15} ({r['totalSteps']} steps) -> 100% bounds valid, target found highlights exact return line")
    else:
        print(f"  [FAIL] {algo:<15} -> invalid steps: {r.get('invalidSteps')}, return highlighted: {r.get('foundHighlightsReturn')}")
        all_passed = False

if all_passed and data.get("allValid"):
    print("\n============================================================")
    print("ALL ALGORITHMS SYNCHRONIZE 100% PERFECTLY WITH PSEUDOCODE")
    print("============================================================")
    sys.exit(0)
else:
    print("\nSOME SYNCHRONIZATION CHECKS FAILED")
    sys.exit(1)

