"""""""""""""""
Data Function
"""""""""""""""

import os
import time
from selenium import webdriver

from city import City
from get_usr_data_dir import get_usr_data_dir
from goto_pages import goto_basic_page, goto_device_scenes_page, goto_device_types_page
from write_data_json import write_data

def get_data(url, write_file='data_temp.json', write_type='a'):
    
    data_label         = '城市等级划分'
    data_city_nums     = 404
    data_city_per_page = 50
    data_sub_label1    = '设备类型分布'
    data_sub_label2    = '场景分布'

    cities_data        = []

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    user_data_path = get_usr_data_dir()
    options.add_argument(user_data_path)
    driver         = webdriver.Chrome(options=options)

    for index in range(150,405):
        page_index     = int(index / data_city_per_page) + 1
        index_in_pages = (index % data_city_per_page) + 1

        city = City()

        driver.get(url)
        time.sleep(1)

        goto_basic_page(driver, label=data_label, page_number=page_index)
        time.sleep(1)

        city.get_basic_info(driver, current_line=index_in_pages)
        time.sleep(1)

        print('{}/{}'.format(index+1, data_city_nums), page_index, city.city_rank, city.city_name, city.city_point, city.city_screens)
        goto_device_types_page(driver, current_line=index_in_pages, label=data_sub_label1)
        time.sleep(1)

        city.get_device_types_distribution(driver)
        time.sleep(1)

        driver.get(url)
        goto_basic_page(driver, label=data_label, page_number=page_index)
        time.sleep(1)

        goto_device_scenes_page(driver, current_line=index_in_pages, label=data_sub_label2)

        city.get_device_scenes_distribution(driver)
        time.sleep(1)

        city_dict = {'城市':city.city_name,  \
                     '城市分类':city.city_rank, \
                     '省份':city.city_province, \
                     '所属地区':city.city_location, \
                     '点位数量':city.city_point, \
                     '屏幕数量':city.city_screens, \
                     '类型分布':city.city_device_types_distribution, \
                     '场景分布':city.city_device_scenes_distribution}

        cities_data.append(city_dict)
        write_data(write_file, city_dict, write_type)

    return cities_data