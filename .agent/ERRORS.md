# Errors

This file tracks errors, root cause analyses, applied fixes, and verification statuses.

---

## Error 001

Date: 2026-10-30
Phase: Phase 0 — Discovery
Command/Action: `node --version`

### Error
`node : The term 'node' is not recognized as the name of a cmdlet, function, script file, or operable program.`

### Root Cause
Node.js runtime is not installed or not present in the system PATH.

### Fix
Adopted HTML5/CSS3/Vanilla JavaScript architecture with zero Node.js/npm dependencies, running directly in modern web browsers. Documented in `DECISIONS.md` under Decision 001.

### Verification
Visualizer and tests run directly in browser and headless Chrome without Node.

### Status
RESOLVED

---

## Error 002

Date: 2026-10-30
Phase: Phase 2 — Core Implementation
Command/Action: `invoke_subagent` for parallel algorithm generation

### Error
`RESOURCE_EXHAUSTED (code 429): Individual quota reached. Please upgrade your subscription to increase your limits.`

### Root Cause
System subagent API quota was reached when spawning multiple concurrent subagent instances.

### Fix
Completed the implementation of all algorithm generators and controllers directly within the primary agent session using direct write and edit tools.

### Verification
All algorithm modules, visualizers, and test suites created, verified, and passing 100%.

### Status
RESOLVED
