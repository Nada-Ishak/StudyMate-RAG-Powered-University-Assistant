from io import BytesIO
from uuid import uuid4

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def process_uploaded_pdf(
    file_bytes: bytes,
    filename: str,
    embedding_model,
    collection
):
    # 1. Read PDF
    reader = PdfReader(BytesIO(file_bytes))

    pages_text = []

    for page in reader.pages:
        text = page.extract_text() or ""

        if text.strip():
            pages_text.append(text)

    full_text = "\n\n".join(pages_text)

    if not full_text.strip():
        raise ValueError(
            "Could not extract text from this PDF."
        )

    # 2. Chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = text_splitter.split_text(full_text)

    if not chunks:
        raise ValueError(
            "No usable text chunks were created."
        )

    # 3. Create unique document ID
    document_id = str(uuid4())

    # 4. Generate embeddings
    embeddings = embedding_model.encode(
        chunks,
        batch_size=16,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # 5. Store in Chroma
    ids = [
        f"upload_{document_id}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "source": filename,
            "document_id": document_id,
            "chunk_id": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return {
        "document_id": document_id,
        "filename": filename,
        "pages": len(reader.pages),
        "chunks": len(chunks)
    }