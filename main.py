from tsp_algorithms import tsp_astar, tsp_rbfs

cities = {
    0: (0, 0),
    1: (1, 5),
    2: (5, 2),
    3: (6, 6),
    4: (8, 3)
}

print("=== A* TSP ===")
path, cost = tsp_astar(cities)
print("Path:", path)
print("Cost:", cost)

print("\n=== RBFS TSP ===")
path, cost = tsp_rbfs(cities)
print("Path:", path)
print("Cost:", cost)
