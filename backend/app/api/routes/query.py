from fastapi import APIRouter, Request

from backend.app.schemas.query import QueryRequest, QueryResponse
from backend.app.services.generation import generate_answer


router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(
    request: Request,
    query_request: QueryRequest
):
    answer, sources = generate_answer(
        question=query_request.question,
        embedding_model=request.app.state.embedding_model,
        collection=request.app.state.collection,
        document_id=query_request.document_id
    )

    return QueryResponse(
        answer=answer,
        sources=sources
    )