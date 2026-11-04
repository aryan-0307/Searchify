import subprocess
import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("ALGOVIZ AUTOMATED VERIFICATION SUITE")
print("=" * 60)

# 1. Algorithm Unit Tests
print("\n--- 1. Testing Algorithm Engine (Headless Chrome) ---")
cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/test_algorithms.html"
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
dom = res.stdout

m = re.search(r'<div id="summary"[^>]*>(.*?)</div>', dom)
if m:
    summary_text = re.sub(r'<[^>]+>', '', m.group(1))
    print("Summary:", summary_text)
    if "Failed: 0" in summary_text and "ALL TESTS PASSED" in summary_text:
        print("[PASS] All algorithm unit tests passed!")
    else:
        print("[FAIL] Some algorithm unit tests failed!")
        sys.exit(1)
else:
    print("[FAIL] Could not find test summary element.")
    sys.exit(1)

# 2. Page Integrity Verification
print("\n--- 2. Verifying Page Integrity & Markers ---")
proc = subprocess.run([sys.executable, "tests/verify_pages.py"], capture_output=True, text=True, encoding="utf-8")
print(proc.stdout)
if proc.returncode != 0:
    print("[FAIL] Page integrity checks failed.")
    sys.exit(1)

# 3. Playground Features Verification
print("\n--- 3. Verifying Restructured Visualizer Features ---")
proc = subprocess.run([sys.executable, "tests/verify_playground_features.py"], capture_output=True, text=True, encoding="utf-8")
print(proc.stdout)
if proc.returncode != 0:
    print("[FAIL] Feature verification failed.")
    sys.exit(1)

# 4. Console Errors Check
print("\n--- 4. Checking Browser Console & Runtime Errors ---")
proc = subprocess.run([sys.executable, "tests/check_console_errors.py"], capture_output=True, text=True, encoding="utf-8")
print(proc.stdout)
if proc.returncode != 0:
    print("[FAIL] Browser console runtime error check failed.")
    sys.exit(1)

# 5. Center Screen Notification Verification
print("\n--- 5. Verifying Center Screen Notifications ---")
proc = subprocess.run([sys.executable, "tests/verify_center_notification.py"], capture_output=True, text=True, encoding="utf-8")
print(proc.stdout)
if proc.returncode != 0:
    print("[FAIL] Center screen notification checks failed.")
    sys.exit(1)

# 6. Homepage Transformation Verification
print("\n--- 6. Verifying Homepage Playground Transformation ---")
proc = subprocess.run([sys.executable, "tests/verify_homepage.py"], capture_output=True, text=True, encoding="utf-8")
print(proc.stdout)
if proc.returncode != 0:
    print("[FAIL] Homepage verification failed.")
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY (100% PASS RATE)")
print("=" * 60)
