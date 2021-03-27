"""
Main
"""

import time
from datetime import datetime

from qa.shenqas import ShenQA
from excel import Excel

from openpyxl.styles import Font

def get_shen_qas():
    base_url  = "http://irm.cninfo.com.cn/"
    lmt_date  = datetime.strptime("2020-09-01",  "%Y-%m-%d")
    key_words = ['华为', '断供']
    save_file = "results/shen-info.xlsx"
    
    excel     = Excel(save_file)
    shenqa    = ShenQA(base_url)

    for keyword in key_words:
        data_arrays = []
        shenqa.go_to_base_page()
        shenqa.set_keyword(keyword=keyword)
        shenqa.click_change_page()

        while(True):
            shenqa.get_qas()
            print("{}:\t{}".format(keyword, shenqa.qas[-1].qa_time))
            try:
                last_time = datetime.strptime(shenqa.qas[-1].qa_time, "%Y-%m-%d")
            except:
                last_time = lmt_date

            if (last_time < lmt_date):
                break

            shenqa.click_next_page()

        excel_col_width  = {'A': 20, 'B':20, 'C':10, 'D':100, 'E':100}
        excel.write(sheet_name=keyword, data_array=["日期","公司名称","公司代码","问题","回答"])

        for qa in shenqa.qas:
            data_arrays.append([qa.qa_time, qa.company_name, qa.company_code, qa.question, qa.answer])
        
        excel.write_list(sheet_name=keyword, data_arrays=data_arrays)
        excel.set_col_width(sheet_name=keyword, cols_width=excel_col_width)
        excel.set_row_auto_wraptext_center(sheet_name=keyword, all=True)
        excel.set_font(sheet_name=keyword, font_style=Font(name='Times New Roman'), all=True)

if __name__ == "__main__":
    get_shen_qas()