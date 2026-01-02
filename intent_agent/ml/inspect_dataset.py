import pandas as pd


def inspect_dataset(csv_path: str):
    """
    Loads the intent classification dataset and prints
    basic sanity checks:
    - first few rows
    - label distribution
    - unique labels
    """

    # Load dataset
    df = pd.read_csv(csv_path)

    # Print first 5 rows
    print("First 5 rows of dataset:")
    print(df.head(), end="\n\n")

    # Print label distribution
    print("Label distribution:")
    print(df["label"].value_counts(), end="\n\n")

    # Print unique labels
    print("Unique labels:")
    print(df["label"].unique())


if __name__ == "__main__":
    # Path is relative to this file (intent_agent/ml/)
    dataset_path = "../data/intent_dataset.csv"
    inspect_dataset(dataset_path)
