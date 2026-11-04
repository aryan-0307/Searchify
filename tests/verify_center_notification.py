import subprocess
import sys
import time
import re

sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("ALGOVIZ CENTER SCREEN NOTIFICATION TEST SUITE")
print("=" * 60)

# 1. Run test_notifications.html with Chrome headless
print("\n--- 1. Testing Notification Unit Specs & Computed Styles ---")
cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--virtual-time-budget=3000",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/test_notifications.html"
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
dom = res.stdout

m = re.search(r'<div id="summary"[^>]*>(.*?)</div>', dom)
if m:
    summary_text = re.sub(r'<[^>]+>', '', m.group(1))
    print("Summary:", summary_text)
    if "Failed: 0" in summary_text and "ALL NOTIFICATION TESTS PASSED" in summary_text:
        print("[PASS] All notification specs & computed styles passed!")
    else:
        print("[FAIL] Some notification tests failed:")
        for line in dom.splitlines():
            if "FAIL:" in line or "PASS:" in line:
                print(" ", line.strip())
        sys.exit(1)
else:
    print("[FAIL] Could not find test summary element.")
    for line in dom.splitlines():
        if "FAIL:" in line or "PASS:" in line:
            print(" ", line.strip())
    sys.exit(1)

# 2. Verify sorting.html live click interaction via Chrome evaluation
print("\n--- 2. Verifying Sorting Visualizer Live Center Notification ---")
# Create a test harness HTML that loads sorting.html and clicks generate-btn
harness_sorting = """<!DOCTYPE html>
<html><body>
<iframe id="frame" src="../sorting.html" style="width:1000px; height:800px;"></iframe>
<script>
window.onload = function() {
    var win = document.getElementById('frame').contentWindow;
    var doc = win.document;
    doc.getElementById('generate-btn').click();
    var notif = doc.getElementById('notification');
    var style = win.getComputedStyle(notif);
    var pass = notif.classList.contains('show') && 
               notif.textContent.includes('New array generated') &&
               style.position === 'fixed' &&
               parseFloat(style.top) <= 24 &&
               Math.abs(parseFloat(style.left) - win.document.documentElement.clientWidth / 2) <= 3;
    var status = pass ? 'PASS' : 'FAIL';
    document.body.innerHTML += '<div id="sorting-result">' + status + ': text="' + notif.textContent + '", pos=' + style.position + ', top=' + style.top + '</div>';
};
</script>
</body></html>"""
with open("tests/temp_test_sorting_click.html", "w", encoding="utf-8") as f:
    f.write(harness_sorting)

cmd_sorting = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--virtual-time-budget=2000",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/temp_test_sorting_click.html"
]
res_sorting = subprocess.run(cmd_sorting, capture_output=True, text=True, encoding="utf-8", errors="ignore")
if "PASS:" in res_sorting.stdout:
    print("[PASS] Sorting Visualizer: Clicking 'Generate Array' displays centered notification!")
else:
    print("[FAIL] Sorting Visualizer notification failed:", res_sorting.stdout)
    sys.exit(1)

# 3. Verify searching.html live click interaction
print("\n--- 3. Verifying Searching Visualizer Live Center Notification ---")
harness_searching = """<!DOCTYPE html>
<html><body>
<iframe id="frame" src="../searching.html" style="width:1000px; height:800px;"></iframe>
<script>
window.onload = function() {
    var win = document.getElementById('frame').contentWindow;
    var doc = win.document;
    doc.getElementById('generate-btn').click();
    var notif = doc.getElementById('notification');
    var style = win.getComputedStyle(notif);
    var pass = notif.classList.contains('show') && 
               notif.textContent.includes('New array generated') &&
               style.position === 'fixed' &&
               parseFloat(style.top) <= 24 &&
               Math.abs(parseFloat(style.left) - win.document.documentElement.clientWidth / 2) <= 3;
    var status = pass ? 'PASS' : 'FAIL';
    document.body.innerHTML += '<div id="searching-result">' + status + ': text="' + notif.textContent + '", pos=' + style.position + ', top=' + style.top + '</div>';
};
</script>
</body></html>"""
with open("tests/temp_test_searching_click.html", "w", encoding="utf-8") as f:
    f.write(harness_searching)

cmd_searching = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--virtual-time-budget=2000",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/temp_test_searching_click.html"
]
res_searching = subprocess.run(cmd_searching, capture_output=True, text=True, encoding="utf-8", errors="ignore")
if "PASS:" in res_searching.stdout:
    print("[PASS] Searching Visualizer: Clicking 'Generate Array' displays centered notification!")
else:
    print("[FAIL] Searching Visualizer notification failed:", res_searching.stdout)
    sys.exit(1)

# 4. Verify searching.html empty apply click interaction
print("\n--- 4. Verifying Searching Visualizer Empty Apply Notification ---")
harness_searching_empty = """<!DOCTYPE html>
<html><body>
<iframe id="frame" src="../searching.html" style="width:1000px; height:800px;"></iframe>
<script>
window.onload = function() {
    var win = document.getElementById('frame').contentWindow;
    var doc = win.document;
    doc.getElementById('custom-array').value = '';
    doc.getElementById('apply-custom-btn').click();
    var notif = doc.getElementById('notification');
    var pass = notif.classList.contains('show') && 
               notif.textContent.includes('No data is given. Tap on Generate for sample input.') &&
               notif.classList.contains('info');
    var status = pass ? 'PASS' : 'FAIL';
    document.body.innerHTML += '<div id="searching-empty-result">' + status + ': text="' + notif.textContent + '"</div>';
};
</script>
</body></html>"""
with open("tests/temp_test_searching_empty.html", "w", encoding="utf-8") as f:
    f.write(harness_searching_empty)

cmd_searching_empty = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--virtual-time-budget=2000",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/temp_test_searching_empty.html"
]
res_searching_empty = subprocess.run(cmd_searching_empty, capture_output=True, text=True, encoding="utf-8", errors="ignore")
if "PASS:" in res_searching_empty.stdout:
    print("[PASS] Searching Visualizer: Clicking 'Apply' with empty input displays 'No data is given' guidance notification!")
else:
    print("[FAIL] Searching Visualizer empty apply notification failed:", res_searching_empty.stdout)
    sys.exit(1)

# 5. Verify sorting.html empty apply click interaction
print("\n--- 5. Verifying Sorting Visualizer Empty Apply Notification ---")
harness_sorting_empty = """<!DOCTYPE html>
<html><body>
<iframe id="frame" src="../sorting.html" style="width:1000px; height:800px;"></iframe>
<script>
window.onload = function() {
    var win = document.getElementById('frame').contentWindow;
    var doc = win.document;
    doc.getElementById('custom-array').value = '';
    doc.getElementById('apply-custom-btn').click();
    var notif = doc.getElementById('notification');
    var pass = notif.classList.contains('show') && 
               notif.textContent.includes('No data is given. Tap on Generate for sample input.') &&
               notif.classList.contains('info');
    var status = pass ? 'PASS' : 'FAIL';
    document.body.innerHTML += '<div id="sorting-empty-result">' + status + ': text="' + notif.textContent + '"</div>';
};
</script>
</body></html>"""
with open("tests/temp_test_sorting_empty.html", "w", encoding="utf-8") as f:
    f.write(harness_sorting_empty)

cmd_sorting_empty = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--virtual-time-budget=2000",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/temp_test_sorting_empty.html"
]
res_sorting_empty = subprocess.run(cmd_sorting_empty, capture_output=True, text=True, encoding="utf-8", errors="ignore")
if "PASS:" in res_sorting_empty.stdout:
    print("[PASS] Sorting Visualizer: Clicking 'Apply' with empty input displays 'No data is given' guidance notification!")
else:
    print("[FAIL] Sorting Visualizer empty apply notification failed:", res_sorting_empty.stdout)
    sys.exit(1)

# Clean up temporary harnesses
import os
try:
    os.remove("tests/temp_test_sorting_click.html")
    os.remove("tests/temp_test_searching_click.html")
    os.remove("tests/temp_test_searching_empty.html")
    os.remove("tests/temp_test_sorting_empty.html")
except Exception:
    pass

print("\n" + "=" * 60)
print("ALL CENTER NOTIFICATION VERIFICATIONS COMPLETED (100% PASS)")
print("=" * 60)
