# Case Study: Service Request Triage Assistant

## Use case

A generative AI assistant drafts suggested categories and response summaries for incoming service requests.

## Governance question

Can this AI use case be approved for controlled internal use?

## Business value

The use case may reduce manual triage time, improve consistency in service categorization, and help staff respond more quickly to recurring request types.

## Key risks
- Hallucinated or inaccurate categorization
- Sensitive information exposure
- Overreliance by staff
- Inconsistent service decisions
- Weak audit trail
- Lack of source traceability

## Required controls
- Human review before action
- No direct personal identifiers in prompts
- Approved source fields only
- Output logging
- Monthly sample review
- Escalation path for incorrect outputs
- Privacy and security review before deployment
- Clear limitation statement for users

## Data readiness findings

| Area | Finding | Status |
|---|---|---|
| Ownership | Business owner and data steward identified | Pass |
| Data quality | Critical category fields require profiling | Partial |
| Metadata | Service category definitions need documentation | Partial |
| Lineage | Source-to-output flow not fully documented | Fail |
| Classification | Data classified as internal | Pass |
| Access | Role-based access required | Partial |

## Decision

Conditional approval for internal pilot only.

## Approval conditions

The use case may proceed only if human review remains mandatory, sensitive data is excluded from prompts, outputs are logged, and the review owner completes monthly quality checks.

## Governance recommendation

This use case should not move to production until lineage documentation, prompt controls, privacy review, and monthly monitoring procedures are complete.

