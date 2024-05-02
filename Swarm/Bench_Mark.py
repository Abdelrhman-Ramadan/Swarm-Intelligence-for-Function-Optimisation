from Algorithms.gwo_algorithm import GWO
from Swarm.GWO_Animated import GWO_animated
from Swarm.PSO_Animated import PSO_animated
from Swarm.Common_libs import np, plt, FuncAnimation


# (-100, 100)
def bohachevsky_function(x):
    return x[0] ** 2 + 2 * x[1] ** 2 - 0.3 * np.cos(3 * np.pi * x[0]) - 0.4 * np.cos(4 * np.pi * x[1]) + 0.7


# (-32.768, 32.768)
def ackley_function(x):
    a = 20
    b = 0.2
    c = 2 * np.pi
    sum1 = x[0] ** 2 + x[1] ** 2
    sum2 = np.cos(c * x[0]) + np.cos(c * x[1])
    term1 = -a * np.exp(-b * np.sqrt(0.5 * sum1))
    term2 = -np.exp(0.5 * sum2)
    result = term1 + term2 + a + np.exp(1)
    return result


# (-500, 500)
def schwefel_function(x):
    d = x.shape[0]
    sum = x[0] * np.sin(np.sqrt(np.abs(x[0]))) + x[1] * np.sin(np.sqrt(np.abs(x[1])))
    return 418.9829 * d - sum


# (-5,5)
def himmelblau_function(x):
    return (x[0] ** 2 + x[1] - 11) ** 2 + (x[0] + x[1] ** 2 - 7) ** 2


# Define the bounds, number of particles, and number of iterations
# bounds = (-500, 500)  # Example bounds for two variables
#
# n_individuals = 400
# n_generations = 500
# bench_mark = bohachevsky_function
# algorithm = GWO_animated
#
# # best_position, best_value = algorithm(schwefel_function, bounds, n_individuals, n_generations, plot_3d=1)
# best_position, best_value = PSO_animated(schwefel_function, bounds, n_individuals, n_generations, plot_3d=1)
# #
# print("Best position:", best_position)
# print("Best value: {:f}".format(best_value))

# bench mark
# n_individuals
# generations
# algorithm
