"""""""""""""""
Write Data
"""""""""""""""

import json

def write_data(file_name, data, write_type = 'w'):

    json_str = json.dumps(data, indent=4, ensure_ascii=False)

    with open(file_name, write_type, encoding='utf-8') as json_file:
        json_file.write(json_str)
        if(write_type == 'a'):
            json_file.write(',\n')
            
        json_file.close()
