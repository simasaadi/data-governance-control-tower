# Controls Framework

## Objective
This controls framework shows how governance expectations are translated into concrete operational controls.

## Control Areas

### 1. Metadata Controls
Purpose: ensure data assets are documented and interpretable.

Examples:
- Each critical asset must have an assigned owner and steward.
- Each published KPI should have a documented definition.
- Data classification should be recorded for each governed asset.

### 2. Data Quality Controls
Purpose: detect and reduce completeness, validity, and integrity issues.

Examples:
- Required identifiers cannot be null.
- Status and category fields must use approved values.
- Numeric measures must stay within expected ranges.
- Exceptions should be logged and assigned for follow-up.

### 3. Access Governance Controls
Purpose: ensure access to sensitive or non-routine data is reviewed and traceable.

Examples:
- Sensitive access requests require documented rationale.
- Conditional approvals must include scope limits or expiry dates.
- Denied requests should still be retained in the decision log.

### 4. Stewardship and Accountability Controls
Purpose: clarify who is responsible for governance actions.

Examples:
- Owners are accountable for business decisions about the data.
- Stewards are responsible for definitions, data quality coordination, and issue follow-up.
- Custodians support storage, movement, logging, and technical administration.

### 5. Issue Management Controls
Purpose: support structured escalation and remediation.

Examples:
- Data issues must be logged with severity, owner, and target date.
- Critical issues should remain visible until resolution.
- Root causes should be captured where known.

### 6. AI Governance Controls
Purpose: extend governance to AI and generative AI use cases.

Examples:
- AI use cases must be registered before deployment.
- Higher-risk use cases require risk review and human oversight.
- Outputs used in operations or reporting should remain reviewable and auditable.

## Monitoring Approach
The repository uses governance KPIs to make control performance visible over time. These indicators help show whether governance is improving, where risks remain, and which controls need attention.

## Design Principle
The core principle is that governance should be observable in day-to-day work through artifacts, checks, decisions, and metrics.
