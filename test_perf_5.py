import time
import math
import timeit

def old_flee(dx, dy):
    dist = math.sqrt(dx * dx + dy * dy)
    if dist > 0:
        flee_x = dx / dist * 5
        flee_y = dy / dist * 5
        return flee_x, flee_y

def new_flee(dx, dy):
    dist_sq = dx * dx + dy * dy
    if dist_sq > 0:
        dist = math.sqrt(dist_sq)
        ratio = 5 / dist
        flee_x = dx * ratio
        flee_y = dy * ratio
        return flee_x, flee_y

print("Old flee:", timeit.timeit("old_flee(10, 10)", globals=globals(), number=1000000))
print("New flee:", timeit.timeit("new_flee(10, 10)", globals=globals(), number=1000000))
