"""""""""""""""
" Goto Pages
"""""""""""""""

import time

def goto_basic_page(driver, label, page_number):
    try:
        tables_item = driver.find_elements_by_class_name("el-tabs__item")

        for tabs_item in tables_item:
            if (tabs_item.get_attribute("innerText") == label):
                driver.execute_script("arguments[0].scrollIntoView();", tabs_item)
                tabs_item.click()
                time.sleep(1)
                break
    except:
        print("[-] Cannot find label!")
        exit()

    if(page_number != 1):
        try:
            pagination = driver.find_elements_by_class_name("paging")[1]
            driver.execute_script("arguments[0].scrollIntoView();", pagination)
            time.sleep(2)

            nag_blank = pagination.find_elements_by_tag_name("input")[0]
            nag_blank.clear()
            time.sleep(0.1)
            nag_blank.send_keys(page_number)
            time.sleep(0.1)
            pagination.find_elements_by_class_name("el-pagination__total")[0].click()
            time.sleep(0.3)

        except:
            print('[-] Cannot go to page {}'.format(page_number))
            exit()


def goto_device_types_page(driver, current_line, label):
    try:
        table_class = driver.find_elements_by_class_name("el-table__body")[1]
        city_line   = table_class.find_elements_by_xpath(".//tbody/tr[{}]".format(current_line))[0]
        driver.execute_script("arguments[0].scrollIntoView();", city_line)

        time.sleep(0.1)
        types_page_bt = city_line.find_element_by_xpath("./td[7]/div/div/a[1]")

        if(types_page_bt.get_attribute("innerText") == label):
            types_page_bt.click()

        time.sleep(0.5)
    except:
        print('[-] Cannot Go to City Type Page!')
        exit()


def goto_device_scenes_page(driver, current_line, label):
    try:
        table_class = driver.find_elements_by_class_name("el-table__body")[1]
        city_line   = table_class.find_elements_by_xpath(".//tbody/tr[{}]".format(current_line))[0]
        driver.execute_script("arguments[0].scrollIntoView();", city_line)

        time.sleep(0.1)
        types_page_bt = city_line.find_element_by_xpath("./td[7]/div/div/a[2]")

        if(types_page_bt.get_attribute("innerText") == label):
            types_page_bt.click()

        time.sleep(0.5)
        
    except:
        print('[-] Cannot Go to City Type Page!')
        exit()

if __name__ == '__main__':
    pass