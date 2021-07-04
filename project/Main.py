import copy
import math

"""
0-1 Multi-Constraint Knapsack Problem
To find best solution approximation we applied greedy algorithm and local search algorithm.
"""


def read_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        # all lines merging as a sublist to lines
        lines = [line.strip("\n").split() for line in lines]

        constraint = [int(i) for i in lines[0]]
        knapsack_number = constraint[0]
        value_number = constraint[1]
        # to find starting point values, knapsacks, weights
        value_limit = math.ceil((value_number / 10))
        knapsack_limit = math.ceil((knapsack_number / 10))
        # split lines to value, knapsack, all weights
        value = lines[1:value_limit + 1]
        knapsack = lines[value_limit + 1:value_limit + 1 + knapsack_limit]
        weight = lines[value_limit + 1 + knapsack_limit:]

        values_list = []
        knapsacks = []
        weights_list = []
        for i in value:
            values_list += i
        for i in knapsack:
            knapsacks += i
        for i in weight:
            weights_list += i
        # we read as a string convert to int all elements
        values_list = [int(i) for i in values_list]
        knapsacks = [int(i) for i in knapsacks]
        weights_list = [int(i) for i in weights_list]
        # until now all the weights were in a single array, now we have divided them into sublists.
        all_weights = [weights_list[x:x + len(values_list)] for x in range(0, len(weights_list), len(values_list))]

        sum_of_weights = [sum(x) for x in zip(*all_weights)]  # sum of all weights we will use for greedy algorithm
        weight_merge = zip(*all_weights)
        # we keep all m1, m2 , m3  weights together
        weight_pair = list(weight_merge)
    return knapsacks, values_list, weight_pair, sum_of_weights


# cap = capacities, sorted_arr = (values, value/weight , weight, order)
def optimization(cap, sorted_list, sorted_list2, total_value, index):
    sorted_order = []
    sorted_val = []
    sorted_weights = []
    for i in range(0, len(sorted_list)):
        sorted_val.append(sorted_list[i][0])
        sorted_weights.append(sorted_list[i][2])
        sorted_order.append(sorted_list[i][3])

    sorted_order2 = []
    sorted_val2 = []
    sorted_weights2 = []
    for i in range(0, len(sorted_list2)):
        sorted_val2.append(sorted_list2[i][0])
        sorted_weights2.append(sorted_list2[i][2])
        sorted_order2.append(sorted_list2[i][3])

    list_sorted_weights = [list(x) for x in sorted_weights]
    weight = copy.deepcopy(list_sorted_weights)

    # gives the total value of the backpack, which is limiting
    max_weight_bag = min(total_value)
    # We find out what bag the limiting backpack is.
    index_max_weight = total_value.index(max_weight_bag)
    knapsack_w2 = [0] * len(cap)
    for i in range(0, len(cap)):
        for j in range(0, index):
            knapsack_w2[i] += weight[j][i]
    new_cap = []
    for i in range(len(cap)):
        new_cap.append(cap[i] - knapsack_w2[i])
    new_cap2 = copy.deepcopy(new_cap)
    new_cap3 = copy.deepcopy(new_cap)
    new_cap4 = copy.deepcopy(cap)

    values_order = []
    after_greedy_weight = []
    after_greedy_weight_all_weight = []
    after_greedy_values = sorted_val[index:]
    for i in range(index, len(sorted_val)):
        values_order.append(sorted_order[i])
        after_greedy_weight.append(weight[i][index_max_weight])
        after_greedy_weight_all_weight.append(weight[i])
    # the new density is recalculated according to the restrictive bag.
    new_density = [a / (b + 1) for a, b in zip(after_greedy_values, after_greedy_weight)]
    new_merge = zip(after_greedy_values, new_density, values_order, after_greedy_weight_all_weight)
    new_merge_list = list(new_merge)
    # we are sorting according to new density
    sorted_density = sorted(new_merge_list, key=lambda x: float(x[1]), reverse=True)

    # we are sorting according to value, check if any of the best value summations work
    value_sorted = sorted(new_merge_list, key=lambda x: float(x[0]), reverse=True)

    new_weight = []
    new_value = []
    new_order = []
    new_weight2 = []
    new_value2 = []
    new_order2 = []

    for i in range(0, len(sorted_density)):
        new_value.append(sorted_density[i][0])
        new_weight.append(sorted_density[i][3])
        new_order.append(sorted_density[i][2])
        new_value2.append(value_sorted[i][0])
        new_weight2.append(value_sorted[i][3])
        new_order2.append(value_sorted[i][2])

    # this is greedy algorithm we add best ratio of value/weight  until it does not exceed the capacity of the bag.
    opt_value2 = []
    value_order2 = []
    for i in range(index + 1, len(sorted_weights)):
        for j in range(0, len(cap)):
            if new_cap[j] >= sorted_weights[i][j]:
                if j == len(cap) - 1:
                    for k in range(0, len(cap)):
                        new_cap[k] -= sorted_weights[i][k]
                    opt_value2.append(sorted_val[i])
                    value_order2.append(sorted_order[i])
            else:
                break

    # In greedy approach function we just find after which value and corresponding weights exceeds the capacity of the bag.
    # we try to improve the solution calculate new density according to bounding knapsack by dividing the remaining values by the bag weights that limit.
    opt_value = []
    value_order = []
    for i in range(0, len(new_weight)):
        for j in range(0, len(cap)):
            if new_cap2[j] >= new_weight[i][j]:
                if j == len(cap) - 1:
                    for k in range(0, len(cap)):
                        new_cap2[k] -= new_weight[i][k]
                    opt_value.append(new_value[i])
                    value_order.append(new_order[i])
            else:
                break

    # In greedy approach function we just find after which value and corresponding weights exceeds the capacity of the bag.In this algorithm.
    # we try to find best values don't exceeds capacity to add knapsack.
    opt_value3 = []
    value_order3 = []
    for i in range(0, len(new_weight2)):
        for j in range(0, len(cap)):
            if new_cap3[j] >= new_weight2[i][j]:
                if j == len(cap) - 1:
                    for k in range(0, len(cap)):
                        new_cap3[k] -= new_weight2[i][k]
                    opt_value3.append(new_value2[i])
                    value_order3.append(new_order2[i])
            else:
                break
    # this is for just control whether max values summation gives us better solution or not.
    opt_value4 = []
    value_order4 = []
    for i in range(0, len(sorted_weights2)):
        for j in range(0, len(new_cap4)):
            if new_cap4[j] >= sorted_weights2[i][j]:
                if j == len(new_cap4) - 1:
                    for k in range(0, len(new_cap4)):
                        new_cap4[k] -= sorted_weights2[i][k]
                    opt_value4.append(sorted_val2[i])
                    value_order4.append(sorted_order2[i])
            else:
                break

    if sum(opt_value2) > sum(opt_value) and sum(opt_value2) > sum(opt_value3):
        opt_value = opt_value2
        value_order = value_order2
    elif sum(opt_value3) > sum(opt_value) and sum(opt_value3) > sum(opt_value2):
        opt_value = opt_value3
        value_order = value_order3

    return total_value, opt_value, value_order, opt_value4, value_order4


# we are finding best rate of value/weight and sorting according to it.
def greedy_approach(cap, value, weight, sum_weight):
    density = [a / b for a, b in zip(value, sum_weight)]
    order_number = list(range(len(value)))
    merge_2 = zip(value, density, weight, order_number)
    value_d = list(merge_2)
    sortedlist = sorted(value_d, key=lambda x: float(x[1]), reverse=True)
    sortedlist2 = sorted(value_d, key=lambda x: float(x[0]), reverse=True)

    sorted_val = []
    sorted_weights = []
    for i in range(0, len(sortedlist)):
        sorted_val.append(sortedlist[i][0])
        sorted_weights.append(sortedlist[i][2])

    knapsack_w = [0] * len(cap)

    knapsack_weight_number = [0] * len(cap)
    total_value = [0] * len(cap)
    capacity = copy.deepcopy(cap)
    value_list = []
    # we add weights to the bags so that they do not exceed the weight of the bags.
    for i in range(0, len(cap)):
        item = []
        for j in range(0, len(sorted_val)):
            capacity[i] -= sorted_weights[j][i]
            if 0 <= capacity[i]:
                knapsack_w[i] += sorted_weights[j][i]
                knapsack_weight_number[i] += 1
                total_value[i] += sorted_val[j]
                item.append(sorted_val[j])
        value_list.append(item)
    index_last = min(knapsack_weight_number)
    # noinspection PyTypeChecker
    res = min(value_list, key=sum)
    return res, sortedlist, sortedlist2, total_value, value_list, sorted_val, index_last


def write_file(res, value, total_value, optimized_value, order_value, optimized_value2, order_value2):
    value_order_list = []

    for i in range(len(res)):
        value_order_list.append(value[i][3])

    for i in range(len(order_value)):
        value_order_list.append(order_value[i])

    new_total = min(total_value) + sum(optimized_value)
    greedy_total = sum(optimized_value2)
    if greedy_total > new_total:
        new_total = greedy_total
        value_order_list = order_value2

    with open("t4.txt", "w") as file:
        t = str(new_total) + "\n"
        file.write(t)

        for i in range(len(value)):
            if i != len(value) - 1:
                if i in value_order_list:
                    file.write('1' + '\n')
                else:
                    file.write("0" + '\n')
            else:
                if i in value_order_list:
                    file.write('1')
                else:
                    file.write("0")


bags, values, weights, sum_weights = read_file("test4.txt")
result, sorted_l, sorted_l2, total_v, arr, sorted_value, last_index = greedy_approach(bags, values, weights,
                                                                                      sum_weights)
total_values, opt1, order1, opt2, value2 = optimization(bags, sorted_l, sorted_l2, total_v, last_index)
write_file(result, sorted_l, total_values, opt1, order1, opt2, value2)
