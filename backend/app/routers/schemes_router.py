from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/schemes", tags=["schemes"])


@router.get("", response_model=List[schemas.SchemeOut])
def list_schemes(
    q: Optional[str] = None,
    category: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Scheme).filter(models.Scheme.status == "active")
    if category:
        query = query.filter(models.Scheme.category == category)
    if department:
        query = query.filter(models.Scheme.department == department)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (models.Scheme.title.ilike(like)) |
            (models.Scheme.title_marathi.ilike(like)) |
            (models.Scheme.description_marathi.ilike(like))
        )
    return query.order_by(models.Scheme.created_at.desc()).all()


@router.get("/{scheme_id}", response_model=schemas.SchemeOut)
def get_scheme(scheme_id: str, db: Session = Depends(get_db)):
    scheme = db.query(models.Scheme).filter(models.Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme


@router.post("", response_model=schemas.SchemeOut)
def create_scheme(payload: dict, db: Session = Depends(get_db), admin=Depends(auth.require_admin)):
    scheme = models.Scheme(**payload)
    db.add(scheme)
    db.commit()
    db.refresh(scheme)
    return scheme


@router.put("/{scheme_id}", response_model=schemas.SchemeOut)
def update_scheme(scheme_id: str, payload: dict, db: Session = Depends(get_db), admin=Depends(auth.require_admin)):
    scheme = db.query(models.Scheme).filter(models.Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    for k, v in payload.items():
        if hasattr(scheme, k):
            setattr(scheme, k, v)
    db.commit()
    db.refresh(scheme)
    return scheme
