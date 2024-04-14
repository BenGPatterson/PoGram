# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import font
from pl_chars import Entry_pl

# Create window
root = tk.Tk()
root.title("PoGram")
root.geometry('874x540')
 
# Add text
lbl = tk.Label(root, text="")
lbl.grid()

text_font = font.Font(family='Helvetica', size=12)

# adding Entry Field
txt = Entry_pl(root, font=text_font, width=10)
txt.grid(column=1, row=0)

# Changes text when clicked
def clicked():
    lbl.configure(text=f"You wrote: {txt.get()}")

# Add button
btn = tk.Button(root, text="Click me", fg="red", command=clicked)
btn.grid(column=2, row=0)

# Run application
root.mainloop()