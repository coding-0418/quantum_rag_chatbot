from app.agents.analyzer import analyze
from app.agents.business import summarize_for_business
from app.agents.citation import cite
from app.agents.planner import plan
from app.workflow.state import AgentState


def test_planner_generates_subqueries():
    state: AgentState = {"query": "How does NISQ affect error correction?"}
    result = plan(state)
    assert len(result["sub_queries"]) >= 1
    assert result["query"] in result["sub_queries"][0]
    assert "plan" in result


def test_analyzer_handles_empty_chunks():
    state: AgentState = {"query": "test", "reranked_chunks": []}
    result = analyze(state)
    assert "No supporting evidence" in result["analysis"]


def test_citation_produces_markers():
    state: AgentState = {
        "query": "test",
        "analysis": "Some analysis text.",
        "reranked_chunks": [
            {
                "chunk_id": "doc1:0",
                "content": "content",
                "metadata": {"title": "Paper A", "source": "src"},
                "classical_score": 0.9,
                "quantum_score": 0.8,
                "final_score": 0.85,
            }
        ],
    }
    result = cite(state)
    assert len(result["citations"]) == 1
    assert result["citations"][0]["marker"] == "[1]"
    assert "[1]" in result["final_answer"]


def test_business_agent_produces_summary():
    state: AgentState = {
        "query": "test",
        "analysis": "This affects cost and security considerations.",
        "citations": [{"marker": "[1]"}],
    }
    result = summarize_for_business(state)
    assert "Executive summary" in result["business_summary"]
