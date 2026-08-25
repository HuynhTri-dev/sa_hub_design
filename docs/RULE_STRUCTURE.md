<!--
name: Google Antigravity Rule Specification & Authoring Guide
description: Standard structure, configuration, activation modes, syntax, and best practices for creating Rules in Google Antigravity.
-->

# Google Antigravity: Rule Structure & Authoring Guide

In the Google Antigravity ecosystem, **Rules** define foundational constraints, coding standards, architectural boundaries, and project-specific guidelines that an AI Agent must strictly adhere to.

Unlike `SKILL.md` (which requires YAML frontmatter), Rule files are standard Markdown documents with a strict limit of **12,000 characters per file**.

---

## 1. Storage Locations & Scopes

Rule configuration operates at two distinct levels:

| Scope | Location | Description |
| :--- | :--- | :--- |
| **Global Rules** | `~/.gemini/GEMINI.md` or `~/.gemini/config/rules/*.md` | Applies universally across all projects and workspaces on your machine. |
| **Workspace Rules** | `.agents/rules/*.md`, `GEMINI.md`, or `AGENTS.md` | Scoped specifically to the current workspace repository. |

---

## 2. Activation Modes

Rules can be configured with four distinct activation triggers determining when they enter the agent's context:

1. **Always On**: The rule is permanently loaded into the agent's active context for every interaction.
2. **Glob Pattern**: The rule is dynamically loaded only when the agent inspects, edits, or operates on files matching specific glob patterns (e.g., `*.ts`, `src/db/**/*.py`, `frontend/**/*.vue`).
3. **Model Decision**: The agent evaluates natural language descriptions to dynamically decide whether the rule is relevant to the current user request.
4. **Manual**: The rule is applied only when the user explicitly references or tags it in the chat prompt.

---

## 3. File Referencing Syntax (`@` Mentions)

You can reference project files directly within a rule using `@filename` syntax:
* **Relative Paths**: Resolved relative to the current rule file's directory.
* **Workspace Resolution**: If a relative target is not found locally, the system automatically attempts to match the path relative to the workspace root (e.g., `@src/db/connection.ts` or `@config/settings.json`).

---

## 4. Standard Rule Template

```markdown
# [Rule Title - e.g., Backend Engineering Standards]

## 1. Directory & Architectural Standards
- Do not create source files directly in the repository root.
- All database queries and schema definitions must reside exclusively under `@src/db/`.
- Maintain strict separation between service handlers and data access layers.

## 2. Code Style & Paradigms
- Use single quotes (`'`) for string literals.
- Enforce `camelCase` for variable/function names and `PascalCase` for classes and interfaces.
- Always validate and sanitize input parameters before executing core business logic.
- Document public functions with clear parameters and return type annotations.

## 3. Testing & Verification Commands
- Before proposing any code modifications, verify changes against the test suite:
  ```bash
  npm run test:unit
  ```
- Ensure overall test coverage remains above 80%.

## 4. Deprecations & Prohibited Patterns
- **Prohibited:** Never use the legacy `request` library. Always use `axios` or native `fetch`.
- **Prohibited:** Never use `console.log()` for production logging; always use the centralized system logger (`@src/utils/logger.ts`).
- **Forbidden:** Never commit secrets, API keys, or raw `.env` files.
```

---

## 5. Authoring Rules & Best Practices

### 📏 1. Respect the 12,000 Character Limit
* Rule files must remain under 12,000 characters. Keep statements concise, direct, and high-signal.
* Avoid redundant explanations or verbose prose. Use bullet points and clear imperative sentences.

### 🎯 2. Use Granular Scoping (Glob over Always-On)
* Avoid placing all guidelines into a single massive Always-On rule.
* Split rules by language or domain (e.g., `python_rules.md` matching `*.py`, `react_rules.md` matching `*.tsx`) using Glob patterns to keep the prompt context lean and focused.

### 🚫 3. Clearly Demarcate Boundaries
* Clearly distinguish between **mandatory requirements** ("Must", "Always") and **prohibited antipatterns** ("Never", "Do not").
* Provide concrete alternatives when prohibiting a pattern (e.g., *"Do not use X; use Y instead."*).

### 🧪 4. Provide Verifiable Test Commands
* Always include the exact shell command that the agent should execute to validate compliance with the rule (e.g., linter, type-checker, test runner).

---

## References

* *Google Antigravity Documentation: Rules & Workflows ([https://antigravity.google/docs/rules-workflows](https://antigravity.google/docs/rules-workflows))*
* *Google Antigravity Documentation: CLI Best Practices ([https://antigravity.google/docs/cli/best-practices](https://antigravity.google/docs/cli/best-practices))*
