"""
Clause splitter using regex and LLM fallback.
"""

from dataclasses import dataclass

from contract_risk_auditor.services.llm.ollama_client import OllamaClient
from contract_risk_auditor.services.segmentation.section_parser import (
    find_section_boundaries,
    has_reliable_numbering,
)


@dataclass
class SegmentedClause:
    """One segmented clause ready for storage."""

    section_number: str | None
    clause_text: str
    page_number: int | None


def split_into_clauses(
    raw_text: str,
    page_number: int | None,
    ollama_client: OllamaClient,
) -> list[SegmentedClause]:
    """Split raw text into clauses using hybrid approach."""
    boundaries = find_section_boundaries(raw_text)

    if has_reliable_numbering(boundaries):
        return _split_by_boundaries(raw_text, boundaries, page_number)

    return _split_by_llm_semantic_boundary(raw_text, page_number, ollama_client)


def _split_by_boundaries(
    raw_text: str,
    boundaries: list,
    page_number: int | None,
) -> list[SegmentedClause]:
    """Split using regex boundaries."""
    clauses: list[SegmentedClause] = []

    for i, boundary in enumerate(boundaries):
        end_index = boundaries[i + 1].start_index if i + 1 < len(boundaries) else len(raw_text)
        clause_text = raw_text[boundary.start_index : end_index].strip()

        clauses.append(
            SegmentedClause(
                section_number=boundary.section_number,
                clause_text=clause_text,
                page_number=page_number,
            )
        )

    return clauses


def _split_by_llm_semantic_boundary(
    raw_text: str,
    page_number: int | None,
    ollama_client: OllamaClient,
) -> list[SegmentedClause]:
    """Split using LLM semantic boundaries (fallback)."""
    boundaries_json = ollama_client.get_semantic_boundaries(raw_text)

    clauses: list[SegmentedClause] = []
    for item in boundaries_json:
        clauses.append(
            SegmentedClause(
                section_number=item.get("section_number"),
                clause_text=item["clause_text"].strip(),
                page_number=page_number,
            )
        )

    return clauses
