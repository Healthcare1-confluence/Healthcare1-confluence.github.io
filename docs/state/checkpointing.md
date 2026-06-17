# Checkpointing and State Persistence

## MongoDB Checkpointer (Primary)

MongoDBSaver provides durable cross-request state for HITL scenarios and multi-turn conversations.

| Property | Value |
|----------|-------|
| **Database** | directline_db |
| **Collection 1** | langgraph_checkpoints — Full serialised CallWorkflowState per thread_id |
| **Collection 2** | langgraph_checkpoint_writes — Incremental write operations |
| **Connection Timeout** | 5 seconds |
| **Connection String** | MONGODB_URL environment variable |

## MemorySaver Fallback

When MongoDB unavailable, LangGraph uses built-in MemorySaver:
- ✓ Stores checkpoints in process memory
- ✓ Enables single-session interactions
- ✗ Not durable across application restarts

## Thread ID Management

The thread_id is a UUID that:
- ✓ Generated on first invocation of a conversation
- ✓ Returned in every InvokeResponse
- ✓ Passed back by client in subsequent requests
- ✓ Used as LangGraph config key for checkpoint selection
- ✓ Scoped to a single member contact session

