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
    root_url       = 'https://www.caifuzhongwen.com/fortune500/paiming/global500/2021_%e4%b8%96%e7%95%8c500%e5%bc%ba.htm'
    out_excel      = 'result.xlsx'
    
    industry_dict  = get_industry_cat(root_url)
    company_list   = get_data_global500(root_url)
    write_excel(industry_dict, company_list, out_excel)

if __name__ == '__main__':
    main()