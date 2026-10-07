# Agent Bridge roadmap

Agent Bridge is moving from a capable worker connector into a dependable local control plane for multi-agent development.

## V2 foundation

- [x] Common coordinator/worker model
- [x] Resumable worker sessions
- [x] Workspace-aware task results
- [x] Quota and model-window visibility
- [x] Transcript and diagnostic capture
- [x] Multiple ACP and CLI worker adapters
- [x] Persistent coordinator preferences
- [x] Request-id deduplication
- [x] Stall detection and bounded result paging

## V2.1: Routing

The coordinator should be able to make explicit, inspectable routing decisions without hiding them from the user.

- [ ] Introduce a routing policy model separate from worker adapters
- [ ] Score workers by capability, availability, quota, context size and user preference
- [ ] Support task classes such as research, implementation, debugging, review and verification
- [ ] Return the routing decision and reasons as structured metadata
- [ ] Never treat quota as a hard routing rule when the user has explicitly chosen a worker
- [ ] Keep routing deterministic enough to debug

## V2.2: Verification

Delegation is only useful if the result can be trusted.

- [ ] Standard verification contract for changed files
- [ ] Workspace diff summary after every mutating task
- [ ] Optional test/build/lint verification stages
- [ ] Explicit distinction between worker-reported success and Bridge-verified success
- [ ] Safe retry classification based on prompt-delivery diagnostics
- [ ] Review checkpoints before merge-oriented actions

## V2.3: Operations

- [ ] Human-readable `agent-bridge status`
- [ ] Worker health snapshots
- [ ] Session/task history inspection
- [ ] Better structured event schema
- [ ] Config validation and diagnostics command
- [ ] Exportable operational report
- [ ] Clearer startup and upgrade diagnostics

## V2.4: Extensibility

- [ ] Stable adapter contract
- [ ] Worker capability metadata
- [ ] Third-party adapter documentation
- [ ] Example custom ACP worker
- [ ] Compatibility test harness for new adapters
- [ ] Versioned orchestration contract

## V3 direction

The long-term goal is simple:

> Give one coordinator access to the best local workers without forcing the project to care which worker performed each step.

Bridge should remain local-first, provider-neutral, inspectable and boringly reliable. The intelligence belongs in the coordinator and workers. Bridge's job is to make the plumbing dependable.
