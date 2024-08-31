import json
import tkinter as tk
from trainer_panels import misc_trainer, verb_trainer, adj_trainer, noun_trainer

# Home page showing trainer settings
class HomePage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        # Grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='column')

        # Title
        title = tk.Label(self, text='PoGram', font=('Segoe UI', 22))
        title.grid(row=0, column=0, columnspan=5, padx=10, pady=0, sticky='nw')
        
        # Create trainer and menu frames
        with open('trainer_config.json') as json_file:
            trainer_config = json.load(json_file)
        self.misc_frame = misc_trainer(self, bga='#ffb3ba', config=trainer_config['misc'])
        self.misc_frame.grid(row=1, column=0, padx=(10, 5), pady=(10, 20), sticky='nsew')
        self.verb_frame = verb_trainer(self, bga='#ffdfba', config=trainer_config['verb'])
        self.verb_frame.grid(row=1, column=1, padx=5, pady=(10, 20), sticky='nsew')
        self.adj_frame = adj_trainer(self, bga='#ffffba', config=trainer_config['adj'])
        self.adj_frame.grid(row=1, column=2, padx=5, pady=(10, 20), sticky='nsew')
        self.noun_frame = noun_trainer(self, bga='#baffc9', config=trainer_config['noun'])
        self.noun_frame.grid(row=1, column=3, padx=5, pady=(10, 20), sticky='nsew')
        menu_frame = menu_display(self, bga='#bae1ff')
        menu_frame.grid(row=1, column=4, padx=30, pady=(10, 50), sticky='nsew')

class menu_display(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.bga = kwargs.pop('bga', None)
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.bg = self.cget('bg')

        # Load play button
        self.load_play(parent)

    # Load play button
    def load_play(self, parent):
        play_btn = tk.Button(self, text='Play', command=lambda: self.save_config(parent), bg=self.bga, activebackground=self.bga)
        play_btn.pack(fill='x', side='bottom')

    def save_config(self, parent):
        
        # Get current config settings for each trainer
        config = {}
        trainers = ['adj' , 'noun', 'verb', 'misc']
        trainer_frames = [parent.adj_frame , parent.noun_frame, parent.verb_frame, parent.misc_frame]
        for trainer, trainer_frame in zip(trainers, trainer_frames):
            config[trainer] = trainer_frame.get_config()

        # Save new config
        with open('trainer_config.json', 'w') as outfile: 
            json.dump(config, outfile)

        print('Saved')

