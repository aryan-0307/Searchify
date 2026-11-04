# AlgoViz — Interactive Sorting & Searching Playground

AlgoViz is a modern, playful, and premium educational platform designed to help students and developers master fundamental sorting and searching algorithms through tactile step-by-step animations, synchronized code editor pseudocode, live operation indicators, and interactive complexity analysis.

---

## Visual Identity & Design Vision

AlgoViz transforms traditional dry algorithmic learning into an engaging **interactive algorithm playground**:
- **Pantone-Inspired Color Identity**:
  - **Warm Ivory (`#F5F3ED`)**: Main background for pages and toolbars.
  - **Soft Cream (`#ECEBDB`)**: Secondary surfaces, container cards, headers, sidebars, and array cells.
  - **Royal Blue (`#224D95`)**: Primary brand color, headings, primary buttons, card borders, and normal array elements.
  - **Vibrant Pink (`#D93D81`)**: Interactive hover states, swapping animations, active search cells, and prominent play button highlights.
  - **Supporting Palette**: Dark text (`#252525`), Secondary text (`#686868`), Beige border (`#D8D5C9`), White canvas (`#FFFFFF`).
- **Interactive Playground Canvas**:
  - Dotted grid background pattern evoking an interactive visual laboratory.
  - Live floating operation badge dynamically tracking the algorithm's state (e.g. `Comparing 8 & 3`, `Swapping 8 ↔ 3`, `Pivot: 7`).
  - Satisfying completion banner with total comparisons, swaps, and a Replay button.
- **Modern Code Editor Pseudocode**:
  - Interactive pseudocode panel styled like a code editor with line numbers, keyword syntax highlighting, and active line auto-scrolling.
- **Rich Explanation Learning Cards**:
  - Contextual operation badges (`COMPARING`, `SWAPPING`, `PIVOT`, `SORTED`, `TARGET FOUND`), value chips, and plain-English next-step decisions.
- **Minimalist Reference Homepage**:
  - Strict preservation of the original sketch: full-screen rounded container, two centered handwritten cards (**Searching** on left, **Sorting** on right) in `Kalam` and `Caveat` with subtle hover lift and pink glow.

---

## Features & Supported Algorithms

### Sorting Playground
- **5 Core Algorithms**:
  - **Bubble Sort**: Adjacent element comparisons, swaps, and early-exit optimization.
  - **Selection Sort**: Tracks minimum values in unsorted partitions.
  - **Insertion Sort**: Shows sorted and unsorted partitions with shifting operations.
  - **Merge Sort**: Visualizes divide-and-conquer sub-array merging.
  - **Quick Sort**: Highlights pivot selection, partition passes, and final placement.
- **Playground Controls**:
  - **Array Controls**: Generate random arrays, custom array input with validation toasts, array size slider (5–50).
  - **Settings**: Animation speed slider (5 presets: Very Slow to Very Fast), Ascending / Descending order toggle.
  - **Playback Cluster**: Previous Step (`⏮`), Prominent Play/Pause (`▶`/`⏸`), Next Step (`⏭`), Reset, and Restart.
  - **Interactive Statistics Cards**: Live comparisons and swaps counters.
  - **Complexity Cards**: Separate cards for Best, Average, Worst Time, Space Complexity, Stability, In-Place, and "When to Use" guidance.

### Searching Playground
- **Linear Search**: Sequential cell examination with current examined cell (Vibrant Pink glow), checked cells (muted beige), and match confirmation (Emerald Green).
- **Binary Search**: Interactive Low (`#1E8449` Forest Green), Mid (`#224D95` Royal Blue), and High (`#D93D81` Vibrant Pink) pointer badges; auto-sorts unsorted input with user notification; visual range elimination.
- **Target Value Input**: Dynamic target detection, duplicate support, and missing target handling.

### Keyboard Shortcuts
- `Space`: Play / Pause
- `ArrowRight`: Next Step
- `ArrowLeft`: Previous Step
- `r` or `R`: Reset to initial array state

---

## Technology Stack

- **HTML5**: Semantic layout.
- **CSS3**: Custom properties, CSS Grid, Flexbox, dotted radial grid pattern, micro-interactions.
- **Vanilla JavaScript**: Pure ES6/ES5 modular architecture with zero external runtime dependencies.
- **Zero Node.js Dependency**: Runs directly in any modern browser via file opening or local Python HTTP server.

---

## File Structure

```
AlgoViz/
├── index.html                   # Minimalist reference-matched homepage
├── sorting.html                 # Sorting Playground interface
├── searching.html               # Searching Playground interface
├── css/
│   ├── style.css                # Global theme, buttons, inputs, chips, toasts, and badges
│   ├── home.css                 # Homepage layout, cards, and hover elevation
│   └── visualizer.css           # Playground canvas, dotted grid, bars, cells, and panels
├── js/
│   ├── main.js                  # Shared utilities (random array, input parsing, speed map)
│   ├── sorting-algorithms.js    # Step trace generator for 5 sorting algorithms
│   ├── searching-algorithms.js  # Step trace generator for linear & binary search
│   ├── sorting-visualizer.js    # Sorting playground controller and animation engine
│   └── searching-visualizer.js  # Searching playground controller and pointer manager
├── tests/
│   ├── test_algorithms.html     # 153-test browser unit test suite
│   ├── verify_pages.py          # DOM integrity verification script
│   ├── check_console_errors.py  # Headless Chrome console error audit script
│   └── verify_playground_features.py # Playground features verification script
├── .agent/                      # Antigravity Agent Operating System persistent memory
├── README.md                    # Project documentation
└── .gitignore                   # Workspace ignore rules
```

---

## Running Locally

Run Python's built-in HTTP server:
```powershell
python -m http.server 8000
```
Then navigate to **`http://localhost:8000`** in any web browser.

Alternatively, open `index.html` directly:
```powershell
Start-Process index.html
```

---

## Verification & Testing
- **153 / 153 Unit Tests Pass** in headless Google Chrome (`tests/test_algorithms.html`).
- **Zero Runtime Console Errors** across all pages.
- **DOM & Feature Integrity Verified** via Python automated scripts.
