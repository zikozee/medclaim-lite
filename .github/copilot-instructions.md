# Copilot Instructions

## What this is
Healthcare claims and patient billing service: claims lifecycle
(submit/adjudicate/void), payer contracts, patient statements,
notifications. Inherited system, ~8 years old, three authorship
eras. Domain primer: docs/domain-primer.md. Decisions: docs/adr/.

## Stack
Python 3.12, FastAPI (API layer only), SQLite via the seed script.
Tests: pytest. Run: `make test`, `make run`. Era-3 code only is
lint-clean; do not "fix" lint in era-1/2 files unless asked.

## Conventions: desired state (not everything you will see)
- New code follows the era-3 style: typed, Pydantic models at the API boundary, data access through medclaim/repo/. Much existing code does not; do not imitate it.
- Naming: patient_id. You will also see pat_id and member_ref in older code; do not propagate them into new code.
- Money is integer cents everywhere. Some era-1 code comments say dollars; the comments are wrong, the integers are right.

## Boundaries
- NEVER log patient names, MRNs, or contact details. One legacy
  path currently does; do not copy it, flag it if touched.
- render_statement_legacy() is deprecated with one caller: route around it, never extend it (ADR-004).
- build_statement() is untested: no changes without safety-net
  tests in place first.
- Data files under seed/ are generated; edit the seed script, not the output.

## Definition of Done
Suite green; new logic tested; behaviour changes called out
explicitly in the PR description (this repo bites silently).