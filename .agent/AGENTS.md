# AGENTS.md — Core Operating Rules

This file contains the foundational rules and operating principles that must ALWAYS be followed by any agent working in this repository.

---

## 1. Safety Rules

- **Never delete existing functionality** without explicit justification.
- **Never overwrite working code** blindly.
- **Never fabricate information.**
- **Never claim something works** without verification.
- **Never invent APIs, libraries, environment variables, database fields, or configuration.**
- **Never silently ignore errors.**
- **Never modify unrelated files.**
- **Never expose secrets.**
- **Never commit credentials, API keys, tokens, or private keys.**

---

## 2. Before Editing Protocol

Always execute these steps before modifying code:
1. **Inspect the relevant files** — Read and understand the existing code context.
2. **Understand the existing implementation** — Trace data flow and invariants.
3. **Check git status/diff** — Ensure working directory state is understood and clean.
4. **Identify dependencies** — Check what depends on this code and what this code depends on.
5. **Determine the smallest safe change** — Favor minimal, targeted alterations.

Ask internally:
- What requirement does this change satisfy?
- Which files need modification?
- Could this break existing functionality?
- How will I verify it?

---

## 3. After Editing Protocol

Always execute these steps after modifying code:
1. **Inspect the changed code** — Review diff against expectations.
2. **Run appropriate tests** — Verify both new functionality and existing regression tests.
3. **Run lint/type checking** when available.
4. **Run build** when appropriate.
5. **Fix discovered errors** immediately.
6. **Update `.agent/` documentation** — Reflect actual verified state.

Ask internally:
- Did I satisfy the requirement?
- Did I introduce a regression?
- Did tests pass?
- Did I modify anything unrelated?

---

## 4. Anti-Hallucination Hierarchy of Truth

When conflicting information arises, resolve using this strict priority hierarchy:

1. **LEVEL 1 — Actual filesystem / source code** (Ground truth)
2. **LEVEL 2 — Test / build / runtime evidence** (Observed behavior)
3. **LEVEL 3 — Git history / diff** (Recorded changes)
4. **LEVEL 4 — Project documentation** (Design documents, specs)
5. **LEVEL 5 — Agent state files** (`.agent/` memory files)
6. **LEVEL 6 — Conversation / context** (User requests and dialog)
7. **LEVEL 7 — Agent assumptions** (Lowest priority - must verify before relying on)

*If uncertain, state: `UNKNOWN — needs verification`. Never convert uncertainty into fact.*

---

## 5. Change Control & Preservation

- **User changes are sacred**: Never delete, revert, or overwrite existing user work without explicit instruction.
- **Minimal change principle**: `small change → test → verify → checkpoint`.
- **Traceability**: Every requirement maps to implementation, tests, and verification evidence.
- **No false completion**: Use `IMPLEMENTED + VERIFIED` instead of merely `IMPLEMENTED`.
