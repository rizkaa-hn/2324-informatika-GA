import numpy as np
import matplotlib.pyplot as plt
import random

# Fungsi untuk menghitung jarak Euclidean antara dua titik
def euclidean_distance(city1, city2):
    return np.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

# Fungsi untuk menghitung total jarak tur
def total_distance(tour, distance_matrix):
    return sum(distance_matrix[tour[i], tour[i+1]] for i in range(len(tour)-1))

# Fungsi untuk membuat populasi awal
def create_initial_population(num_cities, population_size):
    return [random.sample(range(num_cities), num_cities) for _ in range(population_size)]

# Fungsi untuk seleksi orang tua menggunakan metode tournament
def tournament_selection(population, scores, k=3):
    tournament = random.sample(list(zip(population, scores)), k)
    tournament.sort(key=lambda x: x[1])
    return tournament[0][0]

# Fungsi untuk melakukan crossover (reproduksi)
def crossover(parent1, parent2):
    size = len(parent1)
    p, q = sorted(random.sample(range(size), 2))
    temp = parent1[p:q+1]
    child = [city for city in parent2 if city not in temp]
    return child[:p] + temp + child[p:]

# Fungsi untuk melakukan mutasi
def mutate(tour, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour

# Fungsi utama untuk menjalankan algoritma genetika
def genetic_algorithm(cities, population_size, num_generations, mutation_rate):
    num_cities = len(cities)
    distance_matrix = np.array([[euclidean_distance(c1, c2) for c2 in cities] for c1 in cities])
    population = create_initial_population(num_cities, population_size)
    scores = [total_distance(tour, distance_matrix) for tour in population]
    
    best_score = min(scores)
    best_tour = population[scores.index(best_score)]
    
    fitness_history = [best_score]
    
    for _ in range(num_generations):
        new_population = []
        for _ in range(population_size):
            parent1 = tournament_selection(population, scores)
            parent2 = tournament_selection(population, scores)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
        scores = [total_distance(tour, distance_matrix) for tour in population]
        
        current_best_score = min(scores)
        if current_best_score < best_score:
            best_score = current_best_score
            best_tour = population[scores.index(best_score)]
        
        fitness_history.append(best_score)
    
    return best_tour, fitness_history, best_score

# Parameter
num_cities = 20
population_size = 100
num_generations = 100
mutation_rate = 0.05

# Koordinat kota secara acak
np.random.seed(42)
cities = [tuple(coord) for coord in np.random.rand(num_cities, 2) * 100]

# Jalankan algoritma genetika
best_tour, fitness_history, best_score = genetic_algorithm(cities, population_size, num_generations, mutation_rate)

# Konversi jarak dari unit arbitrer ke kilometer
# Misal kita anggap bahwa setiap unit pada koordinat adalah 1 km
best_score_km = best_score

# Tampilkan koordinat kota yang telah diurutkan
print("Koordinat kota yang telah diurutkan:")
for i in best_tour:
    print(f"Kota {i+1}: {cities[i]}")

# Tampilkan jarak terpendek dalam satuan km
print(f"Jarak terpendek: {best_score_km:.2f} km")

# Fungsi untuk memplot tur
def plot_tour(tour):
    plt.figure(figsize=(10, 6))
    for i in range(len(tour) - 1):
        plt.plot([cities[tour[i]][0], cities[tour[i+1]][0]], [cities[tour[i]][1], cities[tour[i+1]][1]], 'bo-')
    plt.scatter([city[0] for city in cities], [city[1] for city in cities], color='red')
    plt.title('Peta Jalur Terpendek TSP dengan Algoritma Genetika')
    plt.xlabel('X Koordinat')
    plt.ylabel('Y Koordinat')
    plt.grid(True)
    plt.show()

# Fungsi untuk memplot grafik fitness
def plot_fitness(fitness_history):
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_history, 'g-', label='Fitness Terbaik per Generasi')
    plt.title('Grafik Fitness Algoritma Genetika untuk TSP')
    plt.xlabel('Generasi')
    plt.ylabel('Fitness (Jarak Total Terkecil)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Memplot jalur terpendek
plot_tour(best_tour)

# Memplot grafik fitness
plot_fitness(fitness_history)