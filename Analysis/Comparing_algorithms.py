import numpy as np
from Algorithms.gwo_algorithm import GWO
from Algorithms.PSO_algorithm import PSO
from Swarm.Bench_Mark import schwefel_function, bohachevsky_function, ackley_function


def run_func_n_times(func, algo, bounds, n_individuals, n_generations, n=30):
    results_with_seeds = []
    for i in range(n):
        random_seed = np.random.randint(0, 100)
        np.random.seed(random_seed)
        best_position, best_value = algo(func, bounds, n_individuals, n_generations)
        result = (random_seed, best_position, best_value)
        results_with_seeds.append(result)

    # Calculate the mean and std of the analysis
    mean = sum(item[2] for item in results_with_seeds) / len(results_with_seeds)

    # Calculate the squared deviations
    squared_deviations = [(item[2] - mean) ** 2 for item in results_with_seeds]

    # Calculate the mean of squared deviations
    mean_of_squared_deviations = sum(squared_deviations) / len(results_with_seeds)

    # Calculate the standard deviation
    standard_deviation = np.sqrt(mean_of_squared_deviations)

    mean_and_std = (mean, standard_deviation)

    return mean_and_std, results_with_seeds


bounds = {
    'bohachevsky': [bohachevsky_function, (-100, 100), ([0, 0], 0)],
    'ackley_f': [ackley_function, (-32.768, 32.768), ([0, 0], 0)],
    'schwefel': [schwefel_function, (-500, 500), ([420.9687, 420.9687], 0)],
}

n_individuals, n_generations = 400, 100
print(f'Function\t\t\t\t\tPSO\t\t\t\t\t\t\tGWO')
print(f'\t\t\t\t\t\t\tMean\t\tStd\t\t\t\tMean\t\tStd')
for func, value in bounds.items():
    mean_std_pso, results_pso = run_func_n_times(value[0], PSO, value[1], n_individuals, n_generations)
    mean_std_gwo, results_gwo = run_func_n_times(value[0], GWO, value[1], n_individuals, n_generations)
    print(f'{func}\t\t\t\t\t{mean_std_pso[0]:.7f}\t{mean_std_pso[1]:.7f}\t\t{mean_std_gwo[0]:.7f}\t{mean_std_gwo[1]:.7f}')
