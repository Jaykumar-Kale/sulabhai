"""Chunking + a simple keyword index used for demo-mode hybrid retrieval.

A production system would add pgvector embeddings on top of this. The
interfaces here (`chunk_text`, `score_chunk`) are written so a real
embedding-based similarity score can be dropped in alongside the keyword
score without changing calling code (see rag.py `hybrid_search`).
"""
import re
from typing import List, Dict

STOPWORDS_MR_EN = set("""
आहे आहेत या ते तो ती हे या साठी व आणि किंवा नाही तर पण या मध्ये चा ची चे
the a an is are of to for and or in on with be will was were this that
""".split())


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80) -> List[str]:
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks


def extract_keywords(text: str) -> List[str]:
    words = re.findall(r"[\w\u0900-\u097F]+", text.lower())
    return [w for w in words if w not in STOPWORDS_MR_EN and len(w) > 1]


def keyword_string(text: str) -> str:
    return " ".join(extract_keywords(text))


def score_chunk(query_keywords: List[str], chunk_keywords: str) -> float:
    """Simple TF overlap score (stand-in for semantic similarity in demo mode)."""
    chunk_words = chunk_keywords.split()
    if not chunk_words or not query_keywords:
        return 0.0
    chunk_set = set(chunk_words)
    overlap = sum(1 for k in query_keywords if k in chunk_set)
    return overlap / (len(query_keywords) ** 0.5 + 1e-6)
