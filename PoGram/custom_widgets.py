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
        self.radio = kwargs.pop('radio', False)
        self.variable = kwargs.pop('variable', None)
        self.value = kwargs.pop('value', None)
        self.e_width = kwargs.pop('e_width', None)
        self.justify = kwargs.pop('justify', 'left')
        self.int_only = kwargs.pop('int_only', False)
        self.bounded = kwargs.pop('bounded', False)
        self.bg = kwargs.get('bg', None)
        tk.Frame.__init__(self, *args, **kwargs)

        # Apply optional restictions on Entry widget
        self.vcmd = (self.register(self.validate), '%d', '%P')

        # Load Check/Radio button and entry widgets
        self.get_entry()
        self.get_button()
        self.btn.pack(side=tk.LEFT)
        self.entry.pack(side=tk.LEFT)
        
    # Loads Check/Radio button
    def get_button(self):
        if self.radio:
            self.btn = tk.Radiobutton(self, variable=self.variable, value=self.value, text=self.text, bg=self.bg, 
                                      activebackground=self.bg)
        else:
            self.btn = tk.Checkbutton(self, variable=self.variable, onvalue=1, offvalue=0, text=self.text,
                       bg=self.bg, activebackground=self.bg)
            self.value = 1
        self.variable.trace_add('write', lambda *args, v=[self.variable], t=[[self.value]], e=[self.entry]: show_widget(v,t,e))

    # Loads Entry widget
    def get_entry(self):
        self.entry = Entry_pl(self, textvariable=self.textvariable, width=self.e_width, justify=self.justify, 
                              bg='SystemWindow', disabledbackground=self.bg, validate='key', validatecommand=self.vcmd)

    # Apply requested restrictions on Entry widget
    def validate(self, action, value_if_allowed):

        # Ensures only integers
        if self.int_only and action=='1':
            if value_if_allowed:
                try:
                    float(value_if_allowed)
                except ValueError:
                    return False
            else:
                return False
            
        # Ensures text stays within bounds
        if self.bounded:
            if len(value_if_allowed) > self.e_width:
                return False
        
        return True
    
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
