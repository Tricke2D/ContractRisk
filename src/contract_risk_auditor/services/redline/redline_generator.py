"""
Redline generator with multi-variant support.
"""

import json
from dataclasses import dataclass

from contract_risk_auditor.services.llm.ollama_client import OllamaClient

_VARIANT_STANCE = {
    "conservative": "perubahan seminimal mungkin yang tetap menghilangkan risiko utama, "
    "realistis untuk langsung disetujui counterparty tanpa negosiasi panjang",
    "assertive": "selaras penuh dengan STANDAR PERUSAHAAN, memaksimalkan posisi perusahaan "
    "meskipun kemungkinan perlu negosiasi lebih lanjut",
}


@dataclass
class RedlineResult:
    variant_label: str
    suggested_replacement_text: str
    rationale: str


def generate_redline_variants(
    clause_text: str,
    standard_language: str,
    deviation_reason: str,
    ollama_client: OllamaClient,
    extra_instruction: str | None = None,
) -> list[RedlineResult]:
    """Generate multiple redline variants."""
    results = []
    for variant_label, stance_description in _VARIANT_STANCE.items():
        result = _generate_single_variant(
            clause_text,
            standard_language,
            deviation_reason,
            variant_label,
            stance_description,
            ollama_client,
            extra_instruction,
        )
        if result:
            results.append(result)
    return results


def _generate_single_variant(
    clause_text: str,
    standard_language: str,
    deviation_reason: str,
    variant_label: str,
    stance_description: str,
    ollama_client: OllamaClient,
    extra_instruction: str | None,
) -> RedlineResult | None:
    """Generate one redline variant."""
    instruction_block = f"\nCATATAN TAMBAHAN: {extra_instruction}" if extra_instruction else ""

    prompt = f"""Kamu legal counsel menyusun counter-proposal klausul kontrak.
Posisi negosiasi: {stance_description}

STANDAR PERUSAHAAN:
{standard_language}

DEVIASI:
{deviation_reason}

KLAUSUL ASLI:
{clause_text}
{instruction_block}

Kembalikan HANYA JSON: {{"suggested_replacement_text": "...", "rationale": "..."}}"""

    try:
        response = ollama_client.chat(prompt)
        cleaned = response.strip().removeprefix("```json").removesuffix("```").strip()
        parsed = json.loads(cleaned)
        return RedlineResult(
            variant_label=variant_label,
            suggested_replacement_text=parsed["suggested_replacement_text"],
            rationale=parsed["rationale"],
        )
    except Exception as e:
        print(f"❌ Failed to generate {variant_label}: {e}")
        return None
