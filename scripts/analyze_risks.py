"""
Analyze risks for all clauses in a contract.
"""

import sys

from contract_risk_auditor.core.database import get_session
from contract_risk_auditor.repositories.clause_repository import ClauseRepository
from contract_risk_auditor.repositories.clause_risk_repository import ClauseRiskRepository
from contract_risk_auditor.repositories.playbook_repository import PlaybookRepository
from contract_risk_auditor.services.deviation.deviation_analyzer import analyze_deviation
from contract_risk_auditor.services.llm.ollama_client import OllamaClient
from contract_risk_auditor.services.risk_scoring.risk_scorer import score_clause_risk


def main(contract_id: str) -> None:
    """Analyze risks for all clauses in a contract."""
    print(f"📊 Analyzing risks for contract: {contract_id}")

    ollama_client = OllamaClient()

    with get_session() as session:
        clause_repository = ClauseRepository(session)
        playbook_repository = PlaybookRepository(session)
        clause_risk_repository = ClauseRiskRepository(session)

        clauses = clause_repository.get_clauses_by_contract(contract_id)
        risk_counter = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

        for clause in clauses:
            print(f"  🔍 Analyzing clause {clause.section_number or '?'}...")

            # Find matching playbook standard
            clause_embedding = ollama_client.embed_text(clause.clause_text)
            candidates = playbook_repository.find_most_similar_standard(
                clause_type=clause.clause_type or "other",
                clause_embedding=clause_embedding,
            )
            if not candidates:
                print(f"    ⚠️ No playbook standard for type: {clause.clause_type}")
                continue

            matched_standard = candidates[0]

            # Deviation analysis
            deviation = analyze_deviation(
                clause.clause_text,
                matched_standard.standard_language,
                ollama_client,
            )

            # Risk scoring
            risk_result = score_clause_risk(
                clause_type=clause.clause_type or "other",
                clause_text=clause.clause_text,
                standard_language=matched_standard.standard_language,
                risk_thresholds=matched_standard.risk_thresholds,
                ollama_client=ollama_client,
            )

            # Save to database
            clause_risk_repository.create_clause_risk(
                clause_id=str(clause.id),
                matched_playbook_standard_id=str(matched_standard.id),
                risk_level=risk_result.risk_level,
                deviation_reason=deviation.deviation_summary,
                confidence_score=risk_result.confidence,
                scored_by=risk_result.scored_by,
                needs_review=risk_result.needs_review,
            )

            risk_counter[risk_result.risk_level] += 1
            review_flag = " [PERLU REVIEW]" if risk_result.needs_review else ""
            print(
                f"    ✅ {risk_result.risk_level} ({risk_result.scored_by}, conf={risk_result.confidence:.2f}){review_flag}"
            )

        print("\n📊 SUMMARY:")
        print(f"  LOW: {risk_counter['LOW']}")
        print(f"  MEDIUM: {risk_counter['MEDIUM']}")
        print(f"  HIGH: {risk_counter['HIGH']}")
        print(f"  Total: {sum(risk_counter.values())}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/analyze_risks.py <contract_id>")
        print("Example: python scripts/analyze_risks.py xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        sys.exit(1)
    main(sys.argv[1])
