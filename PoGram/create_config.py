import json

# Create config and trainer dict
config = {}
config['adj'] = {}

# Create trainer config
config['adj']['active'] = 0
config['adj']['qs'] = [1,1]
config['adj']['inflections_no'] = '3'
config['adj']['case_vars'] = [0, [1,1,0,1,1,1,0]]
config['adj']['word_list'] = 'freq'
config['adj']['freq_no'] = 100


with open('trainer_config.json', 'w') as outfile: 
    json.dump(config, outfile)