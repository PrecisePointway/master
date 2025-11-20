# VORTEX ROUTING — WHY WE KILLED SUDOKU

## 1. What went wrong with the Sudoku metaphor

Sudoku is a constraint puzzle:
- fixed grid
- no repetitions
- static board
- victory = solve once

Our system is:
- dynamic
- recursive
- multi-node
- continuous

Conclusion: Sudoku retired. It cannot model a living mesh.

## 2. What the Vortex model gives instead
Circulating, resonant, revisitable paths. Evaluated over epochs, not single shots.
Rules become operational constraints:
- 3 = minimum diversity
- 6 = minimum cross-node flow per epoch
- 9 = full pod activation window

## 3. Core Concepts
- Node: physical/logical machine (node0, node1, node2)
- Domain: workload family (evidence, property, ops)
- Pod: node × domain
- Path: ordered list of pods
- Epoch: time window for health (e.g. day)

## 4. 3-6-9 (human version)
- 3-Resonance: critical decisions must fan out (>=3 hops + 3 nodes OR 3 domains)
- 6-Flow: >=6 cross-node edges observed per epoch to avoid stagnation
- 9-Activation: across 9 epochs every pod sends & receives at least once

## 5. Spiral patterns
A ? B ? A loops score higher (explore then return). Spiral bonus influences preference, never overrides safety.

## 6. Dead-end pods
Pods with <2 total edges used over >1 epoch are flagged (topology smell). Proposals, not auto-change.

## 7. Draft vs Active
Current state:
- Single-node (node0 only)
- Vortex = Draft Law (simulation only)
- FEATURE_VORTEX = False
Activation needs: Boardroom vote + flag flip + tagged release.

## 8. Example simulation log
```json
{
  "event_type": "VORTEX_SIMULATION",
  "path": ["node0:property", "node0:evidence", "node1:property"],
  "critical": true,
  "nodes_visited": 2,
  "domains_visited": 2,
  "hops": 3,
  "spiral_bonus": 1,
  "meets_3_resonance": false,
  "mesh_health": "UNKNOWN",
  "would_reject": true,
  "note": "Draft law only; no enforcement"
}
```

## 9. Purpose
Ambition lives in explainer; governance lives in Article 11; runtime honesty preserved until activation.
