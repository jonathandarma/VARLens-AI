from datetime import datetime
from pydantic import BaseModel, Field

class MatchSummary(BaseModel):
    id: int
    name: str
    status: str
    created_at: datetime

class AnalysisRequest(BaseModel):
    pass_frame: int | None = Field(default=None, ge=0)

class AnalysisResult(BaseModel):
    decision: str
    confidence: float
    explanation: str
    referee_explanation: str
    fan_explanation: str
    factors: list[dict]
    timeline: list[dict]
    heatmap: list[list[int]]
    tracks: list[dict]
    metadata: dict

class Analytics(BaseModel):
    matches: int
    offside_count: int
    average_confidence: float
    decisions: list[dict]
