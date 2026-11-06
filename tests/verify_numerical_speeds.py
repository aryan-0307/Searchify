import subprocess
import json
import re
import os
import sys

pages = ["sorting.html", "searching.html"]

all_passed = True
print("============================================================")
print("VERIFYING NUMERICAL SPEED SETTINGS (1x - 6x)")
print("============================================================")

harness_template = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<iframe id="test-frame" src="../{page}" style="width: 1200px; height: 800px; border: 0;"></iframe>
<div id="results"></div>
<script>
window.addEventListener('load', () => {{
    const frame = document.getElementById('test-frame');
    const win = frame.contentWindow;
    const doc = frame.contentDocument;

    const slider = doc.getElementById('speed-slider');
    const valueEl = doc.getElementById('speed-value');

    const initial = {{
        min: slider.getAttribute('min'),
        max: slider.getAttribute('max'),
        value: slider.value,
        text: valueEl.textContent.trim()
    }};

    const changes = [];
    for (let i = 1; i <= 6; i++) {{
        slider.value = i;
        slider.dispatchEvent(new win.Event('input', {{ bubbles: true }}));
        changes.push({{
            sliderVal: i,
            text: valueEl.textContent.trim()
        }});
    }}

    document.getElementById('results').textContent = JSON.stringify({{ initial, changes }});
}});
</script>
</body>
</html>
"""

for page in pages:
    print(f"\nTesting {page} speed slider...")
    harness = harness_template.format(page=page)
    temp_file = f"tests/temp_speed_{page}"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(harness)

    eval_cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--virtual-time-budget=2000",
        "--dump-dom",
        f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{temp_file}"
    ]

    res = subprocess.run(eval_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")

    if os.path.exists(temp_file):
        os.remove(temp_file)

    match = re.search(r'<div id="results">(\{.*?\})</div>', res.stdout)
    if not match:
        print(f"  [FAIL] Could not extract results for {page}")
        all_passed = False
        continue

    data = json.loads(match.group(1))
    init = data["initial"]
    changes = data["changes"]

    print(f"  Initial: min={init['min']}, max={init['max']}, value={init['value']}, label='{init['text']}'")
    assert init["min"] == "1", f"Slider min must be '1', got {init['min']}"
    assert init["max"] == "6", f"Slider max must be '6', got {init['max']}"
    assert init["text"] == "1x", f"Initial label must be '1x', got {init['text']}"
    print(f"  [PASS] {page} slider correctly configured with range 1 to 6 and default 1x")

    expected_labels = {1: "1x", 2: "2x", 3: "3x", 4: "4x", 5: "5x", 6: "6x"}
    for step in changes:
        val = step["sliderVal"]
        lbl = step["text"]
        expected = expected_labels[val]
        print(f"  Value {val} -> Label '{lbl}' (expected '{expected}')")
        assert lbl == expected, f"Expected label '{expected}' for value {val}, got '{lbl}'"
    print(f"  [PASS] All numerical speed levels (1x, 2x, 3x, 4x, 5x, 6x) successfully verified on {page}!")

if not all_passed:
    sys.exit(1)

print("\n============================================================")
print("ALL NUMERICAL SPEED SETTINGS VERIFIED (100% PASS)")
print("============================================================")

