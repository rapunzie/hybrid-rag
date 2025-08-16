from structured_retriever import StructuredRetriever
from vector_retriever import VectorRetriever

class HybridRetriever:
    def __init__(self, db_path, qdrant_url, qdrant_api_key, qdrant_collection="annual_report"):
        self.structured = StructuredRetriever(db_path)
        self.vector = VectorRetriever(qdrant_url, qdrant_api_key, qdrant_collection)

    def classify_question(self, question):
        numeric_keywords = [
            "revenue", "income", "net income", "gross profit", "gross margin",
            "operating income", "assets", "liabilities", "equity", "cash",
            "eps", "basic", "diluted", "cost", "cost of sales",
            "investing", "financing", "dividends", "capex", "debt", "profit", "earnings", "expense"
        ]
        narrative_keywords = [
            "management discussion", "risk", "risk factors", "strategy", "plan",
            "product", "overview", "discussion", "governance", "sustainability",
            "board", "executive", "policy", "compliance",
            "operations", "performance", "market", "competition",
            "environment", "social", "human capital", "innovation"
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
        company = self.structured.extract_company(question)
        category = self.classify_question(question)

        if category == "numeric":
            df = self.structured.retrieve(question)
            return {"type": "numeric", "data": df}

        elif category == "narrative":
            contexts = self.vector.retrieve(question, company=company)
            return {"type": "narrative", "data": contexts}

        else:
            df = self.structured.retrieve(question)
            contexts = self.vector.retrieve(question, company=company)
            return {"type": "mixed", "numeric": df, "narrative": contexts}
