from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..services import eligibility as elig_service

router = APIRouter(prefix="/api/eligibility", tags=["eligibility"])


@router.post("/check", response_model=schemas.EligibilityResult)
def check_eligibility(payload: schemas.EligibilityRequest, db: Session = Depends(get_db)):
    if payload.scheme_id:
        scheme = db.query(models.Scheme).filter(models.Scheme.id == payload.scheme_id).first()
        if not scheme:
            raise HTTPException(status_code=404, detail="Scheme not found")
        return elig_service.check_scheme_eligibility(scheme, payload)
    if payload.scholarship_id:
        sch = db.query(models.Scholarship).filter(models.Scholarship.id == payload.scholarship_id).first()
        if not sch:
            raise HTTPException(status_code=404, detail="Scholarship not found")
        return elig_service.check_scholarship_eligibility(sch, payload)
    raise HTTPException(status_code=400, detail="scheme_id or scholarship_id is required")
