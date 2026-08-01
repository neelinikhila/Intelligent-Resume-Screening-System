class ResumeMatcher:

    def __init__(self):

        self.skills = [
            "Python",
            "Java",
            "HTML",
            "CSS",
            "JavaScript",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "Data Science",
            "Artificial Intelligence",
            "Git",
            "GitHub",
            "Flask",
            "FastAPI",
            "Django",
            "React",
            "MongoDB",
            "PostgreSQL",
            "MySQL",
            "Docker"
        ]

    # -----------------------------
    # Find Skills
    # -----------------------------

    def extract_skills(self, text):

        found_skills = []

        for skill in self.skills:

            if skill.lower() in text.lower():
                found_skills.append(skill)

        return found_skills

    # -----------------------------
    # Missing Skills
    # -----------------------------

    def missing_skills(self, found_skills):

        missing = []

        for skill in self.skills:

            if skill not in found_skills:
                missing.append(skill)

        return missing

    # -----------------------------
    # Resume Score
    # -----------------------------

    def resume_score(self, found_skills):

        total = len(self.skills)

        matched = len(found_skills)

        percentage = round(
            (matched / total) * 100,
            2
        )

        return matched, total, percentage

    # -----------------------------
    # Job Match
    # -----------------------------

    def job_match(
        self,
        found_skills,
        job_description
    ):

        jd_skills = []

        for skill in self.skills:

            if skill.lower() in job_description.lower():

                jd_skills.append(skill)

        matched = []

        for skill in jd_skills:

            if skill in found_skills:

                matched.append(skill)

        if len(jd_skills) == 0:

            percentage = 0

        else:

            percentage = round(
                (len(matched) / len(jd_skills)) * 100,
                2
            )

        return jd_skills, matched, percentage

    # -----------------------------
    # Candidate Status
    # -----------------------------

    def candidate_status(
        self,
        job_match_percentage
    ):

        if job_match_percentage >= 85:

            return "Selected"

        elif job_match_percentage >= 65:

            return "Shortlisted"

        else:

            return "Rejected"

    # -----------------------------
    # ATS Score
    # -----------------------------

    def ats_score(
        self,
        resume_percentage,
        job_match_percentage
    ):

        score = round(
            (resume_percentage * 0.4) +
            (job_match_percentage * 0.6),
            2
        )

        return score
    
    # -----------------------------
    # Recommendation
    # -----------------------------

    def recommendation(
        self,
        ats_score,
        semantic_score
    ):

        if ats_score >= 85 and semantic_score >= 85:
            return "⭐⭐⭐⭐⭐ Highly Recommended"

        elif ats_score >= 70 and semantic_score >= 70:
            return "⭐⭐⭐⭐ Recommended"

        elif ats_score >= 50:
            return "⭐⭐ Needs Improvement"

        else:
            return "❌ Not Recommended"