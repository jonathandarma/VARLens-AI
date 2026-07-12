from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import Match, get_db
from ..schemas import Analytics
router = APIRouter(prefix="/analytics", tags=["analytics"])
@router.get("", response_model=Analytics)
def analytics(db: Session = Depends(get_db)):
    results = [m.result for m in db.scalars(select(Match)).all() if m.result]
    return {"matches": len(results), "offside_count": sum(r["decision"] == "OFFSIDE" for r in results), "average_confidence": round(sum(r["confidence"] for r in results) / len(results), 2) if results else 0, "decisions": [{"decision": r["decision"], "confidence": r["confidence"]} for r in results]}
