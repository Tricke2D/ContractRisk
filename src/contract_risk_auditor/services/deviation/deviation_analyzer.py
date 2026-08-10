"""
Deviation analysis engine - compare clause with playbook standard.
"""

import json
from dataclasses import dataclass

from contract_risk_auditor.services.llm.ollama_client import OllamaClient


@dataclass
class DeviationResult:
    """Result of deviation analysis for one clause."""

    deviation_summary: str
    specific_differences: list[str]
    has_material_deviation: bool


def analyze_deviation(
    clause_text: str,
    standard_language: str,
    ollama_client: OllamaClient,
) -> DeviationResult:
    """Analyze deviation between clause and playbook standard."""
    prompt = _build_deviation_prompt(clause_text, standard_language)
    raw_response = ollama_client.chat(prompt)
    parsed = _parse_deviation_response(raw_response)

    return DeviationResult(
        deviation_summary=parsed.get("deviation_summary", "No deviation summary available"),
        specific_differences=parsed.get("specific_differences", []),
        has_material_deviation=parsed.get("has_material_deviation", False),
    )


def _build_deviation_prompt(clause_text: str, standard_language: str) -> str:
    """Build simpler prompt for smaller models."""
    max_len = 300
    clause_preview = clause_text[:max_len] + ("..." if len(clause_text) > max_len else "")
    standard_preview = standard_language[:max_len] + (
        "..." if len(standard_language) > max_len else ""
    )

    return f"""Compare these two legal texts. Return ONLY valid JSON.

STANDARD:
{standard_preview}

CLAUSE:
{clause_preview}

JSON format:
{{"has_material_deviation": true/false, "deviation_summary": "one sentence summary", "specific_differences": ["difference 1", "difference 2"]}}"""


def _parse_deviation_response(raw_response: str) -> dict:
    """Parse JSON response from LLM with fallback."""
    try:
        # Remove markdown code fences
        cleaned = raw_response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        # If empty, return default
        if not cleaned:
            return {
                "has_material_deviation": False,
                "deviation_summary": "No deviation detected (empty response)",
                "specific_differences": [],
            }

        return json.loads(cleaned)

    except json.JSONDecodeError as e:
        print(f"  ⚠️ JSON decode error: {e}")
        print(f"  📝 Raw response: {raw_response[:200]}...")
        return {
            "has_material_deviation": False,
            "deviation_summary": "Could not parse deviation analysis",
            "specific_differences": ["LLM response was not valid JSON"],
        }
