# Changelog

All notable changes to this project are documented in this file.

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
