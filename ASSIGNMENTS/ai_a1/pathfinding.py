# Hassan Imrman
# 22I-0813
# Section E

from heapq import heappush, heappop
from grid import is_cell_free

# manhattan distance to estimate cost
# wen movement only 4 directions :  dx + dy
def heuristic(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

# return valid neighbors
def get_neighbors(pos, grid_height, grid_width):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    neighbors = []
    for dx, dy in directions:
        new_x, new_y = pos[0] + dx, pos[1] + dy
        if 0 <= new_x < grid_height and 0 <= new_y < grid_width:
            neighbors.append((new_x, new_y))
    return neighbors

def a_star_search(start, goal, grid_height, grid_width, static_obstacles, agents, current_time):
    # min heap for unexplored nodes
    open_set = [(0, current_time, start)]  # (f_score, time, position)
    came_from = {}

    # shortest known paths cost from the start to current
    g_score = {(start, current_time): 0}
    # estimated cost from start to goal through current (g_score + heuristic)
    f_score = {(start, current_time): heuristic(start, goal)}

    # expolre nodes till goal is reached
    while open_set:
        # Get node with minimum f_score i.e., highest priority
        score, current_time, current = heappop(open_set)

        if current == goal:
            # Reconstruct path
            path = []
            current_state = (current, current_time)
            while current_state in came_from:
                # add current position to path
                path.append(current_state[0])
                # move to previous position
                current_state = came_from[current_state]
            path.append(start)
            return list(reversed(path)), current_time

        # Check each neighbor
        for next_pos in get_neighbors(current, grid_height, grid_width):
            next_time = current_time + 1

            # Skip if cell is obstaclt (static or dynamic)
            if not is_cell_free(next_pos, next_time, static_obstacles, agents):
                continue

            # compute cost of moving to this neighbor
            tentative_g_score = g_score[(current, current_time)] + 1
            next_state = (next_pos, next_time)

            # Update if new path is better than previous path for this neighbor
            if next_state not in g_score or tentative_g_score < g_score[next_state]:
                # Update path
                came_from[next_state] = (current, current_time)
                # Update cost to reach this neighbor from start
                g_score[next_state] = tentative_g_score
                # Update estimated cost to reach goal using this path
                f_score[next_state] = tentative_g_score + heuristic(next_pos, goal)
                # Add this node to unexplored nodes
                heappush(open_set, (f_score[next_state], next_time, next_pos))

    print("returning no path")
    return None, None  # No path found