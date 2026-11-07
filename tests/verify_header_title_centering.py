"""
tests/verify_header_title_centering.py
Automated verification for visualizer header title and subtitle centering:
- Verifies that .viz-header-title-group (title & subtitle) is centered in the header section
- Verifies text-align: center and align-items: center across desktop and mobile viewports
- Verifies specific text contents on searching.html and sorting.html
"""

import subprocess
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("VERIFYING VISUALIZER HEADER TITLE & SUBTITLE CENTERING")
print("=" * 60)

pages = [
    ("searching.html", "Searching Visualizer", "Explore search paths step by step"),
    ("sorting.html", "Sorting Visualizer", "Watch algorithms come to life")
]

probe_script = """
window.addEventListener('load', () => {
    const header = document.querySelector('.viz-header');
    const titleGroup = document.querySelector('.viz-header-title-group');
    const title = document.querySelector('.viz-title');
    const subtitle = document.querySelector('.viz-subtitle');
    const backBtn = document.querySelector('.back-btn');
    const controls = document.querySelector('.viz-header-controls');
    
    const hRect = header ? header.getBoundingClientRect() : null;
    const tRect = titleGroup ? titleGroup.getBoundingClientRect() : null;
    
    const hCenter = hRect ? (hRect.left + hRect.right) / 2 : 0;
    const tCenter = tRect ? (tRect.left + tRect.right) / 2 : 0;
    const diff = Math.abs(hCenter - tCenter);
    
    const titleCS = title ? window.getComputedStyle(title) : null;
    const subCS = subtitle ? window.getComputedStyle(subtitle) : null;
    
    const res = {
        headerWidth: hRect ? Math.round(hRect.width) : null,
        centerDiff: Math.round(diff),
        isCentered: diff <= 3,
        titleText: title ? title.innerText.trim() : '',
        subtitleText: subtitle ? subtitle.innerText.trim() : '',
        textAlignTitle: titleCS ? titleCS.textAlign : '',
        textAlignSubtitle: subCS ? subCS.textAlign : ''
    };
    
    const out = document.createElement('div');
    out.id = 'header-center-probe';
    out.textContent = JSON.stringify(res);
    document.body.appendChild(out);
});
"""

for page, expected_title, expected_sub in pages:
    print(f"\n--- Checking {page} ---")
    raw_html = open(page, encoding="utf-8").read()
    probe_html = raw_html.replace("</body>", f"<script>{probe_script}</script></body>")
    temp_file = f"temp_hc_{page}"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(probe_html)
        
    try:
        for vw in [1440, 768, 375]:
            cmd = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                "--headless=new", "--no-sandbox", "--disable-gpu",
                f"--window-size={vw},800",
                "--allow-file-access-from-files",
                "--virtual-time-budget=2000",
                "--dump-dom",
                f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{temp_file}"
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
            assert '<div id="header-center-probe">' in proc.stdout, f"Missing probe output for {page} at {vw}px"
            data = json.loads(proc.stdout.split('<div id="header-center-probe">')[1].split("</div>")[0])
            
            assert expected_title in data["titleText"], f"Expected title '{expected_title}', got '{data['titleText']}'"
            assert expected_sub in data["subtitleText"], f"Expected subtitle '{expected_sub}', got '{data['subtitleText']}'"
            assert data["textAlignTitle"] == "center", f"Expected title textAlign 'center', got '{data['textAlignTitle']}'"
            assert data["textAlignSubtitle"] == "center", f"Expected subtitle textAlign 'center', got '{data['textAlignSubtitle']}'"
            assert data["isCentered"], f"{page} at {vw}px: Title group not centered! diff={data['centerDiff']}px"
            
            print(f"  [PASS] {vw}px: Title '{data['titleText']}' & Subtitle '{data['subtitleText']}' centered (diff={data['centerDiff']}px, text-align=center)")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

print("\n" + "=" * 60)
print("ALL HEADER TITLE CENTERING VERIFICATIONS PASSED (100%)")
print("=" * 60)

