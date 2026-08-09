"""
FastAPI application entry point.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Contract Risk Auditor API",
    version="0.1.0",
    description="AI-powered contract risk analysis",
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "contract-risk-auditor"}