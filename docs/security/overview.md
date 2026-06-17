# Security Overview

## Authentication and Authorization

- **API Authentication**: Azure AD Bearer JWT validated by FastAPI middleware
- **Service-to-Service**: Azure Managed Identity for OpenAI, SQL, AI Search
- **Secrets Management**: Azure Key Vault for all connection strings and API keys
- **RBAC**: AKS pods have Reader access to Key Vault secrets only

## Data Protection

### Encryption In Transit
- TLS 1.3 for all inter-service communication
- MongoDB Atlas with encrypted connections
- Azure SQL with TLS encryption

### Encryption At Rest
- Azure SQL: Transparent Data Encryption (TDE) with AES-256
- MongoDB Atlas: Default encryption enabled
- Application logs: Encrypted at rest in Azure Storage

### PHI Handling
- **PHI Detection**: All LLM responses pass through masking pipeline
- **Parameterised Queries**: All Azure SQL calls use pyodbc placeholders (no string interpolation)
- **Field Redaction**: Member IDs, DOB, clinical data redacted in logs
- **Prompt Minimization**: LLM prompts inject only minimum required member data

