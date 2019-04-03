import math

from MinWaitPS import waiting_time_slot


def electric_vehicle_required(demand_time, graph, shortest_distance, shortest_path, path, distance, time_limit, speed,
                              capacity, waiting_time, charging_rate, max_capacity):
    buffer_time = time_limit - int(math.ceil(distance / speed))
    max_distance_covered = time_limit * speed
    if buffer_time < 0 or max_distance_covered <= distance:
        path = shortest_path
        distance = shortest_distance
        buffer_time = time_limit - int(math.ceil(distance / (speed * 1.0)))
    buffer_time_copy = buffer_time
    demand_time_copy = demand_time
    n = len(path) - 1
    node = 0
    current_distance = 0
    number_car, p = 0, []
    p.append(path[node])
    cumulative_dis_intermediate = {}
    cumulative_dis_full = {}
    temp = 0
    for i in range(n):
        temp += graph[path[i]][path[i + 1]]
        cumulative_dis_full[path[i + 1]] = temp
    cumulative_dis_intermediate[path[node]] = 0
    while node < n:
        current_distance += graph[path[node]][path[node + 1]]
        if capacity >= current_distance:
            p.append(path[node + 1])
            cumulative_dis_intermediate[path[node + 1]] = current_distance
            node += 1
        else:
            p.append(path[node + 1])
            cumulative_dis_intermediate[path[node + 1]] = current_distance
            node += 1
            node_info = waiting_time_slot(demand_time, graph, p, current_distance, speed, capacity,
                                          waiting_time, charging_rate, max_capacity)
            options = node_info[0]
            if options == 3:
                node_min, waste_time, charging_amount, distance_covered = node_info[1:]
                charging_amount = min(charging_amount, buffer_time * charging_rate)
                charging_time = int(math.ceil(charging_amount / (1.0 * charging_rate)))
                available_charge = charging_time * charging_rate + (
                        capacity - cumulative_dis_intermediate[path[node - 1]])
                available_charge = min(available_charge, max_capacity)
                if available_charge >= graph[path[node - 1]][path[node]]:
                    capacity = available_charge - graph[path[node - 1]][path[node]]
                    node_waiting_time = list(waiting_time[node_min])
                    node_waiting_time[0] -= charging_time
                    waiting_time[node_min] = tuple(node_waiting_time)
                    current_distance = 0
                    buffer_time -= charging_time
                    demand_time += int(math.ceil(cumulative_dis_intermediate[path[node]] / (1.0 * speed))
                                       ) + charging_time
                    cumulative_dis_intermediate[path[node]] = current_distance
                    p = [path[node]]
                else:
                    capacity = max_capacity
                    current_distance = 0
                    number_car += 1
                    demand_time = demand_time + int(math.ceil(cumulative_dis_intermediate[path[node - 1]]
                                                              / (1.0 * speed)))
                    node = node - 1
                    cumulative_dis_intermediate[path[node]] = current_distance
                    p = [path[node]]
            elif options == 2:
                node_min, waste_time, charging_amount_before, distance_covered = node_info[1:]
                # charging_amount = min(charging_amount, buffer_time * charging_rate)
                charging_time_before = int(math.ceil(charging_amount_before / (1.0 * charging_rate)))
                charging_time_before = min(charging_time_before, max_capacity)
                total_time = charging_time_before + demand_time + waste_time
                # + int(math.ceil(distance_covered/(speed*1.0)))
                if total_time < buffer_time:
                    charging_amount_after = min((buffer_time - total_time) * charging_rate,
                                                current_distance - capacity -
                                                charging_amount_before)
                    #assert (charging_amount_after <= 0, "Charging Amount must be greater than Value ")
                    charging_amount = charging_amount_before + charging_amount_after
                    if capacity - cumulative_dis_intermediate[path[node - 1]] + charging_amount >= \
                            graph[path[node - 1]][path[node]]:
                        charging_time_after = int(math.ceil(charging_amount_after / (1.0 * charging_rate)))
                        charging_amount = charging_amount - charging_amount_after + min(
                            charging_time_after * charging_rate, max_capacity)
                        capacity = capacity - distance_covered + charging_amount - graph[path[node - 1]][path[node]]
                        node_waiting_time = list(waiting_time[node_min])
                        node_waiting_time[0] -= charging_time_before
                        node_waiting_time[1] += charging_time_after
                        waiting_time[node_min] = tuple(node_waiting_time)
                        demand_time += int(math.ceil(cumulative_dis_intermediate[path[node]] / (1.0 * speed))
                                           ) + node_waiting_time[1] - node_waiting_time[0]
                        current_distance = 0
                        cumulative_dis_intermediate[path[node]] = current_distance
                        p = [path[node]]
                    else:
                        capacity = max_capacity
                        current_distance = 0
                        number_car += 1
                        demand_time += int(math.ceil(cumulative_dis_intermediate[path[node - 1]] / (1.0 * speed)))
                        node = node - 1
                        cumulative_dis_intermediate[path[node]] = current_distance
                        p = [path[node]]
                else:
                    capacity = max_capacity
                    current_distance = 0
                    number_car += 1
                    demand_time += int(math.ceil(cumulative_dis_intermediate[path[node - 1]] / (1.0 * speed)))
                    node = node - 1
                    cumulative_dis_intermediate[path[node]] = current_distance
                    p = [path[node]]
            elif options == 1:
                node_min, waste_time, remaining, distance_covered = node_info[1:]
                recharge_amount = min(current_distance - capacity, buffer_time * charging_rate)
                charging_time = int(math.ceil(recharge_amount / (1.0 * charging_rate)))
                if capacity - distance_covered + recharge_amount >= remaining:
                    charging_amount = min(charging_time * charging_rate, max_capacity)
                    buffer_time -= charging_time
                    node_waiting_time = list(waiting_time[node_min])
                    if node_waiting_time[1] == 0:
                        node_waiting_time[1] = int(math.ceil(cumulative_dis_intermediate[node_min] / (speed * 1.0))
                                                   ) + demand_time + charging_time
                        node_waiting_time[0] = int(math.ceil(cumulative_dis_intermediate[node_min] / (speed * 1.0))
                                                   ) + demand_time
                    else:
                        node_waiting_time[1] = int(math.ceil(cumulative_dis_intermediate[node_min] / (speed * 1.0))
                                                   ) + demand_time + charging_time
                    waiting_time[node_min] = tuple(node_waiting_time)
                    # buffer_time -= charging_time
                    capacity = capacity - distance_covered + charging_amount - graph[path[node - 1]][path[node]]
                    current_distance = 0
                    demand_time += int(math.ceil(cumulative_dis_intermediate[path[node]] / (1.0 * speed))
                                       ) + charging_time
                    cumulative_dis_intermediate[path[node]] = current_distance
                    p = [path[node]]
                else:
                    capacity = max_capacity
                    current_distance = 0
                    number_car += 1
                    demand_time += int(math.ceil(cumulative_dis_intermediate[path[node - 1]] / (1.0 * speed)))
                    node = node - 1
                    cumulative_dis_intermediate[path[node]] = current_distance
                    p = [path[node]]
            else:
                pass
                node_min, waste_time, remaining, distance_covered = node_info[1:]
                if waste_time < buffer_time:
                    charging_amount = min((buffer_time - waste_time) * charging_rate, current_distance - capacity)
                    charging_time = int(math.ceil(charging_amount / (1.0 * charging_rate)))
                    if capacity - distance_covered + charging_amount >= remaining:
                        charging_amount = charging_time * charging_rate
                        buffer_time -= charging_time + waste_time
                        node_waiting_time = list(waiting_time[node_min])
                        node_waiting_time[1] = int(math.ceil(cumulative_dis_intermediate[node_min] / (speed * 1.0))
                                                   ) + demand_time + charging_time + waste_time
                        waiting_time[node_min] = tuple(node_waiting_time)
                        capacity = capacity - distance_covered + charging_amount - graph[path[node - 1]][path[node]]
                        current_distance = 0
                        demand_time += int(math.ceil(cumulative_dis_intermediate[path[node]] / (1.0 * speed))
                                           ) + charging_time + waste_time
                        cumulative_dis_intermediate[path[node]] = current_distance
                        p = [path[node]]
                    else:
                        capacity = max_capacity
                        current_distance = 0
                        number_car += 1
                        demand_time += int(math.ceil(cumulative_dis_intermediate[path[node - 1]] / (1.0 * speed)))
                        node = node - 1
                        cumulative_dis_intermediate[path[node]] = current_distance
                        p = [path[node]]
                else:
                    capacity = max_capacity
                    current_distance = 0
                    number_car += 1
                    demand_time += int(math.ceil(cumulative_dis_intermediate[path[node - 1]] / (1.0 * speed)))
                    node = node - 1
                    cumulative_dis_intermediate[path[node]] = current_distance
                    p = [path[node]]

    return number_car
