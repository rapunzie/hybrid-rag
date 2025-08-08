import re

def classify_question(question: str) -> str:
    """
    Classify question into one of three types:
    - numeric_only: needs structured (SQL) data
    - narrative_only: needs unstructured (Qdrant) data
    - hybrid: needs both
    """
    q_lower = question.lower()

    # Kata kunci untuk numeric / structured
    numeric_keywords = [
        "revenue", "income", "earnings", "sales", "profit", "loss", "margin",
        "eps", "cost", "expenses", "operating income", "total assets",
        "total liabilities", "cash flow", "dividend", "growth"
    ]

    # Kata kunci untuk narrative / unstructured
    narrative_keywords = [
        "strategy", "plan", "risk", "market", "business model",
        "competitive", "management", "outlook", "product", "segment"
    ]

    has_numeric = any(re.search(rf"\b{k}\b", q_lower) for k in numeric_keywords)
    has_narrative = any(re.search(rf"\b{k}\b", q_lower) for k in narrative_keywords)

    # Aturan klasifikasi
    if has_numeric and has_narrative:
        return "hybrid"
    elif has_numeric:
        return "numeric_only"
    elif has_narrative:
        return "narrative_only"
    else:
        # Default → kita anggap narrative biar aman
        return "narrative_only"


# Contoh tes cepat
if __name__ == "__main__":
    test_questions = [
        "What is Apple's total revenue in 2023?",
        "Explain Apple's business strategy in 2023.",
        "How much was Apple's revenue in 2023 and why did it change?"
    ]
    for q in test_questions:
        print(q, "→", classify_question(q))
