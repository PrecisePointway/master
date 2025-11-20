from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import yaml

VORTEX_TOPOLOGY_PATH = Path("config/topology_vortex.yaml")

@dataclass(frozen=True)
class Pod:
    id: str
    node: str
    domain: str

class VortexTopology:
    """Minimal topology view for Vortex simulation.
    Fully connected: every pod can reach every other.
    """
    def __init__(self, pods: Dict[str, Pod]):
        self._pods = pods
        self._ids: List[str] = list(pods.keys())

    @classmethod
    def from_default_config(cls) -> "VortexTopology":
        raw = yaml.safe_load(VORTEX_TOPOLOGY_PATH.read_text(encoding="utf-8"))
        pods: Dict[str, Pod] = {}
        for p in raw.get("pods", []):
            pod = Pod(id=p["id"], node=p["node"], domain=p["domain"])
            pods[pod.id] = pod
        return cls(pods=pods)

    def all_pods(self) -> List[str]:
        return list(self._ids)

    def has_pod(self, pod_id: str) -> bool:
        return pod_id in self._pods

    def node_of(self, pod_id: str) -> str:
        return self._pods[pod_id].node

    def domain_of(self, pod_id: str) -> str:
        return self._pods[pod_id].domain
