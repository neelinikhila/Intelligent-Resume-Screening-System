from sentence_transformers import SentenceTransformer


class EmbeddingManager:

    def __init__(self):

        print("Loading Embedding Model...")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        print("Embedding Model Loaded Successfully")

    def get_embedding(self, text):

        if text is None:
            text = ""

        return self.model.encode(
            str(text),
            convert_to_numpy=True
        )

    def get_resume_embedding(self, resume_text):

        return self.get_embedding(resume_text)

    def get_job_embedding(self, job_description):

        return self.get_embedding(job_description)