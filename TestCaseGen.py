import random
from math import ceil

from NumberEV.CarConfiguration import CarConfiguration
from NumberEV.Dijkstra import dijkstra
open("data/Test_node_weight_50.txt", 'w').close()
open("data/Demand_50_node.txt", 'w').close()
car_info = CarConfiguration(12, 17, 70)
max_demand = 1
number_node = 500
time_slot = 96
maximum_number_edge = number_node*(number_node - 1)/2
number_edge_range = [maximum_number_edge/15, maximum_number_edge/10]

for num_test in range(100):
    edges = set()
    for i in range(number_node):
        for j in range(number_node):
            if i != j:
                edges.add((i, j))
    graph = {}
    for i in range(number_node):
        graph[i] = []
    number_edge = random.randint(number_edge_range[0], number_edge_range[1])
    count = 0
    for j in range(number_node):
        k = j
        while j == k:
            k = random.randint(1, number_node)
        if (j, k) in edges:
            edge_weight = random.randint(2, 5)*car_info.speed
            graph[j].append((k, edge_weight))
            graph[k].append((j, edge_weight))
            edges.remove((j, k))
            edges.remove((k, j))
            count += 1

    while count < number_edge:
        selected_edge = random.choice(list(edges))
        j, k = selected_edge
        edge_weight = random.randint(2, 5) * car_info.speed
        graph[j].append((k, edge_weight))
        graph[k].append((j, edge_weight))
        edges.remove((j, k))
        edges.remove((k, j))
        count += 1

    with open("data/Test_node_weight_50.txt", 'a+') as f:
        f.write(str(graph)+"\n")

    # demand_mtx = {}
    # for i in range(time_slot):
    #     demand_mtx[i] = []
    # count = 0
    # for t in range(time_slot - 6):
    #     number_demand = random.randint(0, 6)
    #     number_demand_count = 0
    #     while number_demand_count < number_demand:
    #         if count < max_demand:
    #             source, destination = random.sample(range(number_node), 2)
    #             distance = dijkstra(graph, source, destination)
    #             if distance != float("inf"):
    #                 dist = tuple(distance)
    #                 deadline = int(ceil(distance[0]/car_info.speed)) + t
    #                 if deadline <= time_slot:
    #                     hop = 0
    #                     while distance:
    #                         distance = distance[1]
    #                         hop += 1
    #                     if hop > 3:
    #                         demand_mtx[t].append((source, destination))
    #                         count += 1
    #                         number_demand_count += 1
    #         else:
    #             break
    # while count < max_demand:
    #     t = random.randint(0, time_slot-3)
    #     source, destination = random.sample(range(number_node), 2)
    #     distance = dijkstra(graph, source, destination)
    #     if distance != float("inf"):
    #         deadline = int(ceil(distance[0] / car_info.speed)) + t
    #         if deadline <= time_slot:
    #             hop = 0
    #             while distance:
    #                 distance = distance[1]
    #                 hop += 1
    #             if hop > 3:
    #                 demand_mtx[t].append((source, destination))
    #                 count += 1
    # with open("data/Demand_50_node.txt", 'a+') as f:
    #     f.write(str(demand_mtx)+"\n")

