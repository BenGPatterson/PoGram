from morfeusz2 import Morfeusz
from concraft_pl2 import Concraft, Server # Requires concraft_pl2.py (https://github.com/kawu/concraft-pl) in the same directory
import os
import pandas as pd
import time
from importlib.machinery import SourceFileLoader
dict_fns = SourceFileLoader('dict_fns', os.path.join('PoGram', 'dictionary.py')).load_module()

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
    concraft_path = os.path.join('workflows', 'concraft-pl.exe')
    server = Server(model_path=model_path, concraft_path=concraft_path, port=3001)
    concraft = Concraft(server_addr='http://127.0.0.1', port=3001)
    
    # Loop over each sentence
    print('Analysing sentences', end='')
    start = time.time()
    sentences_path = os.path.join('workflows', 'pol-com_web_2018_1M-sentences.txt')
    with open(sentences_path, encoding="utf-8") as file:
        dup_pos_dict = {}
        count = 0
        for i, line in enumerate(file):

            # Analyse sentence
            sentence = line.split('\t')[1]
            dag = morfeusz.analyse(sentence)
            res = concraft.disamb(dag)

            # Get required information from each interpretation
            current_word = 0
            interp_infos = {0: {}}
            for item in res:
                try:
                    if item[0] != current_word:
                        current_word = item[0]
                        interp_infos[current_word] = {}
                    full_pos = item[2][2]
                    word = item[2][0]
                    lemma = item[2][1].split(':')[0]
                    prob = float(item[3])
                    try:
                        interp_infos[current_word][f'{full_pos}_{word}'].append((lemma, prob))
                    except KeyError:
                        interp_infos[current_word][f'{full_pos}_{word}'] = [(lemma, prob)]
                except:
                    pass

            # Analyse interpretations for probabilities and duplicates
            for i in interp_infos.keys():
                for key in interp_infos[i].keys():

                    # Ignore if empty
                    if len(interp_infos[i][key]) == 0:
                        continue

                    # Check for duplicates
                    elif len(interp_infos[i][key]) > 1:
                        lemmas = [x[0] for x in interp_infos[i][key]]
                        if len(set(lemmas)) == 1:
                            interp_infos[i][key] = [interp_infos[i][key][0]]
                        else:
                            try:
                                dup_pos_dict[key] += interp_infos[i][key]
                            except KeyError:
                                dup_pos_dict[key] = interp_infos[i][key]
                            continue

                    # Otherwise add to frequency list
                    try:
                        full_pos, word = key.split('_')
                        wiki_pos = pos_conv[full_pos.split(':')[0]]
                        lemma, prob = interp_infos[i][key][0]
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
            if count == 10000:
                break

finally:
    server.terminate()
end = time.time()
print(f'\nAnalysis complete in {end-start} seconds')

# Analyse duplicates
print(f'Checking {len(dup_pos_dict)} duplicates')
for key in dup_pos_dict.keys():
    try:
        lemmas = set([x[0] for x in dup_pos_dict[key]])
        probs = [x[1] for x in dup_pos_dict[key]]
        prob = sum(probs)/len(set(lemmas))
        full_pos, word = key.split('_')
        wiki_pos = pos_conv[full_pos.split(':')[0]]
        priors = {}
        total_prior = 0
        for lemma in lemmas:
            try:
                priors[lemma] = word_freqs[wiki_pos][lemma]
            except KeyError:
                priors[lemma] = 0
            total_prior += priors[lemma]
        if total_prior == 0:
            total_prior = len(lemmas)
            for lemma in lemmas:
                priors[lemma] = 1
        for lemma in lemmas:
            try:
                word_freqs[wiki_pos][lemma] += prob*(priors[lemma]/total_prior)
            except KeyError:
                word_freqs[wiki_pos][lemma] = prob*(priors[lemma]/total_prior)
    except:
        pass

# Load wiki pages for post-processing sanity checks
print('Loading dictionary')
data_path = os.path.join('PoGram', 'data', 'wiki_entries.pgz')
dictionary = dict_fns.load_dictionary(data_path)

# Start pruning words
del_word_freqs = []
del_word_lemmas = []
print('Performing sanity checks and saving data')

# Redirect specified lemmas (e.g. to musieć from outdated spelling musić)
redirects = {('verb', 'musić'): ['verb', 'musieć']}
for r_key in redirects.keys():
    if r_key[0] in word_freqs.keys():
        if r_key[1] in word_freqs[r_key[0]].keys():
            item = redirects[r_key]
            word_freqs[item[0]][item[1]] += word_freqs[r_key[0]][r_key[1]]
            del_word_freqs.append(word_freqs[r_key[0]][r_key[1]])
            del_word_lemmas.append(r_key[1])
            del word_freqs[r_key[0]][r_key[1]]

# Loop through all keys and lemmas
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
            # Check words meet checks
            valid = True
            try:
                # Check word in dictionary
                test_word = dictionary[lemma][wiki_pos]

                # Check most basic form of lemma exists
                check_form = True
                if key == 'verb':
                    basic_form_pr = dict_fns.get_conjugation(dictionary, lemma, 'verb', '-', '1s', 'pr')
                    basic_form_f = dict_fns.get_conjugation(dictionary, lemma, 'verb', 'm', '1s', 'f')
                    basic_form = list(set(basic_form_pr+basic_form_f))
                elif key == 'adj':
                    basic_form = dict_fns.get_declension(dictionary, lemma, 'adj', 'sma', 'n')
                elif key == 'noun':
                    basic_form = dict_fns.get_declension(dictionary, lemma, 'noun', 's', 'n')
                else:
                    check_form = False
                if check_form:
                    if basic_form == [None]:
                        valid = False             

            # Mark invalid words to be deleted        
            except KeyError:
                valid = False
            if not valid:
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
    df_save_path = os.path.join('PoGram', 'data', f'all_{key}.csv')
    df.to_csv(df_save_path, sep=',', index=False, encoding='utf-8')

# Save frequencies of deleted lemmas for testing
df = pd.DataFrame({'lemma': del_word_lemmas, 'freq': del_word_freqs})
df = df.sort_values('freq', ascending=False)
del_path = os.path.join('workflows', 'del_freqs.csv')
df.to_csv(del_path, sep=',', index=False, encoding='utf-8')
print('Complete')