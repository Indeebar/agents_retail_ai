# Generated Retail Data for RAG Demo

This package contains synthetic retail data for demonstrating a Retrieval-Augmented Generation (RAG) recommendation agent.

## Contents

1. `products.csv` - 30 product entries with SKUs, descriptions, pricing, etc.
2. `customers.json` - 10 customer profiles with purchase histories
3. `inventory.json` - Stock levels across 5 stores and 1 warehouse
4. `promotions.json` - 3-5 promotional rules
5. `product_brochures/` - 6 PDF brochures with product information
6. `images/` - Placeholder PNG images used in the PDFs

## Ingestion Instructions

### Loading Products CSV with LangChain

```python
from langchain.document_loaders import CSVLoader

loader = CSVLoader(file_path='products.csv')
documents = loader.load()
```

### Loading Product Brochures with LangChain

```python
from langchain.document_loaders import PyPDFLoader
import os

# Load all PDFs in the brochures directory
brochure_docs = []
for filename in os.listdir('product_brochures'):
    if filename.endswith('.pdf'):
        loader = PyPDFLoader(os.path.join('product_brochures', filename))
        brochure_docs.extend(loader.load())
```

## Token Budget Tips

1. For large PDFs, consider splitting into smaller chunks (500-1000 tokens each)
2. Use only 1-2 product sections per retrieval context for the demo
3. The CSV and JSON files include metadata to support Pinecone filters (category, price, store_availability)

## Next Steps

1. Run embedding creation on loaded documents
2. Upsert embeddings into Pinecone vector database
3. Implement retrieval tests with various queries
