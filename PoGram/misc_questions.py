import random
from questions import question

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

    