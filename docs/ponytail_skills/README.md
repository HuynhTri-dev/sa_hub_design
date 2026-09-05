<!--
name: curated-skills-overview
description: Overview of curated AI coding agent skills, anti-overengineering philosophy, and the Ponytail ecosystem.
-->

# Curated AI Agent Skills & Anti-Overengineering Hub

> *"The best code is the code you never wrote."* — Dietrich Gebert, creator of Ponytail

Welcome to the central hub for synthesizing, analyzing, and deploying lean **AI Coding Agent Skills**. The ultimate objective of this documentation repository is to cultivate the mindset of a **"Laziest Senior Developer"**: minimizing source code, fully leveraging existing resources, eliminating bloat (over-engineering), and establishing rigorous controls to **prevent creating redundant skills or code**.

---

## 📑 Documentation Index

This directory is organized into specialized topics, ready for immediate reference and application:

| Document | Key Content |
| :--- | :--- |
| **[01_PONYTAIL_SUITE.md](file:///Users/macbookair/Downloads/agent_vibe_retrival/docs/ponytail_skills/01_PONYTAIL_SUITE.md)** | In-depth breakdown of Ponytail's official 6-skill suite: `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help`. 3-level intensity mechanics (Lite, Full, Ultra). |
| **[02_TOP_ESSENTIAL_SKILLS.md](file:///Users/macbookair/Downloads/agent_vibe_retrival/docs/ponytail_skills/02_TOP_ESSENTIAL_SKILLS.md)** | Curated collection of top international skills & prompt patterns (Caveman, Systematic Debugging, Minimal TDD, DB Tuner, API Contract First, Security Guard). |
| **[03_INSTALLATION_GUIDE.md](file:///Users/macbookair/Downloads/agent_vibe_retrival/docs/ponytail_skills/03_INSTALLATION_GUIDE.md)** | Step-by-step installation instructions across platforms: Antigravity IDE (`agy`), Claude Code, Codex CLI, Cursor, GitHub Copilot, OpenCode, Qoder, Gemini CLI. |
| **[04_ANTI_OVERENGINEERING_CHECKLIST.md](file:///Users/macbookair/Downloads/agent_vibe_retrival/docs/ponytail_skills/04_ANTI_OVERENGINEERING_CHECKLIST.md)** | "The Ponytail Ladder" standards for Backend & AI Agents: 5-step evaluation process before writing code/skills, non-negotiable "Lazy, Not Negligent" boundaries. |

---

## 🎯 The Ponytail Decision Ladder (The Ponytail Ladder)

Before deciding to create an extra service, data table, abstraction layer, dependency, or writing a single line of new code, Agents and Engineers must evaluate through each rung:

```
[RUNG 1] Does this feature strictly need to exist at all?
   ├── (No)  ──► SKIP IT IMMEDIATELY (YAGNI - You Aren't Gonna Need It)
   └── (Yes)
[RUNG 2] Does the current codebase already have something similar?
   ├── (Yes) ──► REUSE IT, NEVER REWRITE IT
   └── (No)
[RUNG 3] Is it built into the Database / Standard Library / Operating System?
   ├── (Yes) ──► USE NATIVE FEATURES (Postgres SKIP LOCKED, stdlib...)
   └── (No)
[RUNG 4] Does an installed Dependency already cover it?
   ├── (Yes) ──► EXPLOIT EXISTING DEPENDENCIES FULLY
   └── (No)
[RUNG 5] Can it be solved with a single function or query?
   ├── (Yes) ──► KEEP IT SIMPLE & INLINE (One-liner / Small function)
   └── (No)
[RUNG 6] FINALLY WRITE: Design the absolute minimal working solution.
```

---

## 🛡️ "Lazy, Not Negligent" Principles

Ponytail cuts complexity, but **never compromises safety**. The following 4 boundaries are **non-negotiable**:

1. **Trust-boundary Validation:** All incoming requests from HTTP, gRPC, MQ must strictly validate data types, schemas, and string lengths.
2. **Defensive Error Handling:** Never swallow errors (`try/except: pass` or empty `catch {}`). Always log structured errors with trace/correlation IDs.
3. **Data Integrity:** Use Database Transactions and ensure Idempotency for critical financial or state mutations.
4. **Graceful Shutdown:** Clean up connection pools and flush queues prior to process termination.

---

## 🚀 Quick Workspace Integration

Ponytail's core skill is pre-configured in this repository at:
- [`.agents/skills/ponytail/SKILL.md`](file:///Users/macbookair/Downloads/agent_vibe_retrival/.agents/skills/ponytail/SKILL.md)
- [`.agents/skills/ponytail-review/SKILL.md`](file:///Users/macbookair/Downloads/agent_vibe_retrival/.agents/skills/ponytail-review/SKILL.md)

See the complete setup instructions at **[03_INSTALLATION_GUIDE.md](file:///Users/macbookair/Downloads/agent_vibe_retrival/docs/ponytail_skills/03_INSTALLATION_GUIDE.md)** to enable global integration across other tools and environments.
