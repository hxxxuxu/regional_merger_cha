##This script is to calculate the changes in each province and merge 
##the csv file with the gpkg file of China.
import csv
import pandas as pd
import geopandas as gpd

name_dict_key = ['Beijing','Tianjin','Hebei','Shanxi','Inner Mongolia','Liaoning','Jilin','Heilongjiang',
                 'Shanghai','Jiangsu','Zhejiang','Anhui','Fujian','Jiangxi','Shandong','Henan','Hubei','Hunan',
                 'Guangdong','Guangxi','Hainan','Chongqing','Sichuan','Guizhou','Yunnan','Tibet','Shaanxi',
                 'Gansu','Qinghai','Ningxia','Xinjiang']

region_index = ['prefecture','prefecture','county','county','county','county','county','township','township','township','township']
def reidx_group(df,idx_list):
    df = df.set_index([idx_list,df.index])
    return df

#get which province or part have the most changes
num_change = []
rel_change=[]
p_levle_pre = []
p_levle_county = []
p_levle_town = []
p_area_urb = []
p_area_rur = []
for province,file in zip(name_dict_key,new_province):
    province = pd.read_csv(file)
    province.set_index(province.columns[0],inplace=True)
    province = province[province.columns[::-1]]
    
    #get the total times of the change
    province_c = province.diff(periods=1,axis=1)
    province_c.fillna(0,inplace=True)
    province_c_abs = province_c.abs()
    sum_change = province_c_abs.values.sum()
    num_change.append(sum_change)
    reln_change = province_c.values.sum()
    rel_change.append(reln_change)
    #compute the number of changes based on the region level
    province_c_by_lev = reidx_group(province_c,region_index).groupby(level=0).sum().sum(axis=1)
    p_levle_pre.append(province_c_by_lev['prefecture'])
    p_levle_county.append(province_c_by_lev['county'])
    p_levle_town.append(province_c_by_lev['township'])
    
    #compute the number of changes based on urban or rural area
    province_c_by_area = area_group(province_c,rur_urb_index).groupby(level=0).sum().sum(axis=1)
    p_area_urb.append(province_c_by_area['urban'])
    p_area_rur.append(province_c_by_area['rural'])

#Form a dataframe to store the numbers
province_sum = pd.DataFrame(index=name_dict_key)
province_sum['Number of changes'] = num_change
province_sum['Changes Relative to 2004']= rel_change
province_sum['Prefecture level Change'] = p_levle_pre
province_sum['County level Change'] = p_levle_county
province_sum['Township level Change'] = p_levle_town
province_sum['Urban regions Change'] = p_area_urb
province_sum['Rural regions Change'] = p_area_rur

province_sum.to_csv('Province_Summary.csv')


#merge the dataset to creat a gpkg file
province_shape = gpd.read_file('gadm36_CHN.gpkg', layer='gadm36_CHN_1')
#replace provinces' names that are not the same in two dataset.
print(province_shape['NAME_1'])
replace_dict = {'Nei Mongol':'Inner Mongolia','Ningxia Hui':'Ningxia','Xinjiang Uygur':'Xinjiang','Xizang':'Tibet'}
province_shape['NAME_1'] = province_shape['NAME_1'].replace(replace_dict)
province_shape = province_shape.merge(province_sum,left_on='NAME_1',right_on=province_sum.index,validate='1:1',indicator=True)
print(province_shape['_merge'].value_counts())
province_shape = province_shape.drop(columns='_merge')
province_shape.to_file('reigional_merger.gpkg')
