from recommender import recommend_products

def main():
    #hardcoded test input
    category = "tech"
    max_price = 5000
    limit = 5
    
    recommended_products = recommend_products(category, max_price, limit)
    print(recommended_products)

    if not recommended_products:
        print("No products found")
        return
    
     
    for idx, product in enumerate(recommended_products, start=1):
        print(f"{idx}. {product['name']}")
        print(f"   Category: {product['category']}")
        print(f"   Price: ₹{product['price']}")
        print("-" * 30)


if __name__ == "__main__":
    main()

