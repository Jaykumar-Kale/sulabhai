import uuid
from datetime import datetime
from sqlalchemy import (Column, String, Integer, Float, Boolean, DateTime,
                         ForeignKey, Text, JSON)
from sqlalchemy.orm import relationship
from .database import Base

def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="citizen")  # citizen, student, farmer, ngo, admin
    district = Column(String, nullable=True)
    taluka = Column(String, nullable=True)
    village = Column(String, nullable=True)
    language = Column(String, default="mr")
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    student_profile = relationship("StudentProfile", uselist=False, back_populates="user")
    farmer_profile = relationship("FarmerProfile", uselist=False, back_populates="user")
    bookmarks = relationship("Bookmark", back_populates="user")
    applications = relationship("Application", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")


class StudentProfile(Base):
    __tablename__ = "student_profiles"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    education_level = Column(String, nullable=True)
    course = Column(String, nullable=True)
    college = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    income = Column(Float, nullable=True)
    category = Column(String, nullable=True)  # OPEN, OBC, SC, ST, EWS...
    rural_urban = Column(String, nullable=True)
    hostel_or_day_scholar = Column(String, nullable=True)

    user = relationship("User", back_populates="student_profile")


class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    landholding_acres = Column(Float, nullable=True)
    crop = Column(String, nullable=True)
    irrigation = Column(String, nullable=True)
    income = Column(Float, nullable=True)
    farmer_category = Column(String, nullable=True)  # small, marginal, large

    user = relationship("User", back_populates="farmer_profile")


class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, default=gen_uuid)
    title = Column(String, nullable=False)
    department = Column(String, nullable=True)
    published_date = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    filename = Column(String, nullable=True)
    status = Column(String, default="uploaded")  # uploaded, processing, indexed, published
    verification_status = Column(String, default="unverified")
    is_demo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    pages = relationship("DocumentPage", back_populates="document", cascade="all, delete-orphan")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentPage(Base):
    __tablename__ = "document_pages"
    id = Column(String, primary_key=True, default=gen_uuid)
    document_id = Column(String, ForeignKey("documents.id"))
    page_number = Column(Integer)
    raw_text = Column(Text)
    cleaned_text = Column(Text)
    ocr_confidence = Column(Float, nullable=True)

    document = relationship("Document", back_populates="pages")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(String, primary_key=True, default=gen_uuid)
    document_id = Column(String, ForeignKey("documents.id"))
    page_number = Column(Integer)
    text = Column(Text)
    keywords = Column(Text)  # simple space-joined keyword index (demo hybrid search)

    document = relationship("Document", back_populates="chunks")


class Scheme(Base):
    __tablename__ = "schemes"
    id = Column(String, primary_key=True, default=gen_uuid)
    title = Column(String, nullable=False)
    title_marathi = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    description_marathi = Column(Text, nullable=True)
    department = Column(String, nullable=True)
    category = Column(String, nullable=True)
    target_group = Column(String, nullable=True)
    eligibility = Column(Text, nullable=True)
    eligibility_marathi = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    benefits_marathi = Column(Text, nullable=True)
    required_documents = Column(Text, nullable=True)
    application_process = Column(Text, nullable=True)
    official_url = Column(String, nullable=True)
    helpline = Column(String, nullable=True)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    status = Column(String, default="active")
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    source_page = Column(Integer, nullable=True)
    last_verified_at = Column(DateTime, nullable=True)
    verification_status = Column(String, default="unverified")
    is_demo = Column(Boolean, default=True)
    # eligibility rule fields (deterministic matching engine)
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)
    max_income = Column(Float, nullable=True)
    applicable_categories = Column(String, nullable=True)  # comma separated
    applicable_occupations = Column(String, nullable=True)  # comma separated: student,farmer,...
    created_at = Column(DateTime, default=datetime.utcnow)


class Scholarship(Base):
    __tablename__ = "scholarships"
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    name_marathi = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    eligibility = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    amount = Column(Float, nullable=True)
    deadline = Column(String, nullable=True)
    required_documents = Column(Text, nullable=True)
    application_url = Column(String, nullable=True)
    verification_status = Column(String, default="unverified")
    is_demo = Column(Boolean, default=True)
    min_income = Column(Float, nullable=True)
    max_income = Column(Float, nullable=True)
    education_levels = Column(String, nullable=True)  # comma separated
    applicable_categories = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String, default="New chat")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(String, primary_key=True, default=gen_uuid)
    session_id = Column(String, ForeignKey("chat_sessions.id"))
    role = Column(String)  # user | assistant
    content = Column(Text)
    readability_level = Column(Integer, default=1)
    citations = Column(JSON, nullable=True)
    confidence = Column(String, nullable=True)  # high | medium | low | none
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    item_type = Column(String)  # scheme | scholarship | document
    item_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookmarks")


class Application(Base):
    __tablename__ = "applications"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    item_type = Column(String)  # scheme | scholarship
    item_id = Column(String)
    status = Column(String, default="interested")
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="applications")


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    message_id = Column(String, nullable=True)
    helpful = Column(Boolean)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    item_type = Column(String)
    item_id = Column(String)
    reason = Column(String)
    details = Column(Text, nullable=True)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
