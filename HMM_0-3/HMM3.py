import sys
import math
 
def print_as_matrix(arr):
    for row in arr:
        for column in row:
            print(f"{column}\t", end="")
        print()
    print()

def print_ans(matrix, rows, columns):
    print(rows, end=" ")
    print(columns, end=" ")
    for x in matrix:
        for element in x:
            print(element, end=" ")

def convert_matrix(arr, rows, columns):
    final_arr = []
    for row in range(rows):
        column_arr = []
        for column in range(columns):
            column_arr.append(arr[column+(row*columns)])
        final_arr.append(column_arr)
    return final_arr

def random_matrix(A,nrow, ncol, scale, value, pi=False):
    # seed(4)
    # scale= 0.01
    # A = random_matrix(A,rowsA, columnsA, scale, 1/N)
    # B = random_matrix(B,rowsB, columnsB, scale, 1/M)
    # Pi = random_matrix(Pi,rowsPi, columnsPi, scale, 1/N, True)
    if pi:
        sum = 0
        for i in range(ncol):
            A[i] = value + scale*random()
            sum += A[i] 
            #print('A[',i,']',A[i], ' sum ', sum)
        #scale
        check = 0
        for i in range(ncol):
            A[i] = A[i]/sum
            check += A[i]
        #print('check', check)

    else:
        for i in range(nrow):
            sum = 0
            for j in range(ncol):
                A[i][j] = value + scale*random()
                sum += A[i][j] 
                #print('A[',i,'][',j,']',A[i][j], ' sum ', sum)

            #scale
            check = 0
            for j in range(ncol):
                A[i][j] = A[i][j]/sum
                check += A[i][j]
            #print('check', check)
    return A

def dist_matrices(A1,A2, nrow, ncol, pi=False):
    # real_A = [[0.7, 0.05, 0.25], [0.1, 0.8, 0.1], [0.2, 0.3, 0.5]]
    # real_B = [[0.7, 0.2, 0.1, 0], [0.1, 0.4, 0.3, 0.2], [0, 0.1, 0.2, 0.7]]
    # real_Pi = [1, 0, 0]

    # distance1 = dist_matrices(real_A, A, rowsA, columnsA)
    # distance2 = dist_matrices(real_B, B, rowsB, columnsB)
    # distance3 = dist_matrices(real_Pi, Pi, rowsPi, columnsPi, True)
    # print('distances', distance1, distance2, distance3 ,' total ', distance1+distance2+distance3)
    
    if pi:
        sum = 0
        for i in range(ncol):
                sum += (A1[i]-A2[i])**2
        sum = sum**0.5

    else:
        sum = 0
        for i in range(nrow):
            for j in range(ncol):
                #print('dis ',A1[i][j],A2[i][j], 'substract ', A1[i][j]-A2[i][j])
                sum += (A1[i][j]-A2[i][j])**2
        sum = sum**0.5
    return sum

input_data = []
 
for line in sys.stdin:
    a_list = line.split()
    map_object = map(float, a_list)
    list_of_integers = list(map_object)
    input_data.append(list_of_integers)


rowsA = int(input_data[0][0])
columnsA = int(input_data[0][1])
 
rowsB = int(input_data[1][0])
columnsB = int(input_data[1][1])

rowsPi = int(input_data[2][0])
columnsPi = int(input_data[2][1])

A_list = input_data[0][2:]
B_list = input_data[1][2:]
Pi = input_data[2][2:]

n_observations = int(input_data[3][0])
observations = input_data[3][1:]
observations = [int(x) for x in observations]

N = rowsA
M = columnsB
T = n_observations

A = convert_matrix(A_list, rowsA, columnsA)
B = convert_matrix(B_list, rowsB, columnsB)

def quick_print(arr):
    for el in arr:
        print(el)


# print_as_matrix(A)
# print_as_matrix(B)
# print(Pi)
# print()
# print(observations)
# print()

maxIters = 1000
oldLogProb = float("-inf")



def baum_welch(A,B, Pi, observations):
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
    beta_t.reverse()
    #print(beta_t)



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

    for i in range(N):
        Pi[i] = gamma_t[0][i]

    #Restimate A

    for i in range(N):
        denom = 0.0
        for t in range(T-1):
            denom = denom + gamma_t[t][i]
        for j in range(N):
            numer = 0.0
            for t in range(T-1):
                numer = numer + digamma_t[t][i][j]
            A[i][j] = float(round(numer/denom, 6))

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
            B[i][j] = float(round(numer/denom, 6))

    ##COMPUTE log[P(0|lambda)]
    logProb = float(0)
    for t in range(T):
        logProb = logProb + math.log(c[t])
    logProb = -logProb
    return logProb


logProb = 0.0
for iters in range(maxIters):
    #print(iters)
    logProb = baum_welch(A, B, Pi, observations)
    #print("New:", logProb, "Old:", oldLogProb)
    if(logProb>oldLogProb):
        oldLogProb = logProb
    else:
        break
    

print_ans(A, N, N)
print()
print_ans(B, N, M)