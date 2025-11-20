import yaml, random
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

TOPO = yaml.safe_load(Path("config/topology_vortex.yaml").read_text())

@dataclass
class Pod:
    id: str
    node: str
    domain: str

PODS: Dict[str, Pod] = {p["id"]: Pod(**p) for p in TOPO["pods"]}
ALL = list(PODS.keys())

def neighbors(pod_id: str) -> List[str]:
    return [p for p in ALL if p != pod_id]

def validate_path(path: List[str], critical: bool = True) -> Dict:
    if not path:
        return {"valid": False, "reason": "empty"}
    if critical and len(path) < 3:
        return {"valid": False, "reason": "too short"}
    nodes = {PODS[p].node for p in path}
    domains = {PODS[p].domain for p in path}
    spiral = sum(1 for i in range(len(path)-2) if path[i] == path[i+2])
    resonance = len(nodes) + len(domains) + spiral
    valid = (not critical) or (len(path) >= 3 and (len(nodes) >= 3 or len(domains) >= 3))
    return {
        "valid": valid,
        "resonance": resonance,
        "nodes": len(nodes),
        "domains": len(domains),
        "spiral_bonus": spiral,
        "length": len(path)
    }

def random_vortex_path(start: str, length: int = 5) -> List[str]:
    if start not in PODS:
        raise ValueError(f"Unknown start pod {start}")
    path = [start]
    for _ in range(length - 1):
        path.append(random.choice(neighbors(path[-1])))
    return path

if __name__ == "__main__":
    origin = "n0_p"
    p = random_vortex_path(origin, length=5)
    print("Path:", " -> ".join(p))
    print("Check:", validate_path(p))
