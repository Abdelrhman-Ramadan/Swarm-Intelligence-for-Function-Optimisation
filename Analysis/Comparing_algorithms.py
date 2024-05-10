import numpy as np
from Algorithms.gwo_algorithm import GWO
from Algorithms.PSO_algorithm import PSO
from Swarm.Bench_Mark import schwefel_function, bohachevsky_function, ackley_function
import json
from datetime import datetime
import matplotlib.pyplot as plt


def convert_to_serializable(results):
    return [(item[0], item[1].tolist(), item[2]) for item in results]


def plot_convergence_plots(history_list, algorithm_name):
    # Plot each history list with corresponding label
    for label, history in zip(bounds.keys(), history_list):
        plt.plot(range(len(history)), history, label=label)

    plt.xlabel('Iteration')
    plt.ylabel('Best Fitness Value')
    plt.title(f'Convergence Plots of {algorithm_name}')
    plt.grid(True)
    plt.legend()  # Show legend indicating which line corresponds to which label
    # Add comments showing parameters
    if algorithm_name == 'PSO':
        plot_comment = f"Size={n_individuals}\nw={w}\nc1={c1}\nc2={c2}"
    else:
        plot_comment = f"Size={n_individuals}"
    plt.text(0.9, 0.69, plot_comment, horizontalalignment='center', verticalalignment='center',
             transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))
    plt.show()


def run_func_n_times(func, algo, bounds, n_individuals, n_generations, n=30):
    results_with_seeds = []
    for i in range(n):
        random_seed = np.random.randint(0, 100)
        np.random.seed(random_seed)
        best_position, best_value, best_fitness_history = 0, 0, 0
        if algo == PSO:
            best_position, best_value, best_fitness_history = algo(func, bounds, n_individuals, n_generations, w=w,
                                                                   c1=c1, c2=c2)
        elif algo == GWO:
            best_position, best_value, best_fitness_history = algo(func, bounds, n_individuals, n_generations)
        result = [random_seed, best_position, best_value, best_fitness_history]
        results_with_seeds.append(result)

    # Calculate the mean and std of the analysis
    mean = sum(item[2] for item in results_with_seeds) / len(results_with_seeds)

    # Calculate the squared deviations
    squared_deviations = [(item[2] - mean) ** 2 for item in results_with_seeds]

    # Calculate the mean of squared deviations
    mean_of_squared_deviations = sum(squared_deviations) / len(results_with_seeds)

    # Calculate the standard deviation
    standard_deviation = np.sqrt(mean_of_squared_deviations)

    mean_and_std = [mean, standard_deviation]

    # Convert the fitness history lists in the results_with_seeds list to a numpy array for efficient computation
    fitness_history = np.array([item[3] for item in results_with_seeds])

    # Calculate the mean along the first axis (axis=0) which represents the lists
    mean_best_fitness_history = np.mean(fitness_history, axis=0)

    return mean_and_std, results_with_seeds, mean_best_fitness_history


bounds = {
    'bohachevsky': [bohachevsky_function, (-100, 100), ([0, 0], 0)],
    'ackley  ': [ackley_function, (-32.768, 32.768), ([0, 0], 0)],
    'schwefel': [schwefel_function, (-500, 500), ([420.9687, 420.9687], 0)],
}

# Generate current time as a string to use in the file name
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# File path with the current time as part of the name
file_path = f"Comparing_algorithms_results_{current_time}.json"

# Initializing number of individuals and max_Generations
n_individuals, n_generations = 300, 80
w = 0.5
c1 = 1
c2 = 2
history_pso_list = []
history_gwo_list = []

# Putting a seed for the random number generator
np.random.seed(20)

print(f'Function\t\t\t\t\tPSO\t\t\t\t\t\t\tGWO')
print(f'\t\t\t\t\t\t\tMean\t\tStd\t\t\t\tMean\t\tStd')
for func, value in bounds.items():
    mean_std_pso, results_pso, history_pso = run_func_n_times(value[0], PSO, value[1], n_individuals, n_generations)
    mean_std_gwo, results_gwo, history_gwo = run_func_n_times(value[0], GWO, value[1], n_individuals, n_generations)
    history_pso_list.append(history_pso)
    history_gwo_list.append(history_gwo)
    print(
        f'{func}\t\t\t\t\t{mean_std_pso[0]:.7f}\t{mean_std_pso[1]:.7f}\t\t{mean_std_gwo[0]:.7f}\t{mean_std_gwo[1]:.7f}')

# Open the file in append mode outside the loop
# with open(file_path, 'a') as f:
#     for func, value in bounds.items():
#         mean_std_pso, results_pso, history_pso = run_func_n_times(value[0], PSO, value[1], n_individuals, n_generations)
#         mean_std_gwo, results_gwo, history_gwo = run_func_n_times(value[0], GWO, value[1], n_individuals, n_generations)
#         history_pso_list.append(history_pso)
#         history_gwo_list.append(history_gwo)
#         print(
#             f'{func}\t\t\t\t\t{mean_std_pso[0]:.7f}\t{mean_std_pso[1]:.7f}\t\t{mean_std_gwo[0]:.7f}\t{mean_std_gwo[1]:.7f}')
#         # Create a dictionary to store the data
#         json_data = {
#             'func_name': func,
#             'Algo_1': 'PSO',
#             'PSO_seeds': [item[0] for item in results_pso],
#             'PSO_positions': [item[1].tolist() for item in results_pso],
#             'PSO_values': [item[2] for item in results_pso],
#             'PSO_Mean': mean_std_pso[0],
#             'PSO_Std': mean_std_pso[1],
#             'Algo_2': 'GWO',
#             'GWO_seeds': [item[0] for item in results_gwo],
#             'GWO_positions': [item[1].tolist() for item in results_gwo],
#             'GWO_values': [item[2] for item in results_gwo],
#             'GWO_Mean': mean_std_gwo[0],
#             'GWO_Std': mean_std_gwo[1]
#         }
#         # Write the dictionary to the JSON file
#         json.dump(json_data, f, indent=4)  # Use 'indent' for pretty formatting (optional)
#         f.write('\n')  # Add a newline to separate JSON objects

# Plotting the convergence for PSO and GWO respectively
plot_convergence_plots(history_pso_list, "PSO")
plot_convergence_plots(history_gwo_list, "GWO")
