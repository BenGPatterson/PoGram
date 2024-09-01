# -*- coding: utf-8 -*-

import json
import tkinter as tk
from custom_widgets import Entrybutton
from dictionary import load_dictionary
from game import run_game

class menu_display(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.config = kwargs.pop('config')
        self.bga = kwargs.pop('bga', None)
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.bg = self.cget('bg')
        self.grid_columnconfigure((0,1), weight=1, uniform='column')

        # Row weights
        self.grid_rowconfigure(0, weight=50)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Load general settings
        self.q_no = tk.StringVar(value=self.config['q_no'])
        q_no = Entrybutton(self, variable=None, text=f'Questions:', textvariable=self.q_no,
                                  btn_type='label', e_width=2, justify='right', int_only=True, bounded=True, bg=self.bg)
        q_no.grid(row=1, column=0, columnspan=2, padx=(5,0), sticky='w')

        # Load play button
        self.play_btn = tk.Button(self, text='Play', command=lambda: self.launch_game(parent, controller), bg=self.bga, activebackground=self.bga)
        self.play_btn.grid(row=2, column=0, columnspan=2, padx=(5,0), sticky='ew')

    # Load dictionary when instructed in start up
    def load_dict(self, path):
        self.word_dict = 'test' # load_dictionary(path)

    # Launch game
    def launch_game(self, parent, controller):
        self.save_config(parent)
        run_game(parent, controller)

    # Get current config settings to be saved
    def get_config(self):

        # Collect settings
        config = {}
        config['q_no'] = self.q_no.get()

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
        with open('trainer_config.json', 'w') as outfile: 
            json.dump(config, outfile)