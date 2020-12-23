"""""""""""""""
Write Data
"""""""""""""""

import json
from city import City

def load_json(file_name='data.json'):
    with open(file_name, 'r') as json_fp:
        json_data = json_fp.read()
        data_arr  = json.loads(json_data)
        return data_arr

if __name__ == '__main__':
    json_file = 'data.json'
    load_json(json_file)