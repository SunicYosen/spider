'''
 Get User Name
'''
import time

def get_user_name(driver, url):
    name = ''
    print("[+]: Getting User Name ...")

    driver.get(url)
    time.sleep(2)

    try:
        name = driver.find_elements_by_class_name("name")[0].get_attribute('innerText')
    except:
        print("[+]: Cannot Get User Name!")

    print("[+]: Got User Name -- " + name)

    return name