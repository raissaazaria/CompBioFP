# app.py
from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

class GeneticAlgorithm:
    def __init__(self, population_size, gene_length=10):
        self.population_size = population_size
        self.gene_length = gene_length
        self.population = self.initialize_population()

    def initialize_population(self):
        return np.random.randint(2, size=(self.population_size, self.gene_length))

    def fitness(self, individual):
        return np.sum(individual)

    def select_parents(self, fitness_values):
        probabilities = fitness_values / np.sum(fitness_values)
        parents_indices = np.random.choice(range(self.population_size), size=2, p=probabilities)
        return self.population[parents_indices]

    def crossover(self, parent1, parent2):
        crossover_point = np.random.randint(1, self.gene_length)
        child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
        return child1, child2

    def mutate(self, individual, mutation_rate=0.01):
        mutation_mask = np.random.rand(self.gene_length) < mutation_rate
        individual[mutation_mask] = 1 - individual[mutation_mask]
        return individual

    def run(self, generations, mutation_rate):
        for generation in range(generations):
            fitness_values = np.array([self.fitness(individual) for individual in self.population])

            parents = np.array([self.select_parents(fitness_values) for _ in range(self.population_size // 2)])
            parents_flat = parents.reshape(-1, self.gene_length)

            offspring = []
            for i in range(0, len(parents_flat), 2):
                parent1, parent2 = parents_flat[i], parents_flat[i + 1]
                child1, child2 = self.crossover(parent1, parent2)
                offspring.extend([child1, child2])

            # Ensure the length of offspring is equal to the remaining population size
            offspring = offspring[:self.population_size - self.population_size // 2]

            offspring = [self.mutate(child, mutation_rate) for child in offspring]

            parents_half = parents_flat[:self.population_size // 2]
            self.population[:self.population_size // 2] = parents_half.reshape(-1, self.gene_length)

            self.population[self.population_size // 2:] = offspring

            best_individual = self.population[np.argmax(fitness_values)]
            print(f"Generation {generation + 1}, Best Individual: {best_individual}, Fitness: {self.fitness(best_individual)}")

        return best_individual

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for running the genetic algorithm
@app.route('/run_genetic_algorithm', methods=['GET', 'POST'])
def run_genetic_algorithm():
    if request.method == 'POST':
        # Get parameters from the form
        population_size = int(request.form['population_size'])
        generations = int(request.form['generations'])
        mutation_rate = float(request.form['mutation_rate'])

        # Create GeneticAlgorithm instance
        genetic_algorithm = GeneticAlgorithm(population_size=population_size, gene_length=10)

        # Run the genetic algorithm
        best_individual = genetic_algorithm.run(generations, mutation_rate)

        # Convert best_individual to a string for easy passing to the template
        best_individual_str = ''.join(map(str, best_individual))

        # Render the result template with the best individual
        return render_template('result.html', best_individual=best_individual_str)

    # Render the form for input
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
