# -*- coding: utf-8 -*-

import os
import pickle
import gzip
import gc

# Loads dictionary from pickled file
def load_dictionary(path):
    gc.disable()
    with gzip.open(path, "rb") as f:
        word_dict = pickle.load(f)
    gc.enable()

    return word_dict

# Gets declined form of word from dictionary
def get_declension(dictionary, lemma, pos, numgen, case):
    
    # Produce tags
    tags = set()
    if pos == 'adj' and case == 'v':
        case = 'n'
    case_dict = {'n': 'nominative', 'g': 'genitive', 'd': 'dative', 'a': 'accusative', 
                 'i': 'instrumental', 'l': 'locative', 'v': 'vocative'}
    tags.add(case_dict[case.lower()])
    number_dict = {'s': ['singular'], 'p': ['plural'], 'sma': ['singular', 'masculine', 'animate'], 'smi': ['singular', 'masculine', 'inanimate'], 
                   'sf': ['singular', 'feminine'], 'sn': ['singular', 'neuter'], 'pv': ['plural', 'virile'], 'pnv': ['plural', 'error-unrecognized-form']}
    tags.update(number_dict[numgen.lower()])
    if case != 'a':
        tags -= {'animate', 'inanimate'}

    # Find corresponding declension(s)
    declensions = set()
    for sense in dictionary[lemma.lower()][pos]:
        declension = next((item['form'] for item in sense['forms'] if set(item['tags']) == tags), None)
        declensions.add(declension)
    if None in declensions and len(declensions) > 1:
        declensions.remove(None)
    
    return list(declensions)

if __name__ == '__main__':

    # Test case
    data_path = os.path.join('data', 'wiki_entries.pgz')
    word_dict = load_dictionary(data_path)

    zmk = get_declension(word_dict, 'zamek', 'noun', 'p', 'n')
    print(zmk)
    