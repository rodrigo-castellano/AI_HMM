import sys
 
input_data = []
 
for line in sys.stdin:
    a_list = line.split()
    map_object = map(float, a_list)
    list_of_integers = list(map_object)
    input_data.append(list_of_integers)

def convert_matrix(arr, rows, columns):
    i = 0
    final_arr = []
    for row in range(rows):
        column_arr = []
        for column in range(columns):
            column_arr.append(arr[column+(row*columns)])
        final_arr.append(column_arr)
    return final_arr


rowsA = int(input_data[0][0])
columnsA = int(input_data[0][1])
 
rowsB = int(input_data[1][0])
columnsB = int(input_data[1][1])

rowsPi = int(input_data[2][0])
columnsPi = int(input_data[2][1])

A_list = input_data[0][2:]
B_list = input_data[1][2:]
Pi = input_data[2][2:]

#print(rowsA)
#print(columnsA)
#print(rowsB)
#print(columnsB)
#print(rowsPi)
#print(columnsPi)

#print(A_list)
#print(B_list)

A = convert_matrix(A_list, rowsA, columnsA)
B = convert_matrix(B_list, rowsB, columnsB)

#print(A)
#print(B)
#print(Pi)

def print_as_matrix(arr):
    for row in arr:
        for column in row:
            print(f"{column}\t", end="")
        print()
    print()

#print_as_matrix(A)

#print_as_matrix(B)

#print(Pi)

def transition(state_probabilities, A, rowsA, columnsA):
    ans = []
    for column in range(columnsA):
        prob = 0
        for state in range(rowsA):
            prob = prob + (state_probabilities[state] * A[state][column])
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

first_transition = transition(Pi, A, rowsA, columnsA)
answer = most_likely_emssion(first_transition, B, rowsB, columnsB)
answer = [1, columnsB] + answer
print_ans(answer)