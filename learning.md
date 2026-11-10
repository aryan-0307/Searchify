# Searchify — Complete Engineering & Architecture Reference Guide (`learning.md`)

Welcome to the complete, in-depth engineering manual for **Searchify** (an interactive Sorting and Searching Algorithm Visualizer and Comparison Laboratory).

This document breaks down every technology in the tech stack and every JavaScript function across the entire codebase. Each entry follows a rigorous 3-question format:
1. **What is it?**
2. **What does it do?**
3. **How does it do it?**

Read this guide to understand the complete architectural flow, design decisions, and implementation details so you can explain any part of the project with absolute confidence.

---

## High-Level Architecture Overview

Before diving into individual functions, understand the core architectural pattern powering Searchify:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        USER INPUT & EVENT LAYER                        │
│   (Click, Scrub Slider, Spacebar, Array Input, Speed, Algorithm Select) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ triggers
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      STEP-GENERATOR PATTERN (Pure)                      │
│        (js/sorting-algorithms.js & js/searching-algorithms.js)        │
│  - Executes algorithm synchronously in memory                          │
│  - Produces immutable timeline array: [Step 0, Step 1, Step 2, ... N] │
│  - Captures: array snapshot, comparing/swapping indices, counters,     │
│    explanation string, active pseudocode line, auxiliary data         │
│  - ZERO DOM access, 100% pure functional logic                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ delivers trace array
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 VISUALIZER PLAYBACK CONTROLLER (Stateful)               │
│   (js/sorting-visualizer.js, js/searching-visualizer.js, showcase)     │
│  - Maintains playback head index: currentStep ∈ [0, totalSteps - 1]    │
│  - Controls timer loop (setTimeout / requestAnimationFrame)            │
│  - Handles Play, Pause, Next, Prev, Reset, Speed multipliers           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ renders
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     REACTIVE DOM & SVG RENDERING                       │
│  - Translates currentStep snapshot into visual CSS bar heights         │
│  - Applies state classes: .comparing, .swapping, .sorted, .pivot       │
│  - Renders auxiliary components (Heap Tree SVG, Radix/Bucket Buckets)  │
│  - Updates counters, operation badges, progress bar, & code trace      │
└────────────────────────────────────────────────────────────────────────┘
```

### Why this architecture is superior:
1. **Decoupled Execution & Rendering**: The algorithms run instantly in zero milliseconds to create a full trace. You never have to pause a JavaScript `for` loop with `await sleep()`. 
2. **True Time-Travel Scrubbing**: Because steps are pre-computed snapshots, clicking "Previous Step" or dragging a timeline works backward and forward seamlessly with zero re-computation bugs.
3. **Multi-Track Simultaneous Racing**: The Comparison Showcase (`compare.html`) simply runs traces for $N$ different algorithms on the exact same array, then increments their step pointers in lockstep.

---

# PART I — THE TECHNOLOGY STACK

---

### HTML5 & Semantic Web Architecture
1. **What is it?**  
   The semantic markup foundation of the client-side application across all four core pages (`index.html`, `sorting.html`, `searching.html`, and `compare.html`).
2. **What does it do?**  
   Provides structured, accessible, search-engine-optimized (SEO) content landmarks (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<figure>`, `<aside>`, `<footer>`, `<dialog>`) and ARIA live regions for assistive technology.
3. **How does it do it?**  
   - Employs dedicated ARIA landmarks (`role="banner"`, `role="region"`, `aria-live="polite"`, `aria-atomic="true"`) to inform screen readers of dynamic algorithm state changes.
   - Eliminates `<div>` soup by grouping related components into semantic tags (e.g., `<figure class="mini-viz">`, `<hgroup class="viz-header-title-group">`).
   - Uses native HTML5 `<input type="range">`, `<input type="text">`, and semantic buttons for zero-dependency accessible form controls.

---

### CSS3 & The Searchify Design System
1. **What is it?**  
   A modular, vanilla stylesheet architecture defined across `css/style.css`, `css/home.css`, `css/visualizer.css`, and `css/learning-features.css`.
2. **What does it do?**  
   Enforces a consistent, retro-futuristic editorial aesthetic ("Warm Ivory" `#F5F3ED`, "Soft Cream" `#ECEBDB`, "Royal Blue" `#224D95`, "Vibrant Pink" `#D93D81`, and "Emerald Green" `#27AE60`) with smooth responsive layouts and 60fps animations.
3. **How does it do it?**  
   - **CSS Custom Properties (Variables)**: Centralizes palette colors, font stacks, and borders on `:root`.
   - **Modern Layouts**: Leverages CSS Grid (`grid-template-columns: repeat(auto-fit, minmax(...))`) and Flexbox for zero-overflow responsiveness from 320px mobile screens to 4K displays.
   - **Fluid Typography**: Employs `clamp()` functions (e.g., `font-size: clamp(34px, 11vw, 50px)`) to automatically scale headers without discrete media-query snapping.
   - **Frosted Glass Glassmorphism**: Utilizes `backdrop-filter: blur(20px) saturate(180%)` for sticky headers.
   - **Accessibility**: Includes `@media (prefers-reduced-motion: reduce)` overrides to suppress non-essential animations for users with motion sensitivity.

---

### Vanilla JavaScript (ES6+ / ES5 Modular Architecture)
1. **What is it?**  
   Pure, framework-free browser JavaScript organized using modular Immediately Invoked Function Expressions (IIFEs) running in `'use strict'` mode.
2. **What does it do?**  
   Powers all algorithm logic, step generation, DOM manipulation, playback timers, keyboard bindings, and data validation with zero dependencies, zero build steps, and zero bundler overhead.
3. **How does it do it?**  
   - Encloses private state and helper functions within IIFE closures: `(function () { 'use strict'; ... })();`.
   - Selectively exports clean public APIs onto global objects: `window.SearchifyUtils`, `window.SortingAlgorithms`, and `window.SearchingAlgorithms`.
   - Operates directly with the native browser DOM API (`querySelector`, `addEventListener`, `classList`), executing with maximum speed and near-zero memory footprint.

---

### SVG (Scalable Vector Graphics) Dynamic Engine
1. **What is it?**  
   Dynamic mathematical graphics markup rendered inline via JavaScript for mathematical coordinate plotting.
2. **What does it do?**  
   Renders the interactive Big-O Growth Curves chart in the Learning Lab and the Binary Heap Tree graph in Heap Sort.
3. **How does it do it?**  
   - Computes dynamic coordinate geometry in JavaScript using mathematical functions (e.g., $O(1) \rightarrow y = c$, $O(\log n) \rightarrow y = \log_2(x)$, $O(n \log n) \rightarrow y = x \log_2(x)$, $O(n^2) \rightarrow y = x^2$).
   - Normalizes coordinates into a defined SVG `viewBox="0 0 620 230"`.
   - Generates SVG `<path d="...">`, `<circle>`, `<line>`, and `<text>` elements with inline styling and appends them directly to the container.

---

### Web Storage API (`localStorage`)
1. **What is it?**  
   The browser's persistent key-value client-side storage mechanism.
2. **What does it do?**  
   Persists user learning progress, experience points (XP), completed algorithm runs, and unlocked achievement badges across browser refreshes.
3. **How does it do it?**  
   - Serializes JavaScript progress state into JSON: `localStorage.setItem('searchify-learning-progress-v1', JSON.stringify(progress))`.
   - Safely parses stored JSON on page initialization inside a `try...catch` block to handle disabled cookies, private browsing modes, or quota limits gracefully.

---

### Browser Timing & Animation APIs (`setTimeout` & `requestAnimationFrame`)
1. **What is it?**  
   Native browser asynchronous scheduling APIs.
2. **What does it do?**  
   Drives the step-by-step playback loop of sorting/searching visualizations and throttles scroll event calculations.
3. **How does it do it?**  
   - **Execution Loop**: Uses recursive `setTimeout` scheduling based on current speed settings (from 850ms down to 35ms per step). This allows instant pausing (`clearTimeout`), dynamic mid-flight speed adjustments, and non-blocking background processing.
   - **Scroll Throttling**: Uses `window.requestAnimationFrame()` in `js/home-nav.js` to batch layout queries and avoid scroll-jank or layout thrashing.

---

### Python 3 & Headless Chrome Testing Suite
1. **What is it?**  
   An automated 32-stage end-to-end regression test suite located in `tests/` driven by Python `subprocess` and headless Google Chrome.
2. **What does it do?**  
   Verifies algorithmic correctness (644 unit tests), DOM structure, semantic HTML5, zero console errors, viewport responsiveness across 4 screen sizes, and layout clearances.
3. **How does it do it?**  
   - Python launches Chrome with flags: `--headless=new --no-sandbox --disable-gpu --virtual-time-budget=8000 --dump-dom`.
   - Injects test harnesses and parses DOM output to assert layout bounding rectangles, horizontal scroll overflow (`scrollWidth <= clientWidth`), and algorithm execution outputs.

---

# PART II — CORE SHARED UTILITIES (`js/main.js`)

Attached to: `window.SearchifyUtils` (and alias `window.AlgoVizUtils`)

---

### `showNotification(message, type, duration)`
1. **What is it?**  
   The centralized toast notification manager.
2. **What does it do?**  
   Displays an animated, center-screen feedback pill to notify the user of actions (e.g., "Array generated!", "Target found!", or "Please enter valid numbers").
3. **How does it do it?**  
   - Queries `#notification` element in the DOM.
   - Cancels any active timeout via `clearTimeout(el._timeout)` to prevent overlapping dismissals.
   - Constructs an icon (`✓` for success, `✕` for error, `ℹ` for info) and text spans.
   - Forces a browser reflow (`void el.offsetWidth;`) to ensure the CSS keyframe scale/fade entrance animation reliably re-triggers.
   - Sets a timer (`duration` default 2500ms) to automatically remove the `.show` CSS class.

---

### `parseCustomArray(str)`
1. **What is it?**  
   A validation and parsing function for user-provided array inputs.
2. **What does it do?**  
   Transforms a comma-separated text string from an `<input>` field into a sanitized array of integers, or returns `null` if invalid.
3. **How does it do it?**  
   - Validates that the input string is not empty.
   - Splits on commas: `str.split(',')`.
   - Iterates through parts, converts each part using `Number(part.trim())`, checks `!isNaN(num) && isFinite(num)`.
   - Rounds floats using `Math.round(num)` and enforces boundary constraints: values must fall between `-999` and `999`.
   - Enforces array length constraints between `2` and `80` elements. Returns array of numbers if valid, `null` otherwise.

---

### `generateRandomArray(size, min, max)`
1. **What is it?**  
   Random dataset generator.
2. **What does it do?**  
   Creates a new array of integers of specified length within a given numerical range.
3. **How does it do it?**  
   - Defaults `min = 5` and `max = 100` if omitted.
   - Loops `size` times and calculates: `Math.floor(Math.random() * (max - min + 1)) + min`.
   - Pushes random values into a new array and returns it.

---

### `getSpeedMs(sliderValue)`
1. **What is it?**  
   A speed preset translator.
2. **What does it do?**  
   Converts an integer slider level (`1` to `6`) into a corresponding delay in milliseconds.
3. **How does it do it?**  
   Looks up the value in an internal dictionary:
   - `1` $\rightarrow$ 850ms (Slowest)
   - `2` $\rightarrow$ 500ms
   - `3` $\rightarrow$ 300ms
   - `4` $\rightarrow$ 160ms
   - `5` $\rightarrow$ 80ms
   - `6` $\rightarrow$ 35ms (Fastest)

---

### `getSpeedLabel(sliderValue)`
1. **What is it?**  
   Speed label formatter.
2. **What does it do?**  
   Returns the human-readable text multiplier label for a given slider value (e.g., `'1x'`, `'2x'`, `'6x'`).
3. **How does it do it?**  
   Maps the integer key to an internal lookup table `{ 1: '1x', 2: '2x', ..., 6: '6x' }`.

---

# PART III — NAVIGATION & SCROLL DYNAMICS (`js/home-nav.js`)

---

### `init()` (in `js/home-nav.js`)
1. **What is it?**  
   Navbar controller bootstrapper.
2. **What does it do?**  
   Initializes sticky navbar transitions, hysteresis scroll detection, and brand click-to-top functionality.
3. **How does it do it?**  
   - Finds `#home-nav` in the DOM.
   - Evaluates initial `window.pageYOffset` on page load to immediately apply `.is-scrolled` if refreshed down the page without showing transition flicker.
   - Binds passive scroll event listener and invokes `enableTransitions()` after initial paint.

---

### `update()` (in `js/home-nav.js`)
1. **What is it?**  
   Scroll position evaluator with hysteresis.
2. **What does it do?**  
   Adds or removes the `.is-scrolled` class on `#home-nav` to switch between full and compact frosted styles without flickering.
3. **How does it do it?**  
   - Implements two distinct thresholds to create a hysteresis deadband:
     - Downward threshold: `SCROLL_DOWN_THRESHOLD = 45`px.
     - Upward threshold: `SCROLL_UP_THRESHOLD = 15`px.
   - If scrolling down and `scrollY > 45px`, adds `.is-scrolled`.
   - If scrolling up and `scrollY <= 15px`, removes `.is-scrolled`.
   - The 30px gap prevents rapid class toggling (flickering/jitter) if the user scrolls near the boundary.

---

### `enableTransitions()`
1. **What is it?**  
   Transition flash suppressor.
2. **What does it do?**  
   Prevents CSS transitions from firing during initial page load/layout computation.
3. **How does it do it?**  
   Waits 40ms after `DOMContentLoaded` or `window.onload`, then removes the `.no-transition` CSS class from the navigation element.

---

# PART IV — HOMEPAGE INTERACTIVE DEMO (`js/home-demo.js`)

---

### `render(activeA, activeB, sorted)` (in `js/home-demo.js`)
1. **What is it?**  
   DOM renderer for the homepage Bubble Sort demo.
2. **What does it do?**  
   Renders 8 vertical bars with value labels, applying active comparing and sorted CSS states.
3. **How does it do it?**  
   - Clears `#home-demo-bars`.
   - Computes maximum value: `Math.max.apply(null, values)`.
   - Iterates through the array and creates a `div.home-demo-bar` per item.
   - Sets proportional percentage height: `style.height = (value / max * 100) + '%'`.
   - Adds `.is-active` if the index equals `activeA` or `activeB`, and `.is-sorted` if included in `sorted`.

---

### `status(message)` (in `js/home-demo.js`)
1. **What is it?**  
   Homepage demo status updater.
2. **What does it do?**  
   Updates the textual explanation badge above the demo bars.
3. **How does it do it?**  
   Finds `#home-demo-status` and sets its `textContent = message`.

---

### `stop()` (in `js/home-demo.js`)
1. **What is it?**  
   Playback canceller.
2. **What does it do?**  
   Halts any active Bubble Sort execution on the homepage and re-enables the Run button.
3. **How does it do it?**  
   Calls `clearTimeout(timer)`, sets `timer = null`, sets `busy = false`, and sets `root.querySelector('#home-demo-run').disabled = false`.

---

### `shuffle()` (in `js/home-demo.js`)
1. **What is it?**  
   Array randomizer using Fisher-Yates algorithm.
2. **What does it do?**  
   Shuffles the 8 demo numbers and resets the visual bars.
3. **How does it do it?**  
   - Halts any active sorting with `stop()`.
   - Runs Fisher-Yates shuffle: loops from `i = values.length - 1` down to `1`, picks random `j = Math.floor(Math.random() * (i + 1))`, and swaps `values[i]` with `values[j]`.
   - Renders neutral state via `render(-1, -1, [])`.

---

### `run()` & `tick()` (in `js/home-demo.js`)
1. **What is it?**  
   The homepage Bubble Sort animation runner.
2. **What does it do?**  
   Executes Bubble Sort step-by-step with visual comparisons and swap delays on the homepage.
3. **How does it do it?**  
   - Sets `busy = true` and disables the Run button.
   - Inside recursive `tick()`: compares adjacent elements `arr[j]` and `arr[j+1]`.
   - Calls `render(j, j+1, [])` and updates status to "Comparing X and Y".
   - If out of order, swaps elements, updates DOM, and schedules next comparison after 360ms.
   - When passes complete, marks all bars `.is-sorted` and updates status to "Sorted!".

---

# PART V — PURE SORTING ALGORITHMS ENGINE (`js/sorting-algorithms.js`)

Attached to: `window.SortingAlgorithms`  
All functions take `(inputArray, order)` where `order` is `'asc'` or `'desc'` and return an array of `Step` objects.

---

### `makeStep(arr, comparing, swapping, sorted, pivot, explanation, pseudocodeLine, counters, auxiliary)`
1. **What is it?**  
   The immutable step snapshot factory.
2. **What does it do?**  
   Creates a structured step object containing the exact state of the algorithm at a single discrete moment in time.
3. **How does it do it?**  
   Clones all arrays using spread syntax `[...arr]` and deep-clones auxiliary objects using `JSON.parse(JSON.stringify(auxiliary))` so subsequent algorithm mutations cannot corrupt historical steps.

---

### `outOfOrder(a, b, order)`
1. **What is it?**  
   Comparator logic helper.
2. **What does it do?**  
   Determines whether two adjacent/compared numbers violate the desired sorting order.
3. **How does it do it?**  
   Returns `a > b` when `order === 'asc'`, and `a < b` when `order === 'desc'`.

---

### `bubbleSort(inputArray, order)`
1. **What is it?**  
   Bubble Sort step generator.
2. **What does it do?**  
   Produces the step trace for Bubble Sort with optimized early-termination detection.
3. **How does it do it?**  
   - Runs nested passes: outer loop `i` from `0` to `n - 1`, inner loop `j` from `0` to `n - 1 - i`.
   - Emits a comparison step for indices `[j, j + 1]`.
   - If `outOfOrder(arr[j], arr[j+1])`, swaps elements, increments swap counter, and emits a swap step.
   - Tracks a boolean `swapped`. If no swaps occur in an entire pass, terminates early.
   - Emits a final step marking all indices sorted.

---

### `selectionSort(inputArray, order)`
1. **What is it?**  
   Selection Sort step generator.
2. **What does it do?**  
   Produces the step trace for Selection Sort, tracking the minimum (or maximum) element index per pass.
3. **How does it do it?**  
   - Outer loop `i` selects boundary between sorted and unsorted portions.
   - Sets candidate index `extremeIdx = i`.
   - Inner loop `j` from `i + 1` to `n`: compares `arr[j]` with `arr[extremeIdx]`.
   - If a new extreme is found, updates `extremeIdx = j`.
   - After scan, if `extremeIdx !== i`, swaps elements at `i` and `extremeIdx`.
   - Marks index `i` as sorted and proceeds.

---

### `insertionSort(inputArray, order)`
1. **What is it?**  
   Insertion Sort step generator.
2. **What does it do?**  
   Produces step trace for Insertion Sort, showing elements shifting right to insert key into sorted subarray.
3. **How does it do it?**  
   - Considers index `0` already sorted.
   - Loops `i` from `1` to `n - 1`, picking `key = arr[i]`.
   - Inner loop compares `key` with preceding elements `arr[j]` (where `j = i - 1` down to `0`).
   - Shifts `arr[j]` to `arr[j+1]` while elements are out of order with `key`.
   - Places `key` at its correct position `arr[j+1]`.
   - Emits comparison and shift steps for each operation.

---

### `mergeSort(inputArray, order)`
1. **What is it?**  
   Divide-and-conquer Merge Sort step generator.
2. **What does it do?**  
   Recursively splits array into halves, then merges sorted subarrays back into the main array.
3. **How does it do it?**  
   - Recursive helper `mergeSortRecursive(left, right)`.
   - Calculates `mid = Math.floor((left + right) / 2)`.
   - Recursively sorts left half and right half.
   - Inside `merge(left, mid, right)`: copies subarray into temp arrays `L` and `R`.
   - Compares elements from `L` and `R`, writing the smaller/larger back into original array `arr[k]`.
   - Emits comparison and overwrite steps at every merge pass.

---

### `quickSort(inputArray, order)`
1. **What is it?**  
   Lomuto-partitioning Quick Sort step generator.
2. **What does it do?**  
   Partitions array around a pivot element, placing smaller elements left and larger elements right.
3. **How does it do it?**  
   - Chooses last element as pivot: `pivot = arr[high]`.
   - Iterates `j` from `low` to `high - 1`. If `arr[j]` is in order with pivot, increments boundary `i++` and swaps `arr[i]` with `arr[j]`.
   - Finally swaps pivot `arr[high]` with `arr[i+1]`.
   - Emits pivot selection, comparison, and partition swap steps.
   - Recursively sorts `[low, i]` and `[i+2, high]`.

---

### `heapSort(inputArray, order)`
1. **What is it?**  
   Binary Heap Sort step generator.
2. **What does it do?**  
   Builds a Max Heap (or Min Heap for descending), repeatedly extracts the root, and restores the heap property.
3. **How does it do it?**  
   - Phase 1 (Build Heap): Loops from `Math.floor(n / 2) - 1` down to `0`, calling `heapify(n, i)`.
   - Phase 2 (Extract Root): Swaps root `arr[0]` with the last unsorted element `arr[i]`, shrinks heap boundary, and calls `heapify(i, 0)` on the reduced heap.
   - Generates auxiliary data `auxiliary: { heapSize, parent, leftChild, rightChild, largest, treeNodes }` representing tree parent-child pointers.

---

### `shellSort(inputArray, order)`
1. **What is it?**  
   Diminishing-gap Shell Sort step generator.
2. **What does it do?**  
   Performs gap-based interleaved insertion sorting with diminishing gaps until gap equals 1.
3. **How does it do it?**  
   - Starts with initial gap: `gap = Math.floor(n / 2)`.
   - Performs insertion sort on elements spaced `gap` apart.
   - Emits comparison and swap steps highlighting indices `j` and `j - gap`.
   - Reduces gap: `gap = Math.floor(gap / 2)` until `gap = 1` performs the final pass.
   - Emits auxiliary data `{ gap, sequence: [..., 4, 2, 1] }`.

---

### `countingSort(inputArray, order)`
1. **What is it?**  
   Non-comparison integer sorting generator.
2. **What does it do?**  
   Sorts integers in $O(n + k)$ time by counting frequencies of each value and writing them into order.
3. **How does it do it?**  
   - Finds `min` and `max` values across the array.
   - Handles negative numbers by using offset: `idx = val - min`.
   - Phase 1: Counts occurrences of each number into a `count` frequency array.
   - Phase 2: Computes cumulative counts (prefix sums) to determine output positions.
   - Phase 3: Traverses input backward to place elements stably into `output` array.
   - Emits auxiliary data `{ countArray, outputArray, min, max, phase }`.

---

### `radixSort(inputArray, order)`
1. **What is it?**  
   Least Significant Digit (LSD) Radix Sort generator.
2. **What does it do?**  
   Sorts integers digit-by-digit from ones place, tens place, hundreds place using stable counting passes.
3. **How does it do it?**  
   - Handles negative integers by separating negatives and non-negatives.
   - Finds maximum absolute value to determine number of digit positions $d$.
   - For exponent `exp = 1, 10, 100, ...`: extracts digit `Math.floor(Math.abs(val) / exp) % 10`.
   - Distributes elements into 10 digit buckets (`0` to `9`).
   - Flattens buckets back into array in stable order.
   - Emits auxiliary data `{ buckets: [[], [], ...], currentExp, digitPlaceName }`.

---

### `bucketSort(inputArray, order)`
1. **What is it?**  
   Distribution-based Bucket Sort generator.
2. **What does it do?**  
   Partitions elements into uniform value buckets, sorts each bucket with insertion sort, and concatenates.
3. **How does it do it?**  
   - Finds `min` and `max`. Computes bucket index: `Math.floor(((val - min) / range) * (numBuckets - 1))`.
   - Distributes elements into $k$ buckets.
   - Iterates through each bucket, sorting its contents using Insertion Sort.
   - Concatenates buckets back into the original array.
   - Emits auxiliary data `{ buckets: [[], ...], activeBucket, phase }`.

---

# PART VI — SORTING VISUALIZER UI CONTROLLER (`js/sorting-visualizer.js`)

---

### `cacheElements()` (in `js/sorting-visualizer.js`)
1. **What is it?**  
   DOM element caching utility.
2. **What does it do?**  
   Caches all necessary DOM element references into a central `el` dictionary to prevent repetitive DOM queries during animation.
3. **How does it do it?**  
   Stores references: `el.vizArea = document.getElementById('visualization-area')`, `el.playBtn`, `el.prevBtn`, `el.nextBtn`, `el.speedSlider`, etc.

---

### `getUsableAreaHeight(areaEl)`
1. **What is it?**  
   Dynamic responsive canvas height calculator.
2. **What does it do?**  
   Calculates the exact pixel height available for rendering bars without overflowing into status pills or auxiliary panels.
3. **How does it do it?**  
   - Inspects `window.innerWidth` to detect desktop vs mobile.
   - If `currentAlgorithm === 'heapSort'`, reserves clearance for the SVG Heap Tree card.
   - If auxiliary algorithms (Shell, Counting, Radix, Bucket) are active, deducts auxiliary reservation height.
   - Returns calibrated bar rendering height (guaranteeing $\ge 20$px–70px clearance below status badges).

---

### `bindEvents()` (in `js/sorting-visualizer.js`)
1. **What is it?**  
   Event listener binder.
2. **What does it do?**  
   Hooks up user interactions (buttons, sliders, inputs, keyboard shortcuts, window resize) to handler functions.
3. **How does it do it?**  
   Attaches listeners: `el.playBtn.addEventListener('click', onPlayPause)`, `document.addEventListener('keydown', handleKeydown)`, `window.addEventListener('resize', handleResize)`.

---

### `onAlgorithmChange()` / `computeSteps()` (in `js/sorting-visualizer.js`)
1. **What is it?**  
   Algorithm switch and execution runner.
2. **What does it do?**  
   Reads user's selected algorithm from `<select>`, executes it via `window.SortingAlgorithms`, and resets visualizer state.
3. **How does it do it?**  
   - Reads `currentAlgorithm = el.algoSelect.value`.
   - Calls `steps = window.SortingAlgorithms[currentAlgorithm](currentArray, sortOrder)`.
   - Resets `currentStep = 0`, pauses playback, renders step 0, and updates complexity tables.

---

### `play()` / `pause()` / `advanceStep()`
1. **What is it?**  
   The animation playback engine.
2. **What does it do?**  
   Starts, stops, or advances the visual playback of algorithm steps across the timeline.
3. **How does it do it?**  
   - `play()` sets `isPlaying = true`, updates button icon to Pause (`⏸`), and calls `advanceStep()`.
   - `advanceStep()` renders `renderStep()`, increments `currentStep++`, and if `currentStep < steps.length`, schedules itself via `playTimer = setTimeout(advanceStep, speed)`.
   - `pause()` calls `clearTimeout(playTimer)` and sets `isPlaying = false`.

---

### `renderStep()` & `renderBars(arr, animateDrop)`
1. **What is it?**  
   Primary canvas renderer.
2. **What does it do?**  
   Draws the array bars for the current step, applying color-coded status classes.
3. **How does it do it?**  
   - Retrieves `step = steps[currentStep]`.
   - Calculates bar heights proportional to `Math.max(...arr)`.
   - Assigns CSS classes:
     - `.comparing` (Pink `#D93D81`) if index is in `step.comparing`.
     - `.swapping` (Orange `#E67E22`) if index is in `step.swapping`.
     - `.pivot` (Purple `#8E44AD`) if index is in `step.pivot`.
     - `.sorted` (Green `#27AE60`) if index is in `step.sorted`.
   - Calls `updateStatusPill(step)`, `updateExplanationCard(step)`, and `updateCounters()`.

---

### `renderHeapTree(aux, step)`
1. **What is it?**  
   Binary Heap Tree visualization renderer.
2. **What does it do?**  
   Renders an interactive tree diagram above the bars during Heap Sort, showing parent-child node relationships.
3. **How does it do it?**  
   - Generates tree levels using binary indices: root at index 0, left child at `2i + 1`, right child at `2i + 2`.
   - Positions node circles dynamically across horizontal tree levels.
   - Highlights comparing parent/child nodes in pink/orange matching the array bars below.

---

### `renderCountingAux(aux, step)` / `renderRadixAux` / `renderBucketAux`
1. **What is it?**  
   Specialized auxiliary structure visualizers.
2. **What does it do?**  
   Renders the secondary data structures used by non-comparison sorting algorithms (Frequency array for Counting Sort, Digit Buckets 0–9 for Radix Sort, Value Range Buckets for Bucket Sort).
3. **How does it do it?**  
   - Injects dedicated containers into `#auxiliary-visualization`.
   - In Radix Sort, renders 10 buckets labelled `0` through `9`, animating numbers flying into their digit buckets and collecting back.
   - In Counting Sort, renders the frequency array showing live count increments and cumulative prefix sums.

---

# PART VII — PURE SEARCHING ALGORITHMS ENGINE (`js/searching-algorithms.js`)

Attached to: `window.SearchingAlgorithms`

---

### `linearSearch(inputArray, target)`
1. **What is it?**  
   Linear Search step generator.
2. **What does it do?**  
   Generates step trace sequentially scanning every element from index 0 to $n - 1$ until the target is found or search completes.
3. **How does it do it?**  
   - Loops `i` from `0` to `n - 1`.
   - Sets `current = i`, increments `comparisons++` and `elementsExamined++`.
   - Emits a step comparing `arr[i]` with `target`.
   - If `arr[i] === target`, emits a success step with `found = i` and exits.
   - If loop ends without match, emits a `notFound = true` step.

---

### `binarySearch(inputArray, target)`
1. **What is it?**  
   Binary Search step generator.
2. **What does it do?**  
   Generates step trace for logarithmic search, halving the search window at each step on sorted data.
3. **How does it do it?**  
   - Automatically ensures array is sorted ascending.
   - Sets pointers: `low = 0`, `high = n - 1`.
   - While `low <= high`:
     - Calculates middle index: `mid = Math.floor((low + high) / 2)`.
     - Emits step highlighting `mid` and marking active window `[low...high]`.
     - If `arr[mid] === target`, records `found = mid` and terminates.
     - If `arr[mid] < target`, eliminates left half: `low = mid + 1`.
     - If `arr[mid] > target`, eliminates right half: `high = mid - 1`.
   - Marks eliminated indices in `step.eliminated` so the UI can fade them out.

---

# PART VIII — SEARCHING VISUALIZER UI CONTROLLER (`js/searching-visualizer.js`)

---

### `renderStep()` (in `js/searching-visualizer.js`)
1. **What is it?**  
   Searching visualizer canvas renderer.
2. **What does it do?**  
   Renders array cells with pointer badges (`Low`, `Mid`, `High`, `Current`), styling eliminated and found cells.
3. **How does it do it?**  
   - Obtains `step = steps[currentStep]`.
   - Renders each number in a cell.
   - Injects pointer badges above the cells:
     - For Binary Search: adds floating badges for `L` (`low`), `M` (`mid`), `H` (`high`).
     - For Linear Search: adds `Current` pointer badge.
   - Applies `.is-eliminated` (dim opacity and strike-through styling) to indices in `step.eliminated`.
   - Applies `.is-found` (vibrant green animation) when `step.found === index`.

---

### `onAlgorithmChange()` (in `js/searching-visualizer.js`)
1. **What is it?**  
   Search algorithm selector listener.
2. **What does it do?**  
   Switches between Linear and Binary Search, automatically sorting array when Binary Search is chosen.
3. **How does it do it?**  
   - Checks `el.algoSelect.value`.
   - If `'binarySearch'` is selected, runs `currentArray.sort((a, b) => a - b)`.
   - Displays a guidance toast: `"Array was sorted automatically for Binary Search"`.
   - Re-computes steps and resets canvas.

---

# PART IX — MULTI-ALGORITHM COMPARISON SHOWCASE (`js/multi-sort-showcase.js`)

Powers the interactive comparison on `compare.html`.

---

### `init()` (in `js/multi-sort-showcase.js`)
1. **What is it?**  
   Comparison showcase bootstrapper.
2. **What does it do?**  
   Initializes the 10 algorithm chips, applies default preset ("Top 3 Popular"), caches DOM nodes, computes initial traces, and renders track cards.
3. **How does it do it?**  
   - Invokes `cacheDOM()`, `renderChips()`, `bindEvents()`.
   - Initializes with `defaultArray = [68, 24, 91, 45, 12, 78, 36, 83, 52, 19]`.
   - Computes trace for all selected algorithms and renders the multi-card grid.

---

### `toggleAlgoSelection(algoId)`
1. **What is it?**  
   Algorithm chip toggler.
2. **What does it do?**  
   Adds or removes an algorithm from the active comparison race.
3. **How does it do it?**  
   - Prevents deselecting the last active algorithm (minimum 1 required).
   - If present, removes `algoId` from `selectedAlgos`.
   - If absent, pushes `algoId` into `selectedAlgos`.
   - Invokes `recomputeTraces()` and `renderGrid()`.

---

### `applyPreset(presetKey)`
1. **What is it?**  
   Comparison preset loader.
2. **What does it do?**  
   Instantly selects a curated group of algorithms for comparison with one click.
3. **How does it do it?**  
   Maps `presetKey` to `PRESETS`:
   - `popular` $\rightarrow$ `['bubbleSort', 'mergeSort', 'quickSort']`
   - `nlogn` $\rightarrow$ `['mergeSort', 'quickSort', 'heapSort']`
   - `n2` $\rightarrow$ `['bubbleSort', 'selectionSort', 'insertionSort']`
   - `linear` $\rightarrow$ `['countingSort', 'radixSort', 'bucketSort']`
   - `all` $\rightarrow$ All 10 algorithms.
   - Updates `selectedAlgos`, recalculates traces, and updates UI chips.

---

### `recomputeTraces()` (in `js/multi-sort-showcase.js`)
1. **What is it?**  
   Multi-algorithm execution manager.
2. **What does it do?**  
   Executes every selected algorithm on the **exact same shared dataset** and calculates timeline bounds.
3. **How does it do it?**  
   - Iterates through `selectedAlgos`.
   - Calls `window.SortingAlgorithms[algoId](sharedArray.slice(), 'asc')`.
   - Saves trace into `traces[algoId]`.
   - Calculates `maxStepsAcrossSelected = Math.max(...lengths)` to determine when all competing algorithms finish.

---

### `renderAllTracksAtStep(stepIdx)`
1. **What is it?**  
   Synchronized multi-track frame renderer.
2. **What does it do?**  
   Updates all active algorithm cards simultaneously at the current timeline step.
3. **How does it do it?**  
   - Iterates through `selectedAlgos`.
   - For each algorithm, clamps `stepIdx` to its own trace length (if an algorithm finishes earlier than others, it stays in its final sorted state).
   - Records algorithm finish order: when an algorithm finishes, logs timestamp into `finishRankings` array with rank badges (`🥇 1st`, `🥈 2nd`, `🥉 3rd`).
   - Updates miniature bar heights, comparison counts, and operation descriptions for each card.
   - When all algorithms complete, reveals the dynamic `#showcase-leaderboard`.

---

### `renderLeaderboard()` (in `js/multi-sort-showcase.js`)
1. **What is it?**  
   Race leaderboard generator.
2. **What does it do?**  
   Displays a comparative efficiency breakdown table ranking algorithms by speed and operations on the identical data.
3. **How does it do it?**  
   - Sorts completed algorithms by finish time/steps: `finishRankings.sort(...)`.
   - Renders leaderboard rows displaying rank, algorithm name, total steps taken, comparison count, and swap count.
   - Makes efficiency differences (e.g., Quick Sort $O(n \log n)$ vs Bubble Sort $O(n^2)$) crystal clear to the user.

---

# PART X — EDUCATIONAL LAB, BIG-O SVG & XP ENGINE (`js/learning-features.js`)

---

### `complexitySVG(n)`
1. **What is it?**  
   Dynamic Big-O SVG coordinate plotter.
2. **What does it do?**  
   Draws an interactive vector coordinate graph visualizing asymptotic growth curves with a live movable $n$ cursor.
3. **How does it do it?**  
   - Defines series functions:
     - $O(1)$: `fn = () => 1` (Pink)
     - $O(\log n)$: `fn = (x) => Math.log2(x)` (Blue)
     - $O(n)$: `fn = (x) => x` (Green)
     - $O(n \log n)$: `fn = (x) => x * Math.log2(x)` (Gold)
     - $O(n^2)$: `fn = (x) => x * x` (Purple)
   - Computes $(x, y)$ SVG coordinate points for $x \in [1, 20]$.
   - Generates SVG `<path>` elements using path data syntax (`M x y L x y ...`).
   - Draws a dashed vertical cursor line at the current value of the $n$-slider.

---

### `renderCodeTrace(algo)` & `highlightTraceStep(detail)`
1. **What is it?**  
   Synchronized pseudocode execution tracer.
2. **What does it do?**  
   Renders formatted pseudocode and highlights the exact line currently executing in real-time.
3. **How does it do it?**  
   - Fetches pseudocode string array from `window.SortingAlgorithms.pseudocode[algo]`.
   - Renders each line inside `<div class="sf-trace-line" data-line="i">`.
   - During visualizer playback, `highlightTraceStep()` removes `.is-active` from previous lines and adds `.is-active` to the line matching `step.pseudocodeLine`.

---

### `awardRun()` & `updateProgress()`
1. **What is it?**  
   Gamified XP and badge reward manager.
2. **What does it do?**  
   Awards experience points (XP) and unlocks achievement badges when the user completes algorithm runs or quizzes.
3. **How does it do it?**  
   - Increments `progress.xp += 25` and `progress.completedRuns++`.
   - Evaluates badge criteria (e.g., `'First Run'`, `'Algo Explorer'`, `'Sorting Master'`).
   - Saves to `localStorage` via `save()`.
   - Updates XP progress counter and renders badges in the UI.

---

# PART XI — DEVELOPER & INTERVIEW CONFIDENCE CHEAT SHEET

When asked about the code in Searchify, use these exact talking points:

### 1. "Why didn't you use React, Vue, or Angular?"
> *"Searchify was deliberately engineered with Vanilla JavaScript to avoid the virtual DOM overhead and bundle weight of heavy frameworks. In algorithm visualizers, you need fine-grained, 60fps control over DOM transformations and coordinate animations. By pre-computing algorithm steps into immutable trace objects and rendering them via direct DOM and SVG manipulation, we achieve instant time-travel scrubbing, zero frame drops, and sub-second page loads with zero external dependencies."*

### 2. "How does the Step-Generator pattern work?"
> *"Instead of slowing down an algorithm with async sleep loops, our algorithm functions (`js/sorting-algorithms.js`) are pure and synchronous. They execute instantly, returning an array of snapshot objects. Each snapshot records the array values, comparing indices, swap indices, sorted indices, explanation text, and active pseudocode line. The playback controller simply increments or decrements a pointer through this array. This makes Previous Step, Next Step, Reset, and Speed adjustments trivial and bug-free."*

### 3. "How do you handle non-comparison algorithms like Counting, Radix, or Bucket Sort?"
> *"Non-comparison algorithms cannot be visualized with simple bar height swaps alone. In `js/sorting-algorithms.js`, we attach an `auxiliary` object to each step. For Counting Sort, this captures the frequency array and prefix sums. For Radix Sort, it captures the 10 digit buckets ($0$–$9$). For Heap Sort, it captures binary tree parent-child pointers. The visualizer renderer (`js/sorting-visualizer.js`) inspects this auxiliary payload and dynamically renders SVG trees, bucket trays, or count tables alongside the main bars."*

### 4. "How does the multi-algorithm race work on `compare.html`?"
> *"All selected algorithms run against the exact same initial array. `js/multi-sort-showcase.js` calls `window.SortingAlgorithms` for each selected algorithm, caching their individual step traces. A single synchronized playback loop advances all tracks together. When an algorithm reaches its final step, its finish time is logged to dynamic leaderboard rankings (`🥇 1st`, `🥈 2nd`, etc.), comparing real-world operation counts on identical data."*

### 5. "How do you ensure responsiveness and avoid scroll-jank?"
> *"All layouts utilize CSS Grid with `minmax()` and `clamp()` to eliminate horizontal overflow across all viewports from 375px mobile screens to desktop. In `js/home-nav.js`, scroll listeners use `requestAnimationFrame` with a dual-threshold hysteresis deadband (15px to 45px), preventing visual jitter. In addition, canvas height calculations dynamically subtract auxiliary component heights to guarantee that bars and labels never overlap status badges or controls."*

---
*Generated for Searchify — DSA Interactive Learning Laboratory.*
