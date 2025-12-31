from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    """
    This class is used to encode text into embeddings.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initializes the EmbeddingModel class.
        """
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        """
        Returns the embeddings for the given text.
        """
        return self.model.encode(texts, convert_to_tensor=True)
        