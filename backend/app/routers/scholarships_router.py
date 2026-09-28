from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db
from ..services import eligibility as elig_service

router = APIRouter(prefix="/api/scholarships", tags=["scholarships"])


@router.get("", response_model=List[schemas.ScholarshipOut])
def list_scholarships(q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Scholarship)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (models.Scholarship.name.ilike(like)) |
            (models.Scholarship.name_marathi.ilike(like))
        )
    return query.order_by(models.Scholarship.created_at.desc()).all()


@router.get("/matches", response_model=List[schemas.EligibilityResult])
def match_scholarships(
    income: Optional[float] = None,
    education_level: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    req = schemas.EligibilityRequest(income=income, education_level=education_level, category=category)
    results = []
    for sch in db.query(models.Scholarship).all():
        result = elig_service.check_scholarship_eligibility(sch, req)
        if result.overall != "LIKELY_NOT_MATCH":
            results.append(result)
    return results


@router.get("/{scholarship_id}", response_model=schemas.ScholarshipOut)
def get_scholarship(scholarship_id: str, db: Session = Depends(get_db)):
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == scholarship_id).first()
    if not sch:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return sch


@router.post("", response_model=schemas.ScholarshipOut)
def create_scholarship(payload: dict, db: Session = Depends(get_db), admin=Depends(auth.require_admin)):
    sch = models.Scholarship(**payload)
    db.add(sch)
    db.commit()
    db.refresh(sch)
    return sch
