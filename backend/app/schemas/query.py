from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    document_id: str | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]