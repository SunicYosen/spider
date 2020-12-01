"""
Country Class
['','','国家','累计确诊','现有确诊','累计治愈','治愈率','累计死亡','死亡率','感染率','人口','人口密度','GDP','人均GDP']
"""

class Country:
    def _init_(self):
        self.rank             = 0
        self.name             = ''
        self.conv19_new       = 0
        self.conv19_all       = 0
        self.conv19_current   = 0
        self.conv19_cure_new  = 0
        self.conv19_cure      = 0
        self.conv19_cure_rate = 0
        self.death_new        = 0
        self.death_all        = 0
        self.death_rate       = 0
        self.conv19_rate      = 0
        self.peoples          = 0
        self.peoples_density  = 0
        self.gdp              = 0
        self.gdp_per          = 0
