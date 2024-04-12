import os
import pickle
import gzip
import gc
import sys
import time

def load_dictionary(path):
    """
    Loads dictionary of wiki pages.

    Parameters:
        path: Path to pickled dictionary object.

    Returns:
        Dictionary of wiki pages.
    """

    gc.disable()
    with gzip.open(data_path, "rb") as f:
        dictionary = pickle.load(f)
    gc.enable()

    return dictionary

def get_declension(dictionary, lemma, pos, numgen, case):
    """
    Gets specified declension of lemma from dictionary.

    Parameters:
        dictionary: Dictionary of word information.
        lemma: Lemma to decline.
        pos: Part of speech lemma belongs to.
        numgen: Letter code specifying singular/plural and gender (if relevant).
        case: Single letter defining grammatical case.

    Returns:
        List of possible declensions.
    """
    
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

    # Load dictionary
    data_path = os.path.join('data', 'wiki_entries.pgz')
    gc.disable()
    with gzip.open(data_path, "rb") as f:
        dictionary = pickle.load(f)
    gc.enable()

    # # Test case
    # cases = ['n', 'g', 'd', 'a', 'i', 'l', 'v']
    # numgens = ['sma', 'smi', 'sf', 'sn', 'pv', 'pnv']
    # for case in cases:
    #     row = []
    #     for ng in numgens:
    #         row.append(get_declension(dictionary, 'elektryczny', 'adj', ng, case))
    #     print(row)
    zmk = get_declension(dictionary, 'zamek', 'noun', 's', 'g')
    print(zmk)

    # print(dictionary['entries'][0].keys())
    # print(len(dictionary['entries'][0]['senses']), dictionary['entries'][0]['senses'])
    