import os
import json
import pickle
import gzip

def process_wiki_pages(source, destination):
    """
    Converts .json of raw wiktionary pages into a format we can use 
    with a key for each word containing all senses of the word.

    Parameters:
        source: Path to raw wiktionary pages .json object.
        destination: Path to save compressed pickled object to.
    """

    # Load raw wiktionary pages
    print('Loading entries')
    raw_data = []
    with open(source, encoding="utf-8") as f:
        for line in f:
            raw_data.append(json.loads(line))

    # Stores each sense in corresponding key
    print(f'Processing {len(raw_data)} entries')
    data = {}
    keep_keys = ['pos', 'head_templates', 'forms', 'sounds', 'hyphenation', 'word', 'senses']
    for sense_raw in raw_data:

        # Used to store sense in processed dictionary
        word = sense_raw['word']
        pos = sense_raw['pos']

        # Keeps only certain information
        sense = {}
        for key in sense_raw.keys():
            if key in keep_keys:
                sense[key] = sense_raw[key]
            if key == 'senses':
                sense_list = []
                for item in sense[key]:
                    if 'glosses' in item.keys():
                        for gloss in item['glosses']:
                            sense_list.append(gloss)
                sense[key] = sense_list

        # Add sense to processed dictionary
        if pos == 'name':
            pos = 'noun'
        try:
            data[word][pos].append(sense)
        except KeyError:
            try:
                data[word][pos] = [sense]
            except KeyError:
                data[word] = {}
                data[word][pos] = [sense]
  
    # Saves processed entries as pickle object
    print('Saving processed entries')
    with gzip.GzipFile(destination, 'w') as f:
        pickle.dump(data, f)
    print('Complete')

if __name__ == '__main__':

    source_file = os.path.join('workflows', 'raw_wiki_entries.json')
    destination_file = os.path.join('PoGram', 'data', 'wiki_entries.pgz')
    process_wiki_pages(source_file, destination_file)