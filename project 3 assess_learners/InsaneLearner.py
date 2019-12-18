import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import LinRegLearner as lrl 		 	 
import BagLearner as bl 				 	 	 		 		 	  		   	  			  			  		 			 	 	 		 		 	  		   	  			  	
class InsaneLearner(object): 	 	 		 		 	  		   	  			  	
    def __init__(self, bags = 20, verbose = False):
        self.bags = bags
        self.learners = []
        for k in range(0,self.bags):
            self.learners.append(bl.BagLearner(lrl.LinRegLearner, verbose = False))   	
    def author(self): 			  		 			 	 	 		 		 	  		   	  			  	
        return 'zzhang726' # replace tb34 with your Georgia Tech username		  	
    def addEvidence(self,dataX,dataY):
        for k in range(0,self.bags):		 		 	  		   	  			  	
            self.learners[k].addEvidence(dataX, dataY) 			 	  		   	  			  	
    def query(self,points): 			  		 			 	 	 		 		 	  		   	  			  	
        result = np.zeros((points.shape[0],))
        for k in range(self.bags):
            result = result + self.learners[k].query(points)* 1.0 / self.bags
        return result