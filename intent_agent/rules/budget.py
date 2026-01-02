import re

def extract_budget(text: str):
   text=text.lower()

   match = re.search(r'(\d+)\s*(k)?', text)

   if not match:
        return None

   amount = int(match.group(1))

   if match.group(2):
        amount = amount * 1000

   return amount