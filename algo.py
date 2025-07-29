import math
from heapq import heappop, heappush

def euclidean(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def tsp_heuristic(path, cities, unvisited):
    last = path[-1]
    if not unvisited:
        return euclidean(cities[last], cities[path[0]])
    h = min(euclidean(cities[last], cities[u]) for u in unvisited)
    h += min(euclidean(cities[u], cities[path[0]]) for u in unvisited)
    return h

def tsp_astar(cities):
    n = len(cities)
    start = (0, [0], 0)  # (f = g + h, path, cost-so-far)
    heap = [start]

    while heap:
        f, path, g = heappop(heap)
        if len(path) == n:
            g += euclidean(cities[path[-1]], cities[path[0]])
            return path + [path[0]], g

        unvisited = set(range(n)) - set(path)
        for u in unvisited:
            new_path = path + [u]
            new_g = g + euclidean(cities[path[-1]], cities[u])
            h = tsp_heuristic(new_path, cities, unvisited - {u})
            heappush(heap, (new_g + h, new_path, new_g))

def tsp_rbfs(cities):
    n = len(cities)

    def rbfs(path, g, f_limit):
        if len(path) == n:
            g += euclidean(cities[path[-1]], cities[path[0]])
            return path + [path[0]], g, float('inf')

        successors = []
        unvisited = set(range(n)) - set(path)
        for u in unvisited:
            new_path = path + [u]
            new_g = g + euclidean(cities[path[-1]], cities[u])
            h = tsp_heuristic(new_path, cities, unvisited - {u})
            f = new_g + h
            successors.append((f, new_path, new_g))

        if not successors:
            return None, float('inf'), float('inf')

        successors.sort()
        while successors:
            best_f, best_path, best_g = successors[0]
            if best_f > f_limit:
                return None, float('inf'), best_f
            alternative = successors[1][0] if len(successors) > 1 else float('inf')
            result, cost, new_f = rbfs(best_path, best_g, min(f_limit, alternative))
            successors[0] = (new_f, best_path, best_g)
            successors.sort()
            if result:
                return result, cost, new_f

    result, cost, _ = rbfs([0], 0, float('inf'))
    return result, cost
