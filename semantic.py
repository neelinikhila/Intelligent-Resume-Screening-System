from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load AI Model (loads only once)
model = SentenceTransformer("all-MiniLM-L6-v2")


class SemanticMatcher:

    def __init__(self):
        self.model = model

    def get_embedding(self, text):

        if text is None:
            text = ""

        text = str(text).strip()

        embedding = self.model.encode(
            text,
            convert_to_numpy=True
        )

        return embedding
    def semantic_similarity(
        self,
        resume_text,
        job_description
    ):

        resume_embedding = self.get_embedding(
            resume_text
        )

        job_embedding = self.get_embedding(
            job_description
        )

        similarity = cosine_similarity(
            [resume_embedding],
            [job_embedding]
        )[0][0]

        similarity = max(0, similarity)

        similarity_percentage = round(
            similarity * 100,
            2
        )

        return similarity_percentage
    def analyze(
        self,
        resume_text,
        job_description
    ):

        semantic_score = self.semantic_similarity(
            resume_text,
            job_description
        )

        if semantic_score >= 90:

            recommendation = "Excellent Match"

        elif semantic_score >= 75:

            recommendation = "Strong Match"

        elif semantic_score >= 60:

            recommendation = "Good Match"

        elif semantic_score >= 40:

            recommendation = "Average Match"

        else:

            recommendation = "Poor Match"

        return {

            "semantic_score": semantic_score,

            "recommendation": recommendation

        }


# Create object

semantic_matcher = SemanticMatcher()