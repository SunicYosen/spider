'''
 Fund Class
'''
import re
import time
import platform
# import requests
from lxml import etree
from selenium import webdriver

class Fund:
    def __init__(self, url):
        self.url                              = url
        self.html_tree                        = None
        self.name                             = ''
        self.code                             = '000000'
        self.current_valuation                = ''
        self.current_valuation_increase       = ''
        self.latest_net_value                 = ''
        self.latest_net_value_increase        = ''
        self.top10_holdings_proportion_growth = {'items':[], 'total':'', 'date':''}
        self.latest10_days_net_value_increase = []
        self.manager_name                     = ''
        self.setup_date                       = ''
        self.latest_date                      = ''
        self.latest_scale                     = ''
        self.date_scale_change_url            = ''
        self.date_scale_change                = []
        self.date_turnover_rate               = ''

    def __get_date_scale_change_html_source(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        # options.add_argument("--user-data-dir=/home/sun/.config/google-chrome/Default")
        # driver  = webdriver.Chrome(options=options)

        if platform.system().lower() == 'linux':
            driver = webdriver.Chrome(options=options)
        elif platform.system().lower() == 'windows':
            driver = webdriver.Chrome('./tools/win/chromedriver.exe', options=options)
        else:
            print('[-] Error', str(platform.system()), 'not supported!')
            exit()

        driver.get(url)
        time.sleep(0.1)

        buttons = driver.find_elements_by_class_name("ip_tips_btn")

        for button in buttons:
            if button.get_attribute("innerText") == "立即开启":
                driver.execute_script("arguments[0].scrollIntoView();", button)
                button.click()
                time.sleep(0.5)
                break

        scale_change_html_source = driver.page_source
        driver.quit()
        return scale_change_html_source

    def get_html_tree(self):
        try:
            html_text  = self.__get_date_scale_change_html_source(self.url)
            time.sleep(0.1)

            with open('test.html', 'w', encoding='utf-8') as html_file:
                html_file.write(html_text)

            self.html_tree = etree.HTML(html_text)

        except:
            print('[-] Warning: Get HTML Tree Failed!')
            self.html_tree = None


    def get_name(self):
        try:
            self.name = self.html_tree.xpath('.//div[@class="fundDetail-tit"]/div/text()')[0]
        except:
            print('[-] Warning: Get Name Failed!')
            self.name = ''

    def get_code(self):
        try:
            self.code = self.html_tree.xpath('.//div[@class="fundDetail-tit"]/div/span[2]/text()')[0]
        except:
            print('[-] Warning: Get Code Failed!')
            self.code = ''
            
    def get_current_valuation(self):
        try:
            self.current_valuation  = self.html_tree.xpath('.//div[@class="dataOfFund"]/dl[1]/dd/dl[1]/span[1]/text()')[0]
        except:
            print('[-] Warning: Get Current Valuation Failed!')
            self.current_valuation  = ''

    def get_current_valuation_increase(self):
        try:
            self.current_valuation_increase   = self.html_tree.xpath('.//div[@class="dataOfFund"]/dl[1]/dd/dl[3]/span[2]/text()')[0]
        except:
            print('[-] Warning: Get Current Valuation Increase Failed!')
            self.current_valuation_increase   = ''

    def get_latest_net_value(self):
        try:
            self.latest_net_value  = self.html_tree.xpath('.//div[@class="dataOfFund"]/dl[2]/dd/span[1]/text()')[0]
        except:
            print('[-] Warning: Get Latest Net Value Info Failed!')
            self.latest_net_value  = ''

    def get_latest_net_value_increase(self):
        try:
            self.latest_net_value_increase   = self.html_tree.xpath('.//div[@class="dataOfFund"]/dl[2]/dd/span[2]/text()')[0]
        except:
            print('[-] Warning: Get Latest Net Value Increase Info Failed!')
            self.latest_net_value_increase   = ''

    def get_manager_name(self):
        try:
            self.manager_name = self.html_tree.xpath('.//div[@class="infoOfFund"]/table/tbody/tr[1]/td[3]/a/text()')[0]
        except:
            print('[-] Warning: Get Manger Name Failed!')
            self.manager_name = ''

    def get_setup_date(self):
        try:
            self.setup_date = self.html_tree.xpath('.//div[@class="infoOfFund"]/table/tbody/tr[2]/td[1]/text()')[0].replace('：','')
        except:
            print('[-] Warning: Get Setup Date Info Failed!')
            self.setup_date = ''
            
    def get_latest_date(self):
        try:
            self.latest_date = self.html_tree.xpath('.//div[@class="infoOfFund"]/table/tbody/tr[1]/td[2]/text()')[0].replace('：','').split('（')[1].replace('）','')
        except:
            print('[-] Warning: Get Latest Date Info Failed!')
            self.latest_date = ''

    def get_latest_scale(self):
        try:
            self.latest_scale = self.html_tree.xpath('.//div[@class="infoOfFund"]/table/tbody/tr[1]/td[2]/text()')[0].replace('：','').split('（')[0]
        except:
            print('[-] Warning: Get Latest Scale Info Failed!')
            self.latest_scale = ''

    def get_top10_holdings_proportion_growth(self):
        try:
            quotation_items_left = self.html_tree.xpath('.//div[@class="quotationItem_left"]')[0]
            top10_holdings       = quotation_items_left.xpath('./div[2]/div[2]/ul/li[1]/div/table/tbody')[0]
            for i in range(2, 12):
                try:
                    stock_name       = top10_holdings.xpath('./tr[{}]/td[1]/a/text()'.format(i))[0]
                    stock_proportion = top10_holdings.xpath('./tr[{}]/td[2]/text()'.format(i))[0]
                    stock_growth     = top10_holdings.xpath('./tr[{}]/td[3]/span/text()'.format(i))[0]
                    self.top10_holdings_proportion_growth['items'].append([stock_name, stock_proportion, stock_growth])
                except:
                    break
            
            self.top10_holdings_proportion_growth['total'] = quotation_items_left.xpath('./div[2]/div[2]/ul/li[1]/div/p/span[1]/a/text()')[0] \
                                                           + quotation_items_left.xpath('./div[2]/div[2]/ul/li[1]/div/p/span[2]/text()')[0]

            self.top10_holdings_proportion_growth['date'] = quotation_items_left.xpath('./div[2]/div[2]/ul/li[1]/div[2]/span/text()')[0]

            # print(self.top10_holdings_proportion_growth)
        except:
            print('[-] Warning: Get Top10 Holdings Info Failed!')
            self.top10_holdings_proportion_growth   = {'items':[], 'total':'', 'date':''}

    def get_latest10_days_net_value_increase(self):
        try:
            quotation_items_left = self.html_tree.xpath('.//div[@class="quotationItem_left"]')[1]
            top10_holdings       = quotation_items_left.xpath('./div[2]/div[2]/ul/li[1]/div/table/tbody')[0]
            for i in range(2, 12):
                date       = top10_holdings.xpath('./tr[{}]/td[1]/text()'.format(i))[0]
                value      = top10_holdings.xpath('./tr[{}]/td[2]/text()'.format(i))[0]
                growth     = top10_holdings.xpath('./tr[{}]/td[4]/span/text()'.format(i))[0]
                self.latest10_days_net_value_increase.append([date, value, growth])
        except:
            print('[-] Warning: Get Lastest 10 Days Info Failed!')
            self.latest10_days_net_value_increase   = {}

    def get_date_scale_change_url(self):
        try:
            quotation_items_left = self.html_tree.xpath('.//div[@class="quotationItem_left quotationItem_left02"]')[0]
            self.date_scale_change_url = quotation_items_left.xpath('./div[4]/div[1]/div[1]/@data-href-more')[0]
        except:
            print('[-] Warning: Get Date Scale Change URL Failed!')
            self.date_scale_change_url = ''

    def get_date_scale_change(self):
        html_text = self.__get_date_scale_change_html_source(self.date_scale_change_url)
        html_tree = etree.HTML(html_text)

        # with open('test_gmbd.html', 'w', encoding='utf-8') as html_file: 
        #     html_file.write(html_text)

        change_data  = []
        change_table = html_tree.xpath('//*[@id="gmbdtable"]/table/tbody')[0]

        for i in range(1, 10):
            try:
                item_date = change_table.xpath('./tr[{}]/td[1]/text()'.format(i))[0]
                item_assets = change_table.xpath('./tr[{}]/td[5]/text()'.format(i))[0]
                change_data.append([item_date, item_assets])
            except:
                break

        self.date_scale_change = change_data

    def get_date_turnover_rate(self):
        try:
            quotation_items_left = self.html_tree.xpath('.//div[@class="quotationItem_left quotationItem_left02"]')[0]
            self.date_turnover_rate = quotation_items_left.xpath('./div[5]/div[2]/ul/li[2]/div/table/tbody/tr[2]/td[1]/text()')[0] + ': '\
                                    + quotation_items_left.xpath('./div[5]/div[2]/ul/li[2]/div/table/tbody/tr[2]/td[2]/text()')[0]
        except:
            print('[-] Warning: Get Date Turnover Failed!')
            self.date_turnover_rate = ''

    def get_all_data(self):
        self.get_html_tree()
        self.get_name()
        self.get_code()
        self.get_current_valuation()
        self.get_current_valuation_increase()
        self.get_latest_net_value()
        self.get_latest_net_value_increase()
        self.get_manager_name()
        self.get_setup_date()
        self.get_latest_date()
        self.get_latest_scale()
        self.get_top10_holdings_proportion_growth()
        self.get_latest10_days_net_value_increase()
        self.get_date_scale_change_url()
        self.get_date_scale_change()
        self.get_date_turnover_rate()

    def get_data_array(self):
        data_array = []
        top10_holdings_data = ''

        for top10_holding_item in self.top10_holdings_proportion_growth['items']:
            item_datas = ''
            for item_data in top10_holding_item:
                item_datas += (item_data + ' ')
            item_datas += '\n'
            top10_holdings_data += item_datas

        top10_holdings_data += (self.top10_holdings_proportion_growth['total']+'\n')
        top10_holdings_data += self.top10_holdings_proportion_growth['date']

        latest10_days_data = ''
        for latest10_days_item in self.latest10_days_net_value_increase:
            item_datas = ''
            for item_data in latest10_days_item:
                item_datas += (item_data + ' ')
            item_datas += '\n'
            latest10_days_data += item_datas

        data_scale_change_data = ''
        for data_scale_change_item in self.date_scale_change:
            item_datas = ''
            for item_data in data_scale_change_item:
                item_datas += (item_data + ' ')
            item_datas += '\n'
            data_scale_change_data += item_datas

        data_array     = [self.name,
                          self.code,
                          self.current_valuation,
                          self.current_valuation_increase,
                          self.latest_net_value,
                          self.latest_net_value_increase, 
                          top10_holdings_data,
                          latest10_days_data,
                          self.manager_name,
                          self.setup_date,
                          self.latest_date,
                          self.latest_scale,
                          data_scale_change_data,
                          self.date_turnover_rate
        ]

        return data_array

def test():
    url          = 'http://fund.eastmoney.com/008903.html'

    fund_example = Fund(url=url)
    fund_example.get_all_data()
    data_array = fund_example.get_data_array()
    print(data_array)
    print(fund_example.date_scale_change)

if __name__ == '__main__':
    test()
    