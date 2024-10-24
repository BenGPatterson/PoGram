# -*- coding: utf-8 -*-

import tkinter as tk

# Wrapper to tk.Entry to allow polish characters
class Entry_pl(tk.Entry):
    def __init__(self, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)

        # Polish character shortcuts
        self.pl_char_dict = {'ą': [17, 18, 81], 'ć': [17, 18, 67], 'ę': [17, 18, 69], 'ł': [17, 18, 76], 'ń': [17, 18, 78], 
                        'ó': [17, 18, 80], 'ś': [17, 18, 68], 'ź': [17, 18, 90], 'ż': [17, 18, 88]}
        self.history = []
        self.setup_pl_chars(self)

    # Keeps track of pressed keys
    def keyup(self, e):
        if  e.keycode in self.history :
            self.history.pop(self.history.index(e.keycode))
    def keydown(self, e):
        if not e.keycode in self.history :
            self.history.append(e.keycode)

    # Replaces old character with polish character
    def on_key_press(self, e):
        for pl_char, pl_code in self.pl_char_dict.items():
            if set(pl_code).issubset(set(self.history)):
                e.widget.insert('insert', e.char[:-1] + pl_char)
                return 'break'

    # Adds polish character functionality to entry widget
    def setup_pl_chars(self, widget):
        widget.bind('<KeyPress>', self.keydown, add='+')
        widget.bind('<KeyRelease>', self.keyup, add='+')
        widget.bind('<KeyPress>', self.on_key_press, add='+')

# Check/Radio button with entry field to right
class Entrybutton(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop('text', None)
        self.textvariable = kwargs.pop('textvariable', None)
        self.btn_type = kwargs.pop('btn_type', 'check')
        self.variable = kwargs.pop('variable', None)
        self.value = kwargs.pop('value', None)
        self.e_width = kwargs.pop('e_width', None)
        self.e_allow = kwargs.pop('e_allow', self.e_width)
        self.justify = kwargs.pop('justify', 'left')
        self.int_only = kwargs.pop('int_only', False)
        self.bounded = kwargs.pop('bounded', False)
        self.bg = kwargs.get('bg', None)
        tk.Frame.__init__(self, *args, **kwargs)

        # Apply optional restictions on Entry widget
        validate_fn = lambda *args, i=self.int_only, b=self.bounded, e=self.e_allow: validate(*args, i, b, e)
        self.vcmd = (self.register(validate_fn), '%d', '%P')

        # Load Check/Radio button and entry widgets
        self.get_entry()
        self.get_button()
        self.btn.pack(side=tk.LEFT)
        self.entry.pack(side=tk.LEFT)
        
    # Loads Check/Radio/Label button
    def get_button(self):
        if self.btn_type == 'radio':
            self.btn = tk.Radiobutton(self, variable=self.variable, value=self.value, text=self.text, bg=self.bg, 
                                      activebackground=self.bg)
        elif self.btn_type == 'check':
            self.btn = tk.Checkbutton(self, variable=self.variable, onvalue=1, offvalue=0, text=self.text,
                       bg=self.bg, activebackground=self.bg)
            self.value = 1
        elif self.btn_type == 'label':
            self.btn = tk.Label(self, text=self.text, bg=self.bg)
            return
        self.variable.trace_add('write', lambda *args, v=[self.variable], t=[[self.value]], e=[self.entry]: show_widget(v,t,e))

    # Loads Entry widget
    def get_entry(self):
        self.entry = Entry_pl(self, textvariable=self.textvariable, width=self.e_width, justify=self.justify, 
                              bg='SystemWindow', disabledbackground=self.bg, validate='key', validatecommand=self.vcmd)
    
    # Expands configure() functionality to these widgets
    def configure(self, *args, **kwargs):

        # Configure individual widgets, filtering incompatible kwargs
        self.btn.configure(*args, **kwargs)
        kwargs.pop('command', None)
        self.entry.configure(*args, **kwargs)
        self.entry.configure(bg='SystemWindow')

        # Call parent configure()
        tk.Frame.configure(self, *args, **kwargs)

    # Override widget type
    def winfo_class(self):
        return 'Entrybutton'
    
    # Bind to specified widget
    def bind(self, *args, **kwargs):
        target_widget = kwargs.pop('target_widget')
        if target_widget.lower() == 'btn':
            self.btn.bind(*args, **kwargs)
        elif target_widget.lower() == 'entry':
            self.entry.bind(*args, **kwargs)

    # Access input from Entry widget
    def get(self, *args, **kwargs):
        return self.entry.get()
    
# Create line border for homepage
class Lineborder(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, bg='black', height=1, bd=0, **kwargs)

    # Ensure parameters we set never change
    def configure(self, *args, **kwargs):
        tk.Frame.configure(self, *args, **kwargs)
        tk.Frame.configure(self, bg='black', height=1, bd=0)

# Apply requested restrictions on Entry widget
def validate(action, value_if_allowed, int_only, bounded, e_allow):

    # Ensures only integers
    if int_only and action=='1':
        if value_if_allowed:
            try:
                float(value_if_allowed)
            except ValueError:
                return False
        else:
            return False
        
    # Ensures text stays within bounds
    if bounded:
        if len(value_if_allowed) > e_allow:
            return False
    
    return True

# A scrollbar that hides itself if it's not needed.
class AutoScrollbar(tk.Scrollbar):
    def set(self, lo, hi, fakescrollbar):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
            fakescrollbar.tk.call("grid", "remove", fakescrollbar)
            self.active = 0
        else:
            self.grid()
            fakescrollbar.grid()
            self.active = 1
        tk.Scrollbar.set(self, lo, hi)

# Creates frame with scrollbar
class Scrollable(tk.Frame):
    def __init__(self, frame, width=16):

        # Grid weights
        frame.grid_columnconfigure(0, weight=0, pad=width)
        frame.grid_columnconfigure(1, weight=1)

        # Scroll bar
        self.scrollbar = AutoScrollbar(frame, width=width)
        self.scrollbar.grid(row=0, column=2, sticky='ns')

        # Ensures canvas is centred
        fakescrollbar = tk.Frame(frame, width=0)
        fakescrollbar.grid(row=0, column=0, sticky='ns')

        # Create canvas and bind scroll bar to it
        self.canvas = tk.Canvas(frame, yscrollcommand=lambda *args, fs=fakescrollbar: self.scrollbar.set(*args, fs))
        self.canvas.grid(row=0, column=1, sticky='nsew')
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.bind('<Configure>', self.__fill_canvas)

        # Base class initialization
        tk.Frame.__init__(self, frame)

        # Assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)

        # Binds scroll on mousewheel
        self.bind('<Enter>', self._bound_to_mousewheel)
        self.bind('<Leave>', self._unbound_to_mousewheel)

    # Enlarge the windows item to the canvas width
    def __fill_canvas(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width=canvas_width)

    # Binds mousewheel to scroll when hovering over
    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    # Uninds mousewheel from scroll when mo longer hovering over
    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    # Scroll frame with mousewheel
    def _on_mousewheel(self, event):
        if self.scrollbar.active:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Update the canvas and the scrollregion
    def update(self):
        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))
        self.canvas.yview_moveto(1)

# Enables/disables widget
def show_widget(vars, onvalues, widgets):
    var_gets = []
    for var in vars:
        var_gets.append(var.get())
    if var_gets in onvalues:
        state='normal'
    else:
        state='disabled'
    for widget in widgets:
         widget.configure(state=state)