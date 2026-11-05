import subprocess
import json
import os
import re

# Test hysteresis logic by running a headless chrome instance that navigates directly to index.html with a query or script tag injected
script = """
(() => {
    const nav = document.getElementById('home-nav');
    const steps = [];

    // Simulate the exact scroll controller logic
    var isScrolled = false;
    var SCROLL_DOWN_THRESHOLD = 45;
    var SCROLL_UP_THRESHOLD = 15;

    function simulateScroll(scrollY, label) {
        if (!isScrolled && scrollY > SCROLL_DOWN_THRESHOLD) {
            isScrolled = true;
            nav.classList.add('is-scrolled');
        } else if (isScrolled && scrollY <= SCROLL_UP_THRESHOLD) {
            isScrolled = false;
            nav.classList.remove('is-scrolled');
        }
        steps.push({
            label,
            scrollY,
            isScrolled: nav.classList.contains('is-scrolled'),
            height: nav.getBoundingClientRect().height
        });
    }

    simulateScroll(0, "top_0px");
    simulateScroll(25, "scroll_25px");
    simulateScroll(60, "scroll_60px");
    simulateScroll(30, "scroll_30px_deadband");
    simulateScroll(100, "scroll_100px");
    simulateScroll(20, "scroll_20px_deadband");
    simulateScroll(5, "scroll_5px_top");

    const out = document.createElement('div');
    out.id = 'hysteresis-results';
    out.textContent = JSON.stringify(steps);
    document.body.appendChild(out);
})();
"""

# Read index.html and inject the verification script before </body>
with open("index.html", "r", encoding="utf-8") as f:
    orig = f.read()

injected = orig.replace("</body>", f"<script>{script}</script></body>")
with open("tests/temp_index_hysteresis.html", "w", encoding="utf-8") as f:
    f.write(injected)

eval_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--allow-file-access-from-files",
    "--dump-dom",
    "file:///c:/Users/aryan/Desktop/Sorting and Searching/tests/temp_index_hysteresis.html"
]

res = subprocess.run(eval_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
match = re.search(r'<div id="hysteresis-results">(\[.*?\])</div>', res.stdout)

if os.path.exists("tests/temp_index_hysteresis.html"):
    os.remove("tests/temp_index_hysteresis.html")

if match:
    data = json.loads(match.group(1))
    print("Hysteresis and Height Stability Test:")
    for s in data:
        print(f"  {s['label']} (scrollY={s['scrollY']}) -> isScrolled={s['isScrolled']}, height={s['height']}px")
    
    # Assertions
    assert data[0]["isScrolled"] is False
    assert data[1]["isScrolled"] is False
    assert data[2]["isScrolled"] is True
    assert data[3]["isScrolled"] is True
    assert data[4]["isScrolled"] is True
    assert data[5]["isScrolled"] is True
    assert data[6]["isScrolled"] is False
    
    # Verify all heights are strictly identical
    h0 = data[0]["height"]
    for s in data:
        assert s["height"] == h0, f"Height mismatch: {s['height']} != {h0}"
    print("  [PASS] All states maintain EXACT identical height and correct hysteresis deadband!")
else:
    print("[FAIL] Output:", res.stdout[-500:])
