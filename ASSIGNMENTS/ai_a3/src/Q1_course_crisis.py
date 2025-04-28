
def read_swap_requests(filename):
    """
    Reads swap requests, filtering invalid cases.
    Input format: roll current_course current_section desired (e.g., '21i-6085 CC-A A CN-A').
    Args:
        filename (str): Path to input file.
    Returns:
        list: Dicts with 'roll', 'current_course', 'current_section', 'desired'.
              Skips requests where desired equals current_section or current_course.
    """
    requests = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 4:
                    roll, current_course, current_section, desired = parts
                    if desired == current_section or desired == current_course:
                        continue
                    requests.append({
                        'roll': roll,
                        'current_course': current_course,
                        'current_section': current_section,
                        'desired': desired
                    })
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return requests

def get_year(roll):
    """
    Extracts year from roll number.
    Args:
        roll (str): Roll number (e.g., '21i-6085').
    Returns:
        int: Year (e.g., 21).
    """
    return int(roll.split('-')[0].replace('i', ''))

def prioritize_requests(requests):
    """
    Sorts requests by year to prioritize older students.
    Uses selection sort to avoid built-in sorting.
    Args:
        requests (list): Request dicts.
    Returns:
        list: Sorted requests by ascending year.
    """
    sorted_requests = []
    requests_copy = requests.copy()
    while requests_copy:
        min_idx = 0
        for j in range(1, len(requests_copy)):
            if get_year(requests_copy[j]['roll']) < get_year(requests_copy[min_idx]['roll']):
                min_idx = j
        sorted_requests.append(requests_copy.pop(min_idx))
    return sorted_requests

def is_valid_swap(req1, req2):
    """
    Checks if two requests form a valid direct swap.
    Valid if:
    - Course-section swap (e.g., 'OS-A' <-> 'CC-B').
    - Same course, section swap (e.g., 'CN-A' <-> 'CN-B').
    Args:
        req1, req2 (dict): Student requests.
    Returns:
        bool: True if valid.
    """
    if req1['roll'] == req2['roll']:
        return False
    if '-' in req1['desired'] and '-' in req2['desired']:
        return (req1['desired'] == req2['current_course'] and 
                req2['desired'] == req1['current_course'])
    course1 = req1['current_course'].split('-')[0]
    course2 = req2['current_course'].split('-')[0]
    if course1 == course2:
        return (req1['desired'] == req2['current_section'] and 
                req2['desired'] == req1['current_section'])
    return False

def can_swap_to(req1, req2):
    """
    Checks if req1 can swap to req2's course-section (one-way).
    Args:
        req1, req2 (dict): Student requests.
    Returns:
        bool: True if req1 wants req2's course-section.
    """
    if req1['roll'] == req2['roll']:
        return False
    if '-' in req1['desired']:
        return req1['desired'] == req2['current_course']
    course1 = req1['current_course'].split('-')[0]
    course2 = req2['current_course'].split('-')[0]
    return course1 == course2 and req1['desired'] == req2['current_section']

def find_swap_chains(requests, start_idx, chain, visited_rolls, all_chains, max_depth=2):
    """
    DFS to find swap chains (e.g., A -> B -> A), limited to max_depth.
    Args:
        requests (list): Prioritized requests.
        start_idx (int): Starting student index.
        chain (list): List of request dicts in chain.
        visited_rolls (set): Students in current chain to avoid loops.
        all_chains (list): Collects valid chains.
        max_depth (int): Max chain length (2 for efficiency).
    """
    if len(chain) > max_depth:
        return
    
    start_req = requests[start_idx]
    current_req = chain[-1]
    
    for i in range(len(requests)):
        req2 = requests[i]
        if req2['roll'] in visited_rolls:
            if req2['roll'] == start_req['roll'] and len(chain) >= 2:
                all_chains.append(chain)
            continue
        if can_swap_to(current_req, req2):
            find_swap_chains(requests, start_idx, chain + [req2],
                            visited_rolls | {req2['roll']}, all_chains, max_depth)

def find_swaps(requests):
    """
    Finds the best swap (direct or chain) for each student, allowing multiple swaps if optimal.
    Args:
        requests (list): Prioritized requests.
    Returns:
        list: Tuples (roll1, roll2, course1, desired1, course2, desired2).
    """
    student_swaps = {}  # Maps roll to list of possible swaps
    
    # Collect direct swaps
    for i in range(len(requests)):
        req1 = requests[i]
        roll1 = req1['roll']
        if roll1 not in student_swaps:
            student_swaps[roll1] = []
        for j in range(len(requests)):
            if i == j:
                continue
            req2 = requests[j]
            if is_valid_swap(req1, req2):
                roll2 = req2['roll']
                swap = [(roll1, roll2, 
                        req1['current_course'], req1['desired'],
                        req2['current_course'], req2['desired'])]
                student_swaps[roll1].append({
                    'type': 'direct',
                    'swap': swap,
                    'students': {roll1, roll2},
                    'weight': 2,
                    'priority': min(get_year(roll1), get_year(roll2))
                })
    
    # Collect chains
    for i in range(len(requests)):
        req1 = requests[i]
        roll1 = req1['roll']
        if roll1 not in student_swaps:
            student_swaps[roll1] = []
        all_chains = []
        find_swap_chains(requests, i, [req1], {roll1}, all_chains, max_depth=2)
        for chain in all_chains[:5]:  # Limit to 5 chains per student
            chain_swaps = []
            chain_students = set(req['roll'] for req in chain)
            for k in range(len(chain) - 1):
                roll_a = chain[k]['roll']
                roll_b = chain[k + 1]['roll']
                chain_swaps.append((roll_a, roll_b, 
                                   chain[k]['current_course'], chain[k]['desired'],
                                   chain[k + 1]['current_course'], chain[k + 1]['desired']))
            # Close chain
            roll_a = chain[-1]['roll']
            roll_b = chain[0]['roll']
            chain_swaps.append((roll_a, roll_b, 
                               chain[-1]['current_course'], chain[-1]['desired'],
                               chain[0]['current_course'], chain[0]['desired']))
            # Add to each student in chain
            for req in chain:
                roll = req['roll']
                if roll not in student_swaps:
                    student_swaps[roll] = []
                student_swaps[roll].append({
                    'type': 'chain',
                    'swap': chain_swaps,
                    'students': chain_students,
                    'weight': len(chain),
                    'priority': min(get_year(req['roll']) for req in chain)
                })
    
    # Select best swap for each student
    def sort_key(swap):
        return (-swap['weight'], swap['priority'])
    
    swaps = []
    for roll in student_swaps:
        if not student_swaps[roll]:
            continue
        # Sort swaps by weight (descending) and priority (ascending)
        best_swap = student_swaps[roll][0]
        min_score = sort_key(best_swap)
        for swap in student_swaps[roll][1:]:
            score = sort_key(swap)
            if score < min_score:
                min_score = score
                best_swap = swap
        swaps.extend(best_swap['swap'])
    
    return swaps

def process_swapping_folder():
    """
    Processes .txt files in Swapping folder independently.
    Displays the best swap for each student, allowing multiple swaps if optimal.
    Chains are printed in one line (e.g., A -> B -> C -> A).
    Returns:
        list: Tuples (roll1, roll2) for all unique swaps across files.
    """
    import os
    folder_path = '../data/Swapping'
    total_swaps = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            print(f"\nProcessing file: {filename}")
            
            requests = read_swap_requests(file_path)
            if not requests:
                print("No requests found.")
                continue
            
            prioritized_requests = prioritize_requests(requests)
            swaps = find_swaps(prioritized_requests)
            
            if swaps:
                print("Swaps found:")
                file_swaps = []
                
                # Build adjacency list to detect chains
                graph = {}
                for roll1, roll2, course1, desired1, course2, desired2 in swaps:
                    if roll1 not in graph:
                        graph[roll1] = []
                    graph[roll1].append((roll2, course1, desired1, course2, desired2))
                
                # Find chains (cycles) using DFS
                def find_cycle(start, current, path, visited):
                    for next_roll, c1, d1, c2, d2 in graph.get(current, []):
                        if next_roll in visited:
                            if next_roll == start and len(path) >= 2:
                                cycle = path + [(next_roll, c1, d1, c2, d2)]
                                return cycle
                            continue
                        visited.add(next_roll)
                        result = find_cycle(start, next_roll, path + [(current, c1, d1, c2, d2)], visited)
                        if result:
                            return result
                        visited.remove(next_roll)
                    return None
                
                # Process swaps to print chains in one line
                printed_swaps = set()
                for roll1, roll2, course1, desired1, course2, desired2 in swaps:
                    swap_pair = (roll1, roll2)
                    if swap_pair in printed_swaps or (roll2, roll1) in printed_swaps:
                        continue
                    # Try to find a cycle starting from roll1
                    cycle = find_cycle(roll1, roll1, [], {roll1})
                    if cycle and len(cycle) > 2:  # Chain with 3+ students
                        # Print chain in one line
                        cycle_str = " -> ".join(
                            f"{roll} ({c1} -> {d1})" for roll, c1, d1, _, _ in cycle
                        ) + f" -> {cycle[0][0]} ({cycle[0][1]} -> {cycle[0][2]})"
                        print(cycle_str)
                        # Mark all swaps in cycle as printed
                        for i in range(len(cycle) - 1):
                            r1 = cycle[i][0]
                            r2 = cycle[i + 1][0]
                            printed_swaps.add((r1, r2))
                            if (r1, r2) not in file_swaps and (r2, r1) not in file_swaps:
                                file_swaps.append((r1, r2))
                        # Add closing swap
                        r1 = cycle[-1][0]
                        r2 = cycle[0][0]
                        printed_swaps.add((r1, r2))
                        if (r1, r2) not in file_swaps and (r2, r1) not in file_swaps:
                            file_swaps.append((r1, r2))
                    else:
                        # Direct swap
                        print(f"{roll1} ({course1} -> {desired1}) <-> "
                              f"{roll2} ({course2} -> {desired2})")
                        printed_swaps.add(swap_pair)
                        if swap_pair not in file_swaps and (roll2, roll1) not in file_swaps:
                            file_swaps.append(swap_pair)
                
                total_swaps.extend(file_swaps)
            else:
                print("No valid swaps found.")
    
    return total_swaps

def main():
    """
    Executes the solution.
    """
    print("Course Crisis Solution")
    print("---------------------")
    
    swaps = process_swapping_folder()
    
    print("\nSummary:")
    print(f"Total swaps performed: {len(swaps)}")
    if swaps:
        print("All swaps:")
        for roll1, roll2 in swaps:
            print(f"  {roll1} <-> {roll2}")

if __name__ == "__main__":
    main()