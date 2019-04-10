import ast
import random
from math import ceil

from NumberEV.CarConfiguration import CarConfiguration
from NumberEV.Dijkstra import dijkstra
open("data/Demand_50_node.txt", 'w').close()
car_info = CarConfiguration(12, 17, 70)
max_demand = 100
number_node = 500
time_slot = 96

with open('data/Test_node_weight_50.txt') as f:
    for line in f:
        line = line.strip("\n")
        graph = ast.literal_eval(line)
        demand_mtx = {}
        visited = set()
        for i in range(time_slot):
            demand_mtx[i] = []
        count = 0
        # for t in range(time_slot - 6):
        #     number_demand = random.randint(0, 6)
        #     number_demand_count = 0
        #     while number_demand_count < number_demand:
        #         if count < max_demand:
        #             source, destination = random.sample(range(number_node), 2)
        #             if (source, destination) not in visited:
        #                 distance = dijkstra(graph, source, destination)
        #                 if distance != float("inf"):
        #                     dist = tuple(distance)
        #                     deadline = int(ceil(distance[0] / car_info.speed)) + t
        #                     if deadline <= time_slot:
        #                         hop = 0
        #                         while distance:
        #                             distance = distance[1]
        #                             hop += 1
        #                         if hop > 4:
        #                             identical = random.randint(10, 50)
        #                             for i in range(identical):
        #                                 demand_mtx[t].append((source, destination))
        #                             count += identical
        #                             number_demand_count += identical
        #                         else:
        #                             visited.add((source, destination))
        #                             visited.add((destination, source))
        #
        #         else:
        #             break
        while count < max_demand:
            #t = random.randint(0, time_slot - 3)
            source, destination = random.sample(range(number_node), 2)
            if (source, destination) not in visited:
                distance = dijkstra(graph, source, destination)
                if distance != float("inf"):
                    deadline = int(ceil(distance[0] / car_info.speed))
                    hop = 0
                    while distance:
                        distance = distance[1]
                        hop += 1
                    if hop > 4:
                        upper_time = time_slot - deadline - 1
                        if upper_time > 0:
                            t = random.randint(0, upper_time)
                            identical = random.randint(10, 50)
                            for i in range(identical):
                                demand_mtx[t].append((source, destination))
                            count += identical
                    else:
                        visited.add((source, destination))
                        visited.add((destination, source))
        with open("data/Demand_50_node.txt", 'a+') as demand:
            demand.write(str(demand_mtx) + "\n")