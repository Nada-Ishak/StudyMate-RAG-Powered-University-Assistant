from ollama import chat

from backend.app.core.config import settings
from backend.app.services.retrieval import retrieve_documents


def build_context(retrieved_docs):
    context_parts = []

    for i, doc in enumerate(retrieved_docs, start=1):
        context_parts.append(
            f"[Source {i}: {doc['source']} | "
            f"Chunk {doc['chunk_id']}]\n"
            f"{doc['text']}"
        )

    return "\n\n".join(context_parts)


def generate_answer(
    question: str,
    embedding_model,
    collection,
    k: int = 3,
    document_id: str | None = None
):
    retrieved_docs = retrieve_documents(
        question=question,
        embedding_model=embedding_model,
        collection=collection,
        k=k,
        document_id=document_id
    )

    # No relevant documents found
    if not retrieved_docs:
        return (
            "I couldn't find this information in the provided "
            "course materials.",
            []
        )

    context = build_context(retrieved_docs)

    prompt = f"""
You are StudyMate, a university study assistant.

Answer the student's question using ONLY the provided course material.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not available in the provided context, say:
"I couldn't find this information in the provided course materials."
4. Keep the answer clear and educational.
5. At the end, list the sources used.

COURSE MATERIAL:
{context}

STUDENT QUESTION:
{question}
"""

    response = chat(
        model=settings.llm_model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    sources = list(
        dict.fromkeys(
            doc["source"]
            for doc in retrieved_docs
        )
    )

    return answer, sources