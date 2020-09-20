'''
Main function for get global500
Author: Sunic
For:    Champagne
'''

import openpyxl
from get_data_global500 import get_data_global500
from get_industry_cat import get_industry_cat
from write_excel import write_excel

def main():
    root_url       = 'https://www.caifuzhongwen.com/fortune500/paiming/global500/2020_%E4%B8%96%E7%95%8C500%E5%BC%BA.htm'
    out_excel      = 'result.xlsx'
    
    industry_dict  = get_industry_cat(root_url)
    company_list   = get_data_global500(root_url)
    write_excel(industry_dict, company_list, out_excel)

if __name__ == '__main__':
    main()