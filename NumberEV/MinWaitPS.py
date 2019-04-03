import math
import sys


def min_wait_time(node_info):
    min_value = sys.maxint
    selected_value = []
    while node_info:
        temp = node_info.pop()
        if temp[2] < min_value:
            min_value = temp[2]
            selected_value = temp
    return selected_value


def waiting_time_slot(demand_time, graph, path, distance, speed, capacity, waiting_time, charging_rate, max_capacity):
    cumulative_dis = 0
    count = 0
    node_info = []
    while capacity >= cumulative_dis and count < len(path) - 1:
        cumulative_dis += graph[path[count]][path[count + 1]]
        if cumulative_dis <= capacity:
            remaining = distance - cumulative_dis
            time_to_reach = int(math.ceil(cumulative_dis / speed)) + demand_time
            waiting_slot = waiting_time[path[count + 1]]
            if waiting_slot[0] <= time_to_reach <= waiting_slot[1]:
                info = [0, path[count + 1], waiting_slot[1] - time_to_reach, remaining, cumulative_dis]
                node_info.append(info)
            elif time_to_reach >= waiting_slot[1]:
                info = [1, path[count + 1], 0, remaining, cumulative_dis]
                node_info.append(info)
            else:
                charging_amount = min((waiting_slot[0] - time_to_reach) * charging_rate, cumulative_dis,
                                      remaining - (capacity - cumulative_dis))
                # amount of charging [waiting, distance to travel, remaining distance to cover ]
                capacity_avail = capacity + charging_amount
                if capacity_avail <= distance:
                    info = [2, path[count + 1], waiting_slot[1] - waiting_slot[0], charging_amount, cumulative_dis]
                    node_info.append(info)
                else:
                    info = [3, path[count + 1], 0, charging_amount, cumulative_dis]
                    node_info.append(info)
        elif capacity < max_capacity:
            time_to_reach = demand_time
            waiting_slot = waiting_time[path[count]]
            cumulative_dis = 0
            remaining = distance
            if waiting_slot[0] <= time_to_reach <= waiting_slot[1]:
                return [0, path[count], waiting_slot[1] - time_to_reach, remaining, cumulative_dis]

            elif time_to_reach >= waiting_slot[1]:
                return [1, path[count], 0, remaining, cumulative_dis]

            else:
                charging_amount = min((waiting_slot[0] - time_to_reach) * charging_rate, cumulative_dis,
                                      remaining - (capacity - cumulative_dis))
                # amount of charging [waiting, distance to travel, remaining distance to cover ]
                capacity_avail = capacity + charging_amount
                if capacity_avail <= distance:
                    return [2, path[count], waiting_slot[1] - waiting_slot[0], charging_amount, cumulative_dis]

                else:
                    return [3, path[count], 0, charging_amount, cumulative_dis]
        count += 1
    return min_wait_time(node_info)
