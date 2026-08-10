"""
Seed playbook data into the database.
"""

import json
from pathlib import Path

from contract_risk_auditor.core.database import get_session
from contract_risk_auditor.repositories.playbook_repository import PlaybookRepository
from contract_risk_auditor.services.embedding.embedding_service import EmbeddingService
from contract_risk_auditor.services.llm.ollama_client import OllamaClient

SEED_FILE_PATH = Path("data/playbook_seed/standard_clauses.json")


def main() -> None:
    """Seed playbook data into database."""
    print("📚 Seeding playbook data...")

    with get_session() as session:
        playbook_repository = PlaybookRepository(session)
        ollama_client = OllamaClient()
        embedding_service = EmbeddingService(ollama_client, playbook_repository)

        if not SEED_FILE_PATH.exists():
            print(f"❌ Seed file not found: {SEED_FILE_PATH}")
            return

        seed_entries = json.loads(SEED_FILE_PATH.read_text())
        print(f"📄 Found {len(seed_entries)} entries to seed")

        for entry in seed_entries:
            print(f"  📌 Seeding: {entry['clause_type']}...")
            standard = playbook_repository.create_standard(
                clause_type=entry["clause_type"],
                standard_language=entry["standard_language"],
                risk_thresholds=entry["risk_thresholds"],
            )
            embedding_service.embed_and_store_standard(
                playbook_standard_id=str(standard.id),
                standard_language=standard.standard_language,
            )
            print(f"    ✅ {entry['clause_type']} seeded with embedding")

    print("✅ Playbook seeding complete!")


if __name__ == "__main__":
    main()
