# RAG Recommendation System Flowchart

This diagram illustrates the complete workflow of the retail recommendation agent using Retrieval-Augmented Generation.

```mermaid
graph TD
    A[Start] --> B[Generate Synthetic Retail Data]
    B --> C[Load Product Data from CSV]
    C --> D[Create Text Embeddings<br/>Sentence Transformers]
    D --> E[Store Embeddings in Pinecone<br/>with Metadata]
    E --> F[User Enters Query in<br/>Streamlit Interface]
    F --> G[Generate Query Embedding]
    G --> H[Search Pinecone for<br/>Similar Product Vectors]
    H --> I[Retrieve Top-K Products<br/>with Metadata]
    I --> J{Apply Filters<br/>Price/Category}
    J -->|Filter Applied| K[Filtered Results]
    J -->|No Filter| L[All Results]
    K --> M[Display Results in<br/>Streamlit Interface]
    L --> M
    M --> N{Use LLM for<br/>Natural Language<br/>Recommendations?}
    N -->|Yes| O[Format Prompt with<br/>Retrieved Products]
    O --> P[Call Llama-2 via<br/>Hugging Face API]
    P --> Q[Generate Natural Language<br/>Recommendations]
    Q --> R[Display Enhanced<br/>Recommendations]
    N -->|No| S[Display Basic<br/>Recommendations]
    R --> T[End]
    S --> T

    style A fill:#f9f,stroke:#333
    style T fill:#f9f,stroke:#333
    style F fill:#bbf,stroke:#333
    style M fill:#bbf,stroke:#333
    style R fill:#bbf,stroke:#333
    style S fill:#bbf,stroke:#333
```

## Component Descriptions

1. **Data Generation**: Creates synthetic retail data including products, customers, inventory, and promotions
2. **Data Loading**: Reads product information from CSV files
3. **Embedding Creation**: Transforms product descriptions into vector representations
4. **Vector Storage**: Stores embeddings in Pinecone for efficient similarity search
5. **User Interface**: Streamlit web app for entering queries and displaying results
6. **Query Processing**: Converts user queries into embeddings for search
7. **Vector Search**: Finds similar products using cosine similarity
8. **Filtering**: Applies price and category filters to refine results
9. **LLM Enhancement**: (Optional) Uses Llama-2 to generate natural language recommendations
10. **Result Display**: Shows recommendations in the web interface

## Data Flow

```mermaid
graph LR
    A[Synthetic Data<br/>Generation] --> B[Product CSV<br/>Files]
    B --> C[Embedding<br/>Creation]
    C --> D[Pinecone<br/>Vector DB]
    E[User Query] --> F[Query<br/>Embedding]
    F --> D
    D --> G[Retrieved<br/>Products]
    G --> H[Streamlit<br/>Interface]
    H --> I[Displayed<br/>Results]
```