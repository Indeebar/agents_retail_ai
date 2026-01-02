from recommender import recommend_products_ml


def main():
    query = "affordable wireless headphones for daily use"
    category = "tech"
    max_price = 5000
    limit = 5

    recommendations = recommend_products_ml(
        query=query,
        category=category,
        max_price=max_price,
        limit=limit
    )

    if not recommendations:
        print("No products found.")
        return

    print("\nML-Based Recommended Products:\n")

    for idx, product in enumerate(recommendations, start=1):
        print(f"{idx}. {product['name']}")
        print(f"   Category: {product['category']}")
        print(f"   Price: ₹{product['price']}")
        print("-" * 30)


if __name__ == "__main__":
    main()
