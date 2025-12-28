# Hybrid ML + Rule-Based Intent Agent

Production-grade intent classification system for omnichannel retail conversational interface.


## Business Context (ABFRL Retail Use Case)

This Intent Agent serves as the first decision layer in an omnichannel conversational sales system for ABFRL (Aditya Birla Fashion and Retail). The system processes natural language queries from customers across multiple channels (web, mobile app, chatbot) to understand purchase intent, enabling:

- Higher Average Order Value (AOV) through intelligent recommendations
- Improved conversion rates via intent-aware product suggestions
- Augmentation of human sales associates with AI-powered insights


## Why a Hybrid ML + Rule-Based System

**Pure Rule-Based Approach:**
- Pros: Deterministic, interpretable, no training data required
- Cons: Brittle, requires extensive manual maintenance, limited to known patterns

**Pure ML Approach:**
- Pros: Handles unseen patterns, adapts to language variations
- Cons: Requires large datasets, potential for catastrophic failures, black box behavior

**Hybrid Approach:**
- ML-first intent classification with rule-based fallback for robustness
- Maintains interpretability while leveraging ML capabilities
- Provides graceful degradation when ML model fails


## Capabilities & Example Output

**Input:** "show me smartphones under 15000 for gaming"
**Output:** `{"intent": "browse", "category": "electronics", "budget": 15000}`

**Supported Intent Labels:**
- browse: User is exploring products
- purchase: User wants to buy or place an order
- compare: User wants to compare products
- reserve: User wants to hold or reserve an item
- support: User needs help or has an issue


## System Architecture

```
User Query (text) → ML Intent Classifier (DistilBERT) → [Success: Return Intent]
                                                    → [Failure: Rule-Based Fallback]
                                                        ↓
Category Extraction (Rule-Based) ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
                                                        ↓
Budget Extraction (Rule-Based) ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
                                                        ↓
Structured JSON Output
```


## Project Structure

```
intent_agent/
├── data/
│   └── intent_dataset.csv          # Training dataset with text-label pairs
├── ml/
│   ├── infer.py                    # ML model inference wrapper
│   ├── train.py                    # Model training pipeline
│   ├── intent_dataset.py           # Dataset class for PyTorch
│   ├── tokenizer_utils.py          # DistilBERT tokenizer wrapper
│   ├── label_encoder.py            # Label encoding utilities
│   └── inspect_dataset.py          # Dataset validation utilities
├── models/intent_classifier/       # Trained model artifacts (not committed)
│   ├── config.json
│   ├── model.safetensors
│   ├── tokenizer.json
│   └── vocab.txt
├── rules/
│   ├── intent_rules.py             # Rule-based intent fallback
│   ├── category.py                 # Rule-based category extraction
│   ├── budget.py                   # Rule-based budget extraction
│   └── rule_extractor.py           # Combined rule-based extractor
├── parser.py                       # Main entry point and orchestrator
└── README.md                     # This file
```


## Machine Learning Details

**Model:** DistilBERT (66% faster than BERT, 60% smaller, maintains 95% performance)
**Framework:** PyTorch + HuggingFace Transformers
**Training:** Transfer learning on custom intent dataset

**Why DistilBERT:**
- Optimal balance between performance and inference speed
- Production-ready with excellent HuggingFace ecosystem support
- Sufficient for intent classification task with limited training data

**Dataset Size:** 25 training samples (learning-focused with extensibility in mind)


## Rule-Based Components

**Intent Fallback:** Keyword matching against predefined intent patterns
**Category Extraction:** Text matching against product category keywords
**Budget Extraction:** Regex pattern matching for monetary amounts


## How to Run

```bash
# From the project root directory
python -m intent_agent.parser

# Example output:
# {'intent': 'purchase', 'category': 'electronics', 'budget': 15000}
```

For interactive usage:

```python
from intent_agent.parser import parse_user_query

result = parse_user_query("I want to buy a phone under 20000")
print(result)  # {'intent': 'purchase', 'category': 'electronics', 'budget': 20000}
```


## Model Artifact & Git Strategy

Trained model artifacts are stored locally in `models/intent_classifier/` and intentionally excluded from Git via `.gitignore`.

**Reasons for this approach:**
- Model files are large and change frequently during training
- Git is not designed for binary file versioning
- Production deployments use model registries or artifact stores
- Maintains repository size and cloning speed


## Integration Strategy

This Intent Agent is designed for:

- **API Wrapping:** Integration with FastAPI for REST endpoint exposure
- **Backend Consumption:** Callable by backend services for intent resolution
- **LangChain Orchestration:** Will serve as first decision layer in agentic workflow
- **Scalable Deployment:** Containerizable for Kubernetes orchestration


## Role in the Larger Agentic AI System

This agent functions as the "first decision layer" in the agentic AI system:

1. User query enters the system
2. Intent Agent determines user intent and extracts structured data
3. Downstream worker agents (product search, recommendation, support) execute based on intent
4. Response is aggregated and presented to the user


## Future Improvements

- **Confidence Thresholding:** Add confidence scores with configurable fallback thresholds
- **Evaluation Metrics:** Implement precision, recall, and F1-score calculations
- **Dataset Expansion:** Collect and label more training data for improved performance
- **API Deployment:** Containerize with Docker and deploy to cloud platform
- **Monitoring:** Add logging and performance tracking


## Author / Learning Notes

This project was built as a self-learning, placement-oriented ML engineering exercise. The focus was on depth over breadth, emphasizing engineering discipline and production thinking rather than taking shortcuts. The goal was to demonstrate practical understanding of ML system architecture, not just model training.