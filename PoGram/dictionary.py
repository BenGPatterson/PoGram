import os
import json
import sys
import time

if __name__ == '__main__':

    data_path = os.path.join('data', 'test.json')
    with open(data_path, encoding="utf-8") as f:
        dictionary = json.load(f)

    print(dictionary['entries'][1]['word'])
    print(dictionary['entries'][0]['word'])
    