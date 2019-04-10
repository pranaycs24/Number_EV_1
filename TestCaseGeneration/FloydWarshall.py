import random
import numpy as np

import constant


def floyd_warshall(graph):
    node = random.sample(range(constant.NODE), constant.MAX_SELECTED_NODE)
    weight = np.zeros((constant.MAX_SELECTED_NODE, constant.MAX_SELECTED_NODE))
    column, row = 0, 0
    for i in node:
        row = 0
        node_dict = dict(graph[i])
        for j in node:
            if j in [x[0] for x in graph[i]]:
                weight[column][row] = node_dict[j]
            else:
                weight[column][row] = constant.INT_MAX
            row += 1
        column += 1
    distance = np.array(weight)
    #print distance
    reachability = np.zeros((constant.MAX_SELECTED_NODE, constant.MAX_SELECTED_NODE), dtype=int)

    for i in range(constant.MAX_SELECTED_NODE):
        for j in range(constant.MAX_SELECTED_NODE):
            if distance[i][j] < constant.INT_MAX or i == j:
                reachability[i][j] = 1
            else:
                reachability[i][j] = constant.INT_MAX
    print reachability
    for k in range(constant.MAX_SELECTED_NODE):

        for i in range(constant.MAX_SELECTED_NODE):

            for j in range(constant.MAX_SELECTED_NODE):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
                reachability[i][j] = min(reachability[i][j], (reachability[i][k] + reachability[k][j]))
    print distance
