"""""""""""""""
Main Function
"""""""""""""""

import os
from get_fund_code import get_fund_code

from fund import Fund
from write_excel import write_excel

def main():
    base_url        = 'http://fund.eastmoney.com'
    data_excel      = 'data.xlsx'

    if not os.path.exists(data_excel):
        print('[-] Error: Data Excel {} does not Exists!'.format(data_excel))
        return

    fund_code_array = get_fund_code(data_excel)
    fund_data_dict  = {}
    for fund_code in fund_code_array:
        fund_url = base_url + '/' + fund_code + '.html'
        fund     = Fund(fund_url)
        fund.get_all_data()
        fund_data_dict.update({fund_code:fund})
        print("[+] Info: {}:{} Done!".format(fund_code, fund.name))
        
    write_excel(fund_data_dict, excel_file=data_excel)

if __name__ == '__main__':
    main()
