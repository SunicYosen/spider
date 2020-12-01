import csv

def write_csv(country_list, out_file='result.csv'):
    csv_file   = open(out_file, "w", newline="")
    csv_writer = csv.writer(csv_file)

    menu_row  = ['排名','国家','新增','累计确诊','现有确诊','新增治愈','累计治愈','治愈率(%)','新增死亡','累计死亡','死亡率(%)','感染率','人口(万人)','人口密度(平方千米)','GDP亿美元','人均GDP万美元']
    csv_writer.writerow(menu_row)

    for country in country_list:
        country_line = [country.rank,
                        country.name,
                        country.conv19_new,
                        country.conv19_all,
                        country.conv19_current,
                        country.conv19_cure_new,
                        country.conv19_cure,
                        country.conv19_cure_rate,
                        country.death_new,
                        country.death_all,
                        country.death_rate,
                        country.conv19_rate,
                        country.peoples,
                        country.peoples_density,
                        country.gdp,
                        country.gdp_per]

        csv_writer.writerow(country_line)
    
    print("[+] Info: Write CSV Done!")

    csv_file.close()
