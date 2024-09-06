import tkinter as tk

# Base class for all question loaders
class question():
    def __init__(self, *args, **kwargs):
        pass

class adj_question(question):
    def __init__(self, *args, **kwargs):
        question.__init__(self, *args, **kwargs)