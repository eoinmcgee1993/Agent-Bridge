# Agent Bridge architecture

## The model

Agent Bridge is a control plane, not another model provider.

```text
User
 │
 ▼
Coordinator
 │
 ▼
Agent Bridge MCP
 │
 ├── Policy / routing
 ├── Registry
 ├── Session lifecycle
 ├── Workspace tracking
 ├── Persistence
 ├── Quota visibility
 └── Observability
 │
 ├── Grok
 ├── Kimi
 ├── Antigravity
 ├── Claude
 ├── Codex
 ├── OpenCode
 ├── DeepSeek
 ├── Devin
 ├── Cursor
 ├── ZCode
 └── MiniMax
```

## Boundaries

### Coordinator

The coordinator owns intent, architecture and acceptance. It can ask Bridge to delegate work, but a worker's self-report is never the final authority.

### Registry

The registry is the runtime authority for sessions and tasks. It owns lifecycle, persistence, task state, result collection and worker adapters.

### Adapter

An adapter translates Bridge's common task/session contract into a worker's native protocol. Provider-specific quirks belong here.

### Observability

Transcripts, diagnostics, quota state and workspace snapshots provide evidence about what happened. They should remain useful even when a worker crashes or reports an ambiguous result.

## Routing

Routing should be policy-driven rather than adapter-driven.

A routing decision should be explainable:

```json
{
  "task_class": "implementation",
  "selected": "grok",
  "reasons": [
    "worker available",
    "matches implementation capability",
    "quota healthy"
  ],
  "alternatives": ["kimi", "codex"]
}
```

The selected worker is still a policy decision, not a hidden side effect.

## Failure model

A timeout is not automatically a failure.

A worker error is not automatically safe to retry.

If prompt delivery is uncertain, Bridge must preserve that uncertainty and avoid blind replay. A clean result requires evidence from the worker plus workspace-level verification where applicable.

## Design rules

1. Keep provider-specific behaviour inside adapters.
2. Keep routing separate from worker lifecycle.
3. Keep coordinator preferences explicit and persistent.
4. Never turn quota telemetry into an invisible hard dependency.
5. Preserve evidence when things fail.
6. Make mutating work verifiable.
7. Prefer small, testable policy objects over a giant routing function.
8. Keep the local-first architecture. Bridge should not require a hosted control plane.
