import pandas as pd
from typing import List, Dict


class LabelEncoder:
    """
    Handles conversion between string labels and integer ids
    for intent classification.
    """

    def __init__(self, labels: List[str]):
        # Sort labels to ensure deterministic ordering
        unique_labels = sorted(set(labels))

        self.label_to_id: Dict[str, int] = {
            label: idx for idx, label in enumerate(unique_labels)
        }
        self.id_to_label: Dict[int, str] = {
            idx: label for label, idx in self.label_to_id.items()
        }

    def encode(self, labels: List[str]) -> List[int]:
        """Convert string labels to integer ids"""
        return [self.label_to_id[label] for label in labels]

    def decode(self, ids: List[int]) -> List[str]:
        """Convert integer ids back to string labels"""
        return [self.id_to_label[idx] for idx in ids]


def load_label_encoder(csv_path: str) -> LabelEncoder:
    """
    Utility function to create a LabelEncoder
    directly from the dataset.
    """
    df = pd.read_csv(csv_path)
    return LabelEncoder(df["label"].tolist())


if __name__ == "__main__":
    # Quick sanity test
    dataset_path = "../data/intent_dataset.csv"
    encoder = load_label_encoder(dataset_path)

    print("Label → ID mapping:")
    print(encoder.label_to_id)

    test_labels = ["browse", "purchase", "support"]
    encoded = encoder.encode(test_labels)
    decoded = encoder.decode(encoded)

    print("Test labels:", test_labels)
    print("Encoded:", encoded)
    print("Decoded:", decoded)
