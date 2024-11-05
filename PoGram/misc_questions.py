import random
from questions import question
from dictionary import get_declension

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
                digits = int(self.trainer.digits_no.get())
                word_list = [str(num) for num in range(10**(digits-1), 10**(digits))]
                if digits == 1:
                    if self.qtype in ['Card', 'Ordi']:
                        word_list.append('0')
                    else:
                        word_list = word_list[1:]
                if self.qtype == 'Ordi':
                    word_list = [num+'.' for num in word_list]
            case 'Dwa':
                word_list = ['dwa', 'oba', 'obydwa', 'dwoje', 'oboje', 'obydwoje']
            case 'Oqua':
                word_list = ['kilka', 'parę', 'wiele', 'ile', 'tyle', 
                             'kilkanaście', 'kilkadziesiąt', 'kilkaset', 'paręnaście', 'parędziesiąt', 'paręset']
            case 'Wini':
                word_list = ['winien', 'powinien']
            case 'Prep':
                self.load_prep_dict()
                word_list = list(self.prep_dict.keys())

        # Set word list
        self.game.word_lists['misc'][self.qtype] = word_list
        self.game.current_word_lists['misc'][self.qtype] = []

    # Load dictionary of prepositions, cases, and definitions
    def load_prep_dict(self):
        pass
        # Get data from https://courseofpolish.com/grammar/cases/cases-after-prepositions/list-of-prepositions

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
            case 'Card'|'Coll'|'Ordi':
                pass
            case 'Dwa':
                pass
            case 'Oqua':
                self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l'], ['pv', 'pnv'])
                self.choose_poss_oqua_declensions()
            case 'Wini':
                pass
            case 'Prep':
                pass

        # Add to subquestions list
        self.add_poss_forms()

        # Ask about noun phrase after numerals/quantifiers
        if self.trainer.qs['Nphr'].get() and self.qtype in ['Card', 'Coll', 'Ordi', 'Dwa', 'Oqua']:
            self.add_noun_phrase_subq()

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
            self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l', 'v'], ['s'])
        elif self.word in ['panowie', 'państwo', 'panie']:
            self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l', 'v'], ['p'])
        else:

            # Add long/clitic/preposition options for familiar forms
            self.forms = []
            cases = ['n', 'g', 'd', 'a', 'i', 'l', 'v']
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

        for f, cf in zip(self.forms, self.correct_forms):
            print(f'{f}: {cf}, ', end='')
        print('\n')

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

    # Choose subquestions for interrogative pronouns word type
    def choose_inte_subqs(self):

        # Get all declensions
        self.get_all_case_gen_declensions(['n', 'g', 'd', 'a', 'i', 'l', 'v'], ['s'])

        # Get answers and keep only possible declensions
        if self.word in ['kto', 'nic', 'nikt']:
            self.choose_poss_declensions('noun')
        else:
            self.choose_poss_declensions('pron')

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
        
        for f, cf in zip(self.forms, self.correct_forms):
            print(f'{f}: {cf}, ', end='')
        print('\n')

        # Remove forms without answers
        for i in range(len(self.forms)-1,-1,-1):
            if self.correct_forms[i] == [None]:
                self.correct_forms.pop(i)
                self.forms.pop(i)

    # Adds subquestion about noun phrase after numeral/quantifier
    def add_noun_phrase_subq(self):

        # Add questions
        self.sub_qs += ['nphr_case', 'nphr_num']

        # Get default settings
        case = self.sub_qs[-3][-1]
        if 's' in self.sub_qs[-3]:
            num = 's'
        else:
            num = 'p'

        # All other quantifiers are special if nominative or accusative
        if self.qtype == 'Oqua' and case in ['n', 'a']:
            case = 'g'
            num = 's'

        # Add correct answers
        case_longhand = {'n': 'nominative', 'g': 'genitive', 'd': 'dative', 'a': 'accusative', 
                         'i': 'instrumental', 'l': 'locative', 'v': 'vocative'}
        num_longhand = {'s': 'singular', 'p': 'plural'}
        self.correct.append([case, case_longhand[case]])
        self.correct.append([num, num_longhand[num]])

    # Load noun phrase question
    def load_noun_phrase(self):

        # Loads subquestion
        nphr_text = {'nphr_case': 'Case of noun:', 'nphr_num': 'Grammatical number of noun phrase:'}
        self.load_subquestion(nphr_text[self.sub_qs[0]], self.correct[0], self.simple_correct)
        self.sub_qs = self.sub_qs[1:]
        self.correct = self.correct[1:]

    # Load next subquestion
    def next_subquestion(self):

        # Check if end of sub questions
        if len(self.sub_qs) == 0 or self.skip==True:
            self.end_question()
            return
        
        # Noun phrase questions
        if self.sub_qs[0] in ['nphr_case', 'nphr_num']:
            self.load_noun_phrase()
        
        # Load subquestion depending on question type
        else:
            match self.qtype:
                case 'Pers':
                    self.load_declension(disable_numgen=True)
                case 'Poss'|'Demo'|'Inte'|'Opro'|'Oqua':
                    self.load_declension()
                case 'Card'|'Coll'|'Ordi':
                    pass
                case 'Dwa':
                    pass
                case 'Wini':
                    pass
                case 'Prep':
                    pass

    