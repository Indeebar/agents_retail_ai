from sales_agent.orchestrator import handle_user_query
from inventory_agent.checker import store


def main():
    query = "I want a laptop under 60000"

    print("\nUser Query:")
    print(query)

    response = handle_user_query(query)

    print("\n--- FINAL RESPONSE ---")
    print(f"Success  : {response.success}")
    print(f"Message  : {response.message}")
    print(f"Intent   : {response.intent}")
    print(f"Category : {response.category}")
    print(f"Budget   : {response.budget}")
    print(f"Products : {response.products}")


if __name__ == "__main__":
    main()
