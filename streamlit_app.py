# streamlit_app.py

import streamlit as st
from loader import load_file
from config import OPENAI_MODEL
import streamlit as st
from pathlib import Path
import tempfile
import base64
from qa_agent import generate_summary, generate_insights, generate_mcq, answer_question, build_retrieval_index

# Page
st.set_page_config(
    page_title="Document Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Utilities 
def save_uploaded_file(uploaded_file, dst_path: Path):
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dst_path, "wb") as f:
        f.write(uploaded_file.read())
    return dst_path

def make_download_link(text: str, filename: str):
    b64 = base64.b64encode(text.encode("utf-8")).decode()
    return f"data:file/txt;base64,{b64}"

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")

    # ✅ Only valid, accessible models
    valid_models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    model = st.selectbox("Select Model", valid_models, index=0)

    temp = st.slider("Temperature", 0.0, 1.0, 0.3, 0.05)
    chunk_size = st.number_input("Document chunk size (tokens)", 256, 4096, 1024, 64)
    reindex = st.button("(Re)Build Retrieval Index")

# Header
col1, col2 = st.columns([8, 2])
with col1:
    st.title("Document Analyzer")
    st.caption("Derive insights, Create MCQs, Summarize")
with col2:
    st.image("https://static.streamlit.io/images/brand/streamlit-mark-color.png", width=72)

st.markdown("---")

# File Upload
uploaded_file = st.file_uploader("Upload PDF/CSV file", type=["pdf", "csv"], accept_multiple_files=False)

if "uploaded_path" not in st.session_state:
    st.session_state.uploaded_path = None

if uploaded_file:
    tmp = Path(tempfile.gettempdir()) / "uploaded_document"
    tmp.mkdir(parents=True, exist_ok=True)
    dst = tmp / uploaded_file.name
    save_uploaded_file(uploaded_file, dst)
    st.session_state.uploaded_path = str(dst)
    st.success(f"✅ Uploaded: {uploaded_file.name}")

# Tabs
tabs = st.tabs(["Document", "Actions", "Chat & QA", "MCQs & Downloads"])

# Document Tab
with tabs[0]:
    st.subheader("Preview Document")
    if st.session_state.uploaded_path:
        file_name = Path(st.session_state.uploaded_path).name
        size_kb = Path(st.session_state.uploaded_path).stat().st_size // 1024
        st.write(f"**File:** {file_name} ({size_kb} KB)")
        st.write(f"**Model:** {model}")
        st.write(f"**Chunk Size:** {chunk_size}")

        with st.expander("📄 Show Extracted Text Preview (first 8000 chars)"):
            try:
                with open(st.session_state.uploaded_path, "rb") as f:
                    _b = f.read()
                if file_name.endswith(".pdf"):
                    st.info("PDF text extraction will occur during indexing or summarization.")
                else:
                    st.write(_b[:2000].decode(errors="replace"))
            except Exception:
                st.error("❌ Could not preview file content.")
    else:
        st.info("Upload a PDF or CSV to begin your analysis.")

# Actions Tab
with tabs[1]:
    st.subheader("Perform Actions")
    if not st.session_state.uploaded_path:
        st.warning("Upload a file first.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Generate Summary"):
                with st.spinner("Generating summary..."):
                    summary = generate_summary(st.session_state.uploaded_path, model=model, temperature=temp)
                    st.session_state.last_summary = summary
                    st.success("Summary Ready")
                    st.write(summary)
        with c2:
            if st.button("Generate Insights"):
                with st.spinner("Generating insights..."):
                    insights = generate_insights(st.session_state.uploaded_path, model=model, chunk_size=chunk_size)
                    st.session_state.last_insights = insights
                    st.success("Insights Ready")
                    st.write(insights)
        with c3:
            if st.button("Generate MCQs"):
                with st.spinner("Generating MCQs..."):
                    mcqs = generate_mcq(st.session_state.uploaded_path, num_questions=10, model=model)
                    st.session_state.last_mcqs = mcqs
                    st.success("MCQs Ready")
                    st.write(mcqs)

        st.markdown("---")
        if reindex:
            with st.spinner("Building retrieval index..."):
                result = build_retrieval_index(st.session_state.uploaded_path, chunk_size=chunk_size)
                st.success(result)

# Chat & QA Tab
with tabs[2]:
    st.subheader("Chat with Your Document")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if not st.session_state.uploaded_path:
        st.info("Upload a file to start chatting.")
    else:
        query = st.text_input("Ask your question:")
        if st.button("Send") and query:
            with st.spinner("Thinking..."):
                ans = answer_question(st.session_state.uploaded_path, query, model=model)
                st.session_state.chat_history.append({"q": query, "a": ans})
        for turn in reversed(st.session_state.chat_history[-10:]):
            st.markdown(f"**Q:** {turn['q']}\n\n**A:** {turn['a']}")

# MCQs & Downloads
with tabs[3]:
    st.subheader("Export Your Results")
    if st.session_state.get("last_mcqs"):
        st.download_button("Download MCQs", st.session_state.last_mcqs, file_name="mcqs.txt")
    else:
        st.info("No MCQs yet. Generate them in the Actions tab.")

    if st.session_state.get("last_summary"):
        st.download_button("Download Summary", st.session_state.last_summary, file_name="summary.txt")
    if st.session_state.get("last_insights"):
        st.download_button("Download Insights", st.session_state.last_insights, file_name="insights.txt")
