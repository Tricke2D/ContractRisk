"""
Redline review workflow API.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from contract_risk_auditor.core.database import get_session
from contract_risk_auditor.repositories.redline_repository import RedlineRepository

router = APIRouter(prefix="/api/v1/redlines", tags=["redlines"])


class UpdateRedlineStatusRequest(BaseModel):
    """Payload for approve/reject redline."""

    status: str  # "APPROVED" | "REJECTED"
    reviewer_note: str | None = None


class RegenerateRedlineRequest(BaseModel):
    """Payload for regenerate with extra instruction."""

    extra_instruction: str


@router.patch("/{redline_id}/status")
def update_redline_status(
    redline_id: str,
    payload: UpdateRedlineStatusRequest,
):
    """Update redline status (APPROVED/REJECTED)."""
    if payload.status not in ["APPROVED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Status must be APPROVED or REJECTED")

    with get_session() as session:
        repo = RedlineRepository(session)
        result = repo.update_status(redline_id, payload.status, payload.reviewer_note)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result


@router.post("/{redline_id}/regenerate")
def regenerate_redline(
    redline_id: str,
    payload: RegenerateRedlineRequest,
):
    """Regenerate redline with additional instruction."""
    # TODO: Implement regeneration logic with extra_instruction
    # This will be implemented in Week 12
    return {
        "message": "Regeneration triggered",
        "redline_id": redline_id,
        "extra_instruction": payload.extra_instruction,
    }
