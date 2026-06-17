# Design Decisions and Trade-offs

## Key Architectural Decisions

### 1. LangGraph over Custom Orchestration

**Decision**: Use LangGraph StateGraph for graph orchestration

**Rationale**:
- ✓ Built-in checkpoint/resume capability
- ✓ Conditional routing with type-safe state
- ✓ Proven pattern for multi-agent systems
- ✓ Community-backed, actively maintained

**Trade-off**:
- ✗ Adds LangGraph dependency (vendor lock-in risk)
- ✗ Graph topology less directly visible than hand-crafted code

### 2. Single CallWorkflowState Class

**Decision**: All data flows through one CallWorkflowState TypedDict

**Rationale**:
- ✓ Eliminates inter-node data passing complexity
- ✓ Type-safe state transitions
- ✓ Single source of truth per conversation
- ✓ Easier testing and debugging

**Trade-off**:
- ✗ State grows as new intents are added
- ✗ Requires careful field lifecycle management

### 3. MongoDBSaver + MemorySaver Fallback

**Decision**: Primary MongoDB, fallback to in-memory storage

**Rationale**:
- ✓ Zero-downtime operation (graceful degradation)
- ✓ Multi-turn HITL works even during MongoDB maintenance
- ✓ Consistent checkpointing across deployment environments

**Trade-off**:
- ✗ During fallback: HITL not durable across application restarts
- ✗ Requires fallback monitoring to alert on MongoDB unavailability

### 4. Safety Net for Claims without Member_ID

**Decision**: Python validation layer overrides LLM output for edge cases

**Rationale**:
- ✓ Belt-and-suspenders protection against LLM hallucination
- ✓ Cannot mis-serve member due to missing identifier
- ✓ Prevents accidental privacy violation

**Trade-off**:
- ✗ Can over-trigger if LLM extracts partial IDs
- ✗ Threshold may need tuning based on real traffic patterns

### 5. ReAct Agent Loops for Specialist Agents

**Decision**: Use LangChain ReAct pattern for multi-turn tool use

**Rationale**:
- ✓ Dynamic tool selection (handles variable query patterns)
- ✓ Transparent reasoning (tool calls are visible in logs)
- ✓ Proven pattern for agent systems
- ✓ No rigid decision trees needed

**Trade-off**:
- ✗ ReAct loops can be verbose for simple cases
- ✗ Requires careful prompt engineering to avoid infinite loops
- ✗ Token usage may be higher than optimized alternatives

### 6. _strip_markdown() on All LLM Output

**Decision**: Remove markdown formatting from all agent responses

**Rationale**:
- ✓ TTS engines cannot render markdown
- ✓ Plain text ensures voice readability
- ✓ Enforces consistent output format
- ✓ Prevents accidental formatting in sensitive member responses

**Trade-off**:
- ✗ Strips intentional formatting (asterisks, headers)
- ✗ Rich content delivery must use separate digital channel

### 7. Lazy Graph Compilation with Singleton Cache

**Decision**: Compile graph on first request, cache thereafter

**Rationale**:
- ✓ Eliminates per-request graph assembly overhead
- ✓ No cold-start cost during pod initialization
- ✓ Scales linearly with request volume (not compilation cost)

**Trade-off**:
- ✗ First request experiences compilation latency (~500ms)
- ✗ If checkpointer changes at runtime, compiled graph must be invalidated manually

### 8. One-Active-Appointment-Per-Member

**Decision**: Enforce maximum one scheduled appointment per member at any time

**Rationale**:
- ✓ Prevents double-booking conflicts
- ✓ Simplifies reschedule/cancel logic
- ✓ Aligns with typical scheduling workflows

**Trade-off**:
- ✗ Members must cancel before booking new appointments
- ✗ Less flexible for members needing multiple upcoming appointments

### 9. Pre-Authorization Enforcement

**Decision**: Appointment bookings restricted to pre-authorized providers only

**Rationale**:
- ✓ Prevents out-of-network bookings (compliance risk)
- ✓ Enforces insurance plan rules automatically
- ✓ Reduces claim denials at booking time

**Trade-off**:
- ✗ Members cannot book out-of-network even if slots exist
- ✗ Requires pre-auth data to be current (fallback to general responder if outdated)

### 10. Natural-Language Date/Time Parsing Client-Side

**Decision**: Parse dates and times in Python tools, not SQL

**Rationale**:
- ✓ Prevents SQL injection
- ✓ Supports human-friendly expressions ("next 5 days", "this weekend")
- ✓ Consistent parsing logic across tools

**Trade-off**:
- ✗ Requires comprehensive parsing logic (dateutil dependency)
- ✗ Parsing logic must be maintained as natural language evolves

---

## Summary Trade-off Matrix

| Decision | Benefit | Cost |
|----------|---------|------|
| LangGraph | Proven, community-backed | Vendor dependency |
| Single State | Simplicity, type safety | State bloat over time |
| MongoDB + Fallback | High availability | Operational complexity |
| Safety Net | Mis-service prevention | Over-triggering possible |
| ReAct Loops | Flexibility, transparency | Token usage, complexity |
| _strip_markdown | TTS readability | Rich content unavailable |
| Lazy Compilation | No startup cost | First request latency |
| One Active Appt | Simplicity | User flexibility reduced |
| Pre-Auth Enforcement | Compliance | Out-of-network blocked |
| Client-side Parsing | Injection prevention | Parsing complexity |

