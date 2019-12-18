""" 			  		 			 	 	 		 		 	  		   	  			  	
Template for implementing StrategyLearner  (c) 2016 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
 					  		 			 	 	 		 		 	  		   	  			  	
#All submitted code must include comments with your name and User ID. 
  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt 			  		 			 	 	 		 		 	  		   	  			  	
import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import util as ut
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import random as rand 			  		 			 	 	 		 		 	  		   	  			  	
import time 			  		 			 	 	 		 		 	  		   	  			  	
import math 			  		 			 	 	 		 		 	  		   	  			  	
import QLearner as ql
import matplotlib.pyplot as plt
from indicators import BollingerBands
from util import get_data, plot_data
import marketsimcode as ms

 	 			  		 			 	 	 		 		 	  		   	  			  	
class StrategyLearner(object):

			  		 			 	 	 		 		 	  		   	  			  	
    def author(self):
        return 'zzhang726' #Change this to your user ID
  	 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # constructor 			  		 			 	 	 		 		 	  		   	  			  	
    def __init__(self, verbose = False, impact=0.0): 			  		 			 	 	 		 		 	  		   	  			  	
        self.verbose = verbose 			  		 			 	 	 		 		 	  		   	  			  	
        self.impact = impact


    # convert the location to a single integer 			  		 			 	 	 		 		 	  		   	  			  	
    def discretize(self, indicator, holding): #holding = -1,0,1
        n = 0
        if indicator >= self.indicator_threshold[-1]:
            n=self.N_indicator-1
        else:
            for i in range(self.N_indicator-1):
                if indicator < self.indicator_threshold[i]:
                    n = i
                    break
			  		 			 	 	 		 		 	  		   	  			  	
        return n*self.N_position + (holding+1) 	
    
    def init_discretize(self, indicators): 
        indicators_c = indicators[:] # copy
        indicators_c.sort()
        self.indicator_threshold = [indicators_c[len(indicators_c)/self.N_indicator*(i+1)] for i in range(self.N_indicator-1)]
    #        self.N_indicator = 10
    #self.N_position = 3
 			  		 			 	 	 		 		 	  		   	  			  	
    # this method should create a QLearner, and train it for trading 			  		 			 	 	 		 		 	  		   	  			  	
    def addEvidence(self, symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 
			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        # add your code to do learning here 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
        # example usage of the old backward compatible util function 			  		 			 	 	 		 		 	  		   	  			  	
        syms=[symbol] 			  		 			 	 	 		 		 	  		   	  			  	
        dates = pd.date_range(sd, ed) 			  		 			 	 	 		 		 	  		   	  			  	
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY 			  		 			 	 	 		 		 	  		   	  			  	
        prices = prices_all[syms]  # only portfolio symbols 			  		 			 	 	 		 		 	  		   	  			  	
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later 			  		 			 	 	 		 		 	  		   	  			  	
        if self.verbose: print prices 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
        # example use with new colname 			  		 			 	 	 		 		 	  		   	  			  	
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY 			  		 			 	 	 		 		 	  		   	  			  	
        volume = volume_all[syms]  # only portfolio symbols 			  		 			 	 	 		 		 	  		   	  			  	
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later 			  		 			 	 	 		 		 	  		   	  			  	
        if self.verbose: print volume 	

        ########
        """        
	
    
        stock_symbol = symbol
        date_range = pd.date_range(sd, ed)
        stock_price = get_data([stock_symbol], date_range)
        stock_price = stock_price[stock_symbol]
        
        #stock_price = stock_price / stock_price.values[0]    
        window = 10
        bbu,bbl,SMA,SMAi,bbi = BollingerBands(stock_price,window = window)
        bbi.dropna(inplace=True)
        
        """      
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
        plt.show()
        plt.close()
        """        
        
        self.N_indicator = 10
        self.N_position = 3
                
        #bbi.columns = ['bbi']
        df = pd.DataFrame()
        df['bbi'] = bbi
        df['price'] = stock_price
        #df.dropna(inplace=True)
        
        indicators = df['bbi'].values.tolist()
        prices     = df['price'].values.tolist()
        
        self.init_discretize(indicators) 
        num_states = self.N_indicator * self.N_position
        num_actions = 3
			  		 			 	 	 		 		 	  		   	  			  	
        self.learner = ql.QLearner(num_states=num_states,\
            num_actions = num_actions, \
            alpha = 0.2, \
            gamma = 0.9, \
            rar = 0.99, \
            radr = 0.999, \
            dyna = 0, \
            verbose=False) #initialize the learner 	 	

        # each epoch involves one trip to the goal 	
        epochs = 500		  		 			 	 	 		 		 	  		   	  			  	
        #startpos = getrobotpos(map) #find where the robot starts 			  		 			 	 	 		 		 	  		   	  			  	
        #goalpos = getgoalpos(map) #find where the goal is 			  		 			 	 	 		 		 	  		   	  			  	
        scores = np.zeros((epochs,1)) 		
        rar_list = np.zeros((epochs,1))	  		 			 	 	 		 		 	  		   	  			  	
        for epoch in range(1,epochs+1): 			  		 			 	 	 		 		 	  		   	  			  	
            total_reward = 0 			  		 			 	 	 		 		 	  		   	  			  	
            #data = map.copy() 			  		 			 	 	 		 		 	  		   	  			  	
            #robopos = startpos
            holding = 0 			  		 			 	 	 		 		 	  		   	  			  	
            state = self.discretize(indicators[0],holding) #convert the location to a state 			  		 			 	 	 		 		 	  		   	  			  	
            action = self.learner.querysetstate(state) - 1 #set the state and get first action 			  		 			 	 	 		 		 	  		   	  			  	
            n = 0 			  		 			 	 	 		 		 	  		   	  			  	
            while (n < len(prices)-1) & (n<10000): 
                
                indicator_prime = indicators[n+1]
                delt_p = prices[n+1]-prices[n]
                
                # consider repeat three times for action
                if action == 0:
                    r = delt_p*holding
                elif action == -1 :
                    if holding < 0:
                        r = delt_p*holding
                    elif holding > 0:
                        r = delt_p*(-1) - self.impact*prices[n]                        
                    else:# holding == 0:  
                        r = 0.5*(delt_p*(-1) - self.impact*prices[n])                        
                    holding = -1
                else:# action == 1 :
                    if holding > 0:
                        r = delt_p*holding
                    elif holding < 0:
                        r = delt_p*(1) - self.impact*prices[n]
                    else:# holding == 0:
                        r = 0.5*(delt_p*(1) - self.impact*prices[n])	
                    holding = 1                        		  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
                state = self.discretize(indicator_prime, holding) 	
		  		 			 	 	 		 		 	  		   	  			  	
                action = self.learner.query(state,r) - 1 	
                
                if (holding > 0) & (action > 0):
                    action = 0
                    self.learner.a = 0 + 1
                if (holding < 0) & (action < 0):
                    action = 0
                    self.learner.a = 0 + 1                 	  		 			 	 	 		 		 	  		   	  			  	
     			  		 			 		 		 		 	  		   	  			  	
                stepreward = r 			  		 			 	 	 		 		 	  		   	  			  	
                total_reward += stepreward 			  		 			 	 	 		 		 	  		   	  			  	
                n = n + 1 			  		 			 	 	 		 		 	  		   	  			  	
            if n == 100000: 			  		 			 	 	 		 		 	  		   	  			  	
                print "timeout" 			  		 			 	 	 		 		 	  		   	  			  	
            #if verbose: printmap(data) 			  		 			 	 	 		 		 	  		   	  			  	
            if self.verbose: print epoch, total_reward 			  		 			 	 	 		 		 	  		   	  			  	
            scores[epoch-1,0] = total_reward
            rar_list[epoch-1,0] = self.learner.rar 
            if self.verbose: 
                print 'learner.rar'
                print(self.learner.rar)
                print 'learner.Q'
                print(self.learner.Q) 
            if (epoch >= 20) & (abs(total_reward-scores[epoch-2,0]) / total_reward < 0.001): #converge
                break
    	if self.verbose:
            print scores.flatten()
            print rar_list.flatten()
        return 0
		  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # this method should use the existing policy and test it against new data 			  		 			 	 	 		 		 	  		   	  			  	
    def testPolicy(self, symbol = "JPM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):
        
        #symbols = [symbol]
        date_range = pd.date_range(sd, ed)
    
        #symbols = ['SPY','AAPL','GOOG','XOM']
        #start_date = '2011-01-01'
        #end_date = '2012-02-01'
        #date_range = pd.date_range(start_date, end_date)
        
        stock_price = get_data([symbol], date_range)
        stock_price = stock_price[[symbol]]
        window = 10  #10 for in sample, 13 14,18,10 for out sample
        bbu,bbl,SMA,SMAi,bbi = BollingerBands(stock_price,window = window)
        
        orders = stock_price.copy()
        orders = orders*0.
        
        #BollingerBand
        #buying signal 
        
        bbi = bbi.dropna()
        holding = 0
        
        for date in bbi.index:
            state = self.discretize(bbi[symbol][date], holding)
            action = self.learner.querysetstate(state) - 1
            orders[symbol][date] = action
            
            if action == -1:                      
                holding = -1
            elif action == 1:
                holding = 1
            #else 
            #    holding = holding     
        #ordersDF = orders.to_frame()    
        trades = ms.assemble_order(orders)
        del trades['Symbol']
        trades = trades.rename(columns={'Shares':symbol})
        
        return trades    
        ''' 			 	 	 		 		 	  		   	  			  	
        # here we build a fake set of trades 			  		 			 	 	 		 		 	  		   	  			  	
        # your code should return the same sort of data 			  		 			 	 	 		 		 	  		   	  			  	
        dates = pd.date_range(sd, ed) 			  		 			 	 	 		 		 	  		   	  			  	
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY   		 			 	 	 		 		 	  		   	  			  	
        trades = prices_all[[symbol,]]  # only portfolio symbols   		 			 	 	 		 		 	  		   	  			  	
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later		  		 			 	 	 		 		 	  		   	  			  	
        trades.values[:,:] = 0 # set them all to nothing 			  		 			 	 	 		 		 	  		   	  			  	
        trades.values[0,:] = 1000 # add a BUY at the start 			  		 			 	 	 		 		 	  		   	  			  	
        trades.values[40,:] = -1000 # add a SELL 			  		 			 	 	 		 		 	  		   	  			  	
        trades.values[41,:] = 1000 # add a BUY 			  		 			 	 	 		 		 	  		   	  			  	
        trades.values[60,:] = -2000 # go short from long 			  		 			 	 	 		 		 	  		   	  			  	
        trades.values[61,:] = 2000 # go long from short 			  		 			 	 	 		 		 	  		   	  			  	
        trades.values[-1,:] = -1000 #exit on the last day 			  		 			 	 	 		 		 	  		   	  			  	
        if self.verbose: print type(trades) # it better be a DataFrame! 			  		 			 	 	 		 		 	  		   	  			  	
        if self.verbose: print trades 			  		 			 	 	 		 		 	  		   	  			  	
        #if self.verbose: print prices_all 			  		 			 	 	 		 		 	  		   	  			  	
        return trades 	
        '''
def test_code_in_sample(learner, commission=0., impact=0.000): #commission=9.95, impact=0.005):  
    
    #symbols = ['SPY','JPM']
    #start_date = '2008-01-01'
    #end_date = '2009-12-31'
    #date_range = pd.date_range(start_date, end_date)
    print '\n\n\n in sample Benchmark:\n'
    date = dt.datetime(2008, 1, 2)
    Benchmark_orders = pd.DataFrame([[1000]],index = [date], columns=['JPM'])
    #date = dt.datetime(2009, 12, 31)
    #Benchmark_orders_last = pd.DataFrame([[-1000]],index = [date], columns=['JPM'])
    #Benchmark_orders = Benchmark_orders.append(Benchmark_orders_last)
    Benchmark_portvals = ms.compute_portvals_pd(Benchmark_orders, start_val = 100000, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), commission=commission, impact=impact)
    ms.print_stats(Benchmark_portvals)
    Benchmark_portvals_n = Benchmark_portvals/Benchmark_portvals.values[0]
    
    print '\n\n\n in sample Stratedy Learner:\n'
    orders = learner.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
    portvals = ms.compute_portvals_pd(orders, start_val = 100000, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), commission=commission, impact=impact)
    ms.print_stats(portvals)
    portvals_n = portvals/portvals.values[0]    
    '''
    trade_buy = orders[orders[orders.columns[0]]>0]
    trade_sell = orders[orders[orders.columns[0]]<0]
    #print trade_buy
    #print trade_sell
    
    date_buy = trade_buy.index.tolist()
    date_sell = trade_sell.index.tolist()
    
    for xc in date_buy:
        plt.axvline(x=xc,c='b')
        
    for xc in date_sell:
        plt.axvline(x=xc,c='k')    
    '''
    plt.plot(portvals_n['Val'],'r', label='Stratedy Learner')
    plt.plot(Benchmark_portvals_n['Val'],'g', label='Benchmark')
    #plt.axis([0, 300, -256, 100])
    plt.xticks(rotation=30)
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title('in sample Stratedy Learner')
    
    #plt.annotate('Blue  lines - LONG entry points', xy=(dt.date(2008,1,1), 1.2), xytext=(dt.date(2007,12,02), 1.47),
    #    #arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
    #    ) 
    #plt.annotate('Black lines - SHORT entry points', xy=(dt.date(2008,1,1), 1.15), xytext=(dt.date(2007,12,02), 1.4),
    ##arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
    #) 
    
    #plt.legend(['Theoretically Optimal Strategy','Benchmark'])
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig('Stratedy Learner in sample.png')
    plt.show()
    plt.close()
def test_code_out_sample(learner, commission=0., impact=0.000): #commission=9.95, impact=0.005):  
    
    #symbols = ['SPY','JPM']
    #start_date = '2008-01-01'
    #end_date = '2009-12-31'
    #date_range = pd.date_range(start_date, end_date)
    print '\n\n\n out sample Benchmark:\n'
    date = dt.datetime(2010, 1, 4)
    Benchmark_orders = pd.DataFrame([[1000]],index = [date], columns=['JPM'])
    #date = dt.datetime(2011, 12, 30)
    #Benchmark_orders_last = pd.DataFrame([[-1000]],index = [date], columns=['JPM'])
    #Benchmark_orders = Benchmark_orders.append(Benchmark_orders_last)    
    Benchmark_portvals = ms.compute_portvals_pd(Benchmark_orders, start_val = 100000, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), commission=commission, impact=impact)
    ms.print_stats(Benchmark_portvals)
    Benchmark_portvals_n = Benchmark_portvals/Benchmark_portvals.values[0]
    
    print '\n\n\n out sample Stratedy Learner:\n'
    orders = learner.testPolicy(symbol = "JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000)
    portvals = ms.compute_portvals_pd(orders, start_val = 100000, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), commission=commission, impact=impact)
    ms.print_stats(portvals)
    portvals_n = portvals/portvals.values[0]    
    '''
    trade_buy = orders[orders[orders.columns[0]]>0]
    trade_sell = orders[orders[orders.columns[0]]<0]
    #print trade_buy
    #print trade_sell
    date_buy = trade_buy.index.tolist()
    date_sell = trade_sell.index.tolist()
    
    for xc in date_buy:
        plt.axvline(x=xc,c='b')
        
    for xc in date_sell:
        plt.axvline(x=xc,c='k')    
    '''
    plt.plot(portvals_n['Val'],'r', label='Stratedy Learner')
    plt.plot(Benchmark_portvals_n['Val'],'g', label='Benchmark')
    #plt.axis([0, 300, -256, 100])
    plt.xticks(rotation=30)
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title('out sample Stratedy Learner')
    
    #plt.annotate('Blue lines - LONG entry points', xy=(dt.date(2010,1,1), 1.2), xytext=(dt.date(2010,1,01), 1.2),
    #    #arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
    #    ) 
    #plt.annotate('Black lines - SHORT entry points', xy=(dt.date(2010,1,1), 1.15), xytext=(dt.date(2010,1,01), 1.16),
    ##arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
    #) 
    
    #plt.legend(['Theoretically Optimal Strategy','Benchmark'])
    plt.legend(loc='lower left')
    plt.tight_layout()
    plt.savefig('Stratedy Learner out sample.png')
    plt.show()
    plt.close()  
 		 			 	 	 		 		 	  		   	  			  	

def test_code():   
    impact = 0.000
    learner = StrategyLearner(verbose = False, impact = impact) # constructor
    learner.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000) # training phase
    #df_trades = learner.testPolicy(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000) # testing phase
    test_code_in_sample(learner,impact = impact)  
    test_code_out_sample(learner,impact = impact)
    
    return 0
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    print "One does not simply think up a strategy"
    #test_code() 			  		 			 	 	 		 		 	  		   	  			  	
