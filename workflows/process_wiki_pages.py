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
    for sense in raw_data:
        word = sense['word']
        pos = sense['pos']
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

    source_file = os.path.join('data', 'raw_wiki_entries.json')
    destination_file = os.path.join('data', 'wiki_entries.pgz')
    process_wiki_pages(source_file, destination_file)