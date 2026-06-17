# Claims Agent

Specialist agent for claim status and denial reason queries.

## Tools

- `query_member_info` — Validates member existence
- `query_claims` — Professional + Institutional claims (max 20 records)
- `query_preauth` — Pre-authorization status

## Database

Azure SQL via pyodbc with parameterised queries.

