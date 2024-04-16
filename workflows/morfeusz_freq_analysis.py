from morfeusz2 import Morfeusz
from concraft_pl2 import Concraft, Server # Requires concraft_pl2.py (https://github.com/kawu/concraft-pl) in the same directory
import os
import pandas as pd
import gc
import gzip
import pickle
import time

# Convert Morfeusz pos to wiktionary pos
pos_conv = {'adv': 'adv', 'imps': 'verb', 'inf': 'verb', 'prep': 'prep', 'praet': 'verb', 'bedzie': 'verb', 'pact': 'verb', 'ppas': 'verb', 
            'part': 'particle', 'winien': 'winien', 'adjp': 'adj', 'adjc': 'adj',
            'num': 'num', 'conj': 'conj', 'interj': 'intj', 'pred': 'def_verb', 'pcon': 'verb', 'comp': 'conj', 'pant': 'verb', 
            'fin': 'verb', 'ppron12': 'pron', 'siebie': 'pron', 'subst': 'noun', 'ger': 'verb',
            'adja': 'adj', 'adj': 'adj', 'impt': 'verb', 'aglt': 'verb', 'ppron3': 'pron'}

# Create empty dictionary for each wikitonary pos
word_freqs = {}
for i in set(pos_conv.values()):
    word_freqs[i] = {}

try:

    # Set up server
    print('Setting up concraft-pl server')
    morfeusz = Morfeusz(expand_tags=True)
    model_path = os.path.join('workflows', 'concraft-pl-model-SGJP-20220221.gz')
    concraft_path = 'C:\\Users\\xasde\\AppData\\Roaming\\local\\bin\\concraft-pl.exe'
    server = Server(model_path=model_path, concraft_path=concraft_path, port=3001)
    concraft = Concraft(server_addr='http://127.0.0.1', port=3001)
    
    # Loop over each sentence
    print('Analysing sentences', end='')
    start = time.time()
    sentences_path = os.path.join('workflows', 'pol-com_web_2018_1M-sentences.txt')
    with open(sentences_path, encoding="utf-8") as file:
        pos_dict = {}
        count = 0
        for line in file:

            # Analyse sentence
            sentence = line.split('\t')[1]
            dag = morfeusz.analyse(sentence)
            res = concraft.disamb(dag)

            # Add frequency of each possible lemma interpretation
            for item in res:
                try:
                    wiki_pos = pos_conv[item[2][2].split(':')[0]]
                    lemma = item[2][1].split(':')[0].lower()
                    prob = float(item[3])
                    try:
                        word_freqs[wiki_pos][lemma] += prob
                    except KeyError:
                        word_freqs[wiki_pos][lemma] = prob
                except:
                    pass
            
            # Progress bar
            count += 1
            if count%100 == 0:
                print(f'\rAnalysed {count} sentences', end='')
finally:
    server.terminate()
end = time.time()
print(f'\nAnalysis complete in {end-start} seconds')

# Load wiki pages for post-processing sanity checks
print('Loading dictionary')
data_path = os.path.join('data', 'wiki_entries.pgz')
gc.disable()
with gzip.open(data_path, "rb") as f:
    dictionary = pickle.load(f)
gc.enable()

del_word_freqs = []
del_word_lemmas = []
print('Performing sanity checks and saving data')
for key in word_freqs:
    del_words = []
    for lemma in word_freqs[key]:

        # Handle defective verbs in separate list
        if key == 'def_verb' or key == 'winien':
            wiki_pos = 'verb'
        else:
            wiki_pos = key

        # Round frequencies down to nearest integer, and cut below 5
        word_freqs[key][lemma] = int(word_freqs[key][lemma])
        if word_freqs[key][lemma] < 5:
            del_word_freqs.append(word_freqs[key][lemma])
            del_word_lemmas.append(lemma)
            del_words.append(lemma)
        else:                
            # Check word is in dictionary
            try:
                test_word = dictionary[lemma][wiki_pos]
            except KeyError:
                del_word_freqs.append(word_freqs[key][lemma])
                del_word_lemmas.append(lemma)
                del_words.append(lemma)
    
    # Delete non-existent words
    for del_word in del_words:
        del word_freqs[key][del_word]

    # Convert word list to dataframe, order by frequency, and save
    lemma_list = list(word_freqs[key].keys())
    freq_list = list(word_freqs[key].values())
    df = pd.DataFrame({'lemma': lemma_list, 'freq': freq_list})
    df = df.sort_values('freq', ascending=False)
    df_save_path = os.path.join('data', f'all_{key}.csv')
    df.to_csv(df_save_path, sep=',', index=False, encoding='utf-8')

# Save frequencies of deleted lemmas for testing
df = pd.DataFrame({'lemma': del_word_lemmas, 'freq': del_word_freqs})
df = df.sort_values('freq', ascending=False)
del_path = os.path.join('workflows', 'del_freqs.csv')
df.to_csv(del_path, sep=',', index=False, encoding='utf-8')
print('Complete')