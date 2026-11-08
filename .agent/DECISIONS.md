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
