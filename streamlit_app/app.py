import os

import httpx
import streamlit as st

API_BASE_URL = os.environ.get("STREAMLIT_API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Quantum RAG Chatbot", page_icon="⚛️", layout="wide")
st.title("⚛️ Quantum RAG Chatbot")
st.caption("Multi-agent retrieval-augmented generation with a quantum swap-test re-ranker")

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("Ingest a document")
    pdf_file = st.file_uploader("PDF file", type=["pdf"])
    title = st.text_input("Title")
    source = st.text_input("Source (URL / citation)")
    content = st.text_area("Content", height=200)
    if st.button("Ingest") and title and content:
        resp = httpx.post(
            f"{API_BASE_URL}/api/v1/documents",
            json={"title": title, "source": source, "content": content},
            timeout=60,
        )
        if resp.status_code == 200:
            st.success(f"Ingested {resp.json()['num_chunks']} chunks")
        else:
            st.error(resp.text)
    if st.button("Ingest PDF") and pdf_file is not None:
        try:
            resp = httpx.post(
                f"{API_BASE_URL}/api/v1/documents/pdf",
                files={"file": (pdf_file.name, pdf_file.getvalue(), "application/pdf")},
                data={"title": title or pdf_file.name, "source": source or pdf_file.name},
                timeout=120,
            )
            resp.raise_for_status()
            st.success(f"Ingested {resp.json()['num_chunks']} PDF chunks")
        except httpx.HTTPError as exc:
            st.error(f"PDF ingestion failed: {exc}")

for role, message in st.session_state.history:
    with st.chat_message(role):
        st.markdown(message)

query = st.chat_input("Ask about quantum computing research...")
if query:
    st.session_state.history.append(("user", query))
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Running planner → retriever → quantum re-ranker → analyzer → citation → business..."):
            try:
                resp = httpx.post(
                    f"{API_BASE_URL}/api/v1/chat", json={"query": query}, timeout=120
                )
                resp.raise_for_status()
                data = resp.json()
                answer = data["answer"]
                st.markdown(answer)
                if data["citations"]:
                    st.subheader("Sources")
                    for citation in data["citations"]:
                        page = f", page {citation['page_number']}" if citation.get("page_number") else ""
                        source = citation.get("source") or ""
                        st.markdown(f"{citation['marker']} **{citation['title']}**{page}  \n{source}")
                with st.expander("Business summary"):
                    st.markdown(data["business_summary"])
                with st.expander("Agent trace"):
                    st.json(data["trace"])
                st.session_state.history.append(("assistant", answer))
            except Exception as exc:  # noqa: BLE001
                st.error(f"Request failed: {exc}")
