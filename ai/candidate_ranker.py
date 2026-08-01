class CandidateRanker:

    def rank_candidates(self, resumes):

        ranked = sorted(
            resumes,
            key=lambda x: (
                x.semantic_score,
                x.ats_score
            ),
            reverse=True
        )

        rank = 1

        for candidate in ranked:

            candidate.rank = rank

            rank += 1

        return ranked