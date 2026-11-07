"""
tests/verify_no_scroll_hijack.py
Verification test:
Ensures that running the algorithm has ZERO effect on page scrolling.
When the algorithm is executing and the user scrolls down the page,
steps executing must NOT yank or reset window.scrollY back up to the visualizer.
"""

import subprocess
import json
import re
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

pages = ["sorting.html", "searching.html"]

all_passed = True
print("=" * 65)
print("VERIFYING ZERO SCROLL HIJACK DURING ALGORITHM EXECUTION")
print("=" * 65)

harness_template = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0;">
<iframe id="frame" src="../{page}" style="width: 1200px; height: 750px; border:0; display:block;"></iframe>
<div id="results"></div>
<script>
window.addEventListener('load', async () => {{
    await new Promise(r => setTimeout(r, 600));
    const frame = document.getElementById('frame');
    const doc = frame.contentDocument;
    const win = frame.contentWindow;

    const issues = [];
    const checks = [];

    // 1. For searching, make sure we have a target so Play can start
    if ('{page}' === 'searching.html') {{
        const targetInput = doc.getElementById('target-input');
        if (targetInput && (!targetInput.value || targetInput.value === '')) {{
            targetInput.value = '42';
            targetInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            targetInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}

    // Set speed to high (e.g. 5 or 6) so multiple steps run quickly
    const speedSlider = doc.getElementById('speed-slider');
    if (speedSlider) {{
        speedSlider.value = '5';
        speedSlider.dispatchEvent(new Event('input', {{ bubbles: true }}));
        speedSlider.dispatchEvent(new Event('change', {{ bubbles: true }}));
    }}

    // 2. Start algorithm execution
    const playBtn = doc.getElementById('play-btn');
    if (!playBtn) {{
        issues.push("Missing #play-btn");
    }} else {{
        playBtn.click();
        checks.push("Started algorithm execution via #play-btn click");
    }}

    // 3. Scroll down the window by 500px
    await new Promise(r => setTimeout(r, 200));
    const targetScrollY = 500;
    win.scrollTo(0, targetScrollY);
    const initialScrolledY = win.pageYOffset || win.scrollY || doc.documentElement.scrollTop;
    checks.push(`Scrolled page to Y = ${{initialScrolledY}}`);

    // 4. Wait while multiple algorithm steps execute
    await new Promise(r => setTimeout(r, 1200));

    // 5. Check if window scroll was preserved or hijacked
    const currentScrollY = win.pageYOffset || win.scrollY || doc.documentElement.scrollTop;
    const diff = Math.abs(currentScrollY - initialScrolledY);

    if (diff > 20) {{
        issues.push(`Scroll hijacked! Initial scroll was ${{initialScrolledY}}, but after steps executed, scroll became ${{currentScrollY}} (diff=${{diff.toFixed(1)}})`);
    }} else {{
        checks.push(`Window scroll was safely preserved at Y = ${{currentScrollY}} (diff=${{diff.toFixed(1)}} <= 20)`);
    }}

    // 6. Pause execution
    if (playBtn) {{
        playBtn.click();
    }}

    document.getElementById('results').textContent = JSON.stringify({{
        page: '{page}',
        passed: issues.length === 0,
        checks: checks,
        issues: issues,
        initialScrollY: initialScrolledY,
        currentScrollY: currentScrollY
    }});
}});
</script>
</body>
</html>
"""

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

harness_file = os.path.join(os.path.dirname(__file__), "harness_scroll_test.html")

total_tests = 0
passed_tests = 0

for page in pages:
    total_tests += 1
    print(f"\n--- Testing Page: {page} ---")
    harness_content = harness_template.format(page=page)
    with open(harness_file, "w", encoding="utf-8") as f:
        f.write(harness_content)

    file_url = "file:///" + os.path.abspath(harness_file).replace("\\", "/")
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--allow-file-access-from-files",
        "--window-size=1280,850",
        "--virtual-time-budget=4000",
        "--dump-dom",
        file_url
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=20)
        dom = res.stdout
        match = re.search(r'<div id="results">(\{.*?\})</div>', dom, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            if data["passed"]:
                passed_tests += 1
                for chk in data["checks"]:
                    print(f"  [PASS] {chk}")
            else:
                all_passed = False
                print(f"  [FAIL] {page}:")
                for iss in data["issues"]:
                    print(f"         - {iss}")
        else:
            all_passed = False
            print(f"  [FAIL] {page}: Could not extract test results from Chrome output")
    except Exception as e:
        all_passed = False
        print(f"  [ERROR] {page}: {e}")

if os.path.exists(harness_file):
    try:
        os.remove(harness_file)
    except:
        pass

print("\n" + "=" * 65)
if all_passed:
    print(f"ALL SCROLL TESTS PASSED ({passed_tests}/{total_tests})")
    print("Zero scroll hijacking detected; algorithm execution has no effect on page scroll!")
else:
    print(f"SOME TESTS FAILED ({passed_tests}/{total_tests} passed)")
    sys.exit(1)

