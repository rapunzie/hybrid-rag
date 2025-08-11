from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class VectorRetriever:
    def __init__(self, qdrant_url, qdrant_api_key, collection_name):
        self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        self.collection_name = collection_name
        # Load embedding model BGE
        self.model = SentenceTransformer("BAAI/bge-base-en-v1.5")

    def embed_query(self, query):
        return self.model.encode(query, normalize_embeddings=True)

    def retrieve(self, query, top_k=5):
        # Embed query
        query_vector = self.embed_query(query)

        # Search ke Qdrant
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
        )

        # Ambil hanya payload teks & metadata
        contexts = []
        for res in results:
            payload = res.payload
            contexts.append({
                "score": res.score,
                "section": payload.get("section"),
                "item": payload.get("item"),
                "text": payload.get("text")
            })

        return contexts
