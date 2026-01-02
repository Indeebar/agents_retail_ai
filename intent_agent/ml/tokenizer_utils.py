from typing import List
from transformers import DistilBertTokenizerFast


class Tokenizer:
    """
    Wrapper around DistilBERT tokenizer for intent classification.
    """

    def __init__(self, model_name: str = "distilbert-base-uncased"):
        self.tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)

    def tokenize(self, texts: List[str], max_length: int = 32):
        """
        Tokenize a batch of texts.
        Returns input_ids and attention_mask.
        """
        return self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt"
        )


if __name__ == "__main__":
    # Sanity test
    tokenizer = Tokenizer()

    sample_texts = [
        "show me shoes under 5000",
        "i want to buy this shirt"
    ]

    encoded = tokenizer.tokenize(sample_texts)

    print("Input IDs shape:", encoded["input_ids"].shape)
    print("Attention mask shape:", encoded["attention_mask"].shape)
    print("Input IDs:", encoded["input_ids"])
