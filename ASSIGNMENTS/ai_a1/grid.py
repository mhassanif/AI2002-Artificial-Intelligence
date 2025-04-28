# Hassan Imrman
# 22I-0813
# Section E

def read_and_initialize_obstacles(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        grid_height = int(lines[0].strip())
        
        static_obstacles = set()
        for i, line in enumerate(lines[1:grid_height + 1]):
            for j, cell in enumerate(line.rstrip('\n')):
                if cell == 'X':
                    static_obstacles.add((i, j))
        
        grid_width = max(len(line.rstrip('\n')) for line in lines[1:grid_height + 1])
    
    return grid_height, grid_width, static_obstacles


def is_cell_free(cell, time_step, static_obstacles, agents):
    # Check against static obstacles
    if cell in static_obstacles:
        # print(f'Cell {cell} is an obstacle!')
        return False

    # Check against agents
    for agent in agents.values():
        path = agent['path']
        times = agent['times']
        for i, t in enumerate(times):
            # mod to see if defined time passes
            if t == time_step % len(times):
                if path[i] == cell:
                    return False
    return True