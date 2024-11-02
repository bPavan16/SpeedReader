# pdf_loader.py

import re
from PyPDF2 import PdfReader


class PDFLoader:
    def __init__(self):
        self.pdf_text = []

    def load_pdf(self, filepath):
        with open(filepath, "rb") as file:
            reader = PdfReader(file)
            self.pdf_text = [page.extract_text().split() for page in reader.pages]
        return self.pdf_text


"""

    def load_pdf(self, filepath):
        with open(filepath, "rb") as file:
            reader = PdfReader(file)
            self.pdf_text = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    # Split text into paragraphs by detecting new lines or consecutive spaces
                    paragraphs = re.split(r"\n+", text.strip())
                    # Normalize whitespace
                    paragraphs = [
                        re.sub(r"\s+", " ", para).strip() for para in paragraphs
                    ]
                    self.pdf_text.append(paragraphs)
        return self.pdf_text
    

"""
