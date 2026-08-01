import re


class ResumeExtractor:

    def extract_candidate_details(self, text, hyperlinks):

        result = {}

        # -----------------------------
        # Candidate Name
        # -----------------------------

        candidate_name = "Not Found"

        for line in text.split("\n"):

            line = line.strip()

            if len(line) > 3 and len(line.split()) <= 4:

                candidate_name = line

                break

        result["candidate_name"] = candidate_name

        # -----------------------------
        # Email
        # -----------------------------

        email = "Not Found"

        email_match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        if email_match:

            email = email_match.group()

        result["email"] = email

        # -----------------------------
        # Phone
        # -----------------------------

        phone = "Not Found"

        phone_match = re.search(
            r"(\+91[- ]?)?[6-9]\d{9}",
            text
        )

        if phone_match:

            phone = phone_match.group()

        result["phone"] = phone

        # -----------------------------
        # LinkedIn
        # -----------------------------

        linkedin = "Not Found"

        for link in hyperlinks:
            if "linkedin.com" in link.lower():
                linkedin = link
                break

        if linkedin == "Not Found":
            linkedin_match = re.search(
                r"(https?://)?(www\.)?linkedin\.com/[^\s]+",
                text,
                re.IGNORECASE
            )

            if linkedin_match:
                linkedin = linkedin_match.group()

        result["linkedin"] = linkedin


        # -----------------------------
        # GitHub
        # -----------------------------

        github = "Not Found"

        for link in hyperlinks:
            if "github.com" in link.lower():
                github = link
                break

        if github == "Not Found":
            github_match = re.search(
                r"(https?://)?(www\.)?github\.com/[^\s]+",
                text,
                re.IGNORECASE
            )

            if github_match:
                github = github_match.group()

        result["github"] = github

        # -----------------------------
        # Portfolio
        # -----------------------------

        portfolio = "Not Found"

        for link in hyperlinks:

            if (
    "github.com" not in link.lower()
    and "linkedin.com" not in link.lower()
    and "mailto:" not in link.lower()
):
                portfolio = link

                break
 
        result["portfolio"] = portfolio

        return result