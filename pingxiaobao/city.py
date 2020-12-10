"""
City Class
"""
import time

from device_type import DeviceType
from device_scene import DeviceScene

class City:
    def __init__(self):
        self.city_name = ''
        self.city_rank = ''
        self.city_province = ''
        self.city_location = ''
        self.city_point    = 0
        self.city_screens  = 0
        self.city_device_types_distribution = {}
        self.city_device_scenes_distribution = {}

    def get_basic_info(self, driver, current_line):
        try:
            table_class = driver.find_elements_by_class_name("el-table__body")[1]
            city_line   = table_class.find_elements_by_xpath(".//tbody/tr[{}]".format(current_line))[0]
            driver.execute_script("arguments[0].scrollIntoView();", city_line)
            time.sleep(0.1)
        except:
            print('[-] Cannot Get Table!')
            exit()

        try:
            self.city_rank     = city_line.find_element_by_xpath("./td[1]/div/div/div").get_attribute("textContent").strip()
            self.city_name     = city_line.find_element_by_xpath("./td[2]/div/div/div").get_attribute("textContent").strip()
            self.city_province = city_line.find_element_by_xpath("./td[3]/div/div/div").get_attribute("textContent").strip()
            self.city_location = city_line.find_element_by_xpath("./td[4]/div/div/div").get_attribute("textContent").strip()
            self.city_point    = int(city_line.find_element_by_xpath("./td[5]/div/div/div").get_attribute("textContent").strip())
            self.city_screens  = int(city_line.find_elements_by_xpath(".//td[6]/div/div/div")[0].get_attribute("textContent").strip())
        except:
            print('[-] Cannot Get City Info!')
            exit()

        if(self.city_name == '北京市'):
            self.city_rank = '一线城市'

        if(self.city_name == '上海市'):
            self.city_rank = '一线城市'

        if(self.city_name == '天津市'):
            self.city_rank = '新一线城市'

        if(self.city_rank == '—'):
            self.city_rank = '其它'

    def get_device_types_distribution(self, driver):
        device_type_t = DeviceType()
        while True:
            try:
                table_class = driver.find_elements_by_class_name("el-table__body")[0]
                table_rows  = table_class.find_elements_by_xpath("./tbody/tr")
                # print(len(table_rows))
                for table_row in table_rows:
                    device_type_t.type_name         = table_row.find_element_by_xpath("./td[2]/div/div/div").get_attribute("textContent").strip()
                    device_type_t.type_point_number = int(table_row.find_element_by_xpath("./td[3]/div/div/div").get_attribute("textContent").strip())
                    device_type_t.type_screens      = int(table_row.find_element_by_xpath("./td[4]/div/div/div").get_attribute("textContent").strip())

                    self.city_device_types_distribution.update({device_type_t.type_name: \
                                                                {'点位数量':device_type_t.type_point_number, \
                                                                 '屏幕数量':device_type_t.type_screens}})

                next_button = driver.find_elements_by_class_name("btn-next")[0]
                driver.execute_script("arguments[0].scrollIntoView();", next_button)

                # print(self.city_device_types_distribution)
                if(next_button.is_enabled()):
                    next_button.click()
                    time.sleep(1)
                else:
                    break

            except:
                print("[-] Get Device Type Info Failed!")
                exit()

    def get_device_scenes_distribution(self, driver):
        device_scene_t = DeviceScene()
        while True:
            try:
                table_class = driver.find_elements_by_class_name("el-table__body")[0]
                table_rows  = table_class.find_elements_by_xpath("./tbody/tr")
                # print(len(table_rows))
                for table_row in table_rows:
                    device_scene_t.scene_name         = table_row.find_element_by_xpath("./td[2]/div/div/div").get_attribute("textContent").strip()
                    device_scene_t.scene_point_number = int(table_row.find_element_by_xpath("./td[3]/div/div/div").get_attribute("textContent").strip())
                    device_scene_t.scene_screens      = int(table_row.find_element_by_xpath("./td[4]/div/div/div").get_attribute("textContent").strip())

                    self.city_device_scenes_distribution.update({device_scene_t.scene_name: \
                                                                {'点位数量':device_scene_t.scene_point_number, \
                                                                 '屏幕数量':device_scene_t.scene_screens}})

                next_button = driver.find_elements_by_class_name("btn-next")[0]
                driver.execute_script("arguments[0].scrollIntoView();", next_button)

                # print(self.city_device_scenes_distribution)
                if(next_button.is_enabled()):
                    next_button.click()
                    time.sleep(1)
                else:
                    break

            except:
                print("[-] Get Device Scenes Info Failed!")
                exit()
