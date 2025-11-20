# BOARDROOM-13 LAWS (Constitution Extract)

Existing articles omitted for brevity.

## ARTICLE 11 — VORTEX ROUTING LAW (DRAFT ONLY)

> **STATUS:** DRAFT — NOT ENFORCED IN RUNTIME  
> This article describes a proposed future-state routing regime for multi-node Sovereign deployments.  
> It is **not** active. It MUST NOT block, influence, or alter any live routing decisions until
> `FEATURE_VORTEX` is explicitly enabled by Boardroom vote and recorded in the ledger.

### 11.1 Scope

11.1.1 Vortex Routing Law defines additional constraints and health metrics for message paths between
logical pods in a multi-node Sovereign mesh.

11.1.2 A **node** is a physical or logical machine participating in the Sovereign mesh (for example:
`node0`, `node1`, `node2`).

11.1.3 A **domain** is a functional class of workload (for example: `evidence`, `property`, `ops`).

11.1.4 A **pod** is the combination of a node and a domain (for example: `node0:property`).

11.1.5 A **path** is an ordered list of pods representing the intended route for a message or state
transition.

11.1.6 An **epoch** is a configured time window over which mesh health is measured (for example:
one day).

11.1.7 While this article is in DRAFT status:

- Vortex simulations and metrics MAY be logged.
- Vortex constraints MUST NOT cause requests to be blocked, downgraded, or rerouted.
- Any enforcement code MUST be gated behind `FEATURE_VORTEX = True`.

---

### 11.2 3-Resonance Rule (Critical Path Diversity)

11.2.1 A **critical path** is any path associated with actions that can directly:

- move or commit funds,
- create or modify legal filings,
- change external commitments, or
- alter constitutional configuration.

11.2.2 A critical path MUST satisfy both of the following conditions:

- (a) Length of at least three (3) hops; and
- (b) Visits at least three (3) distinct nodes **or** three (3) distinct domains.

11.2.3 If a critical path does not satisfy 11.2.2, the system SHOULD record the condition as:

- `CVF.VORTEX_INSUFFICIENT_RESONANCE` (simulation mode), and
- mark `would_reject = true` in vortex simulation logs.

11.2.4 While this article remains in DRAFT status, 11.2.2 MAY be evaluated and logged but MUST NOT
be used to block execution.

---

### 11.3 6-Flow Rule (Cross-Node Mesh Health)

11.3.1 For each epoch, the mesh SHOULD observe at least six (6) cross-node edges. A cross-node edge
is a transition where the source pod and target pod belong to different nodes.

11.3.2 If, within an epoch, fewer than six (6) cross-node edges are observed, the mesh health SHOULD
be classified as `DEGRADED_VORTEX_FLOW`.

11.3.3 While health is `DEGRADED_VORTEX_FLOW`, any vortex simulation MUST record this state in its
output, and readiness checks SHOULD surface it to operators.

11.3.4 While this article remains in DRAFT status, 6-Flow classification is informational only and
MUST NOT change routing behaviour.

---

### 11.4 9-Activation Rule (Pod Participation)

11.4.1 Over a configured activation window of nine (9) consecutive epochs, each configured pod
SHOULD:

- (a) send at least one (1) message; and
- (b) receive at least one (1) message.

11.4.2 A pod that fails 11.4.1 is considered **starved** for that activation window.

11.4.3 Starved pods SHOULD be reported via mesh health reports and MAY be treated as a configuration
smell or capacity planning issue.

11.4.4 Violations of 11.4.1 MUST NOT be treated as constitutional failures. They are advisory only.

---

### 11.5 Spiral Preference (Routing Heuristic)

11.5.1 A **spiral pattern** is a path where a pod is visited again after exactly two intermediate
hops (for example: `A ? B ? A`).

11.5.2 The routing system MAY assign higher scores to paths that exhibit spiral patterns, provided
all other constitutional requirements are satisfied.

11.5.3 Spiral preference is a heuristic only. It MUST NOT override:

- IAM / RBAC,
- track constraints (`stable` / `insider`),
- cost ceilings,
- or any other active constitutional checks.

---

### 11.6 No Dead-End Pods (Topology Smell Detection)

11.6.1 A pod is considered **dead-end** if, for more than one (1) epoch, the combined number of
incoming and outgoing edges actually used is less than two (2).

11.6.2 Dead-end pods SHOULD be logged as a topology smell and MAY generate a configuration proposal
for additional edges or rebalancing.

11.6.3 The system MUST NOT automatically alter topology, add edges, or modify routing behaviour as a
direct consequence of 11.6.2. Any topology changes MUST follow the existing governance and change
control processes.

---

### 11.7 Implementation Status

11.7.1 While `FEATURE_VORTEX` remains `False`:

- Vortex Routing Law is treated as DRAFT.
- Only simulation functions MAY run.
- No enforcement or blocking based on this article is permitted.

11.7.2 Activation of Vortex Routing Law requires:

- (a) explicit Boardroom approval recorded in the ledger; and
- (b) a code change that sets `FEATURE_VORTEX = True`; and
- (c) a tagged release noting activation.

11.7.3 Until 11.7.2 is satisfied, this article remains normative guidance and MUST NOT be described
as active behaviour in any external communication.
