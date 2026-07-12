from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..config import settings
from ..db import Match, get_db
from ..schemas import AnalysisRequest, AnalysisResult, MatchSummary
from ..services.explanations import explain
from ..services.pipeline import VideoAnalyzer

router = APIRouter(prefix="/matches", tags=["matches"])
VALID_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

@router.post("/upload", response_model=MatchSummary, status_code=201)
async def upload_match(name: str, video: UploadFile = File(...), db: Session = Depends(get_db)):
    suffix = Path(video.filename or "").suffix.lower()
    if suffix not in VALID_EXTENSIONS: raise HTTPException(415, "Upload a supported video file.")
    path = settings.upload_path / f"{uuid4()}{suffix}"
    size = 0
    with path.open("wb") as out:
        while chunk := await video.read(1024 * 1024):
            size += len(chunk)
            if size > settings.max_upload_mb * 1024 * 1024:
                path.unlink(missing_ok=True); raise HTTPException(413, "Video exceeds upload limit.")
            out.write(chunk)
    match = Match(name=name.strip() or "Untitled match", video_path=str(path))
    db.add(match); db.commit(); db.refresh(match)
    return match

@router.get("", response_model=list[MatchSummary])
def list_matches(db: Session = Depends(get_db)):
    return db.scalars(select(Match).order_by(Match.created_at.desc())).all()

@router.post("/{match_id}/analyze", response_model=AnalysisResult)
def analyze_match(match_id: int, request: AnalysisRequest, db: Session = Depends(get_db)):
    match = db.get(Match, match_id)
    if not match: raise HTTPException(404, "Match not found.")
    try: result = explain(VideoAnalyzer().analyze(match.video_path, request.pass_frame))
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc
    match.status, match.result = "analyzed", result; db.commit()
    return result

@router.get("/{match_id}", response_model=AnalysisResult)
def get_result(match_id: int, db: Session = Depends(get_db)):
    match = db.get(Match, match_id)
    if not match or not match.result: raise HTTPException(404, "Analysis not available.")
    return match.result
