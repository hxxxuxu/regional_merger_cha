##Analysis country and province's data of the Sulphur Dioxide Emission 
##in Waste Gas(10000 tons) from 2004 to 2022
##Stay in folder 'so2data'
import csv
import pandas as pd
import geopandas as gpd

#read country's data
file = open('Annual.csv',encoding='GBK')
read_rows = csv.reader(file)
rows = [row for row in read_rows]
new_rows = rows[2:4]
with open('so2_annual.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(new_rows)
so2_c = pd.read_csv('so2_annual.csv')
#calculate the percentages change of the so2 emission
so2_c.index = so2_c['Indicators']
so2_c = so2_c.drop(columns=['2023','Indicators'])
so2_c = so2_c[so2_c.columns[::-1]]
so2_c_pct =so2_c.pct_change(axis=1) * 100
so2_c_pct.fillna(0,inplace=True)
so2_c_pct = so2_c_pct.round(2)

#read the provinces' data and compute the percentage change
file = open('AnnualbyProvince.csv',encoding='GBK')
read_rows = csv.reader(file)
rows = [row for row in read_rows]
new_rows = rows[3:-1]
with open('so2_province.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(new_rows)
so2_p = pd.read_csv('so2_province.csv')
so2_p.index = so2_p['Region']
so2_p = so2_p.drop(columns=['2023','Region'])
so2_p = so2_p[so2_p.columns[::-1]]
so2_p_pct =so2_p.pct_change(axis=1) * 100
so2_p_pct.fillna(0,inplace=True)
so2_p_pct = so2_p_pct.round(2)

#compute the percentage change of so2 emission between 2004 and 2022

so2_p['change'] = (so2_p['2022']-so2_p['2004'])/so2_p['2004'] * 100
so2_p['change'] = so2_p['change'].round(2)

#make a plot to check the country's trend on the regional changes and changes in so2 emission
chan_trend= country.sum(axis=0)
plot_data = {'Numbers happened in country':chan_trend,'Percentage changes for so2 emission':so2_c_pct}
#add a vertical line in year 2015
fig,(ax1,ax2) = plt.subplots(2,1,sharex=True,figsize=(10,7))
chan_trend.plot(ax=ax1,kind='line')
ax1.axvline(x=11, color='red', linestyle='--', linewidth=2)
ax1.set_title('Number of Regions from 2004 to 2022')
so2_c.T.plot(ax=ax2,kind='line')
ax2.axvline(x=11, color='red', linestyle='--', linewidth=2)
ax2.set_title('Sulphur Dioxide Emission from 2004 to 2022')
plt.legend()
fig.savefig('Comparison_reg_changes_so2.png')

#make a scatter plot to see if the changing trend of each procince's region numbers and its so2 emission match together

plot_data = {'Number of regional changes':province_sum['Changes Relative to 2004'],'Percentage changes of so2 emission':so2_p['change']}
plot_data = pd.DataFrame(plot_data)
scatter = sns.relplot(data=plot_data,x='Number of regional changes',y='Percentage changes of so2 emission',kind="scatter")
scatter.ax.axhline(0, color='black', linewidth=1, linestyle='--')  
scatter.ax.axvline(0, color='black', linewidth=1, linestyle='--') 
fig.savefig('scatter.png')

#merge the spatial data with the percentage change in so2 emission
so2_merge = so2_p['change'].to_frame()
province_shape = province_shape.merge(so2_merge,left_on='NAME_1',right_on=so2_merge.index,validate='1:1',indicator='merge_status')
print(province_shape['merge_status'].value_counts())
province_shape = province_shape.drop(columns='merge_status')
province_shape.to_file('reigional_merger.gpkg')