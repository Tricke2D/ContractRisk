"""
Report aggregation endpoint for UI.
"""

from fastapi import APIRouter, HTTPException

from contract_risk_auditor.core.database import get_session
from contract_risk_auditor.repositories.clause_repository import ClauseRepository
from contract_risk_auditor.repositories.clause_risk_repository import ClauseRiskRepository
from contract_risk_auditor.repositories.contract_repository import ContractRepository
from contract_risk_auditor.repositories.redline_repository import RedlineRepository

router = APIRouter(prefix="/api/v1/contracts", tags=["report"])


@router.get("/{contract_id}/report")
def get_contract_report(contract_id: str):
    """Get full report for a contract (one call for UI)."""
    with get_session() as session:
        contract_repo = ContractRepository(session)
        clause_repo = ClauseRepository(session)
        risk_repo = ClauseRiskRepository(session)
        redline_repo = RedlineRepository(session)

        contract = contract_repo.get_contract(contract_id)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        clauses = clause_repo.get_clauses_by_contract(contract_id)

        result = {
            "contract": {
                "id": str(contract.id),
                "filename": contract.filename,
                "party_name": contract.party_name,
            },
            "clauses": [],
        }

        for clause in clauses:
            risks = risk_repo.get_risks_by_clause(str(clause.id))
            risk = risks[0] if risks else None
            redlines = redline_repo.get_by_clause(str(clause.id))

            result["clauses"].append(
                {
                    "id": str(clause.id),
                    "section_number": clause.section_number,
                    "clause_text": clause.clause_text,
                    "clause_type": clause.clause_type,
                    "page_number": clause.page_number,
                    "risk": {
                        "risk_level": risk.risk_level,
                        "needs_review": risk.needs_review,
                        "deviation_reason": risk.deviation_reason,
                        "confidence_score": float(risk.confidence_score)
                        if risk.confidence_score
                        else None,
                    }
                    if risk
                    else None,
                    "redlines": [
                        {
                            "id": str(r.id),
                            "variant_label": r.variant_label,
                            "suggested_replacement_text": r.suggested_replacement_text,
                            "rationale": r.rationale,
                            "status": r.status,
                        }
                        for r in redlines
                    ],
                }
            )

        return result


@router.get("/{contract_id}/summary")
def get_contract_summary(contract_id: str):
    """Get summary statistics for a contract."""
    with get_session() as session:
        risk_repo = ClauseRiskRepository(session)
        clause_repo = ClauseRepository(session)

        clauses = clause_repo.get_clauses_by_contract(contract_id)
        total_clauses = len(clauses)

        # Get risk statistics
        high_risks = []
        needs_review = []

        for clause in clauses:
            risks = risk_repo.get_risks_by_clause(str(clause.id))
            if risks:
                risk = risks[0]
                if risk.risk_level == "HIGH":
                    high_risks.append(str(clause.id))
                if risk.needs_review:
                    needs_review.append(str(clause.id))

        return {
            "contract_id": contract_id,
            "total_clauses": total_clauses,
            "high_risk_clauses": len(high_risks),
            "needs_review_clauses": len(needs_review),
            "clause_types": list(set(c.clause_type for c in clauses if c.clause_type)),
        }
