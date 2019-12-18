#An improved version of your marketsim code that accepts a "trades" data frame (instead of a file). More info on the trades data frame below. It is OK not to submit this file if you have subsumed its functionality into one of your other required code files.

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data

def author():
    return 'zzhang726' #Change this to your user ID 	

def compute_portvals_pd(orders, start_val = 100000, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), commission=9.95, impact=0.005):
    #zzhang726
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    #orders_file = "./orders.csv"
    #orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True,  na_values=['nan']) 
    orders.sort_index(inplace=True)
    orders_rows = len(orders.index)
    
    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    start_date = sd #orders.index[0]
    end_date = ed #orders.index[-1]
    #stock_price = get_data(['IBM'], pd.date_range(start_date, end_date))
    #stock_price = stock_price[['IBM']]  # remove SPY
    #portvals = stock_price
    date_range = pd.date_range(start_date, end_date)
    stock_price_all = pd.DataFrame(index = date_range)
    stock_price_all['Cash'] = 1.0 # cash value
    stock_symbols = orders['Symbol'].unique().tolist()
    stock_price_all[stock_symbols] = get_data(stock_symbols, date_range)[stock_symbols]    

    portvals = pd.DataFrame(index = stock_price_all.index) 
    portvals['Val'] = 0

    pf = pd.DataFrame(np.NaN, index = stock_price_all.index, columns=stock_price_all.columns)

    #pf.iloc[[0]] = 0
    pf.values[0,:] = 0
    #pf.iloc[[0]]['Cash']= start_val
    pf.values[0,0] = start_val
    
    holding={'Cash':start_val}
    
    #Date,Symbol,Order,Shares  usecols=['Date', colname],
    #t0 = time.time()
    for i in range(orders_rows): 
        date = orders.index[i]
        stock_symbol = orders['Symbol'].iloc[i]
        #stock_order = orders['Order'].iloc[i]
        stock_shares = orders['Shares'].iloc[i]
        
        if stock_shares == 0:
            continue
        
        '''
        if not stock_price_all.columns.contains(stock_symbol):
            stock_price = get_data([stock_symbol], date_range)
            stock_price_all[stock_symbol] = stock_price[[stock_symbol]]  # remove SPY
                           
        #2011-01-10,AAPL,BUY,1500
        #2011-01-10,AAPL,SELL,1500
        #if stock_order == 'SELL':
        #    stock_shares = 0 - stock_shares
            
        if not pf.columns.contains(stock_symbol):
            #pf_tmp = pd.DataFrame(index = date_range)
            #pf_tmp[stock_symbol] = 0
            pf[stock_symbol] = 0
        '''
        s0 = holding.get(stock_symbol, 0)        
        s1 = s0 + stock_shares
        holding[stock_symbol] = s1
        pf[stock_symbol][date] =  s1
        
        c1 = 0. - stock_shares*stock_price_all[stock_symbol][date] - abs(stock_shares)*impact*stock_price_all[stock_symbol][date] - commission
        c0 = holding.get('Cash', 0)
        c2 = c0 + c1
        holding['Cash'] = c2
        pf['Cash'][date] = c2
    pf = pf.fillna(method='ffill')

    #t1 = time.time()
    #print t1-t0    
    #rv = pd.DataFrame(index=portvals.index, data=portvals.as_matrix())

    #return rv
    pv = portvals.values.flatten()
    for symbol in pf.columns:
        pv = pv + pf[symbol].values.flatten()*stock_price_all[symbol].values.flatten()
    portvals['Val'] = pv
        
    #portvals = portvals.dropna(subset=["Val"])
    portvals = portvals.dropna()
    #t2 = time.time()
    #print t2-t1  
    return portvals

def get_stats(port_val):
    port_val.sort_index(inplace=True) 	
    cum_ret = port_val[port_val.index[-1]] / port_val[port_val.index[0]] - 1		  		 			 	 	 		 		 	  		   	  			  	
    daily_rets = (port_val / port_val.shift(1)) - 1 			  		 			 	 	 		 		 	  		   	  			  	
    daily_rets = daily_rets[1:] 			  		 			 	 	 		 		 	  		   	  			  	
    avg_daily_ret = daily_rets.mean() 			  		 			 	 	 		 		 	  		   	  			  	
    std_daily_ret = daily_rets.std() 			  		 			 	 	 		 		 	  		   	  			  	
    sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret 			  		 			 	 	 		 		 	  		   	  			  	
    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio 	

def print_stats(portvals):	
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
    #print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    #print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    #print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    #print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

def assemble_order(orders):
    
    #keep do nothing
    #orders = orders[(orders != 0).any(axis=1)]
               
    # current holding position    
    SharesHold = {}
    orders_pd = pd.DataFrame(columns=['Symbol','Order','Shares','SignedShares'])
    for date in orders.index:
        for sym in orders.columns:
            holding = SharesHold.get(sym,0)
            if date != orders.index[-1]:
                if (orders.loc[date,sym] > 0) & (holding < 1000):
                    if holding == -1000:
                        amount = 2000
                    else: 
                        amount = 1000
                    SharesHold[sym] = holding + amount
                   #df2 = pd.DataFrame([[sym, 'BUY', amount, amount]],index = [date.date()], columns=['Symbol','Order','Shares','SignedShares'])
                    df2 = pd.DataFrame([[sym, 'BUY', amount, amount]],index = [date], columns=['Symbol','Order','Shares','SignedShares'])
                    orders_pd = orders_pd.append(df2)  
                elif (orders.loc[date,sym] < 0) & (holding > -1000) :
                    if holding == 1000:
                        amount = -2000
                    else: 
                        amount = -1000
                    SharesHold[sym] = holding + amount
                    df2 = pd.DataFrame([[sym, 'SELL', 0-amount, amount]],index = [date], columns=['Symbol','Order','Shares','SignedShares'])
                    orders_pd = orders_pd.append(df2) 
                else:# ==0
                    amount = 0
                    df2 = pd.DataFrame([[sym, 'BUY', amount, amount]],index = [date], columns=['Symbol','Order','Shares','SignedShares'])
                    orders_pd = orders_pd.append(df2)
            else: #last day
                if (holding < 0):
                    
                    amount = abs(holding)
                    
                    SharesHold[sym] = holding + amount
                    df2 = pd.DataFrame([[sym, 'BUY', amount, amount]],index = [date], columns=['Symbol','Order','Shares','SignedShares'])
                    orders_pd = orders_pd.append(df2)  
                elif (holding > 0):
                    amount = 0 - abs(holding)
                    SharesHold[sym] = holding + amount
                    df2 = pd.DataFrame([[sym, 'SELL', 0-amount, amount]],index = [date], columns=['Symbol','Order','Shares','SignedShares'])
                    orders_pd = orders_pd.append(df2) 
                else:# ==0
                    amount = 0
                    df2 = pd.DataFrame([[sym, 'BUY', amount, amount]],index = [date], columns=['Symbol','Order','Shares','SignedShares'])
                    orders_pd = orders_pd.append(df2)
                
                
    #last day, clear stocks           
                                       
                
    orders_pd[['Symbol','Order','Shares']].to_csv('./orders.csv',index_label='Date')
    del orders_pd['Order']
    del orders_pd['Shares']
    return orders_pd.rename(columns={'SignedShares':'Shares'})

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
        orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True,  na_values=['nan'])
        orders['Shares'] = orders['Shares'].where(orders['Order'] != 'SELL',0-orders['Shares'])
        del orders['Order']
        orders.sort_index(inplace=True)
        sd = orders.index[0]
        ed = orders.index[-1]        
        return compute_portvals_pd(orders, start_val = start_val, sd=sd, ed=ed, commission=commission, impact=impact)
   
    
def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    #of = "./orders/orders-02.csv"

    # Process orders
    #of = "./orders/orders-02.csv"
    orders_file = "./orders.csv"

    portvals = compute_portvals(orders_file, start_val = 100000, commission=9.95, impact=0.005)
    #portvals = compute_portvals(orders_file, start_val = 100000, commission=0, impact=0)
    print_stats(portvals)
    print portvals


#if __name__ == "__main__":
    #test_code()
    
