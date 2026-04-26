# NIST Generative AI Profile Mapping

This document maps common generative AI risks to practical governance controls.

| Risk Area | Example Scenario | Governance Control |
|---|---|---|
| Hallucination | AI generates inaccurate KPI commentary or unsupported explanations | Human review before publication; source validation; output sampling |
| Sensitive data exposure | Staff enter confidential, personal, or operational data into an external GenAI tool | Acceptable use policy; data classification; prompt restrictions; privacy review |
| Weak source traceability | AI output cannot be traced back to source data or business rules | RAG traceability checklist; source-linked outputs; metadata documentation |
| Bias and fairness risk | AI-generated recommendations disadvantage specific user groups or service areas | Bias review; fairness testing; business owner validation |
| Overreliance | Staff accept AI-generated outputs without professional judgment | Human-in-the-loop requirement; approval workflow; user guidance |
| Vendor risk | Third-party AI tool uses organizational data for training or secondary purposes | Vendor review checklist; contractual data-use restrictions; security review |
| Prompt injection | Malicious or unexpected prompt input manipulates output | Prompt control template; security testing; restricted deployment |
| Inconsistent outputs | AI produces different answers for similar tasks | Standardized prompts; output review; quality monitoring |
| Lack of accountability | No clear owner exists for AI use-case approval or incident response | AI use-case owner; data steward; escalation pathway |
| Model drift | AI performance declines over time as data or operations change | Scheduled monitoring; review frequency; issue log |

## Practical use

This mapping is designed to help governance, privacy, analytics, and risk teams translate generative AI risks into operating controls, review steps, and monitoring practices.

