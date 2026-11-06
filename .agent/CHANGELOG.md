# Changelog

All notable changes to this project are documented in this file.

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
