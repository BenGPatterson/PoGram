import tkinter as tk
import random
import re
from custom_widgets import Entry_pl
from dictionary import get_definition, get_derived_word, get_conjugation, get_declension

# Base class for all question loaders
class question():
    def __init__(self, *args, **kwargs):
        for widget in self.q_panel.q_frame.winfo_children():
            widget.destroy()
        self.choose_word()

    # Choose word and update title
    def choose_word(self):
        self.word = self.word_list[random.randint(0,len(self.word_list)-1)].lower()
        self.q_panel.parent.title_frame.word.set(self.word)
        self.q_panel.parent.title_frame.update()

    # Load definition subquestion
    def load_definition(self, pos):
            
        # Try to get derived word, skips otherwise
        try:
            correct = get_definition(self.dict, self.word, pos)
        except:
            correct = [None]
        if None in correct:
            print(f'Cannot find definition of {pos}: {self.word}')
            self.sub_qs = self.sub_qs[1:]
            self.next_subquestion()
            return

        # Loads subquestion
        self.load_subquestion('Definition:', correct, self.def_correct)
        self.sub_qs = self.sub_qs[1:]

    # Load derived word subquestion
    def load_derived(self, pos):

        # Try to get derived word, skips otherwise
        try:
            correct = get_derived_word(self.dict, self.word, pos, self.sub_qs[0])
        except:
            correct = [None]
        if None in correct:
            print(f'Cannot find {self.sub_qs[0]} derived word of {pos}: {self.word}')
            self.sub_qs = self.sub_qs[1:]
            self.next_subquestion()
            return
        
        # Loads subquestion
        derived_text = {'comp': 'Comparative:', 'super': 'Superlative:', 'adv': 'Adverb:', 'dim': 'Diminutive:', 'asp': 'Aspect:',
                        'asp_ii': 'Indeterminate:', 'asp_id': 'Determinate', 'asp_if': 'Frequentative', 
                        'asp_i': 'Imperfective', 'asp_p': 'Perfective'}
        self.load_subquestion(derived_text[self.sub_qs[0]], correct, self.simple_correct)
        self.sub_qs = self.sub_qs[1:]

    # Load conjugation subquestion
    def load_conjugation(self, pos):
            
        # Try to get declension, skips otherwise
        gen, voice, tense = self.sub_qs[0].split('_')
        try:
            correct = get_conjugation(self.dict, self.word, pos, gen, voice, tense)
        except: 
            correct = [None]
        if None in correct:
            print(f'Cannot find {self.sub_qs[0]} conjugation of {pos}: {self.word}')
            self.sub_qs = self.sub_qs[1:]
            self.next_subquestion()
            return
        
        # Loads subquestion
        tense_text = {'pr': 'Present', 'pa': 'Past', 'f': 'Future', 'c': 'Conditional', 'i': 'Imperative', 'v': 'Verbal noun',
                      'par-act': 'Active adjectival participle', 'par-pas': 'passive adjectival participle',
                      'par-cont': 'Contemporary adverbial participle', 'par-ant': 'anterior adverbial participle'}
        gen_text = {'m': 'masculine', 'f': 'feminine', 'n': 'neuter', 'v': 'virile', 'nv': 'non-virile'}
        if gen == '-':
            voice_text = {'1s': '1st person singular', '2s': '2nd person singular', '3s': '3rd person singular',
                          '1p': '1st person plural', '2p': '2nd person plural', '3p': '3rd person plural',
                          'i': 'impersonal'}
        else:
            voice_text = {'1s': '1st person', '2s': '2nd person', '3s': '3rd person',
                          '1p': '1st person', '2p': '2nd person', '3p': '3rd person'}
        q_text = tense_text[tense]
        if gen == '-' and voice == '-':
            q_text += ':'
        elif gen == '-' and voice != '-':
            q_text += f' ({voice_text[voice]}):'
        elif gen != '-' and voice == '-':
            q_text += f' ({gen_text[gen]}):'
        elif gen != '-' and voice != '-':
            q_text += f' ({gen_text[gen]}) ({voice_text[voice]}):'
        self.load_subquestion(q_text, correct, self.simple_correct)
        self.sub_qs = self.sub_qs[1:]
    
    # Load declension subquestion
    def load_declension(self, pos):
            
        # Try to get declension, skips otherwise
        numgen, case = self.sub_qs[0].split('_')
        try:
            correct = get_declension(self.dict, self.word, pos, numgen, case)
        except: 
            correct = [None]
        if None in correct:
            print(f'Cannot find {self.sub_qs[0]} declension of {pos}: {self.word}')
            self.sub_qs = self.sub_qs[1:]
            self.next_subquestion()
            return
        
        # Loads subquestion
        gen_text = {'s': 'Singular', 'p': 'Plural', 'sma': 'Masculine (animate)', 'smi': 'Masculine (inanimate)', 
                    'sf': 'Feminine', 'sn': 'Neuter', 'pv': 'Virile', 'pnv': 'Non-virile'}
        case_text = {'n': 'nominative', 'g': 'genitive', 'd': 'dative', 'a': 'accusative', 
                     'i': 'instrumental', 'l': 'locative', 'v': 'vocative'}
        q_text = gen_text[numgen] + ', ' + case_text[case] + ':'
        self.load_subquestion(q_text, correct, self.simple_correct)
        self.sub_qs = self.sub_qs[1:]

    # Load subquestion
    def load_subquestion(self, text, correct, command):

        # Load question text
        q_label = tk.Label(self.q_panel.q_frame, text=text, font=('Segoe UI', 18))
        q_label.pack(side=tk.TOP)

        # Load entry button
        q_answer = tk.StringVar(value='')
        q_entry = Entry_pl(self.q_panel.q_frame, textvariable=q_answer, bg='SystemWindow', justify='center', font=('Segoe UI', 18))
        q_entry.pack(side=tk.TOP, pady=(0,5))

        # Add command to entry button
        q_entry.bind('<Return>', lambda event: command(q_entry, q_answer.get(), correct))
        q_entry.focus_set()

        # Update frame
        self.q_panel.q_frame_update()

    # Check if definition is correct
    def def_correct(self, widget, answer, correct):

        # Only if first time called
        if widget['state'] != 'disabled':

            # Check correct
            self.game.total_questions += 1
            corr_bool = False
            for defn in correct:
                pos_ans = defn.split('(')[0]
                if answer in list(re.split(',| ', pos_ans)) and answer != '':
                    corr_bool = True
            if corr_bool:
                widget.configure(disabledbackground='#98fb98')
                self.game.total_correct += 1
                self.btn_text = tk.StringVar(value='Mark incorrect')
            else:
                widget.configure(disabledbackground='#fa8072')
                self.btn_text = tk.StringVar(value='Mark correct')
            self.def_widget = widget
            self.def_no = 0
            self.defs = correct
            self.def_text = tk.StringVar(value=f'1. {correct[0]}')
            correct_label = tk.Label(self.q_panel.q_frame, textvariable=self.def_text, font=('Segoe UI', 14), wraplength=750)
            correct_label.pack(side=tk.TOP)

            # Load buttons to check definition
            btn_frame = tk.Frame(self.q_panel.q_frame)
            btn_frame.pack(side=tk.TOP)
            left_def = tk.Button(btn_frame, text='<', command=lambda: self.change_def(-1), font=('Segoe UI', 10))
            left_def.grid(row=0, column=0, sticky='w')
            toggle = tk.Button(btn_frame, textvariable=self.btn_text, command=self.toggle_def, font=('Segoe UI', 10))
            toggle.grid(row=0, column=1, padx=10, sticky='ew')
            right_def = tk.Button(btn_frame, text='>', command=lambda: self.change_def(1), font=('Segoe UI', 10))
            right_def.grid(row=0, column=2, sticky='e')

            # Disable and load next question
            widget.configure(state='disable')
            self.q_panel.q_frame_update()
            self.next_subquestion()

    # Change displayed definition
    def change_def(self, direction):
        self.def_no += direction
        if self.def_no > len(self.defs) - 1:
            self.def_no = 0
        elif self.def_no < 0:
            self.def_no = len(self.defs) - 1
        self.def_text.set(f'{self.def_no+1}. {self.defs[self.def_no]}')
        self.q_panel.q_frame_update()

    # Toggle correct/incorrect definition
    def toggle_def(self):
        if self.btn_text.get() == 'Mark correct':
            self.def_widget.configure(disabledbackground='#98fb98')
            self.game.total_correct += 1
            self.btn_text.set('Mark incorrect')
        else:
            self.def_widget.configure(disabledbackground='#fa8072')
            self.game.total_correct -= 1
            self.btn_text.set('Mark correct')
        self.q_panel.q_frame_update()

    # Check if simple subquestion is correct
    def simple_correct(self, widget, answer, correct):

        # Only if first time called
        if widget['state'] != 'disabled':

            # Check correct
            self.game.total_questions += 1
            if answer in correct:
                widget.configure(disabledbackground='#98fb98')
                self.game.total_correct += 1
            else:
                widget.configure(disabledbackground='#fa8072')
                if set(correct) == set(['imperfective', 'i']):
                    correct_text = 'imperfective, '
                elif set(correct) == set(['perfective', 'p']):
                    correct_text = 'perfective, '
                else:
                    correct_text = ''
                    for ans in correct:
                        correct_text += ans + ', '
                correct_label = tk.Label(self.q_panel.q_frame, text=correct_text[:-2], font=('Segoe UI', 14))
                correct_label.pack(side=tk.TOP)

            # Disable and load next subquestion
            widget.configure(state='disable')
            self.q_panel.q_frame_update()
            self.next_subquestion()
    
    # Create button to end question
    def end_question(self):

        # Check that at least one subquestion asked
        if len(self.q_panel.q_frame.winfo_children()) == 0:
            self.game.current_word_no -= 1
            self.game.next_question()
            return

        # Create button
        next_word = tk.Button(self.q_panel.q_frame, text='Next word', command=self.game.next_question, font=('Segoe UI', 10))
        next_word.pack(side=tk.TOP)
        next_word.bind('<Return>', lambda event: self.game.next_question())
        next_word.focus_set()
        self.q_panel.q_frame_update()

# Load verb questions
class verb_question(question):
    def __init__(self, game, q_panel, trainer, word_list, dictionary, *args, **kwargs):
        self.game = game
        self.q_panel = q_panel
        self.trainer = trainer
        self.word_list = word_list
        self.dict = dictionary
        self.q_panel.parent.title_frame.configure(bg='#ffdfba')
        self.q_panel.parent.title_frame.word_lbl.configure(bg='#ffdfba')
        question.__init__(self, *args, **kwargs)

        # Decide subquestions
        self.sub_qs = []
        if self.trainer.qs[0].get():
            self.sub_qs.append('def')
        if self.trainer.qs[1].get():
            self.sub_qs += ['asp', 'asp_ii', 'asp_id', 'asp_if', 'asp_i', 'asp_p']
        if self.trainer.qs[2].get():
            self.choose_conjugations()

        # Load first subquestion
        self.next_subquestion()

    # Choose declensions to ask
    def choose_conjugations(self):
        
        # Get active tenses
        all_tenses = ['pr', 'pa', 'f', 'c', 'i', 'par', 'v']
        tenses = []
        for i, case_var in enumerate(self.trainer.tense_vars):
            if case_var.get():
                tenses.append(all_tenses[i])
        
        # Choose declension for each sub question
        for i in range(int(self.trainer.inflections_no.get())):

            # Get aspect
            aspect = get_derived_word(self.dict, self.word, 'verb', 'asp')
            
            # Choose tense
            tense = tenses[random.randint(0,len(tenses)-1)]
            if tense == 'par':
                if self.word == 'być':
                    tense = ['par-act', 'par-cont', 'par-ant'][random.randint(0,2)]
                elif aspect == 'impf':
                    tense = ['par-act', 'par-pas', 'par-cont'][random.randint(0,2)]
                elif aspect == 'pf':
                    tense = ['par-pas', 'par-ant'][random.randint(0,1)]
            elif tense == 'pr' and 'p' in aspect:
                tense = 'f'

            # Choose voice
            if tense in ['pr', 'pa', 'f', 'c']:
                if self.word == 'być':
                    voice = ['1s', '2s', '3s', '1p', '2p', '3p'][random.randint(0,5)]
                else:
                    voice = ['1s', '2s', '3s', '1p', '2p', '3p', 'i'][random.randint(0,6)]
            elif tense == 'i':
                voice = ['1s', '2s', '3s', '1p', '2p', '3p'][random.randint(0,5)]
            else:
                voice = '-'
            
            # Choose gender
            if tense in ['pa', 'f', 'c', 'par-act', 'par-pas'] and voice != 'i':
                if tense == 'f' and ('p' in aspect or self.word == 'być'):
                    gen = '-'
                else:
                    if 's' in voice:
                        gen = ['m', 'f', 'n'][random.randint(0,2)]
                    elif 'p' in voice:
                        gen = ['v', 'nv'][random.randint(0,1)]
                    else:
                        gen = ['m', 'f', 'n', 'v', 'nv'][random.randint(0,4)]
            else:
                gen = '-'
            
            # Combine
            self.sub_qs.append(gen+'_'+voice+'_'+tense)
    
    # Load next subquestion
    def next_subquestion(self):

        # Check if end of sub questions
        if len(self.sub_qs) == 0:
            self.end_question()
            return
        
        # Definition question
        if self.sub_qs[0] in ['def']:
            self.load_definition('verb')
        
        # Derived word question
        elif self.sub_qs[0] in ['asp', 'asp_ii', 'asp_id', 'asp_if', 'asp_i', 'asp_p']:
            self.load_derived('verb')

        # Inflection question
        elif '_' in self.sub_qs[0]:
            self.load_conjugation('verb')

# Load adjective questions
class adj_question(question):
    def __init__(self, game, q_panel, trainer, word_list, dictionary, *args, **kwargs):
        self.game = game
        self.q_panel = q_panel
        self.trainer = trainer
        self.word_list = word_list
        self.dict = dictionary
        self.q_panel.parent.title_frame.configure(bg='#ffffba')
        self.q_panel.parent.title_frame.word_lbl.configure(bg='#ffffba')
        question.__init__(self, *args, **kwargs)

        # Decide subquestions
        self.sub_qs = []
        if self.trainer.qs[0].get():
            self.sub_qs.append('def')
        if self.trainer.qs[1].get():
            self.sub_qs += ['comp', 'super']
            if self.trainer.adverbs.get():
                self.sub_qs.append('adv')
        if self.trainer.qs[2].get():
            self.choose_declensions()

        # Load first subquestion
        self.next_subquestion()

    # Choose declensions to ask
    def choose_declensions(self):

        # Virile nominative only
        if self.trainer.case_vars[0].get():
            self.sub_qs += ['pv_n']*int(self.trainer.inflections_no.get())
            return
        
        # Get active cases
        all_cases = ['n', 'g', 'd', 'a', 'i', 'l', 'v']
        cases = []
        for i, case_var in enumerate(self.trainer.case_vars[1]):
            if case_var.get():
                cases.append(all_cases[i])
        
        # Choose declension for each sub question
        for i in range(int(self.trainer.inflections_no.get())):

            # Choose gender
            gen = ['sm', 'sf', 'sn', 'pv', 'pnv'][random.randint(0,4)]
            if gen == 'sm':
                gen += ['a', 'i'][random.randint(0,1)]
            
            # Choose case and combine
            cas = cases[random.randint(0,len(cases)-1)]
            self.sub_qs.append(gen+'_'+cas)
    
    # Load next subquestion
    def next_subquestion(self):

        # Check if end of sub questions
        if len(self.sub_qs) == 0:
            self.end_question()
            return
        
        # Definition question
        if self.sub_qs[0] in ['def']:
            self.load_definition('adj')
        
        # Derived words question
        elif self.sub_qs[0] in ['comp', 'super', 'adv']:
            self.load_derived('adj')

        # Inflection question
        elif '_' in self.sub_qs[0]:
            self.load_declension('adj')

# Load noun questions
class noun_question(question):
    def __init__(self, game, q_panel, trainer, word_list, dictionary, *args, **kwargs):
        self.game = game
        self.q_panel = q_panel
        self.trainer = trainer
        self.word_list = word_list
        self.dict = dictionary
        self.q_panel.parent.title_frame.configure(bg='#baffc9')
        self.q_panel.parent.title_frame.word_lbl.configure(bg='#baffc9')
        question.__init__(self, *args, **kwargs)

        # Decide subquestions
        self.sub_qs = []
        if self.trainer.qs[0].get():
            self.sub_qs.append('def')
        if self.trainer.qs[1].get():
            self.sub_qs += ['dim']
        if self.trainer.qs[2].get():
            self.choose_declensions()

        # Load first subquestion
        self.next_subquestion()

    # Choose declensions to ask
    def choose_declensions(self):
        
        # Get active cases
        all_cases = ['n', 'g', 'd', 'a', 'i', 'l', 'v']
        cases = []
        for i, case_var in enumerate(self.trainer.case_vars):
            if case_var.get():
                cases.append(all_cases[i])
        
        # Choose declension for each sub question
        for i in range(int(self.trainer.inflections_no.get())):

            # Choose gender
            if self.trainer.excl_singnom.get() and cases == ['n']:
                gen = 'p'
            else:
                gen = ['s', 'p'][random.randint(0,1)]
            
            # Choose case and combine
            if self.trainer.excl_singnom.get() and gen == 's' and 'n' in cases:
                cas = cases[random.randint(1,len(cases)-1)]
            else:
                cas = cases[random.randint(0,len(cases)-1)]
            self.sub_qs.append(gen+'_'+cas)
    
    # Load next subquestion
    def next_subquestion(self):

        # Check if end of sub questions
        if len(self.sub_qs) == 0:
            self.end_question()
            return
        
        # Definition question
        if self.sub_qs[0] in ['def']:
            self.load_definition('noun')
        
        # Derived words question
        elif self.sub_qs[0] in ['dim']:
            self.load_derived('noun')

        # Inflection question
        elif '_' in self.sub_qs[0]:
            self.load_declension('noun')


            
        