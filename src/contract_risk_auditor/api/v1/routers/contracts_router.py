"""
Contract upload and management API.
"""

import shutil
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from contract_risk_auditor.core.database import get_session
from contract_risk_auditor.repositories.contract_repository import ContractRepository
from contract_risk_auditor.repositories.clause_repository import ClauseRepository
from contract_risk_auditor.services.llm.ollama_client import OllamaClient
from contract_risk_auditor.services.segmentation.clause_splitter import split_into_clauses

router = APIRouter(prefix="/api/v1/contracts", tags=["contracts"])


@router.post("/upload")
async def upload_contract(
    file: UploadFile = File(...),
    party_name: str = Form(...),
):
    """Upload a contract PDF or TXT file and trigger analysis."""
    if file.filename is None:
        raise HTTPException(status_code=400, detail="No filename provided")

    data_dir = Path("data/uploads")
    data_dir.mkdir(parents=True, exist_ok=True)

    file_path = data_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        if file.filename.endswith(".txt"):
            content = file_path.read_text(encoding="utf-8")
            pages = [(1, content)]
        else:
            import pdfplumber

            pages = []
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    pages.append((page_num, page.extract_text() or ""))

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": f"Failed to read file: {str(e)}"},
        )

    with get_session() as session:
        contract_repo = ContractRepository(session)
        clause_repo = ClauseRepository(session)
        ollama_client = OllamaClient()

        contract = contract_repo.create_contract(
            filename=file.filename,
            party_name=party_name,
        )

        total_clauses = 0

        for page_number, page_text in pages:
            if not page_text.strip():
                continue

            segmented_clauses = split_into_clauses(page_text, page_number, ollama_client)

            for segmented in segmented_clauses:
                clause_type = ollama_client.classify_clause_type(segmented.clause_text)

                _ = clause_repo.create_clause(
                    contract_id=str(contract.id),
                    section_number=segmented.section_number,
                    clause_text=segmented.clause_text,
                    clause_type=clause_type,
                    page_number=segmented.page_number,
                )
                total_clauses += 1

        file_path.unlink(missing_ok=True)

        return {
            "contract_id": str(contract.id),
            "filename": file.filename,
            "party_name": party_name,
            "total_clauses": total_clauses,
            "message": "Contract uploaded and analyzed successfully",
        }