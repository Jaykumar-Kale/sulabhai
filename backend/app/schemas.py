from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "citizen"
    district: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    name: str
    email: str
    role: str
    district: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class SchemeOut(BaseModel):
    id: str
    title: str
    title_marathi: Optional[str] = None
    description_marathi: Optional[str] = None
    department: Optional[str] = None
    category: Optional[str] = None
    target_group: Optional[str] = None
    eligibility_marathi: Optional[str] = None
    benefits_marathi: Optional[str] = None
    required_documents: Optional[str] = None
    official_url: Optional[str] = None
    status: str
    verification_status: str
    is_demo: bool

    class Config:
        from_attributes = True


class ScholarshipOut(BaseModel):
    id: str
    name: str
    name_marathi: Optional[str] = None
    provider: Optional[str] = None
    description: Optional[str] = None
    eligibility: Optional[str] = None
    amount: Optional[float] = None
    deadline: Optional[str] = None
    required_documents: Optional[str] = None
    application_url: Optional[str] = None
    is_demo: bool

    class Config:
        from_attributes = True


class EligibilityRequest(BaseModel):
    scheme_id: Optional[str] = None
    scholarship_id: Optional[str] = None
    age: Optional[int] = None
    income: Optional[float] = None
    category: Optional[str] = None
    occupation: Optional[str] = None  # student | farmer | citizen
    education_level: Optional[str] = None


class EligibilityCriterion(BaseModel):
    criterion: str
    result: str  # MATCH | NOT_MATCH | UNKNOWN
    detail: str


class EligibilityResult(BaseModel):
    item_type: str
    item_id: str
    item_title: str
    overall: str  # LIKELY_MATCH | LIKELY_NOT_MATCH | INSUFFICIENT_INFO
    criteria: List[EligibilityCriterion]
    disclaimer: str


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    readability_level: int = 1


class Citation(BaseModel):
    document_title: str
    department: Optional[str] = None
    page: Optional[int] = None
    source_url: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    citations: List[Citation] = []
    confidence: str
    next_steps: Optional[List[str]] = None


class BookmarkCreate(BaseModel):
    item_type: str
    item_id: str


class ApplicationCreate(BaseModel):
    item_type: str
    item_id: str
    status: str = "interested"
    notes: Optional[str] = None


class FeedbackCreate(BaseModel):
    message_id: Optional[str] = None
    helpful: bool
    reason: Optional[str] = None


class ReportCreate(BaseModel):
    item_type: str
    item_id: str
    reason: str
    details: Optional[str] = None
