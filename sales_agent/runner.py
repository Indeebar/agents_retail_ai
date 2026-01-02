from sales_agent.orchestrator import handle_user_query


if __name__ == "__main__":
    test_query = "I want a laptop under 60000"

    response = handle_user_query(test_query)

    print("\n--- SALES AGENT RESPONSE ---")
    print(f"Success   : {response.success}")
    print(f"Message   : {response.message}")
    print(f"Intent    : {response.intent}")
    print(f"Category  : {response.category}")
    print(f"Budget    : {response.budget}")
    print(f"Products  : {response.products}")
