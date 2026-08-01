from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatcher:

    def __init__(self):
        self.model = None

    def get_embedding(self, text):

        if self.model is None:
            print("Loading AI Semantic Model...")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            print("AI Model Loaded Successfully")

        if text is None:
            text = ""

        return self.model.encode(
            str(text),
            convert_to_numpy=True
        )

    def semantic_similarity(
        self,
        resume_text,
        job_description
    ):

        resume_embedding = self.get_embedding(resume_text)
        job_embedding = self.get_embedding(job_description)

        similarity = cosine_similarity(
            [resume_embedding],
            [job_embedding]
        )[0][0]

        percentage = round(float(similarity * 100), 2)

        if percentage < 0:
            percentage = 0

        if percentage > 100:
            percentage = 100

        return percentage

    def recommendation(self, score):

        if score >= 90:
            return "⭐⭐⭐⭐⭐ Excellent Match"
        elif score >= 80:
            return "⭐⭐⭐⭐ Strong Match"
        elif score >= 70:
            return "⭐⭐⭐ Good Match"
        elif score >= 60:
            return "⭐⭐ Average Match"
        else:
            return "❌ Poor Match"

    def candidate_status(self, score):

        if score >= 85:
            return "Selected"
        elif score >= 70:
            return "Shortlisted"
        else:
            return "Rejected"