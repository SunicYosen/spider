"""""""""""""""
Main Function
"""""""""""""""
import os
from get_data import get_data
from write_data_json import write_data

def main():
    url             = 'http://agent.pingxiaobao.com/#/device/districtReport'
    write_file_temp = 'data_temp.json'
    write_file      = 'data.json'

    data            = get_data(url)
    try:
        write_data(write_file, data)
    except:
        print("[-] Write {} Failed!".format(write_file))
        exit()

    if(os.path.exists(write_file_temp)):
        # os.remove(write_file_temp)
        pass

    
if __name__ == '__main__':
    main()
