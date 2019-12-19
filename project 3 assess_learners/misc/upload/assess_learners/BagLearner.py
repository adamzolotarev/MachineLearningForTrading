""" 			  		 			 	 	 		 		 	  		   	  			  	
A simple wrapper for linear regression.  (c) 2015 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
#from scipy.stats.stats import pearsonr
 			  		 			 	 	 		 		 	  		   	  			  	
class BagLearner(object): 			  		 			 	 	 		 		 	  		   	  			  	
		  		 			 	 	 		 		 	  		   	  			  	
    def __init__(self, learner = lrl.LinRegLearner, kwargs = {}, bags = 20, boost = False, verbose = False):

        
        self.bags = bags
        
        self.learners = []
        for k in range(0,bags):
            self.learners.append(learner(**kwargs))
	  		 			 	 	 		 		 	  		   	  			  	
        #pass # move along, these aren't the drones you're looking for 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def author(self): 			  		 			 	 	 		 		 	  		   	  			  	
        return 'zzhang726' # replace tb34 with your Georgia Tech username
 			  		 			 	 	 		 		 	  		   	  			  	
    def boottrapsampling(self,dataX,dataY):
        
        trainX = np.zeros_like(dataX)
        trainY = np.zeros_like(dataY)
        for k in range(dataX.shape[0]):
            i = int(math.floor(np.random.random()*dataX.shape[0]))
            if i == dataX.shape[0]:
                i = i - 1
            trainX[k] = dataX[i]
            trainY[k] = dataY[i]
        return trainX, trainY
 			  		 			 	 	 		 		 	  		   	  			  	
    def addEvidence(self,dataX,dataY): 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Add training data to learner 			  		 			 	 	 		 		 	  		   	  			  	
        @param dataX: X values of data to add 			  		 			 	 	 		 		 	  		   	  			  	
        @param dataY: the Y training values 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
        # slap on 1s column so linear regression finds a constant term 			  		 			 	 	 		 		 	  		   	  			  	
        #newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1]) 			  		 			 	 	 		 		 	  		   	  			  	
        #newdataX[:,0:dataX.shape[1]]=dataX 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
        # build and save the model 			  		 			 	 	 		 		 	  		   	  			  	
        #self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)
        for k in range(self.bags):
            trainX, trainY = self.boottrapsampling(dataX,dataY)
            self.learners[k].addEvidence(trainX, trainY) 		  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def query(self,points): 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Estimate a set of test points given the model we built. 			  		 			 	 	 		 		 	  		   	  			  	
        @param points: should be a numpy array with each row corresponding to a specific query. 			  		 			 	 	 		 		 	  		   	  			  	
        @returns the estimated values according to the saved model. 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        #return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]
        result = np.zeros((points.shape[0],))

        for k in range(self.bags):
            result = result + self.learners[k].query(points)
            
        result = result * 1.0 / self.bags
        return result 
	  		 			 	 	 		 		 	  		   	  			  	
          
            
			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    print "the secret clue is 'zzyzx'" 	
  		 			 	 	 		 		 	  		   	  			  	
