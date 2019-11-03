# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 22:32:17 2019

@author: aaron
"""
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
'''pandas to manipulate data, and the pandas_datareader is the newest pandas io library'''
import mpld3
mpld3.enable_notebook

style.use('ggplot')

''' for saving a dataframe to a csv '''
'''
start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()
df = web.DataReader("TSLA", 'yahoo', start, end)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)
df.to_csv('TSLA.csv')
'''


'''reading a csv file into a data frame'''
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
print(df.head())

'''plotting '''
'''df.plot()
    plt.show()'''
    
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])
''' does volume in terms of a bar chart '''

plt.show()