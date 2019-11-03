# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 18:52:41 2019

@author: aaron
"""

import bs4 as bs 
''' html parsing libary || turns source code into Beautiful Soup object which 
can be treated like a typical python object'''
import pickle
''' saving info so that wikipedia only needs to be hit once'''
import requests
''' grabs source code'''

import datetime as dt
'''specify dates for the Pandas datareader'''
import os
'''check for and create directories'''
import pandas_datareader.data as web



def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    
    tickers = []
    for row in table.findAll('tr')[1:]:
        '''tr is html for table row '''
        ticker = row.findAll('td')[0].text
        '''td is table data'''
        tickers.append(ticker)
        
    with open("sp500tickers.pickle","wb") as f:
        '''wb = write bits'''
        pickle.dump(tickers,f)
        ''' saving the tickers to file'''
    return tickers

#save_sp500_tickers()
    
def get_data_from_yahoo(reload_sp500=False):
    '''if reload_sp500 is true, then find the tickers, if false, open file'''
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
            
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
        '''make a new directory (os) if it doesn't exist already'''
        
    start = dt.datetime(2010, 1, 1)
    end = dt.datetime.now()
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
        
#get_data_from_yahoo()

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
        '''pull ticker data'''
    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers[:69]):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        '''using enumerate so that we know we are reading in all data'''
        '''can also just iterate through tickers'''

        df.rename(columns={'Adj Close': ticker}, inplace=True)
        '''renamed the Adj Close column to whatever the ticker name is'''
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
        '''getting rid of the other columns'''
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
        '''main_df combines all the individual dfs | outer joins all rows'''

        if count % 10 == 0:
            print(count)
            '''just to make sure its counting'''
        
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

compile_data()
                
    

