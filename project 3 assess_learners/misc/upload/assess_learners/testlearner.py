""" 			  		 			 	 	 		 		 	  		   	  			  	
Test a learner.  (c) 2015 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
""" 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import math 			  		 			 	 	 		 		 	  		   	  			  	
import LinRegLearner as lrl 	
import DTLearner as dt
import RTLearner as rt			 
import BagLearner as bl 	
import pandas as pd  	
import matplotlib.pyplot as plt 
import time	 			 	 	 		 		 	  		   	  			  	
#import sys 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 
    
    gtid = 903370141
    np.random.seed(gtid)
    my_leaf_size = 10
  	
	
    '''	
    print sys.argv	
    print len(sys.argv) 
	  		 			 	 	 		 		 	  		   	  			  	
    if len(sys.argv) != 2: 			  		 			 	 	 		 		 	  		   	  			  	
        print "Usage: python testlearner.py <filename>" 			  		 			 	 	 		 		 	  		   	  			  	
        sys.exit(1) 			  		 			 	 	 		 		 	  		   	  			  	
    inf = open(sys.argv[1])
    '''
    
    #inf = open("Istanbul.csv") 			  		 			 	 	 		 		 	  		   	  			  	
    #data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()]) 
    #for s in inf.readlines():
    #    print s.strip().split(',')

    df_temp = pd.read_csv("./Data/Istanbul.csv", index_col='date',  		   	  			    		  		  		    	 		 		   		 		  
                parse_dates=True, na_values=['nan']) 		    			  		 			 	 	 		 		 	  		   	  			  	
 	

    data = df_temp.values		  		 			 	 	 		 		 	  		   	  			  	
    # compute how much of the data is training and testing 			  		 			 	 	 		 		 	  		   	  			  	
    train_rows = int(0.6* data.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    test_rows = data.shape[0] - train_rows 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # separate out training and testing data 			  		 			 	 	 		 		 	  		   	  			  	
    trainX = data[:train_rows,0:-1] 			  		 			 	 	 		 		 	  		   	  			  	
    trainY = data[:train_rows,-1] 			  		 			 	 	 		 		 	  		   	  			  	
    testX = data[train_rows:,0:-1] 			  		 			 	 	 		 		 	  		   	  			  	
    testY = data[train_rows:,-1] 		

    """
    abs_corrcoef = np.zeros(trainX.shape[1],)
    for j in range(trainX.shape[1]):
        abs_corrcoef[j] = abs(np.corrcoef(trainX[:,j], trainY)[0,1])
        if math.isnan(abs_corrcoef[j]):
            abs_corrcoef[j] = 0	  		 			 	 	 		 		 	  		   	  			  	
	  		 			 	 	 		 		 	  		   	  			  	
    # create a learner and train it 	
    print "\n\nLinRegLearner"		  		 			 	 	 		 		 	  		   	  			  	
    learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner 			  		 			 	 	 		 		 	  		   	  			  	
    learner.addEvidence(trainX, trainY) # train it 			  		 			 	 	 		 		 	  		   	  			  	
    print learner.author() 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # evaluate in sample 			  		 			 	 	 		 		 	  		   	  			  	
    predY = learner.query(trainX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "In sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=trainY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # evaluate out of sample 			  		 			 	 	 		 		 	  		   	  			  	
    predY = learner.query(testX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Out of sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=testY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 			
    """	

    list_leaf_size = range(1,51,1)
    
    rmse_DTLearner  = [0. for i in list_leaf_size]
    corr_DTLearner = [0. for i in list_leaf_size]
    
    rmse_BagLearner  = [0. for i in list_leaf_size]
    corr_BagLearner = [0. for i in list_leaf_size]
    
    rmse_RTLearner  = [0. for i in list_leaf_size]
    corr_RTLearner = [0. for i in list_leaf_size]
    
    elapse_DTLearner_Query = [0. for i in list_leaf_size]
    elapse_DTLearner_Train = [0. for i in list_leaf_size]
    elapse_RTLearner_Query = [0. for i in list_leaf_size]
    elapse_RTLearner_Train = [0. for i in list_leaf_size]
    #elapse_BagLearner_Query = [0. for i in list_leaf_size]
    #elapse_BagLearner_Train = [0. for i in list_leaf_size]
    
    for k in range(len(list_leaf_size)):
        print "\n\nDTLearner"
        start = time.time()
        learner = dt.DTLearner(leaf_size = list_leaf_size[k], verbose = False) # constructor
        learner.addEvidence(trainX, trainY) # training step
        end = time.time()
        elapse_DTLearner_Train[k] = end - start
        print learner.author()        
        
        start = time.time()			
        predY = learner.query(trainX) # query  				
        end = time.time()
        elapse_DTLearner_Query[k] = end - start  	
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
        print 			  		 			 	 	 		 		 	  		   	  			  	
        print "In sample results" 			  		 			 	 	 		 		 	  		   	  			  	
        print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
        c = np.corrcoef(predY, y=trainY) 			  		 			 	 	 		 		 	  		   	  			  	
        print "corr: ", c[0,1] 		
    
        # evaluate out of sample   		 			 	 	 		 		 	  		   	  			  	
        predY = learner.query(testX) # get the predictions 	 			 	 	 		 		 	  		   	  			  	
        rmse_DTLearner[k] = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
        print 			  		 			 	 	 		 		 	  		   	  			  	
        print "Out of sample results" 			  		 			 	 	 		 		 	  		   	  			  	
        print "RMSE: ", rmse_DTLearner[k] 			  		 			 	 	 		 		 	  		   	  			  	
        c = np.corrcoef(predY, y=testY) 			  		 			 	 	 		 		 	  		   	  			  	
        print "corr: ", c[0,1] 	
        corr_DTLearner[k] = c[0,1]
   
    for k in range(len(list_leaf_size)):
        print "\n\nRTLearner"
        start = time.time()
        learner = rt.RTLearner(leaf_size = list_leaf_size[k], verbose = False) # constructor
        learner.addEvidence(trainX, trainY) # training step
        end = time.time()
        elapse_RTLearner_Train[k] = end - start
        print learner.author()
        		  		 			 	 	 		 		 	  		   	  			  	
        start = time.time()			
        predY = learner.query(trainX) # query  		
        end = time.time()
        elapse_RTLearner_Query[k] = end - start  		  		
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
        print 			  		 			 	 	 		 		 	  		   	  			  	
        print "In sample results" 			  		 			 	 	 		 		 	  		   	  			  	
        print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
        c = np.corrcoef(predY, y=trainY) 			  		 			 	 	 		 		 	  		   	  			  	
        print "corr: ", c[0,1] 		
    
        # evaluate out of sample 	  		 			 	 	 		 		 	  		   	  			  	
        predY = learner.query(testX) # get the predictions 		 			 	 	 		 		 	  		   	  			  	
        rmse_RTLearner[k] = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
        print 			  		 			 	 	 		 		 	  		   	  			  	
        print "Out of sample results" 			  		 			 	 	 		 		 	  		   	  			  	
        print "RMSE: ", rmse_DTLearner[k] 			  		 			 	 	 		 		 	  		   	  			  	
        c = np.corrcoef(predY, y=testY) 			  		 			 	 	 		 		 	  		   	  			  	
        print "corr: ", c[0,1] 	
        corr_RTLearner[k] = c[0,1]
        
    for k in range(len(list_leaf_size)):    
        #BagLearner
        print "\n\nBagLearner - DTLearner"
    
        learner = bl.BagLearner(learner = dt.DTLearner,  kwargs = {"leaf_size" : list_leaf_size[k]}, verbose = False) # constructor
        learner.addEvidence(trainX, trainY) # training step
        print learner.author()
        
        predY = learner.query(trainX) # query  	
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
        print 			  		 			 	 	 		 		 	  		   	  			  	
        print "In sample results" 			  		 			 	 	 		 		 	  		   	  			  	
        print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
        c = np.corrcoef(predY, y=trainY) 			  		 			 	 	 		 		 	  		   	  			  	
        print "corr: ", c[0,1] 		
    
        # evaluate out of sample 			  		 			 	 	 		 		 	  		   	  			  	
        predY = learner.query(testX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
        rmse_BagLearner[k] = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
        print 			  		 			 	 	 		 		 	  		   	  			  	
        print "Out of sample results" 			  		 			 	 	 		 		 	  		   	  			  	
        print "RMSE: ", rmse_BagLearner[k] 			  		 			 	 	 		 		 	  		   	  			  	
        c = np.corrcoef(predY, y=testY) 			  		 			 	 	 		 		 	  		   	  			  	
        print "corr: ", c[0,1] 	
        corr_BagLearner[k] = c[0,1]  
        
    genplot = True
    if genplot:            
        df = pd.DataFrame(rmse_DTLearner, columns=['DTLearner'], index = list_leaf_size)
        df['BagLearner - DTLearner'] = rmse_BagLearner
        ax = df.plot(title="Over Fitting Analysis", fontsize=12,xlim=(0.,len(list_leaf_size)), ylim=(0.004,0.008))  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_xlabel(xlabel="leaf size")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel(ylabel="RMSE")  
        #fig = ax.get_figure()
        #fig.savefig('DTLearner_RMSE.png')
        plt.tight_layout()      
        plt.savefig('BagLearner_DTLearner_RMSE.png')
        
        df = pd.DataFrame(rmse_DTLearner, columns=['DTLearner'], index = list_leaf_size)
        df['RTLearner'] = rmse_RTLearner
        ax = df.plot(title="Over Fitting Analysis", fontsize=12,xlim=(0.,len(list_leaf_size)), ylim=(0.004,0.008))  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_xlabel(xlabel="leaf size")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel(ylabel="RMSE")  
        plt.tight_layout()      
        plt.savefig('DTLearner_RTLearner_RMSE.png')
        
        df = pd.DataFrame(corr_DTLearner, columns=['DTLearner'], index = list_leaf_size)
        df['RTLearner'] = corr_RTLearner
        ax = df.plot(title="Over Fitting Analysis", fontsize=12,xlim=(0.,len(list_leaf_size)))  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_xlabel(xlabel="leaf size")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel(ylabel="Correlation")  
        plt.tight_layout()      
        plt.savefig('DTLearner_RTLearner_corr.png')
        
        df = pd.DataFrame(elapse_DTLearner_Train, columns=['DTLearner'], index = list_leaf_size)
        df['RTLearner'] = elapse_RTLearner_Train
        ax = df.plot(title="Train Time Elapsed Analysis", fontsize=12,xlim=(0.,len(list_leaf_size)))  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_xlabel(xlabel="leaf size")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel(ylabel="Time Elapse")  
        plt.tight_layout()      
        plt.savefig('DTLearner_RTLearner_Train Time Elapsed.png')
        
        df = pd.DataFrame(elapse_DTLearner_Query, columns=['DTLearner'], index = list_leaf_size)
        df['RTLearner'] = elapse_RTLearner_Query
        ax = df.plot(title="Query Time Elapsed Analysis", fontsize=12,xlim=(0.,len(list_leaf_size)))  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_xlabel(xlabel="leaf size")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel(ylabel="Time Elapse")  
        plt.tight_layout()      
        plt.savefig('DTLearner_RTLearner_Query Time Elapsed.png')
    """    
    print "\n\nDTLearner"
    learner = dt.DTLearner(leaf_size = my_leaf_size, verbose = False) # constructor
    learner.addEvidence(trainX, trainY) # training step
    print learner.author()
    
    predY = learner.query(trainX) # query  	
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "In sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=trainY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 		

    # evaluate out of sample 			  		 			 	 	 		 		 	  		   	  			  	
    predY = learner.query(testX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Out of sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=testY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 		  	

    
    print "\n\nRTLearner"
    learner = rt.RTLearner(leaf_size = my_leaf_size, verbose = False) # constructor
    learner.addEvidence(trainX, trainY) # training step
    print learner.author()
    
    predY = learner.query(trainX) # query  	
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "In sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=trainY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 		

    # evaluate out of sample 			  		 			 	 	 		 		 	  		   	  			  	
    predY = learner.query(testX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Out of sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=testY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 		 	


    #BagLearner
    print "\n\nBagLearner - LinRegLearner"

    learner = bl.BagLearner(lrl.LinRegLearner, verbose = False) # constructor
    learner.addEvidence(trainX, trainY) # training step
    print learner.author()
    
    predY = learner.query(trainX) # query  	
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "In sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=trainY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 		

    # evaluate out of sample 			  		 			 	 	 		 		 	  		   	  			  	
    predY = learner.query(testX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Out of sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=testY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 		 	


    
    #BagLearner
    print "\n\nBagLearner - DTLearner"

    learner = bl.BagLearner(learner = dt.DTLearner,  kwargs = {"leaf_size" : my_leaf_size}, verbose = False) # constructor
    learner.addEvidence(trainX, trainY) # training step
    print learner.author()
    
    predY = learner.query(trainX) # query  	
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "In sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=trainY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 		

    # evaluate out of sample 			  		 			 	 	 		 		 	  		   	  			  	
    predY = learner.query(testX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Out of sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=testY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 		 	 	 			 			 	 	 		 		 	  		   	  			  	


    #BagLearner
    print "\n\nBagLearner - RTLearner"

    learner = bl.BagLearner(learner = rt.RTLearner,  kwargs = {"leaf_size" : my_leaf_size}, verbose = False) # constructor
    learner.addEvidence(trainX, trainY) # training step
    print learner.author()
    
    predY = learner.query(trainX) # query  	
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "In sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=trainY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 		

    # evaluate out of sample 			  		 			 	 	 		 		 	  		   	  			  	
    predY = learner.query(testX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Out of sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=testY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 		 	 	 			 			 	 	 		 		 	  		   	  			  	

    print "\n\n InsaneLearner"
    import InsaneLearner as it
    learner = it.InsaneLearner(verbose = False) # constructor
    learner.addEvidence(trainX, trainY) # training step
    predY = learner.query(testX) # query
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Out of sample results" 			  		 			 	 	 		 		 	  		   	  			  	
    print "RMSE: ", rmse 			  		 			 	 	 		 		 	  		   	  			  	
    c = np.corrcoef(predY, y=testY) 			  		 			 	 	 		 		 	  		   	  			  	
    print "corr: ", c[0,1] 		 	 	 			 			 	 	 		 		 	  		   	  			  	
    """