import subprocess
import sys

pages = [
    ("sorting.html", [
        "viz-subtitle",
        "controls-cluster",
        "btn-play-prominent",
        "canvas-status-pill",
        "completion-banner",
        "interactive-row",
        "explanation-card",
        "counter-card",
        "complexity-section-full",
        "complexity-cards-grid"
    ]),
    ("searching.html", [
        "viz-subtitle",
        "controls-cluster",
        "btn-play-prominent",
        "canvas-status-pill",
        "completion-banner",
        "interactive-row",
        "explanation-card",
        "counter-card",
        "complexity-section-full",
        "complexity-cards-grid"
    ])
]

all_passed = True

for page, markers in pages:
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
    print(f"Testing playground features on {page}...")
    for marker in markers:
        if marker in dom:
            print(f"  [PASS] Found playground element: '{marker}'")
        else:
            print(f"  [FAIL] Missing playground element: '{marker}'")
            all_passed = False

if all_passed:
    print("\nALL PLAYGROUND FEATURE VERIFICATIONS PASSED!")
    sys.exit(0)
else:
    sys.exit(1)
