---
name: database-data-engineering
description: Guides the agent through database design, query optimization, and data architecture decisions. Covers ERD design (entities, relationships, cardinality, normalization, constraints), microservice database patterns (Database-per-Service, Saga, CQRS, Event Sourcing, CAP theorem), caching strategies (Cache-aside, Write-through, Write-behind, Redis vs Memcached), and cloud data infrastructure (AWS/GCP service mapping, VPC topology, Disaster Recovery, Cost Optimization). Activate this skill whenever the user needs to design a schema/ERD, optimize database queries, choose between SQL and NoSQL, design caching layers, evaluate cloud data infrastructure, or review a database for N+1 queries, deadlocks, or scalability issues.
triggers:
  - "design ERD"
  - "thiết kế ERD"
  - "entity relationship"
  - "database schema"
  - "SQL migration"
  - "normalization"
  - "normalize"
  - "chuẩn hóa dữ liệu"
  - "indexing strategy"
  - "N+1 query"
  - "deadlock"
  - "caching strategy"
  - "Redis"
  - "cache invalidation"
  - "database per service"
  - "microservice database"
  - "CQRS"
  - "event sourcing"
  - "saga pattern"
  - "CAP theorem"
  - "polyglot persistence"
  - "data warehouse"
  - "OLTP OLAP"
  - "AWS data architecture"
  - "GCP database"
  - "thiết kế database"
  - "tối ưu query"
  - "tối ưu truy vấn"
---

# Database & Data Engineering Skill

This skill turns the agent into a **Data Architect / Database Engineer** specializing in schema design, query optimization, and cloud data infrastructure. It covers the full stack from conceptual ERD modeling down to physical storage decisions.

## When to Use This Skill

- User needs to design or review a database schema / ERD from business requirements.
- User asks about normalization, indexing, query performance, N+1 queries, or deadlocks.
- User needs to choose between SQL and NoSQL databases or design a polyglot persistence strategy.
- User needs to design caching layers (Redis, Memcached) with proper invalidation strategies.
- User is designing database architecture for a microservice system (Saga, CQRS, Event Sourcing).
- User is evaluating or building cloud data infrastructure on AWS or GCP.
- **Do NOT use** this skill for general backend API design — use `code-architecture-blueprint` instead.
- **Do NOT use** this skill for security audits of databases — use `security-architecture-blueprint` instead.

## Step-by-Step Instructions

### Workflow A — ERD Design from Business Requirements

Trigger: user describes a business domain and asks for a database schema or ERD.

1. **Gather domain context** — ask 2–3 targeted questions if missing:
   - What are the core business operations (CRUD targets)?
   - What are the most critical read queries (use cases that must be fast)?
   - Is this OLTP (transactional) or OLAP (analytical/reporting)?

2. **Run the 12-step ERD design framework** — see `resources/erd_design_framework.md`.
   Follow the exact order: Business Concepts → Entities → Attributes → PKs → Relationships → Cardinality → Optionality → Resolve N:N → Constraints → Normalization → History/Temporal → Use Case Validation.

3. **Apply the ERD design principles** — see `resources/erd_principles.md` for the 24 numbered principles covering naming conventions, God Entity anti-patterns, FK placement, snapshot vs. live data, and business constraints as DB constraints.

4. **Apply ERD design tips** — see `resources/erd_tips.md` for heuristics like "6-question Entity test", "delete cascade test", "Thing vs Value" distinction, and the "Source of Truth" principle.

5. **Output a Mermaid erDiagram** inline in the response (refer to `examples/erd.mmd` for reference syntax, PK/FK/UK annotations, snapshot field naming, and relationship cardinality formatting). Always include:
   - Entity names, attributes, PK/FK/UK annotations.
   - Cardinality notation (||--o{, ||--|{, ||--o|, etc.).
   - Brief rationale for each design decision in a section below the diagram.

6. **Run the 15-question ERD review checklist** — see `resources/erd_principles.md` (Section 24) before finalizing.

---

### Workflow B — Query Optimization and Anti-pattern Review

Trigger: user has an existing schema or query and asks about performance, N+1, indexing.

1. Ask to see the schema (or read from context) and the slow/problematic queries.
2. Check for **N+1 patterns**: any loop that fires queries per record — recommend Eager Loading, JOIN, or Batch/DataLoader pattern.
   - **Pro Tip:** If the user provides a query log, run `scripts/n1_detector.py` on it to automatically detect high-frequency duplicate query shapes.
3. Check **Index coverage**: does the index satisfy the WHERE + ORDER BY + SELECT columns? Suggest composite index column ordering (high-selectivity first).
4. Check **Transaction isolation level** if deadlocks are mentioned — recommend Optimistic Locking (version column) for low-contention writes, Pessimistic Locking (SELECT FOR UPDATE) for high-contention. See `resources/db_principles.md`.
5. Recommend reading the execution plan (EXPLAIN ANALYZE for PostgreSQL, EXPLAIN for MySQL).
   - **Pro Tip:** If the user provides EXPLAIN output, run `scripts/query_explainer.py` on it to auto-generate a human-readable analysis of bottlenecks like Seq Scans or Hash Joins.
6. If pagination is involved: prefer **keyset/cursor-based pagination** over OFFSET/LIMIT for large datasets.

---

### Workflow C — Microservice Database Architecture

Trigger: user is designing a multi-service system and asks about data strategy.

1. Apply **Database-per-Service** principle — no cross-service DB access.
2. Choose consistency pattern per business flow — see `resources/db_principles.md` (Microservice Patterns section):
   - Financial / inventory flows — Saga (Orchestration preferred)
   - Read-heavy dashboards / reporting — CQRS + Read model
   - Audit requirements — Event Sourcing
   - Social feeds / carts — Eventual Consistency (AP)
3. Apply **Polyglot Persistence** — match database type to use case (see decision table in `resources/db_principles.md`).
4. Address cross-service queries via **API Composition** or **Materialized View / CDC**.
5. Discuss CAP theorem trade-off per service boundary.

---

### Workflow D — Caching Strategy Design

Trigger: user asks about caching, Redis, session, performance optimization.

1. Identify the cache tier needed: Client-side → CDN → Application (Redis/Memcached) → DB buffer.
2. Choose cache pattern — see `resources/caching_strategy.md`: Cache-aside, Read-through, Write-through, Write-behind.
3. Design invalidation strategy (TTL + active invalidation on write events).
4. Address stampede risk (mutex/lock on rebuild, random TTL jitter).
5. Recommend Redis vs. Memcached based on data structure needs and persistence requirements.

---

### Workflow E — Cloud Data Infrastructure Evaluation

Trigger: user is designing or reviewing AWS/GCP infrastructure for data workloads.

1. Map requirements to the AWS to GCP service table in `resources/cloud_data_principles.md`.
2. Evaluate against the **6 AWS Well-Architected pillars** (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability).
3. Check network topology: Public/Private subnet separation, Multi-AZ, Defense-in-depth layers.
4. Assess Disaster Recovery tier: Backup and Restore / Pilot Light / Warm Standby / Multi-site Active-Active.
5. Run the **Cloud Infrastructure Evaluation Checklist** in `resources/cloud_data_principles.md`.
6. Note diagram tool limitation: Mermaid cannot render official AWS/GCP icons — state this clearly when producing cloud topology diagrams.

---

## Output Standards

| Deliverable | Format |
|---|---|
| ERD | Mermaid erDiagram block + decision rationale |
| Migration Script | SQL code block with numbered steps and rollback strategy |
| Query Fix | Before/After SQL, with index DDL and explanation |
| Architecture Recommendation | Bullet-point decision + trade-off table |
| Cloud Checklist | Markdown checklist grouped by domain |

## Knowledge Base, Scripts & Reference Files

### Utility Scripts
- `scripts/n1_detector.py` — Auto-detects N+1 query patterns by normalizing and counting query logs.
- `scripts/query_explainer.py` — Analyzes EXPLAIN ANALYZE output and suggests optimizations.

### Resources
- `examples/erd.mmd` — Reference Mermaid ERD diagram showcasing best practices (surrogate keys, PK/FK/UK, snapshot fields, audit history)
- `resources/erd_design_framework.md` — 12-step ERD design process
- `resources/erd_principles.md` — 24 ERD design principles + 15-question review checklist
- `resources/erd_tips.md` — ERD design heuristics and advanced tips (NoSQL, normalization trade-offs)
- `resources/db_principles.md` — Microservice DB patterns, Polyglot Persistence, CAP theorem, query optimization
- `resources/caching_strategy.md` — Caching patterns, invalidation, Redis vs Memcached
- `resources/cloud_data_principles.md` — AWS/GCP mapping, Well-Architected, network topology, DR, cost optimization
