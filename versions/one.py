import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PyPDF2 import PdfReader
import time
import threading
import os


class SpeedreaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speedreader App")

        # Set the initial size of the window
        self.root.geometry("1200x700")  # Width x Height
        self.root.configure(bg="#1e1e1e")  # Dark background

        # Initialize variables
        self.pdf_text = []
        self.page_index = 0
        self.word_index = 0
        self.wpm = 200  # default words per minute
        self.is_reading = False

        # Define theme colors and font
        self.bg_color = "#1e1e1e"
        self.text_color = "#ffffff"
        self.button_bg = "#333333"
        self.button_fg = "#ffffff"
        self.font_main = ("Arial", 14)
        self.font_large = ("Arial", 18, "bold")
        self.font_word_display = ("Arial", 32, "bold")
        self.font_pdf_display = (
            "Helvetica",
            18,
        )  # Using Helvetica for better text appearance

        # Main frames for layout
        self.control_frame = tk.Frame(root, width=400, bg=self.bg_color)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        self.display_frame = tk.Frame(root, bg=self.bg_color)
        self.display_frame.pack(
            side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20, pady=20
        )

        # Control elements in the left frame (centered alignment)
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
        self.wpm_entry.insert(0, str(self.wpm))
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
        self.text_display.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.text_display.config(state=tk.DISABLED)

    def upload_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filepath:
            # Display loading message
            self.loading_label.config(text="Loading PDF...")
            self.root.update_idletasks()  # Update GUI to show the message immediately

            try:
                with open(filepath, "rb") as file:
                    reader = PdfReader(file)
                    self.pdf_text = [
                        page.extract_text().split() for page in reader.pages
                    ]
                self.page_index = 0
                self.word_index = 0
                book_name = os.path.basename(filepath)
                self.loading_label.config(
                    text=f"Loaded: {book_name}"
                )  # Display book name
                self.update_page_display()
                self.update_page_label()
            except Exception as e:
                self.loading_label.config(text="")
                messagebox.showerror("Error", f"Failed to load PDF: {e}")

    def update_page_label(self):
        self.page_label.config(
            text=f"Page: {self.page_index + 1} of {len(self.pdf_text)}"
        )

    def update_page_display(self):
        if not self.pdf_text:
            return
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        page_text = " ".join(self.pdf_text[self.page_index])
        self.text_display.insert(tk.END, page_text)
        self.text_display.config(state=tk.DISABLED)

    def start_reading(self):
        try:
            self.wpm = int(self.wpm_entry.get())
            if self.wpm <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid positive integer for WPM."
            )
            return

        self.is_reading = True
        self.read_thread = threading.Thread(target=self.display_words)
        self.read_thread.start()

    def stop_reading(self):
        self.is_reading = False

    def display_words(self):
        if not self.pdf_text:
            messagebox.showerror("Error", "No PDF loaded.")
            return

        words_per_second = self.wpm / 60
        delay = 1 / words_per_second

        while self.is_reading and self.page_index < len(self.pdf_text):
            if self.word_index < len(self.pdf_text[self.page_index]):
                word = self.pdf_text[self.page_index][self.word_index]
                self.word_display.config(text=word)
                self.word_index += 1
                time.sleep(delay)
            else:
                self.is_reading = False
                self.word_index = 0

    def next_page(self):
        if self.page_index < len(self.pdf_text) - 1:
            self.page_index += 1
            self.word_index = 0
            self.update_page_display()
            self.update_page_label()
            self.word_display.config(text="")

    def prev_page(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.word_index = 0
            self.update_page_display()
            self.update_page_label()
            self.word_display.config(text="")

    def go_to_page(self):
        try:
            page_number = int(self.custom_page_entry.get()) - 1
            if 0 <= page_number < len(self.pdf_text):
                self.page_index = page_number
                self.word_index = 0
                self.update_page_display()
                self.update_page_label()
                self.word_display.config(text="")
            else:
                messagebox.showerror("Error", "Page number out of range.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid page number.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedreaderApp(root)
    root.mainloop()
