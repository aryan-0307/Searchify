# Changelog

All notable changes to this project are documented in this file.

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
