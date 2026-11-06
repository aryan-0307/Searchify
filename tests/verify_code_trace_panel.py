import subprocess
import json
import os
import sys

print("============================================================")
print("VERIFYING LIVE CODE TRACE (80:20 RATIO) VISUALIZER PANEL")
print("============================================================")

test_html_content = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0;">
<iframe id="sort-frame" src="../sorting.html" style="width: 1200px; height: 900px; border: 0;"></iframe>
<iframe id="search-frame" src="../searching.html" style="width: 1200px; height: 900px; border: 0;"></iframe>
<div id="results"></div>

<script>
window.addEventListener('load', async () => {
    await new Promise(r => setTimeout(r, 250));

    const results = {};

    // ========================================================
    // 1. SORTING VISUALIZER (sorting.html)
    // ========================================================
    const sortWin = document.getElementById('sort-frame').contentWindow;
    const sortDoc = document.getElementById('sort-frame').contentDocument;

    const sortWrapper = sortDoc.querySelector('.viz-canvas-wrapper');
    const sortArea = sortDoc.getElementById('visualization-area');
    const sortPanel = sortDoc.getElementById('viz-code-panel');
    const sortCodeLines = sortDoc.getElementById('viz-code-lines');
    const sortAlgoSelect = sortDoc.getElementById('algorithm-select');
    const sortStepBadge = sortDoc.getElementById('viz-code-step-badge');
    const sortStatus = sortDoc.getElementById('viz-code-status');
    const sortToggleBtn = sortDoc.getElementById('viz-code-toggle');

    const sortWrapperRect = sortWrapper.getBoundingClientRect();
    const sortAreaRect = sortArea.getBoundingClientRect();
    const sortPanelRect = sortPanel.getBoundingClientRect();

    const sortTotalWidth = sortAreaRect.width + sortPanelRect.width;
    const sortAreaRatio = sortAreaRect.width / sortTotalWidth;
    const sortPanelRatio = sortPanelRect.width / sortTotalWidth;

    const sortInitialLines = Array.from(sortCodeLines.querySelectorAll('.viz-code-line')).map(el => el.textContent.trim());

    // Test Algorithm Change
    sortAlgoSelect.value = 'quickSort';
    sortAlgoSelect.dispatchEvent(new sortWin.Event('change', { bubbles: true }));
    await new Promise(r => setTimeout(r, 60));

    const sortQuickLines = Array.from(sortCodeLines.querySelectorAll('.viz-code-line')).map(el => el.textContent.trim());

    // Test Stepping / Next Step
    const sortNextBtn = sortDoc.getElementById('next-btn');
    sortNextBtn.click();
    await new Promise(r => setTimeout(r, 80));

    const sortActiveLineEl = sortCodeLines.querySelector('.viz-code-line.active');
    const sortHasActiveLine = sortActiveLineEl !== null;
    const sortActiveLineNum = sortActiveLineEl ? sortActiveLineEl.getAttribute('data-line') : null;
    const sortStepBadgeText = sortStepBadge ? sortStepBadge.textContent.trim() : '';

    // Test Toggle Collapse
    sortToggleBtn.click();
    await new Promise(r => setTimeout(r, 60));
    const sortIsCollapsed = sortWrapper.classList.contains('code-collapsed');

    sortToggleBtn.click();
    await new Promise(r => setTimeout(r, 60));
    const sortIsReExpanded = !sortWrapper.classList.contains('code-collapsed');

    results.sorting = {
        hasWrapper: !!sortWrapper,
        hasArea: !!sortArea,
        hasPanel: !!sortPanel,
        areaRatio: sortAreaRatio,
        panelRatio: sortPanelRatio,
        ratioValid: Math.abs(sortAreaRatio - 0.80) <= 0.05 && Math.abs(sortPanelRatio - 0.20) <= 0.05,
        initialLineCount: sortInitialLines.length,
        quickSortLineCount: sortQuickLines.length,
        hasActiveLineOnStep: sortHasActiveLine,
        activeLineNum: sortActiveLineNum,
        stepBadgeText: sortStepBadgeText,
        toggleCollapsed: sortIsCollapsed,
        toggleReExpanded: sortIsReExpanded
    };

    // ========================================================
    // 2. SEARCHING VISUALIZER (searching.html)
    // ========================================================
    const searchWin = document.getElementById('search-frame').contentWindow;
    const searchDoc = document.getElementById('search-frame').contentDocument;

    const searchWrapper = searchDoc.querySelector('.viz-canvas-wrapper');
    const searchArea = searchDoc.getElementById('visualization-area');
    const searchPanel = searchDoc.getElementById('viz-code-panel');
    const searchCodeLines = searchDoc.getElementById('viz-code-lines');
    const searchAlgoSelect = searchDoc.getElementById('algorithm-select');
    const searchStepBadge = searchDoc.getElementById('viz-code-step-badge');
    const searchNextBtn = searchDoc.getElementById('next-btn');

    const searchWrapperRect = searchWrapper.getBoundingClientRect();
    const searchAreaRect = searchArea.getBoundingClientRect();
    const searchPanelRect = searchPanel.getBoundingClientRect();

    const searchTotalWidth = searchAreaRect.width + searchPanelRect.width;
    const searchAreaRatio = searchAreaRect.width / searchTotalWidth;
    const searchPanelRatio = searchPanelRect.width / searchTotalWidth;

    const searchInitialLines = Array.from(searchCodeLines.querySelectorAll('.viz-code-line')).map(el => el.textContent.trim());

    // Switch to Binary Search
    searchAlgoSelect.value = 'binarySearch';
    searchAlgoSelect.dispatchEvent(new searchWin.Event('change', { bubbles: true }));
    await new Promise(r => setTimeout(r, 60));

    const searchBinaryLines = Array.from(searchCodeLines.querySelectorAll('.viz-code-line')).map(el => el.textContent.trim());

    // Click Next Step
    searchNextBtn.click();
    await new Promise(r => setTimeout(r, 80));

    const searchActiveLineEl = searchCodeLines.querySelector('.viz-code-line.active');
    const searchHasActiveLine = searchActiveLineEl !== null;
    const searchActiveLineNum = searchActiveLineEl ? searchActiveLineEl.getAttribute('data-line') : null;
    const searchStepBadgeText = searchStepBadge ? searchStepBadge.textContent.trim() : '';

    results.searching = {
        hasWrapper: !!searchWrapper,
        hasArea: !!searchArea,
        hasPanel: !!searchPanel,
        areaRatio: searchAreaRatio,
        panelRatio: searchPanelRatio,
        ratioValid: Math.abs(searchAreaRatio - 0.80) <= 0.05 && Math.abs(searchPanelRatio - 0.20) <= 0.05,
        initialLineCount: searchInitialLines.length,
        binarySearchLineCount: searchBinaryLines.length,
        hasActiveLineOnStep: searchHasActiveLine,
        activeLineNum: searchActiveLineNum,
        stepBadgeText: searchStepBadgeText
    };

    document.getElementById('results').textContent = JSON.stringify(results);
});
</script>
</body>
</html>
"""

test_harness_path = os.path.join("tests", "_test_code_trace_harness.html")
with open(test_harness_path, "w", encoding="utf-8") as f:
    f.write(test_html_content)

chrome_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=5000",
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
    print("[FAIL] Could not extract test results from Chrome output")
    print("DOM snippet:", dom[:1000])
    sys.exit(1)

results = json.loads(m.group(1))

all_passed = True

print("\n--- Testing Sorting Visualizer Code Trace ---")
sort_res = results.get("sorting", {})
print(f"  Canvas Area ratio: {sort_res.get('areaRatio', 0):.2%}, Code Panel ratio: {sort_res.get('panelRatio', 0):.2%}")
if sort_res.get("ratioValid"):
    print("  [PASS] 80:20 ratio mathematically verified for sorting visualizer")
else:
    print(f"  [FAIL] Expected ~80% and ~20%, got {sort_res.get('areaRatio'):.2%} and {sort_res.get('panelRatio'):.2%}")
    all_passed = False

if sort_res.get("initialLineCount", 0) > 0 and sort_res.get("quickSortLineCount", 0) > 0:
    print(f"  [PASS] Pseudocode rendered ({sort_res.get('initialLineCount')} bubble lines -> {sort_res.get('quickSortLineCount')} quick lines on switch)")
else:
    print("  [FAIL] Pseudocode lines not rendered properly")
    all_passed = False

if sort_res.get("hasActiveLineOnStep"):
    print(f"  [PASS] Step execution successfully highlights active pseudocode line (line {sort_res.get('activeLineNum')}, badge: {sort_res.get('stepBadgeText')})")
else:
    print("  [FAIL] Active pseudocode line was not highlighted on step execution")
    all_passed = False

if sort_res.get("toggleCollapsed") and sort_res.get("toggleReExpanded"):
    print("  [PASS] Code panel collapse/expand toggle works smoothly")
else:
    print("  [FAIL] Toggle collapse/expand failed")
    all_passed = False

print("\n--- Testing Searching Visualizer Code Trace ---")
search_res = results.get("searching", {})
print(f"  Canvas Area ratio: {search_res.get('areaRatio', 0):.2%}, Code Panel ratio: {search_res.get('panelRatio', 0):.2%}")
if search_res.get("ratioValid"):
    print("  [PASS] 80:20 ratio mathematically verified for searching visualizer")
else:
    print(f"  [FAIL] Expected ~80% and ~20%, got {search_res.get('areaRatio'):.2%} and {search_res.get('panelRatio'):.2%}")
    all_passed = False

if search_res.get("initialLineCount", 0) > 0 and search_res.get("binarySearchLineCount", 0) > 0:
    print(f"  [PASS] Pseudocode rendered ({search_res.get('initialLineCount')} linear lines -> {search_res.get('binarySearchLineCount')} binary lines on switch)")
else:
    print("  [FAIL] Pseudocode lines not rendered properly")
    all_passed = False

if search_res.get("hasActiveLineOnStep"):
    print(f"  [PASS] Step execution successfully highlights active pseudocode line (line {search_res.get('activeLineNum')}, badge: {search_res.get('stepBadgeText')})")
else:
    print("  [FAIL] Active pseudocode line was not highlighted on step execution")
    all_passed = False

if all_passed:
    print("\n============================================================")
    print("ALL LIVE CODE TRACE (80:20 RATIO) VERIFICATIONS PASSED (100%)")
    print("============================================================")
    sys.exit(0)
else:
    print("\nSOME CHECKS FAILED")
    sys.exit(1)
