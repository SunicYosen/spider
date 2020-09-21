import os
import time
from get_url import get_url_global500
from get_canvas import get_canvas

def get_pictures(pic_path='output', company_urls=[], indexes=range(500)):
    numbers      = len(indexes)
    time_begin   = time.time()
    
    for rank in indexes:
        duration  = round(time.time() - time_begin, 2)
        print("[+] Getting Data :{}/{}，Cost Time: {}s".format(rank, numbers, duration), end="\r")
        
        if not os.path.exists(os.path.join(str(pic_path), str(rank+1))):
            os.makedirs(os.path.join(str(pic_path), str(rank+1)))
            get_canvas(company_urls[rank], os.path.join(str(pic_path), str(rank+1)))
        else:
            print("[+] Info: '"+str(os.path.join(str(pic_path), str(rank+1)))+"' exists, Skip!")

    print("\n[+] Info: Got Pictures Done! ")

if __name__ == '__main__':
   company_urls, names = get_url_global500("https://www.caifuzhongwen.com/fortune500/paiming/global500/2020_%E4%B8%96%E7%95%8C500%E5%BC%BA.htm")
   get_pictures('output', company_urls)
