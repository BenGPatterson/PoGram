# -*- coding: utf-8 -*-

import tkinter as tk
import random
import os
import pandas as pd
from questions import verb_question, adj_question, noun_question

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

        # Set initial variables and load first question
        self.current_word_no = 0
        self.total_correct = 0
        self.total_questions = 0
        self.word_lists = {}
        self.current_word_lists = {}
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
        question_loaders = {'misc': adj_question, 'verb': verb_question, 'adj': adj_question, 'noun': noun_question}
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
            if key == 'misc':
                continue

            # Check inflections entry if selected
            if self.trainers[key].qs[2].get():
                inflections_no = self.trainers[key].inflections_no.get()
                if not self.check_pos_int_entry(inflections_no):
                    self.trainers = None
                    return
            
            # Check word list freq entry if selected
            if self.trainers[key].word_list.get() == 'freq':
                freq_no = self.trainers[key].inflections_no.get()
                if not self.check_pos_int_entry(freq_no):
                    self.trainers = None
                    return
                
        # Check question number entry
        w_no = parent.menu_frame.w_no.get()
        if not self.check_pos_int_entry(w_no):
            return None

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