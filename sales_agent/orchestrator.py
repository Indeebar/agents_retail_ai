from typing import Optional

from sales_agent.contracts import (
    UserRequest,
    SalesContext,
    SalesResponse
)
from sales_agent.adapters import (
    adapt_intent_output,
    adapt_recommendation_output
)

# Import worker agents
from intent_agent.parser import parse_user_query
from recommendation_agent.recommender import recommend_products
from inventory_agent.checker import filter_in_stock_products
from pricing_agent.rules import apply_pricing_rules



def handle_user_query(query: str) -> SalesResponse:
    """
    Main entry point for Sales Agent.
    Orchestrates Intent and Recommendation agents.
    """

    if not query or not query.strip():
        return SalesResponse(
            success=False,
            message="Please provide a valid query"
        )

    user_request = UserRequest(query=query)

    
    # Step 1: Intent Extraction
    
    try:
        raw_intent_result = parse_user_query(user_request.query)
    except Exception:
        return SalesResponse(
            success=False,
            message="Failed to understand user intent"
        )

    intent_data = adapt_intent_output(raw_intent_result)

    intent: Optional[str] = intent_data.get("intent")
    category: Optional[str] = intent_data.get("category")
    budget: Optional[float] = intent_data.get("budget")
    is_product_seeking: bool = intent_data.get("is_product_seeking", False)

    # Only return error if not product-seeking
    if not is_product_seeking:
        return SalesResponse(
            success=False,
            message="Sorry, I can only help with product recommendations. Please ask about products you're interested in."
        )

    # If category is unknown, we can still try to provide general recommendations
    if not category or category == "unknown":
        category = None

    
    # Step 2: Recommendations
    
    try:
        raw_recommendations = recommend_products(
            category=category,
            max_price=budget
        )
    except Exception:
        raw_recommendations = []

    recommendations = adapt_recommendation_output(raw_recommendations)
    recommendations = filter_in_stock_products(recommendations)

    # Step 3: Pricing & Offers (INSERT HERE)
    recommendations = apply_pricing_rules(
        recommendations,
        budget=budget
    )

    
    # Step 4: Build Context
    
    context = SalesContext(
        intent=intent,
        category=category,
        budget=budget,
        recommendations=recommendations
    )

    
    # Step 5: Final Response
    
    return SalesResponse(
        success=True,
        message="Recommendations generated successfully",
        intent=context.intent,
        category=context.category,
        budget=context.budget,
        products=context.recommendations
    )
