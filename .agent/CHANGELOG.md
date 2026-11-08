# Changelog

All notable changes to this project are documented in this file.

---

## [2026-11-08 — Multi-Algorithm Sorting Comparison Showcase on Shared Array]

### Added
- **Multi-Algorithm Sorting Comparison Showcase (`index.html`)**:
  - Replaced the legacy single-algorithm quick demo (`.home-quick-demo`) with a comprehensive multi-algorithm comparison showcase section (`.home-showcase-section`, anchored at `#try-it`).
  - Added multi-select algorithm chips toolbar (`.showcase-chips-grid`) featuring all 10 sorting algorithms (Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort, Heap Sort, Shell Sort, Counting Sort, Radix Sort, Bucket Sort) with active toggle states, checkbox indicators, and asymptotic complexity badges.
  - Added 5 comparison preset buttons:
    - *Top 3 (Popular)*: Bubble Sort, Merge Sort, Quick Sort
    - *O(n log n) Trio*: Merge Sort, Quick Sort, Heap Sort
    - *O(n²) Classic*: Bubble Sort, Selection Sort, Insertion Sort
    - *Linear Time*: Counting Sort, Radix Sort, Bucket Sort
    - *Compare All (10)*: All 10 sorting algorithms running side-by-side
- **Exact Same Shared Dataset Execution**:
  - All selected algorithms execute on the exact same shared array.
  - Includes Shuffle Array button for generating randomized shared datasets and a Custom Array input for testing custom numbers (e.g. `50, 20, 80, 10, 40`) across all active algorithms synchronously.
- **Synchronized Multi-Track Engine (`js/multi-sort-showcase.js`)**:
  - Modular controller integrating directly with `window.SortingAlgorithms` step-generator engine with zero code duplication.
  - Replaced bulky "Start Race" text with a clean, prominent Play / Pause toggle button (`#showcase-play-btn`) rendering `▶` when paused and `⏸` when playing with dynamic `title` and `aria-label` updates (`Play` / `Pause`), aligning perfectly with media transport controls (`◀`, `▶`, `▶`, `Reset`).
  - Multi-track lockstep playback loop with Play/Pause, Step Backward, Step Forward, Reset to Start, and a 4-level Speed multiplier slider (1x: 340ms, 2x: 160ms, 3x: 75ms, 4x: 30ms).
  - Dynamic algorithm track cards (`.showcase-algo-card`) rendering real-time array bars with color-coded states: comparing (`#D93D81`), swapping (`#E67E22`), pivot (`#8E44AD`), and sorted (`#27AE60`).
  - Real-time statistics counters per algorithm: comparisons, swaps, step count, percentage progress bar, and descriptive operation explanation.
- **Race Finish Leaderboard & Efficiency Breakdown**:
  - Dynamically records algorithm finish order and places (`🥇 1st`, `🥈 2nd`, `🥉 3rd`, etc.).
  - Displays finish leaderboard banner (`#showcase-leaderboard`) with comparative efficiency metrics (total steps, total comparisons, total swaps) highlighting performance differences on identical input data.
- **Responsive Layout & Typography Integrity**:
  - CSS Grid with `repeat(auto-fit, minmax(min(280px, 100%), 1fr))` on desktop/tablet, and `minmax(0, 1fr)` with `min-width: 0;` on mobile ($\le 860$px).
  - Preserved `.home-demo-heading` class and Aalto Display font styling (`800 26px 'Aalto Display', 'Aalto Display-Personal-use', sans-serif; letter-spacing: 0.03em;`).
  - Zero horizontal overflow across all viewports (Desktop 1280px, iPad 768px, Galaxy S23 412px, iPhone SE 375px).

### Verified
- Created automated test `tests/verify_multi_sort_showcase.py` in headless Chrome across Desktop 1280px, iPad 768px, Galaxy S23 412px, and iPhone SE 375px:
  - Verified DOM structure and metadata: section `#try-it`, 10 chips, 5 presets, controls bar, grid, leaderboard.
  - Verified dynamic multi-selection: adding a 4th algorithm (Heap Sort) dynamically renders its card with the exact same array, removing restores previous selection.
  - Verified presets: "Linear Time" switches selection to Counting, Radix, and Bucket Sort.
  - Verified custom array input: custom values applied synchronously to all active cards.
  - Verified race execution: lockstep synchronized stepping, status pill updates, completion detection, rank assignment, and leaderboard rendering.
  - Verified responsive layout: zero horizontal overflow on all viewports.
  - Result: **100% PASS RATE**.
- Integrated into master test suite `tests/run_all_tests.py` as Stage 32.

---

## [2026-11-08 — Merged Visualizer Controls Layout Split]

### Changed
- **Visualizer Controls Layout Restructuring (`sorting.html` & `searching.html`)**:
  - **Top Controls Toolbar (Above Visualizer Canvas)**:
    - `<nav class="viz-controls">` now exclusively houses the Array configuration controls: `Generate` button, `Custom Array` text input, `Apply` button, `Size` slider, and `Target` input (searching).
    - Playback buttons and speed controls have been removed from the top toolbar.
    - Centered horizontally across all viewports (`justify-content: center; margin: 0 auto;`).
  - **Bottom Controls Toolbar (Just Below Visualizer Canvas)**:
    - Added `<nav class="viz-controls viz-controls-bottom">` immediately below `<section class="viz-canvas-wrapper">` and above `.progress-section`.
    - Merged Playback controls (Start/Stop [Play/Pause `btn-play-prominent`], Step Prev, Step Next, Reset, Restart) and Speed control slider (`Speed: 1x` to `6x`) into a unified cockpit cluster (`.merged-playback-cluster`).
    - In `sorting.html`, also includes the Sort Order toggle (`Asc` / `Desc`).
    - Styled as an elevated soft-cream dock card with subtle borders, gentle box shadow, and elegant inline divider.
    - Centered horizontally across all viewports (`justify-content: center; margin: 0 auto;`).
- **Responsive Stacking & Mobile Behavior**:
  - In `css/visualizer.css`:
    - Desktop ($>860$px): Top and bottom controls render as sleek, single horizontal bars, perfectly centered on the page.
    - Mobile ($\le 860$px): Both clusters wrap gracefully without horizontal overflow (`overflow-x: hidden`). Transport buttons, Reset/Restart, and Speed slider stack neatly with balanced spacing while remaining centered.

### Verified
- Created automated test `tests/verify_merged_visualizer_controls.py` testing Desktop (1280px), iPad (768px), Galaxy S23 (412px), and iPhone SE (375px) in headless Chrome:
  - Verified DOM sequence: Top Array Nav $\to$ Visualizer Canvas $\to$ Bottom Merged Nav $\to$ Progress Section.
  - Verified geometric placement: Top nav strictly above canvas, Bottom nav strictly below canvas.
  - Verified horizontal centering: $0\text{px}$ deviation from viewport center.
  - Verified interactive controls: Play/pause, step scrubbing, speed slider, generate, custom array apply.
  - Result: **100% PASS RATE across all viewports**.
- Updated `tests/verify_controls_layout.py` and `tests/verify_mobile_controls_swap.py` to match the new layout architecture (**100% pass rate**).
- Integrated into master regression suite `tests/run_all_tests.py` as Stage 31 (**31/31 stages pass 100%**).

### Added
- **Unconstrained Zero-Scroll Binary Heap Tree Panel**:
  - In `css/visualizer.css`, added `.viz-auxiliary-panel.heap-tree-mode`: removes height limits (`max-height: none !important; height: auto !important;`), allows visible overflow (`overflow: visible !important; overflow-y: visible !important;`), and provides clean card styling (`background: rgba(255, 255, 255, 0.97); border: 1.5px solid var(--border-color); border-radius: var(--radius-md); box-shadow: 0 4px 18px rgba(34, 77, 149, 0.08);`).
  - All 4 levels of the binary heap tree (root, level 1, level 2, level 3) and up to 15 nodes render with zero clipping and zero internal scrollbars.
- **Dedicated Two-Tier Stage Divider**:
  - Embedded `<div class="heap-array-stage-divider">` between the Heap Tree hierarchical model and the memory array bars below.
  - Features horizontal hairline rules (`.stage-divider-line`) and a pill badge (`.stage-divider-pill`) with label *"Array Elements in Memory (Bars Below)"*.
- **Algorithm-Scoped Dynamic Canvas Height**:
  - In `js/sorting-visualizer.js`, added `updateAlgorithmLayoutMode()`: adds `.heap-sort-active` to `#visualization-area`, `.has-heap-sort` to `.viz-canvas-wrapper`, and `.heap-tree-mode` to `#viz-auxiliary-panel` when `heapSort` is selected.
  - Dynamically cleans up all classes upon switching to any of the other 9 sorting algorithms.
  - In `css/visualizer.css`, added `.viz-area.heap-sort-active` (`min-height: 570px; transition: min-height 0.25s ease;`, 550px on $\le 860$px, 540px on $\le 540$px) and matching min-height for `.viz-canvas-wrapper.has-heap-sort .viz-code-panel`.
- **Heap-Specific Usable Height & Headroom Calibration**:
  - In `getUsableAreaHeight(areaEl)` in `js/sorting-visualizer.js`:
    - On desktop ($>860$px): Bar height is capped to `Math.min(180, Math.max(100, rawHeight - 310))`.
    - On mobile ($\le 860$px): Bar height is capped to `Math.min(95, Math.max(65, rawHeight - 340))`.
  - Guarantees generous clearance ($\ge 35$px desktop, $\ge 20$px mobile; actual observed 24.6px to 155.4px) between the tree card bottom and the highest bar label under all array states, step scrubbing, and screen sizes.

### Verified
- Created automated test `tests/verify_heap_sort_layout.py` testing Desktop (1280x850), iPad (768x900), Galaxy S23 (412x850), and iPhone SE (375x800) in headless Chrome:
  - Verified `scrollHeight <= clientHeight` (zero scrolling) on `#viz-auxiliary-panel`.
  - Verified `overflowY === 'visible'`.
  - Verified 4 tree levels rendered.
  - Verified stage divider exists and separates tree from bars.
  - Verified bar clearance over 10 stepping operations (forward & backward).
  - Verified clean teardown/restoration upon switching to Bubble Sort and back.
  - Result: **100% PASS RATE across all viewports**.
- Integrated into `tests/run_all_tests.py` as Stage 30 (**all 30 stages pass 100%**).

### Added
- **Five Additional Sorting Algorithms**:
  - **Heap Sort**: Build Max-Heap / Min-Heap, sift-down heapify, extract root, and restore heap property for both Ascending and Descending modes ($O(n \log n)$ time, $O(1)$ space).
  - **Shell Sort**: Diminishing increment insertion sort using classic halving sequence, gap tracking, stride comparisons, and final pass $gap=1$ ($O(n \log n)$ best, gap-dependent worst, $O(1)$ space).
  - **Counting Sort**: Min/max finding, negative integer offset, frequency count array, cumulative prefix sums in both Ascending and Descending modes, and stable output placement ($O(n+k)$ time and space).
  - **Radix Sort (LSD)**: Least Significant Digit passes, sign separation for negative numbers, 10 digit buckets (0-9), distribution and collection passes ($O(d(n+k))$ time, $O(n+k)$ space).
  - **Bucket Sort**: Range partitioning, element scattering, individual bucket sorting using insertion sort, concatenation, and identical values handling ($O(n+k)$ avg, $O(n^2)$ worst, $O(n+k)$ space).
- **Specialized Auxiliary Visualizations**:
  - Implemented `#viz-auxiliary-panel` inside `#visualization-area` above the bars with responsive styling.
  - **Binary Heap Tree**: Displays heap as a multi-level tree (up to 15 nodes, 4 levels) with active parent, child, swapping, extracted, and sorted node highlights.
  - **Shell Gap Tracker**: Interactive gap sequence pill track and stride comparison pair indicator.
  - **Counting Sort Arrays**: Real-time Frequency Count Array and Output Array grid with active count/output highlights.
  - **Radix Digit Buckets**: 10 digit buckets (0-9) displaying item distribution, collection, and pass progress.
  - **Bucket Sort Grid**: Value range buckets showing bucket ranges, active sorting indicator, and internal bucket items.
- **Dynamic Proportional Bar Heights**:
  - Dynamic range normalization supporting negative numbers and identical values: `((val - minVal) / (maxVal - minVal || 1)) * (areaHeight - 24) + 14`.
  - Guarantees positive heights ($\ge 14$px) without division by zero.
- **Learning Features & Master Comparison Matrix**:
  - Full learning metadata for all 10 algorithms: Description, How It Works, When to Use, Properties (Stability, In-Place), Key Observations, and Key Differences.
  - Complete pseudocode definitions for all 5 new algorithms, 100% synchronized with step trace line highlights.
  - Master 10-Algorithm Comparison Matrix Table embedded in the complexity section with dynamic active row highlighting.
- **Negative Integer Custom Input**:
  - Extended custom array input range from `1 to 999` to `-999 to 999`.

### Verified
- Expanded unit test runner [tests/test_algorithms.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/test_algorithms.html) from 164 to **644 unit tests** covering all 10 algorithms across 8 test suites (random, sorted, reverse, duplicates, negatives, identical values, single-element, empty array) in both Ascending and Descending modes (**100% pass rate**).
- Verified pseudocode synchronization across all 10 sorting algorithms and 2 searching algorithms in [tests/verify_pseudocode_sync.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_pseudocode_sync.py) (**100% pass rate**).
- Created end-to-end headless Chrome verification [tests/verify_ten_sorting_algorithms.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_ten_sorting_algorithms.py) verifying DOM selector options, complexity cards, 10-row matrix table, auxiliary panel displays, backward/forward stepping, reset/restart, negative heights, and descending order (**135/135 assertions checked, 100% pass rate**).
- Verified zero console errors across all pages in [tests/check_console_errors.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/check_console_errors.py).
- Integrated into master regression suite [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) as Stage 29 (**29/29 stages pass 100%**).

### Changed
- **Visualizer Controls Ordering on Mobile Viewports**:
  - In [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css) inside `@media (max-width: 860px)`:
    - Added `order: 1;` to `.array-cluster` (Array label, Generate, Custom Array Input, Apply, Size slider, Target input).
    - Added `order: 2;` to `.playback-cluster` (Play/Pause, Prev, Next, Reset, Restart buttons).
    - Added `order: 3;` to `.settings-cluster` (Animation speed slider).
  - On mobile screens ($\le 860$px), the Array Configuration controls now sit cleanly at the top of the controls bar, and the Playback Controls (start/stop/reset/restart) are positioned immediately below them, right above the visualizer canvas.
  - On desktop viewports ($> 860$px), original DOM order and layout are 100% preserved (Playback on left, Array centered, Settings on right) with default `order: 0`.

### Verified
- Created automated test [tests/verify_mobile_controls_swap.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_mobile_controls_swap.py) testing 22 viewport and page configurations in headless Chrome:
  - Mobile (320px, 360px, 375px, 390px, 412px, 430px, 768px, 860px): Verified `arrayRect.top < playbackRect.top < settingsRect.top` and computed flex orders (`1`, `2`, `3`).
  - Desktop (861px, 1024px, 1280px): Verified natural DOM left-to-right reading order and default `order: 0`.
  - All **22/22 tests passed**.
- Updated [tests/verify_controls_layout.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_controls_layout.py) mobile checks to reflect the new mobile cluster order (**passed 100%**).
- Full regression test suite [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) executed across all **28 stages with a 100% pass rate**.

---

## [2026-11-07 — Zero Scroll Hijack During Algorithm Execution]

### Changed
- **Code Trace Line Scroll Segregation**:
  - In [js/learning-features.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/learning-features.js), replaced `targetEl.scrollIntoView({ block: 'nearest', behavior: 'smooth' })` inside `highlightTraceStep()` with container-local scrolling on `.viz-code-body`.
  - Calculated relative bounding rect offset between active pseudocode line (`targetEl`) and code body container (`codeBody`):
    - `codeBody.scrollTop -= (bodyRect.top - targetRect.top)` when line is above view.
    - `codeBody.scrollTop += (targetRect.bottom - bodyRect.bottom)` when line is below view.
  - Keeps active pseudocode lines visible inside the Live Code panel without ever affecting `window.scrollY` or triggering document-level scroll.
  - Users can freely scroll down to view live statistics, explanations, and complexity cards while algorithm execution continues uninterrupted.

### Verified
- Created automated test [tests/verify_no_scroll_hijack.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_no_scroll_hijack.py) testing live playback on both `sorting.html` and `searching.html`:
  - Verified window scroll position (`targetScrollY = 500`) is preserved with 0.0px deviation during active execution across multiple steps (2/2 tests pass).
- Integrated as Stage 27 in master regression suite [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) (27/27 stages pass 100%).

---

## [2026-11-07 — Array Status Conditions Layout Under Visualizer Area]

### Changed
- **Array Status Legend Relocation Under Visualizer Area on Mobile**:
  - In [sorting.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/sorting.html) and [searching.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/searching.html), repositioned `.color-legend` as a direct child of `.viz-canvas-wrapper` immediately following `.viz-area`.
  - In [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css):
    - Desktop (>768px): Kept `position: absolute; top: 14px; left: 24px;` within the relative `.viz-canvas-wrapper`, preserving the exact desktop visual display inside the canvas.
    - Mobile (<=768px): Structured `.viz-canvas-wrapper` as a column (`display: flex; flex-direction: column;`), placing `.color-legend` with `order: 2; position: static; width: 100%;` directly underneath `.viz-area` (`order: 1`).
    - Styled the legend bar under the visualizer area with a subtle `#FAF9F5` background, top/bottom borders, and `flex-wrap: wrap; justify-content: center; gap: 8px 14px;`.
    - Every condition (Default, Comparing, Swapping, Pivot, Sorted / Found) fits cleanly and wraps symmetrically without any clipping, cutting off, or horizontal overflow on all screen sizes down to 320px.
- **Visualizer Canvas Optimization**:
  - Decreased `.viz-area` mobile top padding to `56px` to reclaim vertical headroom inside the canvas.
  - Positioned `.canvas-status-pill` at `top: 14px; right: 14px;` floating in its own open, empty area inside the canvas.
  - In [js/sorting-visualizer.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/sorting-visualizer.js), configured dynamic usable height reservation (`reservedSpace = 144`), guaranteeing 40px+ clearance between the tallest bar label and the floating status indicator.

### Verified
- Automated test [tests/verify_mobile_visualizer_clearance.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_mobile_visualizer_clearance.py) verified:
  - `.color-legend` is located cleanly under the visualizer area (`legend.top >= area.bottom - 4`).
  - Zero overflow or cutoff across all legend conditions.
  - Zero collision between floating status pill and array elements across 8 viewports (320px to 1280px) on both visualizers (**16/16 tests pass**).
- Full regression test suite [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) passed all **26 stages with a 100% pass rate**.

---

## [2026-11-07 — Mobile Visualizer Layout & Clearance Overhaul]

### Changed
- **Mobile Color Legend & Floating Status Segregation**:
  - In [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css), updated `@media (max-width: 768px)`:
    - Positioned `.color-legend` as a single horizontal strip across the top of `.viz-area` (`top: 8px; left: 8px; right: 8px;`) with `flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none;` preventing multi-line collisions.
    - Positioned `.canvas-status-pill` cleanly on Level 2 at `top: 44px; right: 10px; left: auto;` in dedicated empty canvas space, fully separated from the legend (zero intersection or space-occupancy conflict).
- **Strict Element Clearance Below Status Options**:
  - In [js/sorting-visualizer.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/sorting-visualizer.js):
    - Added `getUsableAreaHeight(areaEl)` dynamically reserving 176px on mobile viewports ($\le 768$px) and 116px on desktop, ensuring the tallest bar and `.bar-label` are strictly and comfortably lower than both the status pill and the color legend.
    - Updated slider live resize, `renderBars()`, and `renderStep()` to use `getUsableAreaHeight()`.
  - In [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css):
    - Set `.viz-area` on mobile to `min-height: 400px; padding: 96px 14px 38px;`.
    - Overrode `align-items: center` in Searching visualizer to `align-items: flex-start !important; padding-top: 96px !important;` so search cells and target indicators begin comfortably below the status pill.
    - Adjusted mobile `@keyframes gravity-fall` and `gravity-launch` to animate within the lower canvas zone (`translateY(-20px)` instead of `-140px`), eliminating mid-air fly-through collisions when opening on mobile.

### Verified
- Created automated test [tests/verify_mobile_visualizer_clearance.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_mobile_visualizer_clearance.py) testing across 8 mobile/tablet/desktop viewports (320px, 360px, 375px, 390px, 412px, 430px, 768px, 1280px) on both `sorting.html` and `searching.html` (16/16 tests pass).
- Integrated as Stage 26 in master regression suite [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) (26/26 stages pass 100%).

---

## [2026-11-07 — Searchify Brand Font Size & Primary Font Weight Upgrade]

### Changed
- **Searchify Brand Font Size on Homepage**:
  - In [css/home.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/home.css), increased font-size for all occurrences of visible 'Searchify' brand text:
    - `.home-brand-logo`: Increased to `25px` on desktop navbar (was `20px` and `15px`), `21px` on mobile phones (was `18px`), and `19px` on compact screens (was `16px`).
    - `.footer-brand`: Increased to `25px` (was `17px`), and scaled brand spark icon to `22px`.
- **Primary Font Stack Weight Upgrade**:
  - In [css/style.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/style.css), added `--font-primary-weight: 500;` for `--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;`.
  - Configured `font-weight: var(--font-primary-weight, 500);` on `body` in both [css/style.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/style.css) and [css/home.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/home.css).
  - Explicitly upgraded font weights to `500` / `600` on `.hero-description`, `.card-long-desc`, `.section-heading>p`, `.home-demo-heading p`, `.viz-subtitle`, and `.complexity-algo-desc` for cleaner, higher-contrast legibility.

### Verified
- Created automated test [tests/verify_searchify_size_and_weight.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_searchify_size_and_weight.py) verifying `font-size >= 24px` on homepage Searchify elements and `font-weight >= 500` across all pages.
- Integrated as Stage 25 in master test runner [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).

---

## [2026-11-07 — Aalto Display Letter Spacing & Zero-Gravity Space Physics Floating Typography]

### Changed
- **Aalto Display Breathable Letter Spacing**:
  - Replaced tight negative letter spacings with generous, positive letter spacings across all Aalto Display elements to prevent glyph crowding and overlapping.
  - Defined `--letter-spacing-display: 0.03em;` in [css/style.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/style.css).
  - Updated [css/home.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/home.css):
    - `.hero-copy h1`: `letter-spacing: 0.035em;` and line-height `1.08` (was `-3.6px`).
    - Responsive hero headlines: `0.03em` (900px), `0.025em` (680px), `0.02em` (540px).
    - `.section-heading h2`: `letter-spacing: 0.03em;` and line-height `1.15` (was `-1.5px`).
    - `.home-demo-heading h2`: `letter-spacing: 0.03em;` (was `-.7px`).
    - `.card-title`: `letter-spacing: 0.025em;` (was `-0.5px`).
    - `.home-brand-logo`: `letter-spacing: 0.025em;` (was `-.8px`).
    - `.brand-mark`: `letter-spacing: 0.02em;` (was `-0.3px`).
    - `.home-stats>div strong`: `letter-spacing: 0.025em;`.
    - `.footer-brand`: `letter-spacing: 0.025em;`.
  - Updated [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css):
    - `.viz-title`: `letter-spacing: var(--letter-spacing-display, 0.03em);`.
    - `.complexity-algo-name`: `letter-spacing: var(--letter-spacing-display, 0.03em);`.

### Added
- **Zero-Gravity Space Physics Floating Typography**:
  - Structured "Algorithms make more sense when you see them move" in [index.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/index.html) into microgravity floating line groups: `.hero-space-line.line-1`, `.line-2`, `.line-3`, and `.see-them-move`.
  - In [css/home.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/home.css), implemented orbital Lissajous floating curves (`spaceOrbitalDrift1`, `spaceOrbitalDrift2`, `spaceOrbitalDrift3`) with gentle angular tilt ($\pm 0.6^\circ$) and staggered orbital periods (7.4s, 8.6s, 9.4s).
  - Implemented dynamic celestial accent float and cosmic pink glow for `see them move.` (`spaceCosmicAura`).
  - Added microgravity space drift to `.chip-top` and `.chip-bottom` in the hero art.
  - In [css/style.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/style.css), added zero-g floating animation (`spacePillFloat`) to `.canvas-status-pill` above the visualizer canvas.
  - Guaranteed accessibility with `@media (prefers-reduced-motion: reduce)` suppression.

### Verified
- Created automated test [tests/verify_space_physics_and_spacing.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_space_physics_and_spacing.py) verifying positive computed letter spacing across 11 elements and active space physics animations.
- Added as Stage 24 in master test runner [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).

---

## [2026-11-07 — Aalto Display Typography Across the Site]

### Changed
- **Global Typography Upgrade**:
  - Replaced Bricolage Grotesque with **Aalto Display** (`'Aalto Display', 'Aalto Display-Personal-use'`) across all headings, branding, numbers, and display text on [index.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/index.html), [sorting.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/sorting.html), [searching.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/searching.html), and [favicon.svg](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/favicon.svg).
  - Added `@font-face` declarations for `Aalto Display` and `Aalto Display-Personal-use` in [css/style.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/style.css) and defined `--font-display: 'Aalto Display', 'Aalto Display-Personal-use', sans-serif;`.
  - Updated [css/home.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/home.css) for `.home-brand-logo`, `.brand-mark`, `.hero-copy h1`, `.card-title`, `.card-number`, `.section-heading h2`, `.home-demo-heading h2`, and `.footer-brand`.
  - Updated [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css) for `.viz-title` and `.complexity-algo-name`.

### Verified
- Created automated test [tests/verify_font_family.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_font_family.py) testing computed `fontFamily` across 10 elements on all three pages.
- Integrated as Stage 23 in master test runner [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).

---

## [2026-11-07 — Visualizer Header Title & Subtitle Centering]

### Added
- **Centered Header Title & Subtitle**:
  - Moved the visualizer title and subtitle (`Searching Visualizer` / `Explore search paths step by step`, and `Sorting Visualizer` / `Watch algorithms come to life`) to the exact horizontal center of the header section in [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css).
  - Implemented balanced 3-column CSS Grid (`grid-template-columns: 1fr auto 1fr; align-items: center;`) on `.viz-header`:
    - Column 1 (`1fr`): `.back-btn` aligned to `justify-self: start`.
    - Column 2 (`auto`): `.viz-header-title-group` centered with `justify-self: center; text-align: center; align-items: center;`.
    - Column 3 (`1fr`): `.viz-header-controls` aligned to `justify-self: end`.
  - Configured centered alignment on mobile devices (`text-align: center; align-items: center; width: 100%;`).

### Verified
- Created automated test [tests/verify_header_title_centering.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_header_title_centering.py) measuring exact midpoint centering (`centerDiff == 0px`) and `text-align: center` on both [searching.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/searching.html) and [sorting.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/sorting.html) across 1440px desktop, 768px tablet, and 375px mobile viewports.
- Integrated as Stage 22 in master test runner [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).

---

## [2026-11-07 — Mobile Visualizer Layout & Stacked Playback Controls]

### Added
- **Mobile Stacked Playback Controls**:
  - Organized playback controls into `.transport-group` (`#prev-btn`, `#play-btn`, `#next-btn`) and `.reset-restart-group` (`#reset-btn`, `#restart-btn`) in both [sorting.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/sorting.html) and [searching.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/searching.html).
  - In [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css), on mobile viewports ($\le 768$px), configured `.playback-cluster` with `flex-direction: column` and `gap: 10px`, stacking the step navigation group and the reset/restart group on top of each other with balanced spacing and centered alignment.
  - Provided generous mobile touch dimensions (`min-height: 36px`, `max-width: 140px`) for Reset and Restart buttons.
  - On desktop viewports ($\ge 769$px), controls remain horizontally clustered on a single row with zero change to layout geometry.

### Fixed
- **Mobile Visualizer Horizontal Overflow & Zoom-Out Bug**:
  - Fixed issue where the array configuration cluster was overflowing up to 483px on mobile, forcing mobile browsers to zoom out and leave empty space.
  - Configured `flex-wrap: wrap`, auto widths, and responsive input boundaries (`width: min(130px, 36vw)`) on `.array-cluster` and `.settings-cluster`.
  - Added `overflow-x: hidden` and `max-width: 100vw` protection on `.viz-page` and `.viz-controls`.
  - Eliminated horizontal scrollbars across all tested mobile phone widths (320px, 360px, 375px, 390px, 412px, 430px).

### Verified
- Created automated test suite [tests/verify_mobile_visualizer_layout.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_mobile_visualizer_layout.py) verifying zero horizontal overflow, stacked playback groups (10px gap), and desktop single-row preservation across all devices.
- Integrated as Stage 21 in master test suite [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).

---

## [2026-11-07 — Homepage Hero Stray Duplicate Removal & Layout Cleanup]

### Fixed
- **Stray Duplicate Elements on Homepage**:
  - Removed accidental duplicate markup in [index.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/index.html) that had leaked outside `<section class="home-hero">` into `main.home-container`.
  - Removed orphaned code line `04 // repeat & improve`, stray `.hero-mini-bars` visualizer, and footer `Visualising operation STEP 08 / 24` that rendered awkwardly in the gap above `.home-stats`.
  - Removed mismatched duplicate closing tags (`</div>`, `.floating-chip`, `.hero-sparkle`, `</section>`), ensuring valid semantic HTML structure where `<section class="home-stats">` directly succeeds `<section class="home-hero">`.

### Added
- **Automated Verification**:
  - Created [tests/verify_homepage_cleanup.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_homepage_cleanup.py) testing DOM tree integrity, asserting zero stray children in `.home-container` and checking direct sibling adjacency between hero and stats.
  - Added Stage 20 to master test suite [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).

---

## [2026-11-07 — Sticky Top Navbar Positioning Across Visualizers]

### Added
- **Visualizer Top Navbar Sticky Pinning**:
  - Pinned the visualizer top navbar (`.viz-header`) to the top of the viewport in [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css) via `position: sticky; top: 0; left: 0; right: 0; width: 100%; z-index: 1000; box-sizing: border-box;`.
  - Content smoothly passes underneath the navbar with solid background (`var(--soft-cream)` / `#FAF9F5`), bottom border, and subtle drop shadow.
  - Ensures the Back button, algorithm title, notification pill, and algorithm switcher dropdown remain accessible at all scroll depths.

### Fixed
- **Toolbar Cluster Duplication**:
  - Removed an orphaned duplicate playback cluster inside `<nav class="viz-controls">` on both [sorting.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/sorting.html) and [searching.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/searching.html), establishing the exact 3-cluster layout: Playback (Left) $\rightarrow$ Array (Center) $\rightarrow$ Settings (Right).

### Verified
- Enhanced automated test [tests/verify_controls_layout.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_controls_layout.py) to assert `headerPos == 'sticky'` and `headerTop == 0`.
- All 19 stages pass 100% in master test runner [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).

---

## [2026-11-07 — Visualizer Controls Layout (Left Playback, Center Array, Right Settings)]

### Added
- **Visualizer Toolbar Layout Reorganization**:
  - Reorganized `<nav class="viz-controls">` across both [sorting.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/sorting.html) and [searching.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/searching.html):
    - **Left**: Start/Stop & Playback controls cluster (`.playback-cluster`) containing `#prev-btn`, `#play-btn` (prominent circular play/pause), `#next-btn`, `#reset-btn`, and `#restart-btn`, occupying the space left by the array controls.
    - **Center**: Array configuration cluster (`.array-cluster`) containing `#generate-btn`, `#custom-array`, `#apply-custom-btn`, `#array-size`, and `#target-input`, occupying the center space.
    - **Right**: Settings cluster (`.settings-cluster`) containing `#speed-slider` (and Asc/Desc sort order toggle on sorting).
- **Responsive Toolbar Styling in [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css)**:
  - Configured `margin: 0 auto` on `.array-cluster` for wide desktop screens ($\ge 1320$px), producing equal spacing on both sides between Playback and Array, and between Array and Settings.
  - Centered wrapped clusters cleanly on intermediate screens (861px - 1319px).
  - Maintained full-width stacked alignment with centered buttons on mobile viewports ($\le 860$px).

### Verified
- Updated automated test [tests/verify_controls_layout.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_controls_layout.py) testing:
  - DOM cluster sequence `Playback (Left) -> Array (Center) -> Settings (Right)`.
  - Geometric horizontal positioning and equal margin gaps at 1440px desktop.
  - Responsive vertical stacking at 768px mobile.
  - Interactive play/pause toggling, array generation, and live speed slider reactivity.
- Integrated as Stage 19 in [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) with 100% pass across all 19 test suites.

---

## [2026-11-07 — Visualizer Controls Layout (Center Play/Pause & Right Settings)]

### Added
- **Visualizer Toolbar Layout Reorganization**:
  - Reorganized `<nav class="viz-controls">` across both [sorting.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/sorting.html) and [searching.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/searching.html):
    - **Center**: Playback controls cluster (`.playback-cluster`) containing `#prev-btn`, `#play-btn` (prominent circular play/pause), `#next-btn`, `#reset-btn`, and `#restart-btn`.
    - **Right**: Settings cluster (`.settings-cluster`) containing `#speed-slider` (and Asc/Desc sort order toggle on sorting) in the place where start/stop/reset/restart formerly resided.
    - **Left**: Array configuration cluster (`.array-cluster`) containing `#generate-btn`, `#custom-array`, `#apply-custom-btn`, `#array-size`, and `#target-input`.
- **Responsive Toolbar Styling in [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css)**:
  - Configured `margin: 0 auto` on `.playback-cluster` for wide desktop screens ($\ge 1320$px), producing equal spacing on both sides between Array and Playback, and between Playback and Settings.
  - Centered wrapped clusters cleanly on intermediate screens (861px - 1319px).
  - Maintained full-width stacked alignment with centered buttons on mobile viewports ($\le 860$px).

### Verified
- Created automated test [tests/verify_controls_layout.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_controls_layout.py) testing:
  - DOM cluster sequence `Array -> Playback -> Settings`.
  - Geometric horizontal positioning and equal margin gaps at 1440px desktop.
  - Responsive vertical stacking at 768px mobile.
  - Interactive play/pause toggling and live speed slider reactivity.
- Integrated as Stage 19 in [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) with 100% pass across all 19 test suites.

---

## [2026-11-07 — Searchify Brand Logo Favicon Assets & Site Integration]

### Added
- **Searchify Logo Favicon Suite**:
  - `favicon.svg`: Scalable vector SVG featuring the Searchify signature brand squircle (`rx="19"`) filled with royal blue gradient (`#2D62BF` to `#16376E`), subtle top lighting bevel, bold white centered 'S', and vibrant pink algorithm pulse spark dot (`#D93D81` with white core).
  - `favicon-32x32.png` & `favicon-16x16.png`: High-resolution anti-aliased PNG icons generated with 4x supersampling via standalone software rasterizer script `scripts/create_favicons.py`.
  - `apple-touch-icon.png`: 180x180 PNG formatted for iOS home screen bookmarks and Apple devices.
  - `favicon-192x192.png`: 192x192 PNG formatted for Android and PWA manifests.
  - `favicon.ico`: Dual-image standard ICO header bundling both 32x32 and 16x16 payloads for legacy browser backwards-compatibility.
- **HTML Document Integration**:
  - Linked all favicon assets in the `<head>` of [index.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/index.html), [sorting.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/sorting.html), and [searching.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/searching.html):
    - `<link rel="icon" type="image/svg+xml" href="favicon.svg">`
    - `<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">`
    - `<link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">`
    - `<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">`
    - `<link rel="shortcut icon" href="favicon.ico">`

### Verified
- Updated [tests/verify_semantic_seo.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_semantic_seo.py) to assert favicon link presence on all pages.
- Executed master test runner [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) with 100% pass across all 18 test suites.

---

## [2026-11-07 — Perfect Visualization-to-Pseudocode Synchronization]

### Added
- **Exact Line-by-Line Pseudocode Alignment**:
  - Audited and realigned every generated step across all 7 algorithms in [js/sorting-algorithms.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/sorting-algorithms.js) and [js/searching-algorithms.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/searching-algorithms.js) to resolve systematic 1-2 line index mismatches:
    - **Bubble Sort**:
      - Comparisons now highlight `Line 4: if A[j] > A[j+1] then`.
      - Swaps highlight `Line 5: swap A[j] and A[j+1]`.
      - In-order non-swaps highlight `Line 7: end if`.
      - Pass completions highlight `Line 8: end for`.
      - Early terminations highlight `Line 9: if swapped = false then return`.
      - Algorithm finish highlights `Line 11: end procedure`.
    - **Selection Sort**:
      - Pass start / minimum candidate highlights `Line 2: minIdx = i`.
      - Comparisons highlight `Line 4: if A[j] < A[minIdx] then`.
      - New minimum found highlights `Line 5: minIdx = j`.
      - Swaps into sorted position highlight `Line 8: swap A[i] and A[minIdx]`.
      - Pass completion highlights `Line 9: end for`.
      - Final completion highlights `Line 10: end procedure`.
    - **Insertion Sort**:
      - Key extraction highlights `Line 2: key = A[i]`.
      - Comparisons highlight `Line 4: while j >= 0 and A[j] > key`.
      - Shifts highlight `Line 5: A[j+1] = A[j]`.
      - Insertion spot found highlights `Line 7: end while`.
      - Key placement highlights `Line 8: A[j+1] = key`.
      - Final completion highlights `Line 10: end procedure`.
    - **Merge Sort**:
      - Sub-array divide highlights `Line 2: mid = (left + right) / 2`.
      - Sub-array merge start highlights `Line 7: procedure merge(A, left, mid, right)`.
      - Sub-array comparisons highlight `Line 9: if leftArr[i] ≤ rightArr[j]`.
      - Left placements highlight `Line 10: A[k] = leftArr[i]; i++`.
      - Right placements highlight `Line 12: A[k] = rightArr[j]; j++`.
      - Copying remaining elements highlights `Line 14: copy remaining elements`.
      - Merge and full completion highlight `Line 15: end procedure`.
    - **Quick Sort**:
      - Partition start and pivot selection highlight `Line 6: pivot = A[high]`.
      - Pivot comparisons highlight `Line 9: if A[j] ≤ pivot then`.
      - Partition swaps highlight `Line 10: i++; swap A[i] and A[j]`.
      - Stays on right side highlights `Line 11: end if`.
      - Pivot positioning swaps highlight `Line 12: swap A[i+1] and A[high]`.
      - Final pivot return highlights `Line 13: return i + 1`.
      - Final completion highlights `Line 14: end procedure`.
    - **Linear Search**:
      - Element comparisons highlight `Line 2: if A[i] == target then`.
      - Target match highlights `Line 3: return i`.
      - Empty array and absent target highlight `Line 6: return -1`.
    - **Binary Search**:
      - Range initialization highlights `Line 1: low = 0`.
      - Target match highlights `Line 6: return mid`.
      - Range elimination (search right) highlights `Line 8: low = mid + 1`.
      - Range elimination (search left) highlights `Line 10: high = mid - 1`.
      - Empty range / not found highlights `Line 13: return -1`.
- **UI & Active Code Enhancements**:
  - Added CSS active line arrow indicator `▶` on `.viz-code-line.active::after`.
  - Added live `L<num>: <code>` preview in the status footer with tooltip explanation.

### Verified
- Created [tests/verify_pseudocode_sync.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_pseudocode_sync.py) verifying 100% bounds validity and exact semantic mapping between visualizer operations and pseudocode statements.
- Integrated as Stage 18 in [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) with 100% pass across all 18 test suites.

---

## [2026-11-07 — Live Code Trace (80:20 Ratio) Visualizer Panel]

### Added
- **Live Code Trace Demonstration in Visualizer Canvas**:
  - Embedded `<aside class="viz-code-panel" id="viz-code-panel" aria-label="Live code trace demonstration">` directly inside `<section class="viz-canvas-wrapper">` side-by-side with `<figure class="viz-area" id="visualization-area">` on both [sorting.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/sorting.html) and [searching.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/searching.html).
  - Configured exact **80:20 space sharing** in [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css) via `grid-template-columns: 80% 20%`.
  - Added full visualizer palette styling:
    - Pulsing `LIVE CODE` badge with glowing dot animation.
    - Algorithm Trace title that syncs dynamically with the selected algorithm.
    - Active step badge (`Ready`, `Step X / Y`, `Done`).
    - Expand/collapse toggle button `#viz-code-toggle` with smooth `.code-collapsed` state transition.
    - Monospaced code line listing with line numbers, hover effects, and distinct active line highlighting (`#FFF0F6` background with vibrant pink border accent).
    - Status footer showing current step operation and pseudocode tag.
    - Responsive stacked adaptation below 860px width ensuring mobile viewports retain 100% width for unclipped array index numbers.
- **Dynamic Controller Integration in [js/learning-features.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/learning-features.js)**:
  - Renders the complete pseudocode for the currently selected algorithm on initial page load.
  - Automatically re-renders pseudocode lines and header title whenever the algorithm selection changes in `#algorithm-select`.
  - Dynamically highlights executing pseudocode lines on every `searchify:step` event, smoothly auto-scrolling active lines into view.
  - Resets active highlights and restores `Ready` badge upon `#reset-btn`, `#restart-btn`, `#generate-btn` clicks and `searchify:run-reset` events.
  - Removed duplicate code trace card from the bottom learning lab.
- **Visualizer Layout & Resizing in [js/sorting-visualizer.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/sorting-visualizer.js)**:
  - Added debounced window resize handler to automatically recalculate and re-render bar widths when window or layout changes occur.

### Verified
- Created [tests/verify_code_trace_panel.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_code_trace_panel.py) verifying:
  - 80.00% viz area to 20.00% code panel ratio on desktop viewports.
  - Pseudocode line rendering across all algorithms.
  - Real-time active line highlighting during step execution.
  - Collapse and re-expansion toggle operation.
- Added as Stage 17 in [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).
- Master test runner executed and passed 100% across all 17 test suites.

---

## [2026-11-06 — Semantic HTML5 Conversion & Comprehensive SEO Optimization]

### Added
- **Semantic HTML5 Tag Restructuring**:
  - Replaced generic non-semantic `<div>` elements across all three site pages with meaningful HTML5 landmark and content-sectioning elements:
    - **index.html**:
      - `<header class="home-nav" role="banner">` for the top navigation bar.
      - `<main class="home-container" id="main-content">` for the primary page document.
      - `<header class="hero-copy">` encapsulating the hero headline, badge, and intro copy.
      - `<nav class="hero-actions" aria-label="Hero actions">` for primary CTA links.
      - `<aside class="hero-proof" aria-label="Social proof">` for the user metric callout.
      - `<figure class="hero-art" aria-hidden="true">` for the decorative interactive orbit illustration.
      - `<section class="home-playgrounds" aria-labelledby="playgrounds-heading">` for the playground modules.
      - `<article class="card-inner">` inside `a.home-card` providing semantic article representation for both Searching and Sorting cards.
      - `<header class="card-header">`, `<figure class="mini-viz">`, and `<footer class="card-footer">` inside playground cards.
      - `<header class="home-demo-heading">`, `<figure class="home-demo-bars">`, and `<nav class="home-demo-actions">` inside the live interactive playground preview.
      - `<footer class="home-footer" role="contentinfo">` with `<nav class="home-footer-links" aria-label="Footer links">` for footer branding and navigation.
    - **sorting.html**:
      - `<header class="viz-header" role="banner">` with `<hgroup class="viz-header-title-group">` and `<aside class="viz-header-controls">`.
      - `<nav class="viz-controls" aria-label="Algorithm Controls">` containing `<section class="controls-cluster">` blocks.
      - `<main class="viz-content-container" id="main-content">` holding `<figure class="viz-area" aria-label="Sorting Visualization Canvas">`.
      - `<aside class="color-legend">` and `<aside id="completion-banner">`.
      - `<section class="progress-section">` and `<section class="interactive-row">`.
      - `<article class="interactive-col explanation-col">` and `<article class="interactive-col stats-col">`.
      - `<article class="counter-card">` for metrics and operations.
      - `<footer class="viz-footer" role="contentinfo">`.
    - **searching.html**:
      - Parallel semantic structure matching `sorting.html` (`<header role="banner">`, `<hgroup>`, `<aside class="viz-header-controls">`, `<nav class="viz-controls">`, `<section class="controls-cluster">`, `<main id="main-content">`, `<figure class="viz-area">`, `<aside class="color-legend">`, `<aside id="completion-banner">`, `<article class="counter-card">`, and `<footer class="viz-footer" role="contentinfo">`).
- **Comprehensive SEO & Social Graph Metadata**:
  - Primary SEO Meta: `<title>`, `<meta name="description">`, `<meta name="keywords">`, `<meta name="author">`, `<meta name="robots" content="index, follow">`, canonical link `<link rel="canonical">`.
  - Open Graph Meta: `og:title`, `og:description`, `og:type`, `og:site_name`, `og:url`.
  - Twitter Card Meta: `twitter:card`, `twitter:title`, `twitter:description`.
- **CSS Semantic Tag Styles & Fixes**:
  - Added `.viz-footer` in [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css).
  - Added `overflow-x: hidden;` to `html` in [css/home.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/home.css) to eliminate horizontal scrollbar caused by decorative sub-pixel rotated background orbits on tablet viewports.
  - Added `margin: 0;` to `.hero-art` and `.mini-viz` resetting default browser `<figure>` margins.

### Verified
- Created [tests/verify_semantic_seo.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_semantic_seo.py) to validate semantic markup and SEO metadata across all three pages.
- Integrated as Stage 16 in [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).
- Verified 100% pass rate across all 16 automated test suites.

---

## [2026-11-06 — Reverse Gravity Launch Physics for Decreasing Array Size]

### Added
- **Reverse Gravity Launch & Catapult Keyframes (`@keyframes gravity-launch`)**:
  - Implemented the exact mathematical and physical time-reversal of the gravity bounce curve in [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css):
    - **Resting Baseline Equilibrium ($t = 0\%$)**: Elements start at rest on the ground ($y = 0, \text{scale} = 1$).
    - **Pre-Launch Micro-Hop ($t \approx 9\%$)**: A small preparatory upward hop to $y = -5\text{px}$.
    - **Pre-Load Descent & Deep Elastic Ground Compression ($t \approx 18\% - 50\%$)**: Rebounds back down and compresses deep into the baseline floor (`scaleY(0.82) scaleX(1.12)` anchored at `transform-origin: bottom center`) to store maximum kinetic launch energy.
    - **Elastic Spring Decompression & Catapult Ascent ($t \approx 56\% - 84\%$)**: Rapidly decompresses and shoots vertically off the ground with accelerating upward velocity.
    - **Sky Departure ($t = 100\%$)**: Catapults high into the sky ($y = -140\text{px}$, vertically elongated `scaleY(1.08) scaleX(0.94)`) and fades out (`opacity: 0`), cleanly vanishing.
- **Reverse Physics Flight Engine for Slider Removal**:
  - **Sorting Visualizer** in [js/sorting-visualizer.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/sorting-visualizer.js):
    - When reducing array size via slider, bars being removed are converted to `.bar-launching` at their exact absolute pixel coordinates, displaying `.bar-index-launching`.
    - Removed bars execute the reverse gravity catapult into the sky, while remaining bars smoothly expand and glide into place via CSS transition.
  - **Searching Visualizer** in [js/searching-visualizer.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/searching-visualizer.js):
    - When reducing array size via slider, cells being removed are converted to `.cell-launching` at their exact coordinates inside `.search-cells` (styled with `position: relative`), displaying `.cell-index-launching`.
    - Removed cells launch up into the sky and fade out, while remaining cells smoothly re-center.
- **Lifecycle Cleanup**:
  - Automatically clears any in-flight `.bar-launching` or `.cell-launching` elements on rapid slider reversals or execution reset, preventing orphaned nodes.

### Verified
- Updated [tests/verify_gravity_animation.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_gravity_animation.py) validating static reverse keyframes and runtime Chrome verification of both forward falling and reverse launch physics.
- Verified that [tests/verify_live_size_slider.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_live_size_slider.py) passes 100% with exact active bar/cell and index counts.
- Master test runner [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) executed with 100% pass rate across all 15 test suites.

---

## [2026-11-06 — Natural Gravity Drop & Elastic Bounce Physics for Visualizer Slider Operations]

### Added
- **Natural Gravity Drop & Ground Interaction Physics Keyframes**:
  - Implemented `@keyframes gravity-fall` in [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css) modeling realistic free fall under Earth gravity:
    - **Free Fall with Downward Acceleration**: Elements fall from $y = -140\text{px}$, accelerating downward under gravity ($g$).
    - **Ground Impact Collision**: Hits the baseline floor ($y = 0$) at $t \approx 44\%$.
    - **Elastic Ground Compression (Squash)**: At $t \approx 50\%$, converts kinetic energy into elastic strain deformation (`scaleY(0.82) scaleX(1.12)` with `transform-origin: bottom center`), keeping the baseline grounded while compressing downward and bulging outward according to volume conservation principles.
    - **Elastic Rebound (Restitution)**: Rebounds upward to $y = -22\text{px}$ (`scaleY(1.02) scaleX(0.98)`).
    - **Secondary Touchdown & Micro-Bounce**: Lands with subtle micro-compression (`scaleY(0.94) scaleX(1.03)`), hops up $5\text{px}$, and smoothly settles into rest at $y = 0, \text{scale} = 1$.
  - Added `.bar.drop-in` and `.cell.drop-in` classes anchored with `transform-origin: bottom center;`.
  - Added accessibility support with `@media (prefers-reduced-motion: reduce)` to disable animations for users requesting reduced motion.
- **Dynamic Incremental Slider Sliding with Smooth Transitions**:
  - **Sorting Visualizer** in [js/sorting-visualizer.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/sorting-visualizer.js):
    - When increasing array size via slider: existing bars smoothly glide and shrink in width via CSS `transition: width 0.18s cubic-bezier(0.2, 0.8, 0.2, 1)`, while newly added bars rain down from above with staggered gravity drop and bounce.
    - When decreasing array size: excess bars are immediately trimmed and remaining bars smoothly expand to fill the available canvas width.
  - **Searching Visualizer** in [js/searching-visualizer.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/searching-visualizer.js):
    - When increasing array size via slider: newly added cells drop from above with staggered gravity bounces and attached `.cell-index` labels.
    - When decreasing array size: excess cells are cleanly removed and remaining cells smoothly re-center.
- **Array Generation & Load Cascade**:
  - "Generate Array" and initial page load trigger a staggered falling cascade across all bars and cells.

### Verified
- Created [tests/verify_gravity_animation.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_gravity_animation.py) verifying CSS keyframe physics (height drop, elastic compression, restitution apex, settled rest) and runtime live slider additions in Headless Chrome.
- Integrated `verify_gravity_animation.py` as Stage 15 in [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).
- Master test runner executed and passed 100% across all 15 test suites.

---

## [2026-11-06 — Real-Time Live Resizing for Array Size Slider]

### Added
- **Live Dynamic Array Resizing on Slider Input**:
  - Implemented automatic, real-time resizing in [js/sorting-visualizer.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/sorting-visualizer.js) and [js/searching-visualizer.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/searching-visualizer.js) whenever the user slides `#array-size`:
    - **Increasing (Sliding Right)**: Seamlessly appends new random elements to the array (`(newSize - currentArray.length)` items), immediately generating and placing new bars or cells with their index numbering.
    - **Decreasing (Sliding Left)**: Cleanly truncates elements from the end to match `newSize`, smoothly adjusting bar widths and re-centering the remaining elements.
    - **Binary Search Sorting Invariant**: If Binary Search is active, any newly added elements are automatically sorted to maintain the algorithm's ordering requirement.
    - **Execution Reset**: Automatically resets running states and step counters cleanly without requiring manual "Generate New Array" clicks.

### Verified
- Created [tests/verify_live_size_slider.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_live_size_slider.py) validating that moving the slider from 15 to 24 dynamically increases DOM bars/cells to 24, sliding down to 7 reduces them to 7, and playback executes correctly.
- Integrated `verify_live_size_slider.py` as Stage 14 in [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).
- Master test runner executed and passed 100% across all 14 test suites.

---

## [2026-11-06 — Hero Section Streamlining & Mobile Visualizer Index Visibility]

### Removed
- **Hero Pill Badge**:
  - Removed `<div class="hero-pill"><span class="hero-live-dot"></span> YOUR INTERACTIVE DSA LAB</div>` from [index.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/index.html) to keep the hero headline clean and prominent.

### Fixed
- **Mobile Visualizer Array Index Visibility**:
  - **Sorting Visualizer**: Added `.bar-index` generation in [js/sorting-visualizer.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/sorting-visualizer.js) so index values `0, 1, 2...` are rendered directly below each vertical bar.
  - **Index Centering & Monospace Styling**: Styled `.bar-index` with `left: 50%; transform: translateX(-50%)` and `font-family: var(--font-mono)` so multi-digit numbers align cleanly under narrow mobile bars.
  - **Searching Multi-Row Occlusion**: Increased `.search-cells` row gap from 10px to `38px` (`40px` on mobile screens < 540px) in [css/visualizer.css](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/css/visualizer.css), completely eliminating the issue where wrapped row 2 cells rendered over row 1's `.cell-index`.
  - **Bottom Padding Clearance**: Set `padding-bottom: 38px` on `.viz-area` and `36px` on `.search-cells-wrapper` across mobile screen media queries, ensuring indices on the bottom row have generous buffer and are never cut off.

### Verified
- Created [tests/verify_mobile_indexes.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_mobile_indexes.py) verifying index visibility, bounding boxes, and non-overlap across 6 mobile phone viewports (iPhone SE 320px/375px, Galaxy S 360px, iPhone 13-16 390px/430px, Pixel 7/Galaxy S23 412px).
- Integrated `verify_mobile_indexes.py` as Stage 13 in [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py).
- Master test runner executed and passed 100% across all 13 test suites.

---

## [2026-11-06 — Extended Numerical Speed Controls (1x to 6x) for Searching & Sorting Visualizers]

### Changed
- **Extended Numerical Speed Multipliers from 1x to 6x**:
  - Expanded speed settings in [sorting.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/sorting.html) and [searching.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/searching.html) to support a 6-level slider range (`min="1" max="6"`), providing progressively faster stepping speeds:
    - **1x**: Lowest speed (850ms delay per step) — deliberate progression for careful inspection of comparisons.
    - **2x**: 500ms delay per step — comfortable paced animation.
    - **3x**: 300ms delay per step — active steady progression.
    - **4x**: 160ms delay per step — brisk exploratory speed.
    - **5x**: 80ms delay per step — very fast sweep across arrays.
    - **6x**: Highest speed (35ms delay per step) — ultra-fast rapid completion of passes.
  - Updated `SPEED_MAP` and `SPEED_LABELS` in [js/main.js](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/js/main.js).
  - Updated `#speed-slider` elements in both visualizers to `min="1" max="6" value="1"`.

### Verified
- Extended [tests/test_algorithms.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/test_algorithms.html) with assertions for all 6 speed labels and strict monotonic delay decreases (all 164 unit tests pass).
- Updated [tests/verify_numerical_speeds.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/verify_numerical_speeds.py) dynamically verifying slider steps 1 through 6 on both pages in Headless Chrome.
- Master test runner [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) executed and passed 100% across all 12 test suites.

---

## [2026-11-06 — Navbar Clean-up: Removed Redundant Playgrounds Link]

### Removed
- **Redundant Playgrounds Nav Link**:
  - Removed `<a href="#playgrounds" class="nav-link-item">Playgrounds</a>` from `.home-nav-links` in [index.html](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/index.html).
  - The `"Start exploring ↗"` primary CTA button (`.nav-cta`) already navigates to `#playgrounds`, eliminating the duplicate link and keeping the navbar clean and uncluttered.

### Verified
- Master test runner [tests/run_all_tests.py](file:///c:/Users/aryan/Desktop/Sorting%20and%20Searching/tests/run_all_tests.py) executed and passed 100% across all 11 test suites (desktop, tablet, mobile viewports down to 320px).

---

## [2026-11-06 — Staggered Brand Motion: Glide Towards Icon, Then Fade Right Before Entering Box]

### Changed
- **Staggered Motion Choreography**:
  - Re-timed the brand scroll animation so the text visibly glides across the gap towards the icon *before* fading.
  - Translation starts immediately at $t = 0\text{s}$ (`delay: 0s`, `duration: 0.28s`, `cubic-bezier(0.4, 0, 0.2, 1)`), moving the letters leftward towards the `.brand-mark` badge box.
  - Opacity fade is staggered with a `0.08s` delay (`opacity 0.16s cubic-bezier(0.4, 0, 0.2, 1) 0.08s`), keeping the letters at 100% opacity during the approach, and triggering the fade *right before* touching the icon boundary.
  - Added `0.05s` delay on `max-width` collapse so the entire wordmark travels together into the box without premature right-side clipping.
  - On scroll back to top (unboxing), opacity returns with minimal delay (`0.02s`) as the brand text re-emerges from the box.

### Verified
- Created `tests/verify_glide_fade.py` sampling computed styles, transition delays, and durations in headless Chrome.
- Integrated `verify_glide_fade.py` as Stage 11 in `tests/run_all_tests.py`.
- All 11 verification suites passed 100%.

---

## [2026-11-06 — Brand Text "Into the Box" Scroll Animation]

### Changed
- **"Items Going Inside the Box" Brand Animation**:
  - Implemented the user's requested physics metaphor where all text of "Searchify" glides leftward into the logo mark badge like items entering a box.
  - Set `.brand-mark` as the foreground box (`z-index: 2`) with an intake reaction (`transform: scale(1.05)`).
  - Set `.home-brand-text` (`z-index: 1`) to translate leftward directly into the badge box (`transform: translateX(-40px) scale(0.7)`), sliding behind the `[S]` badge as it fades (`opacity: 0`) and collapses (`max-width: 0`).
  - When scrolling back towards the top, the text unboxes smoothly, emerging from behind the `[S]` badge box back to full scale, opacity, and width.

### Verified
- Updated `tests/verify_nav_animation.py` to assert the leftward text translation into the badge box (`matrix(0.7, 0, 0, 0.7, -40, 0)`).
- Master test runner `tests/run_all_tests.py` ran with 100% pass rate across all 10 test suites.

---

## [2026-11-06 — Full-Width Navbar & Phone Variations Support]

### Added
- **Complete Width Edge-to-Edge Coverage**:
  - Moved `.home-nav` to the root `<body>` level with `width: 100%`, `left: 0`, and `right: 0`, removing all side body insets so the liquid glass bar spans the complete viewport from bezel to bezel on any display size (from 320px phones to 1920px+ monitors).
  - Encapsulated header elements within `.home-nav-inner` (`max-width: 1240px; margin: 0 auto; padding: 16px 34px`) to ensure perfect alignment with the hero and playground cards.

### Fixed
- **Mobile Phone Navbar Adaptations & Overflow Prevention**:
  - Diagnosed that on phone viewports (< 400px), 3 nav links + full brand resulted in a 378px–399px width, causing horizontal overflow and CTA clipping.
  - Implemented phone variation rules:
    - On phones (< 540px): Hid redundant anchor links (`.nav-link-item`) to give the prominent `"Start exploring ↗"` CTA button clean breathing room without text squishing or wrapping.
    - On compact phones (< 360px): Gracefully scaled padding and icon dimensions to maintain comfortable touch targets while keeping horizontal overflow at strictly 0px.
    - Added `overflow: hidden` on `.hero-art` to stop decorative spinning orbits from overflowing tablet and mobile screens.

### Verified
- Created `tests/verify_mobile_nav.py` testing 9 device viewports: iPhone SE (320px), Galaxy S (360px), iPhone SE/8 (375px), iPhone 13/14/15/16 (390px), Galaxy S23/Pixel 7 (412px), iPhone Pro Max (430px), iPad (768px), Laptop (1280px), Desktop (1920px).
- Master test runner `tests/run_all_tests.py` ran with 100% pass rate across all 10 test suites.

---

## [2026-11-06 — Persistent Liquid Glass Navbar Background]

### Changed
- **Unified Liquid Glass Background**:
  - Configured `.home-nav` and `.home-nav.is-scrolled` to share the exact same liquid glass background styling across all states:
    - Base color: `rgba(245, 243, 237, 0.72)` (matching the website's warm ivory `#F5F3ED` palette with zero base color difference).
    - Backdrop Filter: `blur(20px) saturate(180%)` for rich optical refraction and vibrant glass diffusion.
    - Glass Border & Shadow: `1px solid rgba(216, 213, 201, 0.55)` and `box-shadow: 0 4px 20px rgba(34, 77, 149, 0.03)`.
  - Content, icons, badges, sorting bars, and code cards passing beneath the sticky navbar now showcase dynamic liquid glass refraction without any background color flickering or gradient shifts.

### Verified
- Updated `tests/verify_nav_animation.py` to assert identical liquid glass background across all states.
- Master test runner `tests/run_all_tests.py` ran with 100% pass rate across all 9 suites.

---

## [2026-11-06 — Page Refresh Transition Flash Elimination]

### Fixed
- **Refresh & Anchor State Synchronization**:
  - Eliminated the initial transition flash where refreshing the page midway down would briefly render the full brand text at the origin and then visibly animate it into the scrolled position.
  - Added parse-time synchronous script in `index.html` to evaluate `window.pageYOffset` and `window.location.hash` before the initial layout paint, applying `.is-scrolled` immediately.
  - Added `.no-transition` CSS rule in `css/home.css` that disables all transitions on the navbar during initial load and browser scroll restoration.
  - Upgraded `js/home-nav.js` to seamlessly release `.no-transition` right after the initial layout cycle, ensuring all subsequent user scrolls transition smoothly and responsively.

### Verified
- Added `tests/test_refresh_sync.py` verifying deep-link/refresh immediate `.is-scrolled` rendering and subsequent transition enablement.
- Master test runner `tests/run_all_tests.py` ran with 100% pass rate across all 9 suites.

---

## [2026-11-06 — Navbar Jitter Elimination & Zero Layout Shift]

### Fixed
- **Navbar Jitter & Animation Feedback Loop**:
  - Eliminated the 14px vertical height jumping caused by padding differences between default and scrolled states. Locked `.home-nav` and `.home-nav.is-scrolled` to an identical `padding: 16px 0` (`10px 0` on mobile), achieving zero cumulative layout shift (0px delta).
  - Upgraded `js/home-nav.js` with dual-threshold scroll hysteresis (`SCROLL_DOWN_THRESHOLD = 45`, `SCROLL_UP_THRESHOLD = 15`). The 30px deadband prevents state flipping, oscillation, and getting stuck in animation loops when the user scrolls near the top.
  - Added hardware acceleration `will-change: transform;` on `.brand-mark` and `will-change: max-width, opacity, transform;` on `.home-brand-text` for smooth GPU compositing.

### Verified
- Added `tests/verify_zero_layout_shift.py` confirming 0px height difference and 0px hero displacement across states.
- Added `tests/test_hysteresis.py` confirming stable deadband behavior and absence of flickering.
- Master test runner `tests/run_all_tests.py` ran with 100% pass rate across all 8 suites.

---

## [2026-11-06 — Navbar Hero Background Merge & Snappier Logo Animation]

### Changed
- **Seamless Hero Integration**:
  - Configured default `.home-nav` background and border-bottom to `transparent` with `backdrop-filter: none`, eliminating the hard horizontal boundary and allowing the hero section's ambient radial gradients (ellipse glows) to flow seamlessly behind the navbar.
  - Floating scrolled state (`.home-nav.is-scrolled`) smoothly applies frosted glass (`rgba(245, 243, 237, 0.88)` with `blur(16px)` and subtle border `rgba(216, 213, 201, 0.45)`) only when the user scrolls down through page content.
- **Faster Logo Scroll Animation**:
  - Increased transition speed by decreasing duration from `0.45s` to `0.22s` (`cubic-bezier(0.2, 0.8, 0.2, 1)`), making the brand mark translation and text fade/expansion feel snappy and instantaneous when scrolling back towards the top.

### Verified
- Added `tests/verify_nav_animation.py` checking initial transparency, scrolled minimization, restored top state, and transition timings in headless Chrome.
- Master test runner `tests/run_all_tests.py` ran with 100% pass rate.

---

## [2026-11-06 — Sticky Navbar & Logo Scroll Transition]

### Added
- **Sticky Frosted-Glass Navbar**:
  - Pinned homepage navbar (`.home-nav`) to `top: 0` (`position: sticky`) with translucent frosted-glass blur (`backdrop-filter: blur(14px)`).
  - Added smooth anchor scrolling with `scroll-margin-top: 88px` on `#playgrounds` and `#try-it`.
- **CSS-Driven Logo Scroll Animation**:
  - When scrolling, `.home-brand-text` ("Searchify | DSA playground") smoothly fades out and blurs, while `.brand-mark` (`[S]`) glides smoothly rightward into the space where the text was.
  - When scrolling back to the top, the logo mark returns to its starting position and the full site name fades back in.
  - Built with pure hardware-accelerated CSS transitions, driven by a minimalist 20-line scroll state controller (`js/home-nav.js`).

---

## [2026-11-06 — Production Deployment Guide & Hosting Evaluation]

### Added
- **`DEPLOYMENT_STEPS.md`**:
  - Comprehensive guide covering hosting analysis, platform comparison, step-by-step setup, and verification.
  - Evaluated Vercel ("Versailles") vs. GitHub Pages vs. Cloudflare Pages vs. Netlify for static DSA visualizer hosting.
  - Web dashboard and CLI deployment instructions.
  - Optional `vercel.json` recipe for clean URLs and security headers.
  - Updated `README.md` with link to deployment guide.

---

## [2026-11-04 — Friendly Guidance Notification for Empty Custom Input]

### Changed
- **Empty Custom Array Handling on "Apply"**:
  - In `searching-visualizer.js` and `sorting-visualizer.js`, clicking "Apply" with an empty input now surfaces a friendly guidance notification: `"No data is given. Tap on Generate for sample input."` instead of an erroneous `"Invalid input. Enter 2–40/80 comma-separated numbers..."` error toast.
  - Set notification type to `'info'`, displaying the clear royal blue information badge (`ℹ`) with a soft neutral border.
  - Maintained the strict format validation and error toast when the user actually supplies non-empty, malformed array input.
  - Added Enter key shortcut support (`keyup`) on the custom array input field to apply values conveniently.

### Verified
- Extended `tests/verify_center_notification.py` with headless Chrome live click interactions for both `searching.html` and `sorting.html`.
- Master test runner `tests/run_all_tests.py` ran with 100% pass rate across all suites.

---

## [2026-10-30 — Homepage Visual Transformation: Interactive Algorithm Playground]

### Added
- **Bricolage Grotesque Typography**:
  - Replaced Kalam/Caveat handwritten font on the homepage with bold, expressive **Bricolage Grotesque** headings and **Inter** body text.
- **Hero Container Elevation**:
  - Preserved the large rounded rectangular container concept (`border-radius: 36px`) and added a subtle radial dotted grid texture (`24px 24px`) with soft ambient shadows.
  - Added a minimal brand mark at top (`AlgoViz • Interactive DSA Playground`).
- **Searching Playground Card**:
  - Magnifying glass icon SVG with hover scale and soft pink tint.
  - Miniature animated array visualization with target pill (`Target: 45`) and 5 array cells (`14, 28, 45, 62, 89`).
  - Interactive step-scanning hover animation: Scans cells 0 and 1, then locks onto match cell 2 in emerald green (`#27AE60`) with checkmark `✓` badge.
  - Descriptive line: *"Find elements, one step at a time."*
  - Action link with animated explore arrow (`Explore →`).
- **Sorting Playground Card**:
  - Bar chart icon SVG with hover scale.
  - Miniature animated vertical bars (`70%, 30%, 90%, 20%, 50%`).
  - Interactive hover animation: Bars smoothly rearrange into sorted ascending heights (`20%, 30%, 50%, 70%, 90%`) with cubic-bezier spring curve and transition into emerald green (`#27AE60`).
  - Descriptive line: *"Watch elements find their place."*
  - Action link with animated explore arrow (`Explore →`).
- **Interactive Micro-Interactions**:
  - Card hover elevation (`translateY(-8px)`), vibrant pink border glow (`#D93D81`), icon scale (`1.12`), and explore arrow slide.
  - Active press feedback (`transform: translateY(-2px) scale(0.99)`).
  - Full keyboard accessibility with `:focus-visible`.
  - Responsive stacking for tablets and mobile devices (`@media (max-width: 680px)`).
  - Reduced motion support via `@media (prefers-reduced-motion: reduce)`.
- **Automated Verification**:
  - Created `tests/verify_homepage.py` and integrated into the master test runner (`tests/run_all_tests.py`), verifying 100% pass rate with zero console errors.

---

## [2026-10-30 — Navbar Notification Pill Integration]
- Moved notification pill to the navbar at the top, leaving canvas bars completely unobstructed.

---

## [2026-10-30 — Center Screen Notification Redesign]
- Initial center-screen notification implementation with Pantone palette styling and 2.5s auto-dismissal.

---

## [2026-10-30 — Visualizer Layout Restructuring: Full-Width Canvas & Below-Canvas Learning]
- Removed right-hand sidebar and pseudocode, expanded canvas to full width, and organized below-canvas learning sections.

---

## [2026-10-30 — Complete UI/UX Transformation: Algorithm Playground]
- Grouped toolbar into visual clusters, added dotted grid canvas, floating status pills, completion celebration banners, structured explanation cards, and compact counter cards.

---

## [2026-10-30 — Visual Redesign Upgrade]
- Upgraded design system to Pantone-inspired palette (Warm Ivory, Soft Cream, Royal Blue, Vibrant Pink).

---

## [2026-10-30 — Initial AlgoViz Release]
- Initial implementation of AlgoViz with 5 sorting algorithms and 2 searching algorithms.
