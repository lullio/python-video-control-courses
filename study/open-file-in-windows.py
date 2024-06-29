import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Oculta a janela principal

file_path = filedialog.askopenfilename(title="Select a file")
print(file_path)
