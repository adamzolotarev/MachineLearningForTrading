
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data, plot_data
from indicators import momentum, SMA, BollingerBands, RSI
from marketsimcode import compute_portvals_pd, get_stats, print_stats, assemble_order

def author():
    return 'zzhang726' #Change this to your user ID 	

def testPolicy(symbol = "JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000):
    
    symbols = [symbol]
    date_range = pd.date_range(sd, ed)

    #symbols = ['SPY','AAPL','GOOG','XOM']
    #start_date = '2011-01-01'
    #end_date = '2012-02-01'
    #date_range = pd.date_range(start_date, end_date)
    
    stock_price = get_data(symbols, date_range)
    stock_price = stock_price[symbols]
    window = 10  #10 for in sample, 13 14,18,10 for out sample
    bbu,bbl,SMA,SMAi,bbi = BollingerBands(stock_price,window = window)
    
    orders = stock_price.copy()
    orders = orders*0.
    
    '''    
    RSIi = RSI(stock_price, window = window)
    momentum_window = 5
    momentum_df = momentum(stock_price, window = momentum_window)

    RSIi_SPY = RSIi.copy()
    RSIi_SPY = RSIi_SPY.where(RSIi_SPY == np.NaN, 1.)    
    RSIi_SPY.values[:,:] = RSIi.iloc[:,0:1]
    
    x10 = SMAi < 0.95
    x20 = bbi < -1
    x30 = RSIi < 30 
    x40 = RSIi_SPY > 30
    
    x11 = SMAi > 1.05
    x21 = bbi > 1
    x31 = RSIi > 70
    x41 = RSIi_SPY < 70
    
    #x50 = x10 & x20 & x30 & x40
    #x51 = x11 & x21 & x31 & x41
    '''
    #BollingerBand
    #buying signal
    orders[bbi < -1] = 1
    
    #selling signal
    orders[bbi > 1] = -1
    
    '''
    SMAi_diff = SMAi.diff()     
    #move up momentum
    orders[((SMAi-1)*(SMAi.shift(1)-1) < 0) & (SMAi_diff > 0) & (momentum_df > 0.05)] = 1    
    #move down momentum
    orders[((SMAi-1)*(SMAi.shift(1)-1) < 0) & (SMAi_diff < 0) & (momentum_df < -0.05)] = -1
    '''        
    return assemble_order(orders)
    
def test_code_in_sample():  
    
    #symbols = ['SPY','JPM']
    #start_date = '2008-01-01'
    #end_date = '2009-12-31'
    #date_range = pd.date_range(start_date, end_date)
    print '\n\n\nBenchmark:\n'
    date = dt.datetime(2008, 1, 2)
    Benchmark_orders = pd.DataFrame([['JPM', 1000]],index = [date.date()], columns=['Symbol','Shares'])
    Benchmark_portvals = compute_portvals_pd(Benchmark_orders, start_val = 100000, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), commission=9.95, impact=0.005)
    print_stats(Benchmark_portvals)
    Benchmark_portvals_n = Benchmark_portvals/Benchmark_portvals.values[0]
    
    print '\n\n\nManual Stratedy:\n'
    orders = testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
    portvals = compute_portvals_pd(orders, start_val = 100000, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), commission=9.95, impact=0.005)
    print_stats(portvals)
    portvals_n = portvals/portvals.values[0]    
    
    trade_buy = orders[orders['Shares']>0]
    trade_sell = orders[orders['Shares']<0]
    #print trade_buy
    #print trade_sell
    date_buy = trade_buy.index.tolist()
    date_sell = trade_sell.index.tolist()
    
    for xc in date_buy:
        plt.axvline(x=xc,c='b')
        
    for xc in date_sell:
        plt.axvline(x=xc,c='k')    
    
    plt.plot(portvals_n['Val'],'r', label='Manual Rule-based Stratedy')
    plt.plot(Benchmark_portvals_n['Val'],'g', label='Benchmark')
    #plt.axis([0, 300, -256, 100])
    plt.xticks(rotation=30)
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title('Manual Rule-based Stratedy')
    plt.annotate('Blue  lines - LONG entry points', xy=(dt.date(2008,1,1), 1.2), xytext=(dt.date(2007,12,02), 1.47),
        #arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
        ) 
    plt.annotate('Black lines - SHORT entry points', xy=(dt.date(2008,1,1), 1.15), xytext=(dt.date(2007,12,02), 1.4),
    #arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
    ) 
    #plt.legend(['Theoretically Optimal Strategy','Benchmark'])
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig('Manual Rule-based Stratedy.png')
    #plt.show()
    plt.close()
def test_code_out_sample():  
    
    #symbols = ['SPY','JPM']
    #start_date = '2008-01-01'
    #end_date = '2009-12-31'
    #date_range = pd.date_range(start_date, end_date)
    print '\n\n\nBenchmark:\n'
    date = dt.datetime(2010, 1, 4)
    Benchmark_orders = pd.DataFrame([['JPM', 1000]],index = [date.date()], columns=['Symbol','Shares'])
    Benchmark_portvals = compute_portvals_pd(Benchmark_orders, start_val = 100000, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), commission=9.95, impact=0.005)
    print_stats(Benchmark_portvals)
    Benchmark_portvals_n = Benchmark_portvals/Benchmark_portvals.values[0]
    
    print '\n\n\nManual Stratedy:\n'
    orders = testPolicy(symbol = "JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000)
    portvals = compute_portvals_pd(orders, start_val = 100000, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), commission=9.95, impact=0.005)
    print_stats(portvals)
    portvals_n = portvals/portvals.values[0]    
    
    trade_buy = orders[orders['Shares']>0]
    trade_sell = orders[orders['Shares']<0]
    #print trade_buy
    #print trade_sell
    date_buy = trade_buy.index.tolist()
    date_sell = trade_sell.index.tolist()
    
    for xc in date_buy:
        plt.axvline(x=xc,c='b')
        
    for xc in date_sell:
        plt.axvline(x=xc,c='k')    
    
    plt.plot(portvals_n['Val'],'r', label='Manual Rule-based Stratedy')
    plt.plot(Benchmark_portvals_n['Val'],'g', label='Benchmark')
    #plt.axis([0, 300, -256, 100])
    plt.xticks(rotation=30)
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title('Manual Rule-based Stratedy')
    plt.annotate('Blue lines - LONG entry points', xy=(dt.date(2010,1,1), 1.2), xytext=(dt.date(2010,1,01), 1.2),
        #arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
        ) 
    plt.annotate('Black lines - SHORT entry points', xy=(dt.date(2010,1,1), 1.15), xytext=(dt.date(2010,1,01), 1.16),
    #arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
    ) 
    #plt.legend(['Theoretically Optimal Strategy','Benchmark'])
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig('out sample Manual Rule-based Stratedy.png')
    #plt.show()
    plt.close()    

def test_code_indicator():
    stock_symbol = 'JPM' #'APPL'
    start_date = '2008-01-01'
    #end_date = '2009-12-31'
    end_date = '2009-12-31'
    date_range = pd.date_range(start_date, end_date)
    stock_price = get_data([stock_symbol], date_range)
    stock_price = stock_price[stock_symbol]
    
    stock_price = stock_price / stock_price.values[0]    
    window = 10    
    bbu,bbl,SMA,SMAi,bbi = BollingerBands(stock_price,window = window)
    
    SMAu = SMA*1.05
    SMAl = SMA*0.95    
    #RSI_i = RSI(stock_price, window = window)
    #momentum_df = momentum(stock_price, window = window)
    
    plt.plot(bbu, label='upper BollingerBand')
    plt.plot(bbl, label='lower BollingerBand')
    plt.plot(SMA, label='SMA')
    plt.plot(stock_price, label='Stock Price')
    #plt.axis([dt.date(2008,1,1), dt.date(2009,12,31), 0.8, 1.2])
    #plt.axis([0, 300, -256, 100])
    plt.xticks(rotation=30)
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.title('BollingerBand Indicator')
    #plt.legend(['Theoretically Optimal Strategy','Benchmark'])
    plt.legend(loc='lower left')
    
    #plt.annotate('Selling Signal', xy=(dt.date(2010,4,15), 1.12), xytext=(dt.date(2010,4,1), 1.17),
    #        arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
    #        )
    #plt.annotate('Buying Signal', xy=(dt.date(2010,5,20), 0.89), xytext=(dt.date(2010,4,20), 0.82),
    #        arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
    #        )
    #    
    plt.tight_layout()
    plt.savefig('Manual_BollingerBand_Indicators.png')
    #plt.show()
    plt.close()
    
    plt.plot(SMAu, label='Price/SMA - over estimate')
    plt.plot(SMAl, label='Price/SMA - under estimate')
    plt.plot(SMA, label='SMA')
    plt.plot(stock_price,label='Stock Price')
    #plt.axis([dt.date(2008,1,1), dt.date(2009,12,31), 0.8, 1.2])
    plt.xticks(rotation=30)
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.title('Price/SMA Indicator')
    #plt.legend(['Theoretically Optimal Strategy','Benchmark'])
    plt.legend(loc='lower left')
    #
    #plt.annotate('Selling Signal', xy=(dt.date(2010,4,15), 1.12), xytext=(dt.date(2010,4,1), 1.17),
    #        arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
    #        )
    #plt.annotate('Buying Signal', xy=(dt.date(2010,5,20), 0.89), xytext=(dt.date(2010,4,20), 0.82),
    #        arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
    #        )
    #    
    plt.tight_layout()
    plt.savefig('Manual_SMA_Indicators.png')
    #plt.show()
    plt.close()
    
if __name__ == "__main__":
    test_code_in_sample()    
    test_code_out_sample()
    #test_code_indicator()
    