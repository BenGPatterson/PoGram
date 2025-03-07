import tkinter as tk
import random
import re
from custom_widgets import Entry_pl
from dictionary import get_definition, get_derived_word, get_conjugation, get_declension

# Base class for all question loaders
class question():
    def __init__(self, pos, *args, **kwargs):

        # Clears current frame and chooses word
        for widget in self.q_panel.q_frame.winfo_children():
            widget.destroy()
        self.skip = False
        if pos != 'misc':
            self.choose_word(pos)

    # Choose word and update title
    def choose_word(self, pos):
        
        # Randomise new word list if current empty
        if len(self.game.current_word_lists[pos]) == 0:
            random.shuffle(self.game.word_lists[pos])
            self.game.current_word_lists[pos] = self.game.word_lists[pos].copy()

        # Pick next word in list
        self.word = self.game.current_word_lists[pos][0]
        self.game.current_word_lists[pos] = self.game.current_word_lists[pos][1:]

        # Update title with new word
        self.q_panel.parent.title_frame.word.set(self.word)
        self.q_panel.parent.title_frame.update()

    # Keeps only conjugations with answers available
    def choose_poss_conjugations(self, pos):

        # Get all correct answers
        self.correct_forms = []
        for form in self.forms:
            gen, voice, tense = form.split('_')
            try:
                self.correct_forms.append(get_conjugation(self.dict, self.word, pos, gen, voice, tense))
            except:
                self.correct_forms.append([None])

        # Remove forms without answers
        for i in range(len(self.forms)-1,-1,-1):
            if self.correct_forms[i] == [None]:
                self.correct_forms.pop(i)
                self.forms.pop(i)

    # Keeps only declensions with answers available
    def choose_poss_declensions(self, pos):

        # Get all correct answers
        self.correct_forms = []
        for form in self.forms:
            numgen, case = form.split('_')
            try:
                self.correct_forms.append(get_declension(self.dict, self.word, pos, numgen, case))
            except:
                self.correct_forms.append([None])

        # Remove forms without answers
        for i in range(len(self.forms)-1,-1,-1):
            if self.correct_forms[i] == [None]:
                self.correct_forms.pop(i)
                self.forms.pop(i)

    # Selects order of form subquestions
    def add_poss_forms(self):

        # Skips if no forms possible
        if len(self.forms) == 0:
            self.skip = True
            return
        
        # Randomises list order and adds to subquestions
        non_form_len = len(self.sub_qs)
        form_zip = list(zip(self.forms, self.correct_forms))
        self.correct = []
        while len(self.sub_qs) < int(self.trainer.inflections_no.get()) + non_form_len:
            random.shuffle(form_zip)
            random_form, random_correct = zip(*form_zip)
            self.sub_qs += list(random_form)
            self.correct += list(random_correct)
        if len(self.sub_qs) > int(self.trainer.inflections_no.get()) + non_form_len:
            self.correct = self.correct[:int(self.trainer.inflections_no.get()) + non_form_len - len(self.sub_qs)]
            self.sub_qs = self.sub_qs[:int(self.trainer.inflections_no.get()) + non_form_len - len(self.sub_qs)]

    # Load definition subquestion
    def load_definition(self, pos):
            
        # Try to get derived word, skips otherwise
        try:
            correct = get_definition(self.dict, self.word, pos)
        except:
            correct = [None]
        if None in correct:
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
            self.sub_qs = self.sub_qs[1:]
            self.next_subquestion()
            return
        
        # Loads subquestion
        derived_text = {'comp': 'Comparative:', 'super': 'Superlative:', 'adv': 'Adverb:', 'dim': 'Diminutive:', 'asp': 'Aspect:',
                        'asp_ii': 'Indeterminate:', 'asp_id': 'Determinate:', 'asp_if': 'Frequentative:', 
                        'asp_i': 'Imperfective:', 'asp_p': 'Perfective:'}
        self.load_subquestion(derived_text[self.sub_qs[0]], correct, self.simple_correct)
        self.sub_qs = self.sub_qs[1:]

    # Load conjugation subquestion
    def load_conjugation(self):
        
        # Loads subquestion
        tense_text = {'pr': 'Present', 'pa': 'Past', 'f': 'Future', 'c': 'Conditional', 'i': 'Imperative', 'v': 'Verbal noun',
                      'par-act': 'Active adjectival participle', 'par-pas': 'passive adjectival participle',
                      'par-cont': 'Contemporary adverbial participle', 'par-ant': 'anterior adverbial participle'}
        gen_text = {'m': 'masculine', 'f': 'feminine', 'n': 'neuter', 'v': 'virile', 'nv': 'non-virile'}
        gen, voice, tense = self.sub_qs[0].split('_')
        if gen == '-':
            voice_text = {'1s': '1st person singular', '2s': '2nd person singular', '3s': '3rd person singular',
                          '1p': '1st person plural', '2p': '2nd person plural', '3p': '3rd person plural',
                          '1': '1st person', '2': '2nd person', '3': '3rd person', 'i': 'impersonal'}
        else:
            voice_text = {'1s': '1st person', '2s': '2nd person', '3s': '3rd person',
                          '1p': '1st person', '2p': '2nd person', '3p': '3rd person',
                          '1': '1st person', '2': '2nd person', '3': '3rd person'}
        q_text = tense_text[tense]
        if gen == '-' and voice == '-':
            q_text += ':'
        elif gen == '-' and voice != '-':
            q_text += f' ({voice_text[voice]}):'
        elif gen != '-' and voice == '-':
            q_text += f' ({gen_text[gen]}):'
        elif gen != '-' and voice != '-':
            q_text += f' ({gen_text[gen]}) ({voice_text[voice]}):'
        self.load_subquestion(q_text, self.correct[0], self.simple_correct)
        self.sub_qs = self.sub_qs[1:]
        self.correct = self.correct[1:]
    
    # Load declension subquestion
    def load_declension(self, disable_numgen=False):
        
        # Forms subquestion text
        gen_text = {'s': 'singular', 'p': 'plural', 'sma': 'masculine (animate)', 'smi': 'masculine (inanimate)', 
                    'sf': 'feminine', 'sn': 'neuter', 'pv': 'virile', 'pnv': 'non-virile', '-': ''}
        case_text = {'n': 'nominative', 'g': 'genitive', 'd': 'dative', 'a': 'accusative', 
                     'i': 'instrumental', 'l': 'locative', 'v': 'vocative', '-': ''}
        lcp_text = {'l': 'stressed form', 'c': 'clitic form', 'p': 'after prepositions', '-': ''}
        if len(self.sub_qs[0].split('_')) == 2:
            self.sub_qs[0] += '_-'
        numgen, case, lcp = self.sub_qs[0].split('_')
        if disable_numgen:
            numgen = '-'
        q_text = ''
        for text, text_dict in zip([numgen, case, lcp], [gen_text, case_text, lcp_text]):
            if len(text_dict[text]) > 0:
                q_text += text_dict[text] +', '
        q_text = q_text[:-2] + ':'

        # Loads subquestion
        self.load_subquestion(q_text.capitalize(), self.correct[0], self.simple_correct)
        self.sub_qs = self.sub_qs[1:]
        self.correct = self.correct[1:]

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
                corr_ans = [ans.strip() for ans in list(re.split(',|;', pos_ans))]
                corr_ans += list(re.split(',| ', pos_ans))
                if answer in corr_ans and answer != '':
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

            # Print correct answer
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
    def __init__(self, game, q_panel, trainer, dictionary, *args, **kwargs):
        self.game = game
        self.q_panel = q_panel
        self.trainer = trainer
        self.dict = dictionary
        self.q_panel.parent.title_frame.configure(bg='#ffdfba')
        self.q_panel.parent.title_frame.word_lbl.configure(bg='#ffdfba')
        question.__init__(self, 'verb', *args, **kwargs)

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

        self.get_all_conjugations()
        self.choose_poss_conjugations('verb')
        self.add_poss_forms()
    
    # Gets all requested conjugations
    def get_all_conjugations(self):

        # List of all requested conjugations
        self.forms = []
        
        # Get active tenses
        all_tenses = ['pr', 'pa', 'f', 'c', 'i', 'par', 'v']
        tenses = []
        for i, case_var in enumerate(self.trainer.tense_vars):
            if case_var.get():
                tenses.append(all_tenses[i])

        # Get aspect
        aspect = get_derived_word(self.dict, self.word, 'verb', 'asp')
        if 'i' not in aspect and 'pr' in tenses:
            tenses.remove('pr')
            if len(tenses) == 0:
                tenses.append('f')
        
        # Choose possible participle tense
        if 'par' in tenses:
            tenses.remove('par')
            if self.word == 'być':
                tenses.append(['par-act', 'par-cont', 'par-ant'][random.randint(0,2)])
            else:
                poss_tenses = ['par-pas']
                if 'i' in aspect:
                    poss_tenses += ['par-act', 'par-cont']
                if 'p' in aspect:
                    poss_tenses += ['par-ant']
                tenses.append(poss_tenses[random.randint(0,len(poss_tenses)-1)])

        # Loop tenses
        for tense in tenses:

            # Choose possible voices
            if tense in ['pr', 'pa', 'f', 'c']:
                if self.word == 'być' or self.trainer.excl_impers.get():
                    voices = ['1s', '2s', '3s', '1p', '2p', '3p']
                else:
                    voices = ['1s', '2s', '3s', '1p', '2p', '3p', 'i']
            elif tense == 'i':
                if self.trainer.excl_niech.get():
                    voices = ['2s', '1p', '2p']
                else:
                    voices = ['1s', '2s', '3s', '1p', '2p', '3p']
            else:
                voices = ['-']

            # Loop voices
            for voice in voices:

                # Choose gender
                if tense in ['pa', 'f', 'c'] and voice != 'i':
                    if tense == 'f' and ('i' not in aspect or self.word == 'być'):
                        gens = ['-']
                    elif 's' in voice:
                        gens = ['m', 'f', 'n']
                    elif 'p' in voice:
                        gens = ['v', 'nv']
                    else:
                        gens = ['m', 'f', 'n', 'v', 'nv']
                elif tense in ['par-act', 'par-pas']:
                    gens = ['m', 'f', 'n', 'v', 'nv'][random.randint(0,4)]
                else:
                    gens = ['-']

                # Loop genders and form all combinations
                for gen in gens:
                    self.forms.append(gen+'_'+voice+'_'+tense)
    
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
            self.load_conjugation()

# Load adjective questions
class adj_question(question):
    def __init__(self, game, q_panel, trainer, dictionary, *args, **kwargs):
        self.game = game
        self.q_panel = q_panel
        self.trainer = trainer
        self.dict = dictionary
        self.q_panel.parent.title_frame.configure(bg='#ffffba')
        self.q_panel.parent.title_frame.word_lbl.configure(bg='#ffffba')
        question.__init__(self, 'adj', *args, **kwargs)

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

        self.get_all_declensions()
        self.choose_poss_declensions('adj')
        self.add_poss_forms()

    # Gets all requested declensions
    def get_all_declensions(self):

        # List of all requested declensions
        self.forms = []

        # Virile nominative only
        if self.trainer.case_vars[0].get():
            self.forms = ['pv_n']

        else:
            # Get active cases
            all_cases = ['n', 'g', 'd', 'a', 'i', 'l', 'v']
            cases = []
            for i, case_var in enumerate(self.trainer.case_vars[1]):
                if case_var.get():
                    cases.append(all_cases[i])
            
            # Form all combinations
            for case in cases:
                for gen in ['sma', 'smi', 'sf', 'sn', 'pv', 'pnv']:
                    self.forms.append(gen+'_'+case)
    
    # Load next subquestion
    def next_subquestion(self):

        # Check if end of sub questions
        if len(self.sub_qs) == 0 or self.skip==True:
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
            self.load_declension()

# Load noun questions
class noun_question(question):
    def __init__(self, game, q_panel, trainer, dictionary, *args, **kwargs):
        self.game = game
        self.q_panel = q_panel
        self.trainer = trainer
        self.dict = dictionary
        self.q_panel.parent.title_frame.configure(bg='#baffc9')
        self.q_panel.parent.title_frame.word_lbl.configure(bg='#baffc9')
        question.__init__(self, 'noun', *args, **kwargs)

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

        self.get_all_declensions()
        self.choose_poss_declensions('noun')
        self.add_poss_forms()

    # Choose declensions to ask
    def get_all_declensions(self):

        # List of all requested declensions
        self.forms = []
        
        # Get active cases
        all_cases = ['n', 'g', 'd', 'a', 'i', 'l', 'v']
        cases = []
        for i, case_var in enumerate(self.trainer.case_vars):
            if case_var.get():
                cases.append(all_cases[i])
        
        # Form all combinations
        for case in cases:
            for gen in ['s', 'p']:
                self.forms.append(gen+'_'+case)
        if self.trainer.excl_singnom.get() and 's_n' in self.forms:
            self.forms.remove('s_n')
    
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
            self.load_declension()