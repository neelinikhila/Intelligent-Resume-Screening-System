class Explainability:

    def generate(
        self,
        matched_skills,
        missing_skills,
        resume_score,
        semantic_score,
        ats_score,
        recommendation
    ):

        explanation = []

        if matched_skills:
            explanation.append(
                f"Matched Skills: {', '.join(matched_skills)}"
            )

        if missing_skills:
            explanation.append(
                f"Missing Skills: {', '.join(missing_skills)}"
            )

        explanation.append(
            f"Resume Score: {resume_score:.2f}%"
        )

        explanation.append(
            f"Semantic Score: {semantic_score:.2f}%"
        )

        explanation.append(
            f"ATS Score: {ats_score:.2f}%"
        )

        explanation.append(
            f"Recommendation: {recommendation}"
        )

        return explanation