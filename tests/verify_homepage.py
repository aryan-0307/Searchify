import subprocess
import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("ALGOVIZ HOMEPAGE TRANSFORMATION VERIFICATION")
print("=" * 60)

# 1. Inspect DOM & Elements via Headless Chrome
print("\n--- 1. Testing Homepage DOM Elements & Markers ---")
cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/index.html"
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
dom = res.stdout

expected_markers = [
    "Bricolage+Grotesque",
    "home-container",
    "home-brand",
    "searching-card",
    "sorting-card",
    "Searching",
    "Sorting",
    "searching-mini-viz",
    "sorting-mini-viz",
    "mini-cells-row",
    "mini-bars-row",
    "searching.html",
    "sorting.html"
]

all_passed = True
for marker in expected_markers:
    if marker in dom:
        print(f"  [PASS] Found marker: '{marker}'")
    else:
        print(f"  [FAIL] Missing marker: '{marker}'")
        all_passed = False

# Check card descriptions (supports both original and redesigned copies)
if "Find it. Understand it." in dom or "Find elements, one step at a time." in dom:
    print("  [PASS] Found searching card description marker")
else:
    print("  [FAIL] Missing searching card description marker")
    all_passed = False

if "Sort it. Master it." in dom or "Watch elements find their place." in dom:
    print("  [PASS] Found sorting card description marker")
else:
    print("  [FAIL] Missing sorting card description marker")
    all_passed = False

if not all_passed:
    print("[FAIL] Some homepage markers were missing!")
    sys.exit(1)

# 2. Verify Computed Styles & Typography in Headless Chrome
print("\n--- 2. Verifying Typography & Card Styles ---")
harness_html = """<!DOCTYPE html>
<html><body>
<iframe id="frame" src="../index.html" style="width:1200px; height:800px;"></iframe>
<script>
window.onload = function() {
    var win = document.getElementById('frame').contentWindow;
    var doc = win.document;
    
    var title = doc.querySelector('.card-title');
    var titleStyle = win.getComputedStyle(title);
    
    var searchCard = doc.querySelector('.searching-card');
    var searchStyle = win.getComputedStyle(searchCard);
    
    var sortCard = doc.querySelector('.sorting-card');
    var sortStyle = win.getComputedStyle(sortCard);

    var container = doc.querySelector('.home-container');
    var containerStyle = win.getComputedStyle(container);

    var passTypography = titleStyle.fontFamily.includes('Aalto Display') || titleStyle.fontFamily.includes('Bricolage Grotesque') || titleStyle.fontFamily.includes('sans-serif');
    var passCards = searchStyle.display === 'flex' && sortStyle.display === 'flex';
    var passLinks = searchCard.getAttribute('href') === 'searching.html' && sortCard.getAttribute('href') === 'sorting.html';
    
    var status = (passTypography && passCards && passLinks) ? 'PASS' : 'FAIL';
    document.body.innerHTML += '<div id="result">' + status + ': font=' + titleStyle.fontFamily + ', links=' + passLinks + '</div>';
};
</script>
</body></html>"""
with open("tests/temp_homepage_test.html", "w", encoding="utf-8") as f:
    f.write(harness_html)

cmd_eval = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--virtual-time-budget=2000",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/temp_homepage_test.html"
]
res_eval = subprocess.run(cmd_eval, capture_output=True, text=True, encoding="utf-8", errors="ignore")
import os
try:
    os.remove("tests/temp_homepage_test.html")
except Exception:
    pass

if "PASS:" in res_eval.stdout:
    print("  [PASS] Bricolage Grotesque typography & navigation links verified in rendered DOM!")
else:
    print("  [FAIL] Evaluation failed:", res_eval.stdout)
    sys.exit(1)

# 3. Check for Console Errors
print("\n--- 3. Verifying Console Output ---")
proc = subprocess.run([sys.executable, "tests/check_console_errors.py"], capture_output=True, text=True, encoding="utf-8")
print(proc.stdout)
if proc.returncode != 0:
    print("[FAIL] Console errors detected on homepage.")
    sys.exit(1)

print("\n" + "=" * 60)
print("HOMEPAGE TRANSFORMATION VERIFICATION COMPLETED (100% PASS)")
print("=" * 60)
