"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers langsung (sudah berupa APIRouter objects)
from contract_risk_auditor.api.v1.routers.contracts_router import router as contracts_router
from contract_risk_auditor.api.v1.routers.redlines_router import router as redlines_router
from contract_risk_auditor.api.v1.routers.report_router import router as report_router

app = FastAPI(
    title="Contract Risk Auditor API",
    version="0.1.0",
    description="AI-powered contract risk analysis",
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(contracts_router)
app.include_router(redlines_router)
app.include_router(report_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "contract-risk-auditor"}
