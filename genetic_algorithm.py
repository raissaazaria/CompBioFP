import numpy as np

class GeneticAlgorithm:
    def __init__(self, population_size, gene_length=10, target_sum=5):
        self.population_size = population_size
        self.gene_length = gene_length
        self.target_sum = target_sum
        self.population = self.initialize_population()

    def initialize_population(self):
        return np.random.randint(2, size=(self.population_size, self.gene_length))

    def fitness(self, individual):
        # Custom fitness function: the closer the sum of genes to the target_sum, the better
        return -abs(np.sum(individual) - self.target_sum)

    def select_parents(self, fitness_values):
        # Roulette wheel selection
        probabilities = fitness_values / np.sum(fitness_values)
        parents_indices = np.random.choice(range(self.population_size), size=2, p=probabilities)
        return self.population[parents_indices]

    def crossover(self, parent1, parent2):
        # Single-point crossover
        crossover_point = np.random.randint(1, self.gene_length)
        child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
        return child1, child2

    def mutate(self, individual, mutation_rate=0.01):
        # Bit-wise mutation
        mutation_mask = np.random.rand(self.gene_length) < mutation_rate
        individual[mutation_mask] = 1 - individual[mutation_mask]
        return individual

    def run(self, generations):
        for generation in range(generations):
            fitness_values = np.array([self.fitness(individual) for individual in self.population])

            # Select parents
            parents = np.array([self.select_parents(fitness_values) for _ in range(self.population_size // 2)])

            # Flatten parents array
            parents_flat = parents.reshape(-1, self.gene_length)

            # Create offspring through crossover
            offspring = []
            for i in range(0, len(parents_flat), 2):
                parent1, parent2 = parents_flat[i], parents_flat[i + 1]
                child1, child2 = self.crossover(parent1, parent2)
                offspring.extend([child1, child2])

            # Mutate offspring
            offspring = [self.mutate(child) for child in offspring]

            # Replace the old generation with the new generation
            parents_half = parents_flat[:self.population_size // 2]
            self.population[:self.population_size // 2] = parents_half.reshape(-1, self.gene_length)

            self.population[self.population_size // 2:] = offspring

            # Find and return the best individual in the current generation
            best_individual = self.population[np.argmax(fitness_values)]
            print(f"Generation {generation + 1}, Best Individual: {best_individual}, Fitness: {self.fitness(best_individual)}")

        return best_individual


