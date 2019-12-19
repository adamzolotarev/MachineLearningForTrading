
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data, plot_data
from indicators import momentum, SMA, BollingerBands, RSI
from marketsimcode import compute_portvals_pd, get_stats, print_stats, assemble_order

def author():
    return 'zzhang726' #Change this to your user ID 	

def testPolicy(symbol = "AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000):

    symbols = [symbol]
    date_range = pd.date_range(sd, ed)
    stock_price = get_data(symbols, date_range)
    del stock_price['SPY']
    
    orders = stock_price.copy()
    orders = orders*0.
    
    stock_price_diff_f = stock_price.diff(-1)
     
    #move up
    orders[stock_price_diff_f<0] = 1
    
    #move down
    orders[stock_price_diff_f>0] = -1
    
    return assemble_order(orders)
    
def test_code():  
    #symbols = ['SPY','JPM']
    #start_date = '2008-01-01'
    #end_date = '2009-12-31'
    #date_range = pd.date_range(start_date, end_date)

    print '\n\n\nBenchmark:\n'
    date = dt.datetime(2008, 1, 2)
    Benchmark_orders = pd.DataFrame([['JPM', 1000]],index = [date.date()], columns=['Symbol','Shares'])
    Benchmark_portvals = compute_portvals_pd(Benchmark_orders, start_val = 100000, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), commission=0, impact=0)
    print_stats(Benchmark_portvals)
    Benchmark_portvals_n = Benchmark_portvals/Benchmark_portvals.values[0]
    
    print '\n\n\nTheoretically Optimal Strategy:\n'
    orders = testPolicy(symbol = 'JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
    portvals = compute_portvals_pd(orders, start_val = 100000, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), commission=0, impact=0)
    print_stats(portvals)
    portvals_n = portvals/portvals.values[0]
        
    plt.plot(portvals_n['Val'],'r', label='Theoretically Optimal Strategy')
    plt.plot(Benchmark_portvals_n['Val'],'g', label='Benchmark')
    #plt.axis([0, 300, -256, 100])
    plt.xticks(rotation=30)
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title('Theoretically Optimal Strategy')
    #plt.legend(['Theoretically Optimal Strategy','Benchmark'])
    plt.legend()
    plt.tight_layout()
    plt.savefig('Theoretically_Optimal_Strategy.png')
    #plt.show()
    plt.close()

    
if __name__ == "__main__":
    test_code()    
    