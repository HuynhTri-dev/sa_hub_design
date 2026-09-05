<!--
name: Google Antigravity Workflow Specification & Authoring Guide
description: Standard structure, directory layout, trajectory orchestration, checkpoints, and best practices for creating Workflows in Google Antigravity.
-->

# Google Antigravity: Workflow Structure & Authoring Guide

In the Google Antigravity ecosystem, a **Workflow** serves as an execution blueprint designed to automate multi-step, sequential trajectories across various development tasks. 

While **Rules** define boundaries and **Skills** provide specialized capabilities, **Workflows** orchestrate how an AI Agent coordinates multiple rules, skills, and tools in a structured, end-to-end pipeline.

Workflow files are written in standard Markdown and are managed via the Workflows panel with a maximum limit of **12,000 characters per file**.

---

## 1. Standard Directory Layout

Workflows should be organized in a dedicated directory to prevent context pollution and ensure clean discovery:

```
.agents/workflows/
├── triage-bug.md        # Automated bug triage and reproduction
├── release-prep.md      # Pre-release verification and checklist
├── pr-review.md         # Multi-step pull request review pipeline
└── db-migration.md      # Safe database migration sequence
```

> **Global Workflows:** User-wide workflows can also be stored at `~/.gemini/config/workflows/`.

---

## 2. Standard Workflow Template

```markdown
# Workflow: Pull Request (PR) Code Review

## Context & Objectives
This workflow orchestrates a thorough, multi-step code review for incoming pull requests.
All steps must be executed sequentially from top to bottom without skipping.

## Prerequisites
- Target Git branch is checked out locally.
- Applicable workspace rules: `@.agents/rules/backend-standards.md`.

## Execution Trajectory

1. **Step 1: Collect Diff & Scope**
   - Inspect git status and analyze the diff against the `main` branch:
     ```bash
     git diff origin/main...HEAD
     ```
   - Identify modified files, newly added dependencies, and configuration changes.

2. **Step 2: Enforce Coding Standards**
   - Apply constraints and formatting rules from `@backend-standards.md`.
   - Flag any deviations in naming conventions, directory structure, or antipatterns.

3. **Step 3: Security & Quality Audit**
   - Invoke the `@security-check` skill to scan modified files for vulnerabilities, exposed secrets, and unescaped inputs.

4. **Step 4: Automated Verification**
   - Run unit and integration tests:
     ```bash
     npm run test:ci
     ```
   - If tests fail, summarize the failures and prompt the user before proceeding.

5. **Step 5: Summarize & Report**
   - Generate a structured Markdown report summarizing:
     - Changes reviewed
     - Passed checks & security scan results
     - Actionable recommendations and required fixes
   - **Checkpoint:** Display the report in the terminal and wait for human confirmation.
```

---

## 3. Core Authoring Principles & Best Practices

### 🔢 1. Strict Sequential Ordering
* Use numbered lists (`1.`, `2.`, `3.`) for trajectory steps.
* State explicit step transitions to ensure the agent executes instructions linearly and does not enter self-invented loops.

### 🎼 2. Orchestration Over Inlining
* Workflows should act as **orchestrators**, not monolithic code dumps.
* Call existing **Rules** (e.g., `@backend-standards.md`) for constraints and invoke **Skills** (e.g., `@security-check`, `@design-ux-ui`) for complex domain tasks instead of duplicating their contents.

### 🛑 3. Define Explicit Checkpoints (Human-in-the-Loop)
* Clearly designate steps where the agent must halt and request human approval, especially before performing destructive actions (e.g., database writes, git push, deployment triggers).
* Example: *"**Checkpoint:** Stop and request user confirmation before running the migration script."*

### 📏 4. Respect the 12,000 Character Limit
* Keep each workflow concise and focused on high-level orchestration steps.
* Break large, multi-phase corporate pipelines into smaller composable workflows if necessary.

### ⚡ 5. Include Exact Verification Commands
* Provide exact CLI commands for build, test, and lint steps so the agent can execute them deterministically without guessing arguments.

---

## References

* *Google Antigravity Documentation: Rules, Workflows, and Skills Architecture.*
