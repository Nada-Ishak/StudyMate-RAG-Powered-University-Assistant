import requests
import streamlit as st

from api_client import (
    ask_studymate,
    summarize_document,
    upload_pdf
)


st.set_page_config(
    page_title="StudyMate",
    page_icon="🎓",
    layout="centered"
)


st.title("🎓 StudyMate")
st.subheader("RAG-Powered University Assistant")

st.write(
    "Upload a course PDF, generate a summary, "
    "or ask questions grounded in your study material."
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "document_id" not in st.session_state:
    st.session_state.document_id = None

if "filename" not in st.session_state:
    st.session_state.filename = None

if "summary" not in st.session_state:
    st.session_state.summary = None


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

st.markdown("## 📄 Upload Course PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


if uploaded_file is not None:

    if st.button("Upload PDF", type="primary"):

        with st.spinner(
            "Processing PDF and creating embeddings..."
        ):
            try:

                result = upload_pdf(uploaded_file)

                st.session_state.document_id = (
                    result["document_id"]
                )

                st.session_state.filename = (
                    result["filename"]
                )

                st.session_state.summary = None

                st.success(
                    "PDF uploaded and indexed successfully!"
                )

                st.info(
                    f"📄 {result['filename']}  |  "
                    f"📑 {result['pages']} pages  |  "
                    f"🧩 {result['chunks']} chunks"
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Could not connect to backend: {e}"
                )

            except Exception as e:

                st.error(
                    f"Upload failed: {e}"
                )


# --------------------------------------------------
# Current Document
# --------------------------------------------------

if st.session_state.document_id:

    st.divider()

    st.markdown("## 📚 Current Document")

    st.success(
        f"📄 {st.session_state.filename}"
    )


    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    st.markdown("## 📝 Generate Summary")

    if st.button("Generate Summary"):

        with st.spinner(
            "Generating summary... This may take a while."
        ):

            try:

                result = summarize_document(
                    st.session_state.document_id
                )

                st.session_state.summary = (
                    result["summary"]
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Could not connect to backend: {e}"
                )

            except Exception as e:

                st.error(
                    f"Summary generation failed: {e}"
                )


    if st.session_state.summary:

        st.markdown("### 📖 Study Summary")

        st.markdown(
            st.session_state.summary
        )


    # --------------------------------------------------
    # Ask Questions
    # --------------------------------------------------

    st.divider()

    st.markdown("## 💬 Ask StudyMate")

    question = st.text_area(
        "Ask a question about this PDF:",
        placeholder=(
            "Example: What is linear regression?"
        ),
        height=100
    )


    if st.button("Ask StudyMate"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching the course material..."
            ):

                try:

                    result = ask_studymate(
                        question,
                        st.session_state.document_id
                    )

                    st.markdown("### 💡 Answer")

                    st.write(
                        result["answer"]
                    )

                    st.markdown("### 📚 Sources")

                    for source in result["sources"]:

                        st.write(
                            f"- {source}"
                        )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Could not connect to backend: {e}"
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )