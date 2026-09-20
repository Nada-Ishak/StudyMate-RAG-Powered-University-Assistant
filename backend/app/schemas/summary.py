from pydantic import BaseModel, Field


class SummaryRequest(BaseModel):
    document_id: str = Field(..., min_length=1)


class SummaryResponse(BaseModel):
    summary: str
    source: str