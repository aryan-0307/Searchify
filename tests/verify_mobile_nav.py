import subprocess
import json
import os
import sys

viewports = [
    (320, 568, "iPhone SE 1st gen (320px)"),
    (360, 740, "Galaxy S8/S9/S10 compact (360px)"),
    (375, 667, "iPhone SE / 8 (375px)"),
    (390, 844, "iPhone 13 / 14 / 15 / 16 (390px)"),
    (412, 915, "Samsung Galaxy S23 / Pixel 7 (412px)"),
    (430, 932, "iPhone 14/15/16 Pro Max (430px)"),
    (768, 1024, "iPad / Tablet (768px)"),
    (1280, 800, "Laptop (1280px)"),
    (1920, 1080, "Desktop Full HD (1920px)")
]

all_passed = True
print("=" * 60)
print("TESTING FULL-WIDTH NAVBAR & MOBILE PHONE VARIATIONS")
print("=" * 60)

harness_template = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0;">
<iframe id="frame" src="../index.html" style="width: {w}px; height: {h}px; border:0; display:block;"></iframe>
<div id="results"></div>
<script>
window.addEventListener('load', () => {{
    const frame = document.getElementById('frame');
    const doc = frame.contentDocument;
    const win = frame.contentWindow;

    const nav = doc.getElementById('home-nav');
    const navRect = nav.getBoundingClientRect();
    const docClientW = doc.documentElement.clientWidth;
    const docScrollW = doc.documentElement.scrollWidth;

    const brand = nav.querySelector('.home-brand');
    const brandRect = brand.getBoundingClientRect();

    const cta = nav.querySelector('.nav-cta');
    const ctaRect = cta.getBoundingClientRect();

    const result = {{
        viewportWidth: {w},
        clientW: docClientW,
        navWidth: navRect.width,
        docScrollWidth: docScrollW,
        coversCompleteWidth: Math.abs(navRect.width - docClientW) <= 1,
        hasHorizontalOverflow: docScrollW > docClientW + 1,
        brandVisible: brandRect.width > 0 && brandRect.height > 0,
        ctaVisible: ctaRect.width > 0 && ctaRect.height > 0,
        ctaFitsInNav: ctaRect.right <= navRect.right + 2
    }};

    document.getElementById('results').textContent = JSON.stringify(result);
}});
</script>
</body>
</html>
"""

for w, h, device_name in viewports:
    harness = harness_template.format(w=w, h=h)
    with open("tests/temp_mobile_test.html", "w", encoding="utf-8") as f:
        f.write(harness)

    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--allow-file-access-from-files",
        f"--window-size={w+50},{h+100}",
        "--dump-dom",
        "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/temp_mobile_test.html"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    import re
    match = re.search(r'<div id="results">(\{.*?\})</div>', res.stdout)
    if os.path.exists("tests/temp_mobile_test.html"):
        os.remove("tests/temp_mobile_test.html")

    if not match:
        print(f"  [FAIL] {device_name}: Could not extract results")
        all_passed = False
        continue

    data = json.loads(match.group(1))
    nav_w = data["navWidth"]
    client_w = data["clientW"]
    overflow = data["hasHorizontalOverflow"]
    cta_fits = data["ctaFitsInNav"]
    covers = data["coversCompleteWidth"]

    print(f"\n{device_name} (w={w}px, clientWidth={client_w}px):")
    print(f"  Nav width: {nav_w:.1f}px (covers complete width: {covers})")
    print(f"  Horizontal overflow: {overflow} (scrollWidth={data['docScrollWidth']}px)")
    print(f"  CTA fits inside navbar: {cta_fits}")

    if not covers:
        print(f"  [FAIL] Nav width ({nav_w}px) does not match client width ({client_w}px)")
        all_passed = False
    elif overflow:
        print(f"  [FAIL] Horizontal overflow detected on {device_name}")
        all_passed = False
    elif not cta_fits:
        print(f"  [FAIL] CTA overflows right edge on {device_name}")
        all_passed = False
    else:
        print(f"  [PASS] {device_name} verified perfectly!")

if all_passed:
    print("\n" + "=" * 60)
    print("ALL VIEWPORTS & PHONE VARIATIONS VERIFIED (100% PASS)!")
    print("=" * 60)
    sys.exit(0)
else:
    print("\nSome viewport checks failed.")
    sys.exit(1)
