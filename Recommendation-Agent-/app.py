import streamlit as st
import pandas as pd
import os
import sys
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv

# ------------------ Setup ------------------
# Add notebook path (if needed)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()
pinecone_key = os.getenv("PINECONE_API_KEY")

# Check if Pinecone API key is available
if not pinecone_key:
    st.error("PINECONE_API_KEY environment variable is not set. Please set it to use the application.")
    st.stop()

# Initialize Pinecone client
try:
    pc = Pinecone(api_key=pinecone_key)
    index = pc.Index("test-index")  # Make sure this matches your actual index name
except Exception as e:
    st.error(f"Failed to initialize Pinecone: {str(e)}")
    st.stop()

# Load embedding model (same one you used in notebook)
try:
    embedding_model = SentenceTransformer(
        'sentence-transformers/all-MiniLM-L6-v2',
        device='cpu'  # force CPU to avoid meta tensor issue
    )
except Exception as e:
    st.error(f"Failed to load embedding model: {str(e)}")
    st.stop()

# Load product dataset for metadata fallback (optional)
try:
    products_df = pd.read_csv("pdf/synthetic_retail_data/products.csv")
except FileNotFoundError:
    st.error("Product data file not found. Please ensure 'pdf/synthetic_retail_data/products.csv' exists.")
    st.stop()
except Exception as e:
    st.error(f"Failed to load product data: {str(e)}")
    st.stop()

# ------------------ Helper Function ------------------
def retrieve_products(query, top_k=5, max_price=None, category=None):
    """Retrieve similar products from Pinecone."""
    if not query:
        return []
    
    query_embedding = embedding_model.encode(query).tolist()

    # Query Pinecone
    query_response = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    # Parse results
    results = []
    for match in query_response["matches"]:
        data = match["metadata"]
        data["similarity_score"] = match["score"]

        # Apply filters
        if max_price and float(data.get("price", 0)) > max_price:
            continue
        if category and category != "All" and data.get("category") != category:
            continue

        results.append(data)

    return results

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="Retail Recommendation Agent", page_icon="🛍️", layout="wide")

st.title("🛍️ Retail Recommendation Agent")
st.markdown("Enter your query below to get personalized product recommendations!")

query = st.text_input("What are you looking for today?", placeholder="e.g., black sneakers for college under 6000")
max_price = st.slider("Maximum price (INR)", 0, 20000, 15000, 500)
categories = ["All", "Footwear", "Apparel", "Accessories", "Tech", "Home"]
selected_category = st.selectbox("Category filter", categories)

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a query first.")
    else:
        st.info("🔍 Searching for the best matches...")
        results = retrieve_products(query, top_k=5, max_price=max_price, category=selected_category)

        if results:
            st.success(f"✅ Found {len(results)} matching products!")
            for i, product in enumerate(results):
                st.subheader(f"{i+1}. {product['title']}")
                col1, col2, col3 = st.columns(3)
                col1.metric("💰 Price", f"₹{product['price']}")
                col2.metric("⭐ Rating", product.get("rating", "N/A"))
                col3.metric("🧾 SKU", product["sku"])
                st.write(f"**Description:** {product['description']}")
                st.caption(f"Category: {product.get('category', 'N/A')} | Brand: {product.get('brand', 'N/A')}")
                st.write("---")
        else:
            st.warning("No products found matching your filters or query.")

# ------------------ Sidebar ------------------
st.sidebar.header("About this Demo")
st.sidebar.markdown("""
This app demonstrates a **Retrieval-Augmented Generation (RAG)** system using:
- 🧠 **Sentence Transformers** for embeddings
- 📦 **Pinecone** as vector database
- 💬 Optional Llama-2 for natural language recommendations

*(Backend uses your working notebook logic — this UI just interfaces with it.)*
""")

st.sidebar.header("How to Use")
st.sidebar.markdown("""
1. Enter a natural query like *"black sneakers under 6000"*
2. Adjust filters for price and category
3. View relevant products with similarity scores
""")
