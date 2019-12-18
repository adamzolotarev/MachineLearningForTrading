#indicators.py Your code that implements your indicators as functions that operate on dataframes. 
#The "main" code in indicators.py should generate the charts that illustrate your indicators in the report.

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data, plot_data

def author():
    return 'zzhang726' #Change this to your user ID 	

def momentum(df, window = 10):
    momentum_df = df/df.shift(window) - 1
    return momentum_df

def SMA(df, window = 10):
    SMA_df = df.rolling(window = window).mean()
    return SMA_df, (df)/SMA_df #(df-SMA_df)/SMA_df

def EMA(df, window = 10):
    EMA_df = df.copy()
    EMA_df.iloc[:] = np.NaN
    EMA_df.iloc[window-1] = df.iloc[0:window].mean()
    for i in range(window,df.index.size):
        EMA_df.iloc[i] = 2./(1+window)*(df.iloc[i] - EMA_df.iloc[i-1]) + EMA_df.iloc[i-1]
        
    return  EMA_df, (df)/EMA_df

def BollingerBands(df, window = 10):
    SMA_df = df.rolling(window = window).mean()
    std = df.rolling(window = window).std()
    upper_band = SMA_df + 2 * std
    lower_band = SMA_df - 2 * std
    return upper_band, lower_band, SMA_df,(df)/SMA_df, (df-SMA_df)/(2 * std)

def RSI(df, window = 10):
    delta = df.diff() #df-df.shift(1)
    delta_p = delta.where(delta>0, 0)
    delta_n = delta.where(delta<0, 0)
    p = delta_p.rolling(window = window).sum()    
    n = 0 - delta_n.rolling(window = window).sum()
    rs = p/n
    rsi_tmp = 100-100./(1+rs)        
    return rsi_tmp
    
def test_code():
    stock_symbol = 'JPM' #'APPL'
    start_date = '2010-01-01'
    #end_date = '2009-12-31'
    end_date = '2011-1-01'
    date_range = pd.date_range(start_date, end_date)
    stock_price = get_data([stock_symbol], date_range)
    stock_price = stock_price[stock_symbol]
    
    stock_price = stock_price / stock_price.values[0]    
    window = 20    
    bbu,bbl,SMA,SMAi,bbi = BollingerBands(stock_price,window = window)
    
    SMAu = SMA*1.05
    SMAl = SMA*0.95    
    
    EMA_df, EMA_i_df = EMA(stock_price, window = window)
    EMAu = EMA_df*1.05
    EMAl = EMA_df*0.95 
    #RSI_i = RSI(stock_price, window = window)
    #momentum_df = momentum(stock_price, window = window)
    
    plt.plot(bbu, label='upper BollingerBand')
    plt.plot(bbl, label='lower BollingerBand')
    plt.plot(SMA, label='SMA')
    plt.plot(stock_price, label='Stock Price')
    plt.axis([dt.date(2010,1,1), dt.date(2010,6,1), 0.8, 1.2])
    #plt.axis([0, 300, -256, 100])
    plt.xticks(rotation=30)
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.title('BollingerBand Indicator')
    #plt.legend(['Theoretically Optimal Strategy','Benchmark'])
    plt.legend(loc='upper left')
    plt.annotate('Selling Signal', xy=(dt.date(2010,4,15), 1.12), xytext=(dt.date(2010,4,1), 1.17),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
            )
    plt.annotate('Buying Signal', xy=(dt.date(2010,5,20), 0.89), xytext=(dt.date(2010,4,20), 0.82),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
            )    
    plt.tight_layout()
    plt.savefig('BollingerBand_Indicators.png')
    #plt.show()
    plt.close()

    plt.plot(SMAu, label='Price/SMA - over estimate')
    plt.plot(SMAl, label='Price/SMA - under estimate')
    plt.plot(SMA, label='SMA')
    plt.plot(stock_price,label='Stock Price')
    plt.axis([dt.date(2010,1,1), dt.date(2010,6,1), 0.8, 1.2])
    plt.xticks(rotation=30)
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.title('Price/SMA Indicator')
    #plt.legend(['Theoretically Optimal Strategy','Benchmark'])
    plt.legend(loc='upper left')
    plt.annotate('Selling Signal', xy=(dt.date(2010,4,15), 1.12), xytext=(dt.date(2010,4,1), 1.17),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
            )
    plt.annotate('Buying Signal', xy=(dt.date(2010,5,20), 0.89), xytext=(dt.date(2010,4,20), 0.82),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
            )    
    plt.tight_layout()
    plt.savefig('SMA_Indicators.png')
    #plt.show()
    plt.close()
    
    
    plt.plot(EMAu, label='Price/EMA - over estimate')
    plt.plot(EMAl, label='Price/EMA - under estimate')
    plt.plot(EMA_df, label='EMA')
    plt.plot(stock_price,label='Stock Price')
    plt.axis([dt.date(2010,1,1), dt.date(2010,6,1), 0.8, 1.2])
    plt.xticks(rotation=30)
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.title('Price/EMA Indicator')
    #plt.legend(['Theoretically Optimal Strategy','Benchmark'])
    plt.legend(loc='upper left')
    plt.annotate('Selling Signal', xy=(dt.date(2010,4,15), 1.12), xytext=(dt.date(2010,4,1), 1.17),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
            )
    plt.annotate('Buying Signal', xy=(dt.date(2010,5,20), 0.89), xytext=(dt.date(2010,4,20), 0.82),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
            )    
    plt.tight_layout()
    plt.savefig('EMA_Indicators.png')
    #plt.show()
    plt.close()


if __name__ == "__main__":
    test_code()