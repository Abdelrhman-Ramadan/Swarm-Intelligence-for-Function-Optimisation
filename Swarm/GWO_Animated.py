from Common_libs import np , plt , FuncAnimation


def GWO_animated(obj_func, bounds, num_wolves=5, max_iterations=100, dim=2, plot_3d=0):
    # Initialize the grey wolves population randomly
    population = np.random.uniform(bounds[0], bounds[1], size=(num_wolves, dim))

    alpha_pos = None
    beta_pos = None
    delta_pos = None
    alpha_score = float('inf')
    beta_score = float('inf')
    delta_score = float('inf')

    if plot_3d == 1:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    else:
        fig, ax = plt.subplots()

    x = np.linspace(bounds[0], bounds[1], 100)
    y = np.linspace(bounds[0], bounds[1], 100)
    X, Y = np.meshgrid(x, y)
    Z = obj_func(np.array([X, Y]))

    # Define the main loop
    def animate(iteration):
        nonlocal population, alpha_pos, beta_pos, delta_pos, alpha_score, beta_score, delta_score
        # Calculate fitness for each wolf in the population
        scores = np.apply_along_axis(obj_func, 1, population)

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
        ax.clear()
        if plot_3d == 1:
            ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)
            ax.scatter(population[:, 0], population[:, 1], obj_func(population.T),
                       color='red', alpha=0.5)
            ax.scatter(alpha_pos[0], alpha_pos[1], obj_func(alpha_pos),
                       color='blue', marker='*', label='Alpha Wolf')
            ax.scatter(beta_pos[0], beta_pos[1], obj_func(beta_pos),
                       color='green', marker='^', label='Beta Wolf')
            ax.scatter(delta_pos[0], delta_pos[1], obj_func(delta_pos),
                       color='yellow', marker='s', label='Delta Wolf')
        else:
            ax.contour(X, Y, Z, levels=20)
            ax.scatter(population[:, 0], population[:, 1], color='red', alpha=0.5)
            ax.scatter(alpha_pos[0], alpha_pos[1], color='blue', marker='*', label='Alpha Wolf')
            ax.scatter(beta_pos[0], beta_pos[1], color='green', marker='^', label='Beta Wolf')
            ax.scatter(delta_pos[0], delta_pos[1], color='yellow', marker='s', label='Delta Wolf')
        ax.legend()
        ax.set_title(f'Iteration {iteration + 1}')

    ani = FuncAnimation(fig, animate, frames=max_iterations, interval=0.1)
    plt.show()

    return alpha_pos, alpha_score
