"""
Ollama API client wrapper with retry logic, timeout handling, and critique support.
"""

import json
import time

import httpx

from contract_risk_auditor.core.config import settings


class OllamaClient:
    """Wrapper for Ollama REST API with retry and timeout handling."""

    def __init__(self, base_url: str = settings.ollama_base_url) -> None:
        self._base_url = base_url
        self._http = httpx.Client(base_url=base_url, timeout=300.0)

    def classify_clause_type(self, clause_text: str) -> str:
        """Classify clause type using LLM with retry logic."""
        allowed_types = [
            "limitation_of_liability",
            "indemnification",
            "termination",
            "auto_renewal",
            "confidentiality",
            "governing_law",
            "payment_terms",
            "warranty",
            "intellectual_property",
            "other",
        ]

        prompt = (
            "Kamu adalah legal analyst. Klasifikasikan klausul kontrak "
            "berikut ke SATU kategori dari daftar ini SAJA: "
            f"{allowed_types}.\n\n"
            f"Klausul:\n{clause_text}\n\n"
            "Jawab HANYA dengan nama kategori, tanpa penjelasan apapun."
        )

        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"  🔄 Classifying (attempt {attempt + 1}/{max_retries})...")
                response = self._chat(prompt)
                classified = response.strip().lower()

                if classified in allowed_types:
                    return classified
                return "other"

            except httpx.ReadTimeout as e:
                print(f"  ⏰ Timeout attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10
                    print(f"  💤 Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"  ❌ All {max_retries} attempts failed")
                    return "other"

            except Exception as e:
                print(f"  ❌ Error: {e}")
                return "other"

        return "other"

    def get_semantic_boundaries(self, raw_text: str) -> list[dict]:
        """Get semantic boundaries using LLM fallback."""
        prompt = (
            "Pecah teks kontrak berikut menjadi klausul-klausul individual "
            "berdasarkan pergantian topik. Kembalikan HANYA JSON array, "
            'format: [{"section_number": null, "clause_text": "..."}]. '
            "Jangan tambahkan teks lain di luar JSON.\n\n"
            f"Teks:\n{raw_text}"
        )

        response = self._chat(prompt)
        return json.loads(response)

    def embed_text(self, text: str) -> list[float]:
        """Generate embedding vector for text."""
        response = self._http.post(
            "/api/embeddings",
            json={"model": settings.ollama_embedding_model, "prompt": text},
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def chat(self, prompt: str, max_retries: int = 3) -> str:
        """General chat completion with retry."""
        for attempt in range(max_retries):
            try:
                print(f"  💬 Chat attempt {attempt + 1}/{max_retries}...")
                return self._chat(prompt)
            except httpx.ReadTimeout as e:
                print(f"  ⏰ Timeout attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10
                    print(f"  💤 Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"  ❌ All {max_retries} chat attempts failed")
                    raise
            except Exception as e:
                print(f"  ❌ Chat error: {e}")
                if attempt < max_retries - 1:
                    wait_time = 5
                    time.sleep(wait_time)
                else:
                    raise
        return ""

    def judge_risk_level(self, clause_text: str, standard_language: str, max_retries: int = 3) -> dict:
        """LLM fallback for risk judgment when no rule matches."""
        max_len = 500
        clause_preview = clause_text[:max_len] + ("..." if len(clause_text) > max_len else "")
        standard_preview = standard_language[:max_len] + ("..." if len(standard_language) > max_len else "")

        prompt = f"""Kamu adalah legal risk analyst. Nilai tingkat risiko
KLAUSUL KONTRAK berikut dibandingkan STANDAR PERUSAHAAN.

STANDAR PERUSAHAAN:
{standard_preview}

KLAUSUL KONTRAK:
{clause_preview}

Kembalikan HANYA JSON:
{{"risk_level": "LOW"|"MEDIUM"|"HIGH", "confidence": 0.0-1.0, "reasoning": "alasan"}}"""

        for attempt in range(max_retries):
            try:
                print(f"  ⚖️ Risk judgment attempt {attempt + 1}/{max_retries}...")
                response = self._chat(prompt)
                cleaned = response.strip().removeprefix("```json").removesuffix("```").strip()
                result = json.loads(cleaned)

                if "risk_level" in result and "confidence" in result and "reasoning" in result:
                    return result
                else:
                    print(f"  ⚠️ Invalid response format, retrying...")
                    if attempt < max_retries - 1:
                        time.sleep(3)
                        continue
                    return {"risk_level": "MEDIUM", "confidence": 0.5, "reasoning": "Failed to get valid judgment"}

            except httpx.ReadTimeout as e:
                print(f"  ⏰ Timeout attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10
                    print(f"  💤 Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"  ❌ All {max_retries} risk judgment attempts failed")
                    return {"risk_level": "MEDIUM", "confidence": 0.4, "reasoning": "Timeout - perlu review manual"}

            except Exception as e:
                print(f"  ❌ Risk judgment error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    return {"risk_level": "MEDIUM", "confidence": 0.4, "reasoning": f"Error: {str(e)[:50]}"}

        return {"risk_level": "MEDIUM", "confidence": 0.4, "reasoning": "Failed after retries"}

    def critique_redline(self, suggested_replacement_text: str, rationale: str, standard_language: str) -> dict:
        """
        Critique redline quality as independent reviewer.

        Args:
            suggested_replacement_text: The proposed redline text
            rationale: The rationale for the redline
            standard_language: The playbook standard language

        Returns:
            Dict with passes_all_criteria, failed_criteria, and notes
        """
        prompt = f"""Kamu legal reviewer independen. Nilai REDLINE berikut terhadap 4 kriteria:
(1) tidak lebih ekstrem dari standar perusahaan,
(2) tidak menghapus hak counterparty yang wajar,
(3) bahasa tetap format legal formal,
(4) rationale konsisten dengan isi redline.

STANDAR PERUSAHAAN:
{standard_language}

REDLINE:
{suggested_replacement_text}

RATIONALE:
{rationale}

Kembalikan HANYA JSON:
{{"passes_all_criteria": true/false, "failed_criteria": ["..."], "notes": "..."}}"""

        try:
            response = self._chat(prompt)
            cleaned = response.strip().removeprefix("```json").removesuffix("```").strip()
            return json.loads(cleaned)
        except Exception as e:
            print(f"  ❌ Critique error: {e}")
            return {
                "passes_all_criteria": False,
                "failed_criteria": ["critique_failed"],
                "notes": f"Critique failed: {str(e)[:100]}",
            }

    def _chat(self, prompt: str) -> str:
        """Internal chat completion helper."""
        try:
            response = self._http.post(
                "/api/generate",
                json={
                    "model": settings.ollama_chat_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 150,
                        "temperature": 0.1,
                        "top_p": 0.9,
                    },
                },
                timeout=120.0,
            )
            response.raise_for_status()
            return response.json()["response"]
        except httpx.ReadTimeout:
            raise
        except httpx.HTTPStatusError as e:
            print(f"  ❌ HTTP error: {e.response.status_code}")
            if e.response.status_code == 404:
                print(f"  ❌ Model '{settings.ollama_chat_model}' not found. Pull it first.")
            raise
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            raise