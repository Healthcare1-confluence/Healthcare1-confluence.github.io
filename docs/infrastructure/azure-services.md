# Azure Services

## Service Overview

| Service | SKU/Variant | Usage |
|---------|------------|-------|
| **Azure OpenAI** | GPT-5.4-mini | All LLM calls – coordinator, agents, synthesis |
| **Azure SQL Database** | Standard | Member, claims, appointments, pre-auth data |
| **Azure AI Search** | Semantic + Keyword | Plan benefits corpus with hybrid search |
| **Azure Kubernetes Service** | Managed | Container orchestration for FastAPI pods |
| **Azure API Management** | Standard | JWT validation, rate limiting, API gateway |
| **Azure Monitor** | Log Analytics + Application Insights | Structured logging, custom metrics, alerting |
| **MongoDB Atlas** | Managed | LangGraph checkpoint storage |

### Azure OpenAI Configuration

- **Model**: GPT-5.4-mini (optimized for cost and speed)
- **Endpoint**: Region-specific (East US recommended for latency)
- **Quota**: Request appropriate tokens-per-minute (TPM) limits
- **Monitoring**: Track token usage per intent via LangFuse

### Azure SQL Configuration

- **Tables**:
  - `Member` — Demographics
  - `Claims_Professional`, `Claims_Institutional` — Claim records
  - `pre_auth` — Authorization constraints
  - `Provider_Slot_2` — Available slots
  - `Appointment` — Booked appointments

- **Access**: pyodbc with parameterised queries
- **Connection Pooling**: Managed at application level
- **Backup**: Daily automated backups

### Azure AI Search Configuration

- **Index**: Plan benefits documents
- **Search Type**: Hybrid (keyword + semantic re-rank)
- **Filtering**: plan_id filter on every search
- **Result Count**: Top-5 chunks per search

