from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db
from ..services import rag

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=schemas.ChatResponse)
def chat(payload: schemas.ChatRequest, db: Session = Depends(get_db),
          current_user: models.User = Depends(auth.get_current_user)):
    session = None
    if payload.session_id:
        session = db.query(models.ChatSession).filter(
            models.ChatSession.id == payload.session_id,
            models.ChatSession.user_id == current_user.id,
        ).first()
    if not session:
        session = models.ChatSession(user_id=current_user.id, title=payload.message[:60])
        db.add(session)
        db.commit()
        db.refresh(session)

    user_msg = models.ChatMessage(session_id=session.id, role="user", content=payload.message)
    db.add(user_msg)
    db.commit()

    result = rag.build_answer(db, payload.message, payload.readability_level)

    assistant_msg = models.ChatMessage(
        session_id=session.id, role="assistant", content=result["answer"],
        readability_level=payload.readability_level,
        citations=result["citations"], confidence=result["confidence"],
    )
    db.add(assistant_msg)
    db.commit()

    return schemas.ChatResponse(
        session_id=session.id,
        answer=result["answer"],
        citations=result["citations"],
        confidence=result["confidence"],
        next_steps=result["next_steps"],
    )


@router.get("/sessions")
def list_sessions(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    sessions = db.query(models.ChatSession).filter(
        models.ChatSession.user_id == current_user.id
    ).order_by(models.ChatSession.created_at.desc()).all()
    return [{"id": s.id, "title": s.title, "created_at": s.created_at} for s in sessions]


@router.get("/sessions/{session_id}")
def get_session(session_id: str, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id, models.ChatSession.user_id == current_user.id
    ).first()
    if not session:
        return {"error": "not found"}
    return {
        "id": session.id,
        "title": session.title,
        "messages": [
            {
                "role": m.role, "content": m.content, "citations": m.citations,
                "confidence": m.confidence, "created_at": m.created_at,
            } for m in session.messages
        ],
    }
