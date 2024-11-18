# -*- coding: utf-8 -*-

import os
import pickle
import gzip
import gc
from ast import literal_eval

# Loads dictionary from pickled file
def load_dictionary(path):
    gc.disable()
    with gzip.open(path, "rb") as f:
        word_dict = pickle.load(f)
    gc.enable()

    return word_dict

# Get conjugation of word from dictionary
def get_conjugation(dictionary, lemma, pos, gen, voice, tense):

    # Produce tags
    tags = set()

    # Tense tags
    tense_dict = {'pr': 'present', 'pa': 'past', 'f': 'future', 'c': 'conditional', 'i': 'imperative', 'v': 'noun-from-verb'}
    part_dict = {'par-act': ['active', 'adjectival', 'participle'], 'par-pas': ['passive', 'adjectival', 'participle'],
                 'par-cont': ['contemporary', 'adjectival', 'participle'], 'par-ant': ['anterior', 'adverbial', 'participle']}
    if 'par' in tense:
        tags.update(part_dict[tense])
    else:
        tags.add(tense_dict[tense])

    # Gender tags
    if tense in ['pa', 'f', 'c', 'par-act', 'par-pas'] and voice != 'i':
        if tense == 'f' and ('p' in get_derived_word(dictionary, lemma, pos, 'asp') or lemma == 'być'):
            pass
        else:
            if tense in ['par-act', 'par-pas']:
                gen_dict = {'m': ['singular', 'masculine'], 'f': ['singular', 'feminine'], 'n': ['singular', 'neuter'], 
                            'v': ['plural', 'virile'], 'nv': ['plural', 'nonvirile']}
            else:
                gen_dict = {'m': ['masculine'], 'f': ['feminine'], 'n': ['neuter'], 'v': ['virile'], 'nv': ['nonvirile']}
            tags.update(gen_dict[gen])
    
    # Voice tags
    if tense in ['pr', 'pa', 'f', 'c', 'i']:
        voice_dict = {'1s': ['first-person', 'singular'], '2s': ['second-person', 'singular'], '3s': ['third-person', 'singular'], 
                      '1p': ['first-person', 'plural'], '2p': ['second-person', 'plural'], '3p': ['third-person', 'plural'],
                      'i': ['impersonal']}
        tags.update(voice_dict[voice])

    # Find corresponding conjugation(s)
    conjugations = set()
    for sense in dictionary[lemma][pos]:
        try:
            conjugation = set(item['form'] for item in sense['forms'] if set(item['tags']) == tags)
            conjugations.update(conjugation)
        except:
            pass
    if len(conjugations) == 0:
        conjugations.add(None)

    # Retry with 1st/2nd person tag removed
    if '1' in str(voice) and None in conjugations:
        tags.remove('first-person')
        for sense in dictionary[lemma][pos]:
            try:
                conjugation = list(item['form'] for item in sense['forms'] if set(item['tags']) == tags)
                conjugation = set(conjugation[:int(len(conjugation)/2)])
                conjugations.update(conjugation)
            except:
                pass
    elif '2' in str(voice) and None in conjugations:
        tags.remove('second-person')
        for sense in dictionary[lemma][pos]:
            try:
                conjugation = list(item['form'] for item in sense['forms'] if set(item['tags']) == tags)
                conjugation = set(conjugation[int(len(conjugation)/2):])
                conjugations.update(conjugation)
            except:
                pass
    if None in conjugations and len(conjugations) > 1:
                conjugations.remove(None)
    

    return list(conjugations)
                    
# Gets declined form of word from dictionary
def get_declension(dictionary, lemma, pos, numgen, case):

    # If numgen or case not specified set to singular/nominative
    if numgen == '-':
        numgen = 's'
    if case == '-':
        case  = 'n'
    
    # Produce tags
    tags = set()

    # Case tags
    if pos == 'adj' and case == 'v':
        case = 'n'
    case_dict = {'n': 'nominative', 'g': 'genitive', 'd': 'dative', 'a': 'accusative', 
                 'i': 'instrumental', 'l': 'locative', 'v': 'vocative'}
    tags.add(case_dict[case.lower()])

    # Gender tags
    number_dict = {'s': ['singular'], 'p': ['plural'], 'sma': ['singular', 'masculine', 'animate'], 'smi': ['singular', 'masculine', 'inanimate'], 
                   'sf': ['singular', 'feminine'], 'sn': ['singular', 'neuter'], 'pv': ['plural', 'virile'], 'pnv': ['plural', 'error-unrecognized-form']}
    tags.update(number_dict[numgen.lower()])

    # Remove tags for specific cases
    if case != 'a':
        tags -= {'animate', 'inanimate'}
    if case not in ['n', 'a', 'v']:
        tags -= {'virile', 'nonvirile', 'error-unrecognized-form'}

    # Exclude certain tags for other quantifiers
    excl_tags = set()
    if pos == 'oqua':
        if case in ['n', 'a'] and numgen == 'pnv':
            tags -= {'error-unrecognized-form'}
            excl_tags.add('virile')
        if lemma in ['kilka', 'kilkanaście', 'kilkadziesiąt', 'paręnaście', 'parędziesiąt']:
            pos = 'det'
        elif lemma in ['wiele', 'tyle']:
            pos = 'num'
        elif lemma in ['ile', 'kilkaset', 'paręset']:
            pos='pron'

    # Certain irregular words
    if pos == 'pron' and lemma in ['ten'] and 'error-unrecognized-form' in tags:
        tags -= {'error-unrecognized-form'}
        tags.add('nonvirile')
    if pos == 'pron' and lemma in ['one'] and 'plural' in tags:
        tags -= {'plural'}
        tags.add('error-unrecognized-form')

    # Backup parts of speech for adjectives
    backups = [pos]
    if pos == 'adj':
        backups += ['particle', 'num', 'verb']

    # Find corresponding declension(s)
    declensions = set()
    for pos_ in backups:
        try:
            for sense in dictionary[lemma][pos_]:
                if pos == 'adj' and pos_ == 'verb' and sense['head_templates'][0]['name'] != 'pl-participle':
                    continue
                declension = set(item['form'] for item in sense['forms'] if tags.issubset(set(item['tags'])) and excl_tags.isdisjoint(set(item['tags'])))
                declensions.update(declension)
            if None in declensions and len(declensions) > 1:
                declensions.remove(None)
            if None not in declensions and len(declensions) > 0:
                break
        except:
            pass
    declensions -= {'-'}
    if len(declensions) == 0:
        declensions = [None]
    
    return list(declensions)

# Gets conjugated form of defective verb from dictionary
def get_def_conjugation(dictionary, lemma, gen, voice, tense):

    # Produce tags
    tags = set()

    # Ajusts tense for winien
    if lemma == 'winien':
        if tense == 'pr':
            tense = 'pa'
        elif tense == 'pa':
            tense = 'plu'

    # Tense tags
    tense_dict = {'pr': 'present', 'pa': 'past', 'plu': 'error-unrecognized-form'}
    tags.add(tense_dict[tense])

    # Gender tags
    if voice != 'i':
        gen_dict = {'m': ['masculine'], 'f': ['feminine'], 'n': ['neuter'], 'v': ['virile'], 'nv': ['nonvirile']}
        tags.update(gen_dict[gen])
    
    # Voice tags
    voice_dict = {'1': ['first-person'], '2': ['second-person'], '3': ['third-person'], 'i': ['impersonal']}
    tags.update(voice_dict[voice])

    # Find corresponding conjugation(s)
    conjugations = set()
    for sense in dictionary[lemma]['verb']:
        try:
            conjugation = set(item['form'] for item in sense['forms'] if set(item['tags']) == tags)
            conjugations.update(conjugation)
        except:
            pass
    if len(conjugations) == 0:
        conjugations.add(None)

    # Clean output
    if None in conjugations and len(conjugations) > 1:
                conjugations.remove(None)
    
    return list(conjugations)

# Gets derived words from dictionary
def get_derived_word(dictionary, lemma, pos, form):

    derived = set()

    # Get aspect of word
    if form == 'asp':
        aspects = {'impf-indet': ['i', 'imperfective'],
                   'impf-det': ['i', 'imperfective'],
                   'impf-freq': ['i', 'imperfective'],
                   'impf': ['i', 'imperfective'],
                   'pf': ['p', 'perfective'],
                   'pl': []}
        for sense in dictionary[lemma][pos]:
            aspect = sense['head_templates'][0]['args']['1']
            derived.update(aspects[aspect])

    # Find aspect pairs
    elif form in ['asp_ii', 'asp_id', 'asp_if', 'asp_i', 'asp_p']:
        aspects = {'asp_ii': 'indet',
                   'asp_id': 'det',
                   'asp_if': 'freq',
                   'asp_i': 'impf',
                   'asp_p': 'pf'}
        for sense in dictionary[lemma][pos]:
            target = aspects[form]
            all_aspects = list(sense['head_templates'][0]['args'].keys())
            if target == 'indet':
                if 'indet' not in all_aspects and 'impf' in all_aspects and 'det' in all_aspects:
                    target = 'impf'
            elif target == 'det':
                if 'det' not in all_aspects and 'impf' in all_aspects and 'indet' in all_aspects:
                    target = 'impf'
            elif target == 'impf':
                if 'indet' in all_aspects or 'det' in all_aspects or 'freq' in all_aspects:
                    target = None
            try:
                aspect = sense['head_templates'][0]['args'][target]
                derived.add(aspect)
            except:
                pass
        if len(derived) == 0:
            derived.add(None)

    # Handle adverbs differently
    elif form == 'adv':
        for sense in dictionary[lemma][pos]:
            try:
                if sense['head_templates'][0]['args']['adv'] == '-':
                    derived.add(None)
                else:
                    derived.add(sense['head_templates'][0]['args']['adv'])
            except:
                derived.add(None)
        if None in derived and len(derived) > 1:
            derived.remove(None)
    
    # Other derived words
    else:
        # Decide tags
        derived_tags = {'comp': set(['comparative']), 'super': set(['superlative']), 'dim': set(['diminutive'])}
        tags = derived_tags[form]

        # Find comparative or superlative
        for sense in dictionary[lemma][pos]:
            derive = next((item['form'] for item in sense['forms'] if set(item['tags']) == tags), None)
            derived.add(derive)
        while None in derived and len(derived) > 1:
            derived.remove(None)

    return list(derived)

# Gets definitions of word from dictionary
def get_definition(dictionary, lemma, pos):

    # Get definitions
    definitions = []
    for sense in dictionary[lemma][pos]:
        definitions += sense['senses']
    if len(definitions) == 0:
        definitions = [None]

    return definitions

# Get declension of components of compound cardinal numeral
def get_num_comp_declension(dictionary, base_comps, c_infl, gen_overrides, numgen, case):
    return(['test'])

if __name__ == '__main__':

    # Test case
    data_path = os.path.join('PoGram', 'data', 'wiki_entries.pgz')
    word_dict = load_dictionary(data_path)
    
    for sense in word_dict['potrafić']['verb']:
        print(sense)
    # print(get_def_conjugation(word_dict, 'winien', 'm', 'i', 'pa'))