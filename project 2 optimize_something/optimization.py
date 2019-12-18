"""MC1-P2: Optimize a portfolio. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
 			  		 			 	 	 		 		 	  		   	  			  	
Student Name: Zhiyong Zhang 			  		 			 	 	 		 		 	  		   	  			  	
GT User ID: zzhang726 			  		 			 	 	 		 		 	  		   	  			  	
GT ID: 903370141 		  		 			 	 	 		 		 	  		   	  			  	
""" 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import matplotlib.pyplot as plt 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt 			  	
import scipy.optimize as sco	
import math 			 	 	 		 		 	  		   	  			  	
from util import get_data, plot_data 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
# This is the function that will be tested by the autograder 			  		 			 	 	 		 		 	  		   	  			  	
# The student must update this code to properly implement the functionality 			  		 			 	 	 		 		 	  		   	  			  	
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False): 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Read in adjusted closing prices for given symbols, date range 			  		 			 	 	 		 		 	  		   	  			  	
    dates = pd.date_range(sd, ed) 			  		 			 	 	 		 		 	  		   	  			  	
    prices_all = get_data(syms, dates)  # automatically adds SPY 			  		 			 	 	 		 		 	  		   	  			  	
    prices = prices_all[syms]  # only portfolio symbols 		
    #print prices.head()	  		 			 	 	 		 		 	  		   	  			  	
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later 	
    #print prices_SPY.head()		  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # find the allocations for the optimal portfolio 			  		 			 	 	 		 		 	  		   	  			  	
    # note that the values here ARE NOT meant to be correct for a test case
    n = len(syms)
    #print n 
    #allocs = np.asarray([0.2, 0.2, 0.3, 0.3]) # add code here to find the allocations 	
    allocs = np.ones((n,), dtype = 'f')*1.0 / n	
    #print allocs	 			 	 	 		 		 	  		   	  			  	
    #cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats 		
    normed = prices/prices.values[0]

    #print type(normed)
    #plt.plot(normed)
    #plt.show()
    #print normed.head()
    
    start_val = 1
    #scipy.optimize.minimize(fun, x0, args=(), method=None, jac=None, hess=None, 
    #hessp=None, bounds=None, constraints=(), tol=None, callback=None, options=None)
    bnds_list = list(range(n))
    #print bnds_list
    bnds_i = (0,1)
    for i in range(n):
        bnds_list[i] = bnds_i
    bnds = tuple(bnds_list)
    #print bnds
    cons=({'type':'eq','fun': lambda p: 1.0 - np.sum(p)})
    #print 'test before minimize'
    res = sco.minimize(fun, allocs, args=(normed), method = 'SLSQP', bounds =bnds, constraints=cons)
    #print 'after before minimize'
    allocs = res.x
    sr = - res.fun
    #print allocs.sum()
    
    
    #normed = normed.values
    alloced = normed * allocs
    start_val = 1.0
    pos_vals = alloced * start_val
    port_val = pos_vals.sum(axis=1)
    #print port_val.head()
    daily_rets = port_val[1:] /  port_val.values[:-1] - 1.0
    #print daily_rets.head()
    cr = port_val[-1]/port_val[0] - 1
    adr  = daily_rets.mean()
    sddr = daily_rets.std()
    k = 252 # 252 days per annual
    daily_rf = 0
    sr = math.sqrt(k) * (daily_rets.mean() - daily_rf) / daily_rets.std()
    
    '''
    allocs: A 1-d Numpy ndarray of allocations to the stocks. All the allocations must be between 0.0 and 1.0 and they must sum to 1.0.
    cr: Cumulative return
    adr: Average daily return
    sddr: Standard deviation of daily return
    sr: Sharpe ratio
    '''


 			  		 			 	 	 		 		 	  		   	  			  	
    # Get daily portfolio value 			  		 			 	 	 		 		 	  		   	  			  	
    prices_SPY = prices_SPY / prices_SPY[0] # add code here to compute daily portfolio values 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Compare daily portfolio value with SPY using a normalized plot 			  		 			 	 	 		 		 	  		   	  			  	
    if gen_plot: 			  		 			 	 	 		 		 	  		   	  			  	
        # add code to plot here 
        #normed_prices_all = prices_all/prices_all.values[0]
        #normed_prices_all.plot()			  		 			 	 	 		 		 	  		   	  			  	
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1) 			  		 			 	 	 		 		 	  		   	  			  	
        #plot_data(df_temp, title="Stock prices", xlabel="Date", ylabel="Price")
        ax = df_temp.plot(title="Stock prices", fontsize=12)  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_xlabel(xlabel="Date")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel(ylabel="Price")  	
        plt.savefig('plot.png')			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    return allocs, cr, adr, sddr, sr 			  		 			 	 	 		 		 	  		   	  			  	


def fun(allocs, normed):

    alloced = normed * allocs
    start_val = 1.0
    pos_vals = alloced * start_val
    port_val = pos_vals.sum(axis=1)
    daily_rets = port_val[1:] / port_val.values[:-1] - 1.0
    #daily_rets = daily_rets[1:]
    #cum_ret = (ort_val[-1]/port_val[0] - 1
    #avg_daily_ret = daily_rets.mean()
    #std_daily_ret = daily_rets.std()

    k = 252 # 252 days per annual
    daily_rf = 0
    SR = math.sqrt(k) * (daily_rets.mean() - daily_rf) / daily_rets.std()

    return  -1.0*SR

 			  		 			 	 	 		 		 	  		   	  			  	
def test_code(): 			  		 			 	 	 		 		 	  		   	  			  	
    # This function WILL NOT be called by the auto grader 			  		 			 	 	 		 		 	  		   	  			  	
    # Do not assume that any variables defined here are available to your function/code 			  		 			 	 	 		 		 	  		   	  			  	
    # It is only here to help you set up and test your code 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Define input parameters 			  		 			 	 	 		 		 	  		   	  			  	
    # Note that ALL of these values will be set to different values by 			  		 			 	 	 		 		 	  		   	  			  	
    # the autograder! 			  		 			 	 	 		 		 	  		   	  			  	


    #Start Date: 2008-06-01, End Date: 2009-06-01, Symbols: ['IBM', 'X', 'GLD', 'JPM']. 
		  		 			 	 	 		 		 	  		   	  			  	
    start_date = dt.datetime(2008,6,1) 			  		 			 	 	 		 		 	  		   	  			  	
    end_date = dt.datetime(2009,6,1) 			  		 			 	 	 		 		 	  		   	  			  	
    symbols = ['IBM', 'X', 'GLD', 'JPM'] 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Assess the portfolio 			  		 			 	 	 		 		 	  		   	  			  	
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True) 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Print statistics 			  		 			 	 	 		 		 	  		   	  			  	
    print "Start Date:", start_date 			  		 			 	 	 		 		 	  		   	  			  	
    print "End Date:", end_date 			  		 			 	 	 		 		 	  		   	  			  	
    print "Symbols:", symbols 			  		 			 	 	 		 		 	  		   	  			  	
    print "Allocations:", allocations 			  		 			 	 	 		 		 	  		   	  			  	
    print "Sharpe Ratio:", sr 			  		 			 	 	 		 		 	  		   	  			  	
    print "Volatility (stdev of daily returns):", sddr 			  		 			 	 	 		 		 	  		   	  			  	
    print "Average Daily Return:", adr 			  		 			 	 	 		 		 	  		   	  			  	
    print "Cumulative Return:", cr 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__ == "__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    # This code WILL NOT be called by the auto grader 			  		 			 	 	 		 		 	  		   	  			  	
    # Do not assume that it will be called 			  		 			 	 	 		 		 	  		   	  			  	
    test_code() 			  		 			 	 	 		 		 	  		   	  			  	
