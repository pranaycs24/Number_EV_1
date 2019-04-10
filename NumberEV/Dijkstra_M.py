from collections import defaultdict
from heapq import *
from math import ceil, floor


def dijkstra(graph, f, t, wait_time, d_t, car_info):
    g = defaultdict(list)
    for key, value in graph.items():
        for r, c in graph[key]:
            g[key].append((c, r))

    q, seen, mins = [(d_t, f, ())], set(), {f: 0}

    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                # print str(c)+" "+str(v2)
                next = cost + c
                # tym=next/4
                # tym=0
                # next=tym
                wt_time = 0
                # if wait_time[v2][0]<=next<=wait_time[v2][1]:
                #     #print v2
                #     wt_time=wait_time[v2][1]-next
                # next+=wt_time
                # print next
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))
    return float("inf")


# def dijkstra(graph, f, t, wait_time, d_t, car_info):
#     g = defaultdict(list)
#     for key, value in graph.items():
#         for r, c in graph[key]:
#             g[key].append((c, r))
#
#     q, seen, mins = [(d_t, f, ())], set(), {f: 0}
#     while q:
#         (cost, v1, path) = heappop(q)
#         if v1 not in seen:
#             seen.add(v1)
#             path = (v1, path)
#             if v1 == t: return (cost, path)
#             for c, v2 in g.get(v1, ()):
#                 if v2 in seen: continue
#                 prev = mins.get(v2, None)
#                 next = cost + c / car_info.speed
#                 wt_time = 0
#                 if wait_time[v2][0] <= next <= wait_time[v2][1]:
#                     wt_time = wait_time[v2][1] - next
#                 next += wt_time
#                 if prev is None or next < prev:
#                     mins[v2] = next
#                     heappush(q, (next, v2, path))
#     return float("inf")


def d_sort(graph, f, t, wait_time, d_t, car_info):
    g = defaultdict(list)
    for key, value in graph.items():
        for r, c in graph[key]:
            g[key].append((c, r))

    q, seen, mins = [(d_t, f, (), 0)], set(), {f: 0}
    elapsed = {f: 0}

    while q:
        (cost, v1, path, wt) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = ([v1, cost], path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c / car_info.speed
                wt_time = 0
                if wait_time[v2][0] <= next <= wait_time[v2][1]:
                    dis = (next - elapsed[v1]) * car_info.speed + min(g.get(v2, ()), key=lambda first: first[0])[0]
                    wt_time = wait_time[v2][1] - next
                    if wt_time > wt:
                        wt_time -= floor((((cost - elapsed[v1]) * car_info.speed) % car_info.car_capacity) /
                                         car_info.charging_rate)
                        wt_time = max(wt_time, 0)

                next += wt_time
                if prev is None or next < prev:
                    mins[v2] = next
                    elapsed[v2] = elapsed[v1] + wt_time
                    heappush(q, (next, v2, path, wt_time))
    return float("inf")


def dijkstra_m(graph, f, t, wait_time, d_t, car_info):
    p = d_sort(graph, f, t, wait_time, d_t, car_info)
    a = []
    while p:
        a.append(p[0])
        p = p[1]
    a = a[1:]
    x = [0] * len(a)
    i = 0
    for x1 in a:
        x[i] = x1[0]
        i += 1
    x.reverse()
    print x
    # p=dijkstra(graph, f, t, wait_time, d_t)
    # #print p
    # a=[]
    # while p:
    #     a.append(p[0])
    #     p=p[1]
    # a=a[1:]
    # a.reverse()
    # #print a

    # #a.remove(a[-1])
    # #print a
    dis = 0
    for x2 in range(len(x) - 1):
        for v2, c in graph.get(x[x2], ()):
            # print v2
            if v2 == x[x2 + 1]:
                dis += c
    # #print dis
    return (dis, x)

def dijkstra_m(graph, f, t, wait_time, d_t, car_info):
    p = dijkstra(graph, f, t, wait_time, d_t, car_info)
    # print p
    a = []
    while p:
        a.append(p[0])
        p = p[1]
    a = a[1:]
    a.reverse()
    # print a

    # a.remove(a[-1])
    # print a
    dis = 0
    for x in range(len(a) - 1):
        for v2, c in graph.get(a[x], ()):
            # print v2
            if v2 == a[x + 1]:
                dis += c
    # print dis
    return (dis, a)
