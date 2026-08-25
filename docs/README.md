<!--
name: Google Antigravity: Skills vs Rules vs Workflows
description: Comprehensive guide and comparison between Skills, Rules, and Workflows in the Google Antigravity ecosystem.
-->

# Google Antigravity: Skills vs. Rules vs. Workflows

In the Google Antigravity ecosystem, **Skills**, **Rules**, and **Workflows** are the primary customization mechanisms used to guide and shape AI Agent behavior. Although all three influence how agents operate, they differ fundamentally in their core purpose, context injection scope, and trigger mechanisms.

---

## 1. Detailed Comparison

| Feature / Aspect | Skills | Rules | Workflows |
| :--- | :--- | :--- | :--- |
| **Primary Purpose** | Instructs the agent on how to solve **a specialized task domain** (e.g., writing unit tests, converting JSON to Pydantic, handling cloud deployments). | Enforces **constraints, coding styles, behavioral guidelines, and foundational context** that the agent must adhere to. | Defines a **sequence of structured steps** to automate repetitive, multi-phase procedures. |
| **Scope & Context Impact** | **Local / On-demand.** Loaded into transient memory only when relevant to the current task, then freed. | **Prompt-level.** Functions as persistent foundational background context across interactions. | **Trajectory-level.** Guides the agent through multi-step executions and interconnected tasks. |
| **Activation Mechanism** | Model-invoked (based on `SKILL.md` description) or directly invoked by the user. | **Always On**, **Glob-based** (e.g., `*.ts`), or **Model Decision**. | Manually triggered by the user via **Slash Commands** (e.g., `/workflow-name`). |
| **Storage Location** | `.agents/skills/<skill-name>/SKILL.md` or `~/.gemini/config/skills/` | `.agents/rules/` or global config `~/.gemini/GEMINI.md` / `rules/` | Standalone Markdown files in the Workflows panel (up to 12,000 chars/file). |

---

## 2. Practical Application Guide

### When to Use Rules
Use **Rules** when you want to define the fundamental identity, boundaries, and conventions of the agent.
* **Example:** *"Never use `print()` statements in production Python code; always use the system `logging` module."*
* **Example:** *"Ensure all commit messages strictly follow the Conventional Commits specification."*

### 🛠️ When to Use Skills
Use **Skills** when you want to provide specialized domain capabilities, cheat sheets, scripts, or reference implementations that the agent can draw upon when necessary.
* **Example:** A step-by-step guide and validator script for converting complex JSON schemas into Pydantic models.
* **Example:** Specialized instructions for debugging and profiling WebAssembly memory leaks.

### 🔄 When to Use Workflows
Use **Workflows** when you need the agent to execute a coordinated, multi-step playbook from start to finish.
* **Example (PR Review Workflow):**
  1. Pull the target branch and diff changes.
  2. Invoke security scanning Skill.
  3. Execute automated test suites.
  4. Summarize findings into a structured review report.

---

## 3. Summary Matrix

```
               ┌─────────────────────────────────────────┐
               │         Google Antigravity Agent        │
               └─────────────────────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
   ┌───────────┐              ┌───────────┐              ┌───────────┐
   │   RULES   │              │  SKILLS   │              │ WORKFLOWS │
   │ (Identity │              │(Capability│              │(Execution │
   │& Baseline)│              │& Toolkit) │              │ Playbook) │
   └───────────┘              └───────────┘              └───────────┘
   • Always on / Glob         • Loaded on-demand         • Slash-command triggered
   • Constraints & style      • Task-specific guides     • Multi-step orchestration
```

---

## 4. Plugins, Hooks, and Sidecars

### Plugins
**Concept**: Plugins are namespaced bundles used to extend Antigravity's capabilities.
**How it works**: Instead of configuring extensions separately, Plugins allow you to group all components—including Skills, Rules, MCP Servers, and Hooks—into a single directory.
**Setup Structure**: Each plugin folder must contain a `plugin.json` declaration file at its root. Plugins can be installed at the project level (in `.agents/plugins/`) or globally (in `~/.gemini/config/plugins/`). The system also provides built-in "Bundled Plugins" developed by Google.

### Hooks
**Concept**: Hooks are a mechanism that allows the system to automatically inject and execute pre-configured scripts or commands when specific AI Agent events are triggered.
**How it works**: Hooks are particularly useful for enforcing rules, automatically running linters for source code checks, or collecting analytics logs. Commonly supported events include `PreToolUse` (triggered before the Agent uses a tool) and `PostToolUse` (triggered after the Agent finishes using a tool). You can use Regex matchers to specify exactly which tools (e.g., `run_command` or `browser_*`) will trigger a specific hook.
**Setup Structure**: Hooks are centrally defined inside a `hooks.json` file, which can be located in either the project's custom directory or the global configuration directory.

### Sidecars
**Concept**: Sidecars are independent background processes that run alongside the main Antigravity application.
**How it works**: Antigravity manages the entire lifecycle of Sidecars, including automatic startup and auto-restarting if the process hangs or encounters an error. This feature is specifically designed for tasks that require continuous execution, recurring scheduled commands (cron/schedule), or event listener services. Notably, from within a Sidecar, you can call the `agentapi` CLI to interact back with the system (for example, to create a new chat or send an automated message to the Agent).
**Setup Structure**: Each sidecar is defined via a `sidecar.json` file. Unlike Plugins and Hooks, for security and resource management reasons, all Sidecars are disabled by default. Users must manually enable them by setting `"enabled": true` inside their `config.json` user configuration file.

---

## References

* *Google Antigravity Documentation: Rules, Workflows, Skills, and Best Practices.*
* [Plugins Documentation](https://antigravity.google/docs/plugins/)
* [Hooks Documentation](https://antigravity.google/docs/hooks/)
* [Sidecars Documentation](https://antigravity.google/docs/sidecars/)
