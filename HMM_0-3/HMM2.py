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
Pi_specific = [(x, Pi[x], None) for x in range(len(Pi))]

# print_as_matrix(A)
# print_as_matrix(B)
# print(Pi)
# print(observations)
# print(Pi_specific)
# print()

def quick_print(arr):
    for el in arr:
        print(el)


def dot_product_specific(delta, observation):
    ans = []
    for state in range(len(delta)):
        prob = delta[state][1] * observation[state]
        ans.append((state, prob, None))
    return ans

def viterbi_algo(delta, A, rowsA, columnsA, observation):
    ans = []
    for i in range(rowsA):
        temp = []
        for j in range(columnsA):
            temp.append((i, delta[j][1] * A[j][i]*observation[i]))
        ans.append(max_viterbi(temp))

    return ans

def max_viterbi(arr):
    constant_node = arr[0][0]
    max_vit = (constant_node, arr[0][1], 0)
    for x in range(1,len(arr)):
        if(max_vit[1] < arr[x][1]):
            max_vit = (constant_node, arr[x][1], x)
    if(max_vit[1] == 0):
        max_vit = (constant_node, 0, None)
    return max_vit

def get_max_last_obs(arr):
    max_vit = arr[0]
    for x in range(1, len(arr)):
        if(max_vit[1] < arr[x][1]):
            max_vit = arr[x]
    return max_vit

def viterbi_sequence(arr):
    arr.reverse()
    current_node = arr[0]
    max_viterbi = get_max_last_obs(current_node)
    ans = [max_viterbi[0]]
    next_delta = max_viterbi[2]
    for x in range(1, len(arr)):
        new_element = arr[x][next_delta]
        ans.append(new_element[0])
        next_delta = new_element[2]
    ans.reverse()
    return ans

        

def most_likely_sequence(obs_in_seq, n_observations, delta, A, B, B_transposed, observations, answers):
    if(obs_in_seq == n_observations):
        #quick_print(answers)
        return viterbi_sequence(answers)
    
    if(obs_in_seq == 0):
        delta_new = dot_product_specific(delta, B_transposed[observations[obs_in_seq]])
        answers.append(delta_new)
        return most_likely_sequence(obs_in_seq+1, n_observations, delta_new, A, B, B_transposed, observations, answers)
    else:
        delta_new = viterbi_algo(delta, A, rowsA, columnsA, B_transposed[observations[obs_in_seq]])
        answers.append(delta_new)
        return most_likely_sequence(obs_in_seq+1, n_observations, delta_new, A, B, B_transposed, observations, answers)


#print_as_matrix(A)
#print_as_matrix(B)
# print(A_transposed)
# print(B_transposed)
#print(Pi)
#print(observations)
#print()
answer = most_likely_sequence(0, n_observations, Pi_specific, A, B, B_transposed, observations, [])
print_ans(answer)


