import random
import numpy as np
import tsplib95
import time

# Definisi Fungsi Utilitas
def calculate_cost(route, distance_matrix):
    return sum(distance_matrix[route[i], route[i + 1]] for i in range(len(route) - 1)) + distance_matrix[route[-1], route[0]]

def create_distance_matrix(problem):
    nodes = list(problem.get_nodes())
    size = len(nodes)
    distance_matrix = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if i != j:
                distance_matrix[i, j] = problem.get_weight(nodes[i], nodes[j])
    return distance_matrix

# Fungsi Mutasi
def mutate(route, mutation_rate):
    size = len(route)
    for i in range(size):
        if random.random() < mutation_rate:
            j = random.randint(0, size - 1)
            route[i], route[j] = route[j], route[i]
    return route

# Implementasi Operator Crossover MSCX Radius
def mscx_radius(parent1, parent2, distance_matrix, r):
    size = len(parent1)
    offspring = [-1] * size
    current_node = parent1[0]
    offspring[0] = current_node
    visited = {current_node}
    
    for i in range(1, size):
        legitimate_nodes = [node for node in parent1[i:] + parent2[i:] if node not in visited]
        
        if not legitimate_nodes:
            break
        
        if len(legitimate_nodes) > r:
            legitimate_nodes = random.sample(legitimate_nodes, r)
        
        next_node = min(legitimate_nodes, key=lambda x: distance_matrix[current_node, x])
        offspring[i] = next_node
        visited.add(next_node)
        current_node = next_node
    
    for i in range(size):
        if offspring[i] == -1:
            for node in parent1 + parent2:
                if node not in visited:
                    offspring[i] = node
                    visited.add(node)
                    break
    
    return offspring

# Implementasi Operator Crossover RX
def rx_crossover(parent1, parent2, pr):
    size = len(parent1)
    num_cities = int(size * pr / 100)
    offspring1, offspring2 = [-1] * size, [-1] * size
    
    selected_indices = random.sample(range(size), num_cities)
    for i in selected_indices:
        offspring1[i] = parent1[i]
        offspring2[i] = parent2[i]
    
    fill_offspring(offspring1, parent2)
    fill_offspring(offspring2, parent1)
    
    return offspring1, offspring2

def fill_offspring(offspring, parent):
    size = len(parent)
    current_pos = 0
    for i in range(size):
        if parent[i] not in offspring:
            while offspring[current_pos] != -1:
                current_pos += 1
            offspring[current_pos] = parent[i]

# Implementasi Algoritma HRX untuk GA yang Dimodifikasi
def hrx_module(population, distance_matrix, prx, pr, r):
    size = len(population)
    num_prx = int(prx * size / 100)
    num_pr = size - num_prx

    # Membagi populasi menjadi dua bagian
    population1 = population[:num_prx]
    population2 = population[num_prx:]

    new_population = []

    # Bagian pertama untuk RX crossover
    for _ in range(num_prx // 2):
        parent1, parent2 = random.choices(population1, k=2)
        offspring1, offspring2 = rx_crossover(parent1, parent2, pr)
        new_population.extend([offspring1, offspring2])

    # Bagian kedua untuk MSCX Radius crossover
    for _ in range(num_pr // 2):
        parent1, parent2 = random.choices(population2, k=2)
        offspring1 = mscx_radius(parent1, parent2, distance_matrix, r)
        offspring2 = mscx_radius(parent2, parent1, distance_matrix, r)
        new_population.extend([offspring1, offspring2])

    return new_population

# Implementasi Algoritma GA yang Dimodifikasi dengan HRX
def genetic_algorithm(problem, population_size, generations, crossover_rate, mutation_rate, r, prx, pr):
    nodes = list(problem.get_nodes())
    nodes = [node - 1 for node in nodes]  # Mengubah indeks agar dimulai dari 0
    distance_matrix = create_distance_matrix(problem)
    population = [random.sample(nodes, len(nodes)) for _ in range(population_size)]
    
    no_change_gen = 0
    best_cost = float('inf')
    
    for generation in range(generations):
        population.sort(key=lambda x: calculate_cost(x, distance_matrix))
        current_best_cost = calculate_cost(population[0], distance_matrix)

        if current_best_cost < best_cost:
            best_cost = current_best_cost
            no_change_gen = 0
        else:
            no_change_gen += 1
        
        print(f"Generation {generation}: Best Cost = {best_cost}")

        if no_change_gen >= 10:  # Jika tidak ada perubahan dalam 10 generasi
            population = hrx_module(population, distance_matrix, prx, pr, r)
            no_change_gen = 0
        
        new_population = population[:population_size // 2]
        
        while len(new_population) < population_size:
            if random.random() < crossover_rate:
                parent1, parent2 = random.choices(population[:population_size // 2], k=2)
                offspring1, offspring2 = rx_crossover(parent1, parent2, pr)
                new_population.extend([offspring1, offspring2])
            else:
                new_population.append(random.choice(population[:population_size // 2]))
        
        population = [mutate(ind, mutation_rate) for ind in new_population]
    
    best_solution = min(population, key=lambda x: calculate_cost(x, distance_matrix))
    return best_solution, calculate_cost(best_solution, distance_matrix)

# Implementasi MSCX Crossover untuk GA Standar
def mscx_crossover(parent1, parent2, distance_matrix):
    size = len(parent1)
    offspring = [-1] * size
    current_node = parent1[0]
    offspring[0] = current_node
    visited = {current_node}
    
    for i in range(1, size):
        legitimate_nodes = [node for node in parent1[i:] + parent2[i:] if node not in visited]
        
        if not legitimate_nodes:
            break
        
        next_node = min(legitimate_nodes, key=lambda x: distance_matrix[current_node, x])
        offspring[i] = next_node
        visited.add(next_node)
        current_node = next_node
    
    for i in range(size):
        if offspring[i] == -1:
            for node in parent1 + parent2:
                if node not in visited:
                    offspring[i] = node
                    visited.add(node)
                    break
    
    return offspring

# Implementasi GA1: Algoritma Genetika dengan MSCX-Radius
def genetic_algorithm_mscx_radius(problem, population_size, generations, crossover_rate, mutation_rate, r):
    nodes = list(problem.get_nodes())
    nodes = [node - 1 for node in nodes]  # Mengubah indeks agar dimulai dari 0
    distance_matrix = create_distance_matrix(problem)
    population = [random.sample(nodes, len(nodes)) for _ in range(population_size)]
    
    for generation in range(generations):
        population.sort(key=lambda x: calculate_cost(x, distance_matrix))
        best_individual = population[0]
        best_cost = calculate_cost(best_individual, distance_matrix)
        print(f"Generation {generation}: Best Cost = {best_cost}")

        new_population = population[:population_size // 2]
        
        while len(new_population) < population_size:
            if random.random() < crossover_rate:
                parent1, parent2 = random.choices(population[:population_size // 2], k=2)
                offspring1 = mscx_radius(parent1, parent2, distance_matrix, r)
                offspring2 = mscx_radius(parent2, parent1, distance_matrix, r)
                new_population.extend([offspring1, offspring2])
            else:
                new_population.append(random.choice(population[:population_size // 2]))
        
        population = [mutate(ind, mutation_rate) for ind in new_population]
    
    best_solution = min(population, key=lambda x: calculate_cost(x, distance_matrix))
    return best_solution, calculate_cost(best_solution, distance_matrix)

# Implementasi GA2: Algoritma Genetika dengan RX Crossover
def genetic_algorithm_rx(problem, population_size, generations, crossover_rate, mutation_rate, pr):
    nodes = list(problem.get_nodes())
    nodes = [node - 1 for node in nodes]  # Mengubah indeks agar dimulai dari 0
    distance_matrix = create_distance_matrix(problem)
    population = [random.sample(nodes, len(nodes)) for _ in range(population_size)]
    
    for generation in range(generations):
        population.sort(key=lambda x: calculate_cost(x, distance_matrix))
        best_individual = population[0]
        best_cost = calculate_cost(best_individual, distance_matrix)
        print(f"Generation {generation}: Best Cost = {best_cost}")

        new_population = population[:population_size // 2]
        
        while len(new_population) < population_size:
            if random.random() < crossover_rate:
                parent1, parent2 = random.choices(population[:population_size // 2], k=2)
                offspring1, offspring2 = rx_crossover(parent1, parent2, pr)
                new_population.extend([offspring1, offspring2])
            else:
                new_population.append(random.choice(population[:population_size // 2]))
        
        population = [mutate(ind, mutation_rate) for ind in new_population]
    
    best_solution = min(population, key=lambda x: calculate_cost(x, distance_matrix))
    return best_solution, calculate_cost(best_solution, distance_matrix)

def standard_genetic_algorithm(problem, population_size, generations, crossover_rate, mutation_rate):
    nodes = list(problem.get_nodes())
    nodes = [node - 1 for node in nodes]  # Mengubah indeks agar dimulai dari 0
    distance_matrix = create_distance_matrix(problem)
    population = [random.sample(nodes, len(nodes)) for _ in range(population_size)]
    
    for generation in range(generations):
        population.sort(key=lambda x: calculate_cost(x, distance_matrix))
        best_individual = population[0]
        best_cost = calculate_cost(best_individual, distance_matrix)
        print(f"Generation {generation}: Best Cost = {best_cost}")

        new_population = population[:population_size // 2]
        
        while len(new_population) < population_size:
            if random.random() < crossover_rate:
                parent1, parent2 = random.choices(population[:population_size // 2], k=2)
                offspring1 = mscx_crossover(parent1, parent2, distance_matrix)
                offspring2 = mscx_crossover(parent2, parent1, distance_matrix)
                new_population.extend([offspring1, offspring2])
            else:
                new_population.append(random.choice(population[:population_size // 2]))
        
        population = [mutate(ind, mutation_rate) for ind in new_population]
    
    best_solution = min(population, key=lambda x: calculate_cost(x, distance_matrix))
    return best_solution, calculate_cost(best_solution, distance_matrix)

# Fungsi untuk memuat file TSP dari direktori lokal
def load_tsp_file(instance):
    filepath = f'{instance}.tsp'
    return tsplib95.load(filepath)

# Eksekusi dan Perbandingan
instances = ['eil51', 'pr76']
results_ga1 = []
results_ga2 = []
results_ga3 = []
results_cxga = []

for instance in instances:
    problem = load_tsp_file(instance)
    
    cost_ga1_runs = []
    cost_ga2_runs = []
    cost_ga3_runs = []
    cost_cxga_runs = []
    
    for _ in range(3):
        print(f"Running GA1 (MSCX-Radius) for instance {instance}...")
        start_time = time.time()
        _, cost_ga1 = genetic_algorithm_mscx_radius(problem, 100, 500, 0.9, 0.01, 5)
        end_time = time.time()
        cost_ga1_runs.append((cost_ga1, end_time - start_time))
        
        print(f"Running GA2 (RX) for instance {instance}...")
        start_time = time.time()
        _, cost_ga2 = genetic_algorithm_rx(problem, 100, 500, 0.9, 0.01, 10)
        end_time = time.time()
        cost_ga2_runs.append((cost_ga2, end_time - start_time))
        
        print(f"Running GA3 (MSCX) for instance {instance}...")
        start_time = time.time()
        _, cost_ga3 = standard_genetic_algorithm(problem, 100, 500, 0.9, 0.01)
        end_time = time.time()
        cost_ga3_runs.append((cost_ga3, end_time - start_time))
        
        print(f"Running CXGA (Combined) for instance {instance}...")
        start_time = time.time()
        _, cost_cxga = genetic_algorithm(problem, 100, 500, 0.9, 0.01, 5, 0.4, 10)
        end_time = time.time()
        cost_cxga_runs.append((cost_cxga, end_time - start_time))
    
    results_ga1.append({
        'instance': instance,
        'min_cost': min(cost for cost, _ in cost_ga1_runs),
        'mean_cost': np.mean([cost for cost, _ in cost_ga1_runs]),
        'std_dev': np.std([cost for cost, _ in cost_ga1_runs]),
        'mean_time': np.mean([time for _, time in cost_ga1_runs])
    })
    
    results_ga2.append({
        'instance': instance,
        'min_cost': min(cost for cost, _ in cost_ga2_runs),
        'mean_cost': np.mean([cost for cost, _ in cost_ga2_runs]),
        'std_dev': np.std([cost for cost, _ in cost_ga2_runs]),
        'mean_time': np.mean([time for _, time in cost_ga2_runs])
    })
    
    results_ga3.append({
        'instance': instance,
        'min_cost': min(cost for cost, _ in cost_ga3_runs),
        'mean_cost': np.mean([cost for cost, _ in cost_ga3_runs]),
        'std_dev': np.std([cost for cost, _ in cost_ga3_runs]),
        'mean_time': np.mean([time for _, time in cost_ga3_runs])
    })
    
    results_cxga.append({
        'instance': instance,
        'min_cost': min(cost for cost, _ in cost_cxga_runs),
        'mean_cost': np.mean([cost for cost, _ in cost_cxga_runs]),
        'std_dev': np.std([cost for cost, _ in cost_cxga_runs]),
        'mean_time': np.mean([time for _, time in cost_cxga_runs])
    })

print("Results for GA1 (MSCX-Radius):", results_ga1)
print("Results for GA2 (RX):", results_ga2)
print("Results for GA3 (MSCX):", results_ga3)
print("Results for CXGA (Combined):", results_cxga)
