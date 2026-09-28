# SulabhAI

**Marathi AI Gateway to Government Schemes, Scholarships & Public Benefits**
*Final-year B.Tech (IT) project — "An OCR and Retrieval-Augmented Generation System for
Readability-Aware Marathi Government Document Assistance"*

SulabhAI helps rural citizens, farmers and students in Maharashtra ask questions about
government schemes and scholarships **in plain Marathi**, and get back **source-cited,
readability-adjusted answers** — instead of dense legal GR language. It combines document
OCR, hybrid (keyword) retrieval, a deterministic eligibility engine, and a chatbot UI.

> ⚠️ **Scope note (read this before your viva):** this repository is a genuinely working,
> testable MVP, not the full enterprise spec (PaddleOCR/Celery/pgvector/a real LLM). It ships
> clean provider abstractions (`OCRProvider`, and the RAG pipeline in `services/rag.py`) so
> those can be swapped in later without touching the API or frontend. See
> [`docs/architecture.md`](docs/architecture.md) for what's real vs. what's a documented
> stand-in, and why — that distinction is itself good material for your viva.

## What's actually implemented (and works, tested)

- **Auth**: JWT registration/login, role-based access (citizen/student/farmer/ngo/admin)
- **Schemes & Scholarships**: full CRUD, search, browsing
- **Document pipeline**: PDF upload → real text extraction (PyMuPDF) for digital PDFs, a
  clearly-labelled demo-OCR fallback for scanned pages → chunking → keyword indexing
- **RAG chatbot**: query → hybrid (keyword-overlap) retrieval over indexed chunks → citation
  extraction → **readability-aware rewrite** (4 levels, preserves numbers/dates/conditions) →
  confidence score → "insufficient evidence" fallback (never hallucinates a citation)
- **Eligibility checker**: deterministic rule engine (age/income/category/occupation), never
  an LLM guess — returns MATCH/NOT_MATCH/UNKNOWN per criterion, never "you are eligible"
- **Bookmarks, application tracker, feedback, reports, admin analytics**
- **Seed script** with clearly labelled DEMO data (a sample GR, 2 schemes, 2 scholarships,
  3 demo logins) so the whole thing runs with **zero paid API keys**
- **6 backend tests (pytest, all passing)**, clean frontend TypeScript build, Docker Compose,
  GitHub Actions CI

## What's a documented stand-in for the full spec

| Full spec asked for | This repo ships | Why |
|---|---|---|
| PaddleOCR | PyMuPDF text extraction + labelled demo fallback | PaddleOCR needs a multi-GB ML stack; the `OCRProvider` interface is ready for it |
| pgvector semantic search | Keyword/TF-overlap hybrid search | Same interface shape (`hybrid_search`) — swap in embeddings later |
| Real LLM generation | Deterministic template-based readability rewrite | Zero hallucination risk, zero API cost, fully explainable for a viva |
| Celery + Redis | Synchronous processing (fast enough for demo-sized PDFs) | Keeps local setup to one command |
| MySQL/Postgres | SQLite by default, Postgres via `docker-compose` | Zero-setup local dev; Postgres path is real and tested |

---

## Quick start (local, no Docker, ~2 minutes)

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m app.seed          # creates sulabhai.db + demo data + demo logins
uvicorn app.main:app --reload --port 8000
```
API docs: http://localhost:8000/docs

### Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```
App: http://localhost:5173

### Demo logins (created by the seed script)
| Role    | Email                  | Password  |
|---------|-------------------------|-----------|
| Admin   | admin@sulabhai.demo     | admin123  |
| Student | student@sulabhai.demo   | student123|
| Farmer  | farmer@sulabhai.demo    | farmer123 |

Try: log in as the farmer → open **AI सहाय्यक** → ask *"सिंचन अनुदान योजना काय आहे?"*
You'll get a cited, simplified answer pulled from the seeded demo GR.

---

## Quick start (Docker Compose, Postgres)
```bash
docker compose up --build
```
- Frontend: http://localhost:5173
- Backend: http://localhost:8000/docs
- Postgres: localhost:5432 (user/pass/db: `sulabhai`)

The backend container runs the seed script automatically on startup.

---

## Running tests
```bash
# backend
cd backend && python -m pytest tests/ -v

# frontend build check (also runs the TS compiler)
cd frontend && npm run build
```

## Project structure
```
sulabhai/
  backend/
    app/
      main.py            FastAPI app + router registration
      models.py           SQLAlchemy models (full schema incl. profiles, docs, chat, etc.)
      schemas.py           Pydantic request/response models
      auth.py              JWT + password hashing
      seed.py               Demo data seeder
      routers/               One router per resource
      services/
        ocr.py                 OCR provider abstraction
        chunking.py            Chunking + keyword index
        rag.py                 Retrieval + readability-aware answer generation
        eligibility.py         Deterministic rule-based matching engine
    tests/                   pytest suite
  frontend/
    src/
      pages/                 Landing, Login/Register, Schemes, Scholarships,
                               Eligibility, Assistant (chat), Dashboard, Admin, ...
      components/            Navbar, ProtectedRoute
      context/AuthContext.tsx
      api/client.ts
  docker-compose.yml
  .github/workflows/ci.yml
  docs/
```

## Environment variables
See `backend/.env.example`. Key one: `DEMO_MODE=true` (default) keeps everything
deterministic and key-free. The `LLM_API_KEY`/`LLM_PROVIDER` fields are wired for a future
real-LLM integration but unused while `DEMO_MODE=true`.

## Known limitations (be upfront about these in your report/viva)
- Retrieval is keyword-overlap, not semantic embeddings — good enough for demo documents,
  will miss paraphrased queries at scale. `services/rag.py` documents exactly where a real
  embedding model would plug in.
- OCR is real digital-text extraction, not scanned-image OCR — swap in PaddleOCR via the
  `OCRProvider` interface in `services/ocr.py` for that capability.
- No async task queue — fine for demo-sized single PDF uploads; would need Celery+Redis for
  bulk/production document ingestion, exactly as the interface anticipates.
- No voice input/output, WhatsApp, or multi-state expansion in this MVP — the docs describe
  these as future roadmap, not shipped code.

## Roadmap (see `docs/`)
`docs/architecture.md`, `docs/rag.md`, `docs/eligibility.md` walk through what's implemented
and the exact extension points for PaddleOCR, pgvector, and a real LLM.

## Deploying to GitHub
```bash
cd sulabhai
git init
git add .
git commit -m "Initial commit: SulabhAI MVP"
git branch -M main
git remote add origin https://github.com/<your-username>/sulabhai.git
git push -u origin main
```
(`.gitignore` already excludes `node_modules`, `.env`, `*.db`, `uploads/`.)
