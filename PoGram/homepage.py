import os
import json
import tkinter as tk
from tkinter import filedialog
from custom_widgets import Entrybutton, Lineborder, show_widget

# Home page showing trainer settings
class HomePage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        # Grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='column')

        # Title
        title = tk.Label(self, text='PoGram', font=('Segoe UI', 28))
        title.grid(row=0, column=0, columnspan=5, padx=10, pady=0, sticky='nw')
        
        # Create trainer and menu frames
        with open('trainer_config.json') as json_file:
            trainer_config = json.load(json_file)
        self.adj_frame = adj_trainer(self, bga='#ffb3ba', config=trainer_config['adj'])
        self.adj_frame.grid(row=1, column=0, padx=(10, 5), pady=(10, 20), sticky='nsew')
        self.noun_frame = trainer_frame(self, bga='#ffdfba', config=trainer_config['adj'])
        self.noun_frame.grid(row=1, column=1, padx=5, pady=(10, 20), sticky='nsew')
        self.verb_frame = trainer_frame(self, bga='#ffffba', config=trainer_config['adj'])
        self.verb_frame.grid(row=1, column=2, padx=5, pady=(10, 20), sticky='nsew')
        self.misc_frame = trainer_frame(self, bga='#baffc9', config=trainer_config['adj'])
        self.misc_frame.grid(row=1, column=3, padx=5, pady=(10, 20), sticky='nsew')
        menu_frame = menu_display(self, bga='#bae1ff')
        menu_frame.grid(row=1, column=4, padx=30, pady=(10, 50), sticky='nsew')

# Parent class for trainer settings
class trainer_frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop('config')
        self.bga = kwargs.pop('bga', None)
        tk.Frame.__init__(self, *args, **kwargs)
        self.bg = self.cget('bg')
        self.widget_status = self.config['widget_status']
        self.grid_columnconfigure((0,1), weight=1, uniform='column')

    # Load active toggle and title
    def load_title(self, row, text):
        self.active = tk.IntVar(value=self.config['active'])
        toggle = tk.Checkbutton(self, variable=self.active, onvalue=1, offvalue=0, bg=self.bg, activebackground=self.bg, 
                                command=self.toggle_active)
        toggle.grid(row=row, column=0, columnspan=2)
        label = tk.Label(self, text=text, bg=self.bg, font=('Segoe UI', 22))
        label.grid(row=row+1, column=0, columnspan=2)
        self.line_border(row+2)

    # Toggles active state of trainer
    def toggle_active(self, widget_status=None):
        self.toggle_status(widget_status=widget_status)
        self.toggle_colour()

    # Enables/disables widgets depending on active state of trainer
    def toggle_status(self, widget_status=None):

        # Turning on
        if self.active.get():
            for i, child in enumerate(self.winfo_children()):
                wtype = child.winfo_class()
                if wtype == 'Entrybutton':
                    for j, entrychild in enumerate(child.winfo_children()):
                        entrychild.configure(state=self.widget_status[i][j])
                elif wtype not in ('Frame','Labelframe','TFrame','TLabelframe') and i!=1:
                    child.configure(state=self.widget_status[i])

        # Turning off, saving current state
        else:
            if widget_status is None:
                self.get_widget_status()
            else:
                self.widget_status = widget_status
            for i, child in enumerate(self.winfo_children()):
                wtype = child.winfo_class()
                if wtype == 'Entrybutton':
                    for entrychild in child.winfo_children():
                        entrychild.configure(state='disable')
                elif wtype not in ('Frame','Labelframe','TFrame','TLabelframe') and i!=1:
                    child.configure(state='disable')

        # Ensure active toggle is always enabled
        self.winfo_children()[0].configure(state='normal')

    # Get status of all widgets
    def get_widget_status(self):
        self.widget_status = []
        for i, child in enumerate(self.winfo_children()):
            wtype = child.winfo_class()
            if wtype == 'Entrybutton':
                self.widget_status.append([])
                for entrychild in child.winfo_children():
                    self.widget_status[-1].append(entrychild['state'])
            elif wtype not in ('Frame','Labelframe','TFrame','TLabelframe') and i!=1:
                self.widget_status.append(child['state'])
            else:
                self.widget_status.append(None)

    # Toggle colour of widgets depending on active state of trainer
    def toggle_colour(self):

        # Turning on
        if self.active.get():
            for child in self.winfo_children():
                if child.winfo_class() == 'Entrybutton':
                    for entrychild in child.winfo_children():
                        self.configure_colour(entrychild, self.bga)
                self.configure_colour(child, self.bga)
            self.configure(bg=self.bga)
        
        # Turning off
        else:
            for child in self.winfo_children():
                if child.winfo_class() == 'Entrybutton':
                    for entrychild in child.winfo_children():
                        self.configure_colour(entrychild, self.bg)
                self.configure_colour(child, self.bg)
            self.configure(bg=self.bg)

    # Change colours of a widget
    def configure_colour(self, widget, colour):
        try:
            widget.configure({'bg': colour, 'activebackground': colour})
        except:
            widget.configure({'bg': colour})

    # Load question settings
    def load_questions(self, row, inflection_type):

        # Load widgets
        self.qs = [tk.IntVar(value=self.config['qs'][0]), tk.IntVar(value=self.config['qs'][1])]
        definitions = tk.Checkbutton(self, variable=self.qs[0], onvalue=1, offvalue=0, text='Ask for definition',
                                     bg=self.bg, activebackground=self.bg)
        definitions.grid(row=row, column=0, columnspan=2, padx=(5,0), sticky='w')
        self.inflections_no = tk.StringVar(value=self.config['inflections_no'])
        inflections = Entrybutton(self, variable=self.qs[1], text=f'Ask {inflection_type}', textvariable=self.inflections_no,
                                  e_width=2, justify='right', int_only=True, bounded=True, bg=self.bg)
        inflections.grid(row=row+1, column=0, columnspan=2, padx=(5,0), sticky='nsew')
        self.line_border(row+2)

        # Ensure at least one is selected
        for var, widget in zip(self.qs, [definitions, inflections]):
            var.trace_add('write', lambda *args, w=widget: self.qn_check(w, args[0]))

    # At least one question must be selected
    def qn_check(self, widget, var):
        if self.qs[0].get() + self.qs[1].get() == 0:
            self.setvar(name=var, value=1)
            widget.configure(bg=widget.cget('bg'))
    
    # Load double columned list of settings
    def load_dcol(self, row, texts, vars, return_btns=False):
        dcol_btns = []
        for i, case in enumerate(texts):
            dcol_btns.append(tk.Checkbutton(self, variable=vars[i], onvalue=1, offvalue=0, text=case, bg=self.bg, activebackground=self.bg))
            dcol_btns[-1].grid(row=row+int(i/2), column=i%2, padx=((1-i%2)*5,0),  sticky='w')
        self.line_border(row+int(i/2)+1)
        if return_btns:
            return dcol_btns
         
    # Load word list settings
    def load_word_lists(self, row):
        self.grid_rowconfigure(row, weight=1)
        self.word_list = tk.StringVar(value=self.config['word_list'])
        word_list_all = tk.Radiobutton(self, text='All words', variable=self.word_list, 
                                        value='all', bg=self.bg, activebackground=self.bg)
        word_list_all.grid(row=row, column=0, columnspan=2, padx=(5,0), sticky='sw')
        self.freq_no = tk.StringVar(value=self.config['freq_no'])
        word_list_freq = Entrybutton(self, text='Most frequent', variable=self.word_list, textvariable=self.freq_no, value='freq',
                                     radio=True, e_width=5, justify='right', int_only=True, bounded=True, bg=self.bg)
        word_list_freq.grid(row=row+1, column=0, columnspan=2, padx=(5,0), sticky='w')
        self.custom_list = self.config['custom_list']
        word_list_label = tk.Label(self, text=os.path.split(self.custom_list)[-1], font=('Segoe UI italic', 9), bg=self.bg)
        word_list_custom = tk.Radiobutton(self, text='Custom list', variable=self.word_list, value='custom', 
                                          bg=self.bg, activebackground=self.bg, command=lambda w=word_list_label: self.choose_word_list_custom(w))
        word_list_custom.grid(row=row+2, column=0, columnspan=2, padx=(5,0), pady=(0,20), sticky='w')
        word_list_label.place(in_=word_list_custom, relx=0, x=17, rely=1, y=-2)
        self.word_list.trace_add('write', lambda *args, v=self.word_list, t='custom', e=[word_list_label]: show_widget(v,t,e))
    
    # Open file explorer to choose path to custom word list
    def choose_word_list_custom(self, widget):

        # Select path
        filename = filedialog.askopenfilename(initialdir='data', title='Select a File', filetypes=[('Comma-separated values files', '*.csv*')])

        # If path selected, update options to new path
        if filename != '':
            self.custom_list = filename
            widget.configure(text=os.path.split(filename)[-1])
        # If no path ever chosen, default back to frequency word list
        elif self.custom_list is None:
            self.word_list.set('freq')
    
    # Draw horizontal line border at specified position
    def line_border(self, row):
        line = Lineborder(self)
        line.grid(row=row, column=0, columnspan=2, padx=3, pady=8, sticky='ew')

# Train adjectives  
class adj_trainer(trainer_frame):
    def __init__(self, *args, **kwargs):
        trainer_frame.__init__(self, *args, **kwargs)

        # Load title and question settings
        self.load_title(0, 'Adjectives')
        self.load_questions(3, 'declensions')

        # Load case settings
        cases = ['Nom.', 'Gen.', 'Dat.', 'Acc.', 'Ins.', 'Loc.', 'Voc.']
        self.case_vars = [tk.IntVar(value=self.config['case_vars'][0]), []]
        for i in range(len(cases)):
            self.case_vars[1].append(tk.IntVar(value=self.config['case_vars'][1][i]))
        case_btns=self.load_dcol(7, cases, self.case_vars[1], return_btns=True)
        self.load_vn_only(6, self.case_vars[0], case_btns)

        # Load word lists
        self.load_word_lists(12)

        # Finish loading
        self.toggle_active(widget_status=self.config['widget_status'])

    # Loads button to only train virile nominative declensions
    def load_vn_only(self, row, var, disable_widgets):
        vn_only = tk.Checkbutton(self, variable=var, onvalue=1, offvalue=0, text='Virile nominative only', 
                                     bg=self.bg, activebackground=self.bg, command=lambda v=var, t=0, e=disable_widgets: show_widget(v,t,e))
        vn_only.grid(row=row, column=0, columnspan=2, padx=(5,0), sticky='w')

    # Get current config settings to be saved
    def get_config(self):

        # Ensures widget_status is updated
        if self.active.get():
            self.get_widget_status()

        # Collect settings
        config = {}
        config['active'] = self.active.get()
        config['qs'] = [self.qs[0].get(), self.qs[1].get()]
        config['inflections_no'] = self.inflections_no.get()
        config['case_vars'] = [self.case_vars[0].get(), []]
        for i in range(len(self.case_vars[1])):
            config['case_vars'][1].append(self.case_vars[1][i].get())
        config['word_list'] = self.word_list.get()
        config['freq_no'] = self.freq_no.get()
        config['custom_list'] = self.custom_list
        config['widget_status'] = self.widget_status

        return config

class menu_display(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.bga = kwargs.pop('bga', None)
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.bg = self.cget('bg')

        # Load play button
        self.load_play(parent)

    # Load play button
    def load_play(self, parent):
        play_btn = tk.Button(self, text='Play', command=lambda: self.save_config(parent), bg=self.bga, activebackground=self.bga)
        play_btn.pack(fill='x', side='bottom')

    def save_config(self, parent):
        
        # Get current config settings for each trainer
        config = {}
        trainers = ['adj']# , 'noun', 'verb', 'misc']
        trainer_frames = [parent.adj_frame]# , parent.noun_frame, parent.verb_frame, parent.misc_frame]
        for trainer, trainer_frame in zip(trainers, trainer_frames):
            config[trainer] = trainer_frame.get_config()

        # Save new config
        with open('trainer_config.json', 'w') as outfile: 
            json.dump(config, outfile)

        print('Saved')

