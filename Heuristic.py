from NumberEV.EVRequired import electric_vehicle_required
from NumberEV.Dijkstra_M import dijkstra_m
from NumberEV.CarConfiguration import CarConfiguration
import ast

open('H_Results.txt', 'w').close()
open('Replaced_car.txt', 'w').close()
demand = []
car_info = CarConfiguration(12, 17, 70)  # speed, charging_rate, car_capacity
with open("data/Demand_50_node.txt") as f:
    for line in f:
        line.strip("\n")
        demand.append(ast.literal_eval(line))

time_limit = []
short_path = []
dis_short = []

with open("data/shortest_path.txt") as f:
    s = f.read()
    sp = s.split("\n")
    sp.remove(sp[-1])
    # print sp
    index = 0
    for line in range(len(sp)):
        if line % 3 == 0:
            time_limit.append(ast.literal_eval(sp[line]))
        elif line % 3 == 1:
            short_path.append(ast.literal_eval(sp[line]))
        elif line % 3 == 2:
            dis_short.append(ast.literal_eval(sp[line]))

line = ''
g = []
with open("data/Test_node_weight_50.txt") as f:
    for line in f:
        line.strip("\n")
        g.append(ast.literal_eval(line))
for ik in range(len(g)):
    graph = {}
    for key, value in g[ik].items():
        graph[key] = {}
        for x in value:
            graph[key][x[0]] = x[1]

    # print graph
    number_car = 0
    number_car_replacement = 0
    flag = {}
    for key, value in dis_short[ik].items():
        flag[key] = 0
    # print flag
    vac_full = {}
    waiting_time = []
    for i in range(500):
        x = (0, 0)
        waiting_time.append(x)
    waiting_time_copy = list(waiting_time)
    kl = 0
    for key, value in demand[ik].items():
        # print value
        for x in value:
            if dis_short[ik][x] < car_info.car_capacity:
                number_car += 1
                number_car_replacement += 1
                print number_car
            else:
                # time_t=dis_short[x]/4+int(ceil((dis_short[x]-33)/3))#right now no use
                number_car_path = 1
                # print waiting_time
                kl += 1
                # print kl
                res = dijkstra_m(g[ik], x[0], x[1], waiting_time, key, car_info)  # return distance and path
                path = short_path[ik][x]
                count = 1
                dist = 0
                number_car_replacement += 1
                for i in range(len(path) - 1):
                    dist += graph[path[i]][path[i + 1]]
                    if dist > count * car_info.car_capacity:
                        number_car_replacement += 1
                speed = 12
                chr_rate = 17
                car_cap = 70
                # print path
                # print res[1]
                #waiting_time_copy = list(waiting_time)
                number_car_path += electric_vehicle_required(key, graph, dis_short[ik][x], path, res[1], res[0],
                                                             time_limit[ik][x], car_info.speed, car_info.car_capacity,
                                                             waiting_time, car_info.charging_rate,
                                                             car_info.car_capacity)
                count += electric_vehicle_required(key, graph, dis_short[ik][x], path, path, dis_short[ik][x],
                                                   time_limit[ik][x], car_info.speed, car_info.car_capacity,
                                                   waiting_time_copy, car_info.charging_rate,
                                                   car_info.car_capacity)
                if count < number_car_path:
                    number_car += count
                    waiting_time = list(waiting_time_copy)
                else:
                    number_car += number_car_path
                    waiting_time_copy = list(waiting_time)
                print number_car

            # print path

    # print number_car
    with open("H_Results.txt", 'a+') as f:
        f.write(str(number_car) + "\n")
    with open("Replaced_car.txt",'a+') as f:
        f.write(str(number_car_replacement) + "\n")
