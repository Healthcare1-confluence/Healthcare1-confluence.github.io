# Graph Design

## LangGraph Topology

The platform uses LangGraph's `StateGraph` to define a one-shot decision tree topology:
- Every invocation enters at `__start__`
- Passes through the coordinator
- Routes to one specialist agent (or HITL gate)
- Terminates at `__end__`
- No cycles except internal ReAct tool-use loops

## Graph Nodes

| Node | Type | Responsibility |
|------|------|-----------------|
| `__start__` | Virtual | LangGraph entry point. Injects initial CallWorkflowState. |
| `coordinator` | Custom | Classifies intent, extracts identifiers, sets clarification flag. |
| `claims_agent` | Agent Node | ReAct loop with query_member_info, query_claims, query_preauth tools. |
| `benefits_agent` | Agent Node | ReAct loop with get_member_plan_id and search_plan_benefits tools. |
| `appointment_agent` | Agent Node | ReAct loop with 8 appointment lifecycle tools. |
| `general_responder` | Custom | Single LLM call with GENERAL_PROMPT. No tools. |
| `__end__` | Virtual | Graph terminal node. Returns final state. |

## Graph Edges

| Edge | Condition |
|------|-----------|
| `START → coordinator` | Unconditional. Every invocation enters here. |
| `coordinator → claims_agent` | intent='claims' AND clarification_needed=false |
| `coordinator → benefits_agent` | intent='benefits' AND clarification_needed=false |
| `coordinator → appointment_agent` | intent='appointment' AND clarification_needed=false |
| `coordinator → general_responder` | intent='general' OR 'default' AND clarification_needed=false |
| `coordinator → __end__` | clarification_needed=true (HITL gate) |
| `claims_agent → __end__` | Unconditional. Agent completes. |
| `benefits_agent → __end__` | Unconditional. Agent completes. |
| `appointment_agent → __end__` | Unconditional. Agent completes. |
| `general_responder → __end__` | Unconditional. Responder completes. |

## Compilation and Startup

### Lazy Singleton Pattern

```python
class CallWorkflow:
    _compiled_graph = None
    
    def compile(self):
        if self._compiled_graph is not None:
            return self._compiled_graph  # Fast path (subsequent calls)
        
        # First call only: expensive setup
        checkpointer = _get_checkpointer()  # MongoDB or MemorySaver
        graph = _build_state_graph()
        self._compiled_graph = graph.compile(checkpointer=checkpointer)
        return self._compiled_graph
```

### Startup Sequence

1. FastAPI starts → calls `CallWorkflow.compile()`
2. MongoClient created with 5-second connection timeout
3. If MongoDB connects → MongoDBSaver instantiated
4. If MongoDB timeout → MemorySaver fallback
5. StateGraph nodes added: coordinator, claims_agent, benefits_agent, appointment_agent, general_responder
6. Graph compiled into CompiledGraph
7. CompiledGraph cached as singleton
8. Subsequent requests retrieve from cache (no per-request assembly cost)

## Configuration

### Environment Variables

```bash
# MongoDB Persistence
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/

# LLM & Data Services
AZURE_OPENAI_ENDPOINT=https://...
OPENAI_API_KEY=...
AZURE_SQL_CONNECTION_STRING=...
AZURE_SEARCH_ENDPOINT=...
AZURE_SEARCH_KEY=...
AZURE_SEARCH_INDEX_NAME=benefits
```

