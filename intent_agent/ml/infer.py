import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
from typing import List
import pandas as pd
from .label_encoder import load_label_encoder


class IntentClassifier:
    """
    Loads a trained DistilBERT model for intent classification.
    """
    
    def __init__(self, model_path: str, csv_path: str = None):
        """
        Initialize the classifier with a pre-trained model.
        
        Args:
            model_path: Path to the saved model directory
            csv_path: Path to the CSV file to load the label encoder (optional if not needed)
        """
        # Load the pre-trained model
        self.model = DistilBertForSequenceClassification.from_pretrained(model_path)
        
        # Load the tokenizer
        self.tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
        
        # Set device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        
        # Load label encoder if CSV path is provided
        if csv_path:
            df = pd.read_csv(csv_path)
            labels = df["label"].tolist()
            unique_labels = sorted(set(labels))
            self.label_to_id = {label: idx for idx, label in enumerate(unique_labels)}
            self.id_to_label = {idx: label for label, idx in self.label_to_id.items()}
        else:
            # Default label mapping - this should match your training labels
            self.label_to_id = {
                "browse": 0,
                "compare": 1,
                "purchase": 2,
                "reserve": 3,
                "support": 4
            }
            self.id_to_label = {v: k for k, v in self.label_to_id.items()}

    def predict(self, text: str) -> str:
        """
        Predict the intent for a given text.
        
        Args:
            text: Input text to classify
            
        Returns:
            Predicted intent label
        """
        # Tokenize the input text
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=32,
            return_tensors="pt"
        )
        
        # Move inputs to device
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class_id = torch.argmax(predictions, dim=-1).item()
        
        # Convert class ID back to label
        predicted_label = self.id_to_label.get(predicted_class_id, "unknown")
        return predicted_label

    def predict_batch(self, texts: List[str]) -> List[str]:
        """
        Predict intents for a batch of texts.
        
        Args:
            texts: List of input texts to classify
            
        Returns:
            List of predicted intent labels
        """
        # Tokenize the input texts
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=32,
            return_tensors="pt"
        )
        
        # Move inputs to device
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class_ids = torch.argmax(predictions, dim=-1).cpu().numpy()
        
        # Convert class IDs back to labels
        predicted_labels = [self.id_to_label.get(idx, "unknown") for idx in predicted_class_ids]
        return predicted_labels