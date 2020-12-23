"""
Province Class
"""
import time

from city import City
from device_type import DeviceType
from device_scene import DeviceScene

class Province:
    def __init__(self):
        self.province_name     = ''
        self.province_cities   = []
        self.province_point    = 0
        self.province_screens  = 0
        self.total_type_points = 0
        self.total_scene_points= 0
        self.province_device_types_distribution = {}
        self.province_device_scenes_distribution = {}

    def add_city(self, city):
        self.province_cities.append(city.city_name)
        self.province_point     += city.city_point
        self.province_screens   += city.city_screens
        self.total_type_points  += city.total_type_points
        self.total_scene_points += city.total_scene_points

        for type_name in city.city_device_types_distribution:
            if type_name in self.province_device_types_distribution.keys():
                for key in city.city_device_types_distribution[type_name]:
                    if key in self.province_device_types_distribution[type_name].keys():
                        self.province_device_types_distribution[type_name][key] += city.city_device_types_distribution[type_name][key]
                    else:
                        self.province_device_types_distribution[type_name][key] = city.city_device_types_distribution[type_name][key]

            else:
                self.province_device_types_distribution[type_name] = {}
                for key in city.city_device_types_distribution[type_name]:
                    self.province_device_types_distribution[type_name][key] = city.city_device_types_distribution[type_name][key]

        for scene_name in city.city_device_scenes_distribution:
            if scene_name in self.province_device_scenes_distribution.keys():
                for key in city.city_device_scenes_distribution[scene_name]:
                    if key in self.province_device_scenes_distribution[scene_name].keys():
                        self.province_device_scenes_distribution[scene_name][key] += city.city_device_scenes_distribution[scene_name][key]
                    else:
                        self.province_device_scenes_distribution[scene_name][key] = city.city_device_scenes_distribution[scene_name][key]

            else:
                self.province_device_scenes_distribution[scene_name] = {}
                for key in city.city_device_scenes_distribution[scene_name]:
                    self.province_device_scenes_distribution[scene_name][key] = city.city_device_scenes_distribution[scene_name][key]
