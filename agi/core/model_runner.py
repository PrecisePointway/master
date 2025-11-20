# agi/core/model_runner.py
"""Unified model runner for Sovereign model wrapper with sensitivity and provider override logic."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Literal, Tuple
import requests
import yaml

ROOT_DIR = Path(__file__).resolve().parent
STACK_PATH = ROOT_DIR / "model_stack.yaml"
_StackCache: Dict[str, Any] | None = None

Sensitivity = Literal["normal", "high"]

class ModelRunnerError(Exception):
    pass

def load_model_stack() -> Dict[str, Any]:
    global _StackCache
    if _StackCache is None:
        if not STACK_PATH.exists():
            raise ModelRunnerError(f"model_stack.yaml not found at {STACK_PATH}")
        with STACK_PATH.open("r", encoding="utf-8") as f:
            _StackCache = yaml.safe_load(f) or {}
    return _StackCache

def resolve_model_key(task_type: str, sensitivity: Sensitivity) -> Tuple[str, Dict[str, Any]]:
    stack = load_model_stack()
    routing = stack.get("routing_rules", {})
    default_key = routing.get("default", "local_small")
    key = routing.get("by_task_type", {}).get(task_type, default_key)
    if sensitivity == "high":
        ov = routing.get("overrides", {}).get("high_sensitivity", {})
        if not ov.get("allow_remote", True):
            # if chosen key is remote_tier -> replace with fallback
            if key == "remote_tier":
                key = ov.get("fallback", default_key)
    models = stack.get("models", {})
    cfg = models.get(key)
    if not cfg:
        raise ModelRunnerError(f"Model key '{key}' not defined for task '{task_type}'")
    return key, cfg

def call_ollama(model_id: str, prompt: str, **kwargs: Any) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {"model": model_id, "prompt": prompt, "stream": False}
    payload.update(kwargs)
    try:
        resp = requests.post(url, json=payload, timeout=90)
    except Exception as e:
        raise ModelRunnerError(f"Ollama request failed: {e}") from e
    if resp.status_code != 200:
        raise ModelRunnerError(f"Ollama HTTP {resp.status_code}: {resp.text}")
    data = resp.json()
    return (data.get("response") or data.get("output") or "").strip()

def call_cloud_stub(model_id: str, prompt: str) -> str:
    # Placeholder: replace with real cloud provider integration
    return f"[REMOTE_STUB:{model_id}] {prompt[:180]}"

def run_model_for_task(task_type: str, prompt: str, sensitivity: Sensitivity = "normal") -> Dict[str, Any]:
    key, cfg = resolve_model_key(task_type, sensitivity)
    provider = cfg.get("provider", "ollama")
    model_id = cfg.get("id")
    if provider == "ollama":
        text = call_ollama(model_id=model_id, prompt=prompt)
    elif provider == "cloud-llm":
        text = call_cloud_stub(model_id=model_id, prompt=prompt)
    else:
        raise ModelRunnerError(f"Unsupported provider '{provider}'")
    return {
        "model_key": key,
        "model_id": model_id,
        "provider": provider,
        "text": text,
        "sensitivity": sensitivity,
    }

if __name__ == "__main__":
    out = run_model_for_task("governance", "Test governance prompt", sensitivity="high")
    print(out)
