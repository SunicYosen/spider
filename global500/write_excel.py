
import openpyxl
import get_data_global500
import get_industry_cat

def write_excel(industry_dict, company_list, out_file='result.xlsx'):

    wb = openpyxl.Workbook()

    for key in industry_dict:
        ws        = wb.create_sheet(str(industry_dict[key]))
        menu_row  = ['2021年500强排名', '公司名', '销售额销售额\n百万美元', '国家', '员工数', '营收', '% vs 上一年', '利润', '% vs上一年', '总资产', '股东权益']
        ws.append(menu_row)
        # ws['D2'] = '销售额M$'
        # ws['E2'] = '国家'
        # ws['F2'] = '员工数'
        # ws['G2'] = '营收'
        # ws['H2'] = '% vs 上一年'
        # ws['I2'] = '利润'
        # ws['J2'] = '% vs上一年'
        # ws['K2'] = '总资产'
        # ws['L2'] = '股东权益'

    for company in company_list:
        ws = wb.get_sheet_by_name(company.industry)
        data_first_line = [company.rank, company.company_name, company.revenue, company.country, company.employee, company.revenue, company.revenue_change_percent, company.profit, company.profit_change_percent, company.total_money, company.shareholders_equity]
        ws.append(data_first_line)
        ws.append([''])

    wb.save(out_file)

    print("[+] Info: Write Excel Done!")

if __name__ == '__main__':
    root_url       = 'https://www.caifuzhongwen.com/fortune500/paiming/global500/2021_%e4%b8%96%e7%95%8c500%e5%bc%ba.htm'
    industry_dict  = get_industry_cat(root_url)
    company_list   = get_data_global500(root_url)
    write_excel(industry_dict, company_list)

