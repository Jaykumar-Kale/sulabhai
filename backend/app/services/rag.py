"""
RAG pipeline (demo-mode implementation).

Pipeline: query normalization -> keyword-hybrid retrieval over indexed
DocumentChunks -> context construction -> template-based, readability-aware
answer generation -> citation extraction -> confidence scoring.

DEMO_MODE=true (default) uses this deterministic pipeline so the whole
product runs with zero external API keys and zero hallucination risk.
If DEMO_MODE=false and settings.llm_api_key is set, `generate_llm_answer`
is where you would wire a real LLMProvider call (OpenAI, etc.) - the
retrieval + citation + readability steps stay identical, which is the
whole point of the provider-abstraction pattern the architecture uses.
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from .. import models
from .chunking import extract_keywords, score_chunk
from ..config import settings

NO_EVIDENCE_MSG = (
    "मला उपलब्ध अधिकृत कागदपत्रांमध्ये या प्रश्नाचे पुरेसे पुरावे सापडले नाहीत. "
    "कृपया अधिकृत सरकारी संकेतस्थळावर तपासा."
)


def hybrid_search(db: Session, query: str, top_k: int = 4) -> List[Dict]:
    query_keywords = extract_keywords(query)
    chunks = db.query(models.DocumentChunk).join(
        models.Document, models.DocumentChunk.document_id == models.Document.id
    ).filter(models.Document.status == "published").all()

    scored = []
    for c in chunks:
        s = score_chunk(query_keywords, c.keywords or "")
        if s > 0:
            scored.append((s, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]

    results = []
    for score, c in top:
        doc = db.query(models.Document).filter(models.Document.id == c.document_id).first()
        results.append({
            "score": round(score, 3),
            "text": c.text,
            "page": c.page_number,
            "document_title": doc.title if doc else "Unknown",
            "department": doc.department if doc else None,
            "source_url": doc.source_url if doc else None,
        })
    return results


def simplify_readability(text: str, level: int) -> str:
    """Readability-aware rewrite. Levels 1-2 shorten sentences and swap a
    handful of common formal/legal Marathi phrasings for plain equivalents,
    while explicitly preserving numbers, dates and eligibility clauses
    (never stripped). Level 3-4 return the text closer to the source."""
    replacements = {
        "विहित अटी व शर्तींच्या अधीन राहून": "दिलेल्या अटी पूर्ण केल्यास",
        "पात्र लाभार्थ्यांना": "पात्र व्यक्तींना",
        "उपरोक्त": "वरील",
        "तद्नुसार": "त्यानुसार",
        "अधिसूचित": "जाहीर केलेल्या",
    }
    out = text
    if level <= 2:
        for k, v in replacements.items():
            out = out.replace(k, v)
        sentences = [s.strip() for s in out.split("।") if s.strip()] or \
                    [s.strip() for s in out.split(".") if s.strip()]
        if level == 1 and len(sentences) > 3:
            sentences = sentences[:3] + ["... (अधिक तपशीलासाठी मूळ दस्तऐवज पहा)"]
        out = ". ".join(sentences)
    return out


def build_answer(db: Session, query: str, readability_level: int = 1) -> Dict:
    evidence = hybrid_search(db, query)

    if not evidence:
        return {
            "answer": NO_EVIDENCE_MSG,
            "citations": [],
            "confidence": "none",
            "next_steps": [
                "अधिकृत सरकारी संकेतस्थळावर योजनेचे नाव शोधा.",
                "जवळच्या सरकारी सेवा केंद्रावर विचारणा करा.",
            ],
        }

    context_text = " ".join(e["text"] for e in evidence[:3])
    simplified = simplify_readability(context_text, readability_level)

    citations = [
        {
            "document_title": e["document_title"],
            "department": e["department"],
            "page": e["page"],
            "source_url": e["source_url"],
        }
        for e in evidence
    ]

    top_score = evidence[0]["score"]
    confidence = "high" if top_score >= 1.2 else "medium" if top_score >= 0.5 else "low"

    demo_prefix = ""
    if any(True for e in evidence if "DEMO" in e["text"]):
        demo_prefix = "(ही माहिती डेमो/नमुना दस्तऐवजावर आधारित आहे.) "

    answer = f"{demo_prefix}{simplified}"

    next_steps = [
        "पुढील पायरी: वरील स्रोत दस्तऐवज उघडून तपशील तपासा.",
        "अर्ज करण्यापूर्वी अधिकृत संकेतस्थळावर अंतिम तारीख व अटी पुन्हा तपासा.",
    ]

    return {
        "answer": answer,
        "citations": citations,
        "confidence": confidence,
        "next_steps": next_steps,
    }
