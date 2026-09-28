from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api", tags=["misc"])


@router.post("/bookmarks")
def add_bookmark(payload: schemas.BookmarkCreate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth.get_current_user)):
    bm = models.Bookmark(user_id=current_user.id, item_type=payload.item_type, item_id=payload.item_id)
    db.add(bm)
    db.commit()
    db.refresh(bm)
    return {"id": bm.id}


@router.get("/bookmarks")
def list_bookmarks(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    bms = db.query(models.Bookmark).filter(models.Bookmark.user_id == current_user.id).all()
    return [{"id": b.id, "item_type": b.item_type, "item_id": b.item_id} for b in bms]


@router.delete("/bookmarks/{bookmark_id}")
def delete_bookmark(bookmark_id: str, db: Session = Depends(get_db),
                      current_user: models.User = Depends(auth.get_current_user)):
    bm = db.query(models.Bookmark).filter(models.Bookmark.id == bookmark_id,
                                            models.Bookmark.user_id == current_user.id).first()
    if bm:
        db.delete(bm)
        db.commit()
    return {"ok": True}


@router.post("/applications")
def create_application(payload: schemas.ApplicationCreate, db: Session = Depends(get_db),
                         current_user: models.User = Depends(auth.get_current_user)):
    app_row = models.Application(user_id=current_user.id, item_type=payload.item_type,
                                   item_id=payload.item_id, status=payload.status, notes=payload.notes)
    db.add(app_row)
    db.commit()
    db.refresh(app_row)
    return {"id": app_row.id}


@router.get("/applications")
def list_applications(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    apps = db.query(models.Application).filter(models.Application.user_id == current_user.id).all()
    return [{"id": a.id, "item_type": a.item_type, "item_id": a.item_id, "status": a.status} for a in apps]


@router.put("/applications/{application_id}")
def update_application(application_id: str, payload: dict, db: Session = Depends(get_db),
                         current_user: models.User = Depends(auth.get_current_user)):
    app_row = db.query(models.Application).filter(
        models.Application.id == application_id, models.Application.user_id == current_user.id
    ).first()
    if app_row:
        if "status" in payload:
            app_row.status = payload["status"]
        if "notes" in payload:
            app_row.notes = payload["notes"]
        db.commit()
    return {"ok": True}


@router.post("/feedback")
def submit_feedback(payload: schemas.FeedbackCreate, db: Session = Depends(get_db),
                      current_user: models.User = Depends(auth.get_current_user)):
    fb = models.Feedback(user_id=current_user.id, message_id=payload.message_id,
                           helpful=payload.helpful, reason=payload.reason)
    db.add(fb)
    db.commit()
    return {"ok": True}


@router.post("/reports")
def submit_report(payload: schemas.ReportCreate, db: Session = Depends(get_db),
                    current_user: models.User = Depends(auth.get_current_user)):
    r = models.Report(user_id=current_user.id, item_type=payload.item_type, item_id=payload.item_id,
                        reason=payload.reason, details=payload.details)
    db.add(r)
    db.commit()
    return {"ok": True}


@router.get("/admin/reports")
def admin_list_reports(db: Session = Depends(get_db), admin: models.User = Depends(auth.require_admin)):
    reports = db.query(models.Report).order_by(models.Report.created_at.desc()).all()
    return [{"id": r.id, "item_type": r.item_type, "item_id": r.item_id, "reason": r.reason,
             "status": r.status} for r in reports]


@router.get("/admin/analytics")
def admin_analytics(db: Session = Depends(get_db), admin: models.User = Depends(auth.require_admin)):
    return {
        "users": db.query(models.User).count(),
        "schemes": db.query(models.Scheme).count(),
        "scholarships": db.query(models.Scholarship).count(),
        "documents": db.query(models.Document).count(),
        "chat_sessions": db.query(models.ChatSession).count(),
        "feedback": db.query(models.Feedback).count(),
        "reports_open": db.query(models.Report).filter(models.Report.status == "open").count(),
    }
