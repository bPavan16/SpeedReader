# main.py

import tkinter as tk
from user_interface import SpeedreaderUI

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedreaderUI(root)
    root.mainloop()
