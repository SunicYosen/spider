"""
Set Province for Cities Array
"""

from province import Province
from city import City

def set_data_from_arr(data_arr):
    provinces_dict = {}
    cities_arr     = []
    for city_dict in data_arr:
        city = City()
        city.set_city_from_dict(city_dict)
        city.get_total_scene_points()
        city.get_total_type_points()
        print(city.city_name)

        cities_arr.append(city)

        if city.city_province not in provinces_dict.keys():
            province = Province()
            province.province_name = city.city_province
        else:
            province = provinces_dict[city.city_province]

        province.add_city(city)

        if(city.city_name ==  '路凼填海区'):
            print('1', city.city_device_types_distribution)

        provinces_dict.update({province.province_name:province})
        if(city.city_name ==  '路凼填海区'):
            print('2', city.city_device_types_distribution)

    for city in cities_arr:
        if(city.city_name ==  '路凼填海区'):
            print('3', city.city_device_types_distribution)

    return cities_arr, provinces_dict

