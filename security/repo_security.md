# Security Testing and Simulated Attack Repositories

<!--
name: security-testing-attack-repos
description: A curated list of GitHub repositories and tools for static/dynamic security analysis, dependency vulnerability scanning, secrets detection, penetration testing, and simulated attack emulation.
-->

This document provides a curated collection of industry-standard security repositories and tools categorized for security auditing, vulnerability scanning, and simulated attack emulation.

---

## 1. Security Auditing & Vulnerability Scanning (Defensive / SAST / DAST)

These tools are used to check, audit, and secure applications, container images, dependencies, and cloud infrastructures.

| Tool / Repository | Primary Focus | Language / Type | Description |
|---|---|---|---|
| [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | Secret Detection | Go / CLI | Finds hardcoded secrets (API keys, passwords, private keys) in git history and workspace files. |
| [semgrep/semgrep](https://github.com/semgrep/semgrep) | SAST | Multi-language | Lightweight, fast static analysis tool to find bugs, security vulnerabilities, and enforce code standards. |
| [aquasecurity/trivy](https://github.com/aquasecurity/trivy) | Vulnerability Scanner | Go / CLI | Scans container images, file systems, git repositories, and Kubernetes clusters for vulnerabilities and misconfigurations. |
| [zaproxy/zaproxy](https://github.com/zaproxy/zaproxy) | DAST | Java / GUI & CLI | OWASP Zed Attack Proxy (ZAP) is a widely used web application vulnerability scanner. |
| [projectdiscovery/nuclei](https://github.com/projectdiscovery/nuclei) | Vulnerability Scanner | Go / CLI | Fast, template-based vulnerability scanner for scanning networks and web applications based on a simple YAML DSL. |
| [PyCQA/bandit](https://github.com/PyCQA/bandit) | Python SAST | Python | Analyzes Python code to find common security issues (e.g., hardcoded passwords, shell executions, unsafe deserialization). |
| [snyk/cli](https://github.com/snyk/cli) | SCA & SAST | Node.js / CLI | Scans project dependencies, container images, and IaC templates for known security vulnerabilities. |
| [github/codeql](https://github.com/github/codeql) | Semantic Code Analysis | Multi-language | Query engine used to discover vulnerabilities across codebases by treating code as data. |

---

## 2. Attack Simulation & Penetration Testing (Offensive / Red Teaming)

These tools and frameworks are used to perform simulated attacks, automate threat emulation, and test security defenses against real-world attack techniques.

| Tool / Repository | Primary Focus | Use Case | Description |
|---|---|---|---|
| [mitre/caldera](https://github.com/mitre/caldera) | Adversary Emulation | Breach & Attack Simulation (BAS) | Built on the MITRE ATT&CK framework to automate adversary emulation and test defensive configurations. |
| [redcanaryco/atomic-red-team](https://github.com/redcanaryco/atomic-red-team) | Adversary Emulation | Unit Testing Defenses | A library of simple, scriptable, and mapped tests to MITRE ATT&CK, allowing defenders to validate security controls. |
| [rapid7/metasploit-framework](https://github.com/rapid7/metasploit-framework) | Penetration Testing | Exploit Execution | The most widely used penetration testing framework to find, exploit, and validate vulnerabilities. |
| [sqlmapproject/sqlmap](https://github.com/sqlmapproject/sqlmap) | Penetration Testing | Database Takeover | Automated SQL injection tool to detect and exploit SQL injection vulnerabilities and take control of database servers. |
| [nmap/nmap](https://github.com/nmap/nmap) | Network Scanning | Port & OS Discovery | Industry standard network mapper used for network discovery, port scanning, and vulnerability assessment. |
| [danielmiessler/SecLists](https://github.com/danielmiessler/SecLists) | Security Wordlists | Brute-force & Fuzzing | A collection of security wordlists containing usernames, passwords, URLs, sensitive files, and fuzzing payloads. |
| [SpecterOps/BloodHound](https://github.com/SpecterOps/BloodHound) | Active Directory Audit | Path Finder | Uses graph theory to reveal hidden and unintended relationships in Active Directory and Azure environments for privilege escalation. |
| [trustedsec/social-engineer-toolkit](https://github.com/trustedsec/social-engineer-toolkit) | Social Engineering | Phishing Simulation | Open-source penetration testing framework designed for social engineering attacks (credential harvesting, phishing, spear-phishing). |

---

## 3. Chaos Engineering & Resilience Testing

These tools simulate server crashes, network latency, and service disruptions to verify availability and disaster recovery mechanisms.

- **[chaos-mesh/chaos-mesh](https://github.com/chaos-mesh/chaos-mesh)**: A powerful chaos engineering platform for Kubernetes that orchestrates various kinds of fault injections (network delay, pod killing, disk stress).
- **[netflix/chaosmonkey](https://github.com/netflix/chaosmonkey)**: Resiliency tool that randomly terminates virtual machine instances and containers in production to ensure services survive hosting failures.

---

> [!NOTE]
> All offensive testing tools should only be used in authorized staging/development environments or within isolated sandboxes. Never perform simulated attacks against live production services without explicit permission and scheduling.
