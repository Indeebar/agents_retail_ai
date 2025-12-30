import csv
from itertools import product
from typing import List, Dict,Optional

from filters import filter_by_category, filter_by_budget

def load_products(csv_path:str)-> List[Dict]:
  products=[]

  with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      products.append(row)

  return products


def recommend_products(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    limit: int = 5
 ) -> List[Dict]:
    products = load_products("recommendation_agent/data/products.csv")

    products = filter_by_category(products, category)
    products = filter_by_budget(products, max_price)

    return products[:limit]
