import subprocess
import json
import re
import os
import sys

harness_html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<iframe id="test-frame" src="../index.html" style="width: 1200px; height: 800px; border: 0;"></iframe>
<div id="results"></div>
<script>
window.addEventListener('load', async () => {
    const frame = document.getElementById('test-frame');
    const win = frame.contentWindow;
    const doc = frame.contentDocument;

    const nav = doc.getElementById('home-nav');
    const brandMark = nav.querySelector('.brand-mark');
    const brandText = nav.querySelector('.home-brand-text');

    // Wait for initial load protection (no-transition) to lift
    await new Promise(r => setTimeout(r, 150));

    // 1. Initial / Default Top State
    const s1Text = win.getComputedStyle(brandText);
    const initial = {
        opacity: s1Text.opacity,
        maxWidth: s1Text.maxWidth,
        transform: s1Text.transform,
        transition: s1Text.transition,
        transitionProperty: s1Text.transitionProperty,
        transitionDuration: s1Text.transitionDuration,
        transitionDelay: s1Text.transitionDelay
    };

    // 2. Scrolled State (transition active)
    nav.classList.add('is-scrolled');
    const s2Text = win.getComputedStyle(brandText);
    const scrolled = {
        opacity: s2Text.opacity,
        maxWidth: s2Text.maxWidth,
        transform: s2Text.transform,
        transition: s2Text.transition,
        transitionProperty: s2Text.transitionProperty,
        transitionDuration: s2Text.transitionDuration,
        transitionDelay: s2Text.transitionDelay,
        pointerEvents: s2Text.pointerEvents
    };

    // 3. Test values without transition to ensure target endpoint matches
    brandText.style.transition = 'none';
    const s2Target = win.getComputedStyle(brandText);
    const targetScrolled = {
        opacity: s2Target.opacity,
        maxWidth: s2Target.maxWidth,
        transform: s2Target.transform
    };

    // 4. Restore
    brandText.style.transition = '';
    nav.classList.remove('is-scrolled');
    brandText.style.transition = 'none';
    const s3Target = win.getComputedStyle(brandText);
    const targetRestored = {
        opacity: s3Target.opacity,
        maxWidth: s3Target.maxWidth,
        transform: s3Target.transform
    };

    document.getElementById('results').textContent = JSON.stringify({
        initial,
        scrolled,
        targetScrolled,
        targetRestored
    });
});
</script>
</body>
</html>
"""

temp_file = "tests/temp_glide_test.html"
with open(temp_file, "w", encoding="utf-8") as f:
    f.write(harness_html)

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
    print("[FAIL] Could not extract test results from DOM:", res.stdout[-500:])
    sys.exit(1)

data = json.loads(match.group(1))
initial = data["initial"]
scrolled = data["scrolled"]
targetScrolled = data["targetScrolled"]
targetRestored = data["targetRestored"]

print("============================================================")
print("VERIFYING NAV BRAND 'GLIDE THEN FADE INTO BOX' MOTION")
print("============================================================")

# Check 1: Initial state
assert initial["opacity"] == "1", f"Initial opacity must be 1, got {initial['opacity']}"
assert initial["maxWidth"] == "280px", f"Initial maxWidth must be 280px, got {initial['maxWidth']}"
print(f"  [PASS] Initial resting state: full width ({initial['maxWidth']}), full opacity ({initial['opacity']})")

# Check 2: Scrolled transition delays & durations
# In scrolled state, opacity MUST have a delay so text glides towards icon BEFORE fading
scrolled_props = [p.strip() for p in scrolled["transitionProperty"].split(",")]
scrolled_delays = [d.strip() for d in scrolled["transitionDelay"].split(",")]
scrolled_durations = [t.strip() for t in scrolled["transitionDuration"].split(",")]

delay_map = dict(zip(scrolled_props, scrolled_delays))
duration_map = dict(zip(scrolled_props, scrolled_durations))

print(f"  Transition delays: {delay_map}")
print(f"  Transition durations: {duration_map}")

# Verify transform has 0s delay (starts moving immediately)
assert "transform" in delay_map, "Transform must be in transition properties"
transform_delay = float(delay_map["transform"].replace("s", ""))
assert transform_delay == 0.0, f"Transform must start gliding immediately (delay 0s), got {transform_delay}s"
print("  [PASS] Transform movement starts immediately upon scroll (delay: 0s)")

# Verify opacity has > 0s delay (starts fading right before touching icon)
assert "opacity" in delay_map, "Opacity must be in transition properties"
opacity_delay = float(delay_map["opacity"].replace("s", ""))
assert 0.05 <= opacity_delay <= 0.12, f"Opacity fade must be delayed by 0.05s-0.12s so text glides first, got {opacity_delay}s"
print(f"  [PASS] Opacity fade is delayed by {opacity_delay}s (glides towards icon before fading)")

# Verify transform duration is snappy (0.2s - 0.35s)
transform_dur = float(duration_map["transform"].replace("s", ""))
assert 0.20 <= transform_dur <= 0.35, f"Transform duration must be snappy (0.20s - 0.35s), got {transform_dur}s"
print(f"  [PASS] Snappy translation duration: {transform_dur}s")

# Check 3: Scrolled target values
assert targetScrolled["opacity"] == "0", f"Target opacity in scrolled state must be 0, got {targetScrolled['opacity']}"
assert targetScrolled["maxWidth"] == "0px", f"Target maxWidth in scrolled state must be 0px, got {targetScrolled['maxWidth']}"
assert "-" in targetScrolled["transform"], f"Transform must translate negatively towards the icon, got {targetScrolled['transform']}"
print(f"  [PASS] Scrolled endpoints: fully inside box (transform: {targetScrolled['transform']}, maxWidth: 0px, opacity: 0)")

# Check 4: Restored target values
assert targetRestored["opacity"] == "1", f"Restored opacity must be 1, got {targetRestored['opacity']}"
assert targetRestored["maxWidth"] == "280px", f"Restored maxWidth must be 280px, got {targetRestored['maxWidth']}"
print("  [PASS] Restored endpoints: text cleanly emerges from box back to origin (opacity: 1, maxWidth: 280px)")

print("============================================================")
print("ALL 'GLIDE THEN FADE INTO BOX' VERIFICATIONS PASSED (100%)")
print("============================================================")

