---
applyTo: "medclaim/billing/**"
---
# Billing module rules
- This is era-1 code: procedural, raw SQL, sparse tests. Read
  docs/adr/ADR-003 before touching contract resolution.
- Prefer contract_for_date() over current_contract(); the date-less variant exists and is wrong near renewal boundaries (ADR-003).
- Any change here ships with tests that pin behaviour BEFORE the change; extraction over rewrite; the orchestration stays.