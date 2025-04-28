from collections import defaultdict, Counter

def read_graph(file_path):
    """
    Reads the graph from the file and constructs an adjacency list.
    Ignores the "Heuristic" column.
    """
    graph = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            source, destination, _ = line.strip().split()
            graph[source].append(destination)
            graph[destination].append(source)  # Since the graph is undirected
    return graph

def read_predefined_colors(file_path):
    """
    Reads predefined colors from the file and stores them in a dictionary.
    Colors are represented as integers.
    """
    predefined_colors = {}
    with open(file_path, 'r') as file:
        for line in file:
            index, color = line.strip().split()
            predefined_colors[index] = int(color)  # Convert color to integer
    return predefined_colors

def generate_initial_state(graph, predefined_colors):
    """
    Generates a random valid initial state using predefined colors.
    Higher-degree vertices are colored first.
    Predefined colors are not changed.
    If predefined colors are exhausted, new colors (integers) are introduced.
    """
    state = {}
    vertices = list(graph.keys())

    # Sort vertices by degree in descending order
    vertices.sort(key=lambda x: len(graph[x]), reverse=True)

    # Start with predefined colors
    available_colors = list(set(predefined_colors.values()))

    # Assign predefined colors first
    for vertex in vertices:
        if vertex in predefined_colors:
            state[vertex] = predefined_colors[vertex]

    # Assign colors to uncolored vertices, starting with higher-degree vertices
    for vertex in vertices:
        if vertex not in state:  # Skip vertices with predefined colors
            # Get colors of adjacent vertices
            adjacent_colors = set()
            for neighbor in graph[vertex]:
                if neighbor in state:
                    adjacent_colors.add(state[neighbor])

            # Get colors of vertices two hops away
            two_hop_colors = set()
            for neighbor in graph[vertex]:
                for two_hop_neighbor in graph[neighbor]:
                    if two_hop_neighbor in state:
                        two_hop_colors.add(state[two_hop_neighbor])

            # Find the smallest available color that is not in adjacent or two-hop colors
            color = 0
            while True:
                if color not in adjacent_colors and color not in two_hop_colors:
                    break
                color += 1

            # Assign the color to the vertex
            state[vertex] = color

            # If the color is new, add it to the available colors list
            if color not in available_colors:
                available_colors.append(color)

    return state, available_colors

def generate_successors(state, graph, predefined_colors):
    """
    Generates successor states by recoloring one vertex at a time.
    Higher-degree vertices are prioritized.
    Predefined colors are not changed.
    Constraints (adjacent and two-hop colors) are respected.
    """
    successors = []
    vertices = list(graph.keys())

    # Sort vertices by degree in descending order
    vertices.sort(key=lambda x: len(graph[x]), reverse=True)

    # Iterate over vertices to generate successors
    for vertex in vertices:
        # Skip vertices with predefined colors
        if vertex in predefined_colors:
            continue

        # Get colors of adjacent vertices
        adjacent_colors = set()
        for neighbor in graph[vertex]:
            if neighbor in state:
                adjacent_colors.add(state[neighbor])

        # Get colors of vertices two hops away
        two_hop_colors = set()
        for neighbor in graph[vertex]:
            for two_hop_neighbor in graph[neighbor]:
                if two_hop_neighbor in state:
                    two_hop_colors.add(state[two_hop_neighbor])

        # Find all valid colors for the current vertex
        valid_colors = []
        color = 0
        while True:
            if color not in adjacent_colors and color not in two_hop_colors:
                valid_colors.append(color)
            color += 1
            if color > max(state.values(), default=0) + 1:
                break  # Stop if no more colors are needed

        # Generate successor states by recoloring the vertex
        for new_color in valid_colors:
            if new_color != state[vertex]:  # Skip if the color is the same
                new_state = state.copy()
                new_state[vertex] = new_color
                successors.append(new_state)

    return successors

def heuristic(state):
    # Count of each color
    color_counts = Counter(state.values())
    
    # Calculate variance of color distribution
    color_usage = list(color_counts.values())
    mean_usage = sum(color_usage) / len(color_usage)
    
    # Variance measures spread of color distribution
    variance = sum((x - mean_usage) ** 2 for x in color_usage) / len(color_usage)
    
    # Number of colors used
    num_colors = len(color_counts)
    
    # lower varience + lover color better
    return num_colors + variance

def local_beam_search(graph, predefined_colors, beam_width=2, max_iterations=100):
    # Generate multiple initial states
    current_states = []
    for i in range(beam_width):
        initial_state, _ = generate_initial_state(graph, predefined_colors)
        current_states.append(initial_state)

    # Track the best state found so far
    best_state = min(current_states, key=heuristic)
    best_score = heuristic(best_state)

    # Print initial states
    print("Initial States:")
    for i, state in enumerate(current_states):
        print(f"State {i + 1}:")
        for vertex, color in state.items():
            print(f"{vertex}: {color}")
        print(f"Heuristic Score: {heuristic(state)}")
    print("\n" + "=" * 50 + "\n")

    for iteration in range(max_iterations):
        new_states = []
        for state in current_states:
            # Generate successors for current state
            local_successors = generate_successors(state, graph, predefined_colors)
            
            if not local_successors:
                new_states.append(state)
                continue

            # Select bestsuccessor
            best_local_successor = min(local_successors, key=heuristic)
            new_states.append(best_local_successor)

        current_states = new_states

        # Update overall best state
        current_best = min(current_states, key=heuristic)
        current_best_score = heuristic(current_best)

        # Print current iteration details
        print(f"Iteration {iteration + 1}:")
        for vertex, color in current_best.items():
            print(f"{vertex}: {color}")
        print(f"Heuristic Score: {current_best_score}")
        print("\n" + "=" * 50 + "\n")

        # Update best state if improved
        if current_best_score < best_score:
            best_state = current_best
            best_score = current_best_score

        # Early stopping if optimal solution found
        if best_score == 0:
            break

    return best_state, best_score

# Main function to execute Local Beam Search
def main():
    # hypercube_dataset_orignal.txt
    graph_file = "hypercube_dataset.txt"
    predefined_colors_file = "predefined_colors.txt"

    # Read the graph and predefined colors
    graph = read_graph(graph_file)
    predefined_colors = read_predefined_colors(predefined_colors_file)

    # Run Local Beam Search
    best_state, best_score = local_beam_search(graph, predefined_colors, beam_width=5, max_iterations=10)

    # Print the final results
    print("Final Best State (Coloring):")
    for vertex, color in best_state.items():
        print(f"{vertex}: {color}")

    print(f"\nFinal Best Heuristic Score: {best_score}")

# Run the program
if __name__ == "__main__":
    main()