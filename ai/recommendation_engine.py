class RecommendationEngine:

    def recommend(self, ats_score):

        if ats_score >= 90:
            return "⭐⭐⭐⭐⭐ Highly Recommended"

        elif ats_score >= 80:
            return "⭐⭐⭐⭐ Strong Match"

        elif ats_score >= 70:
            return "⭐⭐⭐ Good Match"

        elif ats_score >= 60:
            return "⭐⭐ Average Match"

        else:
            return "❌ Not Recommended"