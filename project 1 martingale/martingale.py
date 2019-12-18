"""Assess a betting strategy. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 	
from math import factorial
import matplotlib.pyplot as plt		  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
def author(): 			  		 			 	 	 		 		 	  		   	  			  	
        return 'zzhang726' # replace tb34 with your Georgia Tech username. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
def gtid(): 			  		 			 	 	 		 		 	  		   	  			  	
	return 903370141 # replace with your GT ID number 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
def get_spin_result(win_prob): 
    result = False		 	 	 		 		 	  		   	  			  	
    if np.random.random() <= win_prob: 			  		 			 	 	 		 		 	  		   	  			  	
        result = True
    return result
 			  		 			 	 	 		 		 	  		   	  			  	
def test_code(): 			  		 			 	 	 		 		 	  		   	  			  	
    win_prob = 18.0/38.0 # set appropriately to the probability of a win 			  		 			 	 	 		 		 	  		   	  			  	
    np.random.seed(gtid()) # do this only once 			  		 			 	 	 		 		 	  		   	  			  	
    #print get_spin_result(win_prob) # test the roulette spin 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
	# add your code here to implement the experiments 	
    nRuns = 1000		  		 			 	 	 		 		 	  		   	  			  	
    winnings = 1.0 * np.zeros((nRuns,1001), dtype=int)

    for i in range(nRuns):    
        ibet = 0
        while winnings[i,ibet] < 80 and ibet < 1000:
            won = False
            bet_amount = 1
            
            while (not won) and ibet < 1000:
    			#wager bet_amount on black
                won = get_spin_result(win_prob)
                ibet = ibet + 1
                if won == True:
                    winnings[i, ibet] = winnings[i, ibet-1] + bet_amount
                    #print winnings
                else:
                    winnings[i, ibet] = winnings[i, ibet-1] - bet_amount
                    #print winnings
                    bet_amount = bet_amount * 2
                    
        #print i
        winnings[i, ibet+1:] = winnings[i, ibet]
    #print winnings
    #winnings = np.append(winnings, [1])
    #print winnings
    print 'In Experiment 1 ' + str(np.sum(winnings[:,-1] == 80)) + ' of the 1000 runs have winnings of $80'
    n = 1000
    lost_chance = 0
    for k in range(80):
        lost_chance = lost_chance + factorial(n) / factorial(k) / factorial(n - k) * win_prob ** k * (1-win_prob) ** (n-k)
    print 'In Experiment 1, using Binomial distribtuion, chance of not making $80 is ' + str(lost_chance)
    
    
    winnings_t = np.transpose(winnings)
    plt.plot(winnings_t[:,0:10])
    plt.axis([0, 300, -256, 100])
    plt.xlabel('Episode')
    plt.ylabel('Winnings')
    plt.title('Experiment 1 Figure 1')
    legend=[];
    for i in range(10):
        legend.append("run " + str(i+1))
    plt.legend(legend)
    plt.savefig('Experiment 1 Figure 1.png')
    #plt.show()
    plt.close()
    
    winnings_mean = winnings.mean(axis = 0)
    winnings_std = winnings.std(axis = 0)
    winnings_sta = np.array([winnings_mean,winnings_mean-winnings_std,winnings_mean+winnings_std])
    plt.plot(np.transpose(winnings_sta))
    plt.axis([0, 300, -256, 100])
    plt.xlabel('Episode')
    plt.ylabel('Winnings_Mean')
    plt.title('Experiment 1 Figure 2')
    plt.legend(['mean','mean - std', 'mean + std' ])
    plt.savefig('Experiment 1 Figure 2.png')
    plt.close()
    #plt.show()
    
    winnings_median = np.median(winnings, axis = 0)
    winnings_std = winnings.std(axis = 0)
    winnings_sta = np.array([winnings_median,winnings_median-winnings_std,winnings_median+winnings_std])
    plt.plot(np.transpose(winnings_sta))
    plt.axis([0, 300, -256, 100])
    plt.xlabel('Episode')
    plt.ylabel('Winnings_Median')
    plt.title('Experiment 1 Figure 3')
    plt.legend(['median','median - std', 'median + std'] )
    plt.savefig('Experiment 1 Figure 3.png')
    plt.close()
    #plt.show()
    
    
    #with bank roll limit
    bank_roll = 256
    nRuns = 1000		  		 			 	 	 		 		 	  		   	  			  	
    winnings = 1.0 * np.zeros((nRuns,1001), dtype=int)

    for i in range(nRuns):    
        ibet = 0
        while winnings[i,ibet] + bank_roll > 0 and winnings[i,ibet] < 80 and ibet < 1000:
            won = False
            bet_amount = 1
            
            while (not won) and ibet < 1000:
    			#wager bet_amount on black
                won = get_spin_result(win_prob)
                ibet = ibet + 1
                if won == True:
                    winnings[i, ibet] = winnings[i, ibet-1] + bet_amount
                    #print winnings
                else:
                    winnings[i, ibet] = winnings[i, ibet-1] - bet_amount
                    #print winnings
                    if winnings[i, ibet] + bank_roll <= 0 :
                        break
                    elif winnings[i, ibet] + bank_roll < bet_amount * 2 :
                        bet_amount = winnings[i, ibet] + bank_roll
                    else:
                        bet_amount = bet_amount * 2
                    

        winnings[i, ibet+1:] = winnings[i, ibet]

    #print winnings
    print "In Experiment 2, " + str(np.sum(winnings[:,-1] == 80)) + ' of the 1000 runs have winnings of $80 using bank roll of $256'
    
    winnings_mean = winnings.mean(axis = 0)
    winnings_std = winnings.std(axis = 0)
    winnings_sta = np.array([winnings_mean,winnings_mean-winnings_std,winnings_mean+winnings_std])
    plt.plot(np.transpose(winnings_sta))
    plt.axis([0, 300, -256, 100])
    plt.xlabel('Episode')
    plt.ylabel('Winnings_Mean')
    plt.title('Experiment 2 Figure 4')
    plt.legend(['mean','mean - std', 'mean + std' ])
    plt.savefig('Experiment 2 Figure 4.png')
    plt.close()
    print "In Experiment 2, the estimated expected value of our winnings after 1000 sequential bets is " + str(winnings_mean[1000])
    #plt.show()
    
    winnings_median = np.median(winnings, axis = 0)
    winnings_std = winnings.std(axis = 0)
    winnings_sta = np.array([winnings_median,winnings_median-winnings_std,winnings_median+winnings_std])
    plt.plot(np.transpose(winnings_sta))
    plt.axis([0, 300, -256, 100])
    plt.xlabel('Episode')
    plt.ylabel('Winnings_Median')
    plt.title('Experiment 2 Figure 5')
    plt.legend(['median','median - std', 'median + std'] )
    plt.savefig('Experiment 2 Figure 5.png')
    plt.close()
    #plt.show()
    
    """
    winnings_t = np.transpose(winnings)
    plt.plot(winnings_t[:,0:150])
    plt.axis([0, 300, -256, 100])
    plt.xlabel('Episode')
    plt.ylabel('Winnings')
    plt.title('Experiment 2 Figure 6')
    plt.savefig('Experiment 2 Figure 6.png')
    #plt.show()
    """
		  		 			 	 	 		 		 	  		   	  			  	
if __name__ == "__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    test_code() 			  		 			 	 	 		 		 	  		   	  			  	
