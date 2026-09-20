from fastapi import APIRouter, HTTPException, Request

from backend.app.schemas.summary import (
    SummaryRequest,
    SummaryResponse
)

from backend.app.services.summary_service import (
    summarize_document
)


router = APIRouter()


@router.post(
    "/summarize",
    response_model=SummaryResponse
)
def summarize(
    request: Request,
    summary_request: SummaryRequest
):
    try:
        summary, source = summarize_document(
            collection=request.app.state.collection,
            document_id=summary_request.document_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate summary: {str(e)}"
        )

    return SummaryResponse(
        summary=summary,
        source=source
    )