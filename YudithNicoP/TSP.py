import numpy as np
import matplotlib.pyplot as plt
import random

# Function to compute Euclidean distance between two points
def compute_euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Function to calculate the total distance of a path
def calculate_total_distance(path, distance_matrix):
    return sum(distance_matrix[path[i], path[i+1]] for i in range(len(path)-1))

# Function to generate the initial population
def generate_initial_population(city_count, population_size):
    return [random.sample(range(city_count), city_count) for _ in range(population_size)]

# Function for parent selection using tournament method
def tournament_selection(population, fitness_scores, k=3):
    tournament = random.sample(list(zip(population, fitness_scores)), k)
    tournament.sort(key=lambda x: x[1])
    return tournament[0][0]

# Function to perform crossover (reproduction)
def crossover(parent1, parent2):
    length = len(parent1)
    p, q = sorted(random.sample(range(length), 2))
    segment = parent1[p:q+1]
    offspring = [city for city in parent2 if city not in segment]
    return offspring[:p] + segment + offspring[p:]

# Function to perform mutation
def mutate(path, mutation_probability):
    if random.random() < mutation_probability:
        i, j = random.sample(range(len(path)), 2)
        path[i], path[j] = path[j], path[i]
    return path

# Main function to run the genetic algorithm
def genetic_algorithm(cities, population_size, num_generations, mutation_probability):
    city_count = len(cities)
    distance_matrix = np.array([[compute_euclidean_distance(c1, c2) for c2 in cities] for c1 in cities])
    population = generate_initial_population(city_count, population_size)
    fitness_scores = [calculate_total_distance(path, distance_matrix) for path in population]
    
    best_fitness = min(fitness_scores)
    best_path = population[fitness_scores.index(best_fitness)]
    
    fitness_history = [best_fitness]
    
    for _ in range(num_generations):
        new_population = []
        for _ in range(population_size):
            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_probability)
            new_population.append(child)
        
        population = new_population
        fitness_scores = [calculate_total_distance(path, distance_matrix) for path in population]
        
        current_best_fitness = min(fitness_scores)
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_path = population[fitness_scores.index(best_fitness)]
        
        fitness_history.append(best_fitness)
    
    return best_path, fitness_history, best_fitness

# Parameters
city_count = 20
population_size = 100
num_generations = 100
mutation_probability = 0.05

# Random city coordinates
np.random.seed(42)
cities = [tuple(coord) for coord in np.random.rand(city_count, 2) * 100]

# Run the genetic algorithm
best_path, fitness_history, best_fitness = genetic_algorithm(cities, population_size, num_generations, mutation_probability)

# Convert distance from arbitrary units to kilometers
# Assume that each unit in the coordinates is 1 km
best_fitness_km = best_fitness

# Display the sorted city coordinates
print("Sorted city coordinates:")
for i in best_path:
    print(f"City {i+1}: {cities[i]}")

# Display the shortest distance in kilometers
print(f"Shortest distance: {best_fitness_km:.2f} km")

# Function to plot the path
def plot_path(path):
    plt.figure(figsize=(10, 6))
    for i in range(len(path) - 1):
        plt.plot([cities[path[i]][0], cities[path[i+1]][0]], [cities[path[i]][1], cities[path[i+1]][1]], 'bo-')
    plt.scatter([city[0] for city in cities], [city[1] for city in cities], color='red')
    plt.title('Shortest Path Map of TSP using Genetic Algorithm')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.show()

# Function to plot the fitness graph
def plot_fitness(fitness_history):
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_history, 'g-', label='Best Fitness per Generation')
    plt.title('Genetic Algorithm Fitness Graph for TSP')
    plt.xlabel('Generation')
    plt.ylabel('Fitness (Smallest Total Distance)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot the shortest path
plot_path(best_path)

# Plot the fitness graph
plot_fitness(fitness_history)
