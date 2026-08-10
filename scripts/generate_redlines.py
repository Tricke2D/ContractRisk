"""
Generate redlines for HIGH risk clauses.
"""

import sys

from contract_risk_auditor.core.database import get_session
from contract_risk_auditor.repositories.clause_risk_repository import ClauseRiskRepository
from contract_risk_auditor.repositories.redline_repository import RedlineRepository
from contract_risk_auditor.services.llm.ollama_client import OllamaClient
from contract_risk_auditor.services.redline.redline_generator import generate_redline_variants


def main(contract_id: str) -> None:
    """Generate redlines for HIGH risk clauses in a contract."""
    print(f"📝 Generating redlines for contract: {contract_id}")

    ollama_client = OllamaClient()

    with get_session() as session:
        risk_repo = ClauseRiskRepository(session)
        redline_repo = RedlineRepository(session)

        high_risks = risk_repo.get_high_risk_by_contract(contract_id)

        if not high_risks:
            print("  ℹ️ No HIGH risk clauses found")
            return

        print(f"  📌 Found {len(high_risks)} HIGH risk clauses")

        for risk in high_risks:
            clause = risk.clause
            print(f"  🔍 Processing clause {clause.section_number or '?'}...")

            # Get the matched playbook standard
            matched_standard = None
            if risk.matched_playbook_standard_id:
                from contract_risk_auditor.repositories.playbook_repository import (
                    PlaybookRepository,
                )

                playbook_repo = PlaybookRepository(session)
                matched_standard = playbook_repo.get_standard(risk.matched_playbook_standard_id)

            if not matched_standard:
                print("    ⚠️ No matched playbook standard found")
                continue

            # Generate redline variants
            variants = generate_redline_variants(
                clause_text=clause.clause_text,
                standard_language=matched_standard.standard_language,
                deviation_reason=risk.deviation_reason or "No specific deviation reason",
                ollama_client=ollama_client,
            )

            for variant in variants:
                redline_repo.create_redline(
                    clause_id=str(clause.id),
                    suggested_replacement_text=variant.suggested_replacement_text,
                    rationale=variant.rationale,
                    variant_label=variant.variant_label,
                    status="DRAFT",
                )
                print(f"    ✅ Generated {variant.variant_label} variant")

        print("\n✅ Redline generation complete!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_redlines.py <contract_id>")
        sys.exit(1)
    main(sys.argv[1])
