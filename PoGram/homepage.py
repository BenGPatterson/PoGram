# -*- coding: utf-8 -*-

import json
import tkinter as tk
from trainer_panels import misc_trainer, verb_trainer, adj_trainer, noun_trainer
from menu_panel import menu_display

# Home page showing trainer settings
class HomePage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        # Grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='column')

        # Title
        title = tk.Label(self, text='Options', font=('Segoe UI', 22))
        title.grid(row=0, column=0, columnspan=5, padx=10, pady=0, sticky='nw')
        
        # Create trainer and menu frames
        with open('trainer_config.json') as json_file:
            trainer_config = json.load(json_file)
        self.misc_frame = misc_trainer(self, bg='#ffb3ba', config=trainer_config['misc'])
        self.misc_frame.grid(row=1, column=0, padx=(10, 5), pady=(10, 20), sticky='nsew')
        self.verb_frame = verb_trainer(self, bg='#ffdfba', config=trainer_config['verb'])
        self.verb_frame.grid(row=1, column=1, padx=5, pady=(10, 20), sticky='nsew')
        self.adj_frame = adj_trainer(self, bg='#ffffba', config=trainer_config['adj'])
        self.adj_frame.grid(row=1, column=2, padx=5, pady=(10, 20), sticky='nsew')
        self.noun_frame = noun_trainer(self, bg='#baffc9', config=trainer_config['noun'])
        self.noun_frame.grid(row=1, column=3, padx=5, pady=(10, 20), sticky='nsew')
        self.menu_frame = menu_display(self, controller, bg='#bae1ff', config=trainer_config['menu'])
        self.menu_frame.grid(row=1, column=4, padx=(5,10), pady=(10, 20), sticky='nsew')

# Loading page when program first opens
class LoadingPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        # Loading text
        label = tk.Label(self, text='Loading...', font=('Segoe UI', 64))
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
