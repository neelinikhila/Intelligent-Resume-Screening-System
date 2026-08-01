import re

class SkillExtractor:

    def __init__(self):

        self.skill_database = [

            "Python",
            "Java",
            "C",
            "C++",
            "SQL",
            "MySQL",
            "PostgreSQL",
            "MongoDB",

            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Angular",
            "Vue",
            "Bootstrap",

            "Flask",
            "FastAPI",
            "Django",

            "Git",
            "GitHub",
            "Docker",
            "Kubernetes",

            "Machine Learning",
            "Deep Learning",
            "Artificial Intelligence",
            "Data Science",
            "Data Analytics",

            "TensorFlow",
            "PyTorch",
            "Pandas",
            "NumPy",
            "Scikit-learn",

            "AWS",
            "Azure",
            "GCP",

            "Linux",
            "REST API",
            "JSON",
            "Node.js"
        ]

    def extract_skills(self, text):

        found = []

        text = text.lower()

        for skill in self.skill_database:

            if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text):

                found.append(skill)

        return sorted(list(set(found)))

    def compare_skills(self, resume_text, job_description):

        candidate_skills = self.extract_skills(resume_text)

        required_skills = self.extract_skills(job_description)

        matched = []

        missing = []

        extra = []

        for skill in required_skills:

            if skill in candidate_skills:

                matched.append(skill)

            else:

                missing.append(skill)

        for skill in candidate_skills:

            if skill not in required_skills:

                extra.append(skill)

        if len(required_skills) == 0:

            match_percentage = 0

        else:

            match_percentage = round(
                (len(matched) / len(required_skills)) * 100,
                2
            )

        return {

            "required_skills": required_skills,

            "candidate_skills": candidate_skills,

            "matched_skills": matched,

            "missing_skills": missing,

            "extra_skills": extra,

            "match_percentage": match_percentage
        }