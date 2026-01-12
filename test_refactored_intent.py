from sales_agent.orchestrator import handle_user_query

# Test various queries to make sure they work regardless of intent label
test_queries = [
    # Original supported intents
    "show me phones",
    "I want to buy a laptop", 
    
    # Previously unsupported but product-related
    "compare phones",
    "hold this laptop for me",
    
    # Non-product related (should get error)
    "track my order",
    "where is my package",
    
    # Ambiguous but product-seeking
    "what's available in electronics",
    "show me good deals"
]

print("Testing refactored Intent Agent with various queries:\n")

for query in test_queries:
    print(f"Query: '{query}'")
    response = handle_user_query(query)
    print(f"  Success: {response.success}")
    print(f"  Message: {response.message}")
    print(f"  Intent: {response.intent}")
    print(f"  Category: {response.category}")
    print(f"  Budget: {response.budget}")
    print(f"  Products Count: {len(response.products) if response.products else 0}")
    print()

print("Refactored Intent Agent test completed!")