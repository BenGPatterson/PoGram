import tkinter as tk
from tkinter import filedialog
import os
from custom_widgets import Entrybutton, show_widget

# Home page showing trainer settings
class HomePage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        # Grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='column')

        # Title
        title = tk.Label(self, text='PoGram', font=('Segoe UI', 32))
        title.grid(row=0, column=0, columnspan=5, padx=10, pady=0, sticky='nw')
        
        # Create trainer and menu frames
        tframe_1 = adj_trainer(self, bg=self.cget('bg'))
        tframe_1.grid(row=1, column=0, padx=10, pady=(10, 20), sticky='nsew')
        tframe_2 = adj_trainer(self, bg=self.cget('bg'))
        tframe_2.grid(row=1, column=1, padx=10, pady=(10, 20), sticky='nsew')
        tframe_3 = adj_trainer(self, bg=self.cget('bg'))
        tframe_3.grid(row=1, column=2, padx=10, pady=(10, 20), sticky='nsew')
        tframe_4 = adj_trainer(self, bg=self.cget('bg'))
        tframe_4.grid(row=1, column=3, padx=10, pady=(10, 20), sticky='nsew')
        menu_frame = tk.Frame(self, bg=self.cget('bg'))
        menu_frame.grid(row=1, column=4, padx=10, pady=(10, 20), sticky='nsew')

# Parent class for trainer settings
class trainer_frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.bg = kwargs.get('bg', None)
        self.grid_columnconfigure((0,1), weight=1, uniform='column')

    # Load active toggle and title
    def load_title(self, row, text):
        self.active = tk.IntVar()
        toggle = tk.Checkbutton(self, variable=self.active, onvalue=1, offvalue=0, bg=self.bg, activebackground=self.bg)
        toggle.grid(row=row, column=0, columnspan=2)
        label = tk.Label(self, text=text, bg=self.bg, font=('Segoe UI', 22))
        label.grid(row=row+1, column=0, columnspan=2)
        self.line_border(row+2)

    # Load question settings
    def load_questions(self, row, inflection_type):

        # Load widgets
        self.qs = [tk.IntVar(), tk.IntVar()]
        definitions = tk.Checkbutton(self, variable=self.qs[0], onvalue=1, offvalue=0, text='Ask for definition',
                                     bg=self.bg, activebackground=self.bg)
        definitions.grid(row=row, column=0, columnspan=2, sticky='w')
        declensions = Entrybutton(self, variable=self.qs[1], text=f'Ask {inflection_type}', e_width=2, justify='right',
                                  int_only=True, bounded=True, bg=self.bg)
        declensions.grid(row=row+1, column=0, columnspan=2, sticky='nsew')
        self.line_border(row+2)

        # Ensure at least one is selected
        for var, widget in zip(self.qs, [definitions, declensions]):
            var.trace_add('write', lambda *args, w=widget: self.qn_check(w, *args))

    # At least one question must be selected
    def qn_check(self, widget, var, index, mode):
        if self.qs[0].get() + self.qs[1].get() == 0:
            self.setvar(name=var, value=1)
            widget.configure(bg=widget.cget('bg'))
    
    # Load double columned list of settings
    def load_dcol(self, row, texts, vars, return_btns=False):
        dcol_btns = []
        for i, case in enumerate(texts):
            dcol_btns.append(tk.Checkbutton(self, variable=vars[i], onvalue=1, offvalue=0, text=case, bg=self.bg, activebackground=self.bg))
            dcol_btns[-1].grid(row=row+int(i/2), column=i%2, sticky='w')
        self.line_border(row+int(i/2)+1)
        if return_btns:
            print(len(dcol_btns))
            return dcol_btns
         
    # Load word list settings
    def load_word_lists(self, row):
        self.grid_rowconfigure(row, weight=1)
        self.word_list = tk.StringVar(value='freq')
        word_list_all = tk.Radiobutton(self, text='All words', variable=self.word_list, 
                                        value='all', bg=self.bg, activebackground=self.bg)
        word_list_all.grid(row=row, column=0, columnspan=2, sticky='sw')
        word_list_freq = Entrybutton(self, text='Most frequent', variable=self.word_list, value='freq', radio=True,
                                     e_width=5, justify='right', int_only=True, bounded=True, bg=self.bg)
        word_list_freq.grid(row=row+1, column=0, columnspan=2, sticky='w')
        word_list_label = tk.Label(self, text='', font=('Segoe UI italic', 9), bg=self.bg)
        self.custom_list = None
        word_list_custom = tk.Radiobutton(self, text='Custom list', variable=self.word_list, value='custom', 
                                          bg=self.bg, activebackground=self.bg, command=lambda w=word_list_label: self.choose_word_list_custom(w))
        word_list_custom.grid(row=row+2, column=0, columnspan=2, pady=(0,20), sticky='w')
        word_list_label.place(in_=word_list_custom, relx=0, x=17, rely=1, y=-2)
    
    # Open file explorer to choose path to custom word list
    def choose_word_list_custom(self, widget):

        # Select path
        filename = filedialog.askopenfilename(initialdir='.', title='Select a File', filetypes=[('Comma-separated values files', '*.csv*')])

        # If path selected, update options to new path
        if filename != '':
            self.custom_list = filename
            short_path = os.path.split(filename)[-1]
            widget.configure(text=short_path)
        # If no path ever chosen, default back to frequency word list
        elif self.custom_list is None:
            self.word_list.set('freq')

    
    # Draw horizontal line border at specified position
    def line_border(self, row):
        line = tk.Frame(self, bg='black', height=1, bd=0)
        line.grid(row=row, column=0, columnspan=2, sticky='ew')

# Train adjectives  
class adj_trainer(trainer_frame):
    def __init__(self, *args, **kwargs):
        trainer_frame.__init__(self, *args, **kwargs)

        # Load title and question settings
        self.load_title(0, 'Adjectives')
        self.load_questions(3, 'declensions')

        # Load case settings
        cases = ['Nom.', 'Gen.', 'Dat.', 'Acc.', 'Ins.', 'Loc.', 'Voc.']
        self.case_vars = [tk.IntVar(), [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]]
        case_btns=self.load_dcol(7, cases, self.case_vars[1], return_btns=True)
        self.load_vn_only(6, self.case_vars[0], case_btns)

        # Load word lists
        self.load_word_lists(12)

    # Loads button to only train virile nominative declensions
    def load_vn_only(self, row, var, disable_widgets):
        vn_only = tk.Checkbutton(self, variable=var, onvalue=1, offvalue=0, text='Virile nominative only', 
                                     bg=self.bg, activebackground=self.bg, command=lambda v=var, t=0, e=disable_widgets: show_widget(v,t,e))
        vn_only.grid(row=row, column=0, columnspan=2, sticky='w')
         