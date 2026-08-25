<!--
name: Google Antigravity Skill Specification & Guide
description: Standard structure, YAML frontmatter specification, template, and best practices for creating SKILL.md files in Google Antigravity.
-->

# Google Antigravity: Skill Structure & Authoring Guide

In the Google Antigravity ecosystem, a **Skill** is an on-demand capability package that guides an AI Agent through specialized tasks. A skill is structured around a central `SKILL.md` file consisting of two primary parts: **YAML Frontmatter** (metadata for discovery and activation) and the **Markdown Body** (actionable instructions and execution rules).

---

## 1. Skill Directory Layout

Skills reside in `.agents/skills/<skill-name>/` (workspace level) or `~/.gemini/config/skills/<skill-name>/` (global level).

```
.agents/skills/<skill-name>/
├── SKILL.md            # [Required] Core instruction file with YAML frontmatter
├── scripts/            # [Optional] Helper scripts and executable utilities
├── examples/           # [Optional] Reference implementations and code samples
└── resources/          # [Optional] Checklists, templates, and reference assets
```

---

## 2. Standard `SKILL.md` Template

```markdown
---
name: lowercase-hyphenated-skill-name
description: Clear, third-person description of what the skill accomplishes and the specific conditions or triggers under which the agent should activate it. (e.g., "Generates comprehensive pytest unit tests for Python backend services.")
triggers:
  - "create unit test"
  - "test suite"
  - "pytest"
---

# [Skill Name]

[A concise summary explaining the primary objective and domain of this skill.]

## When to Use This Skill
- Use this skill when [Condition 1: e.g., writing new test suites].
- Especially helpful for [Condition 2: e.g., mocking database calls with pytest-mock].
- **Do NOT use** when [Exception: e.g., running end-to-end browser automation].

## Step-by-Step Instructions
[Provide sequential steps, conventions, or architectural patterns the agent must strictly follow.]

1. **Step 1: Context & Discovery**
   - [Detailed action or inspection step]
2. **Step 2: Execution & Implementation**
   - [Detailed coding or generation guidelines]
3. **Step 3: Verification & Validation**
   - [Verification checks, linting, or test execution]

## Decision Trees (Optional)
[For complex workflows with branching logic]
- If **[Scenario A]** -> Apply **[Approach A]**.
- If **[Scenario B]** -> Apply **[Approach B]**.

## Accompanying Scripts & Resources (Optional)
- When validating output, execute: `python scripts/validator.py --input <path>`
- Use `--help` flags to inspect tool arguments rather than reading script source files into context.
```

---

## 3. Core Authoring Rules & Best Practices

### 🏷️ 1. Frontmatter is Mandatory
* The `description` field is the **critical decision signal** used by the agent to determine whether the skill is relevant to the user request.
* Write descriptions in the **third person** and clearly state **what** the skill does and **when** it should be triggered. Vague descriptions will cause the agent to bypass the skill.

### 🎯 2. Keep Skills Focused (Single Responsibility)
* Each skill should address **one specific task domain** (e.g., unit testing, UI/UX design, database migration).
* Avoid combining unrelated domains (e.g., QA/testing and visual design) into a single skill file. Split distinct workflows into separate skills.

### 📦 3. Treat Scripts as Black Boxes
* When bundling executable helper scripts in `scripts/`, instruct the agent to run them with CLI arguments (e.g., `--help` or required flags).
* Do not prompt the agent to read and parse the entire source code of helper scripts unless debugging is explicitly required. This saves context tokens and prevents hallucinated modifications.

### ⚡ 4. Token Efficiency & Progressive Disclosure
* Keep `SKILL.md` concise, high-signal, and strictly actionable.
* Offload extensive reference tables, deep documentation, or large schemas into separate markdown files in `resources/` or `examples/` that the agent can read on demand.

---

## References

* *Google Antigravity Documentation: Creating a Skill & Best Practices.*
