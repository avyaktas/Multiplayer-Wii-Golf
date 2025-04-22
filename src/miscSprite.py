import tkinter as tk
from tkinter import font

# Create a root window (it won't be displayed)
root = tk.Tk()

# Get the list of available fonts
available_fonts = list(font.families())

# Print the fonts
for f in available_fonts:
    print(f)

# Destroy the root window
root.destroy()