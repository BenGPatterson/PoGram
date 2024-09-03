# -*- coding: utf-8 -*-

import os
import pickle
import gzip
import gc
import sys
from typing import Optional, Set

def getSize(obj, seen: Optional[Set[int]] = None) -> int:
  """Recursively finds size of objects. Needs: import sys """
  seen = set() if seen is None else seen

  if id(obj) in seen: return 0  # to handle self-referential objects
  seen.add(id(obj))

  size = sys.getsizeof(obj, 0) # pypy3 always returns default (necessary)
  if isinstance(obj, dict):
    size += sum(getSize(v, seen) + getSize(k, seen) for k, v in obj.items())
  elif hasattr(obj, '__dict__'):
    size += getSize(obj.__dict__, seen)
  elif hasattr(obj, '__slots__'): # in case slots are in use
    slotList = [getattr(C, "__slots__", []) for C in obj.__class__.__mro__]
    slotList = [[slot] if isinstance(slot, str) else slot for slot in slotList]
    size += sum(getSize(getattr(obj, a, None), seen) for slot in slotList for a in slot)
  elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
    size += sum(getSize(i, seen) for i in obj)
  return size

# Loads dictionary from pickled file
def load_dictionary(path):
    gc.disable()
    with gzip.open(path, "rb") as f:
        word_dict = pickle.load(f)
    gc.enable()

    size = getSize(word_dict)
    print(size)

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

    # zmk = get_declension(word_dict, 'zamek', 'noun', 'p', 'n')
    # print(zmk)
    