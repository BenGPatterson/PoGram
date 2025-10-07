# -*- coding: utf-8 -*-

import json
import tkinter as tk
import os
from custom_widgets import Entrybutton
from dictionary import load_dictionary
from game import Game

class menu_display(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.config = kwargs.pop('config')
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.bg = kwargs.get('bg', self.cget('bg'))
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0,1), weight=1, uniform='column')

        # Load general settings
        self.w_no = tk.StringVar(value=self.config['w_no'])
        w_no = Entrybutton(self, variable=None, text=f'Words:', textvariable=self.w_no, btn_type='label', 
                           e_width=2, justify='right', int_only=True, bounded=True, bg=self.bg)
        w_no.grid(row=2, column=0, columnspan=2, padx=(30,0), pady=(0,10), sticky='w')

        # Load play button
        self.play_btn = tk.Button(self, text='Play', command=lambda: self.start_game(parent, controller))
        self.play_btn.grid(row=3, column=0, columnspan=2, padx=30, pady=(0,10), sticky='ew')
        self.play_btn.bind('<Return>', lambda event: self.start_game(parent, controller))

    # Load dictionary when instructed in start up
    def load_dict(self, path):
        self.word_dict = load_dictionary(path)

    # Launch game
    def start_game(self, parent, controller):
        controller.current_game = Game(self.word_dict, parent, controller)

    # Get current config settings to be saved
    def get_config(self):

        # Collect settings
        config = {}
        config['w_no'] = self.w_no.get()

        return config

    # Save trainer panel config
    def save_config(self, parent):
        
        # Get current config settings for each trainer
        config = {}
        trainers = ['misc', 'verb', 'adj', 'noun', 'menu']
        trainer_frames = [parent.misc_frame, parent.verb_frame, parent.adj_frame , parent.noun_frame, self]
        for trainer, trainer_frame in zip(trainers, trainer_frames):
            config[trainer] = trainer_frame.get_config()

        # Save new config
        config_path = os.path.join('PoGram', 'trainer_config.json')
        with open(config_path, 'w') as outfile: 
            json.dump(config, outfile)