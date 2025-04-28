# Hassan Imrman
# 22I-0813
# Section E

import random

def detect_robot_collisions(robots):
    """Detect if any robots occupy the same cell."""
    positions = {}
    for robot in robots:
        if robot.current in positions:
            # already a robot at this position
            positions[robot.current].append(robot)
        else:
            # first robot at this position
            positions[robot.current] = [robot]
    
    # all the list where more than one robot is present agaist a key
    return [robots for robots in positions.values() if len(robots) > 1]

def get_random_direction():
    """Return a random direction for robot movement."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    return random.choice(directions)