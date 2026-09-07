"""Business agent: translates technical findings into an executive summary."""

from app.workflow.state import AgentState


class BusinessAgent:
    def run(self, state: AgentState) -> AgentState:
        return summarize_for_business(state)

_IMPACT_KEYWORDS = {
    "cost": "cost reduction",
    "risk": "risk mitigation",
    "security": "cryptographic security posture",
    "optimization": "operational optimization",
    "roi": "return on investment",
}


def summarize_for_business(state: AgentState) -> AgentState:
    analysis = state.get("analysis", "")
    lower = analysis.lower()

    impacts = [label for keyword, label in _IMPACT_KEYWORDS.items() if keyword in lower]
    if not impacts:
        impacts = ["strategic technology positioning"]

    num_sources = len(state.get("citations", []))
    summary = (
        f"Executive summary: Based on {num_sources} peer-reviewed/technical source(s), "
        f"the key business implications relate to {', '.join(impacts)}. "
        "Recommended next step: validate findings against a proof-of-concept before "
        "committing production budget to quantum-accelerated workflows."
    )

    state["business_summary"] = summary
    state.setdefault("trace", []).append({"agent": "business", "impacts": impacts})
    return state
