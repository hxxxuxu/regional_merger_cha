##This file is to analysis the trend and the number of changes in both country 
##and each province's perspective.
##Stay in the folder 'Annual_by_Province'.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
plt.rcParams['figure.dpi'] = 300

##Read the country's data
#Give the new index and the column names to make them convinience to refer to.
country = pd.read_csv('new_annual.csv',index_col=0)
country.index = new_index
#Drop the column 2023 as it has not been published so far.
country = country.drop(columns='2023')
#reverse the order of the columns, so now the data shouls be from 2024 to 2022.
country = country[country.columns[::-1]]

#Count the yearly changes
change_c = country.diff(periods=1,axis=1)
#Get the absolute number of the change
change_c_abs = country.diff(periods=1,axis=1).abs()
#As we didn't include 2003' data, fill the 'nan' with 0 in column 2004
change_c['2004'] = change_c['2004'].fillna(0)
change_c_abs['2004'] = change_c_abs['2004'].fillna(0) 


#plot the yearly changes of each reigion level (in details) in the country.
plot_data = change_c.T
fig,ax1 = plt.subplots()
plot_data.plot(ax=ax1)
ax1.legend(loc='best',bbox_to_anchor=(1.35,0.9))
ax1.set_xlabel('Year',fontsize=12)
ax1.set_ylabel('')
fig.suptitle('Annual Changes for Each Region Level: 2004-2022',fontsize=16)
fig.savefig('annual_changes_by_region.png',bbox_inches='tight')



#compute the number of changes in each year
annual_sum_c = change_c_abs.sum(axis=0)
#plot the annual number of changes
fig,ax1 = plt.subplots()
plot_data = {'Number of Changes':annual_sum_c}
plot_data = pd.DataFrame(plot_data)
plot_data.plot(ax=ax1)
ax1.set_xlabel('Year',fontsize=12)
plt.xticks(rotation=45)
fig.suptitle('Annual Reginal Changes (2004-2022)',fontsize=16)
fig.savefig('ann_changes.png',bbox_inches='tight')




#Compute the number of changes for rural and urban region
rur_urb_index = ['urban','urban','rural','urban','rural','urban']
def area_group(df,idx_list):
    grouped = df.loc[['pref_city_distr','county_city','county','city_town','rural_town','street']]
    grouped = grouped.set_index([idx_list,grouped.index])
    return grouped
    
rur_urb_change = area_group(change_c,rur_urb_index).groupby(level=0).sum()
rur_urb_change_abs = area_group(change_c_abs,rur_urb_index).groupby(level=0).sum()

#plot the changes based on the group 
plot_data = rur_urb_change.T
fig,(ax1,ax2) = plt.subplots(2,1,sharex=True,figsize=(10,7))
ax1.bar(plot_data.index,plot_data['urban'],color='#9467bd')
ax2.bar(plot_data.index,plot_data['rural'],color='#ff7f0e')
ax1.set_title('Changes in Urban Area')
ax2.set_title('Changes in Rural Area')
fig.savefig('urban_rural_change.png')
