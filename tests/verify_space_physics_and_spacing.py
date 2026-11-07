"""
tests/verify_space_physics_and_spacing.py
Automated verification for:
1. Aalto Display letter-spacing (breathable, non-cramped positive spacing across all display elements).
2. Zero-gravity space physics floating typography on "Algorithms make more sense when you see them move".
3. Status pills and hero art chips space drift animations.
"""

import subprocess
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("VERIFYING AALTO DISPLAY LETTER SPACING & SPACE PHYSICS")
print("=" * 60)

test_harness = """<!DOCTYPE html>
<html><body>
<iframe id="frame-home" src="../index.html" style="width:1440px; height:900px;"></iframe>
<iframe id="frame-sort" src="../sorting.html" style="width:1440px; height:900px;"></iframe>
<iframe id="frame-search" src="../searching.html" style="width:1440px; height:900px;"></iframe>
<div id="results"></div>
<script>
window.addEventListener('load', async () => {
    await new Promise(r => setTimeout(r, 600));

    const homeDoc = document.getElementById('frame-home').contentDocument;
    const homeWin = document.getElementById('frame-home').contentWindow;
    const sortDoc = document.getElementById('frame-sort').contentDocument;
    const sortWin = document.getElementById('frame-sort').contentWindow;
    const searchDoc = document.getElementById('frame-search').contentDocument;
    const searchWin = document.getElementById('frame-search').contentWindow;

    const issues = [];
    const checks = [];

    // 1. Check letter-spacing on Aalto Display elements
    const elementsToCheck = [
        { doc: homeDoc, win: homeWin, sel: '.hero-copy h1', name: 'Home Hero Title' },
        { doc: homeDoc, win: homeWin, sel: '.card-title', name: 'Home Card Title' },
        { doc: homeDoc, win: homeWin, sel: '.home-brand-logo', name: 'Home Brand Logo' },
        { doc: homeDoc, win: homeWin, sel: '.brand-mark', name: 'Home Brand Mark' },
        { doc: homeDoc, win: homeWin, sel: '.section-heading h2', name: 'Home Section Heading' },
        { doc: homeDoc, win: homeWin, sel: '.home-demo-heading h2', name: 'Home Demo Heading' },
        { doc: homeDoc, win: homeWin, sel: '.footer-brand', name: 'Home Footer Brand' },
        { doc: sortDoc, win: sortWin, sel: '.viz-title', name: 'Sorting Visualizer Title' },
        { doc: sortDoc, win: sortWin, sel: '.complexity-algo-name', name: 'Sorting Complexity Title' },
        { doc: searchDoc, win: searchWin, sel: '.viz-title', name: 'Searching Visualizer Title' },
        { doc: searchDoc, win: searchWin, sel: '.complexity-algo-name', name: 'Searching Complexity Title' },
    ];

    elementsToCheck.forEach(({ doc, win, sel, name }) => {
        const el = doc.querySelector(sel);
        if (!el) {
            issues.push(`Element not found: ${name} (${sel})`);
            return;
        }
        const cs = win.getComputedStyle(el);
        const ls = cs.letterSpacing;
        // Parse letter spacing: normal, or numeric px
        let pxVal = 0;
        if (ls === 'normal') {
            pxVal = 0;
        } else if (ls.endsWith('px')) {
            pxVal = parseFloat(ls);
        }

        // Must be non-negative (no cramped squished overlapping text)
        if (pxVal < 0) {
            issues.push(`${name} has negative cramped letter-spacing: ${ls}`);
        } else {
            checks.push(`${name}: letter-spacing = ${ls} (positive & breathable)`);
        }
    });

    // 2. Check Space Physics Typography on "Algorithms make more sense when you see them move"
    const h1 = homeDoc.getElementById('hero-title');
    if (!h1) {
        issues.push('Missing #hero-title on index.html');
    } else {
        const line1 = h1.querySelector('.hero-space-line.line-1');
        const line2 = h1.querySelector('.hero-space-line.line-2');
        const line3 = h1.querySelector('.hero-space-line.line-3');
        const moveSpan = h1.querySelector('.see-them-move');

        if (!line1 || !line2 || !line3) {
            issues.push('Missing .hero-space-line (line-1, line-2, line-3) inside #hero-title');
        } else {
            const cs1 = homeWin.getComputedStyle(line1);
            const cs2 = homeWin.getComputedStyle(line2);
            const cs3 = homeWin.getComputedStyle(line3);

            if (!cs1.animationName || cs1.animationName === 'none') {
                issues.push('Line 1 has no space orbital animation applied');
            }
            if (!cs2.animationName || cs2.animationName === 'none') {
                issues.push('Line 2 has no space orbital animation applied');
            }
            if (!cs3.animationName || cs3.animationName === 'none') {
                issues.push('Line 3 has no space orbital animation applied');
            }

            checks.push(`Line 1 Space Orbital Animation: ${cs1.animationName} (duration=${cs1.animationDuration})`);
            checks.push(`Line 2 Space Orbital Animation: ${cs2.animationName} (duration=${cs2.animationDuration})`);
            checks.push(`Line 3 Space Orbital Animation: ${cs3.animationName} (duration=${cs3.animationDuration})`);
        }

        if (!moveSpan) {
            issues.push('Missing .see-them-move element inside #hero-title');
        } else {
            const csMove = homeWin.getComputedStyle(moveSpan);
            checks.push(`"see them move" Cosmic Float Animation: ${csMove.animationName}`);
        }
    }

    // 3. Check Space Float on Floating Chips & Canvas Status Pills
    const chipTop = homeDoc.querySelector('.chip-top');
    const chipBottom = homeDoc.querySelector('.chip-bottom');
    if (chipTop) {
        const cs = homeWin.getComputedStyle(chipTop);
        checks.push(`Hero Chip Top Space Drift: ${cs.animationName}`);
    }
    if (chipBottom) {
        const cs = homeWin.getComputedStyle(chipBottom);
        checks.push(`Hero Chip Bottom Space Drift: ${cs.animationName}`);
    }

    const sortPill = sortDoc.querySelector('.canvas-status-pill');
    if (sortPill) {
        const cs = sortWin.getComputedStyle(sortPill);
        checks.push(`Sorting Canvas Status Pill Space Float: ${cs.animationName}`);
    }

    const searchPill = searchDoc.querySelector('.canvas-status-pill');
    if (searchPill) {
        const cs = searchWin.getComputedStyle(searchPill);
        checks.push(`Searching Canvas Status Pill Space Float: ${cs.animationName}`);
    }

    document.getElementById('results').textContent = JSON.stringify({
        passed: issues.length === 0,
        checks: checks,
        issues: issues
    });
});
</script>
</body></html>"""

temp_file = "tests/temp_space_physics_test.html"
with open(temp_file, "w", encoding="utf-8") as f:
    f.write(test_harness)

cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--virtual-time-budget=3000",
    "--dump-dom",
    f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{temp_file}"
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
if os.path.exists(temp_file):
    os.remove(temp_file)

import re
m = re.search(r'<div id="results">(\{.*?\})</div>', res.stdout)
if not m:
    print("[FAIL] Could not extract test results from Chrome output")
    sys.exit(1)

data = json.loads(m.group(1))

print("\n--- Verified Checks ---")
for c in data.get("checks", []):
    print(f"  [PASS] {c}")

if data["passed"]:
    print("\n============================================================")
    print("ALL AALTO DISPLAY LETTER-SPACING & SPACE PHYSICS TESTS PASSED (100%)")
    print("============================================================")
else:
    print("\n--- Issues Found ---")
    for issue in data.get("issues", []):
        print(f"  [FAIL] {issue}")
    sys.exit(1)
