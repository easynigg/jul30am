import math
from heapq import heappop, heappush

# --------------------------------------------
# Calculates the Euclidean distance between two points
# --------------------------------------------
def euclidean(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


# --------------------------------------------
# Heuristic Function:
# Estimates cost to complete the TSP from current path
# Strategy:
#   1. Minimum distance from last visited city to any unvisited
#   2. Minimum distance from any unvisited back to starting city
# Ensures admissibility and low overestimation
# --------------------------------------------
def tsp_heuristic(path, cities, unvisited):
    last = path[-1]

    # If no unvisited cities left, return cost to go back to start
    if not unvisited:
        return euclidean(cities[last], cities[path[0]])

    # Heuristic: connect to nearest unvisited + return from nearest unvisited to start
    h = min(euclidean(cities[last], cities[u]) for u in unvisited)
    h += min(euclidean(cities[u], cities[path[0]]) for u in unvisited)
    return h


# --------------------------------------------
# A* Search for TSP
# Each node = (f = g + h, path, cost-so-far)
# Path expands by exploring all unvisited cities from current city
# --------------------------------------------
def tsp_astar(cities):
    n = len(cities)
    
    # Initial state: starting at city 0, cost = 0
    start = (0, [0], 0)  # f, path, g
    heap = [start]       # Priority queue based on f = g + h

    while heap:
        f, path, g = heappop(heap)  # Get best node from frontier

        # If all cities are visited, add return-to-start cost and return
        if len(path) == n:
            g += euclidean(cities[path[-1]], cities[path[0]])
            return path + [path[0]], g

        # Explore all unvisited cities
        unvisited = set(range(n)) - set(path)
        for u in unvisited:
            new_path = path + [u]
            # g: actual cost to reach new city
            new_g = g + euclidean(cities[path[-1]], cities[u])
            # h: heuristic estimate to complete the tour
            h = tsp_heuristic(new_path, cities, unvisited - {u})
            # Push new state into priority queue
            heappush(heap, (new_g + h, new_path, new_g))


# --------------------------------------------
# Recursive Best-First Search (RBFS) for TSP
# Optimizes memory over A* by using recursive backtracking
# Maintains only best alternative f-value
# --------------------------------------------
def tsp_rbfs(cities):
    n = len(cities)

    # Recursive helper function
    def rbfs(path, g, f_limit):
        # If all cities are visited, return complete path with return to start
        if len(path) == n:
            g += euclidean(cities[path[-1]], cities[path[0]])
            return path + [path[0]], g, float('inf')  # float('inf') is dummy f-cost

        # Generate successors: all unvisited cities
        successors = []
        unvisited = set(range(n)) - set(path)
        for u in unvisited:
            new_path = path + [u]
            new_g = g + euclidean(cities[path[-1]], cities[u])
            h = tsp_heuristic(new_path, cities, unvisited - {u})
            f = new_g + h
            successors.append((f, new_path, new_g))

        if not successors:
            return None, float('inf'), float('inf')  # No path forward

        # Sort successors by f = g + h
        successors.sort()

        while successors:
            best_f, best_path, best_g = successors[0]

            # If best f exceeds the allowed f_limit, backtrack
            if best_f > f_limit:
                return None, float('inf'), best_f

            # Get f-cost of next best alternative (for limiting)
            alternative = successors[1][0] if len(successors) > 1 else float('inf')

            # Recurse with best path
            result, cost, new_f = rbfs(best_path, best_g, min(f_limit, alternative))

            # Update best node’s f-value after recursion
            successors[0] = (new_f, best_path, best_g)
            successors.sort()

            # If we found a complete result, return it
            if result:
                return result, cost, new_f

    # Start recursion from city 0
    result, cost, _ = rbfs([0], 0, float('inf'))
    return result, cost
