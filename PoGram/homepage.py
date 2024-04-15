import tkinter as tk
from custom_widgets import Entry_pl, Entrybutton, show_widget

# Home page showing trainer settings
class HomePage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        # Grid weights
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight = 1, uniform='column')

        # Title
        title = tk.Label(self, text='PoGram', font=('Segoe UI', 32))
        title.grid(row=0, column=0, columnspan=5, padx=10, pady=0, sticky='nw')
        
        # Create trainer and menu frames
        tframe_1 = tk.Frame(self, bg='grey')
        tframe_1.grid(row=1, column=0, padx=10, pady=(10, 20), sticky='nsew')
        tframe_2 = tk.Frame(self, bg='grey')
        tframe_2.grid(row=1, column=1, padx=10, pady=(10, 20), sticky='nsew')
        tframe_3 = tk.Frame(self, bg='grey')
        tframe_3.grid(row=1, column=2, padx=10, pady=(10, 20), sticky='nsew')
        tframe_4 = adj_trainer(self, bg='grey')
        tframe_4.grid(row=1, column=3, padx=10, pady=(10, 20), sticky='nsew')
        menu_frame = tk.Frame(self, bg='grey')
        menu_frame.grid(row=1, column=4, padx=10, pady=(10, 20), sticky='nsew')

        # Load trainer and menu frames
        self.load_adj_frame(tframe_3)

    # Loads frame for adjective trainer
    def load_adj_frame(self, frame):

            # Toggle and title
            frame.grid_columnconfigure((0,1), weight=1, uniform='column')
            self.adj_active = tk.IntVar()
            toggle = tk.Checkbutton(frame, variable=self.adj_active, onvalue=1, offvalue=0, bg='grey', activebackground='grey')
            toggle.grid(row=0, column=0, columnspan=2)
            label = tk.Label(frame, text='Adjectives', bg='grey', font=('Segoe UI', 22))
            label.grid(row=1, column=0, columnspan=2)

            # Which questions
            q_line = tk.Frame(frame, bg='black', height=1, bd=0)
            q_line.grid(row=2, column=0, columnspan=2, sticky='ew')
            self.adj_qs = [tk.IntVar(), tk.IntVar()]
            definitions = tk.Checkbutton(frame, variable=self.adj_qs[0], onvalue=1, offvalue=0, text='Ask for definition', bg='grey', activebackground='grey')
            definitions.grid(row=3, column=0, columnspan=2, sticky='w')
            declensions = Entrybutton(frame, variable=self.adj_qs[1], text='Ask declensions', e_width=2, justify='right', int_only=True, bounded=True, bg='grey')
            declensions.grid(row=4, column=0, columnspan=2, sticky='nsew')

            # Which cases
            case_line = tk.Frame(frame, bg='black', height=1, bd=0)
            case_line.grid(row=5, column=0, columnspan=2, sticky='ew')
            self.adj_vn_only = tk.IntVar()
            self.adj_cases = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
            adj_case_btns = []
            for i, case in enumerate(['Nom.', 'Gen.', 'Dat.', 'Acc.', 'Ins.', 'Loc.', 'Voc.']):
                adj_case_btns.append(tk.Checkbutton(frame, variable=self.adj_cases[i], onvalue=1, offvalue=0, text=case, bg='grey', activebackground='grey'))
                adj_case_btns[-1].grid(row=7+int(i/2), column=i%2, sticky='w')
            vn_only = tk.Checkbutton(frame, variable=self.adj_vn_only, onvalue=1, offvalue=0, text='Virile nominative only', 
                                     bg='grey', activebackground='grey', command=lambda v=self.adj_vn_only, e=adj_case_btns: show_widget(v, e))
            vn_only.grid(row=6, column=0, columnspan=2, sticky='w')

            # Which word list
            word_line = tk.Frame(frame, bg='black', height=1, bd=0)
            word_line.grid(row=11, column=0, columnspan=2, sticky='ew')

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
            var.trace_add('write', lambda *args, widget=widget: self.qn_check(widget, *args))

    # At least one question must be selected
    def qn_check(self, widget, var, index, mode):
        if self.qs[0].get() + self.qs[1].get() == 0:
            self.setvar(name=var, value=1)
            widget.configure(bg=widget.cget('bg'))
    
    # Load double columned list of settings
    def load_dcol(self, row):
        pass
         
    # Load word list settings
    def load_word_lists(self, row):
        pass
    
    # Draw horizontal line border at specified position
    def line_border(self, row):
        line = tk.Frame(self, bg='black', height=1, bd=0)
        line.grid(row=row, column=0, columnspan=2, sticky='ew')
    
class adj_trainer(trainer_frame):
    def __init__(self, *args, **kwargs):
        trainer_frame.__init__(self, *args, **kwargs)

        # Load widgets
        self.load_title(0, 'Adjectives')
        self.load_questions(3, 'declensions')
            
         