# Runtime Architecture

## Three-Tier Agent Hierarchy

The platform organizes agents into three logical tiers:

### Tier 0: Orchestration Agents
Model: Azure OpenAI GPT-5.4-mini (fast + cheap)

| Agent | Purpose | Calls |
|-------|---------|-------|
| **IntentClassifier** | Classify intent from utterance | Once per query |
| **Coordinator** | Determine agent dispatch plan | After intent known |
| **HITLGuard** | Validate required data presence | Before specialist agent |
| **ReflectionGuard** | Strip markdown, check for PHI | After agent response |

### Tier 1: Primary Specialist Agents
Model: Azure OpenAI GPT-5.4-mini (multi-turn ReAct loop, max 5 tool calls)

| Agent | Domain | Tools |
|-------|--------|-------|
| **ClaimsAgent** | Claims status and denial reasons | query_member_info, query_claims, query_preauth |
| **BenefitsAgent** | Plan coverage and benefits | get_member_plan_id, search_plan_benefits |
| **AppointmentAgent** | Appointment lifecycle | 8 tools for slots, booking, rescheduling |
| **GeneralAgent** | Greetings and miscellaneous | No tools (single LLM call) |
| **CausalityAgent** | Denial chain analysis | Spawns sub-agents |

### Tier 2: Sub-Agents
Model: Azure OpenAI GPT-5.4-mini (single tool call, no loop)

**Spawned by ClaimsAgent:**
- `MemberLookupSubAgent` — Validates member existence
- `ClaimsQuerySubAgent` — Professional + institutional claims
- `PreAuthSubAgent` — Pre-authorization status

**Spawned by BenefitsAgent:**
- `PlanResolverSubAgent` — Resolves plan_id from SQL
- `BenefitsSearchSubAgent` — Azure AI Search retrieval

**Spawned by AppointmentAgent:**
- `SlotFinderSubAgent` — Available slot queries
- `BookingSubAgent` — Atomic booking operations
- `RescheduleSubAgent` — Appointment modifications
- `AppointmentFetchSubAgent` — Upcoming schedule lookup

## Execution Flow

```
Query arrives
    ↓
[Tier 0] Coordinator classifies intent
    ↓
[If HITL needed] ReflectionGuard returns clarification
    ↓
[Tier 1] Specialist Agent selected
    ├→ ReAct Loop Iteration 1 (Tool selection)
    ├→ [Tier 2] Sub-agent spawned if needed
    ├→ Tool result returned to Tier 1 agent
    ├→ Repeat until answer is complete (max 5 iterations)
    ↓
[Tier 0] ReflectionGuard formats response
    ↓
Response delivered

```

## Performance Considerations

- **Tier 0 agents** optimized for speed (classification, routing, safety checks)
- **Tier 1 agents** balance accuracy with latency (ReAct loops with timeout)
- **Tier 2 agents** focused single operations (no loops, minimal overhead)
- **Caching** of compiled graph eliminates per-request assembly cost

