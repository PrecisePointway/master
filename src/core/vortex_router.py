from __future__ import annotations
from dataclasses import dataclass
from typing import List
from core.vortex_feature_flags import FEATURE_VORTEX
from core.vortex_topology import VortexTopology

@dataclass
class VortexSimulationResult:
    valid: bool
    critical: bool
    reason: str | None
    nodes_visited: int
    domains_visited: int
    hops: int
    spiral_bonus: int
    meets_3_resonance: bool
    mesh_health: str
    would_reject: bool

def _current_mesh_health() -> str:
    return "UNKNOWN"

def simulate_vortex_path(pod_path: List[str], critical: bool) -> VortexSimulationResult:
    topo = VortexTopology.from_default_config()
    if not pod_path:
        return VortexSimulationResult(False, critical, "Empty path", 0, 0, 0, 0, False, _current_mesh_health(), bool(critical))

    for pid in pod_path:
        if not topo.has_pod(pid):
            return VortexSimulationResult(False, critical, f"Unknown pod '{pid}'", 0, 0, len(pod_path), 0, False, _current_mesh_health(), bool(critical))

    hops = len(pod_path)
    nodes = {topo.node_of(p) for p in pod_path}
    domains = {topo.domain_of(p) for p in pod_path}
    spiral_bonus = sum(1 for i in range(len(pod_path)-2) if pod_path[i] == pod_path[i+2])
    meets_3_resonance = hops >= 3 and (len(nodes) >= 3 or len(domains) >= 3)
    mesh_health = _current_mesh_health()
    would_reject = bool(critical and not meets_3_resonance)

    return VortexSimulationResult(True, critical, None, len(nodes), len(domains), hops, spiral_bonus, meets_3_resonance, mesh_health, would_reject)


def enforce_vortex_constraints(pod_path: List[str], critical: bool) -> List[str]:
    if not FEATURE_VORTEX:
        return []
    result = simulate_vortex_path(pod_path, critical=critical)
    cvfs: List[str] = []
    if not result.valid and critical:
        cvfs.append("CVF.VORTEX_INVALID_PATH")
        return cvfs
    if critical and not result.meets_3_resonance:
        cvfs.append("CVF.VORTEX_INSUFFICIENT_RESONANCE")
    if result.mesh_health == "DEGRADED_VORTEX_FLOW" and critical:
        cvfs.append("CVF.VORTEX_DEGRADED_FLOW")
    return cvfs
