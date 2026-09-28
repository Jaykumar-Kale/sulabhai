"""
Seed script. Run with: python -m app.seed

Populates demo users, documents (with OCR-processed chunks), schemes, and
scholarships so the whole product is demoable end-to-end with zero external
API keys. All demo records are clearly flagged is_demo=True and labelled
"DEMO SCHEME" / "DEMO SCHOLARSHIP" per the project's data-integrity rules -
these are NOT real government schemes.
"""
from datetime import datetime
from .database import Base, engine, SessionLocal
from . import models, auth
from .services.chunking import chunk_text, keyword_string

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def get_or_create_user(name, email, password, role, **kw):
    u = db.query(models.User).filter(models.User.email == email).first()
    if u:
        return u
    u = models.User(name=name, email=email, hashed_password=auth.hash_password(password), role=role, **kw)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

print("Seeding users...")
admin = get_or_create_user("Admin", "admin@sulabhai.demo", "admin123", "admin")
student = get_or_create_user("Demo Student", "student@sulabhai.demo", "student123", "student", district="Pune")
farmer = get_or_create_user("Demo Farmer", "farmer@sulabhai.demo", "farmer123", "farmer", district="Nashik")

print("Seeding demo document + OCR pipeline...")
doc = db.query(models.Document).filter(models.Document.title == "DEMO GR - Farmer Subsidy Scheme").first()
if not doc:
    doc = models.Document(
        title="DEMO GR - Farmer Subsidy Scheme",
        department="Agriculture Department (DEMO)",
        published_date="2025-04-01",
        source_url=None,
        status="published",
        verification_status="unverified",
        is_demo=True,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    demo_text = (
        "शासन निर्णय: शेतकरी अनुदान योजना (DEMO). विहित अटी व शर्तींच्या अधीन राहून "
        "पात्र लाभार्थ्यांना सिंचन उपकरणांसाठी 50% पर्यंत अनुदान दिले जाईल. "
        "अर्जदार महाराष्ट्राचा रहिवासी शेतकरी असावा. वार्षिक उत्पन्न 2,00,000 रुपयांपेक्षा कमी असावे. "
        "आवश्यक कागदपत्रे: सातबारा उतारा, आधार कार्ड, बँक पासबुक, उत्पन्नाचा दाखला. "
        "अर्ज ऑनलाईन पद्धतीने https://example-demo-gov.in या संकेतस्थळावर करावा. "
        "अर्ज करण्याची अंतिम तारीख 31 डिसेंबर 2026 आहे. (ही सर्व माहिती डेमो हेतूसाठी आहे.)"
    )
    page = models.DocumentPage(document_id=doc.id, page_number=1, raw_text=demo_text,
                                 cleaned_text=demo_text, ocr_confidence=1.0)
    db.add(page)
    for chunk in chunk_text(demo_text):
        db.add(models.DocumentChunk(document_id=doc.id, page_number=1, text=chunk,
                                      keywords=keyword_string(chunk)))
    db.commit()

print("Seeding schemes...")
if db.query(models.Scheme).count() == 0:
    schemes = [
        models.Scheme(
            title="DEMO SCHEME - Farmer Irrigation Subsidy",
            title_marathi="डेमो योजना - शेतकरी सिंचन अनुदान",
            description_marathi="सिंचन उपकरणांसाठी अनुदान देणारी योजना.",
            department="Agriculture Department (DEMO)",
            category="agriculture",
            target_group="farmer",
            eligibility_marathi="महाराष्ट्राचा रहिवासी शेतकरी, वार्षिक उत्पन्न 2 लाखांपेक्षा कमी.",
            benefits_marathi="सिंचन उपकरणांवर 50% पर्यंत अनुदान.",
            required_documents="सातबारा उतारा, आधार कार्ड, बँक पासबुक, उत्पन्नाचा दाखला",
            official_url="https://example-demo-gov.in",
            helpline="1800-000-000",
            status="active",
            verification_status="unverified",
            is_demo=True,
            source_document_id=doc.id,
            source_page=1,
            min_age=18, max_age=70, max_income=200000,
            applicable_occupations="farmer",
        ),
        models.Scheme(
            title="DEMO SCHEME - Girls Education Support",
            title_marathi="डेमो योजना - मुलींसाठी शिक्षण सहाय्य",
            description_marathi="शालेय मुलींसाठी शिक्षण सहाय्य योजना.",
            department="Education Department (DEMO)",
            category="education",
            target_group="student",
            eligibility_marathi="इयत्ता 8 वी ते 12 वी मधील मुली, कौटुंबिक उत्पन्न 1 लाखांपेक्षा कमी.",
            benefits_marathi="वार्षिक रु. 5,000 शिष्यवृत्ती.",
            required_documents="शाळेचा दाखला, आधार कार्ड, उत्पन्नाचा दाखला",
            official_url="https://example-demo-gov.in/education",
            status="active",
            verification_status="unverified",
            is_demo=True,
            min_age=12, max_age=18, max_income=100000,
            applicable_occupations="student",
        ),
    ]
    db.add_all(schemes)
    db.commit()

print("Seeding scholarships...")
if db.query(models.Scholarship).count() == 0:
    scholarships = [
        models.Scholarship(
            name="DEMO SCHOLARSHIP - Merit cum Means",
            name_marathi="डेमो शिष्यवृत्ती - गुणवत्ता व गरजेवर आधारित",
            provider="State Education Board (DEMO)",
            description="Merit-cum-means based scholarship for undergraduate students.",
            eligibility="Family income below 3,00,000/year; minimum 60% marks.",
            benefits="Annual tuition fee waiver up to Rs. 25,000.",
            amount=25000,
            deadline="2026-12-31",
            required_documents="Income certificate, mark sheet, Aadhaar card",
            application_url="https://example-demo-gov.in/scholarship",
            verification_status="unverified",
            is_demo=True,
            max_income=300000,
            education_levels="undergraduate,diploma",
        ),
        models.Scholarship(
            name="DEMO SCHOLARSHIP - Rural Talent Award",
            name_marathi="डेमो शिष्यवृत्ती - ग्रामीण प्रतिभा पुरस्कार",
            provider="NGO Consortium (DEMO)",
            description="For students from rural backgrounds pursuing higher education.",
            eligibility="Rural domicile; family income below 2,00,000/year.",
            benefits="One-time award of Rs. 10,000.",
            amount=10000,
            deadline="2026-11-30",
            required_documents="Domicile certificate, income certificate",
            application_url="https://example-demo-gov.in/rural-talent",
            verification_status="unverified",
            is_demo=True,
            max_income=200000,
            education_levels="undergraduate,postgraduate",
        ),
    ]
    db.add_all(scholarships)
    db.commit()

print("Seed complete.")
print("Demo logins:")
print("  admin@sulabhai.demo / admin123")
print("  student@sulabhai.demo / student123")
print("  farmer@sulabhai.demo / farmer123")
db.close()
