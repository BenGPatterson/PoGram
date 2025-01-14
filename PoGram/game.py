# -*- coding: utf-8 -*-

import tkinter as tk
import random
import os
import pandas as pd
from questions import verb_question, adj_question, noun_question
from misc_questions import misc_question

# Game instance
class Game():
    def __init__(self, dictionary, parent, controller):
        self.dict = dictionary
        self.parent = parent
        self.controller = controller

        # Sense check settings and find active trainers
        self.sense_check(parent)
        if self.trainers is None:
            return
        parent.menu_frame.save_config(parent)

        # Load game page and get canvas
        controller.show_frame('game')
        self.q_panel = controller.frames['game'].question_frame
        self.q_panel.q_frame_update()

        # Set initial variables and loads first question
        self.current_word_no = 0
        self.total_correct = 0
        self.total_questions = 0
        self.word_lists = {'misc': {}}
        self.current_word_lists = {'misc': {}}
        self.misc_qtypes = []
        self.current_misc_qtypes = []

        # Loads on screen word counter and next question
        self.word_counter = tk.StringVar(value=f'{self.current_word_no}/{int(self.parent.menu_frame.w_no.get())}')
        try:
            self.q_panel.counter_lbl.configure(textvariable=self.word_counter)
        except:
            self.q_panel.counter_lbl = tk.Label(self.q_panel, textvariable=self.word_counter, font=('Segoe UI', 18))
            self.q_panel.counter_lbl.place(anchor=tk.NE, relx=0.98, rely=0.02)
        self.next_question()

    # Loads next question
    def next_question(self):
        
        # Update word counter, exit if limit reached
        self.current_word_no += 1
        if self.current_word_no > int(self.parent.menu_frame.w_no.get()):
            tk.messagebox.showinfo('Score', f'{self.total_correct} questions correct out of {self.total_questions}.')
            self.controller.show_frame('home')
            self.parent.menu_frame.play_btn.focus_set()
            return
        self.word_counter.set(f'{self.current_word_no}/{int(self.parent.menu_frame.w_no.get())}')
        
        # Select trainer to choose word from and load relevant word list
        train_key = list(self.trainers.keys())[random.randint(0,len(self.trainers)-1)]
        if train_key not in self.word_lists.keys():
            self.load_word_list(train_key, self.controller)

        # Load question
        self.load_question(train_key)

    # Load word list
    def load_word_list(self, key, controller):

        # No word list required for miscellaneous questions
        if key != 'misc':

            # Load custom list if requested
            if self.trainers[key].word_list.get() == 'custom':
                try:
                    file = pd.read_csv(self.trainers[key].custom_list, header=0)
                except:
                    tk.messagebox.showerror('Error', f'Custom word list at {self.trainers[key].custom_list} not found')
                    controller.show_frame('home')
                    return
            
            # Otherwise load from default location
            else:
                file_path = os.path.join('PoGram', 'data', f'all_{key}.csv')
                file = pd.read_csv(file_path, header=0)

                # Apply frequency cut if requested
                if self.trainers[key].word_list.get() == 'freq':
                    file = file[:int(self.trainers[key].freq_no.get())]

            # Save word list
            self.word_lists[key] = list(file['lemma'])
            self.current_word_lists[key] = []

    # Load question
    def load_question(self, key):
        question_loaders = {'misc': misc_question, 'verb': verb_question, 'adj': adj_question, 'noun': noun_question}
        question_loaders[key](self, self.q_panel, self.trainers[key], self.dict)

    # Checks valid trainer settings and gets active trainers
    def sense_check(self, parent):
        
        # Get active trainers and check at least one exists
        trainers = {'misc': parent.misc_frame, 'verb': parent.verb_frame, 'adj': parent.adj_frame, 'noun': parent.noun_frame}
        self.trainers = {}
        for key in trainers.keys():
            if trainers[key].active.get():
                self.trainers[key] = trainers[key]
        if len(self.trainers) == 0:
            tk.messagebox.showerror('Error', 'No trainers selected')
            self.trainers = None
            return
        
        # Checks all entry variables for positive integers
        for key in self.trainers.keys():

            # Check inflections entry if selected
            if key == 'misc' or self.trainers[key].qs[2].get():
                inflections_no = self.trainers[key].inflections_no.get()
                if not self.check_pos_int_entry(inflections_no):
                    self.trainers = None
                    return
            
            # Check word list freq entry if selected
            if key != 'misc':
                if self.trainers[key].word_list.get() == 'freq':
                    freq_no = self.trainers[key].freq_no.get()
                    if not self.check_pos_int_entry(freq_no):
                        self.trainers = None
                        return
            else:
                digits_no = self.trainers[key].digits_no.get()
                if not self.check_pos_int_entry(digits_no):
                    self.trainers = None
                    return
                
        # Check question number entry
        w_no = parent.menu_frame.w_no.get()
        if not self.check_pos_int_entry(w_no):
            self.trainers = None
            return None
        
        # Warning about present only for perfective verbs
        if 'verb' in self.trainers:
            tenses = [tense.get() for tense in self.trainers['verb'].tense_vars]
            if self.trainers['verb'].qs[2].get() == 1 and tenses == [1,0,0,0,0,0,0]:
                tk.messagebox.showwarning('Warning', 'Perfective verbs will ask for future tense instead of present')

    # Checks entry string for positive integer
    def check_pos_int_entry(self, string):
        try:
            string = int(string)
        except:
            string = 0
        if string < 1:
            tk.messagebox.showerror('Error', 'Please enter a positive integer')
            return 0
        return 1        