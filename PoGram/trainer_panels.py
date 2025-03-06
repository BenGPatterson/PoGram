# -*- coding: utf-8 -*-

import os
from itertools import product
import tkinter as tk
from tkinter import filedialog
from custom_widgets import Entrybutton, Lineborder, show_widget

# Parent class for trainer settings
class trainer_frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop('config')
        tk.Frame.__init__(self, *args, **kwargs)
        self.bg = kwargs.get('bg', self.cget('bg'))
        self.widget_status = self.config['widget_status']
        self.grid_columnconfigure((0,1), weight=1, uniform='column')

    # Load active toggle and title
    def load_title(self, row, text):
        self.active = tk.IntVar(value=self.config['active'])
        toggle = tk.Checkbutton(self, variable=self.active, onvalue=1, offvalue=0, bg=self.bg, activebackground=self.bg, 
                                command=self.toggle_active)
        toggle.grid(row=row, column=0, columnspan=2)
        title = tk.Label(self, text=text, bg=self.bg, font=('Segoe UI', 22))
        title.grid(row=row+1, column=0, columnspan=2)

    # Enables/disables widgets depending on active state of trainer
    def toggle_active(self, widget_status=None):

        # Turning on
        if self.active.get():
            for i, child in enumerate(self.winfo_children()):
                wtype = child.winfo_class()
                if wtype == 'Entrybutton':
                    for j, entrychild in enumerate(child.winfo_children()):
                        entrychild.configure(state=self.widget_status[i][j])
                elif wtype not in ('Frame','Labelframe','TFrame','TLabelframe'):
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
                elif wtype not in ('Frame','Labelframe','TFrame','TLabelframe'):
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
            elif wtype not in ('Frame','Labelframe','TFrame','TLabelframe'):
                self.widget_status.append(child['state'])
            else:
                self.widget_status.append(None)

    # Load question settings
    def load_questions(self, row, derivation, inflection_type, return_btns=False):

        # Load widgets
        self.qs = [tk.IntVar(value=self.config['qs'][0]), tk.IntVar(value=self.config['qs'][1]), tk.IntVar(value=self.config['qs'][2])]
        definitions = tk.Checkbutton(self, variable=self.qs[0], onvalue=1, offvalue=0, text='Ask for definition',
                                     bg=self.bg, activebackground=self.bg)
        definitions.grid(row=row, column=0, columnspan=2, padx=(5,0), sticky='w')
        derived_words = tk.Checkbutton(self, variable=self.qs[1], onvalue=1, offvalue=0, text=f'Ask for {derivation}',
                                       bg=self.bg, activebackground=self.bg)
        derived_words.grid(row=row+1, column=0, columnspan=2, padx=(5,0), sticky='w')
        self.inflections_no = tk.StringVar(value=self.config['inflections_no'])
        inflections = Entrybutton(self, variable=self.qs[2], text=f'Ask {inflection_type}', textvariable=self.inflections_no,
                                  btn_type='check', e_width=2, justify='right', int_only=True, bounded=True, bg=self.bg)
        inflections.grid(row=row+2, column=0, columnspan=2, padx=(5,0), sticky='nsew')

        if return_btns:
            return definitions, derived_words, inflections
    
    # Load double columned list of settings
    def load_dcol(self, row, texts, vars, return_btns=False, last_span=False):
        dcol_btns = []
        for i, text in enumerate(texts):
            dcol_btns.append(tk.Checkbutton(self, variable=vars[i], onvalue=1, offvalue=0, text=text, bg=self.bg, activebackground=self.bg))
            if last_span and i == len(texts)-1:
                dcol_btns[-1].grid(row=row+int(i/2), column=i%2, columnspan=2, padx=((1-i%2)*5,0), sticky='w')
            else:
                dcol_btns[-1].grid(row=row+int(i/2), column=i%2, padx=((1-i%2)*5,0), sticky='w')
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
                                     btn_type='radio', e_width=5, justify='right', int_only=True, bounded=True, bg=self.bg)
        word_list_freq.grid(row=row+1, column=0, columnspan=2, padx=(5,0), sticky='w')
        self.custom_list = self.config['custom_list']
        word_list_label = tk.Label(self, text=os.path.split(self.custom_list)[-1], font=('Segoe UI italic', 9), bg=self.bg)
        word_list_custom = tk.Radiobutton(self, text='Custom list', variable=self.word_list, value='custom', 
                                          bg=self.bg, activebackground=self.bg, command=lambda w=word_list_label: self.choose_word_list_custom(w))
        word_list_custom.grid(row=row+2, column=0, columnspan=2, padx=(5,0), pady=(0,20), sticky='w')
        word_list_label.place(in_=word_list_custom, relx=0, x=17, rely=1, y=-2)
        self.word_list.trace_add('write', lambda *args, v=[self.word_list], t=[['custom']], e=[word_list_label]: show_widget(v,t,e))
    
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

    # Enforce disabling restrictions on settings
    def disable_restrictions(self, vars_list, ts_list, widgets_list):
        for i in range(len(vars_list)):
            for j in range(len(vars_list[i])):
                vars_list[i][j].trace_add('write', lambda *args, v=vars_list[i], t=ts_list[i], e=widgets_list[i]: show_widget(v,t,e))

    # Link buttons, enforcing at least one option selected and multi-select functionality
    def link_buttons(self, vars, widgets):
        for i, (var, widget) in enumerate(zip(vars, widgets)):
            if widget.winfo_class() == 'Entrybutton':
                widget.bind('<Button-3>', lambda *args, w=widget, vs=vars, idx=i: self.multi_select(*args, w, vs, idx), target_widget='btn')
            else:
                widget.bind('<Button-3>', lambda *args, w=widget, vs=vars, idx=i: self.multi_select(*args, w, vs, idx))
            var.trace_add('write', lambda *args, w=widget, vs=vars: self.min_check(w, vs, args[0]))

    # At least one option must be selected
    def min_check(self, widget, vars, var):
        no_selected = 0
        for i in range(len(vars)):
            no_selected += vars[i].get()
        if no_selected == 0:
            self.setvar(name=var, value=1)
            widget.configure(bg=widget.cget('bg'))
        
    # Select or deselect all
    def multi_select(self, event, widget, vars, idx):
        if widget.winfo_class() == 'Entrybutton':
            state = widget.btn['state']
        else:
            state = widget['state']
        if state != 'disabled':
            target = 1 - vars[idx].get()
            var_list = vars.copy()
            if target == 0:
                var_list.pop(idx)
            for i in range(len(var_list)):
                var_list[i].set(target)
    
    # Draw horizontal line border at specified position
    def line_border(self, row):
        line = Lineborder(self)
        line.grid(row=row, column=0, columnspan=2, padx=3, pady=4, sticky='ew')

# Train miscellaneous  
class misc_trainer(trainer_frame):
    def __init__(self, *args, **kwargs):
        trainer_frame.__init__(self, *args, **kwargs)

        # Load title
        self.load_title(0, 'Misc.')
        self.line_border(2)

        # Load pronoun questions
        text_dict = {'Pers': 'Personal pronouns', 'Poss': 'Possessive pron.', 'Demo': 'Demonstrative pron.', 
                     'Inte': 'Interrogative pron.', 'Opro': 'Other pronouns', 'Card': 'Cardinal numerals',
                     'Coll': 'Collective numerals', 'Dwa': 'Dwa/Oba/Obydwa', 'Ordi': 'Ordinal numerals',
                     'Nnum': 'Numeral nouns', 'Oqua': 'Other quantifiers', 'Wini': 'Winien-like verbs', 
                     'Prep': 'Prepositions'}
        q_order = ['Pers', 'Poss', 'Demo', 'Inte', 'Opro', 'Card', 'Coll', 'Dwa', 'Ordi', 'Nnum', 'Oqua', 'Wini', 'Prep']
        self.qs = {}
        for key in text_dict.keys():
            self.qs[key] = tk.IntVar(value=self.config['qs'][key])
        other_rows = {8: None, 15: None}
        btns_list = self.load_scol(3, [text_dict[key] for key in q_order], [self.qs[key] for key in q_order], other_rows=other_rows, return_btns=True)
        misc_btns = {}
        for i, key in enumerate(q_order):
            misc_btns[key] = btns_list[i]

        # Load option to select number of inflections and number of digits
        self.line_border(18)
        self.inflections_no = tk.StringVar(value=self.config['inflections_no'])
        inf_no = Entrybutton(self, variable=None, text=f'Forms:', textvariable=self.inflections_no, btn_type='label', 
                           e_width=2, justify='right', int_only=True, bounded=True, bg=self.bg)
        inf_no.grid(row=19, column=0, columnspan=1, padx=(10,0), pady=(4,0), sticky='w')
        self.digits_no = tk.StringVar(value=self.config['digits_no'])
        dig_no = Entrybutton(self, variable=None, text=f'Digits:', textvariable=self.digits_no, btn_type='label', 
                           e_width=2, e_allow=1, justify='right', int_only=True, bounded=True, bg=self.bg)
        dig_no.grid(row=19, column=1, columnspan=1, pady=(4,0), sticky='w')

        # Enforce disabling restrictions
        inf_no_keys = ['Pers', 'Poss', 'Demo', 'Inte', 'Opro', 'Card', 'Coll', 'Dwa', 'Ordi', 'Nnum', 'Oqua', 'Wini']
        dig_no_keys = ['Card', 'Coll', 'Ordi']
        vars_list = [[self.qs[key] for key in inf_no_keys], 
                     [self.qs[key] for key in dig_no_keys]]
        inf_no_ts = [[*seq] for seq in product((True, False), repeat=len(inf_no_keys))][:-1]
        dig_no_ts = [[*seq] for seq in product((True, False), repeat=len(dig_no_keys))][:-1]
        ts_list = [inf_no_ts, dig_no_ts]
        widgets_list = [inf_no.winfo_children(), dig_no.winfo_children()]
        self.disable_restrictions(vars_list, ts_list, widgets_list)

        # Enforce at least one option select, and multi-select functionality
        self.link_keys = text_dict.keys()
        self.link_buttons([self.qs[key] for key in self.link_keys], [misc_btns[key] for key in self.link_keys])

        # Finish loading
        self.toggle_active(widget_status=self.config['widget_status'])

    # Load single columned list of settings
    def load_scol(self, row, texts, vars, other_rows={}, return_btns=False):
        scol_btns = []
        for i, case in enumerate(texts):
            while row+i in list(other_rows.keys()):
                if other_rows[row+i] is None:
                    self.line_border(row+i)
                else:
                    label = tk.Label(self, text=other_rows[row+i], bg=self.bg)
                    label.grid(row=row+i, column=0, columnspan=2, padx=(5,0), sticky='w')
                row+=1
            scol_btns.append(tk.Checkbutton(self, variable=vars[i], onvalue=1, offvalue=0, text=case, bg=self.bg, activebackground=self.bg))
            scol_btns[-1].grid(row=row+i, column=0, columnspan=2, padx=(5,0),  sticky='w')
        if return_btns:
            return scol_btns

    # Get current config settings to be saved
    def get_config(self):

        # Ensures widget_status is updated
        if self.active.get():
            self.get_widget_status()

        # Collect settings
        config = {}
        config['active'] = self.active.get()
        config['qs'] = {}
        for key in self.qs.keys():
            config['qs'][key] = self.qs[key].get()
        config['inflections_no'] = self.inflections_no.get()
        config['digits_no'] = self.digits_no.get()
        config['widget_status'] = self.widget_status

        return config
    
# Train verbs  
class verb_trainer(trainer_frame):
    def __init__(self, *args, **kwargs):
        trainer_frame.__init__(self, *args, **kwargs)

        # Load title and question settings
        self.load_title(0, 'Verbs')
        self.line_border(2)
        q_btns = self.load_questions(3, 'verb pairs', 'conjugations', return_btns=True)
        self.line_border(6)

        # Load tense settings
        tenses = ['Pres.', 'Past', 'Fut.', 'Cond.', 'Imp.', 'Part.', 'Verbal noun']
        self.tense_vars = []
        for i in range(len(tenses)):
            self.tense_vars.append(tk.IntVar(value=self.config['tense_vars'][i]))
        conj_btns = self.load_dcol(7, tenses, self.tense_vars, return_btns=True, last_span=True)
        self.line_border(11)

        # Load additional settings
        self.excl_impers = tk.IntVar(value=self.config['excl_impers'])
        impers_btn = tk.Checkbutton(self, variable=self.excl_impers, onvalue=1, offvalue=0,
                                    text='Exclude impersonal', bg=self.bg, activebackground=self.bg)
        impers_btn.grid(row=12, column=0, columnspan=2, padx=(5,0), sticky='w')
        self.excl_niech = tk.IntVar(value=self.config['excl_niech'])
        niech_btn = tk.Checkbutton(self, variable=self.excl_niech, onvalue=1, offvalue=0,
                                   text='Exclude niech imp.', bg=self.bg, activebackground=self.bg)
        niech_btn.grid(row=13, column=0, columnspan=2, padx=(5,0), sticky='w')

        # Enforce disabling restrictions
        vars_list = [[self.qs[2]], [*self.tense_vars[0:4], self.qs[2]], [self.tense_vars[4], self.qs[2]]]
        impers_ts = [[*seq, 1] for seq in product((True, False), repeat=4)][:-1]
        ts_list = [[[1]], impers_ts, [[1,1]]]
        widgets_list = [conj_btns, [impers_btn], [niech_btn]]
        self.disable_restrictions(vars_list, ts_list, widgets_list)

        # Enforce at least one option select, and multi-select functionality
        self.link_buttons(self.qs, q_btns)
        self.link_buttons(self.tense_vars, conj_btns)

        # Load word lists
        self.load_word_lists(14)

        # Finish loading
        self.toggle_active(widget_status=self.config['widget_status'])

    # Get current config settings to be saved
    def get_config(self):

        # Ensures widget_status is updated
        if self.active.get():
            self.get_widget_status()

        # Collect settings
        config = {}
        config['active'] = self.active.get()
        config['qs'] = [self.qs[0].get(), self.qs[1].get(), self.qs[2].get()]
        config['inflections_no'] = self.inflections_no.get()
        config['tense_vars'] = []
        for i in range(len(self.tense_vars)):
            config['tense_vars'].append(self.tense_vars[i].get())
        config['excl_impers'] = self.excl_impers.get()
        config['excl_niech'] = self.excl_niech.get()
        config['word_list'] = self.word_list.get()
        config['freq_no'] = self.freq_no.get()
        config['custom_list'] = self.custom_list
        config['widget_status'] = self.widget_status

        return config
    
# Train adjectives  
class adj_trainer(trainer_frame):
    def __init__(self, *args, **kwargs):
        trainer_frame.__init__(self, *args, **kwargs)

        # Load title and question settings
        self.load_title(0, 'Adjectives')
        self.line_border(2)
        q_btns = self.load_questions(3, 'derived words', 'declensions', return_btns=True)
        self.line_border(6)

        # Load case settings
        cases = ['Nom.', 'Gen.', 'Dat.', 'Acc.', 'Ins.', 'Loc.', 'Voc.']
        self.case_vars = [tk.IntVar(value=self.config['case_vars'][0]), []]
        for i in range(len(cases)):
            self.case_vars[1].append(tk.IntVar(value=self.config['case_vars'][1][i]))
        case_btns = self.load_dcol(7, cases, self.case_vars[1], return_btns=True)
        self.line_border(11)

        # Load additional settings
        vn_only = tk.Checkbutton(self, variable=self.case_vars[0], onvalue=1, offvalue=0,
                                 text='Virile nominative only', bg=self.bg, activebackground=self.bg)
        vn_only.grid(row=12, column=0, columnspan=2, padx=(5,0), sticky='w')
        self.adverbs = tk.IntVar(value=self.config['adverbs'])
        adverbs = tk.Checkbutton(self, variable=self.adverbs, onvalue=1, offvalue=0, text='Include adverbs',
                                 bg=self.bg, activebackground=self.bg)
        adverbs.grid(row=13, column=0, columnspan=2, padx=(5,0), sticky='w')

        # Enforce disabling restrictions
        vars_list = [[self.case_vars[0], self.qs[2]], [self.qs[2]], [self.qs[1]]]
        ts_list = [[[0,1]], [[1]], [[1]]]
        widgets_list = [case_btns, [vn_only], [adverbs]]
        self.disable_restrictions(vars_list, ts_list, widgets_list)

        # Enforce at least one option select, and multi-select functionality
        self.link_buttons(self.qs, q_btns)
        self.link_buttons(self.case_vars[1], case_btns)

        # Load word lists
        self.load_word_lists(14)

        # Finish loading
        self.toggle_active(widget_status=self.config['widget_status'])

    # Get current config settings to be saved
    def get_config(self):

        # Ensures widget_status is updated
        if self.active.get():
            self.get_widget_status()

        # Collect settings
        config = {}
        config['active'] = self.active.get()
        config['qs'] = [self.qs[0].get(), self.qs[1].get(), self.qs[2].get()]
        config['inflections_no'] = self.inflections_no.get()
        config['case_vars'] = [self.case_vars[0].get(), []]
        for i in range(len(self.case_vars[1])):
            config['case_vars'][1].append(self.case_vars[1][i].get())
        config['adverbs'] = self.adverbs.get()
        config['word_list'] = self.word_list.get()
        config['freq_no'] = self.freq_no.get()
        config['custom_list'] = self.custom_list
        config['widget_status'] = self.widget_status

        return config
    
# Train nouns  
class noun_trainer(trainer_frame):
    def __init__(self, *args, **kwargs):
        trainer_frame.__init__(self, *args, **kwargs)

        # Load title and question settings
        self.load_title(0, 'Nouns')
        self.line_border(2)
        q_btns = self.load_questions(3, 'diminutive', 'declensions', return_btns=True)
        self.line_border(6)

        # Load case settings
        cases = ['Nom.', 'Gen.', 'Dat.', 'Acc.', 'Ins.', 'Loc.', 'Voc.']
        self.case_vars = []
        for i in range(len(cases)):
            self.case_vars.append(tk.IntVar(value=self.config['case_vars'][i]))
        case_btns = self.load_dcol(7, cases, self.case_vars, return_btns=True)
        self.line_border(11)

        # Load additional settings
        self.excl_singnom = tk.IntVar(value=self.config['excl_singnom'])
        exclude_singnom = tk.Checkbutton(self, variable=self.excl_singnom, onvalue=1, offvalue=0, text='Exclude singular nom.',
                                 bg=self.bg, activebackground=self.bg)
        exclude_singnom.grid(row=12, column=0, columnspan=2, padx=(5,0), sticky='w')

        # Enforce disabling restrictions
        vars_list = [[self.case_vars[0], self.qs[2]], [self.qs[2]]]
        ts_list = [[[1,1]], [[1]]]
        widgets_list = [[exclude_singnom], case_btns]
        self.disable_restrictions(vars_list, ts_list, widgets_list)

        # Enforce at least one option select, and multi-select functionality
        self.link_buttons(self.qs, q_btns)
        self.link_buttons(self.case_vars, case_btns)

        # Load word lists
        self.load_word_lists(14)

        # Finish loading
        self.toggle_active(widget_status=self.config['widget_status'])

    # Get current config settings to be saved
    def get_config(self):

        # Ensures widget_status is updated
        if self.active.get():
            self.get_widget_status()

        # Collect settings
        config = {}
        config['active'] = self.active.get()
        config['qs'] = [self.qs[0].get(), self.qs[1].get(), self.qs[2].get()]
        config['inflections_no'] = self.inflections_no.get()
        config['case_vars'] = []
        for i in range(len(self.case_vars)):
            config['case_vars'].append(self.case_vars[i].get())
        config['excl_singnom'] = self.excl_singnom.get()
        config['word_list'] = self.word_list.get()
        config['freq_no'] = self.freq_no.get()
        config['custom_list'] = self.custom_list
        config['widget_status'] = self.widget_status

        return config