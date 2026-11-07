"""
tests/verify_mobile_visualizer_layout.py
Automated verification for mobile visualizer layout:
1. Zero horizontal overflow across all mobile viewports (320px, 360px, 375px, 390px, 412px, 430px)
2. Playback cluster stacked layout for mobile:
   - Transport group ([prev] [play] [next]) and Reset/Restart group ([reset] [restart]) appear on each other like a stack with spacing
3. Desktop layout preserved: horizontal single-row playback controls on desktop viewports
"""

import subprocess
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("VERIFYING MOBILE VISUALIZER LAYOUT & CONTROLS STACKING")
print("=" * 60)

pages = ["sorting.html", "searching.html"]
mobile_viewports = [320, 360, 375, 390, 412, 430]

probe_script = """
window.addEventListener('load', () => {
    const docW = document.documentElement.clientWidth;
    const scrollW = document.documentElement.scrollWidth;
    
    const playbackCluster = document.querySelector('.playback-cluster');
    const transportGroup = document.querySelector('.playback-btn-group.transport-group');
    const resetGroup = document.querySelector('.playback-btn-group.reset-restart-group');
    
    const prevBtn = document.getElementById('prev-btn');
    const playBtn = document.getElementById('play-btn');
    const nextBtn = document.getElementById('next-btn');
    const resetBtn = document.getElementById('reset-btn');
    const restartBtn = document.getElementById('restart-btn');
    
    const tRect = transportGroup ? transportGroup.getBoundingClientRect() : null;
    const rRect = resetGroup ? resetGroup.getBoundingClientRect() : null;
    const pRect = playbackCluster ? playbackCluster.getBoundingClientRect() : null;
    
    const isStacked = tRect && rRect ? (rRect.top >= tRect.bottom - 1) : false;
    const vGap = tRect && rRect ? Math.round(rRect.top - tRect.bottom) : 0;
    
    const res = {
        docWidth: docW,
        scrollWidth: scrollW,
        hasHorizontalOverflow: scrollW > docW + 2,
        isStacked: isStacked,
        vGap: vGap,
        transportTop: tRect ? Math.round(tRect.top) : null,
        resetTop: rRect ? Math.round(rRect.top) : null,
        clusterWidth: pRect ? Math.round(pRect.width) : null
    };
    
    const out = document.createElement('div');
    out.id = 'mobile-probe-output';
    out.textContent = JSON.stringify(res);
    document.body.appendChild(out);
});
"""

for page in pages:
    print(f"\n--- Testing {page} across Mobile Viewports ---")
    raw_html = open(page, encoding="utf-8").read()
    probe_html = raw_html.replace("</body>", f"<script>{probe_script}</script></body>")
    temp_file = f"temp_mob_{page}"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(probe_html)
        
    try:
        for vw in mobile_viewports:
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
            assert '<div id="mobile-probe-output">' in proc.stdout, f"Probe output missing on {page} at {vw}px"
            data = json.loads(proc.stdout.split('<div id="mobile-probe-output">')[1].split("</div>")[0])
            
            assert not data["hasHorizontalOverflow"], f"{page} at {vw}px has horizontal overflow! scrollWidth={data['scrollWidth']}, docWidth={data['docWidth']}"
            assert data["isStacked"], f"{page} at {vw}px: Transport and Reset/Restart groups should be vertically stacked! transportTop={data['transportTop']}, resetTop={data['resetTop']}"
            assert 4 <= data["vGap"] <= 20, f"{page} at {vw}px: Vertical gap between stacked groups should be between 4px and 20px, got {data['vGap']}px"
            
            print(f"  [PASS] {vw}px: zero overflow (w={data['docWidth']}), stacked groups (transport top={data['transportTop']}, reset top={data['resetTop']}, gap={data['vGap']}px)")

        # Verify Desktop 1440px preserves horizontal single-row playback
        print(f"\n--- Testing {page} Desktop Single-Row Playback Preservation ---")
        cmd_dt = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "--headless=new", "--no-sandbox", "--disable-gpu",
            "--window-size=1440,900",
            "--allow-file-access-from-files",
            "--virtual-time-budget=2000",
            "--dump-dom",
            f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{temp_file}"
        ]
        proc_dt = subprocess.run(cmd_dt, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        data_dt = json.loads(proc_dt.stdout.split('<div id="mobile-probe-output">')[1].split("</div>")[0])
        assert not data_dt["isStacked"], f"{page} at 1440px: Transport and Reset/Restart groups should be on the SAME row on desktop!"
        print(f"  [PASS] 1440px desktop: Transport and Reset/Restart sit horizontally on the same row (top={data_dt['transportTop']})")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

print("\n" + "=" * 60)
print("ALL MOBILE VISUALIZER LAYOUT VERIFICATIONS PASSED (100%)")
print("=" * 60)

