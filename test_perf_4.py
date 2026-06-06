import time
import math
import timeit

def old_way(dx, dy, speed, dt):
    dist = math.sqrt(dx * dx + dy * dy)
    if dist < 0.01:
        return 0, 0
    else:
        step = min(speed * dt, dist)
        new_x = step * dx / dist
        new_y = step * dy / dist
        return new_x, new_y

def new_way(dx, dy, speed, dt):
    dist_sq = dx * dx + dy * dy
    if dist_sq < 0.0001:
        return 0, 0
    else:
        dist = math.sqrt(dist_sq)
        step = speed * dt
        if step >= dist:
            return dx, dy # actually this means new_x = dx, new_y = dy which is the rest of the path
        else:
            step_ratio = step / dist
            new_x = step_ratio * dx
            new_y = step_ratio * dy
            return new_x, new_y

print("Old:", timeit.timeit("old_way(10, 10, 5, 0.1)", globals=globals(), number=1000000))
print("New:", timeit.timeit("new_way(10, 10, 5, 0.1)", globals=globals(), number=1000000))
