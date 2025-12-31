from sklearn.metrics.pairwise import cosine_similarity


def rank_products(
    query_embedding,
    product_embeddings,
    products,
    top_k=5
):
    """
    Rank products based on cosine similarity
    between query embedding and product embeddings.
    """

    similarities = cosine_similarity(
        query_embedding.reshape(1, -1),
        product_embeddings
    )[0]

    scored_products = list(zip(products, similarities))
    scored_products.sort(key=lambda x: x[1], reverse=True)

    return [product for product, _ in scored_products[:top_k]]
