# Hassan Imrman
# 22I-0813
# Section E


import random
from pathfinding import a_star_search
from collision import get_random_direction
from grid import is_cell_free

class Robot:
    def __init__(self, start, goal, static_obstacles,grid_width,grid_height,agents):

        while not is_cell_free(start,0,static_obstacles,agents):
            start = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
            print("New start  " , start)
            
        self.start = start
        self.goal = goal
        self.current = start
        self.path = []
        self.total_time = 0
        self.save_path = [start]  
        self.collision_count = 0
        self.noPath = False


    def handle_collision(self, grid_height, grid_width, static_obstacles, agents, current_time, direction):
        # random direction and replan path
        self.collision_count += 1
        self.current = (self.current[0]+direction[0],self.current[1]+direction[1])
        print("Collision! Changing Direction!")
        self.path = [] #reset path
        #plan the path again
        success = self.plan_path(grid_height, grid_width, static_obstacles, agents, current_time)
        if not success:
            print(f'Robot at {self.current} failed to find new path after collision')
            
        return success

    def move(self):
        if self.path and not self.is_done():
            next_pos = self.path.pop(0)
            self.current = next_pos
            self.save_path.append(next_pos)
            return True
        return False

    def plan_path(self, grid_height, grid_width, static_obstacles, agents, current_time):


        if self.goal in static_obstacles:
            self.path = []
            self.noPath = True
            return False
        
        # Plan path using A* algorithm
        path, total_time = a_star_search(
            self.current,
            self.goal,
            grid_height,
            grid_width,
            static_obstacles,
            agents,
            current_time
        )
        
        if path:
            self.path = path[1:]  # Exclude current position
            self.total_time = total_time
            return True
        
        if not path:
            print("Robot can't find path!")
            self.noPath = True
            return False

    def is_done(self):
        # reached goal or no path
        return self.current == self.goal or self.noPath == True

    def display_path_and_time(self):
        if self.noPath:
            print(f'Robot path: No Path')
        else :
            print(f'Robot path: {self.save_path}')
            print(f'Total time taken: {self.total_time}')
            print(f'Number of collisions: {self.collision_count}')


def read_robots(file_path):
    robots = []
    with open(file_path, 'r') as file:
        for line in file:
            start, goal = line.strip().split(' End ')
            start = tuple(map(int, start.split('Start ')[1].strip('()').split(',')))
            goal = tuple(map(int, goal.strip('()').split(',')))
            robots.append({'start': start, 'goal': goal, 'current': start})
    return robots