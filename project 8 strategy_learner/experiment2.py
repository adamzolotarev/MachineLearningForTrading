"""
Student Name: Zhiyong Zhang 			  		 			 	 	 		 		 	  		   	  			  	
GT User ID: zzhang726 			  		 			 	 	 		 		 	  		   	  			  	
GT ID: 903370141 			  		 			 	 	 		 		 	  		   	  			  	
""" 

# =============================================================================
# Experiment 2: Provide a hypothesis regarding how changing the value of impact
#  should affect in sample trading behavior and results (provide at least 
#  two metrics). Conduct an experiment with JPM on the in sample period to 
# test that hypothesis. Provide charts, graphs or tables that illustrate the 
# results of your experiment. The code that implements this experiment and 
# generates the relevant charts and data should be submitted as experiment2.py. 
# Be sure to add in an author method.
# =============================================================================

import datetime as dt 			  		 			 	 	 		 		 	  		   	  			  	
import pandas as pd 
import matplotlib.pyplot as plt
import marketsimcode as ms
import StrategyLearner as sl

def author():
    return 'zzhang726' #Change this to your user ID 	
def test_code_in_sample(learner, commission=0., impact=0.000): #commission=9.95, impact=0.005):  
    
    #symbols = ['SPY','JPM']
    #start_date = '2008-01-01'
    #end_date = '2009-12-31'
    #date_range = pd.date_range(start_date, end_date)

    
    print '\n\n\n in sample Stratedy Learner' + ' impact ' + str(impact) + ' :\n'
    orders = learner.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
    portvals = ms.compute_portvals_pd(orders, start_val = 100000, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), commission=commission, impact=impact)
    ms.print_stats(portvals)
    portvals_n = portvals/portvals.values[0]  
    
    if abs(impact - 0.005) < 0.0000001:
        print '\n\n\n in sample Benchmark:\n'
        date = dt.datetime(2008, 1, 2)
        Benchmark_orders = pd.DataFrame([[1000]],index = [date], columns=['JPM'])
        #date = dt.datetime(2009, 12, 31)
        #Benchmark_orders_last = pd.DataFrame([[-1000]],index = [date], columns=['JPM'])
        #Benchmark_orders = Benchmark_orders.append(Benchmark_orders_last)
        Benchmark_portvals = ms.compute_portvals_pd(Benchmark_orders, start_val = 100000, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), commission=commission, impact=impact)
        ms.print_stats(Benchmark_portvals)
        Benchmark_portvals_n = Benchmark_portvals/Benchmark_portvals.values[0]
        
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
    plt.plot(portvals_n['Val'], label='Stratedy Learner' + ' impact ' + str(impact))
    if abs(impact - 0.005) < 0.0000001:
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
        plt.savefig('Stratedy Learner in sample impact.png')
        #plt.show()
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
    #plt.show()
    plt.close()  
 		 			 	 	 		 		 	  		   	  			  	

def test_code(): 
    for i in range(6):
        impact = 0.001*i
        learner = sl.StrategyLearner(verbose = False, impact = impact) # constructor
        learner.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000) # training phase
        #df_trades = learner.testPolicy(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000) # testing phase
        test_code_in_sample(learner,impact = impact)  
        #test_code_out_sample(learner,impact = impact)    
    
    return 0
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    #print "One does not simply think up a strategy"
    test_code() 	