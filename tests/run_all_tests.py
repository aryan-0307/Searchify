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

# 7. Sticky Navbar & Icon Animation Verification
print("\n--- 7. Verifying Navbar Background Merge & Fast Icon Transition ---")
proc = subprocess.run([sys.executable, "tests/verify_nav_animation.py"], capture_output=True, text=True, encoding="utf-8")
print(proc.stdout)
if proc.returncode != 0:
    print("[FAIL] Navbar animation verification failed.")
    sys.exit(1)

# 8. Zero Layout Shift & Hysteresis Verification
print("\n--- 8. Verifying Zero Layout Shift & Scroll Hysteresis ---")
proc_shift = subprocess.run([sys.executable, "tests/verify_zero_layout_shift.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_shift.stdout)
if proc_shift.returncode != 0:
    print("[FAIL] Zero layout shift verification failed.")
    sys.exit(1)

proc_hyst = subprocess.run([sys.executable, "tests/test_hysteresis.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_hyst.stdout)
if proc_hyst.returncode != 0:
    print("[FAIL] Scroll hysteresis verification failed.")
    sys.exit(1)

# 9. Page Refresh & Deep-Link State Sync Verification
print("\n--- 9. Verifying Refresh Sync & Transition Suppression ---")
proc_refresh = subprocess.run([sys.executable, "tests/test_refresh_sync.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_refresh.stdout)
if proc_refresh.returncode != 0:
    print("[FAIL] Page refresh sync verification failed.")
    sys.exit(1)

# 10. Full-Width Navbar & Phone Variations Verification
print("\n--- 10. Verifying Full-Width Navbar & Phone Variations ---")
proc_mobile = subprocess.run([sys.executable, "tests/verify_mobile_nav.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_mobile.stdout)
if proc_mobile.returncode != 0:
    print("[FAIL] Full-width & phone variations verification failed.")
    sys.exit(1)

# 11. Staggered 'Glide Then Fade Into Box' Motion Verification
print("\n--- 11. Verifying Staggered 'Glide Then Fade Into Box' Brand Motion ---")
proc_glide = subprocess.run([sys.executable, "tests/verify_glide_fade.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_glide.stdout)
if proc_glide.returncode != 0:
    print("[FAIL] 'Glide then fade into box' brand motion verification failed.")
    sys.exit(1)

# 12. Numerical Speed Settings (1x - 6x) Verification
print("\n--- 12. Verifying Numerical Speed Settings (1x - 6x) ---")
proc_speed = subprocess.run([sys.executable, "tests/verify_numerical_speeds.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_speed.stdout)
if proc_speed.returncode != 0:
    print("[FAIL] Numerical speed settings verification failed.")
    sys.exit(1)

# 13. Mobile Visualizer Array Index Visibility Verification
print("\n--- 13. Verifying Mobile Visualizer Array Index Visibility ---")
proc_idx = subprocess.run([sys.executable, "tests/verify_mobile_indexes.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_idx.stdout)
if proc_idx.returncode != 0:
    print("[FAIL] Mobile visualizer index visibility verification failed.")
    sys.exit(1)

# 14. Dynamic Array Size Slider (Live Resizing) Verification
print("\n--- 14. Verifying Dynamic Array Size Slider (Live Resizing) ---")
proc_size = subprocess.run([sys.executable, "tests/verify_live_size_slider.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_size.stdout)
if proc_size.returncode != 0:
    print("[FAIL] Dynamic array size slider verification failed.")
    sys.exit(1)

# 15. Gravity Drop & Elastic Bounce Physics Verification
print("\n--- 15. Verifying Gravity Drop & Elastic Bounce Physics ---")
proc_gravity = subprocess.run([sys.executable, "tests/verify_gravity_animation.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_gravity.stdout)
if proc_gravity.returncode != 0:
    print("[FAIL] Gravity drop & elastic bounce verification failed.")
    sys.exit(1)

# 16. Semantic HTML5 Tags & SEO Optimization Verification
print("\n--- 16. Verifying Semantic HTML5 Tags & SEO Optimization ---")
proc_seo = subprocess.run([sys.executable, "tests/verify_semantic_seo.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_seo.stdout)
if proc_seo.returncode != 0:
    print("[FAIL] Semantic HTML5 tags & SEO verification failed.")
    sys.exit(1)

# 17. Live Code Trace (80:20 Ratio) Visualizer Panel Verification
print("\n--- 17. Verifying Live Code Trace (80:20 Ratio) Visualizer Panel ---")
proc_trace = subprocess.run([sys.executable, "tests/verify_code_trace_panel.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_trace.stdout)
if proc_trace.returncode != 0:
    print("[FAIL] Live code trace verification failed.")
    sys.exit(1)

# 18. Visualization-to-Pseudocode Synchronization Verification
print("\n--- 18. Verifying Visualization-to-Pseudocode Synchronization ---")
proc_sync = subprocess.run([sys.executable, "tests/verify_pseudocode_sync.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_sync.stdout)
if proc_sync.returncode != 0:
    print("[FAIL] Pseudocode synchronization verification failed.")
    sys.exit(1)

# 19. Visualizer Controls Layout (Center Play/Pause & Right Settings) Verification
print("\n--- 19. Verifying Visualizer Controls Layout (Center Play/Pause & Right Settings) ---")
proc_layout = subprocess.run([sys.executable, "tests/verify_controls_layout.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_layout.stdout)
if proc_layout.returncode != 0:
    print("[FAIL] Visualizer controls layout verification failed.")
    sys.exit(1)

# 20. Homepage Hero Cleanup & Duplicate Removal Verification
print("\n--- 20. Verifying Homepage Hero Cleanup & Duplicate Removal ---")
proc_cleanup = subprocess.run([sys.executable, "tests/verify_homepage_cleanup.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_cleanup.stdout)
if proc_cleanup.returncode != 0:
    print("[FAIL] Homepage hero cleanup verification failed.")
    sys.exit(1)

# 21. Mobile Visualizer Layout & Stacked Controls Verification
print("\n--- 21. Verifying Mobile Visualizer Layout & Stacked Controls ---")
proc_mobile = subprocess.run([sys.executable, "tests/verify_mobile_visualizer_layout.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_mobile.stdout)
if proc_mobile.returncode != 0:
    print("[FAIL] Mobile visualizer layout verification failed.")
    sys.exit(1)

# 22. Visualizer Header Title & Subtitle Centering Verification
print("\n--- 22. Verifying Visualizer Header Title & Subtitle Centering ---")
proc_header = subprocess.run([sys.executable, "tests/verify_header_title_centering.py"], capture_output=True, text=True, encoding="utf-8")
print(proc_header.stdout)
if proc_header.returncode != 0:
    print("[FAIL] Visualizer header title centering verification failed.")
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY (100% PASS RATE)")
print("=" * 60)
