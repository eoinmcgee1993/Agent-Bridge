from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any


TASK_CLASSES = ("research", "implementation", "debugging", "review", "verification", "general")

_CLASS_HINTS: dict[str, tuple[str, ...]] = {
    "research": ("research", "investigate", "compare", "survey", "find out", "look up"),
    "implementation": ("implement", "build", "create", "add", "refactor", "feature", "code"),
    "debugging": ("debug", "fix", "bug", "broken", "failing", "error", "regression"),
    "review": ("review", "audit", "inspect", "critique", "security review"),
    "verification": ("verify", "test", "validate", "check", "prove"),
}

_CAPABILITY_HINTS: dict[str, tuple[str, ...]] = {
    "research": ("antigravity",),
    "implementation": ("grok", "kimi", "codex", "claude", "opencode", "cursor", "devin"),
    "debugging": ("grok", "kimi", "claude", "codex", "opencode", "devin"),
    "review": ("claude", "codex", "grok", "kimi"),
    "verification": ("codex", "claude", "grok", "kimi"),
}


@dataclass(frozen=True)
class RouteDecision:
    task_class: str
    selected: str | None
    score: float
    reasons: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)


def classify_task(message: str) -> str:
    text = message.lower()
    scores = {
        name: sum(1 for hint in hints if hint in text)
        for name, hints in _CLASS_HINTS.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] else "general"


def _health_score(agent: dict[str, Any]) -> float:
    if not agent.get("available"):
        return -100.0
    quota = agent.get("quota") or {}
    status = quota.get("status")
    if status == "exhausted":
        return -20.0
    if status == "ok":
        windows = quota.get("windows") or []
        remaining = [w.get("remaining_percent") for w in windows if isinstance(w, dict)]
        remaining = [float(x) for x in remaining if isinstance(x, (int, float))]
        if remaining:
            return min(10.0, max(0.0, min(remaining) / 10.0))
        return 2.0
    return 0.0


def choose_route(
    message: str,
    agents: list[dict[str, Any]],
    *,
    preferred: str | None = None,
) -> RouteDecision:
    task_class = classify_task(message)
    preferred = preferred.strip().lower() if preferred else None
    scored: list[tuple[float, str, list[str]]] = []

    for agent in agents:
        name = str(agent.get("name", "")).strip().lower()
        if not name:
            continue

        score = _health_score(agent)
        reasons: list[str] = []

        if not agent.get("available"):
            reasons.append("worker unavailable")
        else:
            reasons.append("worker available")

        if name in _CAPABILITY_HINTS.get(task_class, ()):
            score += 8.0
            reasons.append(f"matches {task_class} capability")

        if preferred and name == preferred:
            score += 100.0
            reasons.append("matches explicit user preference")

        scored.append((score, name, reasons))

    scored.sort(key=lambda item: (-item[0], item[1]))
    if not scored or scored[0][0] < -50:
        return RouteDecision(task_class, None, 0.0, ["no available worker"], [])

    winner = scored[0]
    alternatives = [name for score, name, _ in scored[1:] if score > -50]
    return RouteDecision(
        task_class=task_class,
        selected=winner[1],
        score=winner[0],
        reasons=winner[2],
        alternatives=alternatives,
    )
