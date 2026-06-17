# Observability and Monitoring

## Key Metrics

All application logs are structured JSON emitted to stdout, captured by AKS, and forwarded to Azure Log Analytics.

### Custom Metrics

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `graph_invocation_count` | Counter | Total call workflow invocations | — |
| `graph_intent_distribution` | Histogram | Breakdown by intent type | — |
| `graph_execution_duration_ms` | Histogram | End-to-end execution time (P50, P95, P99) | P95 > 5s |
| `hitl_trigger_rate` | Gauge | % invocations triggering HITL | > 30% |
| `llm_token_usage` | Counter | Tokens per model per intent | High spend spike |
| `mongodb_checkpoint_errors` | Counter | MongoDB connection failures | > 0 in 5min |

### Log Levels

- **DEBUG**: Development environments only
- **INFO**: Standard operation tracking
- **WARNING**: HITL triggers, fallback events
- **ERROR**: Unhandled exceptions, service failures

### Alerting Rules

| Alert | Severity | Action |
|-------|----------|--------|
| P95 latency > 5s | 🔴 High | Review LLM/SQL performance |
| HITL rate > 30% | 🟡 Medium | Review intent classification accuracy |
| MongoDB unavailable | 🔴 High | Escalate to infrastructure |
| Error rate > 1% | 🔴 High | Review Application Insights |
| Token budget exceeded | 🟡 Medium | Compress prompt history |

## LangFuse Integration (Optional)

When enabled via `LANGFUSE_ENABLED=true`:
- Each graph invocation creates a root trace
- Coordinator and agent nodes create child spans
- Traces queryable by thread_id, intent, member_id
- Token usage and cost tracked automatically

