# Roadmap

## Near-Term (Next 3 Months)

### ✓ Appointment Scheduler Agent
- **Status**: In Progress
- **Description**: Eight-tool ReAct agent for full appointment lifecycle
- **Includes**: Slot availability, booking, rescheduling, cancellation with pre-authorization enforcement
- **Impact**: Reduce appointment booking handle time to <30 seconds

### ⏳ Streaming Responses
- **Status**: Planned
- **Description**: LangGraph streaming to return partial answers token-by-token
- **Benefit**: Reduce perceived latency for long responses
- **Expected Impact**: Improved member experience

### ⏳ LangFuse Dashboards
- **Status**: Planned
- **Description**: Per-intent analytics dashboards
- **Tracks**: Model accuracy, HITL rate trends, cost-per-query, latency distributions
- **Users**: Platform team for monitoring and optimization

### ⏳ Prompt Versioning
- **Status**: Planned
- **Description**: LangFuse-backed A/B testing framework for prompts
- **Enables**: Data-driven improvements to INTENT_PROMPT and GENERAL_PROMPT
- **Benefit**: Iterate on classification accuracy without full redeployment

---

## Medium-Term (3–9 Months)

### Multi-Language Support
- **Description**: Language detection in coordinator, language-specific prompts
- **Languages**: Spanish, Mandarin, Vietnamese (based on market demand)
- **Impact**: Expand addressable member population

### Pre-Authorization Agent
- **Description**: Dedicated agent for complex pre-auth workflows
- **Use Cases**: Appeal workflows, authorization extension requests, clinical reviews
- **Impact**: Higher automation rate for pre-auth-related calls

### Outbound Call Workflow
- **Description**: Proactive outreach initiated by platform
- **Use Cases**: Appointment reminders, care gap outreach, benefits enrollment notifications
- **Impact**: Improve member engagement, reduce no-shows

### Azure AI Search Index Upgrade
- **Description**: Vector embeddings for benefit documents
- **Benefit**: Semantic search accuracy improvement for benefit queries
- **Expected Accuracy Lift**: 5–10% improvement in relevance ranking

---

## Long-Term (9+ Months)

### Federated Multi-Tenant Architecture
- **Description**: Separate MongoDB databases per health plan tenant
- **Benefit**: Data isolation, HIPAA compliance per payer, independent scaling
- **Impact**: Enable SaaS pricing model

### Fine-Tuned Intent Classifier
- **Description**: Replace GPT-5.4-mini coordinator with smaller fine-tuned model
- **Benefits**: Lower latency, reduced cost-per-query, faster inference
- **Training Data**: Real traffic patterns after 6+ months of production data

### Agent Evaluation Framework
- **Description**: Automated regression tests via LangSmith / LangFuse evaluations
- **Enables**: Safe prompt iteration without manual testing
- **Impact**: Faster iteration cycles, higher confidence in changes

### Compliance-Driven Intelligence
- **Description**: Encode healthcare compliance standards as first-class knowledge sources
- **Includes**: HIPAA Technical Safeguards, insurance plan contracts, CMS billing specs, member SLAs
- **Benefit**: Policy-to-response traceability, compliance-aware root cause analysis

---

## Parking Lot (Future Consideration)

- **Voice Emotion Detection**: Detect member frustration, escalate appropriately
- **Predictive Escalation**: Predict calls likely to require manual escalation before they occur
- **Provider Integration**: Real-time EHR integration for clinical notes, medication history
- **Patient Engagement**: Follow-up outreach campaigns based on call outcomes

---

## Success Metrics for Each Phase

### Near-Term Success
- ✓ Appointment automation rate reaches 60%
- ✓ HITL rate stabilizes <15%
- ✓ Intent accuracy validated ≥95%

### Medium-Term Success
- ✓ Multi-language support reaches 20% of call volume
- ✓ Outbound appointment reminders reduce no-show rate by 15%
- ✓ Cost-per-call reduced by 40% vs baseline

### Long-Term Success
- ✓ Multi-tenant platform deployed with 3+ health plan customers
- ✓ Fine-tuned model reaches parity with GPT-5.4-mini at 50% lower cost
- ✓ Compliance violations: zero

