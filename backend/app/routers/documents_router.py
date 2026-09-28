import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from .. import models, auth
from ..database import get_db
from ..config import settings
from ..services.ocr import process_pdf
from ..services.chunking import chunk_text, keyword_string

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload")
def upload_document(
    title: str,
    department: str = "",
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.require_admin),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    safe_name = f"{uuid.uuid4()}.pdf"
    path = os.path.join(settings.upload_dir, safe_name)
    with open(path, "wb") as f:
        f.write(file.file.read())

    doc = models.Document(title=title, department=department, filename=safe_name, status="processing")
    db.add(doc)
    db.commit()
    db.refresh(doc)

    _process_document(db, doc, path)
    return {"id": doc.id, "status": doc.status, "pages": len(doc.pages)}


def _process_document(db: Session, doc: models.Document, path: str):
    pages = process_pdf(path)
    for p in pages:
        page_row = models.DocumentPage(
            document_id=doc.id, page_number=p["page_number"],
            raw_text=p["raw_text"], cleaned_text=p["cleaned_text"],
            ocr_confidence=p["confidence"],
        )
        db.add(page_row)
        for chunk in chunk_text(p["cleaned_text"]):
            db.add(models.DocumentChunk(
                document_id=doc.id, page_number=p["page_number"],
                text=chunk, keywords=keyword_string(chunk),
            ))
    doc.status = "published"
    db.commit()


@router.get("")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(models.Document).order_by(models.Document.created_at.desc()).all()
    return [
        {"id": d.id, "title": d.title, "department": d.department, "status": d.status,
         "pages": len(d.pages), "verification_status": d.verification_status, "is_demo": d.is_demo}
        for d in docs
    ]


@router.get("/{document_id}")
def get_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "id": doc.id, "title": doc.title, "department": doc.department, "status": doc.status,
        "pages": [{"page_number": p.page_number, "text": p.cleaned_text} for p in doc.pages],
    }
