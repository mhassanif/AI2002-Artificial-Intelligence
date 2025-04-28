import random
import pandas as pd
from data import products, shelves ,complementary_pairs



# Precompute Eligible Shelves for Each Product
eligible_shelves_per_product = []
for product in products:
    eligible_shelves = []
    for shelf_id, shelf_info in shelves.items():
        if product["hazardous"]:
            if shelf_info["hazardous"]:
                eligible_shelves.append(shelf_id)
        elif product["perishable"]:
            if shelf_info["refrigerated"]:
                eligible_shelves.append(shelf_id)
        else:
            if not shelf_info["hazardous"] and not shelf_info["refrigerated"]:
                eligible_shelves.append(shelf_id)
    eligible_shelves_per_product.append(eligible_shelves)


# Chromosome Generation
def generate_chromosome():
    return [random.choice(eligible_shelves) for eligible_shelves in eligible_shelves_per_product]


def generate_initial_population(population_size=10):
    return [generate_chromosome() for i in range(population_size)]


# decode representaion for fitness calculation
def decode_chromosome(chromosome):
    """Convert chromosome to shelf-wise product mapping with metadata"""
    shelf_data = {shelf_id: {
        "products": [],
        "product_indices": [], 
        "total_weight": 0,
        "categories": set(),
        "hazardous": False,
        "perishable": False,
        "types": shelves[shelf_id]["type"]
    } for shelf_id in shelves}
    
    for product_idx, shelf_id in enumerate(chromosome):
        product = products[product_idx]
        shelf = shelf_data[shelf_id]
        
        # Update shelf metadata
        shelf["products"].append(product["name"])
        shelf["product_indices"].append(product_idx)  # Store product index
        shelf["total_weight"] += product["weight_kg"]
        shelf["categories"].add(product["category"])
        if product["hazardous"]: shelf["hazardous"] = True
        if product["perishable"]: shelf["perishable"] = True
        
    return shelf_data

def print_decoded_chromosome(chromosome):
    decoded_data = decode_chromosome(chromosome)
    for shelf, data in decoded_data.items():
        print(f"  {shelf}: {data['products']} (Total Weight: {data['total_weight']}kg/{shelves[shelf]['capacity_kg']}kg)")


# Fitness Function
def calculate_fitness(chromosome):
    penalty = 0
    shelf_data = decode_chromosome(chromosome)

    for shelf_id, data in shelf_data.items():
        shelf_info = shelves[shelf_id]

        # Shelf Capacity & Weight Limit
        capacity = shelf_info["capacity_kg"]
        if data["total_weight"] > capacity:
            penalty += (data["total_weight"] - capacity) * 10  # Penalize excess weight

        # Product Category 
        category_count = len(data["categories"])
        if category_count > 1:
            penalty += (category_count - 1) * 5  # Penalize multiple categories

        # Hazardous 
        if shelf_info["hazardous"]:
            # Penalize non-hazardous items in hazardous shelves
            for p_idx in data["product_indices"]:
                if not products[p_idx]["hazardous"]:
                    penalty += 10
        else:
            # Penalize hazardous items in non-hazardous shelves
            for p_idx in data["product_indices"]:
                if products[p_idx]["hazardous"]:
                    penalty += 10


    for product_idx, shelf_id in enumerate(chromosome):
        product = products[product_idx]
        shelf_info = shelves[shelf_id]

        # High-Demand Product Accessibility
        if product["high_demand"] and not shelf_info["high_visibility"]:
            penalty += 8  # Penalize high-demand items not in high-visibility shelves

        # Perishable vs. Non-Perishable Separation
        if product["perishable"] and not shelf_info["refrigerated"]:
            penalty += 15  # Penalize perishables not in refrigerated shelves

        # Restocking Efficiency
        if product["weight_kg"] >= 7 and not shelf_info["lower_shelf"]:
            penalty += 10  # Penalize heavy items not in lower shelves

        # Promotional and Discounted Items Visibility
        if product["discounted"] and not shelf_info["high_visibility"]:
            penalty += 8  # Penalize discounted items not in high-visibility shelves

        # Theft Prevention
        if product["high_theft"] and not shelf_info["secure"]:
            penalty += 10  # Penalize high-theft items not in secure shelves

    # Product Compatibility and Cross-Selling
    # Penalize if complementary products are not placed on the same shelf.
    for p1, p2 in complementary_pairs:
        if chromosome[p1] != chromosome[p2]:
            penalty += 12  # Penalize separated pairs

    # Refrigeration Efficiency
    # Reward solutions that use fewer fridges 
    refrigerated_products = [p_idx for p_idx, product in enumerate(products) if product["perishable"]]
    if len(refrigerated_products) > 0:
        # Get all refrigerated shelves
        refrigerated_shelves = [shelf_id for shelf_id, shelf_info in shelves.items() if shelf_info["refrigerated"]]
    
        # Track which fridges are used
        used_fridges = set()
        for p_idx in refrigerated_products:
            shelf_id = chromosome[p_idx]
            if shelf_id in refrigerated_shelves:
                used_fridges.add(shelf_id)
    
    # Reduce penalty based on the number of fridges used
    penalty -= 10 * (len(refrigerated_shelves) - len(used_fridges))  # Reward for fewer fridges used

    return penalty


# selection for next iteration
def selection(population, fitness_scores, num_parents=5):
    # Select top-performing chromosomes based on fitness scores
    # Combine population and fitness scores
    population_with_fitness = list(zip(population, fitness_scores))
    # Sort by fitness (lower is better)
    population_with_fitness.sort(key=lambda x: x[1])
    # Select top `num_parents` chromosomes
    return [chromosome for chromosome, i in population_with_fitness[:num_parents]]

def crossover(parent1, parent2):
    # Perform crossover between two parents to create two offspring
    # Randomly select a crossover point
    crossover_point = random.randint(1, len(parent1) - 1)
    # Create offspring
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    return offspring1, offspring2


def mutation(chromosome, mutation_rate=0.1):
    # Mutate a chromosome by randomly changing shelf assignments
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            # Randomly reassign to a valid shelf
            chromosome[i] = random.choice(eligible_shelves_per_product[i])
    return chromosome



# Genetic Algorithm Main Loop
def genetic_algorithm(population_size=10, max_iterations=100, mutation_rate=0.1):
    # Generate initial population
    population = generate_initial_population(population_size)
    
    # Track best fitness 
    best_fitness = float("inf")
    no_improvement_count = 0
    
    for iteration in range(max_iterations):
        # Calculate fitness for all chromosomes
        fitness_scores = [calculate_fitness(chromosome) for chromosome in population]
        
        if min(fitness_scores) == 0:
            print(f"Optimal solution found at iteration {iteration}!")
            break
        
        # Update best fitness
        current_best_fitness = min(fitness_scores)
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            no_improvement_count = 0
        else:
            no_improvement_count += 1
        
        # # Stop if no improvement for 10 iterations
        if no_improvement_count >= 10:
            break
        
        # Select parents
        parents = selection(population, fitness_scores)
        
        # Generate next generation
        next_generation = []
        while len(next_generation) < population_size:
            # Randomly select two parents
            parent1, parent2 = random.sample(parents, 2)
            # Perform crossover
            offspring1, offspring2 = crossover(parent1, parent2)
            # Perform mutation
            offspring1 = mutation(offspring1, mutation_rate)
            offspring2 = mutation(offspring2, mutation_rate)
            # Add to next generation
            next_generation.extend([offspring1, offspring2])
        
        # Update population
        population = next_generation[:population_size]
    
    # Return the best solution
    best_index = fitness_scores.index(min(fitness_scores))
    return population[best_index], fitness_scores[best_index]


def save_shelf_allocation_to_excel(chromosome, products, shelves, filename="shelf_allocation.xlsx"):
    # Decode the chromosome to get shelf-wise product mapping
    shelf_data = decode_chromosome(chromosome)
    
    # Create a list to store the allocation data
    allocation_data = []
    
    # Iterate over each shelf and its assigned products
    for shelf_id, data in shelf_data.items():
        for product_idx in data["product_indices"]:
            product = products[product_idx]
            allocation_data.append({
                "Shelf ID": shelf_id,
                "Shelf Type": shelves[shelf_id]["type"],
                "Product ID": f"P{product_idx}",
                "Product Name": product["name"],
                "Product Weight (kg)": product["weight_kg"],
                "Product Category": product["category"],
                "Perishable": product["perishable"],
                "Hazardous": product["hazardous"],
                "High Demand": product["high_demand"],
                "Discounted": product["discounted"],
                "High Theft": product["high_theft"],
                "Shelf Capacity (kg)": shelves[shelf_id]["capacity_kg"],
                "Shelf Total Weight (kg)": data["total_weight"]
            })
    
    # Create a DataFrame from the allocation data
    df = pd.DataFrame(allocation_data)
    
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    # print(f"Shelf allocation saved to {filename}")



def save_shelf_allocation_shelf_by_shelf(chromosome, products, shelves, filename="shelf_allocation.xlsx"):
    # Decode the chromosome to get shelf-wise product mapping
    shelf_data = decode_chromosome(chromosome)
    
    # Create a dictionary to store products for each shelf
    shelf_products = {shelf_id: [] for shelf_id in shelves}
    
    # Populate the dictionary with product names for each shelf
    for shelf_id, data in shelf_data.items():
        for product_idx in data["product_indices"]:
            product_name = products[product_idx]["name"]
            shelf_products[shelf_id].append(product_name)
    
    # Convert the dictionary to a DataFrame
    # Each shelf is a column, and products are listed in rows under the shelf
    df = pd.DataFrame.from_dict(shelf_products, orient="index").transpose()
    
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    # print(f"Shelf allocation saved to {filename}")


if __name__ == "__main__":
    # Run the genetic algorithm
    best_solution, best_fitness = genetic_algorithm(population_size=10, max_iterations=1000, mutation_rate=0.1)
    
    # Print the best solution
    print("\nBest Solution : ")
    print(f"Chromosome: {best_solution}")
    # print(f"Fitness Score: {best_fitness}")
    print_decoded_chromosome(best_solution)

    # Save the shelf allocation to an Excel file
    save_shelf_allocation_to_excel(best_solution, products, shelves, filename="optimized_shelf_allocation.xlsx")

    # Save the shelf allocation to an Excel file (shelf by shelf)
    save_shelf_allocation_shelf_by_shelf(best_solution, products, shelves, filename="shelf_allocation_shelf_by_shelf.xlsx")