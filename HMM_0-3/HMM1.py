import sys
 
def print_as_matrix(arr):
    for row in arr:
        for column in row:
            print(f"{column}\t", end="")
        print()
    print()


def transition(state_probabilities, A, rowsA, columnsA):
    ans = []
    for column in range(columnsA):
        prob = 0
        for state in range(rowsA):
            prob = prob + (state_probabilities[state] * A[state][column])
        ans.append(prob)
    return ans

def forward_algo(alpha, A, rowsA, columnsA):
    ans = []
    for i in range(rowsA):
        prob = 0
        for j in range(columnsA):
            #print(f"{alpha[j]}* {A[j][i]}")
            prob = prob + (alpha[j] * A[j][i])
        #print(prob)
        ans.append(prob)
    return ans

def most_likely_emssion(state_probabilities, B, rowsB, columnsB):
    ans = []
    for column in range(columnsB):
        prob = 0
        for state in range(rowsB):
            prob = prob + (state_probabilities[state] * B[state][column])
        ans.append(prob)
    return ans


def print_ans(ans):
    for element in ans:
        print(element, end=" ")

def convert_matrix(arr, rows, columns):
    final_arr = []
    for row in range(rows):
        column_arr = []
        for column in range(columns):
            column_arr.append(arr[column+(row*columns)])
        final_arr.append(column_arr)
    return final_arr

def transpose(arr):
    return list(map(list, zip(*arr)))

def identity_of_matrix(dimension):
    identity = []
    for row in range(dimension):
        column_arr = []
        for column in range(dimension):
            value = 1 if column == row else 0
            column_arr.append(value)
        identity.append(column_arr)
    return identity

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

n_observations = input_data[3][0]
observations = input_data[3][1:]
observations = [int(x) for x in observations]

A = convert_matrix(A_list, rowsA, columnsA)
B = convert_matrix(B_list, rowsB, columnsB)
B_transposed = transpose(B)
A_transposed = transpose(A)

def observation_probability(current_state, observation):
    ans = []
    #print("Alpha:", current_state, "Obs:", observation)
    for state in range(len(current_state)):
        # print(f"{current_state[state]}* {observation[state]}")
        prob = current_state[state] * observation[state]
        ans.append(prob)
    return ans


def probability_of_sequence(obs_in_seq, n_observations, alpha, A, B, B_transposed, observations):
    if(obs_in_seq == (n_observations)):
        return sum(alpha)
    
    if(obs_in_seq == 0):
        alpha_new = observation_probability(alpha, B_transposed[observations[obs_in_seq]])
        #print(alpha_new)
        return probability_of_sequence(obs_in_seq+1, n_observations, alpha_new, A, B, B_transposed, observations)
    else:
        temp = forward_algo(alpha, A, rowsA, columnsA)
        alpha_new = observation_probability(temp, B_transposed[observations[obs_in_seq]])
       #print(alpha_new)
        return probability_of_sequence(obs_in_seq+1, n_observations, alpha_new, A, B, B_transposed, observations)


#print_as_matrix(A)
#print_as_matrix(B)
# print(A_transposed)
# print(B_transposed)
#print(Pi)
#print(observations)
#print()
answer = probability_of_sequence(0, n_observations, Pi, A, B, B_transposed, observations)
print(answer)


