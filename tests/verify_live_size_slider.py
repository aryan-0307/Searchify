import subprocess
import json
import re
import os
import sys

pages = ["sorting.html", "searching.html"]

all_passed = True
print("============================================================")
print("VERIFYING DYNAMIC ARRAY SIZE SLIDER (LIVE RESIZING)")
print("============================================================")

harness_template = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<iframe id="test-frame" src="../{page}" style="width: 1200px; height: 800px; border: 0;"></iframe>
<div id="results"></div>
<script>
window.addEventListener('load', async () => {{
    await new Promise(r => setTimeout(r, 200));
    const frame = document.getElementById('test-frame');
    const win = frame.contentWindow;
    const doc = frame.contentDocument;

    const slider = doc.getElementById('array-size');
    const sizeValEl = doc.getElementById('size-value');
    const isSorting = '{page}' === 'sorting.html';
    const selector = isSorting ? '.bar' : '.cell';
    const idxSelector = isSorting ? '.bar-index' : '.cell-index';

    const results = [];

    // 1. Initial State
    results.push({{
        step: 'initial',
        sliderValue: slider.value,
        labelValue: sizeValEl.textContent.trim(),
        itemCount: doc.querySelectorAll(selector).length,
        indexCount: doc.querySelectorAll(idxSelector).length
    }});

    // 2. Increase Size to 24
    slider.value = 24;
    slider.dispatchEvent(new win.Event('input', {{ bubbles: true }}));
    await new Promise(r => setTimeout(r, 50));

    results.push({{
        step: 'increased_to_24',
        sliderValue: slider.value,
        labelValue: sizeValEl.textContent.trim(),
        itemCount: doc.querySelectorAll(selector).length,
        indexCount: doc.querySelectorAll(idxSelector).length
    }});

    // 3. Decrease Size to 7
    slider.value = 7;
    slider.dispatchEvent(new win.Event('input', {{ bubbles: true }}));
    await new Promise(r => setTimeout(r, 50));

    results.push({{
        step: 'decreased_to_7',
        sliderValue: slider.value,
        labelValue: sizeValEl.textContent.trim(),
        itemCount: doc.querySelectorAll(selector).length,
        indexCount: doc.querySelectorAll(idxSelector).length
    }});

    // 4. Test Playback after resizing
    const playBtn = doc.getElementById('play-btn');
    playBtn.click();
    await new Promise(r => setTimeout(r, 120));

    const stepDisplay = doc.getElementById('step-display').textContent.trim();
    results.push({{
        step: 'playback_after_resize',
        stepDisplay: stepDisplay,
        itemCount: doc.querySelectorAll(selector).length
    }});

    document.getElementById('results').textContent = JSON.stringify(results);
}});
</script>
</body>
</html>
"""

for page in pages:
    print(f"\n--- Testing live size slider on {page} ---")
    harness = harness_template.format(page=page)
    temp_file = f"tests/temp_size_{page}"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(harness)

    eval_cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--virtual-time-budget=3000",
        "--dump-dom",
        f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{temp_file}"
    ]

    res = subprocess.run(eval_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if os.path.exists(temp_file):
        os.remove(temp_file)

    match = re.search(r'<div id="results">(\[.*?\])</div>', res.stdout)
    if not match:
        print(f"  [FAIL] {page}: Could not extract results")
        all_passed = False
        continue

    data = json.loads(match.group(1))
    s1, s2, s3, s4 = data[0], data[1], data[2], data[3]

    print(f"  Initial: slider={s1['sliderValue']}, items={s1['itemCount']}, indices={s1['indexCount']}")
    assert int(s1["itemCount"]) == 15, f"Expected 15 initial items, got {s1['itemCount']}"
    assert int(s1["indexCount"]) == 15, f"Expected 15 initial indices, got {s1['indexCount']}"
    print(f"  [PASS] Initial 15 items and 15 indices rendered")

    print(f"  Increased to 24: slider={s2['sliderValue']}, items={s2['itemCount']}, indices={s2['indexCount']}")
    assert int(s2["itemCount"]) == 24, f"Expected 24 items after sliding up, got {s2['itemCount']}"
    assert int(s2["indexCount"]) == 24, f"Expected 24 indices after sliding up, got {s2['indexCount']}"
    assert s2["labelValue"] == "24", f"Expected label 24, got {s2['labelValue']}"
    print(f"  [PASS] Slider sliding up dynamically increased items to 24")

    print(f"  Decreased to 7: slider={s3['sliderValue']}, items={s3['itemCount']}, indices={s3['indexCount']}")
    assert int(s3["itemCount"]) == 7, f"Expected 7 items after sliding down, got {s3['itemCount']}"
    assert int(s3["indexCount"]) == 7, f"Expected 7 indices after sliding down, got {s3['indexCount']}"
    assert s3["labelValue"] == "7", f"Expected label 7, got {s3['labelValue']}"
    print(f"  [PASS] Slider sliding down dynamically decreased items to 7")

    print(f"  Playback on resized array: stepDisplay='{s4['stepDisplay']}', items={s4['itemCount']}")
    assert "/" in s4["stepDisplay"], f"Expected step progression, got {s4['stepDisplay']}"
    assert int(s4["itemCount"]) == 7, f"Item count must remain 7 during playback, got {s4['itemCount']}"
    print(f"  [PASS] Playback successfully executes steps on the dynamically resized array")

if not all_passed:
    sys.exit(1)

print("\n============================================================")
print("ALL DYNAMIC SIZE SLIDER VERIFICATIONS PASSED (100%)")
print("============================================================")

