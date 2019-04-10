import ast

import FloydWarshall


with open("../data//Test_node_weight_50.txt") as f:
    for line in f:
        line = line.strip("\n")
        graph = ast.literal_eval(line)
        FloydWarshall.floyd_warshall(graph)
        break
