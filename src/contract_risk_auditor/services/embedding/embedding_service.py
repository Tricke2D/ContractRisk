"""
Embedding service for generating and storing vectors.
"""

from contract_risk_auditor.repositories.playbook_repository import PlaybookRepository
from contract_risk_auditor.services.llm.ollama_client import OllamaClient


class EmbeddingService:
    """Generate and store embeddings for playbook standards."""

    def __init__(
        self, ollama_client: OllamaClient, playbook_repository: PlaybookRepository
    ) -> None:
        self._ollama_client = ollama_client
        self._playbook_repository = playbook_repository

    def embed_and_store_standard(self, playbook_standard_id: str, standard_language: str) -> None:
        """Generate embedding for a playbook standard and store it."""
        embedding_vector = self._ollama_client.embed_text(standard_language)
        self._playbook_repository.update_embedding(playbook_standard_id, embedding_vector)
