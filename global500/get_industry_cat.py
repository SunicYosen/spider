from lxml import etree
import requests
import time
import pandas as pd
import pandas as pd

def get_industry_cat(root_url):

    industry_cat_dict = {}

    try:
        data              = requests.get(root_url).text
        s                 = etree.HTML(data)
        industry_cat_path = s.xpath('/html/body/main/div[1]/div[4]/div[2]/div/div/div/div[2]')[0]
        index             = 1
        while True:
            try:
                index        = index + 1
                industry_cat = industry_cat_path.xpath('./p[{}]/a/text()'.format(index))[0].encode('iso-8859-1').decode('utf-8')
                industry_cat_dict.update({index:industry_cat})
            except:
                print("[+] Info: End of industry. Total: " + str(index-2))
                break

    except:
        print("ERROR: Error parse the website content!\n")
    
    return industry_cat_dict


if __name__ == '__main__':
    cat_dict = get_industry_cat("https://www.caifuzhongwen.com/fortune500/paiming/global500/2020_%E4%B8%96%E7%95%8C500%E5%BC%BA.htm")
    
    for key in cat_dict:
        print(str(key-1)+'\t: '+str(cat_dict[key]))
