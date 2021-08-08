import os
import json
import requests
from lxml import etree

def get_industry_cat(root_url, cat_file='cat2021.json'):
    industry_cat_dict = {}

    got_cat = False

    if os.path.isfile(cat_file):
        try:
            with open(cat_file, 'r', encoding="utf-8") as f:
                industry_cat_dict = json.load(f)
            got_cat = True
        except:
            print("[-]: Load cat json failed!")
            os.remove(cat_file)
            got_cat = False

    if not industry_cat_dict:
        got_cat = False
    
    if not got_cat:
        try:
        # with open("cat.html", 'w') as cat_html:
            requests_session  = requests.session()
            
            response          = requests_session.get(root_url)
            response.encoding = response.apparent_encoding
            data              = response.text
            # cat_html.write(data)

            s                 = etree.HTML(data) 
            industry_cat_path = s.xpath('/html/body/main/div[1]/div[6]/div[2]/div/div/div/div[2]')[0]
            index             = 1

            while True:
                try:
                    index        = index + 1
                    industry_cat = industry_cat_path.xpath('./p[{}]/a/text()'.format(index))[0]
                    industry_cat_dict.update({index-1:industry_cat})
                except:
                    print("[+] Info: End of industry. Total: " + str(index-2))
                    break

            with open(cat_file, 'w', encoding="utf-8") as f:
                json.dump(industry_cat_dict, f, ensure_ascii=False,indent = 4)

        except:
            print("ERROR: Error parse the website content!\n")
    
    return industry_cat_dict


if __name__ == '__main__':
    cat2021_dict = get_industry_cat("https://www.caifuzhongwen.com/fortune500/paiming/global500/2021_%e4%b8%96%e7%95%8c500%e5%bc%ba.htm", cat_file='cat2021.json')
    cat2020_dict = get_industry_cat("https://www.caifuzhongwen.com/fortune500/paiming/global500/2020_%E4%B8%96%E7%95%8C500%E5%BC%BA.htm", cat_file='cat2020.json')

    assert cat2021_dict == cat2020_dict

    for key in cat2021_dict:
        print(str(key-1)+'\t: '+str(cat2021_dict[key]))
