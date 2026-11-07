"""
tests/verify_font_family.py
Automated verification that Aalto Display is applied across headings, brand elements,
card titles, and visualizer page titles on index.html, sorting.html, and searching.html.
"""

import subprocess
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("VERIFYING AALTO DISPLAY FONT APPLICATION")
print("=" * 60)

test_targets = [
    {
        "page": "index.html",
        "elements": [
            (".hero-copy h1", "hero title"),
            (".card-title", "card title"),
            (".home-brand-logo", "brand logo"),
            (".brand-mark", "brand mark"),
            (".section-heading h2", "section heading"),
            (".home-demo-heading h2", "demo heading")
        ]
    },
    {
        "page": "sorting.html",
        "elements": [
            (".viz-title", "visualizer title"),
            (".complexity-algo-name", "complexity title")
        ]
    },
    {
        "page": "searching.html",
        "elements": [
            (".viz-title", "visualizer title"),
            (".complexity-algo-name", "complexity title")
        ]
    }
]

probe_script = """
window.addEventListener('load', () => {
    const selectors = %SELECTORS%;
    const results = selectors.map(sel => {
        const el = document.querySelector(sel);
        const cs = el ? window.getComputedStyle(el) : null;
        return {
            selector: sel,
            found: !!el,
            fontFamily: cs ? cs.fontFamily : null
        };
    });
    const out = document.createElement('div');
    out.id = 'font-probe-output';
    out.textContent = JSON.stringify(results);
    document.body.appendChild(out);
});
"""

for target in test_targets:
    page = target["page"]
    print(f"\n--- Checking {page} ---")
    selectors = [item[0] for item in target["elements"]]
    
    raw_html = open(page, encoding="utf-8").read()
    script = probe_script.replace("%SELECTORS%", json.dumps(selectors))
    probe_html = raw_html.replace("</body>", f"<script>{script}</script></body>")
    temp_file = f"temp_font_{page}"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(probe_html)
        
    try:
        cmd = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "--headless=new", "--no-sandbox", "--disable-gpu",
            "--window-size=1440,900",
            "--allow-file-access-from-files",
            "--virtual-time-budget=2000",
            "--dump-dom",
            f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{temp_file}"
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        assert '<div id="font-probe-output">' in proc.stdout, f"Missing probe output for {page}"
        results = json.loads(proc.stdout.split('<div id="font-probe-output">')[1].split("</div>")[0])
        
        for item, (sel, label) in zip(results, target["elements"]):
            assert item["found"], f"Element '{sel}' not found in {page}"
            ff = item["fontFamily"]
            assert "Aalto Display" in ff, f"Expected 'Aalto Display' in {sel} ({label}) fontFamily, got '{ff}'"
            print(f"  [PASS] {label} ({sel}) -> fontFamily: {ff}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

print("\n" + "=" * 60)
print("ALL AALTO DISPLAY FONT VERIFICATIONS PASSED (100%)")
print("=" * 60)

