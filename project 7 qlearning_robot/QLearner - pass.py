""" 			  		 			 	 	 		 		 	  		   	  			  	
Template for implementing QLearner  (c) 2015 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import random as rand 			  		 			 	 	 		 		 	  		   	  			  	

	

class QLearner(object): 
			  		 			 	 	 		 		 	  		   	  			  	
    def author(self):
        return 'zzhang726' #Change this to your user ID
  			  		 			 	 	 		 		 	  		   	  			  	
    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False): 	
        #num_states integer, the number of states to consider
        #num_actions integer, the number of actions available.
        #alpha float, the learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.
        #gamma float, the discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.
        #rar float, random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.
        #radr float, random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.
        #dyna integer, conduct this number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.
        #verbose boolean, if True, your class is allowed to print debugging statements, if False, all printing is prohibited.		  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
        self.verbose = verbose 	
        self.num_states = num_states	  		 			 	 	 		 		 	  		   	  			  	
        self.num_actions = num_actions 			  		 			 	 	 		 		 	  		   	  			  	
        self.s = 0 			  		 			 	 	 		 		 	  		   	  			  	
        self.a = 0 	
        self.Q = np.zeros((num_states,num_actions)) 
        self.Qmax = np.zeros((num_states))
        self.alpha = alpha
        self.gamma = gamma
        #self.rar = np.ones((num_states))*rar
        self.rar = rar
        self.radr = radr
        
        self.dyna = dyna
        if self.dyna > 0:
            self.T = np.zeros((num_states,num_actions,num_states))
            self.R = np.zeros((num_states,num_actions))
            self.visited = np.zeros((num_states,num_actions)) # mark the [s,a] that have been updated 
            self.visitedList = [] #updated [s,a] stored in a list

        np.random.seed(1)            
 
        
    def get_action(self):
        #if rand.uniform(0.0, 1.0) <= self.rar[self.s]:
        if rand.uniform(0.0, 1.0) <= self.rar:
            #self.rar[self.s] = self.rar[self.s] * self.radr
            #self.rar = self.rar * self.radr
            action = rand.randint(0, self.num_actions-1)  # choose the random direction
        else: 
            #listy = self.Q[self.s]            
            #winner = np.argwhere(listy == np.amax(listy))
            #winnerList = winner.flatten().tolist()
            #action = winnerList[rand.randint(0, len(winnerList)-1)]
            action = np.argmax(self.Q[self.s])
        return action    
          		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def querysetstate(self, s): 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Update the state without updating the Q-table 			  		 			 	 	 		 		 	  		   	  			  	
        @param s: The new state 			  		 			 	 	 		 		 	  		   	  			  	
        @returns: The selected action 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        self.s = s 			  		 			 	 	 		 		 	  		   	  			  	
        #action = rand.randint(0, self.num_actions-1) 
        action = self.get_action()
        self.a = action			  		 			 	 	 		 		 	  		   	  			  	
        if self.verbose: print "s =", s,"a =",action 			  		 			 	 	 		 		 	  		   	  			  	
        return action 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def query(self,s_prime,r): 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Update the Q table and return an action 			  		 			 	 	 		 		 	  		   	  			  	
        @param s_prime: The new state 			  		 			 	 	 		 		 	  		   	  			  	
        @param r: The reward#ne state 			  		 			 	 	 		 		 	  		   	  			  	
        @returns: The selected action 			  		 			 	 	 		 		 	  		   	  			  	
        """ 
        q = self.Q[self.s,self.a]
        ##self.Q[self.s,self.a] = (1-self.alpha)*self.Q[self.s,self.a] + self.alpha*(r + self.gamma*max(self.Q[s_prime]))
        #if self.s != s_prime:
        self.Q[self.s,self.a] = (1-0)*self.Q[self.s,self.a] + self.alpha*( r + self.gamma*max(self.Q[s_prime]) - self.Q[self.s,self.a] )
        #else:
        #    #self.Q[self.s,self.a] = (1-0)*self.Q[self.s,self.a] + self.alpha*( r + 0.0)
        #    self.Q[self.s,self.a] = (1-0)*self.Q[self.s,self.a] + self.alpha*( r + self.gamma*max(self.Q[s_prime]) - self.Q[self.s,self.a] )
        self.Qmax[self.s] = max(self.Q[self.s])    
        if (self.dyna> 0) &(self.Q[self.s,self.a] != q):
            self.R[self.s,self.a] = (1-self.alpha)*self.R[self.s,self.a] + self.alpha*r
            if(self.visited[self.s,self.a] == 0):
                self.visitedList.append((self.s,self.a))
            self.visited[self.s,self.a] = self.visited[self.s,self.a] + 1                            
            self.T[self.s, self.a, s_prime] = self.T[self.s, self.a, s_prime] + 1
            listcount = len(self.visitedList)
            #dyna_nN0 = [rand.randint(0,listcount-1) for _ in range(self.dyna)] 
            dyna_nN = np.random.randint( listcount, size=self.dyna )            
            #print dyna_nN
            dyna_nN= np.unique(dyna_nN)
            #print dyna_nN
            for dyna_n in dyna_nN:
                
                dyna_s = self.visitedList[dyna_n][0]
                dyna_a = self.visitedList[dyna_n][1]
                dyna_r = self.R[dyna_s,dyna_a]
                
                #nm = np.max(self.Q, axis=1)
                nt = self.T[dyna_s,dyna_a,:]
                b = nt>0
                nt1 = nt[b]
                nm1 = self.Qmax[b]
                
                Q_prime = sum(nt1*nm1)/sum(nt1)
                self.Q[dyna_s,dyna_a] = (1-self.alpha)*self.Q[dyna_s,dyna_a] + self.alpha*(dyna_r + self.gamma*Q_prime)
                self.Qmax[dyna_s] = max(self.Q[dyna_s])
                if len(self.visitedList) == 1: 
                    break
        
        self.s = s_prime  		 			 	 	 		 		 	  		   	  			  	
        action = self.get_action()
        
        self.rar = self.rar * self.radr
        
        self.a = action
			  		 			 	 	 		 		 	  		   	  			  	
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r 		 			 	 	 		 		 	  		   	  			  	
        return action 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    print "Remember Q from Star Trek? Well, this isn't him" 			  		 			 	 	 		 		 	  		   	  			  	
