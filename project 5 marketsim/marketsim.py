"""MC2-P1: Market simulator.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Tucker Balch (replace with your name)
GT User ID: tb34 (replace with your User ID)
GT ID: 900897987 (replace with your GT ID)
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def author():
    return 'zzhang726' #Change this to your user ID 	

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    #zzhang726
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here


    orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True,  na_values=['nan']) 
    orders.sort_index(inplace=True)
    orders_rows = len(orders.index)
    
    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    start_date = orders.index[0]
    end_date = orders.index[-1]
    #stock_price = get_data(['IBM'], pd.date_range(start_date, end_date))
    #stock_price = stock_price[['IBM']]  # remove SPY
    #portvals = stock_price
    date_range = pd.date_range(start_date, end_date)
    stock_price_all = pd.DataFrame(index = date_range)
    stock_price_all['Cash'] = 1.0 # cash value
    portvals = pd.DataFrame(index = date_range) 
    portvals['Val'] = 0
    
    pf = pd.DataFrame(index = date_range)
    pf['Cash'] = start_val
    
    #Date,Symbol,Order,Shares  usecols=['Date', colname],

    for i in range(orders_rows): 
        date = orders.index[i]
        stock_symbol = orders['Symbol'].iloc[i]
        stock_order = orders['Order'].iloc[i]
        stock_shares = orders['Shares'].iloc[i]
        
        if not stock_price_all.columns.contains(stock_symbol):
            stock_price_single = get_data([stock_symbol], date_range)
            stock_price_single = stock_price_single[[stock_symbol]]  # remove SPY
            stock_price_all[stock_symbol] = stock_price_single
                
        #2011-01-10,AAPL,BUY,1500
        #2011-01-10,AAPL,SELL,1500
        if stock_order == 'SELL':
            stock_shares = 0 - stock_shares
            
        if not pf.columns.contains(stock_symbol):
            pf_tmp = pd.DataFrame(index = date_range)
            pf_tmp[stock_symbol] = 0
            pf[stock_symbol] = pf_tmp
        
        pf[stock_symbol][date:] =  pf[stock_symbol][date] + stock_shares 
        pf['Cash'][date:] = pf['Cash'][date:] - stock_shares*stock_price_all[stock_symbol][date] - abs(stock_shares)*impact*stock_price_all[stock_symbol][date] - commission
            
    
    #rv = pd.DataFrame(index=portvals.index, data=portvals.as_matrix())

    #return rv
    pv = portvals.values.flatten()
    for symbol in pf.columns:
        pv = pv + pf[symbol].values.flatten()*stock_price_all[symbol].values.flatten()
    portvals['Val'] = pv
    #portvals = portvals.dropna(subset=["Val"])
    portvals = portvals.dropna()
    return portvals

def get_stats(port_val):
    port_val.sort_index(inplace=True) 	
    cum_ret = port_val[port_val.index[-1]] / port_val[port_val.index[0]] -1 		  		 			 	 	 		 		 	  		   	  			  	
    daily_rets = (port_val / port_val.shift(1)) - 1 			  		 			 	 	 		 		 	  		   	  			  	
    daily_rets = daily_rets[1:] 			  		 			 	 	 		 		 	  		   	  			  	
    avg_daily_ret = daily_rets.mean() 			  		 			 	 	 		 		 	  		   	  			  	
    std_daily_ret = daily_rets.std() 			  		 			 	 	 		 		 	  		   	  			  	
    sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret 			  		 			 	 	 		 		 	  		   	  			  	
    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio 		

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-02.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        print "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    
    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    start_date = portvals.index[0]
    end_date = portvals.index[-1]
    
    
    stock_price_SPY = get_data(['SPY'], pd.date_range(start_date, end_date))
    stock_price_SPY = stock_price_SPY['SPY']
    
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_stats(portvals)#[0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = get_stats(stock_price_SPY)#[0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
