import random
import math

def hill_climbing_8_queens():
    state = [random.randrange(8) for _ in range(8)]
    def heuristic(s):
        conflicts = 0
        for i in range(8):
            for j in range(i+1, 8):
                if s[i] == s[j] or abs(s[i]-s[j]) == j-i:
                    conflicts += 1
        return conflicts
    while True:
        current = heuristic(state)
        if current == 0:
            return state
        neighbors = []
        best = current
        for col in range(8):
            for row in range(8):
                if state[col] == row:
                    continue
                s = state.copy()
                s[col] = row
                h = heuristic(s)
                if h < best:
                    best = h
                    neighbors = [s]
                elif h == best:
                    neighbors.append(s)
        if best >= current:
            return state
        state = random.choice(neighbors)

def simulated_annealing_8_queens(kmax=100000, t0=1.0, cooling_rate=0.00001):
    state = [random.randrange(8) for _ in range(8)]
    def heuristic(s):
        conflicts = 0
        for i in range(8):
            for j in range(i+1, 8):
                if s[i] == s[j] or abs(s[i]-s[j]) == j-i:
                    conflicts += 1
        return conflicts
    t = t0
    for k in range(1, kmax+1):
        if heuristic(state) == 0:
            break
        col = random.randrange(8)
        row = random.randrange(8)
        neighbor = state.copy()
        neighbor[col] = row
        delta = heuristic(neighbor) - heuristic(state)
        if delta < 0 or random.random() < math.exp(-delta/t):
            state = neighbor
        t = t0 / (1 + cooling_rate*k)
    return state
