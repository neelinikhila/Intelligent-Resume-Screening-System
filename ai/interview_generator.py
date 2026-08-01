import re

class InterviewGenerator:

    def generate_questions(self, resume_text):

        questions = []

        resume_text = resume_text.lower()

        skill_keywords = [
            "python",
            "java",
            "sql",
            "html",
            "css",
            "javascript",
            "react",
            "node",
            "fastapi",
            "flask",
            "django",
            "mysql",
            "mongodb",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "pandas",
            "numpy",
            "power bi",
            "excel",
            "data analytics",
            "aws",
            "git",
            "docker"
        ]

        found_skills = []

        for skill in skill_keywords:
            if re.search(r"\b" + re.escape(skill) + r"\b", resume_text):
                found_skills.append(skill)

        for skill in found_skills[:5]:
            questions.append(
                f"Explain your experience with {skill}."
            )
            questions.append(
                f"What projects have you completed using {skill}?"
            )

        questions.append(
            "Tell me about yourself."
        )

        questions.append(
            "Why are you interested in this role?"
        )

        questions.append(
            "Explain one challenging project you worked on."
        )

        questions.append(
            "What are your strengths and weaknesses?"
        )

        return questions