# Hassan Imrman
# 22I-0813
# Section E


def read_agents(file_path):
    agents = {}
    with open(file_path, 'r') as file:
        for line in file:
            path_str, times_str = line.strip().split(' at times ')
            path = [tuple(map(int, pos.strip('()').split(','))) for pos in path_str.split(': ')[1].strip('[]').split('), (')]
            times = list(map(int, times_str.strip('[]').split(', ')))
            agent_id = len(agents) + 1
            agents[agent_id] = {'path': path, 'times': times}
    return agents

