"""
Main
"""

import time
from datetime import datetime

from qa.huqas import HuQAS
from excel import Excel

from openpyxl.styles import Font

def get_hu_qas():
    base_url  = "http://sns.sseinfo.com/"
    lmt_date  = datetime.strptime("2020-09-01",  "%Y-%m-%d")
    key_words = ['华为', '供应', '断供']
    save_file = "results/hu-info.xlsx"
    
    excel     = Excel(save_file)
    huqas     = HuQAS(base_url)

    current_month = 0
    current_year  = 2021

    for keyword in key_words:
        data_arrays = []
        huqas.go_to_base_page()
        huqas.set_keyword(keyword=keyword)
        huqas.click_change_page()

        while(True):
            huqas.scroll_bottom()
            huqas.get_qas()
            time_str = huqas.qas[-1].q_time if (huqas.qas[-1].a_time == 'NONE') else  huqas.qas[-1].a_time
            try:
                last_time = datetime.strptime(time_str.split(' ')[0], "%m月%d日")

                if(last_time.month == 12 and current_month == 1):
                    current_year = current_year - 1

                current_month  = last_time.month

            except:
                last_time = lmt_date

            last_time = datetime.strptime("{}-{}-{}".format(current_year, last_time.month, last_time.day), "%Y-%m-%d")

            print("{}:\t{}-{}-{}".format(keyword, last_time.year, last_time.month, last_time.day))

            if (last_time < lmt_date):
                break

            huqas.click_next_page()

        excel_col_width  = {'A': 20, 'B':20, 'C':10, 'D':100, 'E':100}
        excel.write(sheet_name=keyword, data_array=["日期","公司名称","公司代码","问题","回答"])

        for qa in huqas.qas:
            data_arrays.append([qa.q_time.split(' ')[0], qa.company_name, qa.company_code, qa.question, qa.answer])
        
        excel.write_list(sheet_name=keyword, data_arrays=data_arrays)
        excel.set_col_width(sheet_name=keyword, cols_width=excel_col_width)
        excel.set_row_auto_wraptext_center(sheet_name=keyword, all=True)
        excel.set_font(sheet_name=keyword, font_style=Font(name='Times New Roman'), all=True)

if __name__ == "__main__":
    get_hu_qas()