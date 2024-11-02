# reader.py

import time
import threading

class PDFReader:
    def __init__(self):
        self.page_index = 0
        self.word_index = 0
        self.wpm = 200  # Default words per minute
        self.is_reading = False

    def start_reading(self, pdf_text):
        if not pdf_text:
            return None

        words_per_second = self.wpm / 60
        delay = 1 / words_per_second

        while self.is_reading and self.page_index < len(pdf_text):
            if self.word_index < len(pdf_text[self.page_index]):
                word = pdf_text[self.page_index][self.word_index]
                self.word_index += 1
                time.sleep(delay)
                yield word
            else:
                self.is_reading = False
                self.word_index = 0

    def next_page(self):
        self.page_index += 1
        self.word_index = 0

    def prev_page(self):
        self.page_index -= 1
        self.word_index = 0

    def go_to_page(self, page_number):
        self.page_index = page_number
        self.word_index = 0
