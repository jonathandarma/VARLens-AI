from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import init_db
from .routers import analytics, matches

app = FastAPI(title="VARLens AI API", version="1.0.0", description="Explainable football video decision support.")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.api_cors_origins.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(matches.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
@app.on_event("startup")
def startup(): init_db()
@app.get("/health")
def health(): return {"status": "ok", "service": "varlens-ai"}
