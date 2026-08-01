class SectionParser:

    def __init__(self):

        self.sections = {
            "education": [
                "education",
                "academic",
                "qualification",
                "degree"
            ],

            "experience": [
                "experience",
                "work experience",
                "employment",
                "internship",
                "professional experience"
            ],

            "projects": [
                "projects",
                "project"
            ],

            "skills": [
                "skills",
                "technical skills",
                "key skills"
            ],

            "certifications": [
                "certifications",
                "certification",
                "certificate",
                "licenses"
            ],

            "achievements": [
                "achievements",
                "achievement",
                "awards"
            ],

            "languages": [
                "languages",
                "language"
            ]
        }

    def parse_sections(self, text):

        result = {
            "education": [],
            "experience": [],
            "projects": [],
            "skills": [],
            "certifications": [],
            "achievements": [],
            "languages": []
        }

        current_section = None

        lines = text.split("\n")

        for line in lines:

            clean_line = line.strip()

            if clean_line == "":
                continue

            lower_line = clean_line.lower()

            found = False

            for section, keywords in self.sections.items():

                if lower_line in keywords:

                    current_section = section
                    found = True
                    break

            if found:
                continue

            if current_section:

                result[current_section].append(clean_line)

        return result