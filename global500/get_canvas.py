import os
import time
import random
import base64

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def get_canvas(url, output_path='output/0'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver  = webdriver.Chrome(options=options)
    driver.set_window_size(4096,2160)

    driver.get(url)
    time.sleep(1)

    def click(block):
        action = ActionChains(driver)
        action.click(block).perform()
        time.sleep(2)

    guide_btn = driver.find_element_by_class_name("guide")
    click(guide_btn)

    company_name = driver.find_elements_by_xpath('/html/body/main/div[1]/div[4]/div/h1')[0].text.split('\n')[0]
    # rank         = driver.find_element_by_xpath('//*[@id="carousel-slide"]/div/div/div/div/div[2]/p[2]/b').text
    
    slide_btn = driver.find_element_by_xpath('/html/body/main/div/div[6]/ol/li[3]')
    click(slide_btn)

    js_script = "return document.getElementsByTagName('canvas')[0].toDataURL('image/png');"
    im_info   = driver.execute_script(js_script)
    im_base64 = im_info.split(',')[1]
    im_bytes  = base64.b64decode(im_base64)

    chart3_name = driver.find_element_by_xpath("/html/body/main/div/div[6]/div/div[3]/div/p").text
    image3_path  = os.path.join(str(output_path), str(company_name)+'_'+chart3_name+'.png').replace('&','')
    with open(image3_path, 'wb') as f:
        f.write(im_bytes)

    slide_btn = driver.find_element_by_xpath('/html/body/main/div/div[6]/ol/li[4]')
    click(slide_btn)

    js_script = "return document.getElementsByTagName('canvas')[1].toDataURL('image/png');"
    im_info   = driver.execute_script(js_script)
    im_base64 = im_info.split(',')[1]
    im_bytes  = base64.b64decode(im_base64)

    chart4_name = driver.find_element_by_xpath("/html/body/main/div/div[6]/div/div[4]/div/p").text
    image4_path  = os.path.join(str(output_path), str(company_name)+'_'+chart4_name+'.png').replace('&','')
    with open(image4_path, 'wb') as f:
        f.write(im_bytes)

    slide_btn = driver.find_element_by_xpath('/html/body/main/div/div[6]/ol/li[5]')
    click(slide_btn)

    js_script = "return document.getElementsByTagName('canvas')[2].toDataURL('image/png');"
    im_info   = driver.execute_script(js_script)
    im_base64 = im_info.split(',')[1]
    im_bytes  = base64.b64decode(im_base64)

    chart5_name = driver.find_element_by_xpath("/html/body/main/div/div[6]/div/div[5]/div/p").text
    image5_path  = os.path.join(str(output_path), str(company_name)+'_'+chart5_name+'.png').replace('&','')
    with open(image5_path, 'wb') as f:
        f.write(im_bytes)

    driver.quit()

if __name__ == '__main__':
    url = 'https://www.caifuzhongwen.com/fortune500/gongsi/global500/2021/3.htm'
    get_canvas(url)
