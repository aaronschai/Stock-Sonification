# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 21:07:27 2019

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

import pyaudio
import numpy as np

def generateFreq(values, minFreq, maxFreq):
    min1 = values[0]
    max1 = values[0]
    print(values)
    for v in values:
        if v < min1:
            min1 = v
        if v > max1:
            max1 = v
    freqVal = []
    
    for v in values:
        tmpVal = (v-min1)/(max1 - min1)*(maxFreq - minFreq) + minFreq
        freqVal.append(tmpVal)
    print(values)
    return freqVal

def toSound(freqVal):
    p = pyaudio.PyAudio()
    
    volume = 0.5     # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz, must be integer
    duration = 0.5   # in seconds, may be float
    stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)
    for f in freqVal:
        # sine frequency, Hz, may be float
        
        # generate samples, note conversion to float32 array
        samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
        
        # for paFloat32 sample values must be in range [-1.0, 1.0]
        
        
        # play. May repeat with different volume values (if done interactively) 
        stream.write(volume*samples)
        
    stream.stop_stream()
    stream.close()
    
    p.terminate()
    
if __name__ == '__main__':
    t1 = generateFreq(df['Adj Close'], 440, 880)
    print(t1)
    toSound(t1)