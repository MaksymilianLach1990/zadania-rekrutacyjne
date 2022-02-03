"""
    A program that calculates the minimum effort needed to arrange the elephants in the right places.
    The program collects data by means of 4 standard inputs:
    1. Number of elephants - The number should be an integer.
    2. Weights of individual elephants, separated by a single space.
    3. Elephant numbers in their initial position, separated by a single space
    4. Elephant numbers in their final position, separated by a single space
"""

# First line: the number of elephants in the example
number_of_elephants = input()
number_of_elephants = int(number_of_elephants)                                                       

# Second line: the weight of the next elephants
weight_of_elephants = input()
# Separation of text into individual elements
weight_of_elephants = weight_of_elephants.split(' ')
# Replace 'string' elements into 'int' elements
list_of_elephants_weights = []                                                                   
for elephant in weight_of_elephants:                                                            
    list_of_elephants_weights.append(int(elephant))

# Third line: the initial position of the elephants
initial_layout = input()
# Separation of text into individual elements
initial_layout = initial_layout.split(' ')

# Fourth line: the target elephants pattern
final_layout = input()
# Separation of text into individual elements
final_layout = final_layout.split(' ')

# The lightest elephant in this example
the_lightest_elephant = min(list_of_elephants_weights)

# A dictionary that will include weights assigned to specific elephants
elephant_position_weight = {}                                                               
# A dictionary that will contain starting positions to target positions
elephant_position_starting_final = {}

# The list in which the cycles will be collected
cycles = [[], [], []]
# A list in which the optimal results of the cycles will be collected
result_optimal_methode = []


# Putting relevant data in dictionaries
def data_preparation(number_of_elephants, list_of_elephants_weights, position_start, position_end):
    for elephant in range(0, number_of_elephants):
        elephant_position_starting_final[position_start[elephant]] = position_end[elephant]

    for elephant in range(1, number_of_elephants+1):
        elephant_position_weight[str(elephant)] = list_of_elephants_weights[elephant-1]


# Assigning elephants to the appropriate cycles
def creating_cycles(elephant_position_starting_final, cycles):
    while True:
        # Checking the list, if it is empty - exit from the loop
        if len(elephant_position_starting_final.keys()) == 0:
            break
        
        elephant = elephant_position_starting_final.popitem()
        # Elephants in their place
        if elephant[0] == elephant[1]:
            cycles[0].append(elephant)
        # Elephant pairs that you just need to swap with each other
        elif elephant[0] != elephant[1] and elephant[0] == elephant_position_starting_final.get(elephant[1]):
            cycles[1].append((elephant, (elephant[1], elephant_position_starting_final.pop(elephant[1]))))
        # Cycles over 2 elephants
        elif elephant[0] != elephant[1] and elephant[0] != elephant_position_starting_final.get(elephant[1]):
            elephant_first = elephant
        # Separation of specific cycles
            long_cycle = []
            while True:
                long_cycle.append(elephant_first)
                
                if elephant_first[1] == elephant[0]:
                    
                    for elephant in long_cycle[1:]:
                        elephant_position_starting_final.pop(elephant[0])
                    cycles[2].append(tuple(long_cycle))
                    break
                
                else:
                    elephant_next = (elephant_first[1], elephant_position_starting_final[elephant_first[1]])
                
                elephant_first = elephant_next
    

# Pattern checking the first method
def method_1(sum_weight_elephants, cycle_lenght, min_weight_elephant):
    method_score = sum_weight_elephants + ((cycle_lenght - 2) * min_weight_elephant)
    return method_score


# Pattern checking the second method
def method_2(sum_weight_elephants, cycle_lenght, min_weight_elephant, the_lightest_elephant):
    method_score = sum_weight_elephants + min_weight_elephant + ((cycle_lenght + 1) * the_lightest_elephant)
    return method_score


# Calculate the total weight of elephants in a given cycle
def sum_weight_elephants_in_cycle(cycle, elephant_position_weight):
    sum_weight = 0
    for elephant in cycle:
        sum_weight += int(elephant_position_weight[elephant[0]])
    return sum_weight


# Determining the lightest elephant in a given cycle
def min_weight_elephant_in_cycle(cycle, elephant_position_weight):
    weight_elephants = []
    for elephant in cycle:
        weight_elephants.append(int(elephant_position_weight[elephant[0]]))
    return min(weight_elephants)


# Calculation of the effort required to rearrange elephants in a given cycle
def sum_of_effort_in_the_cycle(cycles): 
    # If the list is empty, continue on
    if len(cycles) == 0:
        return
    # Checking subsequent cycles
    for cycle in cycles:
        # If the cycle only contains 2 elephants, choose the first method
        if len(cycle) <= 2:
            result_optimal_methode.append(method_1(sum_weight_elephants_in_cycle(cycle, elephant_position_weight),
                                                   len(cycle), 
                                                   min_weight_elephant_in_cycle(cycle, elephant_position_weight)))
        # If the cycle contains more than 2 elephants, make calculations for 2 methods
        else:
            method_1_ = method_1(sum_weight_elephants_in_cycle(cycle, elephant_position_weight), len(cycle),
                                 min_weight_elephant_in_cycle(cycle, elephant_position_weight))
            method_2_ = method_2(sum_weight_elephants_in_cycle(cycle, elephant_position_weight), len(cycle),
                                 min_weight_elephant_in_cycle(cycle, elephant_position_weight), the_lightest_elephant)
        # Check which method gives the lower result and add to the list        
            if method_1_ <= method_2_:
                result_optimal_methode.append(method_1_)

            elif method_1_ > method_2_:
                result_optimal_methode.append(method_2_)


if __name__ == '__main__':
    # Preparation of appropriate data needed to perform the calculations
    data_preparation(number_of_elephants, weight_of_elephants, initial_layout, final_layout)
    creating_cycles(elephant_position_starting_final, cycles)
    # Performing appropriate calculations on cycles. Cycles with 2 elephants, and cycles with more than 2 words
    sum_of_effort_in_the_cycle(cycles[1])
    sum_of_effort_in_the_cycle(cycles[2])   
    # Calculate the total effort required to put the elephants in the right places
    score = sum(result_optimal_methode)
    # Displaying the result on the standard output
    print(score)
    