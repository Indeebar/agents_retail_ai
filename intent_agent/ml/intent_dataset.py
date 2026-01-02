import pandas as pd
import torch
from torch.utils.data import Dataset

from tokenizer_utils import Tokenizer
from label_encoder import load_label_encoder


class IntentDataset(Dataset):
    """
    PyTorch Dataset for intent classification.
    Each item returns input_ids, attention_mask, and label.
    """

    def __init__(self, csv_path: str):
        # Load raw data
        df = pd.read_csv(csv_path)

        self.texts = df["text"].tolist()
        self.labels = df["label"].tolist()

        # Initialize helpers
        self.tokenizer = Tokenizer()
        self.label_encoder = load_label_encoder(csv_path)

        # Encode labels once
        self.encoded_labels = self.label_encoder.encode(self.labels)

        # Tokenize texts once
        self.encodings = self.tokenizer.tokenize(self.texts)

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings["input_ids"][idx],
            "attention_mask": self.encodings["attention_mask"][idx],
            "labels": torch.tensor(self.encoded_labels[idx], dtype=torch.long),
        }


if __name__ == "__main__":
    dataset = IntentDataset("../data/intent_dataset.csv")

    print("Total samples:", len(dataset))
    print("Sample item 0:")
    print(dataset[0])
