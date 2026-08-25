# Central Hub for Solution Architecture & System Design

This repository operates as a **Solution Architecture Consultancy**. It is designed to act as the "Brain" of software development projects, providing comprehensive system designs and strategies before any implementation begins.

**Core Philosophy**: We do NOT write implementation code here. This repository focuses 100% on **Analysis, Architectural Blueprints, Risk Assessment, and System Design**. The outputs are detailed specifications, contracts, and blueprints that separate engineering teams will implement.

---

## The Consulting Workflow

All interactions within this framework are focused on strategic design. The execution (coding) phase is strictly out-of-scope for this repository and must be handled by independent implementation teams.

### The `/solution` Mode
- **Trigger:** Requesting a system design, analysis, or architecture blueprint.
- **Objective:** Understand the business problem, assess real-world constraints, and produce enterprise-grade blueprints.
- **Constraints:**
  - **NO CODING ALLOWED**. Do not generate implementation source code (e.g., `.js`, `.py`, `.go`).
  - Outputs must be structured markdown artifacts (e.g., `architecture.md`, `brd.md`, `api-contract.md`, `threat-model.md`).
  - Always consider the triad of successful software: Business Value, Technical Feasibility, and Risk/Compliance.

---

## Skill Installation & Distribution (Quick Setup)

You can easily import these skills into any project repository or your global Antigravity configuration using [`degit`](https://github.com/Rich-Harris/degit) via `npx` without cloning the entire repository.

### Option 1: Download All Skills (Full Suite)

To install the entire consulting skill suite into your current workspace:

```bash
# Install to workspace (.agent/skills)
npx degit HuynhTri-dev/sa_hub_design/.agent/skills .agent/skills --force

# Or install globally across all projects (~/.gemini/config/skills)
npx degit HuynhTri-dev/sa_hub_design/.agent/skills ~/.gemini/config/skills --force
```

---

### Option 2: Download Individual Skills (On-Demand)

Pick and download only the specific department skills needed for your project:

#### 1. Security & Risk Architecture (`security`)
```bash
npx degit HuynhTri-dev/sa_hub_design/.agent/skills/security .agent/skills/security --force
```

#### 2. System Architecture Blueprint (`code-architecture-blueprint`)
```bash
npx degit HuynhTri-dev/sa_hub_design/.agent/skills/code-architecture-blueprint .agent/skills/code-architecture-blueprint --force
```

#### 3. Business Solutions & Analysis (`bda`)
```bash
npx degit HuynhTri-dev/sa_hub_design/.agent/skills/bda .agent/skills/bda --force
```

#### 4. UX/UI Strategy & Analysis (`design-ux-ui`)
```bash
npx degit HuynhTri-dev/sa_hub_design/.agent/skills/design-ux-ui .agent/skills/design-ux-ui --force
```

#### 5. Quality Assurance Strategy (`qa-qc`)
```bash
npx degit HuynhTri-dev/sa_hub_design/.agent/skills/qa-qc .agent/skills/qa-qc --force
```

> [!TIP]
> Use the `--force` flag to overwrite existing skill files when updating to the latest versions.

---

## Company Departments (Specialized Skills)

Our AI agents operate within distinct "Departments," each responsible for a specific phase of the solution lifecycle. The agent will automatically load and follow these instructions when relevant tasks arise.

### Active Departments (Currently Available)

1. **Business Solutions & Analysis (BDA)**
   - *Focus:* Requirements gathering, scope definition, and business process modeling.
   - *Outputs:* Business Requirements Documents (BRD), Software Requirements Specifications (SRS), User Stories, and BPMN flows via Mermaid.

2. **System Architecture Blueprint**
   - *Focus:* High-Level (HLD) and Low-Level Design (LLD), system topology, and technology stack selection.
   - *Outputs:* Layered architectures, Design Patterns, and structural blueprints.

3. **UX/UI Strategy & Analysis**
   - *Focus:* Information architecture, user flows, and interface logic.
   - *Outputs:* Wireframe logic, accessibility audits, and heuristic evaluations (pre-implementation).

4. **Security & Risk Architecture**
   - *Focus:* Threat modeling and proactive vulnerability mitigation at the design level.
   - *Outputs:* Security Policies, RBAC models, and mitigation strategies for AI/LLM risks, Business Logic abuse, and Chained Attacks.

5. **Quality Assurance (QA) Strategy**
   - *Focus:* Defining testing standards and acceptance criteria.
   - *Outputs:* Test plans, coverage requirements, and ISO/ISTQB compliance strategies.

---

### In Development (Planned Departments)

6. **Legal, Compliance & Feasibility Assessment**
   - *Focus:* Evaluating legal risks (e.g., healthcare data privacy, GDPR, local data laws) and assessing technical feasibility against real-world project constraints.
   - *Outputs:* Compliance checklists and Resource-to-Architecture mapping (e.g., recommending a Monolith over Microservices for small teams, or cost-optimized infrastructure for low-budget projects to avoid over-engineering).

7. **Data & Cloud Solutions**
   - *Focus:* Database schema design and cloud infrastructure topology.
   - *Outputs:* Entity-Relationship Diagrams (ERD), caching strategies, and AWS/GCP architecture diagrams.

8. **API & Integration Design**
   - *Focus:* Defining the communication contracts between system boundaries and external services.
   - *Outputs:* OpenAPI/Swagger specifications, GraphQL schemas, and 3rd-party integration strategies (Payment, SMS).

---

## How to Use This Hub

1. **Initiate Consultation:** Start by providing a business problem or an idea. Ask the agent to act as a Business Analyst to extract requirements.
2. **Assess Feasibility:** Evaluate the constraints (budget, team size, legal requirements) to shape the architectural approach.
3. **Architect the Solution:** Engage the Architecture and Security departments to draft the blueprints (HLD/LLD, Threat Models).
4. **Handoff:** Deliver the finalized markdown blueprints, ERDs, and API contracts to your independent engineering/development teams for actual implementation.
