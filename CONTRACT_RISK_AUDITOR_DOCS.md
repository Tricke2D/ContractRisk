# 📄 Contract Risk Auditor
## AI-Powered Legal Contract Analysis Engine

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?logo=typescript&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-LLM-000000?logo=ollama&logoColor=white)
![pgvector](https://img.shields.io/badge/pgvector-0.7+-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

> **Sistem analisis risiko kontrak otomatis** dengan segmentasi klause, penilaian risiko hybrid, dan pembuatan redline berbasis AI—semua dalam satu platform yang siap produksi.

---

## 📋 Daftar Isi

1. [📍 Studi Kasus & Masalah](#studi-kasus--masalah)
2. [✨ Fitur Utama](#fitur-utama)
3. [🏗️ Arsitektur Sistem](#arsitektur-sistem)
4. [🛠️ Tech Stack](#tech-stack)
5. [💻 Requirements](#requirements)
6. [🚀 Instalasi & Menjalankan](#instalasi--menjalankan)
7. [📊 Risk Scoring Rubric](#risk-scoring-rubric)
8. [🔌 API Reference](#api-reference)
9. [🧪 Testing & Debugging](#testing--debugging)
10. [🐳 Docker Setup](#docker-setup)
11. [📁 Struktur Project](#struktur-project)
12. [⚠️ Batasan & Roadmap](#batasan--roadmap)
13. [🔧 Troubleshooting](#troubleshooting)
14. [📞 Kontribusi](#kontribusi)

---

## 📍 Studi Kasus & Masalah

### Konteks: Tim Legal yang Overloaded

Bayangkan tim legal Anda harus menganalisis **ratusan kontrak setiap bulan** — mencari pasal berbahaya, klausa tidak standar, dan ketidaksesuaian regulasi. Proses manual ini memakan waktu berhari-hari, rawan human error, dan menghambat negosiasi bisnis.

### ❌ Masalah yang Dipecahkan

| Masalah | Dampak |
|---------|--------|
| **Manual Review** | Legal team harus baca setiap halaman kontrak satu per satu (wasted talent!) |
| **Inconsistent Analysis** | Review yang berbeda hasilnya beda (subjective, not auditable) |
| **Missed Risks** | Klausa berbahaya terlewat karena kelelahan (liability exposure!) |
| **No Standard Comparison** | Tidak ada baseline "kontrak ideal" untuk membandingkan (no playbook) |
| **Slow Negotiation** | Feedback legal team lambat karena volume tinggi (business delay) |
| **No Redline Suggestions** | Hanya flag masalah, tidak ada solusi counter-language (wasted iteration) |
| **Knowledge Silos** | Pelajaran dari kontrak sebelumnya tidak terdokumentasi (reinventing wheel) |

### ✅ Solusi: Contract Risk Auditor

Implementasi **AI-powered contract analysis engine** dengan hybrid risk scoring (14 minggu development):

- ✅ **PDF/TXT Extraction** — Ekstrak teks dari PDF atau plain text (preserve page numbers)
- ✅ **Clause Segmentation** — Pecah kontrak jadi clause individual (regex + LLM fallback)
- ✅ **Clause Classification** — 10 kategori legal (limitation_of_liability, indemnification, dll)
- ✅ **Playbook Embedding** — Standard clause library dengan semantic search (pgvector)
- ✅ **Deviation Analysis** — Bandingkan clause vs standard, deteksi perbedaan substansi
- ✅ **Hybrid Risk Scoring** — Rule-based (deterministic) + LLM (nuanced) dengan confidence
- ✅ **Redline Generation** — Counter-language suggestions (conservative + assertive variants)
- ✅ **Review Workflow** — Approve/reject redlines dengan reviewer notes
- ✅ **Web UI** — Upload, analyze, dan review kontrak dari browser (React + Tailwind)
- ✅ **Dockerized** — One-command deployment (Postgres + Ollama + backend + frontend)

**Hasil: Legal contract analysis yang consistent, auditable, dan 10x lebih cepat daripada review manual.**

---

## ✨ Fitur Utama

### 🎯 Core Features

| Fitur | Deskripsi | Implementasi |
|-------|-----------|--------------|
| PDF/TXT Extraction | Ekstrak teks dengan page number tracking | pdfplumber + fallback PyMuPDF |
| Clause Segmentation | Pecah kontrak menjadi clause individual | Regex nested numbering + LLM fallback |
| Clause Classification | Klasifikasi ke 10 kategori legal | Ollama llama3.1:8b / phi3:mini |
| Playbook Library | Standard clause dengan embeddings | pgvector similarity search |
| Deviation Analysis | Deteksi perbedaan substansi vs standard | LLM-based structured output |
| Hybrid Risk Scoring | Rule-based + LLM fallback dengan confidence | Deterministic untuk red-flag jelas |
| Redline Generation | Counter-language draft (2 variants) | Conservative + Assertive |
| Review Workflow | Approve/Reject dengan notes | Status DRAFT/APPROVED/REJECTED |
| Quality Self-Critique | LLM checks redline quality | 4 criteria checklist |
| Web UI | Upload + analysis + review from browser | React + TypeScript + Tailwind |

### 🤖 Hybrid Risk Scoring Strategy

| Prioritas | Sumber | Kapan Dipakai | Confidence |
|-----------|--------|--------------|------------|
| 1 | Hardcoded Rule | Red-flag jelas: "unlimited liability" | 1.0 (deterministic) |
| 2 | Playbook Threshold | Notice period, cap amount, etc. | 1.0 (data-driven) |
| 3 | LLM Judgment | Nuance yang butuh konteks | 0.0–1.0 (explicit) |

**Rule-based detectors:** limitation_of_liability, auto_renewal, indemnification, termination, confidentiality

### 📊 Supported LLM Models

| Model | Ukuran | Fungsi | Status |
|-------|--------|--------|--------|
| llama3.1:8b | 4.9 GB | Classification, Deviation, Risk, Redline | ✅ Production |
| phi3:mini | 2.0 GB | Alternative (faster) | ✅ Supported |
| tinyllama | 0.6 GB | Lightweight fallback | ⚠️ Less accurate |
| nomic-embed-text | 274 MB | Embedding untuk semantic search | ✅ Production |

### 🎨 Frontend Features

- **Upload Dropzone** — Drag & drop PDF/TXT
- **Party Name Input** — Identifikasi counterparty
- **Risk Summary Cards** — LOW/MEDIUM/HIGH/Needs Review
- **Clause List** — Section number, type, risk badge
- **Deviation Reason** — Why clause is risky
- **Redline Review** — Side-by-side diff view
- **Approve/Reject** — Update status dengan notes
- **Responsive UI** — Works on desktop & tablet

---

## 🏗️ Arsitektur Sistem

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Contract Risk Auditor System                     │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     Frontend (React + TS)                    │   │
│  │                                                              │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  Upload Dropzone                                    │   │   │
│  │  │  • Drag & drop PDF/TXT                              │   │   │
│  │  │  • Party name input                                 │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  Dashboard                                          │   │   │
│  │  │  • Risk Summary (LOW/MEDIUM/HIGH/Needs Review)      │   │   │
│  │  │  • Clause list with risk badges                     │   │   │
│  │  │  • Deviation reasons                                │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  Redline Review Panel                               │   │   │
│  │  │  • Diff view (original vs suggested)                │   │   │
│  │  │  • Variant selector (conservative/assertive)        │   │   │
│  │  │  • Approve/Reject with notes                        │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  └──────────────────────────┬──────────────────────────────────┘   │
│                              │  REST API (HTTP)                    │
│                              ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     Backend (FastAPI + Python)               │   │
│  │                                                              │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  API Routers                                        │   │   │
│  │  │  • contracts_router (upload, ingest)                │   │   │
│  │  │  • report_router (aggregated report)                │   │   │
│  │  │  • redlines_router (approve/reject/regenerate)      │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  Services                                           │   │   │
│  │  │  • Clause Segmentation (regex + LLM)                │   │   │
│  │  │  • Clause Classification (LLM)                      │   │   │
│  │  │  • Deviation Analysis (LLM)                         │   │   │
│  │  │  • Risk Scoring (rule + LLM)                        │   │   │
│  │  │  • Redline Generation (LLM + self-critique)         │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  ┌─────────────────────────────────────────────────────┐   │   │
│  │  │  Repositories (SQLAlchemy)                          │   │   │
│  │  │  • Contracts, Clauses, ClauseRisks                  │   │   │
│  │  │  • PlaybookStandards (pgvector)                     │   │   │
│  │  │  • RedlineSuggestions                               │   │   │
│  │  └─────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  └──────────────────────────┬──────────────────────────────────┘   │
│                              │                                    │
│  ┌──────────────────────────▼──────────────────────────────────┐   │
│  │                     Ollama (Local LLM)                      │   │
│  │  • Llama 3.1 8B (classification, reasoning)                │   │
│  │  • nomic-embed-text (embedding for pgvector)               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                    │
│  ┌──────────────────────────▼──────────────────────────────────┐   │
│  │                     PostgreSQL (pgvector)                    │   │
│  │  • Contract metadata                                         │   │
│  │  • Clause text + classification                              │   │
│  │  • Playbook standards + embeddings                           │   │
│  │  • Risk scores + redlines                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

#### Upload & Analysis Flow

```
┌──────────────────────────────────────────────────────────────┐
│ 1. User Uploads Contract (PDF/TXT)                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Frontend → POST /contracts/upload (file + party_name)      │
│ ↓                                                            │
│ Backend: Read file → Extract text (page by page)           │
│ ↓                                                            │
│ For each page:                                              │
│   → split_into_clauses (regex + LLM fallback)              │
│   → classify_clause_type (LLM)                             │
│   → embed clause_text (nomic-embed-text)                   │
│   → find_most_similar_standard (pgvector)                  │
│   → analyze_deviation (LLM)                                │
│   → score_clause_risk (rule + LLM)                         │
│ ↓                                                            │
│ Save: Contracts → Clauses → ClauseRisks                     │
│ ↓                                                            │
│ Return: {contract_id: "..."}                                │
│ ↓                                                            │
│ Frontend → GET /contracts/{id}/report                      │
│ ↓                                                            │
│ Display: Risk Summary + Clauses + Risks                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

#### Redline Generation Flow

```
┌──────────────────────────────────────────────────────────────┐
│ 2. Redline Generation (HIGH Risk Clauses)                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Backend: For each HIGH risk clause:                         │
│   → generate_redline_variants (LLM)                        │
│   → conservative variant (minimal change)                   │
│   → assertive variant (full standard alignment)             │
│   → critique_redline (self-review as independent reviewer)  │
│   → If critique fails → retry once                         │
│   → If still fails → flag needs_review = true              │
│ ↓                                                            │
│ Save: RedlineSuggestions (variant_label, text, rationale)  │
│ ↓                                                            │
│ Frontend → GET /contracts/{id}/report                      │
│   → Display redlines in review panel                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Komponen | Teknologi | Alasan Pilihan |
|----------|-----------|----------------|
| Backend Language | Python 3.11+ | Fast development, rich AI ecosystem |
| Web Framework | FastAPI 0.111+ | Async, auto OpenAPI, type safety |
| LLM Engine | Ollama | Local, private, no API costs |
| LLM Models | llama3.1:8b, phi3:mini | Classification, reasoning, generation |
| Embedding | nomic-embed-text | Semantic search for playbook matching |
| Vector Database | pgvector 0.7+ | PostgreSQL extension, ACID compliance |
| ORM | SQLAlchemy 2.0 | Async support, migration framework |
| Validation | Pydantic v2 | Clean domain models |
| Frontend | React 18 + TypeScript | Type safety, component reusability |
| Build Tool | Vite | Fast HMR, modern bundling |
| Styling | Tailwind CSS | Utility-first, responsive |
| Containerization | Docker + Compose | Reproducible environments |
| Testing | pytest + pytest-asyncio | Async test support |
| Linting | Ruff | Fast, modern Python linter |
| Package Manager | Poetry | Deterministic dependencies |

---

## 💻 Requirements

- **Python** v3.11 atau lebih baru
- **Node.js** v18 atau lebih baru (frontend)
- **Docker** v20.x atau lebih baru (recommended)
- **RAM** 8GB+ (untuk Ollama + llama3.1:8b)
- **Git** v2.x atau lebih baru

---

## 🚀 Instalasi & Menjalankan

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Tricke2D/ContractRisk.git
cd ContractRisk
```

### 2️⃣ Setup Docker (Postgres + Ollama)

```bash
# Jalankan containers
docker compose -f docker/docker-compose.yml up -d

# Pull Ollama models (tunggu 5-10 menit)
docker exec -it cra_ollama ollama pull llama3.1:8b
docker exec -it cra_ollama ollama pull nomic-embed-text

# Verifikasi models
docker exec -it cra_ollama ollama list
# Output:
# llama3.1:8b              4.9 GB
# nomic-embed-text         274 MB
```

### 3️⃣ Backend Setup

```bash
# Install Poetry (jika belum)
pip install poetry

# Install dependencies
poetry install

# Set PYTHONPATH
export PYTHONPATH=src  # Linux/Mac
$env:PYTHONPATH = "src"  # Windows PowerShell

# Jalankan migrations
poetry run alembic -c alembic.ini upgrade head

# Seed playbook data
poetry run python scripts/seed_playbook.py

# Jalankan backend
poetry run uvicorn contract_risk_auditor.main:app --reload --port 8000
```

### 4️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Jalankan development server
npm run dev
```

### 5️⃣ Akses Aplikasi

| Service | URL | Tujuan |
|---------|-----|--------|
| Frontend | http://localhost:5173 | Main UI |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Health Check | http://localhost:8000/health | Service status |

### 6️⃣ Test Upload

```bash
# Upload sample contract
curl -X POST http://localhost:8000/api/v1/contracts/upload \
  -F "file=@data/sample_contracts/demo_contract.txt" \
  -F "party_name=Demo Corp"
```

---

## 📊 Risk Scoring Rubric

### Risk Levels

| Level | Kriteria | Confidence | Aksi |
|-------|----------|------------|------|
| **HIGH** | Red-flag explicit (unlimited liability, no notice period) | 1.0 (rule) | Immediate redline generation |
| **HIGH** | LLM confidence ≥ 0.7 + material deviation | 0.7-1.0 | Redline generation |
| **MEDIUM** | Material deviation but moderate confidence | 0.4-0.7 | Needs review |
| **LOW** | No material deviation or aligned with standard | 0.0-0.4 | No action |

### Rule-Based Detectors

| Clause Type | Red-flag | Risk Level |
|-------------|----------|------------|
| limitation_of_liability | "unlimited liability", "no cap" | HIGH |
| limitation_of_liability | Cap < 6 months fee | MEDIUM |
| auto_renewal | No notice period | HIGH |
| auto_renewal | Notice period < 30 days | MEDIUM |
| indemnification | "sole discretion", "unlimited" | HIGH |
| termination | Without notice | HIGH |
| termination | Under 30 days notice | MEDIUM |
| confidentiality | Less than 3 years | MEDIUM |

---

## 🔌 API Reference

### REST Endpoints

#### Contracts

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/v1/contracts/upload` | Upload & analyze contract |
| GET | `/api/v1/contracts/{id}/report` | Full report (one-call) |
| GET | `/api/v1/contracts/{id}/summary` | Risk summary statistics |

#### Redlines

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| PATCH | `/api/v1/redlines/{id}/status` | Approve/Reject |
| POST | `/api/v1/redlines/{id}/regenerate` | Regenerate with note |

### Example API Calls

#### Upload Contract

```bash
curl -X POST http://localhost:8000/api/v1/contracts/upload \
  -F "file=@contract.pdf" \
  -F "party_name=Acme Corp"

# Response:
{
  "contract_id": "abc-123",
  "filename": "contract.pdf",
  "party_name": "Acme Corp",
  "total_clauses": 23,
  "message": "Contract uploaded and analyzed successfully"
}
```

#### Get Report

```bash
curl http://localhost:8000/api/v1/contracts/abc-123/report | jq '.'

# Response:
{
  "contract": {
    "id": "abc-123",
    "filename": "contract.pdf",
    "party_name": "Acme Corp"
  },
  "clauses": [
    {
      "id": "def-456",
      "section_number": "2.1",
      "clause_text": "Party A shall have unlimited liability...",
      "clause_type": "limitation_of_liability",
      "page_number": 3,
      "risk": {
        "risk_level": "HIGH",
        "needs_review": false,
        "deviation_reason": "Standard cap 12 months fee, contract has no cap",
        "confidence_score": 1.0
      },
      "redlines": [
        {
          "id": "ghi-789",
          "variant_label": "conservative",
          "suggested_replacement_text": "...",
          "rationale": "...",
          "status": "DRAFT"
        }
      ]
    }
  ]
}
```

#### Approve Redline

```bash
curl -X PATCH http://localhost:8000/api/v1/redlines/ghi-789/status \
  -H "Content-Type: application/json" \
  -d '{"status": "APPROVED", "reviewer_note": "Looks good"}'
```

---

## 🧪 Testing & Debugging

### Backend Tests

```bash
# Jalankan semua unit tests
poetry run pytest tests/unit/ -v

# Integration tests
poetry run pytest tests/integration/ -v

# Specific module
poetry run pytest tests/unit/core/test_risk_scorer.py -v

# Dengan coverage report
poetry run pytest --cov=contract_risk_auditor --cov-report=html tests/
```

### Expected Test Results

| Test Module | Tests | Status |
|-------------|-------|--------|
| test_section_parser | 4 | ✅ PASSED |
| test_index | 3 | ✅ PASSED |
| test_hashing | 4 | ✅ PASSED |
| test_risk_scorer | 6 | ✅ PASSED |
| test_deviation_analyzer | 3 | ✅ PASSED |
| test_merge | 4 | ✅ PASSED |
| **Total** | **24+** | **✅ ALL PASSED** |

### Debug Commands

#### Check Database

```bash
docker exec -it cra_postgres psql -U cra_admin -d contract_risk_auditor

# Queries:
SELECT COUNT(*) FROM contracts;
SELECT COUNT(*) FROM clauses;
SELECT risk_level, COUNT(*) FROM clause_risks GROUP BY risk_level;
SELECT status, COUNT(*) FROM redline_suggestions GROUP BY status;
```

#### Test Ollama Connection

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.1:8b", "prompt": "Hello", "stream": false}'
```

---

## 🐳 Docker Setup

### Quick Start

```bash
# Jalankan semua services
docker compose -f docker/docker-compose.yml up -d

# Lihat logs
docker compose -f docker/docker-compose.yml logs -f

# Stop semua services
docker compose -f docker/docker-compose.yml down

# Reset everything (clean slate)
docker compose -f docker/docker-compose.yml down -v
docker compose -f docker/docker-compose.yml up -d
```

### Environment Variables

```bash
# .env file
DATABASE_URL=postgresql://cra_admin:change_me_locally@localhost:5432/contract_risk_auditor
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=llama3.1:8b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

### Production Docker Compose

```yaml
version: "3.9"

services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: cra_admin
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: contract_risk_auditor
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - cra_network

  ollama:
    image: ollama/ollama
    volumes:
      - ollama_data:/root/.ollama
    networks:
      - cra_network

  backend:
    build:
      context: .
      dockerfile: Dockerfile.prod
    environment:
      DATABASE_URL: postgresql://cra_admin:${POSTGRES_PASSWORD}@postgres:5432/contract_risk_auditor
      OLLAMA_BASE_URL: http://ollama:11434
    depends_on:
      - postgres
      - ollama
    networks:
      - cra_network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - cra_network

volumes:
  postgres_data:
  ollama_data:

networks:
  cra_network:
    driver: bridge
```

---

## 📁 Struktur Project

```
ContractRisk/
├── .gitignore
├── .env.example
├── README.md
├── LICENSE
├── Makefile
├── pyproject.toml
├── poetry.lock
├── alembic.ini
│
├── docker/
│   ├── docker-compose.yml
│   └── postgres/
│       └── init/
│           └── 001_bootstrap_extensions.sql
│
├── src/
│   └── contract_risk_auditor/
│       ├── __init__.py
│       ├── main.py                     # FastAPI app
│       │
│       ├── core/
│       │   ├── config.py               # Pydantic settings
│       │   ├── database.py             # SQLAlchemy engine
│       │   └── logging_config.py
│       │
│       ├── domain/
│       │   └── models/
│       │       ├── contract.py
│       │       ├── clause.py
│       │       ├── playbook_standard.py
│       │       ├── clause_risk.py
│       │       └── redline_suggestion.py
│       │
│       ├── schemas/                    # Pydantic DTOs
│       │
│       ├── services/
│       │   ├── segmentation/
│       │   │   ├── section_parser.py   # Regex numbering
│       │   │   └── clause_splitter.py  # Hybrid splitter
│       │   ├── deviation/
│       │   │   └── deviation_analyzer.py
│       │   ├── risk_scoring/
│       │   │   ├── detectors.py       # Rule-based
│       │   │   ├── rule_engine.py
│       │   │   └── risk_scorer.py     # Hybrid orchestrator
│       │   ├── redline/
│       │   │   └── redline_generator.py
│       │   └── llm/
│       │       └── ollama_client.py    # Ollama wrapper
│       │
│       ├── repositories/
│       │   ├── contract_repository.py
│       │   ├── clause_repository.py
│       │   ├── playbook_repository.py
│       │   ├── clause_risk_repository.py
│       │   └── redline_repository.py
│       │
│       ├── api/
│       │   └── v1/
│       │       ├── routers/
│       │       │   ├── contracts_router.py
│       │       │   ├── report_router.py
│       │       │   └── redlines_router.py
│       │       └── dependencies.py
│       │
│       └── migrations/
│           ├── versions/
│           │   ├── 001_initial_schema.py
│           │   ├── 002_add_risk_scoring_columns.py
│           │   └── 003_add_redline_review_workflow.py
│           └── env.py
│
├── scripts/
│   ├── seed_playbook.py               # Seed playbook data
│   ├── ingest_contract.py             # CLI ingest
│   ├── analyze_risks.py               # CLI risk analysis
│   └── generate_redlines.py           # CLI redline generation
│
├── data/
│   ├── sample_contracts/
│   │   ├── demo_contract.txt
│   │   └── risky_contract.txt
│   └── playbook_seed/
│       └── standard_clauses.json
│
├── tests/
│   ├── unit/
│   │   ├── core/
│   │   │   ├── test_section_parser.py
│   │   │   ├── test_index.py
│   │   │   ├── test_risk_scorer.py
│   │   │   └── test_deviation_analyzer.py
│   │   └── services/
│   └── integration/
│       └── test_ingest_contract.py
│
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── contractApi.ts
    │   ├── components/
    │   │   ├── ContractUpload.tsx
    │   │   └── RiskSummary.tsx
    │   ├── App.tsx
    │   ├── main.tsx
    │   └── index.css
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    └── Dockerfile
```

---

## ⚠️ Batasan & Roadmap

### Batasan Saat Ini

| Batasan | Penjelasan | Solusi Future |
|---------|-----------|----------------|
| Model Size | llama3.1:8b butuh 4.9GB RAM | Use phi3:mini atau API model |
| PDF OCR | Tidak support scanned PDF | Add Tesseract OCR |
| Single User | Hanya 1 session concurrent | Multi-user auth |
| No Export | Tidak bisa export report | PDF/Word export |
| Limited Categories | Hanya 10 clause types | Expand to 25+ categories |
| No Authentication | Tidak ada login system | JWT authentication |
| Manual Deploy | Perlu command line | One-click deployment |

### Roadmap Pengembangan

#### Phase 1: Core Engine ✅ (Selesai)

- ✅ Clause segmentation & classification
- ✅ Playbook embedding & retrieval
- ✅ Hybrid risk scoring
- ✅ Redline generation
- ✅ Web UI
- ✅ Docker deployment

#### Phase 2: Advanced Features (Q1 2027)

- ☐ Multi-user authentication (JWT)
- ☐ PDF export for reports
- ☐ Bulk upload (batch processing)
- ☐ Custom playbook editor
- ☐ Version history for contracts

#### Phase 3: Enterprise (Q2 2027)

- ☐ OCR untuk scanned PDFs
- ☐ Integration dengan contract management systems
- ☐ API rate limiting
- ☐ Audit trail (who approved what)
- ☐ Slack/Email notifications

#### Phase 4: AI Enhancements (Q3 2027)

- ☐ Fine-tuned legal LLM
- ☐ Automated negotiation suggestions
- ☐ Regulatory compliance checking
- ☐ Multi-language support
- ☐ Voice input untuk legal notes

---

## 🔧 Troubleshooting

### ❌ "Ollama timeout" saat upload

**Penyebab:** Model llama3.1:8b terlalu berat untuk PC Anda.

**Solusi:**

```bash
# Gunakan phi3:mini (2GB)
docker exec -it cra_ollama ollama pull phi3:mini

# Update .env: OLLAMA_CHAT_MODEL=phi3:mini
```

### ❌ "Database connection refused"

**Penyebab:** Postgres container tidak running.

**Solusi:**

```bash
docker compose -f docker/docker-compose.yml up -d postgres
docker exec -it cra_postgres psql -U cra_admin -d contract_risk_auditor -c "SELECT 1"
```

### ❌ "No module named 'contract_risk_auditor'"

**Penyebab:** PYTHONPATH tidak diatur.

**Solusi:**

```bash
export PYTHONPATH=src  # Linux/Mac
$env:PYTHONPATH = "src"  # Windows
```

### ❌ "Frontend cannot connect to backend (CORS)"

**Penyebab:** CORS middleware tidak diatur.

**Solusi:**

```python
# src/contract_risk_auditor/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📞 Kontribusi

**Repository:** https://github.com/Tricke2D/ContractRisk

**Issues:** https://github.com/Tricke2D/ContractRisk/issues

Contributions sangat welcome! 🎉

### Cara Berkontribusi

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Guidelines

- ✅ Write tests untuk setiap perubahan (target: 85%+ coverage)
- ✅ Jalankan `poetry run pytest` sebelum commit
- ✅ Follow PEP 8 untuk Python (gunakan Ruff)
- ✅ Update documentation sesuai perubahan

---

## 📜 License

**MIT License** — Silakan digunakan untuk keperluan belajar, pengembangan, dan produksi.

```
Made with ❤️ by Muhamad Syukron Zakka
© 2026 Contract Risk Auditor — AI-Powered Legal Analysis Engine
```

---

## 🙏 Terima Kasih

Dokumen ini adalah hasil konsolidasi dan optimalisasi untuk kemudahan pembacaan, maintenance, dan kolaborasi tim. Untuk pertanyaan atau saran perbaikan, silakan buka issue di repository.

**Happy coding! 🚀**
