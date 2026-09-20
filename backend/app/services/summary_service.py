from ollama import chat

from backend.app.core.config import settings


def get_document_chunks(collection, document_id: str):
    results = collection.get(
        where={
            "document_id": document_id
        }
    )

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    chunks = []

    for document, metadata in zip(documents, metadatas):
        chunks.append({
            "text": document,
            "chunk_id": metadata["chunk_id"],
            "source": metadata["source"]
        })

    chunks.sort(key=lambda x: x["chunk_id"])

    return chunks


def summarize_chunk_group(chunks):
    combined_text = "\n\n".join(
        f"CHUNK {chunk['chunk_id']}:\n{chunk['text']}"
        for chunk in chunks
    )

    prompt = f"""
You are StudyMate, a university study assistant.

Summarize the following course material.

Rules:
1. Use ONLY the provided text.
2. Do not add outside information.
3. Keep important concepts, definitions, formulas,
   methods, and examples.
4. Remove unnecessary repetition.
5. Organize the summary using clear headings
   and bullet points.
6. Make it useful for a student studying for an exam.

COURSE MATERIAL:

{combined_text}

SUMMARY:
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

    return response["message"]["content"]


def generate_final_summary(group_summaries):
    combined = "\n\n".join(
        f"SECTION {i + 1}:\n{summary}"
        for i, summary in enumerate(group_summaries)
    )

    prompt = f"""
You are StudyMate, a university study assistant.

Create a final study summary from the section summaries below.

Rules:
1. Use ONLY the provided summaries.
2. Do not add outside information.
3. Remove repetition.
4. Organize the summary with clear headings
   and bullet points.
5. Preserve important definitions, concepts,
   formulas, methods, and examples.
6. Make it useful for exam revision.

SECTION SUMMARIES:

{combined}

FINAL STUDY SUMMARY:
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

    return response["message"]["content"]


def summarize_document(collection, document_id: str):
    chunks = get_document_chunks(
        collection,
        document_id
    )

    if not chunks:
        raise ValueError(
            "No uploaded document found with this document_id."
        )

    # Group every 5 chunks together
    chunk_groups = [
        chunks[i:i + 5]
        for i in range(0, len(chunks), 5)
    ]

    group_summaries = []

    for group in chunk_groups:
        summary = summarize_chunk_group(group)
        group_summaries.append(summary)

    final_summary = generate_final_summary(
        group_summaries
    )

    source = chunks[0]["source"]

    return final_summary, source