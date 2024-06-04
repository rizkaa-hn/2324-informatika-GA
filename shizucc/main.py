# NAMA : ALFI SYIFANA GHOZWY
# NIM : H1D021037


import random
import numpy as np

distances = [
    [0, 94, 76, 141, 91, 60, 120, 145, 91, 74, 90, 55, 145, 108, 41, 49, 33, 151, 69, 111, 24],
    [94, 0, 156, 231, 64, 93, 108, 68, 37, 150, 130, 57, 233, 26, 62, 140, 61, 229, 120, 57, 109],
    [76, 156, 0, 80, 167, 133, 124, 216, 137, 114, 154, 100, 141, 161, 116, 37, 100, 169, 49, 185, 84],
    [141, 231, 80, 0, 229, 185, 201, 286, 216, 139, 192, 178, 113, 239, 182, 92, 171, 155, 128, 251, 137],
    [91, 64, 167, 229, 0, 49, 163, 65, 96, 114, 76, 93, 200, 91, 51, 139, 72, 185, 148, 26, 92],
    [60, 93, 133, 185, 49, 0, 165, 115, 112, 65, 39, 91, 151, 117, 39, 99, 61, 139, 128, 75, 49],
    [120, 108, 124, 201, 163, 165, 0, 173, 71, 194, 203, 74, 254, 90, 127, 136, 104, 269, 75, 163, 144],
    [145, 68, 216, 286, 65, 115, 173, 0, 103, 179, 139, 123, 265, 83, 104, 194, 116, 250, 186, 39, 152],
    [91, 37, 137, 216, 96, 112, 71, 103, 0, 160, 151, 39, 236, 25, 75, 130, 61, 239, 95, 93, 112],
    [74, 150, 114, 139, 114, 65, 194, 179, 160, 0, 54, 127, 86, 171, 89, 77, 99, 80, 134, 140, 50],
    [90, 130, 154, 192, 76, 39, 203, 139, 151, 54, 0, 129, 133, 155, 78, 117, 99, 111, 159, 101, 71],
    [55, 57, 100, 178, 93, 91, 74, 123, 39, 127, 129, 0, 199, 61, 53, 91, 30, 206, 63, 101, 78],
    [145, 233, 141, 113, 200, 151, 254, 265, 236, 86, 133, 199, 0, 251, 171, 118, 176, 46, 182, 226, 125],
    [108, 26, 161, 239, 91, 117, 90, 83, 25, 171, 155, 61, 251, 0, 83, 151, 75, 251, 119, 81, 127],
    [41, 62, 116, 182, 51, 39, 127, 104, 75, 89, 78, 53, 171, 83, 0, 90, 24, 168, 99, 69, 49],
    [49, 140, 37, 92, 139, 99, 136, 194, 130, 77, 117, 91, 118, 151, 90, 0, 80, 139, 65, 159, 50],
    [33, 61, 100, 171, 72, 61, 104, 116, 61, 99, 99, 30, 176, 75, 24, 80, 0, 179, 76, 86, 52],
    [151, 229, 169, 155, 185, 139, 269, 250, 239, 80, 111, 206, 46, 251, 168, 139, 179, 0, 202, 211, 128],
    [69, 120, 49, 128, 148, 128, 75, 186, 95, 134, 159, 63, 182, 119, 99, 65, 76, 202, 0, 161, 90],
    [111, 57, 185, 251, 26, 75, 163, 39, 93, 140, 101, 101, 226, 81, 69, 159, 86, 211, 161, 0, 115],
    [24, 109, 84, 137, 92, 49, 144, 152, 112, 50, 71, 78, 125, 127, 49, 50, 52, 128, 90, 115, 0]
]

cities = [
    "Kota1", "Kota2", "Kota3", "Kota4", "Kota5", "Kota6", "Kota7", "Kota8", "Kota9", "Kota10", 
    "Kota11", "Kota12", "Kota13", "Kota14", "Kota15", "Kota16", "Kota17", "Kota18", "Kota19", "Kota20", "Kota21"
]

POPULATION_SIZE = 100
NUM_GENERATIONS = 500
MUTATION_RATE = 0.01


def initialize_population(pop_size, num_cities):
    population = []
    for _ in range(pop_size):
        individual = list(np.random.permutation(num_cities))
        population.append(individual)
    return population


def calculate_fitness(individual, distances):
    total_distance = 0
    for i in range(len(individual) - 1):
        total_distance += distances[individual[i]][individual[i+1]]
    total_distance += distances[individual[-1]][individual[0]] 
    return total_distance


def tournament_selection(population, fitnesses, k=3):
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]


def order_crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    child[start:end] = parent1[start:end]

    p2_index = end
    c_index = end
    while None in child:
        if parent2[p2_index % len(parent2)] not in child:
            child[c_index % len(child)] = parent2[p2_index % len(parent2)]
            c_index += 1
        p2_index += 1

    return child


def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual


def genetic_algorithm(distances, pop_size, num_generations, mutation_rate):
    num_cities = len(distances)
    population = initialize_population(pop_size, num_cities)
    best_individual = None
    best_fitness = float('inf')

    for generation in range(num_generations):
        fitnesses = [calculate_fitness(ind, distances) for ind in population]


        for ind, fit in zip(population, fitnesses):
            if fit < best_fitness:
                best_fitness = fit
                best_individual = ind

        new_population = []
        for _ in range(pop_size // 2):
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child1 = order_crossover(parent1, parent2)
            child2 = order_crossover(parent2, parent1)
            new_population.extend([child1, child2])

        new_population = [mutate(ind, mutation_rate) for ind in new_population]

        population = new_population

        print(f'Generasi {generation+1} - Solusi Terbaik: {best_fitness}')

    best_route = [cities[i] for i in best_individual]

    return best_route, best_fitness

best_route, best_fitness = genetic_algorithm(distances, POPULATION_SIZE, NUM_GENERATIONS, MUTATION_RATE)

print("NAMA : ALFI SYIFANA GHOZWY")
print("NIM : H1D021037")
print("Solusi terbaik:")
print(" -> ".join(best_route))
print(f"Jarak total: {best_fitness}")
