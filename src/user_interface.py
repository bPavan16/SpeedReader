# ui.py

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pdf_loader import PDFLoader
from text_reader import PDFReader


class SpeedreaderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Speedreader App")

        # Set the initial size of the window
        self.root.geometry("1200x700")  # Width x Height
        self.root.configure(bg="#1e1e1e")  # Dark background

        # Initialize variables
        self.pdf_loader = PDFLoader()
        self.pdf_reader = PDFReader()
        self.loading_label = None

        # Define theme colors and font
        self.bg_color = "#1e1e1e"
        self.text_color = "#ffffff"
        self.button_bg = "#333333"
        self.button_fg = "#ffffff"
        self.font_main = ("Arial", 14)
        self.font_large = ("Arial", 18, "bold")
        self.font_word_display = ("Arial", 32, "bold")
        self.font_pdf_display = ("Helvetica", 18)

        # Main frames for layout
        self.control_frame = tk.Frame(root, width=400, bg=self.bg_color)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        self.display_frame = tk.Frame(root, bg=self.bg_color)
        self.display_frame.pack(
            side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20, pady=20
        )

        # Control elements in the left frame (centered alignment)
        self.create_controls()

    def create_controls(self):
        self.upload_button = tk.Button(
            self.control_frame,
            text="Upload PDF",
            command=self.upload_pdf,
            bg=self.button_bg,
            fg=self.button_fg,
            font=self.font_main,
            width=20,
        )
        self.upload_button.pack(pady=(0, 15), anchor="center")

        self.loading_label = tk.Label(
            self.control_frame,
            text="",
            fg="#66ff66",
            bg=self.bg_color,
            font=self.font_main,
        )
        self.loading_label.pack(anchor="center", pady=(0, 15))

        self.wpm_label = tk.Label(
            self.control_frame,
            text="Words per Minute:",
            fg=self.text_color,
            bg=self.bg_color,
            font=self.font_main,
        )
        self.wpm_label.pack(anchor="center")

        self.wpm_entry = tk.Entry(
            self.control_frame, justify="center", width=10, font=self.font_main
        )
        self.wpm_entry.insert(0, str(self.pdf_reader.wpm))
        self.wpm_entry.pack(pady=(0, 15), anchor="center")

        self.page_label = tk.Label(
            self.control_frame,
            text="Page: 0",
            fg=self.text_color,
            bg=self.bg_color,
            font=self.font_main,
        )
        self.page_label.pack(pady=(0, 15), anchor="center")

        self.word_display = tk.Label(
            self.control_frame,
            font=self.font_word_display,
            fg="#ffffff",
            bg=self.bg_color,
            wraplength=300,
            width=15,
        )
        self.word_display.pack(pady=(0, 20), anchor="center")

        self.start_button = tk.Button(
            self.control_frame,
            text="Start",
            command=self.start_reading,
            bg=self.button_bg,
            fg=self.button_fg,
            font=self.font_main,
            width=20,
        )
        self.start_button.pack(pady=(5, 10), anchor="center")

        self.stop_button = tk.Button(
            self.control_frame,
            text="Stop",
            command=self.stop_reading,
            bg=self.button_bg,
            fg=self.button_fg,
            font=self.font_main,
            width=20,
        )
        self.stop_button.pack(pady=(5, 20), anchor="center")

        self.next_page_button = tk.Button(
            self.control_frame,
            text="Next Page",
            command=self.next_page,
            bg=self.button_bg,
            fg=self.button_fg,
            font=self.font_main,
            width=20,
        )
        self.next_page_button.pack(pady=(5, 10), anchor="center")

        self.prev_page_button = tk.Button(
            self.control_frame,
            text="Previous Page",
            command=self.prev_page,
            bg=self.button_bg,
            fg=self.button_fg,
            font=self.font_main,
            width=20,
        )
        self.prev_page_button.pack(pady=(5, 10), anchor="center")

        # Custom Page Navigation
        self.custom_page_label = tk.Label(
            self.control_frame,
            text="Go to Page:",
            fg=self.text_color,
            bg=self.bg_color,
            font=self.font_main,
        )
        self.custom_page_label.pack(anchor="center")

        self.custom_page_entry = tk.Entry(
            self.control_frame, justify="center", width=10, font=self.font_main
        )
        self.custom_page_entry.pack(pady=(0, 10), anchor="center")

        self.go_to_page_button = tk.Button(
            self.control_frame,
            text="Go",
            command=self.go_to_page,
            bg=self.button_bg,
            fg=self.button_fg,
            font=self.font_main,
            width=20,
        )
        self.go_to_page_button.pack(pady=(5, 15), anchor="center")

        # PDF display area in the right frame
        self.text_display = scrolledtext.ScrolledText(
            self.display_frame,
            wrap=tk.WORD,
            height=25,
            width=80,
            font=self.font_pdf_display,
            bg="#262626",
            fg=self.text_color,
        )
        self.text_display.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.text_display.config(state=tk.DISABLED)

    def upload_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filepath:
            self.loading_label.config(text="Loading PDF...")
            self.root.update_idletasks()

            try:
                self.pdf_loader.load_pdf(filepath)
                self.pdf_reader.page_index = 0
                self.pdf_reader.word_index = 0
                book_name = os.path.basename(filepath)
                self.loading_label.config(text=f"Loaded: {book_name}")
                self.update_page_display()
                self.update_page_label()
            except Exception as e:
                self.loading_label.config(text="")
                messagebox.showerror("Error", f"Failed to load PDF: {e}")

    def update_page_label(self):
        self.page_label.config(
            text=f"Page: {self.pdf_reader.page_index + 1} of {len(self.pdf_loader.pdf_text)}"
        )

    def update_page_display(self):
        if not self.pdf_loader.pdf_text:
            return
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        page_text = " ".join(self.pdf_loader.pdf_text[self.pdf_reader.page_index])
        self.text_display.insert(tk.END, page_text)
        self.text_display.config(state=tk.DISABLED)

    """

    def update_page_display(self):
        if not self.pdf_loader.pdf_text:
            return
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        page_paragraphs = self.pdf_loader.pdf_text[self.pdf_reader.page_index]
        # Join paragraphs with two newlines for better visibility
        page_text = "\n\n".join(page_paragraphs)
        self.text_display.insert(tk.END, page_text)
        self.text_display.config(state=tk.DISABLED)
        
    """

    def start_reading(self):
        try:
            self.pdf_reader.wpm = int(self.wpm_entry.get())
            if self.pdf_reader.wpm <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid positive integer for WPM."
            )
            return

        self.pdf_reader.is_reading = True
        self.read_thread = threading.Thread(target=self.display_words)
        self.read_thread.start()

    def stop_reading(self):
        self.pdf_reader.is_reading = False

    def display_words(self):
        for word in self.pdf_reader.start_reading(self.pdf_loader.pdf_text):
            if not self.pdf_reader.is_reading:
                break
            self.word_display.config(text=word)

    def next_page(self):
        if self.pdf_reader.page_index < len(self.pdf_loader.pdf_text) - 1:
            self.pdf_reader.next_page()
            self.update_page_display()
            self.update_page_label()
            self.word_display.config(text="")

    def prev_page(self):
        if self.pdf_reader.page_index > 0:
            self.pdf_reader.prev_page()
            self.update_page_display()
            self.update_page_label()
            self.word_display.config(text="")

    def go_to_page(self):
        try:
            page_number = int(self.custom_page_entry.get()) - 1
            if 0 <= page_number < len(self.pdf_loader.pdf_text):
                self.pdf_reader.go_to_page(page_number)
                self.update_page_display()
                self.update_page_label()
                self.word_display.config(text="")
            else:
                messagebox.showerror("Error", "Page number out of range.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid page number.")
