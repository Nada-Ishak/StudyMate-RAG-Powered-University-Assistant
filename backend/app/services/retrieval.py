import torch
import chromadb
from sentence_transformers import SentenceTransformer

from backend.app.core.config import settings


def load_embedding_model():
    device = (
        settings.embedding_device
        if torch.cuda.is_available()
        else "cpu"
    )

    return SentenceTransformer(
        settings.embedding_model,
        device=device
    )


def load_collection():
    client = chromadb.PersistentClient(
        path=settings.vector_store_path
    )

    return client.get_collection(
        name=settings.chroma_collection
    )


def retrieve_documents(
    question: str,
    embedding_model,
    collection,
    k: int = 3,
    document_id: str | None = None
):
    query_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True
    )[0]

    query_kwargs = {
        "query_embeddings": [query_embedding.tolist()],
        "n_results": k
    }

    # If a specific uploaded PDF is selected,
    # retrieve only from that document.
    if document_id:
        query_kwargs["where"] = {
            "document_id": document_id
        }

    results = collection.query(**query_kwargs)

    retrieved = []

    for i in range(len(results["documents"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_id": results["metadatas"][0][i]["chunk_id"],
            "distance": results["distances"][0][i]
        })

    return retrieved