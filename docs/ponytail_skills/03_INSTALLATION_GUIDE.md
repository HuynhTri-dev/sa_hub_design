<!--
name: agent-skills-installation-guide
description: Step-by-step installation instructions for Ponytail and complementary skills across Antigravity, Claude Code, Cursor, Codex, and others.
-->

# Multi-Platform Skill Installation & Setup Guide

This document provides exact installation commands to integrate **Ponytail** and minimalist skill suites into your development environment, covering **Google Antigravity**, **Claude Code**, **Cursor**, **Codex**, **GitHub Copilot**, **OpenCode**, and **Qoder**.

---

## 1. Google Antigravity (IDE & Antigravity CLI `agy`)

Google Antigravity supports loading skills at 3 distinct scopes: Plugin CLI installation, Local Workspace Scope (`.agents/skills/`), or Global Scope (`~/.gemini/config/skills/`).

### Option A: Direct Installation via Antigravity CLI (`agy`)
If running inside terminal with the `agy` CLI:
```bash
agy plugin install https://github.com/DietrichGebert/ponytail
```
*Note: Once installed, you can invoke `/ponytail`, `/ponytail-review`, `/ponytail-audit` directly in chat.*

### Option B: Workspace-Level Setup (Recommended)
Your repository structure already includes `.agents/skills/`. You can copy or curl directly:

```bash
# Create skill directories for Ponytail in the current project
mkdir -p .agents/skills/ponytail
mkdir -p .agents/skills/ponytail-review

# Download official SKILL.md files from repository
curl -s https://raw.githubusercontent.com/DietrichGebert/ponytail/main/skills/ponytail/SKILL.md \
  -o .agents/skills/ponytail/SKILL.md

curl -s https://raw.githubusercontent.com/DietrichGebert/ponytail/main/skills/ponytail-review/SKILL.md \
  -o .agents/skills/ponytail-review/SKILL.md
```

### Option C: Global Scope across All Projects
To enable Ponytail automatically across every workspace in Antigravity:
```bash
mkdir -p ~/.gemini/config/skills/ponytail
curl -s https://raw.githubusercontent.com/DietrichGebert/ponytail/main/skills/ponytail/SKILL.md \
  -o ~/.gemini/config/skills/ponytail/SKILL.md
```

---

## 2. Claude Code (Anthropic)

In an interactive Claude Code session, execute the following two commands:

```text
/plugin marketplace add DietrichGebert/ponytail
```
*(Wait for confirmation, then run the second command):*
```text
/plugin install ponytail@ponytail
```

> **Environment Note:** Ensure `node` is available in your system `$PATH` so lifecycle hooks execute cleanly.

---

## 3. Codex (OpenAI Codex CLI & Desktop)

Execute in terminal:
```bash
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```
Launch `codex`, enter `/hooks` to approve lifecycle hooks, and start a new session.

---

## 4. Cursor IDE

Cursor manages instructions via `.cursorrules` or `.cursor/rules/*.mdc`.

### Quick Cursor Setup:
Create `.cursor/rules/ponytail.mdc` in your workspace root:
```markdown
---
description: Enforce minimal code and anti-overengineering (Ponytail Ladder)
globs: *
alwaysApply: true
---

# Ponytail Philosophy: The Laziest Senior Dev
- The best code is the code you never wrote.
- Stop at the first rung that holds:
  1. Does this need to exist at all? (YAGNI -> skip it)
  2. Already in codebase? (Reuse it)
  3. Stdlib does it? (Use it)
  4. Native platform feature? (Use HTML5/CSS3/Postgres native)
  5. Installed dependency? (Use it)
  6. One line? (One line)
  7. Only then: minimum code that works.
- Lazy, not negligent: Never skip trust-boundary validation, defensive error handling, data integrity, and security.
```

---

## 5. GitHub Copilot CLI

In an interactive Copilot CLI session:
```bash
copilot plugin marketplace add DietrichGebert/ponytail
copilot plugin install ponytail@ponytail
```
Copilot namespaces plugin slash commands:
```text
/ponytail:ponytail ultra
/ponytail:ponytail-review
```

---

## 6. OpenCode & Qoder

### OpenCode:
Add to `opencode.json` at your project root:
```json
{
  "plugin": ["@dietrichgebert/ponytail"]
}
```

### Qoder:
Qoder auto-loads `AGENTS.md` from the repo root. To apply project-wide rules, copy the rule file to `.qoder/rules/ponytail.md`.

---

## 7. Shell One-Liner to Download All 6 Official Skills

Execute this shell script in your terminal to fetch all 6 official skills into `.agents/skills/`:

```bash
for skill in ponytail ponytail-review ponytail-audit ponytail-debt ponytail-gain ponytail-help; do
  mkdir -p ".agents/skills/$skill"
  curl -s "https://raw.githubusercontent.com/DietrichGebert/ponytail/main/skills/$skill/SKILL.md" \
    -o ".agents/skills/$skill/SKILL.md"
  echo "✅ Downloaded: .agents/skills/$skill/SKILL.md"
done
```
