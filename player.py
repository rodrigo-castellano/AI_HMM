#!/usr/bin/env python3

from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *
import random
import math

Pi_var          = 0
A_var           = 1
B_var           = 2
Obs_var         = 1
fish_ID_var     = 0
start_guessing  = 110

class PlayerControllerHMM(PlayerControllerHMMAbstract):
    def init_parameters(self):
        self.fishes_observations = [(i, []) for i in range(N_FISH)]
        B_arrays = []
        for i in range(N_SPECIES):
            B_arrays.append(self.random_matrix(1, 8, 0.1, 1/8))

        self.fishes_models = [([1], [[1]], B_arrays[i]) for i in range(N_SPECIES)]

    def guess(self, step, observations):
        
        for i in range(N_FISH):
            self.fishes_observations[i][Obs_var].append(observations[i])


        if(step<start_guessing):        
            return None
        else:
            #print("OBSERVATIONS: ", self.fishes_observations)
            #for i in range(7):
                #print("\nMODELS",i, self.fishes_models[i])
            fish_target_ID = self.fishes_observations[step-start_guessing][fish_ID_var]
            fish_target_observations = self.fishes_observations[step-start_guessing][Obs_var]
            maximum = float('-inf')
            fish_type = -1
            for i in range(N_SPECIES):
                prob = self.forward(self.fishes_models[i][A_var], self.fishes_models[i][B_var], 
                                        self.fishes_models[i][Pi_var], fish_target_observations)
                if prob>maximum:
                    maximum = prob
                    fish_type = i
            
            #print('fish_target_ID, fish_type',fish_target_ID, fish_type)
            return (fish_target_ID, fish_type)
        # This code would make a random guess on each step:
        # return (step % N_FISH, random.randint(0, N_SPECIES - 1))

        #return None

    def reveal(self, correct, fish_id, true_type):
        """
        This methods gets called whenever a guess was made.
        It informs the player about the guess result
        and reveals the correct type of that fish.
        :param correct: tells if the guess was correct
        :param fish_id: fish's index
        :param true_type: the correct type of the fish
        :return:
        """
       # print('correct, fish_id, true_type',correct, fish_id, true_type)
        if not correct:
            new_Pi, new_A, new_B = self.baum_welch(self.fishes_models[true_type][A_var], self.fishes_models[true_type][B_var],
                                                 self.fishes_models[true_type][Pi_var], self.fishes_observations[fish_id][Obs_var], 1, 8)
            #print('new',new_Pi, new_A, new_B)   
            self.fishes_models[true_type] = (new_Pi, new_A, new_B)

    def random_matrix(self, nrow, ncol, scale, value):
        B = [[0 for _ in range(ncol)] for _ in range(nrow)]
        for i in range(nrow):
            sum = 0
            for j in range(ncol):
                B[i][j] = value + scale*random.random()
                sum += B[i][j] 
                #print('A[',i,'][',j,']',A[i][j], ' sum ', sum)

            #scale
            check = 0
            for j in range(ncol):
                B[i][j] = B[i][j]/sum
                check += B[i][j]
            #print('check', check)
        return B

    def baum_welch(self, A, B, Pi, observations, rowsA, columnsB):

        maxIters = 1000
        iters = 0
        oldLogProb = float("-inf")
        N = rowsA
        M = columnsB
        T = len(observations)
        
        while(True):
            ## ALPHA
            alpha = []
            alpha_t = []
            c = [0.0 for x in range(T)]
            # compute initial alpha(i)

            for i in range(N):
                alpha0 = Pi[i] * B[i][observations[0]]
                alpha.append(alpha0)
                c[0] = c[0] + alpha0

            #Scale initial alpha(i)
            #c[0] = 1.0/c[0]
            if c[0]==0:
                c[0]=1
            else:
                c[0] = 1.0/c[0]
            for i in range(N):
                alpha[i] = c[0]*alpha[i]

            alpha_t.append(alpha)
            

            #Compute alphat(i)
            for t in range(1, T):
                c[t] = 0.0
                new_alpha = []
                for i in range(N):
                    at = 0.0
                    for j in range(N):
                        at = at + (alpha[j] * A[j][i])
                    at = at*B[i][observations[t]]
                    new_alpha.append(at)
                    c[t] = c[t] + at
                #Scale at
                #c[t] = 1.0/c[t]
                if c[t]==0:
                    c[t]=1
                else:
                    c[t] = 1.0/c[t]
                for i in range(N):
                    new_alpha[i] = c[t]*new_alpha[i]
                alpha_t.append(new_alpha)
                alpha = new_alpha.copy()


            ##BETA
            #Let Bt-1(i), scaled by Ct-1
            beta = []
            beta_t = []
            for i in range(N):
                beta.append(c[T-1])
            beta_t.append(beta)
            #print(beta_t)

            #Bpass
            for t in range(T-2, -1, -1):
                new_beta = []
                for i in range(N):
                    bt = 0
                    for j in range(N):
                        bt = bt + (A[i][j]*beta[j]*B[j][observations[t+1]])
                    new_beta.append(bt * c[t])
                beta = new_beta.copy()
                beta_t.append(beta)

            #print(len(beta_t))
            print(beta_t)
            beta_t.reverse()
            print(beta_t)


            ## COMPUTE GAMMA AND DIGAMMA
            digamma_t = []
            gamma_t = []

            for t in range(T-1):
                digamma = [[0.0 for x in range(N)] for x in range(N)]
                gamma = [0.0 for x in range(N)]
                for i in range(N):
                    gm = 0.0
                    for j in range(N):
                        digamma[i][j] = alpha_t[t][i]*A[i][j]*B[j][observations[t+1]]*beta_t[t+1][j]
                        gm = gm + digamma[i][j]
                    gamma[i] = gm
                digamma_t.append(digamma)
                gamma_t.append(gamma)

            gamma_t.append(alpha_t[T-1])

            ##RESTIMATE A, B, AND PI

            #reestimate Pi

            # for i in range(N):
            #     Pi[i] = gamma_t[0][i]

            # #Restimate A

            # for i in range(N):
            #     denom = 0.0
            #     for t in range(T-1):
            #         denom = denom + gamma_t[t][i]
            #     for j in range(N):
            #         numer = 0.0
            #         for t in range(T-1):
            #             numer = numer + digamma_t[t][i][j]
            #         A[i][j] = float(round(numer/denom, 6))

            #Resestimate B
            for i in range(N):
                denom = 0.0
                for t in range(T):
                    denom = denom + gamma_t[t][i]
                for j in range(M):
                    numer = 0.0
                    for t in range(T):
                        if(observations[t] == j):
                            numer = numer + gamma_t[t][i]
                    #B[i][j] = float(round(numer/denom, 6))
                    if denom==0:
                        B[i][j] = float(round(numer/1, 6))
                    else:
                        B[i][j] = float(round(numer/denom, 6))

            ##COMPUTE log[P(0|lambda)]
            logProb = float(0)
            for t in range(T):
                logProb = logProb + math.log(c[t])
            logProb = -logProb
            
            iters = iters + 1
            #print("New:", logProb, "Old:", oldLogProb)
            if(logProb>oldLogProb and iters<maxIters):
                oldLogProb = logProb
            else:
                break
        return (Pi, A, B)

    def forward_algo(self, alpha, A, rowsA, columnsA):
        ans = []
        for i in range(rowsA):
            prob = 0
            for j in range(columnsA):
                #print(f"{alpha[j]}* {A[j][i]}")
                prob = prob + (alpha[j] * A[j][i])
            #print(prob)
            ans.append(prob)
        return ans

    def observation_probability(self, current_state, observation):
        ans = []
        #print("Alpha:", current_state, "Obs:", observation)
        for state in range(len(current_state)):
            # print(f"{current_state[state]}* {observation[state]}")
            prob = current_state[state] * observation[state]
            ans.append(prob)
        return ans

    def probability_of_sequence(self,obs_in_seq, n_observations, alpha, A, B, B_transposed, observations):
        if(obs_in_seq == (n_observations)):
            return sum(alpha)
        
        if(obs_in_seq == 0):
            alpha_new = self.observation_probability(alpha, B_transposed[observations[obs_in_seq]])
            #print(alpha_new)
            return self.probability_of_sequence(obs_in_seq+1, n_observations, alpha_new, A, B, B_transposed, observations)
        else:
            temp = self.forward_algo(alpha, A, 1, 1)
            alpha_new = self.observation_probability(temp, B_transposed[observations[obs_in_seq]])
        #print(alpha_new)
        return self.probability_of_sequence(obs_in_seq+1, n_observations, alpha_new, A, B, B_transposed, observations)

    def forward(self, A, B, Pi, observations):
        n_observations = len(observations)
        B_transposed = self.transpose(B)

        answer = self.probability_of_sequence(0, n_observations, Pi, A, B, B_transposed, observations)
        
        return answer

    def transpose(self, arr):
        return list(map(list, zip(*arr)))