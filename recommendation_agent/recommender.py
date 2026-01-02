_PRODUCT_EMBEDDINGS_CACHE = None
_PRODUCT_TEXTS_CACHE = None

import csv
from typing import List, Dict, Optional

from .filters import filter_by_category, filter_by_budget
from .ml.embedder import EmbeddingModel
from .ml.ranker import rank_products


import os

def load_products(csv_path: str) -> List[Dict]:
    products = []
    
    # Get the directory of this file and construct the path relative to it
    current_dir = os.path.dirname(__file__)
    full_path = os.path.join(current_dir, csv_path)

    with open(full_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append(row)

    return products



# v2: Deterministic recommender
def recommend_products(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    limit: int = 5
) -> List[Dict]:

    products = load_products("data/products.csv")
    products = filter_by_category(products, category)
    products = filter_by_budget(products, max_price)

    return products[:limit]



# v3: ML-based recommender

def recommend_products_ml(
    query: str,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    limit: int = 5
) -> List[Dict]:

    global _PRODUCT_EMBEDDINGS_CACHE, _PRODUCT_TEXTS_CACHE

    # Step 1: deterministic filtering (v2)
    products = load_products("data/products.csv")
    products = filter_by_category(products, category)
    products = filter_by_budget(products, max_price)

    if not products:
        return []

    # Step 2: ML embedding + ranking (v3)
    try:
        embedder = EmbeddingModel()

        product_texts = [
            f"{p.get('name', '')}. {p.get('description', '')}"
            for p in products
        ]

        # Cache product embeddings
        if (
            _PRODUCT_EMBEDDINGS_CACHE is None
            or _PRODUCT_TEXTS_CACHE != product_texts
        ):
            _PRODUCT_EMBEDDINGS_CACHE = embedder.encode(product_texts)
            _PRODUCT_TEXTS_CACHE = product_texts

        query_embedding = embedder.encode(query)
        product_embeddings = _PRODUCT_EMBEDDINGS_CACHE

        ranked_products = rank_products(
            query_embedding=query_embedding,
            product_embeddings=product_embeddings,
            products=products,
            top_k=limit
        )

        return ranked_products

    except Exception:
        # Graceful fallback to deterministic v2
        return products[:limit]


