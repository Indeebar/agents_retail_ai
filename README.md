# Retail AI Agents: Intent Classification & Product Recommendation System

A comprehensive AI-powered retail solution combining intent classification and product recommendation capabilities. This repository contains two complementary systems designed to work together as part of an intelligent retail conversational interface.

## 🏗️ System Architecture Overview

```
┌─────────────────┐    Intent & Structured Data     ┌──────────────────┐
│   User Query    │ ──────────────────────────────→ │ Intent Classifier│
│ (Natural Lang.) │                                   │   (Hybrid ML +   │
└─────────────────┘                                   │   Rule-Based)    │
       │                                              └──────────────────┘
       │                                                        │
       │ Structured Query & Intent                            API Call
       │                                                        │
       ▼                                                        ▼
┌─────────────────┐                                   ┌──────────────────┐
│ Recommendation  │ ←──────────────────────────────── │ Recommendation   │
│   Agent (RAG)   │    Filtered Product Data        │     System       │
└─────────────────┘                                   └──────────────────┘
       │                                                        │
       └───────────────── Aggregated Response ←────────────────┘
```

## 📦 Components

### 1. Intent Agent (`intent_agent/`)
A production-grade intent classification system that processes natural language queries to understand user purchase intent. The system combines machine learning with rule-based fallback for robustness.

**Key Features:**
- **Hybrid Architecture**: ML-first with rule-based fallback for reliability
- **Intent Classification**: Identifies browse, purchase, compare, reserve, and support intents
- **Entity Extraction**: Extracts category and budget information
- **Production Ready**: Designed for omnichannel retail deployment
- **Technology Stack**: DistilBERT, PyTorch, HuggingFace Transformers

**Example:**
- **Input**: "show me smartphones under 15000 for gaming"
- **Output**: `{"intent": "browse", "category": "electronics", "budget": 15000}`

### 2. Retail Recommendation Agent with RAG (`Recommendation-Agent-/`)
A Retrieval-Augmented Generation (RAG) system that provides personalized product recommendations using vector similarity search and LLM capabilities.

**Key Features:**
- **Synthetic Data Generation**: Creates realistic retail data including products, customers, inventory, and promotions
- **Vector Embeddings**: Uses sentence-transformers for product similarity matching
- **Vector Database**: Pinecone for efficient similarity search
- **Web Interface**: Streamlit app for interactive product recommendations
- **Filtering**: Price and category filters for refined searches
- **Technology Stack**: Pinecone, Sentence Transformers, Streamlit, Pandas

## 🎯 Business Value

This integrated system enables:
- **Higher Average Order Value (AOV)** through intelligent recommendations
- **Improved conversion rates** via intent-aware product suggestions
- **Enhanced customer experience** with personalized, context-aware responses
- **Scalable omnichannel support** across web, mobile, and chat interfaces
- **Augmentation of human sales associates** with AI-powered insights

## 🛠️ Technologies Used

### Intent Agent
- **ML Framework**: PyTorch + HuggingFace Transformers
- **Model**: DistilBERT (66% faster than BERT, 60% smaller, maintains 95% performance)
- **Architecture**: Hybrid ML + Rule-based system
- **Languages**: Python

### Recommendation Agent
- **Vector Database**: Pinecone
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **Web Interface**: Streamlit
- **Data Processing**: Pandas
- **LLM Integration**: Hugging Face (optional)
- **Languages**: Python, Jupyter Notebooks

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Indeebar/agents_retail_ai.git
cd agents_retail_ai
```

### 2. Set up Intent Agent
```bash
cd intent_agent
# Create virtual environment
python -m venv intent_env
source intent_env/bin/activate  # On Windows: intent_env\Scripts\activate

# Install dependencies
pip install torch transformers pandas numpy

# Run the intent classifier
python -m intent_agent.parser
```

### 3. Set up Recommendation Agent
```bash
cd ../Recommendation-Agent-
# Create virtual environment
python -m venv retail_rag_env
source retail_rag_env/bin/activate  # On Windows: retail_rag_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API keys in .env file:
# PINECONE_API_KEY=your_pinecone_api_key
# HUGGINGFACE_API_KEY=your_huggingface_api_key  # Optional for LLM features

# Run the Streamlit app
streamlit run app.py
```

## 📊 Workflow

### For End Users
1. User provides natural language query
2. Intent Agent processes query and extracts structured data (intent, category, budget)
3. Structured data is passed to Recommendation Agent
4. Recommendation Agent retrieves relevant products using vector search
5. Results are filtered and presented to the user

### For Developers
1. Intent Agent can be deployed as an API service
2. Recommendation Agent can be integrated via API or direct calls
3. Both systems can be orchestrated using LangChain or similar frameworks

## 🏁 Example Usage

**User Query**: "I want to buy a comfortable running shoe under 8000 for daily jogging"

**System Response Flow**:
1. Intent Agent: `{"intent": "purchase", "category": "footwear", "budget": 8000}`
2. Recommendation Agent: Returns top 5 running shoes matching criteria
3. User receives personalized recommendations with prices and features

## 📈 Integration Strategy

This system is designed for:
- **API Wrapping**: Integration with FastAPI for REST endpoint exposure
- **Backend Consumption**: Callable by backend services for intent resolution
- **LangChain Orchestration**: Serves as first decision layer in agentic workflow
- **Scalable Deployment**: Containerizable for Kubernetes orchestration
- **Omnichannel Support**: Integration with web, mobile, and chat interfaces

## 🚧 Future Improvements

- **Confidence Thresholding**: Add confidence scores with configurable fallback thresholds
- **Evaluation Metrics**: Implement precision, recall, and F1-score calculations
- **Dataset Expansion**: Collect and label more training data for improved performance
- **API Deployment**: Containerize with Docker and deploy to cloud platform
- **Monitoring**: Add logging and performance tracking
- **A/B Testing**: Framework for comparing model performance
- **Real-time Learning**: Feedback loop to improve recommendations over time

## 📁 Project Structure
```
agents_retail_ai/
├── intent_agent/                 # Intent classification system
│   ├── intent_agent/
│   │   ├── data/                # Training dataset
│   │   ├── ml/                  # ML training and inference
│   │   ├── models/              # Model artifacts (config only)
│   │   ├── rules/               # Rule-based fallback logic
│   │   └── parser.py            # Main orchestrator
│   └── .gitignore               # Git ignore for large model files
├── Recommendation-Agent-/       # RAG recommendation system
│   ├── app.py                   # Streamlit web interface
│   ├── 01_recommendation_agent_rag.ipynb  # Main RAG implementation
│   ├── pdf/                     # Generated retail data
│   └── requirements.txt         # Dependencies
├── .gitignore                   # Comprehensive ignore file
└── README.md                    # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 Business Context (ABFRL Retail Use Case)

This system was designed as a self-learning, placement-oriented ML engineering exercise for ABFRL (Aditya Birla Fashion and Retail). The focus was on depth over breadth, emphasizing engineering discipline and production thinking rather than taking shortcuts. The goal was to demonstrate practical understanding of ML system architecture and integration, not just individual model training.