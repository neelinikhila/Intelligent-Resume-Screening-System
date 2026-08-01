from transformers import pipeline

class SkillClassifier:

    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )

        self.skill_labels = [
            "Python",
            "Java",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "FastAPI",
            "Docker",
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "PostgreSQL",
            "Git",
            "Leadership",
            "Communication",
            "Teamwork"
        ]

    def extract_skills(self, text):

        result = self.classifier(
            text,
            self.skill_labels,
            multi_label=True
        )

        extracted = []

        for label, score in zip(result["labels"], result["scores"]):
            if score > 0.50:
                extracted.append(label)

        return extracted