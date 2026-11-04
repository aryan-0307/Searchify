import subprocess
import sys
import re

pages = [
    ("index.html", ["home-container", "Searching", "Sorting"]),
    ("sorting.html", ["algorithm-select", "generate-btn", "visualization-area", "complexity-display", "viz-content-container", "interactive-row"]),
    ("searching.html", ["algorithm-select", "generate-btn", "target-input", "visualization-area", "complexity-display", "viz-content-container", "interactive-row"])
]

all_passed = True

for page, expected_markers in pages:
    url = f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{page}"
    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--dump-dom",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    dom = res.stdout
    print(f"Checking {page}...")
    for marker in expected_markers:
        if marker in dom:
            print(f"  [PASS] Found marker: '{marker}'")
        else:
            print(f"  [FAIL] Missing marker: '{marker}'")
            all_passed = False

if all_passed:
    print("\nALL PAGE INTEGRITY CHECKS PASSED!")
    sys.exit(0)
else:
    print("\nSOME CHECKS FAILED!")
    sys.exit(1)
