import tkinter as tk
import random

# Base class for all question loaders
class question():
    def __init__(self, *args, **kwargs):
        self.choose_word()

    # Choose word and update title
    def choose_word(self):
        self.word = self.word_list[random.randint(0,len(self.word_list)-1)]
        self.q_panel.parent.title_frame.word.set(self.word)
        self.q_panel.parent.title_frame.update()

# Load adjective questions
class adj_question(question):
    def __init__(self, q_panel, trainer, word_list, *args, **kwargs):
        self.q_panel = q_panel
        self.trainer = trainer
        self.word_list = word_list
        question.__init__(self, *args, **kwargs)

        # Decide subquestions
        self.sub_qs = []
        if self.trainer.qs[2].get():
            self.choose_declensions()
        if self.trainer.qs[1].get():
            if self.trainer.adverbs.get():
                self.sub_qs.append('adv')
            self.sub_qs.append(['comp', 'super'][random.randint(0,1)])
        if self.trainer.qs[0].get():
            self.sub_qs.append('def')

        # Load first subquestion
        self.next_subquestion()

    # Choose declensions to ask
    def choose_declensions(self):

        # Virile nominative only
        if self.trainer.case_vars[0].get():
            return ['pv_n']*int(self.trainer.inflections_no.get())
        
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
        pass
            
        