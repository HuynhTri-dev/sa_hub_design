<!--
name: top-essential-agent-skills
description: Curated catalog of high-impact AI coding skills and prompt patterns to complement Ponytail and eliminate redundancy.
-->

# Essential AI Agent Skills & Preventing Redundancy

In AI Agent software development, installing too many disjointed skills leads to **"Context Pollution"**, causing the Agent to get distracted, reason slower, or experience conflicting instructions.

To maximize efficiency, a system should only equip a **Lean Agent Toolkit** consisting of mutually complementary skills covering core domains:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        LEAN AGENT TOOLKIT MATRIX                       │
├────────────────────────────────┬───────────────────────────────────────┤
│ Code Governance Domain         │ • ponytail (Anti-overengineering)     │
│                                │ • systematic-debugging (Root-cause)   │
├────────────────────────────────┼───────────────────────────────────────┤
│ Communication & Token Economy  │ • caveman (Terse prose, zero fluff)   │
├────────────────────────────────┼───────────────────────────────────────┤
│ Data Layer & Native Tuning     │ • database-native-tuner (Postgres 1st)│
├────────────────────────────────┼───────────────────────────────────────┤
│ Minimalist Quality Assurance   │ • minimalist-tdd (High-signal checks) │
├────────────────────────────────┼───────────────────────────────────────┤
│ Non-negotiable Security        │ • security-guard (Trust boundaries)   │
└────────────────────────────────┴───────────────────────────────────────┘
```

---

## 1. Top Essential Skills Complementing Ponytail

### ⚡ 1. `caveman` (Terse Communication - Julius Brussee)
* **Repository:** [https://github.com/JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
* **Problem Solved:** Most LLMs tend to generate conversational fluff, polite greetings, and apologetic explanations ("Certainly! I would be happy to help you with..."), wasting 30% to 60% of output tokens.
* **Mechanism:** Forces the Agent to communicate concisely like a caveman or a busy engineer: presenting facts, error codes, and runnable commands only.
* **Perfect Synergy with Ponytail:**
  - `ponytail` governs **code length and minimal diffs**.
  - `caveman` governs **text verbosity and conversational brevity**.

---

### 🔬 2. `systematic-debugging` (Root Cause Investigation First)
* **Motto:** *"A patch fixing a symptom is the seed of the next bug."*
* **Problem Solved:** Agents often tend to "add an if/else wherever an error surfaces", creating messy spaghetti patches.
* **Mechanism:**
  1. Mandates the Agent to grep the entire caller hierarchy of the failing function.
  2. Reproduces the bug with a minimal single command or single test case before modifying code.
  3. Places guard clauses at the root origin where data corruption occurs rather than wrapping `try/catch` at the top level.

---

### 🧪 3. `minimalist-tdd` (High-Signal, Low-Boilerplate Testing)
* **Motto:** *"Lazy code without its check is unfinished. But test cases more complex than the implementation are maintenance debt."*
* **Problem Solved:** Agents generating dozens of low-value unit tests (testing getters/setters, testing framework initialization) or setting up 100-line mock fixtures for a 5-line function.
* **Mechanism:**
  - Only write tests for high-risk business logic: payment calculations, authorization rules, complex parsers, multi-branch conditionals.
  - Prefer self-contained execution: inline `assert` checks in `if __name__ == "__main__":` or a single test function free of heavy mock frameworks.

---

### 🐘 4. `database-native-tuner` (Maximizing Database Native Capabilities)
* **Problem Solved:** Overcoming the reflex of "spinning up a new microservice for everything".
* **Exploiting Postgres & DB Engine Features:**
  - **Queue / Background Task:** Use `SELECT ... FOR UPDATE SKIP LOCKED` instead of setting up RabbitMQ/Kafka clusters when throughput is < 1,000 msg/s.
  - **Full-Text Search:** Use `to_tsvector` and GIN Indexes instead of Elasticsearch for datasets under tens of millions of records.
  - **Atomic Updates:** Use `UPDATE accounts SET balance = balance - 10 WHERE id = 1 AND balance >= 10;` instead of complex application-level locks.
  - **JSON Storage:** Use `JSONB` for flexible schema data instead of adding MongoDB.

---

### 🛡️ 5. `security-guard` (Trust Boundary Defense)
* **Motto:** Save code lines, but **never save on security**.
* **Mandatory Control Checkpoints:**
  - 100% input validation at Route Handlers / Controllers via strict schemas (Pydantic / Zod / Typebox).
  - Prevent Timing Attacks when comparing secrets using constant-time string comparison (`hmac.compare_digest` / `crypto.timingSafeEqual`).
  - Always use Parameterized Queries to eradicate SQL Injection completely.

---

## 2. Skill Inflation Prevention Rules

To prevent repositories from becoming cluttered with redundant skill files that fragment AI reasoning, adhere to these **3 Golden Rules**:

1. **The "3-Project Rule":** Only abstract a workflow into a standalone Skill if you have manually performed the exact process across at least 3 distinct projects or domains.
2. **Single Responsibility Principle:** Each skill must cover exactly 1 domain. If a single skill contains both CSS guidelines and Docker setup, split or remove it.
3. **Local-First, Global-Second:** Store skills locally at `.agents/skills/`. Only promote them to global `~/.gemini/config/skills/` once proven language/framework agnostic.
