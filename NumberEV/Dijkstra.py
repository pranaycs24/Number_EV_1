from collections import defaultdict
from heapq import *
import ast
from math import ceil


def dijkstra(graph, f, t):
    g = defaultdict(list)
    for key, value in graph.items():
        for r, c in graph[key]:
            g[key].append((c, r))

    q, seen, mins = [(0, f, ())], set(), {f: 0}

    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))
    return float("inf")


if __name__ == "__main__":
    # a sample graph
    open('../data/shortest_path.txt', 'w').close()
    line = ''
    graph = []
    speed_car = 12
    with open('../data/Test_node_weight_50.txt') as f:
        for line in f:
            line = line.strip("\n")
            graph.append(ast.literal_eval(line))

    # print dijkstra(graph, 1, 5)
    dem_d = []
    with open("../data/Demand_50_node.txt") as f:
        for line in f:
            line = line.strip("\n")
            dem_d.append(ast.literal_eval(line))

    # print type(dem_d)
    for ik in range(len(dem_d)):
        demnd = set()
        for key, value in dem_d[ik].items():
            for v in dem_d[ik][key]:
                demnd.add(v)
        # print demnd
        deadline_time, pathl, distance = {}, {}, {}
        for i in demnd:
            res = dijkstra(graph[ik], i[0], i[1])
            print res
            pp = []
            for k in res:
                if type(0) == type(k):
                    deadline_time[i] = int(ceil((k / speed_car) * 2))
                    distance[i] = k
                else:
                    while len(k) == 2:
                        pp.append(k[0])
                        k = k[1]
            pp.reverse()
            pathl[i] = pp  # I represents?
        # print max(weight)
        print pathl
        print distance

        # t=max(weight)/speed_car
        # deadline_time=int(ceil(t))
        # print deadline_time
        with open("../data/shortest_path.txt", 'a+') as f:
            f.write(str(deadline_time) + "\n")
            f.write(str(pathl) + "\n")
            f.write(str(distance) + "\n")
    # print "F -> G:"
    # print dijkstra(edges, "F", "G")
