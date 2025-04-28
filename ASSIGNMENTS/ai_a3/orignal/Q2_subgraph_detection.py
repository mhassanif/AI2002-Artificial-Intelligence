# Description: Solves the "Study Group Dilemma" by reading graph files from the Identification folder
#              (data1.txt, data2.txt, data3.txt), detecting subgraphs (cliques, chains, stars, cycles),
#              and classifying them with priority based on size and lowest node value (e.g., '1' first).
#              Uses DFS, BFS, and heuristics. Handles formats 'src tgt' and 'src, tgt' (no weights).
#              Fixes ValueError in star output, invalid cycles, and chain formatting.
#              Output: Lists subgraphs per file with type, nodes, and size.

import os
import re

def read_graph(filename):
    """
    Reads a graph file into an adjacency list, handling formats 'src tgt' and 'src, tgt'.
    Args:
        filename (str): Path to graph file (e.g., 'Identification/data1.txt').
    Returns:
        dict: Adjacency list {node: [(neighbor, weight), ...]}.
              Undirected graph (adds edges both ways). Weight defaults to 1.0.
    """
    graph = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Try comma and space, or space only
                parts = re.split(r',\s*|\s+', line)
                if len(parts) < 2:
                    continue
                src, tgt = parts[0].strip(','), parts[1].strip(',')  # Remove stray commas
                weight = 1.0  # No weights
                # Initialize nodes
                if src not in graph:
                    graph[src] = []
                if tgt not in graph:
                    graph[tgt] = []
                # Add undirected edges (avoid duplicates)
                if tgt not in [n for n, _ in graph[src]]:
                    graph[src].append((tgt, weight))
                if src not in [n for n, _ in graph[tgt]]:
                    graph[tgt].append((src, weight))
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return graph

def get_node_value(node):
    """
    Extracts a numerical value from a node for prioritization (e.g., '1' -> 1).
    Args:
        node (str): Node identifier (integer as string).
    Returns:
        int: Node value (defaults to 9999 if invalid).
    """
    try:
        return int(node)
    except ValueError:
        return 9999  # High value for non-integer nodes

def calculate_priority(subgraph_nodes, graph, size):
    """
    Calculates priority for a subgraph based on size and minimum node value.
    Priority: Larger size > lower node value (e.g., '1' first).
    Args:
        subgraph_nodes (set/list): Nodes in the subgraph.
        graph (dict): Adjacency list.
        size (int): Subgraph size (nodes for cliques/stars, edges for chains/cycles).
    Returns:
        tuple: (-size, min_node_value) for sorting (lower tuple = higher priority).
    """
    min_node_value = min(get_node_value(node) for node in subgraph_nodes)
    return (-size, min_node_value)

def find_cliques(graph):
    """
    Finds maximal cliques using Bron-Kerbosch algorithm (DFS-based).
    Cliques: Fully connected subgraphs (every node connected to every other).
    Limits cliques to size 3–6.
    Args:
        graph (dict): Adjacency list.
    Returns:
        list: Tuples (clique_set, priority), sorted by priority.
    """
    def bron_kerbosch(R, P, X, cliques):
        """
        Recursive Bron-Kerbosch with pivoting.
        Args:
            R: Current clique nodes.
            P: Possible nodes to add.
            X: Nodes already considered.
            cliques: List to store maximal cliques.
        """
        if len(R) > 6:
            return
        if not P and not X:
            if len(R) >= 3:
                cliques.append(R.copy())
            return
        pivot = max(P | X, key=lambda u: len([v for v, _ in graph.get(u, [])]), default=None)
        if pivot is None:
            pivot_neighbors = set()
        else:
            pivot_neighbors = set(v for v, _ in graph.get(pivot, []))
        for u in P - pivot_neighbors:
            neighbors = set(v for v, _ in graph.get(u, []))
            if len(neighbors) > 15:
                continue
            bron_kerbosch(R | {u}, P & neighbors, X & neighbors, cliques)
            P.remove(u)
            X.add(u)
    
    cliques = []
    nodes = set(graph.keys())
    bron_kerbosch(set(), nodes, set(), cliques)
    prioritized_cliques = []
    for clique in cliques:
        priority = calculate_priority(clique, graph, len(clique))
        prioritized_cliques.append((clique, priority))
    return prioritized_cliques[:20]

def find_chains(graph):
    """
    Finds maximal chains using BFS.
    Chains: Linear paths where internal nodes have degree 2, endpoints degree 1 or dead ends.
    Limits chains to length 2–6.
    Args:
        graph (dict): Adjacency list.
    Returns:
        list: Tuples (chain_list, priority), sorted by priority.
    """
    def bfs_chain(start, visited):
        """
        Finds a chain starting from a node using BFS.
        Args:
            start (str): Starting node.
            visited (set): Nodes already in chains.
        Returns:
            list: Ordered nodes in chain, or None if not a chain.
        """
        queue = [(start, [start])]
        while queue:
            node, path = queue.pop(0)
            if len(path) > 7:
                return None
            neighbors = [n for n, _ in graph.get(node, []) if n not in visited and n not in path]
            degree = len([n for n, _ in graph.get(node, [])])
            if len(path) == 1 and degree <= 2:
                pass
            elif len(path) > 1 and len(neighbors) > 1:
                continue
            elif len(neighbors) == 0 and len(path) >= 3:
                return path
            for neighbor in neighbors:
                if len(graph.get(neighbor, [])) > 5:
                    continue
                queue.append((neighbor, path + [neighbor]))
        return None if len(path) < 3 else path
    
    chains = []
    visited = set()
    for node in sorted(graph.keys(), key=get_node_value):
        if node not in visited and len(graph[node]) <= 2:
            chain = bfs_chain(node, visited)
            if chain:
                chains.append(chain)
                visited.update(chain)
    
    prioritized_chains = []
    for chain in chains:
        priority = calculate_priority(chain, graph, len(chain) - 1)
        prioritized_chains.append((chain, priority))
    prioritized_chains.sort(key=lambda x: x[1])
    return prioritized_chains[:20]

def find_stars(graph):
    """
    Finds stars using a degree-based heuristic.
    Stars: Central node connected to multiple leaves, leaves unconnected to each other.
    Requires 2+ leaves.
    Args:
        graph (dict): Adjacency list.
    Returns:
        list: Tuples (star_dict, priority), sorted by priority.
              star_dict: {'center': node, 'leaves': set(nodes)}.
    """
    stars = []
    for center in graph:
        neighbors = [n for n, _ in graph.get(center, [])]
        if len(neighbors) < 2:
            continue
        leaves = set()
        for leaf in neighbors:
            leaf_neighbors = set(n for n, _ in graph.get(leaf, []))
            if leaf_neighbors == {center}:
                leaves.add(leaf)
        if len(leaves) >= 2:
            stars.append({'center': center, 'leaves': leaves})
    
    prioritized_stars = []
    for star in stars:
        nodes = {star['center']} | star['leaves']
        priority = calculate_priority(nodes, graph, len(star['leaves']) + 1)
        prioritized_stars.append((star, priority))
    prioritized_stars.sort(key=lambda x: x[1])
    return prioritized_stars[:20]

def find_cycles(graph):
    """
    Finds simple cycles using DFS with strict limits.
    Cycles: Closed loops returning to start node.
    Limits cycles to length 3–4, starts from low-value nodes, caps at 20.
    Args:
        graph (dict): Adjacency list.
    Returns:
        list: Tuples (cycle_list, priority), sorted by priority.
    """
    def dfs_cycle(node, parent, start, path, visited, cycles, depth, cycle_count):
        """
        DFS to find cycles starting from a node.
        Args:
            node: Current node.
            parent: Parent node in DFS.
            start: Starting node of cycle.
            path: Current path.
            visited: Nodes in current DFS path.
            cycles: Set of cycle tuples.
            depth: Current recursion depth.
            cycle_count: List tracking number of cycles.
        Returns:
            bool: False if cycle limit reached, else True.
        """
        if cycle_count[0] >= 20:
            return False
        if depth > 4:
            return True
        path.append(node)
        visited.add(node)
        for neighbor, _ in sorted(graph.get(node, []), key=lambda x: get_node_value(x[0])):
            # Only allow cycle to close at start node
            if neighbor == start and len(path) >= 3 and depth >= 2:
                cycle_nodes = tuple(sorted(path) + [start])
                if cycle_nodes not in cycles:
                    cycles.add(cycle_nodes)
                    cycle_count[0] += 1
                if cycle_count[0] >= 20:
                    return False
            elif (neighbor != parent and 
                  neighbor not in visited and 
                  len(graph.get(neighbor, [])) <= 5 and 
                  depth < 4):
                if not dfs_cycle(neighbor, node, start, path, visited, cycles, depth + 1, cycle_count):
                    return False
        path.pop()
        visited.remove(node)
        return True
    
    cycles = set()
    cycle_count = [0]
    nodes = sorted(graph.keys(), key=get_node_value)[:10]
    for node in nodes:
        if len(graph.get(node, [])) > 5:
            continue
        if not dfs_cycle(node, None, node, [], set(), cycles, 0, cycle_count):
            break
    
    cycle_lists = [list(cycle) for cycle in cycles]
    prioritized_cycles = []
    for cycle in cycle_lists:
        priority = calculate_priority(cycle[:-1], graph, len(cycle) - 1)
        prioritized_cycles.append((cycle, priority))
    prioritized_cycles.sort(key=lambda x: x[1])
    return prioritized_cycles[:20]

def process_identification_folder():
    """
    Processes graph files in Identification folder, detecting and classifying subgraphs.
    Handles case-insensitive filenames.
    Returns:
        dict: {filename: {'cliques': [...], 'chains': [...], 'stars': [...], 'cycles': [...]}}
    """
    folder_path = '../data/Identification'
    results = {}
    
    if not os.path.exists(folder_path):
        print(f"Error: {folder_path} not found.")
        return results
    
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            print(f"\nProcessing file: {filename}")
            graph = read_graph(file_path)
            
            if not graph:
                print("No valid graph data found.")
                continue
            
            print("Finding cliques...")
            cliques = find_cliques(graph)
            print("Finding chains...")
            chains = find_chains(graph)
            print("Finding stars...")
            stars = find_stars(graph)
            print("Finding cycles...")
            cycles = find_cycles(graph)
            print(f"Found {len(cycles)} cycles.")
            
            results[filename] = {
                'cliques': cliques,
                'chains': chains,
                'stars': stars,
                'cycles': cycles
            }
            
            print("Subgraphs found:")
            if cliques:
                print("Cliques:")
                for clique, _ in cliques:
                    size = len(clique)
                    nodes = ', '.join(sorted(clique, key=get_node_value))
                    print(f"  Size {size}: {{{nodes}}}")
            if chains:
                print("Chains:")
                for chain, _ in chains:
                    length = len(chain) - 1
                    path = ' -> '.join(str(n) for n in chain)
                    print(f"  Length {length}: {path}")
            if stars:
                print("Stars:")
                for star, _ in stars:
                    size = len(star['leaves']) + 1
                    center = star['center']
                    leaves = ', '.join(sorted(star['leaves'], key=get_node_value))
                    print(f"  Size {size}: Center {center}, Leaves {{{leaves}}}")
            if cycles:
                print("Cycles:")
                for cycle, _ in cycles:
                    length = len(cycle) - 1
                    path = ' -> '.join(str(n) for n in cycle)
                    print(f"  Length {length}: {path}")
            if not (cliques or chains or stars or cycles):
                print("  None found.")
    
    return results

def main():
    """
    Main function to execute subgraph detection and classification.
    """
    print("Study Group Subgraph Detection")
    print("-----------------------------")
    
    results = process_identification_folder()
    
    print("\nSummary:")
    for filename in sorted(results.keys()):
        print(f"{filename}:")
        cliques = len(results[filename]['cliques'])
        chains = len(results[filename]['chains'])
        stars = len(results[filename]['stars'])
        cycles = len(results[filename]['cycles'])
        print(f"  Cliques: {cliques}, Chains: {chains}, Stars: {stars}, Cycles: {cycles}")

if __name__ == "__main__":
    main()