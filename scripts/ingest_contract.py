"""
Ingest contract - full Phase 1 pipeline.
"""

import sys
from pathlib import Path

import pdfplumber
from contract_risk_auditor.core.database import get_session
from contract_risk_auditor.repositories import (
    ClauseRepository,
    ContractRepository,
    PlaybookRepository,
)
from contract_risk_auditor.services.llm.ollama_client import OllamaClient
from contract_risk_auditor.services.segmentation.clause_splitter import split_into_clauses


def extract_pages_text(pdf_path: Path) -> list[tuple[int, str]]:
    """Extract text from each page of PDF."""
    pages: list[tuple[int, str]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            pages.append((page_number, page.extract_text() or ""))
    return pages


def extract_text_from_file(file_path: Path) -> list[tuple[int, str]]:
    """Extract text from PDF or plain text file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() == ".pdf":
        try:
            return extract_pages_text(file_path)
        except Exception as e:
            print(f"⚠️ PDF error: {e}. Trying as text...")
            return [(1, file_path.read_text(encoding="utf-8"))]
    else:
        # Plain text file - read all as one page
        content = file_path.read_text(encoding="utf-8")
        return [(1, content)]


def main(pdf_path_str: str, party_name: str) -> None:
    """Ingest contract and run Phase 1 pipeline."""
    pdf_path = Path(pdf_path_str)
    if not pdf_path.exists():
        print(f"❌ File not found: {pdf_path}")
        return

    print(f"📄 Ingesting: {pdf_path.name}")
    print(f"🏢 Party: {party_name}")

    ollama_client = OllamaClient()

    with get_session() as session:
        contract_repository = ContractRepository(session)
        clause_repository = ClauseRepository(session)
        playbook_repository = PlaybookRepository(session)

        # Create contract
        contract = contract_repository.create_contract(
            filename=pdf_path.name,
            party_name=party_name,
        )
        print(f"✅ Contract created: {contract.id}")

        total_clauses = 0
        clause_type_counts = {}

        for page_number, page_text in extract_text_from_file(pdf_path):
            if not page_text.strip():
                continue

            segmented_clauses = split_into_clauses(page_text, page_number, ollama_client)

            for segmented in segmented_clauses:
                clause_type = ollama_client.classify_clause_type(segmented.clause_text)

                clause = clause_repository.create_clause(
                    contract_id=str(contract.id),
                    section_number=segmented.section_number,
                    clause_text=segmented.clause_text,
                    clause_type=clause_type,
                    page_number=segmented.page_number,
                )

                # Retrieval - find most similar playbook standard
                try:
                    clause_embedding = ollama_client.embed_text(clause.clause_text)
                    candidates = playbook_repository.find_most_similar_standard(
                        clause_type=clause_type,
                        clause_embedding=clause_embedding,
                    )
                    match_info = (
                        candidates[0].standard_language[:60] if candidates else "TIDAK ADA MATCH"
                    )
                    print(
                        f"  [{clause.section_number or '?'}] {clause_type} -> match: {match_info}..."
                    )
                except Exception as e:
                    print(f"  [{clause.section_number or '?'}] {clause_type} -> error: {e}")

                total_clauses += 1
                clause_type_counts[clause_type] = clause_type_counts.get(clause_type, 0) + 1

        print("\n📊 SUMMARY:")
        print(f"  Total clauses: {total_clauses}")
        print(f"  Clause types: {len(clause_type_counts)}")
        for ct, count in sorted(clause_type_counts.items(), key=lambda x: -x[1]):
            print(f"    {ct}: {count}")
        print("\n✅ Ingestion complete!")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/ingest_contract.py <file_path> <party_name>")
        print(
            "Example: python scripts/ingest_contract.py data/sample_contracts/demo_contract.txt AcmeCorp"
        )
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
