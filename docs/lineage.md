# Data Lineage Overview

## Asset Lineage Summaries

### DA001 - Customer Service Requests
Source system: CRM  
Flow: CRM -> daily extract -> quality checks -> analyst review -> reporting/dashboard use

### DA002 - Work Order History
Source system: Maximo  
Flow: Maximo -> operational export -> quality checks -> curated dataset -> maintenance reporting

### DA003 - Fleet Maintenance Logs
Source system: M5 Fleet  
Flow: M5 Fleet -> scheduled extract -> analyst transformation -> internal reporting

### DA004 - Route Operations GPS
Source system: Route Optimization Platform  
Flow: route system -> GPS event logs -> exception analysis -> operational review

### DA005 - Public Dashboard Metrics
Source system: BI Semantic Layer  
Flow: curated reporting tables -> KPI calculation -> dashboard publication

## Lineage Status Definitions
- None: no documented lineage available
- Partial: major upstream and downstream flow is known, but transformations are not fully documented
- Complete: source, transformations, and downstream outputs are documented end to end

## Governance Note
Lineage is included here as a governance artifact because trusted reporting depends on understanding where data comes from, how it changes, and where it is used.
