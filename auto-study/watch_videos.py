'''
 Watch Videos
'''
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from get_usr_data_dir import get_usr_data_dir

def watch_videos(driver, url=''):
    titles=['新闻联播','学习新视界','学习专题报道','重要活动视频专辑']
#"""观看视频"""#视频好像会需要每天都看新的，前一天看的算旧的，今天再看不算任务
    driver.get(url)
    driver.implicitly_wait(10)

    for indexs, title in enumerate(titles):
        print("[+]: Watching: ", title)
        driver.find_elements_by_xpath("//*[contains(text(), '"+title+"')]")[0].click()
#这个是直接打开页面，是图文
        time.sleep(2)
        videos = driver.find_elements_by_xpath("//div[@class='textWrapper']")
        time.sleep(2)
#上面是图文选取，如果你想点到列表里面选取，则改为以下代码：
    #titles=driver.find_elements_by_xpath("//*[contains(text(), '列表')]")[0]
    #titles.click()
    #videos = driver.find_elements_by_xpath("//div[@class='text-link-item-title']")
        for i, video in enumerate(videos):
            if i > 1:
                break
            video.click()
            all_handles = driver.window_handles
            driver.switch_to.window(all_handles[-1])
            #模拟点击播放，因为直接点开连接播放，积分不会增长，可能也是因为反爬机制，必须刷新页面后，点击播放才算做是观看一次
            driver.get(driver.current_url)
            print("[+]: --", i+1, '/', 2, '\t', driver.current_url)
            driver.find_element_by_xpath("//div[@class='outter']").click()
            time.sleep(3)
            # driver.save_screenshot('vidoes'+str(indexs)+'_'+str(i)+'.png')

#可以获取视频当前时长，但是没有必要，只要看3分钟就好了
            #video_current_time_str = driver.find_element_by_xpath("//span[@class='current-time']").get_attribute('innerText')
            #print(video_current_time_str)
            #video_duration = int(video_duration_str.split(':')[0]) * 60 + int(video_duration_str.split(':')[1])

#每个视频开启后停留190秒，然后把所有句柄关闭
            time.sleep(180)
            driver.close()
            driver.switch_to.window(all_handles[0])

# 保持学习，直到视频结束
        #time.sleep(video_duration + 3)
    print("[+]: 播放视频完毕\n")
