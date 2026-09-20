from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from backend.app.schemas.upload import UploadResponse
from backend.app.services.upload_service import process_uploaded_pdf


router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    request: Request,
    file: UploadFile = File(...)
):

    # Check file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # Read file
    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    try:
        result = process_uploaded_pdf(
            file_bytes=file_bytes,
            filename=file.filename,
            embedding_model=request.app.state.embedding_model,
            collection=request.app.state.collection
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )

    return UploadResponse(
        message="PDF uploaded and indexed successfully.",
        **result
    )