import tkinter as tk
from pl_chars import Entry_pl

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
        tframe_4 = tk.Frame(self, bg='grey')
        tframe_4.grid(row=1, column=3, padx=10, pady=(10, 20), sticky='nsew')
        menu_frame = tk.Frame(self, bg='grey')
        menu_frame.grid(row=1, column=4, padx=10, pady=(10, 20), sticky='nsew')

        # Load trainer and menu frames
        self.load_adj_frame(tframe_3)

    # Loads frame for adjective trainer
    def load_adj_frame(self, frame):

            # Toggle and title
            frame.grid_columnconfigure((0,1,2,3), weight=1, uniform='column')
            self.adj_active = tk.IntVar()
            toggle = tk.Checkbutton(frame, variable=self.adj_active, onvalue=1, offvalue=0, bg='grey', activebackground='grey')
            toggle.grid(row=0, column=0, columnspan=4)
            label = tk.Label(frame, text='Adjectives', bg='grey', font=('Segoe UI', 22))
            label.grid(row=1, column=0, columnspan=4)

            # Which questions
            q_line = tk.Frame(frame, bg='black', height=1, bd=0)
            q_line.grid(row=2, column=0, columnspan=4, sticky='ew')
            self.adj_qs = [tk.IntVar(), tk.IntVar()]
            definitions = tk.Checkbutton(frame, variable=self.adj_qs[0], onvalue=1, offvalue=0, text='Ask for definition', bg='grey', activebackground='grey')
            definitions.grid(row=3, column=0, columnspan=4, sticky='w')
            decl_frame = tk.Frame(frame, bg='grey')
            decl_frame.grid(row=4, column=0, columnspan=4, sticky='nsew')
            declensions_no = Entry_pl(decl_frame, width=2, justify='right')
            declensions_no.insert(tk.END, '1')
            declensions = tk.Checkbutton(decl_frame, variable=self.adj_qs[1], onvalue=1, offvalue=0, text='Ask declensions',
                                         bg='grey', activebackground='grey', command=lambda v=self.adj_qs[1], e=declensions_no: self.show_entry(v,e))
            declensions.pack(side=tk.LEFT)
            declensions_no.pack(side=tk.LEFT)

            # Which cases
            case_line = tk.Frame(frame, bg='black', height=1, bd=0)
            case_line.grid(row=5, column=0, columnspan=4, sticky='ew')
            self.adj_vn_only = tk.IntVar()
            vn_only = tk.Checkbutton(frame, variable=self.adj_vn_only, onvalue=1, offvalue=0, text='Virile nominative only', 
                                     bg='grey', activebackground='grey', command=lambda v=self.adj_vn_only: self.show_adj_cases(v))
            vn_only.grid(row=6, column=0, columnspan=4, sticky='w')
            self.adj_cases = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
            self.adj_case_btns = []
            for i, case in enumerate(['Nom.', 'Gen.', 'Dat.', 'Acc.', 'Ins.', 'Loc.', 'Voc.']):
                self.adj_case_btns.append(tk.Checkbutton(frame, variable=self.adj_cases[i], onvalue=1, offvalue=0, text=case, bg='grey', activebackground='grey'))
                self.adj_case_btns[-1].grid(row=7+int(i/2), column=i%2*2, columnspan=2, sticky='w')

            # Which word list
            word_line = tk.Frame(frame, bg='black', height=1, bd=0)
            word_line.grid(row=11, column=0, columnspan=4, sticky='ew')

    # Enables/disables entry widget
    def show_entry(self, var, widget):
        if var.get():
            print('disabling')
            widget.configure(state='disabled')
        else:
            print('enabling')
            widget.configure(state='normal')

    # Enables/disables adj case selection when virile nominative only selected
    def show_adj_cases(self, var):
        if var.get():
             state='disabled'
        else:
             state='normal'
        for i in range(7):
             self.adj_case_btns[i].configure(state=state)