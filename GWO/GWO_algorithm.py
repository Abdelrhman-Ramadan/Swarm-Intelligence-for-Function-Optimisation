import numpy as np


def GWO(obj_func, bounds, num_wolves=5, max_iterations=100):
    # Initialize the grey wolves population randomly
    dim = len(bounds)
    population = np.random.uniform(bounds[0], bounds[1], size=(num_wolves, dim))

    alpha_pos = None
    beta_pos = None
    delta_pos = None
    alpha_score = float('inf')
    beta_score = float('inf')
    delta_score = float('inf')

    # Define the main loop
    for iteration in range(max_iterations):
        # Calculate fitness for each wolf in the population
        scores = obj_func(population)

        # Update alpha, beta, and delta positions
        alpha_index = np.argmin(scores)
        beta_index = np.argsort(scores)[1]
        delta_index = np.argsort(scores)[2]

        if scores[alpha_index] < alpha_score:
            alpha_score = scores[alpha_index]
            alpha_pos = population[alpha_index]
        if scores[beta_index] < beta_score:
            beta_score = scores[beta_index]
            beta_pos = population[beta_index]
        if scores[delta_index] < delta_score:
            delta_score = scores[delta_index]
            delta_pos = population[delta_index]

        # Update the positions of the wolves
        a = 2 - iteration * (2 / max_iterations)  # Linearly decreased from 2 to 0
        r1 = np.random.random((num_wolves, dim))
        r2 = np.random.random((num_wolves, dim))
        A1 = 2 * a * r1 - a
        C1 = 2 * r2
        D_alpha = np.abs(C1 * alpha_pos - population)
        X1 = alpha_pos - A1 * D_alpha

        r1 = np.random.random((num_wolves, dim))
        r2 = np.random.random((num_wolves, dim))
        A2 = 2 * a * r1 - a
        C2 = 2 * r2
        D_beta = np.abs(C2 * beta_pos - population)
        X2 = beta_pos - A2 * D_beta

        r1 = np.random.random((num_wolves, dim))
        r2 = np.random.random((num_wolves, dim))
        A3 = 2 * a * r1 - a
        C3 = 2 * r2
        D_delta = np.abs(C3 * delta_pos - population)
        X3 = delta_pos - A3 * D_delta

        population = (X1 + X2 + X3) / 3

        # Apply boundary constraints
        population = np.clip(population, bounds[0], bounds[1])

    return alpha_pos, alpha_score
