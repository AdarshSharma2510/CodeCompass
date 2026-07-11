from pathlib import Path
import shutil
from app.ingestion.pipeline import RepositoryIngestionPipeline
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ingestion.extractor import RepositoryExtractor

router = APIRouter(prefix="/repositories", tags=["Repositories"])

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

    extractor = RepositoryExtractor()

    try:
        repository_path = extractor.extract(UPLOAD_PATH)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    UPLOAD_PATH.unlink(missing_ok=True)

    return {
        "message": "Repository uploaded successfully.",
        "repository_path": str(repository_path),
    }