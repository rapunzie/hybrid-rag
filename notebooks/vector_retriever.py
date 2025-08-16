from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class VectorRetriever:
    def __init__(self, qdrant_url, qdrant_api_key, collection_name="annual_report"):
        self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        self.collection_name = collection_name
        self.model = SentenceTransformer("BAAI/bge-base-en-v1.5")

    def embed_query(self, query):
        return self.model.encode(query, normalize_embeddings=True)

    def retrieve(self, query, company=None, top_k=5):
        query_vector = self.embed_query(query)

        search_params = {
            "collection_name": self.collection_name,
            "query_vector": query_vector,
            "limit": top_k,
            "with_payload": True,
        }

        if company:
            search_params["query_filter"] = {
                "must": [
                    {"key": "company", "match": {"value": company.lower()}}
                ]
            }

        results = self.client.search(**search_params)

        contexts = []
        for res in results:
            payload = res.payload
            contexts.append({
                "score": res.score,
                "company": payload.get("company"),
                "section": payload.get("section"),
                "item": payload.get("item"),
                "text": payload.get("text")
            })

        return contexts
