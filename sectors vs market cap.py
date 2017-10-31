import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.style as style
style.use('fivethirtyeight')

from util_nepse import clean_names

#read dataset
df = pd.read_csv('company_full_25_10_2017.csv')
df.columns = clean_names(list(df.columns))

df['sector'] = np.where(df['sector']=='Development Bank Limited', 
                                        'Development Banks',np.where(
                        df['sector']=='Manufacturing And Processing',
                                        'Manufactur & Process',
                                        df['sector']))

# change object data to float
df['market_capitalization_rs'] = df['market_capitalization_rs'].str.replace(',','').astype('float')/1000000000
df['total_listed_shares'] = df['total_listed_shares'].str.replace(',','').astype('float')/1000000000

print("total market capital is ", np.sum(df['market_capitalization_rs']))
print("total_share ", np.sum(df['total_listed_shares']))

# plot sectors vs market cap
plt.figure(figsize=(10, 5))
plt.tick_params(axis = 'both', which = 'major', labelsize = 12)
sns.swarmplot(x='sector', y='market_capitalization_rs', data=df, size=4, linewidth=1)
plt.xticks(rotation=-75)
plt.text(y=-75, x =-1,
    s = '   ©Rpy3                                                                                                                                Source: NEPSE   ',
    fontsize = 14, color = '#f0f0f0', backgroundcolor = 'grey')
plt.text(x = -1, y = 155, s = "Sectors Vs Market capital (Billion Rs.)",
               fontsize = 26, weight = 'bold', alpha = .75)
plt.text(x = -1, y = 137, 
               s = 'NEPSE has total market capital of Rs. 1818.8 billion and total no of shares 4.9 Billion.\nDemoniated by banks and insurances.',
              fontsize = 16, alpha = .85)
plt.text(x = 0.13, y = 126, s = 'NTC', color = 'grey', fontsize = 8, weight = 'bold', backgroundcolor = '#f0f0f0')
plt.text(x = 1.13, y = 99, s = 'Nabil', color = 'grey', fontsize = 8, weight = 'bold', backgroundcolor = '#f0f0f0')
plt.text(x = 2.13, y = 61, s = 'Nepal Life', color = 'grey',  fontsize = 8, weight = 'bold', backgroundcolor = '#f0f0f0')
plt.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)
plt.xlabel("")
plt.ylabel("")
plt.savefig('plot.png', dpi =144, bbox_inches='tight')
plt.close()

#-----------------------------------------------------------------------------------------------#
