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

# Get conjugation of word from dictionary
def get_conjugation(dictionary, lemma, pos, gen, voice, tense):

    # Produce tags
    base_tags = set()

    # Tense tags
    tense_dict = {'pr': 'present', 'pa': 'past', 'f': 'future', 'c': 'conditional', 'i': 'imperative', 'v': 'noun-from-verb'}
    part_dict = {'par-act': ['active', 'adjectival', 'participle'], 'par-pas': ['passive', 'adjectival', 'participle'],
                 'par-cont': ['contemporary', 'adjectival', 'participle'], 'par-ant': ['anterior', 'adverbial', 'participle']}
    if 'par' in tense:
        base_tags.update(part_dict[tense])
    else:
        base_tags.add(tense_dict[tense])
    
    # Voice tags
    if tense in ['pr', 'pa', 'f', 'c', 'i']:
        voice_dict = {'1s': ['first-person', 'singular'], '2s': ['second-person', 'singular'], '3s': ['third-person', 'singular'], 
                      '1p': ['first-person', 'plural'], '2p': ['second-person', 'plural'], '3p': ['third-person', 'plural'],
                      'i': ['impersonal']}
        base_tags.update(voice_dict[voice])

    # Repeat for each aspect
    conjugations = set()
    aspects = [asp for asp in get_derived_word(dictionary, lemma, pos, 'asp') if len(asp) == 1]
    for aspect in aspects:
        tags = set(base_tags)

        # Gender tags
        if tense in ['pa', 'f', 'c', 'par-act', 'par-pas'] and voice != 'i':
            if tense == 'f' and (aspect == 'p' or lemma == 'być'):
                pass
            else:
                if tense in ['par-act', 'par-pas']:
                    gen_dict = {'m': ['singular', 'masculine'], 'f': ['singular', 'feminine'], 'n': ['singular', 'neuter'], 
                                'v': ['plural', 'virile'], 'nv': ['plural', 'nonvirile']}
                else:
                    gen_dict = {'m': ['masculine'], 'f': ['feminine'], 'n': ['neuter'], 'v': ['virile'], 'nv': ['nonvirile']}
                tags.update(gen_dict[gen])

        # Find corresponding conjugation(s)
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
    elif len(conjugations) == 0:
        conjugations.add(None)
    
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
                   'biasp': ['i', 'imperfective', 'p', 'perfective'],
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
                if 'obsolete' not in aspect:
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

def hardcode_num_declensions(dictionary, word):

    forms = []

    if word == 'dwa':
        form_codes = {'dwaj': ['pv_n'], 'dwóch': ['pv_n', 'g', 'pv_a', 'l'], 'dwa': ['pm_n', 'pn_g', 'pm_a', 'pn_a'],
                      'dwie': ['pf_n', 'pf_a'], 'dwóm': ['d'], 'dwoma': ['i'], 'dwiema': ['pf_i']}
        numgen_codes = {'pv': ['plural', 'virile'], 'pm': ['plural', 'masculine'], 'pn': ['plural', 'neutral'], 'pf': ['plural', 'feminine']}
        case_codes = {'n': ['nominative'], 'g': ['genitive'], 'd': ['dative'], 'a': ['accusative'], 'i': ['instrumental'], 'l': ['locative']}
        for form in form_codes.keys():
            for form_code in form_codes[form]:
                if len(form_code) == 1:
                    for code in numgen_codes.keys():
                        forms.append({'form': form, 'tags': numgen_codes[code] + case_codes[form_code]})
                else:
                    forms.append({'form': form, 'tags': numgen_codes[form_code[:-2]] + case_codes[form_code[-1]]})
                
    elif word in ['trzy', 'cztery']:
        if word == 'trzy':
            form_codes = {'trzej': ['pv_n'], 'trzech': ['pv_n', 'pnv_g', 'pv_a', 'pnv_l'], 'trzy': ['pnv_n', 'pnv_a'],
                          'trzem': ['pnv_d'], 'trzema': ['pnv_i']}
        elif word == 'cztery':
            form_codes = {'czterej': ['pv_n'], 'czterech': ['pv_n', 'pnv_g', 'pv_a', 'pnv_l'], 'cztery': ['pnv_n', 'pnv_a'],
                          'czterem': ['pnv_d'], 'czterema': ['pnv_i']}
        numgen_codes = {'pv': ['plural', 'virile'], 'pnv': ['plural']}
        case_codes = {'n': ['nominative'], 'g': ['genitive'], 'd': ['dative'], 'a': ['accusative'], 'i': ['instrumental'], 'l': ['locative']}
        for form in form_codes.keys():
            for form_code in form_codes[form]:
                forms.append({'form': form, 'tags': numgen_codes[form_code[:-2]] + case_codes[form_code[-1]]})

    elif word == 'sześć':
        forms = dictionary[word]['noun'][0]['forms']

    dictionary[word]['num'].append({'forms': forms})
    
    return dictionary


# Get declension of components of compound cardinal numeral
def get_card_comp_declension(dictionary, base_comps, loose_infl, numgen, case):

    # Hardcode missing declensions
    for base_comp in set(base_comps):
        if base_comp in ['dwa', 'trzy', 'cztery', 'sześć']:
            dictionary = hardcode_num_declensions(dictionary, base_comp)

    # Dictionaries for case/voices
    case_dict = {'n': 'nominative', 'g': 'genitive', 'd': 'dative', 'a': 'accusative', 
                 'i': 'instrumental', 'l': 'locative', 'v': 'vocative'}
    numgen_dict = {'sma': ['singular', 'masculine', 'animate'], 'smi': ['singular', 'masculine', 'inanimate'], 'sf': ['singular', 'feminine'],
                   'sn': ['singular', 'neuter'], 'pv': ['plural', 'virile'], 'pnv': ['plural', 'error-unrecognized-form'],
                   'pm': ['plural', 'masculine'], 'pf': ['plural', 'feminine'], 'pn': ['plural', 'neutral']}
    
    # Get declension for each component
    comp_declensions = []
    for base_comp in base_comps:

        if base_comp == 'jeden' and loose_infl[-1] == 1:
            comp_declensions.append([base_comp])
            continue
    
        tags = set()
        tags.add(case_dict[case])
        tags.update(numgen_dict[numgen])
        if numgen == 'pnv' and base_comp != 'jeden':
            tags.remove('error-unrecognized-form')

        # Find corresponding declension(s)
        declensions = set()
        for sense in dictionary[base_comp]['num']:
            try:
                declension = set(item['form'] for item in sense['forms'] if set(item['tags']) == tags)
                declensions.update(declension)
            except KeyError:
                pass
        if 'virile' in tags and len(declensions) == 0:
            tags.remove('virile')
            try:
                declension = set(item['form'] for item in sense['forms'] if set(item['tags']) == tags)
                declensions.update(declension)
            except KeyError:
                pass
        if 'stoma' in declensions:
            declensions.remove('stoma')
        if None in declensions and len(declensions) > 1:
            declensions.remove(None)
        if len(declensions) == 0:
            declensions = [None]
        comp_declensions.append(list(declensions))

    print(comp_declensions)

    # Get total declension for compound numeral
    total_declensions = []
    strict_inflections = ['']
    loose_inflection = ['']
    for i in range(len(base_comps)):
        new_stricts = []
        for j in range(len(comp_declensions[i])):
            for strict in strict_inflections:
                new_stricts.append(strict + comp_declensions[i][j] + ' ')
        strict_inflections = new_stricts
        if loose_infl[i]:
            new_looses = []
            for j in range(len(comp_declensions[i])):
                for loose in loose_inflection:
                    new_looses.append(loose + comp_declensions[i][j] + ' ')
            loose_inflection = new_looses
        else:
            for j in range(len(loose_inflection)):
                loose_inflection[j] += base_comps[i] + ' '
    total_declensions = strict_inflections + loose_inflection
    for i in range(len(total_declensions)):
        total_declensions[i] = total_declensions[i][:-1]  # Remove trailing space

    return list(set(total_declensions))

if __name__ == '__main__':

    # Test case
    data_path = os.path.join('PoGram', 'data', 'wiki_entries.pgz')
    word_dict = load_dictionary(data_path)

    conv_dict = {1: 'jeden', 2: 'dwa', 3: 'trzy', 4: 'cztery', 5: 'pięć', 6: 'sześć', 7: 'siedem', 8: 'osiem', 9: 'dziewięć', 10: 'dziesięć',
                     11: 'jedenaście', 12: 'dwanaście', 13: 'trzynaście', 14: 'czternaście', 15: 'piętnaście', 16: 'szesnaście', 
                     17: 'siedemnaście', 18: 'osiemnaście', 19: 'dziewiętnaście', 20: 'dwadzieścia', 30: 'trzydzieści', 40: 'czterdzieści',
                     50: 'pięćdziesiąt', 60: 'sześćdziesiąt', 70: 'siedemdziesiąt', 80: 'osiemdziesiąt', 90: 'dziewięćdziesiąt', 100: 'sto',
                     200: 'dwieście', 300: 'trzysta', 400: 'czterysta', 500: 'pięćset', 600: 'sześćset', 700: 'siedemset', 800: 'osiemset', 
                     900: 'dziewięćset'}
    
    # for num in conv_dict.values():
    #     try:
    #         print(num, word_dict[num].keys())
    #     except:
    #         print(f'{num} not found in dictionary')
    # word_dict = hardcode_num_declensions(word_dict, 'dwa')
    # print(word_dict['czterysta']['num'][0]['forms'])

    # for sense in word_dict['jedenastka']['noun']:
    #     print(sense)

    base_comps = ['trzydzieści', 'dwa']

    for numgen in ['pv', 'pm', 'pf', 'pn']:
        for case in ['n', 'g', 'd', 'a', 'i', 'l']:
            print(f'numgen: {numgen}, case: {case}')
            print(get_card_comp_declension(word_dict, base_comps, [True, True], numgen, case))