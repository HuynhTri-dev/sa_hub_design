<!--
name: Documentation Readiness & Pre-Code Gatekeeper Standard
description: Enforces thorough inspection of the docs directory and mandatory alignment on business and technical specifications before completing design or transitioning to code execution.
-->

# Documentation Readiness & Pre-Code Gatekeeper Standard

## 1. Core Objective
Before declaring a system design complete or allowing any transition to code execution (Code Mode), the Agent MUST audit the project documentation in the `@docs/` directory to ensure all business logic, architectural blueprints, data models, API contracts, and security policies are 100% complete, unambiguous, and aligned with the user.

---

## 2. Mandatory Pre-Code Documentation Audit Workflow

Whenever preparing to finalize designs or transitioning towards implementation:

```
                  ┌─────────────────────────────────────┐
                  │ 1. Search & Inventory @docs/ folder │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │ 2. Audit against Required Blueprints│
                  └──────────────────┬──────────────────┘
                                     │
                   ┌─────────────────┴─────────────────┐
                   ▼                                   ▼
        [Any Gaps / Ambiguities?]             [All Complete & Validated?]
                   │                                   │
                   ▼                                   ▼
   ┌───────────────────────────────┐   ┌───────────────────────────────┐
   │ 3. HALT & Ask User for Clarify│   │ 4. Request Explicit Sign-off  │
   │    (Do NOT assume or code)    │   │    from User to proceed       │
   └───────────────────────────────┘   └───────────────────────────────┘
```

### Step 1: Inventory Verification (`@docs/` Inspection)
The Agent must scan the `@docs/` directory and verify that all necessary specification artifacts exist:
- [ ] **Business & Scope:** BRD / SRS with SMART objectives, User Stories, and Acceptance Criteria.
- [ ] **System Architecture:** High-Level Design (HLD), Component diagrams, and Tech Stack decisions.
- [ ] **Data & Database:** ERD diagrams, schema definitions, normalization, and caching strategies.
- [ ] **API Contracts:** OpenAPI 3.1 specifications, request/response payloads, and error schemas.
- [ ] **Security & Compliance:** Threat models (STRIDE), authentication/authorization mechanisms, data privacy.
- [ ] **QA & Verification:** Acceptance test criteria, edge cases, and test plan matrix.

### Step 2: Gap Analysis & Proactive User Clarification
* If **ANY** business rule, technical constraint, data relationship, or edge case is missing or contradictory:
  * **STRICTLY PROHIBITED:** The Agent must **never make assumptions or invent logic** to fill documentation gaps.
  * **MANDATORY ACTION:** The Agent must list the exact missing items or ambiguous requirements and ask the user directly for clarification.

### Step 3: Formal Alignment & Gate Passage
* The design phase is ONLY considered complete when:
  1. All `@docs/` files have up-to-date Version Headers (aligned with `doc_format_and_version_control.md`).
  2. The user has reviewed and explicitly approved the specifications.
  3. No open technical or business questions remain unresolved.
