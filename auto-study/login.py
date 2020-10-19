import time
import re
import base64

from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from get_usr_data_dir import get_usr_data_dir

def get_qrcode_pic(driver, qrcode_src):
    driver.get(qrcode_src)
    qrcode_img = driver.find_elements_by_tag_name('img')
    im_info   = qrcode_img[0].get_attribute('src')
    im_base64 = im_info.split(',')[1]
    im_bytes  = base64.b64decode(im_base64)
    img = Image.open(BytesIO(im_bytes))
    return img

    # plt.figure("学习强国扫码登录")
    # plt.imshow(img)
    # plt.show()
    #

def get_qrcode_src(driver):
    login_qrcode = driver.find_elements_by_id('ddlogin-iframe')
    qrcode_src    = login_qrcode[0].get_attribute('src')
    return qrcode_src

def login_study(driver, url="https://pc.xuexi.cn/points/login.html"):
    driver.get(url)
    driver.execute_script("var q=document.documentElement.scrollTop=950")
    driver.execute_script("var q=document.documentElement.scrollLeft=225")
    time.sleep(1)

    qrcode_src = get_qrcode_src(driver)
    time.sleep(1)
    qrcode_pic = get_qrcode_pic(driver, qrcode_src)
    time.sleep(1)
    qrcode_pic.show()

    driver.get(url)

    try:
        WebDriverWait(driver,60).until(EC.title_is(u"我的学习"))
        print("[+]: 登录成功!")
        return 0

    except:
        print("[-]: 登录失败，正在重试...")
        return 1


def check_login(driver, url="https://pc.xuexi.cn/points/login.html"):
    driver.get(url)
    driver.execute_script("var q=document.documentElement.scrollTop=950")
    driver.execute_script("var q=document.documentElement.scrollLeft=225")
    time.sleep(2)
    try:
        WebDriverWait(driver,5).until(EC.title_is(u"我的学习"))
        print("[+]: 登录成功!")
        return 0

    except:
        return 1

def main():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    user_data_path = get_usr_data_dir()
    # chrome_options.add_argument(user_data_path)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.xuexi.cn/")
    driver.implicitly_wait(5)

    login_url = "https://pc.xuexi.cn/points/login.html"

    while check_login(driver, login_url):
        login_study(driver, url=login_url)
    
    driver.quit()

if __name__ == '__main__':
    main()