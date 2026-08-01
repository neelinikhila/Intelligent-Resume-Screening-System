import fitz
from docx import Document


class ResumeParser:

    def extract_text(self, file_path):

        text = ""

        if file_path.lower().endswith(".pdf"):

            pdf = fitz.open(file_path)

            for page in pdf:
                text += page.get_text()

            pdf.close()

        elif file_path.lower().endswith(".docx"):

            doc = Document(file_path)

            for para in doc.paragraphs:
                text += para.text + "\n"

        return text

    def extract_hyperlinks(self, file_path):

        links = []

        if file_path.lower().endswith(".pdf"):

            pdf = fitz.open(file_path)

            for page in pdf:

                page_links = page.get_links()

                for link in page_links:

                    if "uri" in link:

                        links.append(link["uri"])

            pdf.close()

        return links

    def parse_resume(self, file_path):

        text = self.extract_text(file_path)

        hyperlinks = self.extract_hyperlinks(file_path)

        return {
            "text": text,
            "hyperlinks": hyperlinks
        }