def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_readiness(client):
    resp = client.get("/health/ready")
    assert resp.status_code == 200


def test_chat_endpoint_empty_kb(client):
    resp = client.post("/api/v1/chat", json={"query": "What is NISQ?"})
    assert resp.status_code == 200
    body = resp.json()
    assert "answer" in body
    assert "citations" in body
    assert "trace" in body


def test_chat_endpoint_rejects_empty_query(client):
    resp = client.post("/api/v1/chat", json={"query": ""})
    assert resp.status_code == 422


def test_document_ingestion_roundtrip(client):
    ingest_resp = client.post(
        "/api/v1/documents",
        json={
            "title": "Test Quantum Paper",
            "source": "unit-test",
            "content": "Qiskit is an open-source SDK for working with quantum computers "
            "at the level of pulses, circuits, and application modules. " * 10,
        },
    )
    assert ingest_resp.status_code == 200
    body = ingest_resp.json()
    assert body["num_chunks"] > 0

    chat_resp = client.post("/api/v1/chat", json={"query": "Tell me about Qiskit"})
    assert chat_resp.status_code == 200
    assert len(chat_resp.json()["citations"]) > 0
