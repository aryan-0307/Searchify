# Skills

This document describes the required agent capabilities and operating procedures for this repository.

---

## Repository Understanding
- Read existing architecture and directory structure before modifying anything.
- Identify entry points and execution flows.
- Identify dependencies and environment configurations.
- Identify test strategy and existing test suites.

## Coding
- Follow existing project conventions, style guides, and idioms.
- Prefer small, clean, maintainable, self-documenting changes.
- Avoid unnecessary refactoring or churn.
- Reuse existing utilities, standard library tools, and shared modules.
- Ensure type hints and robust docstrings are present where applicable.

## Debugging
- Reproduce the problem reliably with minimal test cases.
- Read and analyze the actual error stack trace and logs.
- Identify root causes before proposing or applying fixes.
- Apply the smallest reliable fix.
- Re-run failing tests and verify no regressions are introduced.

## Testing
- Unit tests: Test individual functions, edge cases, boundary conditions, and invalid inputs.
- Integration tests: Test multi-component interactions and pipeline flows.
- Regression tests: Ensure fixed bugs do not reoccur.
- Property-based and invariant testing: Verify algorithmic properties (e.g., sorted output, stability, search correctness).

## Security
- Never hardcode secrets, tokens, or credentials.
- Validate and sanitize all inputs.
- Follow the principle of least privilege.
- Avoid unsafe dependency usage and arbitrary code execution vulnerabilities.

## Git
- Inspect `git status` and `git diff` before and after changes.
- Keep commits and changes logically grouped with descriptive messages.
- Never discard or overwrite unrelated user modifications.
- Review full diff before marking any phase or task as complete.

## Documentation
- Update `.agent/` state files concurrently with code modifications.
- Record architectural decisions in `DECISIONS.md`.
- Document public APIs, complexity bounds, and usage examples.

## Algorithms & Data Structures (Domain-Specific)
- Correct implementation of sorting algorithms (QuickSort, MergeSort, HeapSort, TimSort, InsertionSort, etc.).
- Correct implementation of searching algorithms (Binary Search, Exponential Search, QuickSelect, etc.).
- Explicit time and space complexity verification (Best, Average, Worst case).
- Empirical benchmarking and correctness verification across diverse dataset topologies (random, sorted, reverse sorted, duplicates).
