from dataclasses import dataclass
from typing import List, Optional, Dict


# Incoming user request

@dataclass
class UserRequest:
    query: str


# Internal sales context
# (after calling worker agents)

@dataclass
class SalesContext:
    intent: Optional[str]
    category: Optional[str]
    budget: Optional[float]
    recommendations: List[Dict]

# Final response to user
@dataclass
class SalesResponse:
    success: bool
    message: str
    intent: Optional[str] = None
    category: Optional[str] = None
    budget: Optional[float] = None
    products: Optional[List[Dict]] = None
