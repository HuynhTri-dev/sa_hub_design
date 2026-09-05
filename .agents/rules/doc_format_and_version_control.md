<!--
name: Document Format and Version Control Standard
description: Enforces mandatory metadata headers, standardized Project Information, and strict document versioning to prevent hallucinations or stale context usage.
-->

# Document Format & Version Control Standard

## 1. Mandatory File Header & Metadata
All generated documentation and architectural specification Markdown files (`.md`) MUST start with an HTML comment block containing `name` and `description`:

```markdown
<!--
name: [Short, descriptive name of the document]
description: [Concise summary of the document purpose, scope, and target system]
-->
```

## 2. Standardized Project Information Section
Every specification document (BRD, SRS, Architecture Blueprint, API Spec, ERD, Threat Model, etc.) MUST include Section 1 formatted exactly as follows:

```markdown
## 1. Project Information
- **Project Name:** [Exact Project Name]
- **Document Date:** [YYYY-MM-DD]
- **Requester / Sponsor:** [Stakeholder / Client / Department]
- **Version:** [Semantic Version, e.g., 1.0, 1.1, 2.0, 2.1]
```

### Version Tracking & Change History Table
To prevent referencing deprecated or removed logic across iterations, whenever a document is updated:
1. Increment the **Version** number explicitly.
2. Update the **Document Date** to the current modification date.
3. Append a brief entry to a **Version History** table right below Section 1:

```markdown
### Version History
| Version | Date | Author / Agent | Summary of Changes |
| :--- | :--- | :--- | :--- |
| 1.0 | 2026-08-20 | BDA Agent | Initial requirements baseline |
| 2.0 | 2026-08-25 | SA Agent | Refactored architecture to Microservices |
| 2.1 | 2026-08-27 | SA Agent | Deprecated legacy Auth, replaced with OAuth2/OIDC |
```

---

## 3. Strict Version Management Rules for AI Agents

* **Always Parse Active Version First:** When reading any `.md` file, the Agent must read the `Version:` field in Section 1 before analyzing technical details.
* **No Stale Memory Bleed:** If a document is updated from `v2.0` to `v2.1`, the Agent MUST strictly discard all assumptions, schemas, endpoints, and data flows that were deleted or modified in `v2.0`.
* **Single Source of Truth:** If conflicting versions of the same specification exist in the workspace, the Agent must prioritize the file with the highest version and newest date, and flag the ambiguity to the user immediately.
