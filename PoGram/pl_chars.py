import tkinter as tk

# Polish character shortcuts
pl_char_dict = {'ą': [17, 18, 81], 'ć': [17, 18, 67], 'ę': [17, 18, 69], 'ł': [17, 18, 76], 'ń': [17, 18, 78], 
                'ó': [17, 18, 80], 'ś': [17, 18, 68], 'ź': [17, 18, 90], 'ż': [17, 18, 88]}

# Keeps track of pressed keys
history = []
def keyup(e):
    if  e.keycode in history :
        history.pop(history.index(e.keycode))
def keydown(e):
    if not e.keycode in history :
        history.append(e.keycode)

# Replaces old character with polish character
def on_key_press(e):
    for pl_char, pl_code in pl_char_dict.items():
        if set(pl_code).issubset(set(history)):
            e.widget.insert('insert', e.char[:-1] + pl_char)
            return 'break'

# Adds polish character functionality to entry widget
def setup_pl_chars(widget):
    widget.bind('<KeyPress>', keydown, add='+')
    widget.bind('<KeyRelease>', keyup, add='+')
    widget.bind('<KeyPress>', on_key_press, add='+')

# Wrapper to tk.Entry to allow polish characters
class Entry_pl(tk.Entry):
    def __init__(self, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        setup_pl_chars(self)