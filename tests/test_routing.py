from agent_bridge.routing import choose_route, classify_task


def test_classify_task():
    assert classify_task("research competitors and compare them") == "research"
    assert classify_task("implement the authentication feature") == "implementation"
    assert classify_task("fix the failing test") == "debugging"


def test_explicit_preference_wins():
    agents = [
        {"name": "antigravity", "available": True, "quota": {"status": "ok"}},
        {"name": "grok", "available": True, "quota": {"status": "ok"}},
    ]
    decision = choose_route("implement the feature", agents, preferred="antigravity")
    assert decision.selected == "antigravity"
    assert "explicit user preference" in decision.reasons


def test_unavailable_workers_are_not_selected():
    agents = [
        {"name": "grok", "available": False, "quota": {"status": "ok"}},
        {"name": "kimi", "available": True, "quota": {"status": "ok"}},
    ]
    decision = choose_route("implement the feature", agents)
    assert decision.selected == "kimi"
