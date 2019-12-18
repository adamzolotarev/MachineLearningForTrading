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
#from scipy.stats.stats import pearsonr
 			  		 			 	 	 		 		 	  		   	  			  	
class RTLearner(object): 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.DT = None
        self.build_tree_itr = 0	
        #gtid = 903370141
        #np.random.seed(gtid)  		 			 	 	 		 		 	  		   	  			  	
        #pass # move along, these aren't the drones you're looking for 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def author(self): 			  		 			 	 	 		 		 	  		   	  			  	
        return 'zzhang726' # replace tb34 with your Georgia Tech username 			  		 			 	 	 		 		 	  		   	  			  	

 			  		 			 	 	 		 		 	  		   	  			  	
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
        
        self.DT = self.build_tree(dataX,dataY) 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def query(self,points): 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Estimate a set of test points given the model we built. 			  		 			 	 	 		 		 	  		   	  			  	
        @param points: should be a numpy array with each row corresponding to a specific query. 			  		 			 	 	 		 		 	  		   	  			  	
        @returns the estimated values according to the saved model. 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        #return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]
        result = np.zeros((points.shape[0],))
        for i in range(points.shape[0]):
            result[i] = self.query_tree(points[i])
        return result		  		 			 	 	 		 		 	  		   	  			  	
    

    def build_tree(self,dataX, dataY):
        #print dataX.shape
        #print dataY.shape
        self.build_tree_itr = self.build_tree_itr + 1
        
        if dataX.shape[0] <= self.leaf_size or dataY.std() == 0:
            return np.array([[-1,np.mean(dataY),-1,-1]])
        else:
            '''
            abs_corrcoef = np.zeros(dataX.shape[1],)
            for j in range(dataX.shape[1]):
                abs_corrcoef[j] = abs(np.corrcoef(dataX[:,j], dataY)[0,1])
                if math.isnan(abs_corrcoef[j]):
                    abs_corrcoef[j] = 0
            i = np.argmax(abs_corrcoef)
            '''
            i = int(math.floor(np.random.random()*dataX.shape[1]))
            if i == dataX.shape[1]:
                i = i - 1
                
            splitVal = np.median(dataX[:,i])
            
            #if self.build_tree_itr > 20:
            #    print 'interation' + str(self.build_tree_itr) #debug
                
            dataX_L = dataX[dataX[:, i] <= splitVal]
            dataY_L = dataY[dataX[:, i] <= splitVal]
            dataX_R = dataX[dataX[:, i] >  splitVal]
            dataY_R = dataY[dataX[:, i] >  splitVal]
            
            if dataY_R.shape[0] == 0: # avoid empty data and infinity recursion
                max_i = np.argmax(dataX[:, i])                    
                dataX_R = dataX_L[max_i:max_i+1]
                dataY_R = dataY_L[max_i:max_i+1]
                dataX_L = np.delete(dataX_L,max_i, 0)
                dataY_L = np.delete(dataY_L,max_i, 0)
            elif dataY_L.shape[0] == 0:
                min_i = np.argmin(dataX[:, i])                    
                dataX_L = dataX_R[min_i:min_i+1]
                dataY_L = dataY_R[min_i:min_i+1]
                dataX_R = np.delete(dataX_R,min_i, 0)
                dataY_R = np.delete(dataY_R,min_i, 0)                
                
            lefttree  = self.build_tree(dataX_L,dataY_L)
            righttree = self.build_tree(dataX_R,dataY_R)        
                
           
            root	= np.array([[i,	splitVal, 1, lefttree.shape[0] + 1]])
            # [split value index, slplit value, lefttree row off set, right tree row of set]

            self.build_tree_itr = 0
            return	np.vstack((root, lefttree, righttree))
        
    def query_tree(self, point):
        row = 0  #starting from root
        while self.DT[row, 0] >= 0: #loop util finding leef
            if point[int(self.DT[row, 0])] <= self.DT[row, 1]:
                row = row + int(self.DT[row, 2]) #left tree
            else: 
                row = row + int(self.DT[row, 3]) #right tree
            
        return self.DT[row, 1]
         
			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    print "the secret clue is 'zzyzx'" 	
