class ATSCalculator:

    def calculate(
        self,
        resume_score,
        semantic_score
    ):

        ats = (
            (resume_score * 0.40) +
            (semantic_score * 0.60)
        )

        return round(ats, 2)