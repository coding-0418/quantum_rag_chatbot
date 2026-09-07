"""Planner agent: decomposes a user query into retrievable sub-queries."""

from app.workflow.state import AgentState

TOPIC_KEYWORDS = {
    "nisq": ["nisq", "noisy intermediate-scale", "near-term quantum"],
    "error_correction": ["error correction", "steane", "fault-tolerant", "logical qubit"],
    "qiskit": ["qiskit", "sdk", "circuit", "transpile"],
    "business": ["business", "adoption", "roi", "industry", "use case", "enterprise"],
}


class PlannerAgent:
    def run(self, state: AgentState) -> AgentState:
        return plan(state)


def plan(state: AgentState) -> AgentState:
    query = state["query"]
    lower = query.lower()

    sub_queries = [query]
    matched_topics = [topic for topic, kws in TOPIC_KEYWORDS.items() if any(k in lower for k in kws)]

    if not matched_topics:
        matched_topics = list(TOPIC_KEYWORDS.keys())[:2]

    for topic in matched_topics:
        sub_queries.append(f"{query} ({topic.replace('_', ' ')})")

    plan_steps = [
        "decompose query into topic-scoped sub-queries",
        "retrieve candidate chunks via dense vector search",
        "quantum re-rank candidates via swap-test overlap",
        "analyze and synthesize retrieved evidence",
        "attach citations to every claim",
        "produce a business-oriented executive summary",
    ]

    state["plan"] = plan_steps
    state["sub_queries"] = list(dict.fromkeys(sub_queries))
    state.setdefault("trace", []).append({"agent": "planner", "sub_queries": state["sub_queries"]})
    return state
