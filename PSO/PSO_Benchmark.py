import numpy as np
from PSO_algorithm import PSO
# import GWO
# from GWO_animated import GWO_animated


def bohachevsky_function(x):
    return x[0] ** 2 + 2 * x[1] ** 2 - 0.3 * np.cos(3 * np.pi * x[0]) - 0.4 * np.cos(4 * np.pi * x[1]) + 0.7


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


def rastrigin_function(x):
    A = 10
    return A * 2 + (x[0] ** 2 - A * np.cos(2 * np.pi * x[0])) + (x[1] ** 2 - A * np.cos(2 * np.pi * x[1]))


def schwefel_function(x):
    d = x.shape[0]
    sum = x[0] * np.sin(np.sqrt(np.abs(x[0]))) + x[1] * np.sin(np.sqrt(np.abs(x[1])))
    return 418.9829 * d - sum


def himmelblau_function(x):
    return (x[0] ** 2 + x[1] - 11) ** 2 + (x[0] + x[1] ** 2 - 7) ** 2


# Define the bounds, number of particles, and number of iterations
bounds = (-10, 10)  # Example bounds for two variables
n_particles = 40
n_iterations = 400

# np.random.seed(20)
# Call the PSO function
best_position, best_value = PSO(himmelblau_function, bounds, n_particles, n_iterations)

print("Best position:", best_position)
print("Best value: {:f}".format(best_value))
