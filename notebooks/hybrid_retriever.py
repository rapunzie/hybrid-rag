# hybrid_retriever.py

from structured_retriever import StructuredRetriever
from vector_retriever import VectorRetriever
import re

class HybridRetriever:
    def __init__(self, db_path, qdrant_url, qdrant_api_key, qdrant_collection):
        self.structured = StructuredRetriever(db_path)
        self.vector = VectorRetriever(qdrant_url, qdrant_api_key, qdrant_collection)

    def classify_question(self, question):
        """
        Simple heuristic:
        - If question contains keywords related to numeric data, classify as 'numeric'
        - If question contains keywords related to narrative/unstructured, classify as 'narrative'
        - Else 'mixed'
        """
        numeric_keywords = [
            "revenue", "income", "assets", "liabilities", "equity", 
            "cash", "eps", "cost", "margin", "operating", "finance"
        ]
        narrative_keywords = [
            "management discussion", "strategy", "risk", "product", "overview",
            "discussion", "governance", "sustainability"
        ]

        question_lower = question.lower()
        num_hits = sum(kw in question_lower for kw in numeric_keywords)
        nar_hits = sum(kw in question_lower for kw in narrative_keywords)

        if num_hits > 0 and nar_hits == 0:
            return "numeric"
        elif nar_hits > 0 and num_hits == 0:
            return "narrative"
        else:
            return "mixed"

    def retrieve(self, question):
        category = self.classify_question(question)

        if category == "numeric":
            # Structured only
            df = self.structured.retrieve(question)
            return {"type": "numeric", "data": df}

        elif category == "narrative":
            # Vector only
            contexts = self.vector.retrieve(question)
            return {"type": "narrative", "data": contexts}

        else:
            # Mixed: combine both
            df = self.structured.retrieve(question)
            contexts = self.vector.retrieve(question)
            return {"type": "mixed", "numeric": df, "narrative": contexts}
