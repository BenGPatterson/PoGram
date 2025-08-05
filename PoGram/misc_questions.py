import tkinter as tk
import random
import pandas as pd
import os
import re
from ast import literal_eval
from questions import question
from dictionary import get_declension, get_def_conjugation, get_card_comp_declension

# Load misc questions
class misc_question(question):
    def __init__(self, game, q_panel, trainer, dictionary, *args, **kwargs):
        self.game = game
        self.q_panel = q_panel
        self.trainer = trainer
        self.dict = dictionary
        self.q_panel.parent.title_frame.configure(bg='#ffb3ba')
        self.q_panel.parent.title_frame.word_lbl.configure(bg='#ffb3ba')
        question.__init__(self, 'misc', *args, **kwargs)

        # Decide question type and word
        self.choose_qtype()
        self.choose_word()

        # Decide subquestions
        self.sub_qs = []
        self.choose_subqs()

        # Load first subquestion
        self.next_subquestion()

    # Choose question type from those active
    def choose_qtype(self):

        # Get active question types if not already calculated
        if len(self.game.misc_qtypes) == 0:
            for key in self.trainer.link_keys:
                if self.trainer.qs[key].get():
                    self.game.misc_qtypes.append(key)

        # Randomise order if current question type list is empty
        if len(self.game.current_misc_qtypes) == 0:
            random.shuffle(self.game.misc_qtypes)
            self.game.current_misc_qtypes = self.game.misc_qtypes.copy()

        # Pick next question type
        self.qtype = self.game.current_misc_qtypes[0]
        self.game.current_misc_qtypes = self.game.current_misc_qtypes[1:]

    # Choose word
    def choose_word(self):

        # Create word list if does not already exist
        if self.qtype not in self.game.word_lists['misc'].keys():
            self.create_word_list()
        
        # Randomise order if word list is empty
        if len(self.game.current_word_lists['misc'][self.qtype]) == 0:
            random.shuffle(self.game.word_lists['misc'][self.qtype])
            self.game.current_word_lists['misc'][self.qtype] = self.game.word_lists['misc'][self.qtype].copy()

        # Pick next word
        self.word = self.game.current_word_lists['misc'][self.qtype][0]
        self.game.current_word_lists['misc'][self.qtype] = self.game.current_word_lists['misc'][self.qtype][1:]

        # Update title with new word
        self.q_panel.parent.title_frame.word.set(self.word)
        self.q_panel.parent.title_frame.update()

    # Create word list
    def create_word_list(self):

        # Find word list for each question type
        match self.qtype:
            case 'Pers':
                word_list = ['ja', 'ty', 'pan', 'pani', 'on', 'ono', 'ona', 
                             'my', 'wy', 'panowie', 'państwo', 'panie', 'oni', 'one']
            case 'Poss':
                word_list = ['mój', 'twój', 'swój', 'nasz', 'wasz']
            case 'Demo':
                word_list = ['ten', 'tamten']
            case 'Inte':
                word_list = ['co', 'kto', 'coś', 'ktoś', 'cokolwiek', 'ktokolwiek', 'nic', 'nikt']
            case 'Opro':
                word_list = ['który', 'wszystek', 'każdy', 'żaden', 'się']
            case 'Card'|'Coll'|'Ordi':
                word_list = self.create_num_word_list()
            case 'Dwa':
                word_list = ['dwa', 'oba', 'obydwa', 'dwoje', 'oboje', 'obydwoje']
            case 'Nnum':
                word_list = [str(num)+' (noun)' for num in range(0,13)]
            case 'Oqua':
                word_list = ['kilka', 'parę', 'wiele', 'ile', 'tyle', 
                             'kilkanaście', 'kilkadziesiąt', 'kilkaset',
                             'paręnaście', 'parędziesiąt', 'paręset']
            case 'Wini':
                word_list = ['winien', 'powinien']
            case 'Prep':
                word_list = self.load_prep_csv()

        # Set word list
        self.game.word_lists['misc'][self.qtype] = word_list
        self.game.current_word_lists['misc'][self.qtype] = []

    # Create word list for numeral options
    def create_num_word_list(self):

        # Add all values for each qtype
        sfs = {'Card': 3, 'Coll': 1, 'Ordi': 2}
        word_list = [str(i) for i in range(0, 10**sfs[self.qtype]+1)]
        if self.qtype == 'Coll':
            word_list = word_list[2:]
        elif self.qtype == 'Ordi':
            word_list += [str(num*100) for num in range(2, 11)]

        # Add digit separators
        word_list = [re.sub(r"(\d)(?=(\d{3})+(?!\d))", r"\1 ", "%d" % int(num)) for num in word_list]

        # Add periods for ordinal numerals and collective tag for collective numerals
        if self.qtype == 'Coll':
            word_list = [num+' (collective)' for num in word_list]
        elif self.qtype == 'Ordi':
            word_list = [num+'.' for num in word_list]

        return word_list

    # Load csv of prepositions, cases, and definitions
    def load_prep_csv(self):
        
        # Load raw preposition data
        self.game.prep_data = pd.read_csv(os.path.join('PoGram', 'data', 'prep_cases.csv'), converters={'prep_en': literal_eval, 'cases': literal_eval})

        # Create word list
        word_list = []
        for prep in list(self.game.prep_data['prep_pl']):
            if len(list(self.game.prep_data.loc[self.game.prep_data['prep_pl']==prep]['cases'])[0]) == 1:
                word_list.append(prep)
            else:
                word_list += [f'{prep} (movement)', f'{prep} (no movement)']

        return word_list

    # Choose subquestions to ask
    def choose_subqs(self):

        # Choose sub questions depending on question type
        match self.qtype:
            case 'Pers':
                self.get_all_pers_declensions()
                self.choose_poss_pers_declensions()
            case 'Poss'|'Demo':
                self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l'], ['sma', 'smi', 'sf', 'sn', 'pv', 'pnv'])
                self.choose_poss_declensions('pron')
            case 'Inte':
                self.choose_inte_subqs()
            case 'Opro':
                self.choose_opron_subqs()
            case 'Card':
                self.get_all_card_declensions()
                self.choose_poss_card_declensions()
            case 'Coll'|'Ordi':
                pass
            case 'Dwa':
                pass
            case 'Nnum':
                self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l', 'v'], ['s', 'p'])
                self.choose_poss_nnum_declensions()
            case 'Oqua':
                self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l'], ['pv', 'pnv'])
                self.choose_poss_oqua_declensions()
            case 'Wini':
                self.get_all_wini_conjugations()
                self.choose_poss_wini_conjugations()
            case 'Prep':
                self.sub_qs += ['prep_def', 'prep_case']

        # Add to subquestions list
        if self.qtype != 'Prep':
            self.add_poss_forms()

    # Get all declensions for requested cases and genders
    def get_all_case_gen_declensions(self, cases, gens):

        # List of all requested declensions
        self.forms = []
        
        # Form all combinations
        for case in cases:
            for gen in gens:
                self.forms.append(gen+'_'+case)

    # Get all declensions of personal pronouns
    def get_all_pers_declensions(self):

        # Get all declensions for polite forms
        if self.word in ['pan', 'pani']:
            self.get_all_case_gen_declensions(['g', 'd', 'a', 'i', 'l', 'v'], ['s'])
        elif self.word in ['panowie', 'państwo', 'panie']:
            self.get_all_case_gen_declensions(['g', 'd', 'a', 'i', 'l', 'v'], ['p'])
        else:

            # Add long/clitic/preposition options for familiar forms
            self.forms = []
            cases = ['g', 'd', 'a', 'i', 'l']
            if self.word in ['ja', 'ty', 'on', 'ono', 'ona']:
                gens = ['s']
            elif self.word in ['my', 'wy', 'oni', 'one']:
                gens = ['p']
            for form in ['l', 'c', 'p']:
                for case in cases:
                    for gen in gens:
                        self.forms.append(gen+'_'+case+'_'+form)

    # Keeps only declensions with answers available for personal pronouns
    def choose_poss_pers_declensions(self):

        # Lemmas to use for polite forms
        pol_lemma_dict = {'pan': 'pan', 'pani': 'pani', 'panowie': 'pan', 
                          'państwo': 'państwo', 'panie': 'pani'}

        # Correct answers for familiar 3rd person masculine singular pronoun 'on'
        on_correct_dict = {'n_l': ['on'], 'n_c': ['on'], 'n_p': ['on'],
                           'g_l': ['jego'], 'g_c': ['go'], 'g_p': ['niego'],
                           'd_l': ['jemu'], 'd_c': ['mu'], 'd_p': ['niemu'],
                           'a_l': ['jego'], 'a_c': ['go'], 'a_p': ['niego'],
                           'i_l': ['nim'], 'i_c': ['nim'], 'i_p': ['nim'],
                           'l_l': ['nim'], 'l_c': ['nim'], 'l_p': ['nim'],
                           'v_l': [None], 'v_c': [None], 'v_p': [None]}

        # Get all correct answers
        self.correct_forms = []
        for form in self.forms:

            # Polite form
            if self.word in ['pan', 'pani', 'panowie', 'państwo', 'panie']:
                numgen, case = form.split('_')
                try:
                    self.correct_forms.append(get_declension(self.dict, pol_lemma_dict[self.word], 'pron', numgen, case))
                except:
                    self.correct_forms.append([None])

            # Hardcoded for 'on' only
            elif self.word == 'on':
                self.correct_forms.append(on_correct_dict[form[2:]])

            # Includes long/clitic/preposition form
            else:
                numgen, case, lcp = form.split('_')
                try:
                    lcp_forms = get_declension(self.dict, self.word, 'pron', numgen, case)

                    if len(lcp_forms) == 1: # If all are the same
                        lcp_dict = {'l': 0, 'c': 0, 'p': 0}
                    elif len(lcp_forms) == 2 and self.word in ['ja', 'ty']: # If long clitic different, no preposition form
                        c = lcp_forms.index(min(lcp_forms, key=len))
                        lcp_dict = {'l': 1-c, 'c': c, 'p': 1-c}
                    elif len(lcp_forms) == 2 and self.word in ['ono', 'ona', 'oni', 'one']: # If long, clitic same, separate preposition form
                        p = [lcp_forms.index(x) for x in lcp_forms if x[0] == 'n'][0]
                        lcp_dict = {'l': 1-p, 'c': 1-p, 'p': p}
                    elif len(lcp_forms) == 3: # If all are different
                        c = lcp_forms.index(min(lcp_forms, key=len))
                        p = [lcp_forms.index(x) for x in lcp_forms if x[0] == 'n'][0]
                        lcp_dict = {'l': 3-c-p, 'c': c, 'p': p}

                    # Add correct form
                    self.correct_forms.append([lcp_forms[lcp_dict[lcp]]])
                except:
                    self.correct_forms.append([None])

                # 'mię' is now considered dated or dialectal
                if self.correct_forms[-1] == ['mię']:
                    self.correct_forms[-1].append('mnie')

        # Remove forms without answers
        for i in range(len(self.forms)-1,-1,-1):
            if self.correct_forms[i] == [None]:
                self.correct_forms.pop(i)
                self.forms.pop(i)

    # Choose subquestions for other pronouns word type
    def choose_opron_subqs(self):

        # Get all declensions
        if self.word == 'się':
            self.get_all_case_gen_declensions(['g', 'd', 'a', 'i', 'l'], ['-'])
        else:
            self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l'], ['sma', 'smi', 'sf', 'sn', 'pv', 'pnv'])

        # Get answers and keep only possible declensions
        if self.word in ['wszystek', 'żaden']:
            self.choose_poss_declensions('adj')
        else:
            self.choose_poss_declensions('pron')

    # Keeps only declensions with answers available for cardinal numerals
    def get_all_card_declensions(self):

        if self.word in ['0']:
            self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l'], ['s', 'p'])
        elif self.word in ['1']:
            self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l'], ['sma', 'smi', 'sf', 'sn', 'pv', 'pnv'])
        elif self.word[-1] == '2' and self.word[-2] != '1':
            self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l'], ['pv', 'pm', 'pf', 'pn'])
        else:
            self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l'], ['pv', 'pnv'])

    # Splits number into components
    def split_num(self):

        # Sanitize word to remove digit separators, ordinal marker
        word = re.sub('[ .]|\(.*', '', self.word)

        # Single digit case and one thousand case
        if word == '0':
            return ['zero']
        elif word == '1000':
            return ['tysiąc']

        # Identify number components
        num_comps = []
        while len(word) > 0:
            while len(word) > 0 and word[0] == '0':
                word = word[1:]
            if len(word) == 1:
                num_comps.append(int(word[0]))
                word = word[1:]
            elif len(word) == 2:
                if word[0] == '1' or word[1] == '0':
                    num_comps.append(int(word))
                else:
                    num_comps += [int(word[0])*10, int(word[1])]
                word = word[2:]
            elif len(word) == 3:
                num_comps.append(int(word[0])*100)
                word = word[1:]

        # Convert components from numbers to words
        conv_dict = {1: 'jeden', 2: 'dwa', 3: 'trzy', 4: 'cztery', 5: 'pięć', 6: 'sześć', 7: 'siedem', 8: 'osiem', 9: 'dziewięć', 10: 'dziesięć',
                     11: 'jedenaście', 12: 'dwanaście', 13: 'trzynaście', 14: 'czternaście', 15: 'piętnaście', 16: 'szesnaście', 
                     17: 'siedemnaście', 18: 'osiemnaście', 19: 'dziewiętnaście', 20: 'dwadzieścia', 30: 'trzydzieści', 40: 'czterdzieści',
                     50: 'pięćdziesiąt', 60: 'sześćdziesiąt', 70: 'siedemdziesiąt', 80: 'osiemdziesiąt', 90: 'dziewięćdziesiąt', 100: 'sto',
                     200: 'dwieście', 300: 'trzysta', 400: 'czterysta', 500: 'pięćset', 600: 'sześćset', 700: 'siedemset', 800: 'osiemset', 
                     900: 'dziewięćset'}
        word_comps = [conv_dict[num] for num in num_comps]

        return word_comps
    
    # Works out correct declensions for cardinal numerals
    def choose_poss_card_declensions(self):

        # Split number into components
        comps = self.split_num()

        # Work out which components to inflect in loose case
        loose_infl = [False for _ in range(len(comps))]
        if len(comps) == 1:
            loose_infl[-1] = True
        elif comps[-1] == 'jeden':
            loose_infl[-2] = True
        else:
            loose_infl[-1] = True
            units_check = comps[-1] in ['dwa', 'trzy', 'cztery', 'pięć', 'sześć', 'siedem', 'osiem', 'dziewięć']
            tens_check = comps[-2] in ['dwadzieścia', 'trzydzieści', 'czterdzieści', 'pięćdziesiąt',
                                       'sześćdziesiąt', 'siedemdziesiąt', 'osiemdziesiąt', 'dziewięćdziesiąt']
            if units_check and tens_check:
                loose_infl[-2] = True
        
        # Get all correct answers
        self.correct_forms = []
        for form in self.forms:
            numgen, case = form.split('_')
            self.correct_forms.append(get_card_comp_declension(self.dict, comps, loose_infl, numgen, case))
            
        # Remove forms without answers
        for i in range(len(self.forms)-1,-1,-1):
            if self.correct_forms[i] == [None]:
                self.correct_forms.pop(i)
                self.forms.pop(i)
        
    # Choose subquestions for interrogative pronouns word type
    def choose_inte_subqs(self):

        # Get all declensions
        self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l', 'v'], ['s'])

        # Get answers and keep only possible declensions
        if self.word in ['kto', 'nic', 'nikt']:
            self.choose_poss_declensions('noun')
        else:
            self.choose_poss_declensions('pron')

    # Keeps only declensions with answers available for numeral nouns
    def choose_poss_nnum_declensions(self):

        # Find base polish form from number
        num = int(self.word.split(' ')[0])
        words = {0: 'zero', 1: 'jedynka', 2: 'dwójka', 3: 'trójka', 4: 'czwórka',
                 5: 'piątka', 6: 'szóstka', 7: 'siódemka', 8: 'ósemka', 9: 'dziewiątka',
                 10: 'dziesiątka', 11: 'jedenastka', 12: 'dwunastka'}
        word = words[num]

        # Get all correct answers
        self.correct_forms = []
        for form in self.forms:
            numgen, case = form.split('_')
            try:
                if word != 'dwunastka':
                    self.correct_forms.append(get_declension(self.dict, word, 'noun', numgen, case))
                else:
                    correct_11 = get_declension(self.dict, 'jedenastka', 'noun', numgen, case)
                    correct_12 = ['dwu' + ans[4:] for ans in correct_11]
                    self.correct_forms.append(correct_12)
            except:
                self.correct_forms.append([None])

        # Remove forms without answers
        for i in range(len(self.forms)-1,-1,-1):
            if self.correct_forms[i] == [None]:
                self.correct_forms.pop(i)
                self.forms.pop(i)

    # Keeps only declensions with answers available for other quantifiers
    def choose_poss_oqua_declensions(self):

        # Correct answers for 'parę'
        parę_correct_dict = {'pv_n': ['parę'], 'pv_g': ['paru'], 'pv_d': ['paru'], 
                             'pv_a': ['parę'], 'pv_i': ['paroma'], 'pv_l': ['paru'],
                             'pnv_n': ['paru'], 'pnv_g': ['paru'], 'pnv_d': ['paru'], 
                             'pnv_a': ['paru'], 'pnv_i': ['paroma'], 'pnv_l': ['paru']}
        
        # Get all correct answers
        self.correct_forms = []
        for form in self.forms:

            # Hardcoded for 'parę'
            if self.word == 'parę':
                self.correct_forms.append(parę_correct_dict[form])

            # Otherwise handle normally
            else:
                numgen, case = form.split('_')
                try:
                    self.correct_forms.append(get_declension(self.dict, self.word, 'oqua', numgen, case))
                except:
                    self.correct_forms.append([None])

        # Remove forms without answers
        for i in range(len(self.forms)-1,-1,-1):
            if self.correct_forms[i] == [None]:
                self.correct_forms.pop(i)
                self.forms.pop(i)

    # Get all conjugations of winien-like verbs
    def get_all_wini_conjugations(self):

        # List of all requested conjugations
        self.forms = []

        # Form all combinations
        for tense in ['pr', 'pa']:
            for voice in ['1', '2', '3', 'i']:
                if voice == 'i':
                    gens = ['-']
                else:
                    gens = ['m', 'f', 'n', 'v', 'nv']
                for gen in gens:
                    self.forms.append(gen+'_'+voice+'_'+tense)

    # Keeps only conjugations with answers available for winien-like verbs
    def choose_poss_wini_conjugations(self):

        # Get all correct answers
        self.correct_forms = []
        for form in self.forms:
            gen, voice, case = form.split('_')
            try:
                self.correct_forms.append(get_def_conjugation(self.dict, self.word, gen, voice, case))
            except:
                self.correct_forms.append([None])

        # Remove forms without answers
        for i in range(len(self.forms)-1,-1,-1):
            if self.correct_forms[i] == [None]:
                self.correct_forms.pop(i)
                self.forms.pop(i)

    # Load preposition definition subquestion
    def load_prep_def(self):

        # Identifies version of preposition
        if '(movement)' in self.word:
            self.vers = 'mov'
            word = self.word[:-11]
        elif '(no movement)' in self.word:
            self.vers = 'nomov'
            word = self.word[:-14]
        else:
            self.vers = None
            word = self.word

        # Get correct definition(s)
        row = self.game.prep_data.loc[self.game.prep_data['prep_pl']==word]
        if self.vers == 'nomov':
            correct = list(row['prep_en'])[0][1].split(',')
            self.prep_correct_ans = correct + re.split(',| ', list(row['prep_en'])[0][1])
        else:
            correct = list(row['prep_en'])[0][0].split(',')
            self.prep_correct_ans = correct +  re.split(',| ', list(row['prep_en'])[0][0])
        correct = [ans.strip() for ans in correct]
        self.prep_correct_ans = [ans.strip() for ans in self.prep_correct_ans]

        # Loads subquestion
        self.load_subquestion('Definition:', correct, self.prep_def_correct)
        self.sub_qs = self.sub_qs[1:]

    # Check if preposition definition is correct
    def prep_def_correct(self, widget, answer, correct):

        # Only if first time called
        if widget['state'] != 'disabled':

            # Check correct
            self.game.total_questions += 1
            corr_bool = False
            if answer in self.prep_correct_ans and answer != '':
                corr_bool = True
            if corr_bool:
                widget.configure(disabledbackground='#98fb98')
                self.game.total_correct += 1
                self.btn_text = tk.StringVar(value='Mark incorrect')
            else:
                widget.configure(disabledbackground='#fa8072')
                self.btn_text = tk.StringVar(value='Mark correct')

            # Print correct answer
            self.def_widget = widget
            def_text = ''
            for ans in correct:
                def_text += ans + ', '
            def_text = def_text[:-2]
            correct_label = tk.Label(self.q_panel.q_frame, text=def_text, font=('Segoe UI', 14))
            correct_label.pack(side=tk.TOP)

            # Load button to toggle correct status
            btn_frame = tk.Frame(self.q_panel.q_frame)
            btn_frame.pack(side=tk.TOP)
            toggle = tk.Button(btn_frame, textvariable=self.btn_text, command=self.toggle_def, font=('Segoe UI', 10))
            toggle.grid(row=0, column=1, padx=10, sticky='ew')

            # Disable and load next question
            widget.configure(state='disable')
            self.q_panel.q_frame_update()
            self.next_subquestion()

    # Load preposition case subquestion
    def load_prep_case(self):

        # Identifies version of preposition
        if self.vers == 'mov':
            word = self.word[:-11]
        elif self.vers == 'nomov':
            word = self.word[:-14]
        else:
            word = self.word

        # Get correct case
        case_dict = {'n': 'nominative', 'a': 'accusative', 'g': 'genitive',
                     'd': 'dative', 'i': 'instrumental', 'l': 'locative'}
        row = self.game.prep_data.loc[self.game.prep_data['prep_pl']==word]
        if self.vers == 'nomov':
            case = list(row['cases'])[0][1]
        else:
            case = list(row['cases'])[0][0]
        correct = [case, case_dict[case]]
        
        # Loads subquestion
        self.load_subquestion('Case:', correct, self.simple_correct)
        self.sub_qs = self.sub_qs[1:]

    # Load next subquestion
    def next_subquestion(self):

        # Check if end of sub questions
        if len(self.sub_qs) == 0 or self.skip==True:
            self.end_question()
            return

        # Preposition sub questions
        elif self.sub_qs[0] == 'prep_def':
            self.load_prep_def()
        elif self.sub_qs[0] == 'prep_case':
            self.load_prep_case()
        
        # Load subquestion depending on question type
        else:
            match self.qtype:
                case 'Pers':
                    self.load_declension(disable_numgen=True)
                case 'Poss'|'Demo'|'Inte'|'Opro'|'Nnum'|'Oqua':
                    self.load_declension()
                case 'Card':
                    self.load_declension(wide_entry=170)
                case 'Card'|'Coll'|'Ordi':
                    pass
                case 'Dwa':
                    pass
                case 'Wini':
                    self.load_conjugation()

    