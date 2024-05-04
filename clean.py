##This script is to clean the data downloaded from the website.
##Open the folder 'Annual_by_Province'
import csv
import pandas as pd

##Select the rows that we need and write into a new csv file.
#For the country's data
file = open('Annual.csv',encoding='GBK')
read_rows = csv.reader(file)
rows = [row for row in read_rows]
new_rows = rows[2:-1]
with open('new_annual.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(new_rows)

##Select the rows that we need and write into new csv files.
#for the provinces' data

name_dict_key = ['Beijing','Tianjin','Hebei','Shanxi','Inner Mongolia','Liaoning','Jilin','Heilongjiang',
                 'Shanghai','Jiangsu','Zhejiang','Anhui','Fujian','Jiangxi','Shandong','Henan','Hubei','Hunan',
                 'Guangdong','Guangxi','Hainan','Chongqing','Sichuan','Guizhou','Yunnan','Tibet','Shaanxi',
                 'Gansu','Qinghai','Ningxia','Xinjiang']
name_dict_value = ['AnnualbyProvince.csv','AnnualbyProvince-2.csv','AnnualbyProvince-3.csv','AnnualbyProvince-4.csv',
                  'AnnualbyProvince-5.csv','AnnualbyProvince-6.csv','AnnualbyProvince-7.csv','AnnualbyProvince-8.csv',
                  'AnnualbyProvince-9.csv','AnnualbyProvince-10.csv','AnnualbyProvince-11.csv','AnnualbyProvince-12.csv',
                  'AnnualbyProvince-13.csv','AnnualbyProvince-14.csv','AnnualbyProvince-15.csv','AnnualbyProvince-16.csv',
                  'AnnualbyProvince-17.csv','AnnualbyProvince-18.csv','AnnualbyProvince-19.csv','AnnualbyProvince-20.csv',
                  'AnnualbyProvince-21.csv','AnnualbyProvince-22.csv','AnnualbyProvince-23.csv','AnnualbyProvince-24.csv',
                  'AnnualbyProvince-25.csv','AnnualbyProvince-26.csv','AnnualbyProvince-27.csv','AnnualbyProvince-28.csv',
                  'AnnualbyProvince-29.csv','AnnualbyProvince-30.csv','AnnualbyProvince-31.csv']
#set a new index fot the csv files at the same time.
new_index = ['pref_reg','pref_city','county_reg','pref_city_distr','county_city','county',
            'auto_county','town_reg','city_town','rural_town','street']
#creat a list for new file names for future convenience
new_province = []

for name,file in zip(name_dict_key,name_dict_value):
    province = open(file,encoding='GBK')
    read_rows = csv.reader(province)
    rows = [row for row in read_rows]
    new_rows = rows[3:-1]
    with open(f'{name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(new_rows)
    new_province.append(f'{name}.csv')
    df = pd.read_csv(f'{name}.csv')
    df.index = new_index
    df = df.drop(columns = ['2023','Indicators'])
    df.to_csv(f'{name}.csv')