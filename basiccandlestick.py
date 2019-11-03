# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 23:25:21 2019

@author: aaron
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
style.use('ggplot')

df = pd.read_csv('TSLA.csv', parse_dates=True, index_col=0)

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()
print(df_ohlc.head())

"""Unfortunately, making candlestick graphs right from Pandas isn't built 
in, even though creating OHLC data is.
So, we want to now move this information to matplotlib, as well as 
convert the dates to the mdates version."""

df_ohlc = df_ohlc.reset_index()
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
"""converts from dates to mdates which is the date type matplotlib graphs"""

fig = plt.figure()
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)

ax1.xaxis_date() 
"""converts the axis from the raw mdate numbers to dates"""


candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
'''instead of the bar chart, we fill between 0 and the height of the volume '''
plt.show()