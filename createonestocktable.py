# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 15:01:39 2019

@author: aaron
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import mpld3
mpld3.enable_notebook

style.use('ggplot')


start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()
df = web.DataReader("EXC", 'yahoo', start, end)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)
df.to_csv('EXC.csv')
