"""
Deterministic rule-based eligibility/matching engine.

Deliberately NOT an LLM call: eligibility must be explainable and
reproducible, per the "AI safety" requirements (never claim guaranteed
eligibility). Each criterion is evaluated independently and the overall
result is a conservative aggregate (worst case wins; missing data -> UNKNOWN).
"""
from typing import Optional
from .. import models, schemas

DISCLAIMER = (
    "ही केवळ प्राथमिक तपासणी आहे, अधिकृत निर्णय नाही. अंतिम पात्रता संबंधित "
    "सरकारी विभागाच्या अधिकृत संकेतस्थळावर किंवा कार्यालयात तपासा."
)


def _check_range(value, low, high, label) -> schemas.EligibilityCriterion:
    if value is None:
        return schemas.EligibilityCriterion(criterion=label, result="UNKNOWN",
                                             detail=f"{label}: माहिती दिलेली नाही.")
    if low is not None and value < low:
        return schemas.EligibilityCriterion(criterion=label, result="NOT_MATCH",
                                             detail=f"{label}: किमान मर्यादेपेक्षा कमी.")
    if high is not None and value > high:
        return schemas.EligibilityCriterion(criterion=label, result="NOT_MATCH",
                                             detail=f"{label}: कमाल मर्यादेपेक्षा जास्त.")
    return schemas.EligibilityCriterion(criterion=label, result="MATCH",
                                         detail=f"{label}: जुळते.")


def check_scheme_eligibility(scheme: models.Scheme, req: schemas.EligibilityRequest) -> schemas.EligibilityResult:
    criteria = []

    criteria.append(_check_range(req.age, scheme.min_age, scheme.max_age, "वय"))

    if scheme.max_income is not None:
        criteria.append(_check_range(req.income, None, scheme.max_income, "उत्पन्न"))
    else:
        criteria.append(schemas.EligibilityCriterion(criterion="उत्पन्न", result="UNKNOWN",
                                                       detail="उत्पन्न मर्यादा या योजनेसाठी नोंदवलेली नाही."))

    if scheme.applicable_categories:
        allowed = [c.strip().lower() for c in scheme.applicable_categories.split(",")]
        if req.category:
            result = "MATCH" if req.category.lower() in allowed else "NOT_MATCH"
            criteria.append(schemas.EligibilityCriterion(
                criterion="प्रवर्ग (Category)", result=result,
                detail=f"स्वीकार्य प्रवर्ग: {', '.join(allowed)}"))
        else:
            criteria.append(schemas.EligibilityCriterion(
                criterion="प्रवर्ग (Category)", result="UNKNOWN", detail="प्रवर्ग माहिती दिलेली नाही."))

    if scheme.applicable_occupations:
        allowed = [o.strip().lower() for o in scheme.applicable_occupations.split(",")]
        if req.occupation:
            result = "MATCH" if req.occupation.lower() in allowed else "NOT_MATCH"
            criteria.append(schemas.EligibilityCriterion(
                criterion="लाभार्थी गट", result=result,
                detail=f"लागू गट: {', '.join(allowed)}"))
        else:
            criteria.append(schemas.EligibilityCriterion(
                criterion="लाभार्थी गट", result="UNKNOWN", detail="व्यवसाय/गट माहिती दिलेली नाही."))

    overall = _aggregate(criteria)
    return schemas.EligibilityResult(
        item_type="scheme", item_id=scheme.id, item_title=scheme.title_marathi or scheme.title,
        overall=overall, criteria=criteria, disclaimer=DISCLAIMER,
    )


def check_scholarship_eligibility(sch: models.Scholarship, req: schemas.EligibilityRequest) -> schemas.EligibilityResult:
    criteria = []
    if sch.min_income is not None or sch.max_income is not None:
        criteria.append(_check_range(req.income, sch.min_income, sch.max_income, "उत्पन्न"))
    else:
        criteria.append(schemas.EligibilityCriterion(criterion="उत्पन्न", result="UNKNOWN",
                                                       detail="उत्पन्न मर्यादा नोंदवलेली नाही."))

    if sch.education_levels:
        allowed = [e.strip().lower() for e in sch.education_levels.split(",")]
        if req.education_level:
            result = "MATCH" if req.education_level.lower() in allowed else "NOT_MATCH"
            criteria.append(schemas.EligibilityCriterion(
                criterion="शिक्षण स्तर", result=result, detail=f"स्वीकार्य स्तर: {', '.join(allowed)}"))
        else:
            criteria.append(schemas.EligibilityCriterion(
                criterion="शिक्षण स्तर", result="UNKNOWN", detail="शिक्षण स्तर दिलेला नाही."))

    if sch.applicable_categories:
        allowed = [c.strip().lower() for c in sch.applicable_categories.split(",")]
        if req.category:
            result = "MATCH" if req.category.lower() in allowed else "NOT_MATCH"
            criteria.append(schemas.EligibilityCriterion(
                criterion="प्रवर्ग (Category)", result=result, detail=f"स्वीकार्य प्रवर्ग: {', '.join(allowed)}"))
        else:
            criteria.append(schemas.EligibilityCriterion(
                criterion="प्रवर्ग (Category)", result="UNKNOWN", detail="प्रवर्ग माहिती दिलेली नाही."))

    overall = _aggregate(criteria)
    return schemas.EligibilityResult(
        item_type="scholarship", item_id=sch.id, item_title=sch.name_marathi or sch.name,
        overall=overall, criteria=criteria, disclaimer=DISCLAIMER,
    )


def _aggregate(criteria) -> str:
    results = [c.result for c in criteria]
    if "NOT_MATCH" in results:
        return "LIKELY_NOT_MATCH"
    if "UNKNOWN" in results:
        return "INSUFFICIENT_INFO"
    return "LIKELY_MATCH"
