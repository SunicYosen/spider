#

class Company:
    data_year              = '2021'
    money_unit             = 'Million U.S. Dollar'
    company_name           = ''
    company_name_en        = ''
    rank                   = 0
    industry               = ''
    revenue                = ''
    country                = ''
    city                   = ''
    employee               = 0
    revenue_change_percent = 0.0
    profit                 = 0
    profit_change_percent  = 0.0
    total_money            = 0
    shareholders_equity    = 0
    ceo                    = ''
    website                = ''
    data_site              = ''
    image1_suffix          = '历年营收与利润'
    image2_suffix          = '历年排名'
    image3_suffix          = '历年总资产'

    def __init__(self, data_dict) -> None:
        try:
            self.data_year              = data_dict['data_year']
            self.money_unit             = data_dict['money_unit']
            self.company_name           = data_dict['company_name']
            self.company_name_en        = data_dict['company_name_en']
            self.rank                   = data_dict['rank']
            self.industry               = data_dict['industry']
            self.revenue                = data_dict['revenue']
            self.country                = data_dict['country']
            self.city                   = data_dict['city']
            self.employee               = data_dict['employee']
            self.revenue_change_percent = data_dict['revenue_change_percent']
            self.profit                 = data_dict['profit']
            self.profit_change_percent  = data_dict['profit_change_percent']
            self.total_money            = data_dict['total_money']
            self.shareholders_equity    = data_dict['shareholders_equity']
            self.ceo                    = data_dict['ceo']
            self.website                = data_dict['website']
            self.data_site              = data_dict['data_site']
            self.image1_suffix          = data_dict['image1_suffix']
            self.image2_suffix          = data_dict['image2_suffix']
            self.image3_suffix          = data_dict['image3_suffix']
        except:
            print("[-]: Initial with dict failed!")

    def keys(self):
        return ('data_year',
                'money_unit',
                'company_name',
                'company_name_en',
                'rank',
                'industry',
                'revenue',
                'country',
                'city',
                'employee',
                'revenue_change_percent',
                'profit',
                'profit_change_percent',
                'total_money',
                'shareholders_equity',
                'ceo',
                'website',
                'data_site',
                'image1_suffix',
                'image2_suffix',
                'image3_suffix')

    def __getitem__(self, item):
        return getattr(self, item)