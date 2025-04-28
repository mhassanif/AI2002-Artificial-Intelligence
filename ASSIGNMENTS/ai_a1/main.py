# Hassan Imrman
# 22I-0813
# Section E

import time
import os
from grid import read_and_initialize_obstacles,is_cell_free
from robot import read_robots
from agent import read_agents
from robot import Robot
from collision import detect_robot_collisions,get_random_direction

def display_grid_with_obstacles(grid_height, grid_width, static_obstacles, agents, robots, timestamp):
    for i in range(grid_height):
        for j in range(grid_width):
            if (i, j) in static_obstacles:
                print('X', end=' ')
            elif not is_cell_free((i, j), timestamp, static_obstacles, agents):
                print('A', end=' ')
            elif any(robot.current == (i, j) for robot in robots):
                print('R', end=' ')
            else:
                print('.', end=' ')
        print()

def main():
    grid_height, grid_width, static_obstacles = read_and_initialize_obstacles(
        'Data/data0.txt')
    agents = read_agents(
        'Data/Agent0.txt')
    robot_data = read_robots(
        'Data/Robots0.txt')
    
    # print(agents)
    
    # Create robot instances
    robots = [Robot(data['start'], data['goal'],static_obstacles,grid_width,grid_height,agents) for data in robot_data]

    timestamp = 0

    # plan paths before time starts
    for robot in robots:
        robot.plan_path(grid_height, grid_width, static_obstacles, agents, timestamp)

    while True:
        os.system('cls')
        
        for robot in robots:
            print("Robot @ ",robot.current)
            robot.move()
        
        # Check for collisions
        collisions = detect_robot_collisions(robots)
        for colliding_robots in collisions:
            print(f'Collision detected between robots at position {colliding_robots[0].current}')
            for robot in colliding_robots:
                robot.handle_collision(grid_height, grid_width, static_obstacles, agents, timestamp,get_random_direction())
        
        # Display current state
        # display_grid_with_obstacles(grid_height, grid_width, static_obstacles, agents, robots, timestamp)
        
        # Check if all robots have reached their goals
        if all(robot.is_done() for robot in robots):
            for robot in robots:
                robot.display_path_and_time()
            break
        
        # time.sleep(1)
        timestamp += 1

if __name__ == "__main__":
    main()

