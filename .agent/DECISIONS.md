# Architecture Decisions

## Decision 001
Date: 2026-10-30
Phase: Phase 0 — Discovery
Problem: Establish project runtime and architecture.
Decision: Vanilla Web (HTML5/CSS3/Vanilla JS) with zero server runtime dependencies.

## Decision 002
Date: 2026-10-30
Phase: Phase 1 — Foundation
Problem: Playback engine model.
Decision: Pre-computed step tracing for deterministic bidirectional scrubbing.

## Decision 003
Date: 2026-10-30
Phase: Phase 1 — Foundation
Problem: Homepage layout reference.
Decision: Minimalist two-card layout matching sketch with handwritten font.

## Decision 004
Date: 2026-10-30
Phase: Phase 5 — Visual Redesign
Problem: Brand identity and color system.
Decision: Pantone-inspired palette (Warm Ivory `#F5F3ED`, Soft Cream `#ECEBDB`, Royal Blue `#224D95`, Vibrant Pink `#D93D81`).

## Decision 005
Date: 2026-10-30
Phase: Phase 6 — Complete UI/UX Transformation
Problem: Transform into an interactive algorithm playground.
Decision: Clustered toolbars, dotted-grid canvas, floating status pills, completion banners, and structured learning cards.

## Decision 006
Date: 2026-10-30
Phase: Phase 7 — Visualizer Layout Restructuring

### Problem
The right-hand sidebar squeezed the visualization canvas into a narrower horizontal space, and the pseudocode panel added visual complexity that distracted students from the core visualization and explanation.

### Options Considered
1. Collapsible sidebar (drawer toggle).
   - Still forces sidebar mental model and complicates layout.
2. Complete removal of sidebar and pseudocode; full-width canvas with learning information and complexity cards placed below the canvas in a logical top-to-bottom flow.

### Decision
Option 2: Complete removal of sidebar and pseudocode; full-width visualization canvas.

### Layout Flow:
1. Header & Algorithm Selector
2. Controls Toolbar
3. Full-width Interactive Visualization Canvas
4. Step Progress Bar & Current Operation Pill
5. Side-by-side interactive grid: "What's Happening" (Explanation Card) & "Live Statistics" (Comparisons & Swaps)
6. Dedicated Algorithm Complexity Section:
   - Algorithm Title & Beginner-Friendly Description
   - 4 Complexity Cards (Best, Average, Worst, Space) in a clean grid
   - Stability, In-Place, and Requires-Sorted tags
   - Dedicated "When to Use" card with beginner explanation

### Reason
Gives the animation maximum horizontal canvas space to breathe, removes pseudocode clutter, and provides an intuitive, readable top-to-bottom learning journey.

### Consequences
The visualization is wider and more legible; bar widths scale cleanly; and learning information is organized below without cramped sidebars.


## Decision 007
Date: 2026-10-30
Phase: Phase 8 — Center Screen Notification Redesign

### Problem
Previously, notifications (such as "New array generated") appeared in the upper-right corner of the screen, which could easily be overlooked during active visualizer interaction and felt disconnected from the central learning canvas.

### Options Considered
1. Modal overlay with backdrop:
   - High visibility, but blocks user interaction and breaks playback flow.
2. Center-screen toast notification:
   - Fixed viewport centering (`top: 50%; left: 50%; transform: translate(-50%, -50%)`).
   - `pointer-events: none` ensuring user clicks are never blocked or intercepted.
   - Smooth entrance scale-up and fade transition, with 2.5-second dismissal.
   - Single container instance to eliminate stacking artifacts.

### Decision
Option 2: Center-screen non-blocking toast notification.

### Visual Styling:
- Background: Soft Cream (`#ECEBDB`).
- Text: Royal Blue (`#224D95`).
- Success Accent: Green badge (`#27AE60`) with checkmark (`✓`).
- Border: Subtle beige (`#D8D5C9`).
- Shadow: `0 12px 32px rgba(34, 77, 149, 0.16), 0 4px 12px rgba(37, 37, 37, 0.08)`.
- Z-Index: `10000`.

### Consequences
Provides clear, prominent, beautiful user feedback in the exact center of the screen without interrupting animation viewing or blocking user controls.


## Decision 008
Date: 2026-10-30
Phase: Phase 9 — Navbar Notification Pill Integration

### Problem
When the notification pill was centered in the middle of the viewport (`top: 50%`), it visually overlapped the vertical bars and numbers in the sorting playground canvas.

### Options Considered
1. Centered in canvas viewport:
   - Covers bars while visible, distracting the user.
2. Positioned in the navbar at the top:
   - `position: fixed; top: 12px; left: 50%; transform: translateX(-50%)`.
   - Anchored within the navbar header area.
   - Leaves the entire canvas and all bars completely unobstructed.
   - Refined to stadium pill shape (`border-radius: 9999px`) matching user reference screenshot.

### Decision
Option 2: Position notification pill horizontally centered in the navbar (`top: 12px`).

### Consequences
Zero obstruction of the visualization canvas bars, elegant pill aesthetic matching reference, seamless 2.5-second feedback in the header.


## Decision 009
Date: 2026-10-30
Phase: Phase 10 — Homepage Visual Transformation

### Problem
The initial homepage design was too plain, static, and empty. Kalam/Caveat handwritten typography felt inconsistent with a modern developer/student platform, and the two cards lacked visual demonstration of what Searching and Sorting do.

### Options Considered
1. Generic SaaS landing page with navbar, hero text, feature grids, and testimonials:
   - Violates minimalism and user constraint ("Do not add unnecessary navigation bars, hero heading, or promotional copy").
2. Interactive algorithm playground homepage:
   - Preserves original two-card layout (Searching & Sorting).
   - Upgrades typography to bold **Bricolage Grotesque** with Inter supporting copy.
   - Embeds miniature interactive algorithm visualizations inside the cards:
     - Searching: 5 array cells with target highlight (`Target: 45`) and sequential scan animation on hover.
     - Sorting: 5 vertical bars that smoothly rearrange into sorted ascending heights on hover.
   - Refines hero container with subtle radial grid texture, rounded corners (`36px`), and soft depth.

### Decision
Option 2: Interactive algorithm playground homepage.

### Consequences
Delivers an engaging, premium, playful educational experience that communicates the core concepts immediately upon hovering, while preserving 100% of the visualizer pages and algorithm logic intact.


## Decision 018
Date: 2026-11-08
Phase: Phase 40 — Five New Sorting Algorithms & Auxiliary Visualizations

### Problem
Searchify supported only five basic/classic sorting algorithms (Bubble, Selection, Insertion, Merge, Quick). The user requested expanding the platform with five additional algorithms: Heap Sort, Shell Sort, Counting Sort, Radix Sort (LSD), and Bucket Sort, including specialized auxiliary structural visualizations (Binary Heap Tree, Gap Sequence Tracker, Counting Arrays, Radix Digit Buckets, Value Range Buckets), full learning features, and a master 10-algorithm comparison matrix table.

### Architecture & Engineering Decisions
1. **Unified Step Generator Architecture**:
   - Each new algorithm is implemented in `js/sorting-algorithms.js` and produces standard step objects with `{ array, comparing, swapping, sorted, pivot, counters, explanation, pseudocodeLine, auxiliary }`.
   - The playback controller in `js/sorting-visualizer.js` consumes these steps deterministically, guaranteeing smooth forward/backward scrubbing, step-by-step navigation, and speed control.
2. **Negative Integers & Proportional Bar Heights**:
   - Extended custom array input range from `1 to 999` to `-999 to 999`.
   - Handled negative values in bar rendering via dynamic range normalization: `((val - minVal) / (maxVal - minVal || 1)) * (areaHeight - 24) + 14`.
   - Avoids negative CSS heights or collapsed bars; preserves exact visual relative proportions.
3. **Auxiliary Visualization Container**:
   - Implemented `#viz-auxiliary-panel` inside `#visualization-area` above the bars.
   - For auxiliary algorithms, `getUsableAreaHeight` reserves 110px on desktop (70px on mobile) to ensure bars never collide with auxiliary panels.
   - For classic 5 algorithms, reserved headroom remains 0px, maintaining 100% regression freedom.
4. **Binary Heap Tree Auxiliary**:
   - Displays up to 15 nodes across 4 heap levels (1, 2, 4, 8) with parent/child/swapping/extracted/sorted highlights.
5. **Shell Sort Gap Tracker**:
   - Tracks classic gap sequences (halving from $n/2$ down to 1), renders interactive gap pills, and highlights stride distance comparisons.
6. **Counting Sort Asc/Desc Stability**:
   - Supports negative numbers with minimum value offsets.
   - In descending order, reverse prefix sums compute counts of elements $\ge c$, mapped via `pos = workingCounts[cIdx] - 1` to guarantee stable placement.
7. **Radix Sort Negative Handling**:
   - Uses sign separation: partitions negative and non-negative numbers, sorts negative values by absolute values in reverse order via LSD digit buckets, and prepends them to the sorted non-negative list.
8. **Bucket Sort Generalization**:
   - Computes dynamic span $\Delta = (max - min) / k$, scatters elements into buckets, sorts each bucket using animated insertion passes, and concatenates.
9. **Master 10-Algorithm Comparison Matrix**:
   - Embedded below the canvas in the complexity section, comparing all 10 algorithms across Best, Average, Worst, Space, and Stability metrics, dynamically highlighting the active algorithm's row.

## Decision 019
Date: 2026-11-08
Phase: Phase 41 — Heap Sort Zero-Scroll & Layout Separation

### Problem
In the Heap Sort visualizer:
1. The auxiliary panel had `max-height: 125px; overflow-y: auto;`. The 4-level binary heap tree requires ~175px–195px to display all nodes, triggering an internal vertical scrollbar that forced the user to scroll inside the card to inspect parent/child relationships and heap operations.
2. In the 460px default canvas, the auxiliary panel extended down to ~228px, while tall array bars (up to 240px tall with labels positioned above them) rose into the same vertical zone, causing the heap tree card and array bars to visually collide and overlap.

### Options Considered
1. Shrink node sizes down to tiny dots (<14px) and squeeze the tree into <100px.
   - Degrades legibility, cuts off 2-digit/3-digit node values, and makes parent/child lines and swap states unreadable.
2. Dynamically expand the visualizer canvas height exclusively for Heap Sort, remove height constraints on the heap tree card (`overflow-y: visible`, `max-height: none`), introduce a clear stage divider, and calibrate usable bar height.

### Decision
Option 2: Algorithm-scoped canvas expansion with two-tier layout separation and calibrated usable bar height.

### Engineering Details
1. **Dynamic Algorithm Layout Mode**:
   - `updateAlgorithmLayoutMode()` in `js/sorting-visualizer.js` toggles `.heap-sort-active` on `#visualization-area` and `.has-heap-sort` on `.viz-canvas-wrapper`.
   - `.viz-area.heap-sort-active` expands `min-height` to 570px (desktop), 550px (tablet), and 540px (mobile) with smooth `min-height: 0.25s ease` transitions.
   - Cleanly removed when switching to any other algorithm, restoring default 460px height.
2. **Unconstrained Heap Tree Card**:
   - `.viz-auxiliary-panel.heap-tree-mode` sets `max-height: none !important; height: auto !important; overflow: visible !important; overflow-y: visible !important;`.
   - All 4 levels (root, level 1, level 2, level 3) and up to 15 nodes render with zero scrolling (`scrollHeight <= clientHeight`).
3. **Dedicated Stage Divider**:
   - `<div class="heap-array-stage-divider">` provides a distinct visual boundary between the conceptual tree model above and the memory array bars below.
4. **Calibrated Headroom & Bar Height Capping**:
   - In `getUsableAreaHeight(areaEl)`:
     - Desktop: `Math.min(180, Math.max(100, rawHeight - 310))`
     - Mobile: `Math.min(95, Math.max(65, rawHeight - 340))`
   - Guarantees clearance of $\ge 35$px desktop and $\ge 20$px mobile (observed: 24.6px to 155.4px) between the tree card bottom and the highest bar label.

## Decision 020
Date: 2026-11-08
Phase: Phase 42 — Merged Visualizer Controls Layout Split

### Problem
In the visualizer pages (`sorting.html` and `searching.html`), all controls (Playback, Array Configuration, and Settings) were clustered in a single top toolbar above the canvas. This crowded the top header area and separated the playback actions (play, pause, step, reset, restart) and speed control from the animation display where the user's attention is focused. The user requested:
1. Merge the start/stop/reset/restart buttons with the speed control button.
2. Shift this merged controls dock just below the visualizer canvas.
3. Keep only the generate and applying options above the visualizer canvas.
4. Ensure both top and bottom control groups are horizontally centered.

### Decision
Split visualizer controls into a two-tier top/bottom architecture:
1. **Top Controls (`<nav class="viz-controls">`)**:
   - Houses only data creation & array configuration: Generate button, Custom Array text input, Apply button, Size slider, and Target input (searching).
   - Horizontally centered via `justify-content: center` and `margin: 0 auto`.
2. **Bottom Controls (`<nav class="viz-controls viz-controls-bottom">`)**:
   - Positioned immediately below `.viz-canvas-wrapper` and above `.progress-section`.
   - Merges Playback transport (`#play-btn`, `#prev-btn`, `#next-btn`), Reset/Restart (`#reset-btn`, `#restart-btn`), Speed slider (`#speed-slider`, `#speed-value`), and Sort order (`#asc-btn`, `#desc-btn` in sorting) into a unified dock card (`.merged-playback-cluster`).
   - Horizontally centered via `justify-content: center` and `margin: 0 auto`.
3. **Responsive Execution**:
   - Desktop: Single elegant horizontal row above and below canvas.
   - Mobile ($\le 860$px): Clean vertical wrapping with centered items, stacked transport and reset groups, and zero horizontal overflow. All interactive IDs and event bindings preserved 100%.

## Decision 021
Date: 2026-11-08
Phase: Phase 43 — Multi-Algorithm Sorting Comparison Showcase on Shared Array

### Problem
The user requested replacing the single-algorithm "GET HANDS-ON" demo on the homepage (`index.html`) with a section that allows users to select $N$ sorting techniques of their choice and showcases all selected algorithms sorting the EXACT same array simultaneously, allowing direct visual and performance comparison.

### Decision
1. **Homepage Section Overhaul**:
   - Replaced `.home-quick-demo` with `.home-showcase-section` under `#try-it`.
   - Added `home-demo-heading` class to preserve Aalto Display typography verification.
2. **Multi-Algorithm Dynamic Selection**:
   - Selector panel with 10 algorithm chips (`.showcase-chip`), displaying algorithm name and asymptotic complexity.
   - 5 convenient comparison presets: Top 3 (Popular), $O(n \log n)$ Trio, $O(n^2)$ Classic, Linear Time, and Compare All (10).
   - Allows users to select any subset of $1$ to $10$ algorithms simultaneously.
3. **Identical Shared Dataset**:
   - All active algorithms share and sort the exact same initial array data.
   - Provides Shuffle Array button and Custom Array text input to load any custom dataset across all cards synchronously.
4. **Synchronized Multi-Track Engine**:
   - Implemented standalone modular controller `js/multi-sort-showcase.js`.
   - Uses `window.SortingAlgorithms` step-generator engine directly with zero code duplication.
   - Lockstep playback with Start/Pause Race, Step Backward, Step Forward, Reset, and Speed multiplier slider (1x: 340ms to 4x: 30ms).
   - Real-time card animations with color-coded comparison (`#D93D81`), swap (`#E67E22`), pivot (`#8E44AD`), and sorted (`#27AE60`) states.
   - Real-time statistics per card: comparison counter, swap counter, step counter, progress bar, and operation explanation.
5. **Race Leaderboard & Comparison Summary**:
   - Dynamic race finish recording with rank badges (`🥇 1st`, `🥈 2nd`, `🥉 3rd`, etc.).
   - Comparison summary table/cards displaying final steps, comparisons, and swaps across all competing algorithms.
6. **Responsive Layout & Zero Overflow**:
   - CSS Grid with `repeat(auto-fit, minmax(min(280px, 100%), 1fr))` on desktop/tablet, and `minmax(0, 1fr)` on mobile.
   - Zero horizontal scroll across all desktop, tablet, and mobile devices (1280px, 768px, 412px, 375px).
