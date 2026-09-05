<!--
name: anti-overengineering-backend-checklist
description: Practical checklist and architectural evaluation criteria for backend systems based on Ponytail philosophy.
-->

# Anti-Overengineering Standards & Backend Checklist

This document formalizes golden engineering principles when designing backend system architecture and writing code in the spirit of **Ponytail**: *Lazy about writing complex solutions, extremely diligent when understanding the domain, and never compromising on safety.*

---

## 1. The Backend Decision Ladder (The Ponytail Ladder)

Before writing any new file or service, answer these 6 questions sequentially:

```
[1] Does this component strictly need to exist at all?
    └── NO  ──► Skip it (YAGNI). Do not create speculative DB tables or future-proofing logic.

[2] Does the current codebase already contain a similar function/module?
    └── YES ──► Reuse it. Grep before writing code; re-implementing existing helpers is the most common form of bloat.

[3] Is it provided natively by Database / Standard Library / OS?
    └── YES ──► Leverage native capabilities:
                • Postgres SKIP LOCKED instead of spinning up Kafka/RabbitMQ.
                • Database Constraints (UNIQUE, CHECK) instead of app-level locks/mutexes.
                • Full-text search (tsvector) instead of Elasticsearch.
                • Standard Library (`math`, `datetime`, `itertools`, `crypto`) over new npm/pip packages.

[4] Does an installed Dependency already support it?
    └── YES ──► Fully exploit libraries declared in package.json / pyproject.toml.

[5] Can it be solved with a single function or short query?
    └── YES ──► Keep it simple and inline. Avoid creating 3 separate interface/service/repo files.

[6] FINALLY: Design the absolute minimal working solution fulfilling real requirements.
```

---

## 2. Eliminating "The 7-Layer Onion" Antipattern

### ⚠️ Classic Symptom:
A simple read query forced through 7 to 9 meaningless boilerplate layers:
`Router` ➔ `Controller` ➔ `RequestDTO` ➔ `Validator` ➔ `Service` ➔ `RepositoryInterface` ➔ `RepositoryImpl` ➔ `Entity` ➔ `Mapper` ➔ `ResponseDTO`.

### ✅ Ponytail's Pragmatic Approach:
1. **Simple Read Queries:** Route Handlers can query DB directly or use concise query helpers. No empty Service layers merely forwarding method calls.
2. **Only Create Interfaces / Abstractions When:**
   - There are 2 or more real implementations to swap at runtime (e.g., Stripe, VNPay, PayPal gateways).
   - Complex business rules require isolation for unit testing multiple branching conditions.
3. **Locality of Behavior:** A developer opening a file should understand the execution flow end-to-end without jumping through 6 empty interface files.

---

## 3. Four Non-Negotiable Boundaries ("Lazy, Not Negligent")

Saving code lines does NOT mean sloppy engineering. The following four pillars **must never be compromised**:

| Pillar | Technical Requirement | Risk if Omitted |
| :--- | :--- | :--- |
| **1. Trust-Boundary Validation** | Validate 100% of input data from HTTP, gRPC, and webhooks using strict schemas (lengths, types, formats). | Injections, memory corruption, app crashes. |
| **2. Defensive Error Handling** | Never swallow errors (`except: pass` or empty `catch {}`). Always return precise HTTP status codes, structured logging with `trace_id` / `correlation_id`. | Lost failure traces, un-debuggable production outages at 3 AM. |
| **3. Data Integrity** | Wrap mutation operations inside DB Transactions; enforce Idempotency for payment, debit, or message queue consumer endpoints. | Account balance mismatches, duplicate charges, orphaned records. |
| **4. Graceful Shutdown** | Listen for `SIGTERM` / `SIGINT`, drain active requests, and release DB pools before process exit. | Broken connections, hanging sockets, corrupted state in background tasks. |

---

## 4. Presenting System Architecture Convincingly

When writing Design Docs or presenting system architecture to review committees:

1. **Focus on "Why" over "What":** Don't just draw box diagrams; justify choices with empirical data: projected QPS, latency targets, payload sizes.
2. **Highlight What You Chose NOT to Build:**
   - *"We selected a Modular Monolith over Microservices to eliminate network latency and avoid operational overhead of distributed clusters."*
   - *"We chose Postgres SKIP LOCKED over Kafka because current volume is 50 msg/s; Postgres saves 100% of additional infra cost."*
   - *"We used PostgreSQL Full-Text Search over Elasticsearch because dataset is under 1M records, eliminating data synchronization pipelines."*

> **Remember:** Explicitly deciding NOT to build unnecessary components is the hallmark of architectural maturity and senior engineering experience.
