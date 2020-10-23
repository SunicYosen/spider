'''
 Watch Videos
'''
import os
import time
import json
import math
import random
import datetime

from init_chromedriver import init_chromedriver

def get_videos_list(json_filename):
    videos_lists = []

    if not os.path.exists(json_filename):
        print("[-]: Watch Videos Failed! JSON file doesn't exist!")
        return videos_lists

    json_file     = open(json_filename, "r")
    json_elems    = json.load(json_file)

    videos_address = json_elems["ADDRESS"]
    videos_lists   = json_elems["LISTS"]

    json_file.close()

    return videos_address, videos_lists

def watch_videos(driver, json_filename="videos.json", watch_nums=6):
    videos_address, videos_lists = get_videos_list(json_filename)
    random.seed(datetime.datetime.now)

    url_random  = random.randint(1, len(videos_address))
    for index, address_key in enumerate(videos_address):
        if index + 1 == url_random:
            video_address_key = address_key
    
    video_url = videos_address[video_address_key]

    titles_random = random.randint(1, len(videos_lists[video_address_key]))
    for index, title_key in enumerate(videos_lists[video_address_key]):
        if index + 1 == titles_random:
            video_title_key = title_key
    
    video_title_list = videos_lists[video_address_key][video_title_key]

    videos_per_title = math.ceil(watch_nums / len(video_title_list))

    """
    观看视频
    """
    # 视频好像会需要每天都看新的，前一天看的算旧的，今天再看不算任务
    driver.get(video_url)
    driver.implicitly_wait(3 + random.random())

    driver.find_elements_by_xpath("//*[contains(text(), '" + video_title_key + "')]")[0].click()
    time.sleep(2 + random.random())

    print("[+]: Watching: ", video_title_key)
    for title in video_title_list:
        print("[+]: - Watching: ", title)
        driver.find_elements_by_xpath("//*[contains(text(), '" + title + "')]")[0].click()
        time.sleep(2 + random.random())

        #这个是直接打开页面，是图文
        videos = driver.find_elements_by_xpath("//div[@class='textWrapper']")
        time.sleep(1 + random.random())

        # 上面是图文选取，如果你想点到列表里面选取，则改为以下代码：
        # titles = driver.find_elements_by_xpath("//*[contains(text(), '列表')]")[0]
        # titles.click()
        # videos = driver.find_elements_by_xpath("//div[@class='text-link-item-title']")

        # for i, video in enumerate(videos):
        for i in range(videos_per_title):
            video_index = random.randint(0, len(videos)-1)
            video       = videos[video_index]
            video.click()
            all_handles = driver.window_handles
            driver.switch_to.window(all_handles[-1])
            time.sleep(0.1+random.random())

            #模拟点击播放，因为直接点开连接播放，积分不会增长，可能也是因为反爬机制，必须刷新页面后，点击播放才算做是观看一次
            driver.get(driver.current_url)
            print("[+]: --", i+1, '/', 2, '\t', driver.current_url)

            driver.find_element_by_xpath("//div[@class='outter']").click()
            time.sleep(3 + random.random())

            # 可以获取视频当前时长，但是没有必要，只要看3分钟就好了
            # video_current_time_str = driver.find_element_by_xpath("//span[@class='current-time']").get_attribute('innerText')
            # print(video_current_time_str)
            # video_duration = int(video_duration_str.split(':')[0]) * 60 + int(video_duration_str.split(':')[1])

            # 每个视频开启后停留190秒，然后把所有句柄关闭
            time.sleep(180 + random.random()*10)
            driver.close()
            driver.switch_to.window(all_handles[0])

            # 保持学习，直到视频结束
            # time.sleep(video_duration + 3)

    print("[+]: 播放视频完毕\n")


def main():
    driver = init_chromedriver(show_flag=True)

    videos_address, videos_lists = get_videos_list("videos.json")
    url_random  = random.randint(1, len(videos_address))
    for index, address_key in enumerate(videos_address):
        if index + 1 == url_random:
            video_address_key = address_key
    
    video_url = videos_address[video_address_key]

    titles_random = random.randint(1, len(videos_lists[video_address_key]))
    for index, title_key in enumerate(videos_lists[video_address_key]):
        if index + 1 == titles_random:
            video_title_key = title_key

    video_title_list = videos_lists[video_address_key][video_title_key]

    print(video_url)
    print(video_title_list)

    watch_videos(driver)

if __name__ == '__main__':
    main()
