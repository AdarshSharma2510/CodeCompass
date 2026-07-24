from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ingestion.pipeline import RepositoryIngestionPipeline

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)

UPLOAD_PATH = Path("data/upload.zip")


@router.post("/upload")
async def upload_repository(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Only ZIP files are supported.",
        )

    UPLOAD_PATH.parent.mkdir(parents=True, exist_ok=True)

    with UPLOAD_PATH.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pipeline = RepositoryIngestionPipeline()

    try:
        pipeline.ingest(UPLOAD_PATH)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    finally:
        UPLOAD_PATH.unlink(missing_ok=True)

    return {
        "message": "Repository indexed successfully."
    }
    