from langgraph.graph import END, StateGraph

from app.agents.analyzer import analyze
from app.agents.business import summarize_for_business
from app.agents.citation import cite
from app.agents.planner import plan
from app.agents.quantum_reranker import rerank
from app.agents.retriever import retrieve
from app.workflow.state import AgentState


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", plan)
    graph.add_node("retriever", retrieve)
    graph.add_node("quantum_reranker", rerank)
    graph.add_node("analyzer", analyze)
    graph.add_node("citation", cite)
    graph.add_node("business", summarize_for_business)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "retriever")
    graph.add_edge("retriever", "quantum_reranker")
    graph.add_edge("quantum_reranker", "analyzer")
    graph.add_edge("analyzer", "citation")
    graph.add_edge("citation", "business")
    graph.add_edge("business", END)

    return graph.compile()


_compiled_graph = None


def get_compiled_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


def run_query(query: str) -> AgentState:
    app_graph = get_compiled_graph()
    initial_state: AgentState = {"query": query, "trace": []}
    return app_graph.invoke(initial_state)
