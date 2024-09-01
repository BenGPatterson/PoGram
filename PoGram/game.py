# -*- coding: utf-8 -*-

import tkinter as tk

def launch_game(parent, controller):

    # Sense check settings and find active trainers
    active = sense_check(parent)
    if active is None:
        return

    # Load game page
    controller.show_frame('game')

# Checks valid trainer settings and gets active trainers
def sense_check(parent):
    
    # Get active trainers and check at least one exists
    trainers = {'misc': parent.misc_frame, 'verb': parent.verb_frame, 'adj': parent.adj_frame, 'noun': parent.noun_frame}
    active = {}
    for key in trainers.keys():
        if trainers[key].active.get():
            active[key] = trainers[key]
    if len(active) == 0:
        tk.messagebox.showerror('Error', 'No trainers selected')
        return None
    
    # Checks all entry variables for positive integers
    for key in active.keys():
        if key == 'misc':
            continue

        # Check inflections entry if selected
        if active[key].qs[2].get():
            inflections_no = active[key].inflections_no.get()
            if not check_pos_int_entry(inflections_no):
                return None
        
        # Check word list freq entry if selected
        if active[key].word_list.get() == 'freq':
            freq_no = active[key].inflections_no.get()
            if not check_pos_int_entry(freq_no):
                return None
            
    # Check question number entry
    w_no = parent.menu_frame.w_no.get()
    if not check_pos_int_entry(w_no):
        return None
    
    return active

# Checks entry string for positive integer
def check_pos_int_entry(string):
    try:
        string = int(string)
    except:
        string = 0
    if string < 1:
        tk.messagebox.showerror('Error', 'Please enter a positive integer')
        return 0
    return 1