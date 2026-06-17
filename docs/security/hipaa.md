# HIPAA Alignment

## HIPAA Controls Implementation

| Control | Implementation |
|---------|-----------------|
| **Access Controls** | Azure AD authentication + RBAC on all data stores. No anonymous access. |
| **Audit Logging** | All invocations logged: thread_id, intent, member_id (hashed), timestamp to Azure Monitor |
| **Data Minimisation** | LLM prompts inject only minimum required member data. Full demographics not sent unless required. |
| **PHI in Checkpoints** | MongoDB Atlas field-level encryption available for additional compliance |
| **Retention** | Configurable TTL per organisation. Default: 30-day retention with automated deletion. |
| **Business Associate Agreement** | Azure OpenAI, Azure SQL, MongoDB — covered under BAA where applicable |

## Compliance Checklist

- ✓ PHI is never logged in plain text
- ✓ Parameterised queries prevent injection attacks
- ✓ Encryption covers data in transit and at rest
- ✓ Access to sensitive data is audited
- ✓ Retention policies are enforced
- ✓ Business Associate Agreements are in place

## Risk Mitigation

- **LLM Prompt Risk**: Data minimisation + _strip_markdown() to prevent accidental PHI in outputs
- **Database Risk**: Parameterised queries + encryption + RBAC
- **Network Risk**: TLS 1.3 + Azure managed networking
- **Application Risk**: Regular dependency updates, security scanning in CI/CD

