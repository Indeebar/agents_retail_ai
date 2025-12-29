import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

load_dotenv()

# ------------------ Internal State ------------------
_embedding_model = None
_index = None


# ------------------ Lazy Loaders ------------------
def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )
    return _embedding_model


def _get_pinecone_index():
    global _index

    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise RuntimeError("PINECONE_API_KEY is not set")

    if _index is None:
        pc = Pinecone(api_key=api_key)
        _index = pc.Index("test-index")

    return _index


# ------------------ Public API ------------------
def retrieve_products(query, top_k=5, max_price=None, category=None):
    """
    Core Recommendation Agent API.
    Returns a list of product dicts based on semantic similarity.
    """

    if not query:
        return []

    model = _get_embedding_model()
    index = _get_pinecone_index()

    query_embedding = model.encode(query).tolist()

    response = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    results = []
    for match in response.get("matches", []):
        data = match.get("metadata", {})

        if max_price and float(data.get("price", 0)) > max_price:
            continue
        if category and category != "All" and data.get("category") != category:
            continue

        results.append({
            "id": data.get("sku"),
            "name": data.get("title"),
            "price": data.get("price")
        })

    return results
