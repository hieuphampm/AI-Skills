# Code Review Checklist

Consult this checklist during Step 3 of `code-review` execution. Prioritize correctness and security over stylistic preferences.

## 1. Correctness & Logic
- [ ] Boundary conditions handled (`null`/`None`, empty collections, zero, negative numbers, off-by-one).
- [ ] State transitions and invariants remain valid on both success and failure paths.
- [ ] Public API signatures, return types, and error contracts remain backward compatible (or breaking changes are intentional and documented).
- [ ] Timezones, encoding (UTF-8), and floating-point comparisons handled safely.

## 2. Security & Data Protection
- [ ] Untrusted inputs validated and parameterized (SQL, shell commands, HTML/XSS, path traversal, SSRF).
- [ ] Authentication and authorization checks enforced at every entry point (no IDOR / missing role checks).
- [ ] No hardcoded secrets, API keys, or sensitive PII in code, logs, or error responses.
- [ ] Safe deserialization and bounded resource allocation (timeouts, upload limits, pagination).

## 3. Reliability & Performance
- [ ] External I/O (HTTP, DB, files) uses timeouts, proper resource cleanup (`with` / `finally`), and explicit error handling.
- [ ] No silent exception swallowing (`except Exception: pass`).
- [ ] No obvious N+1 queries, unbounded in-memory buffering, or quadratic loops on user-controlled sizes.
- [ ] Concurrency hazards addressed (shared mutable state, lock ordering, idempotency).

## 4. Maintainability & Testing
- [ ] Changes are modular without duplicated business logic.
- [ ] New behaviors and bug fixes include targeted unit or integration tests covering failure modes.
- [ ] Comments explain *why* for non-obvious decisions rather than restating *what* the code does.
