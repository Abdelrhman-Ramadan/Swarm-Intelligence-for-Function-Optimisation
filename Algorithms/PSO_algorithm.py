import numpy as np


def PSO(objective_function, bounds, n_particles, n_iterations, d=2, clip=0):
    # Initializing the PSO weights
    inertia_weight = 0.5  # w
    cognitive_weight = 1  # c_1
    social_weight = 2  # c_2

    # Initializing the particles with random positions and velocities within the bounds
    particles_positions = np.random.uniform(bounds[0], bounds[1], (n_particles, d))
    particles_velocity = np.zeros((n_particles, d))

    # Initializing the local best position
    local_best_positions = np.copy(particles_positions)
    local_best_fitness = np.array([objective_function(pos) for pos in particles_positions])

    # Initializing the global best position
    global_best_position = particles_positions[np.argmin(local_best_fitness)]
    global_best_fitness = objective_function(global_best_position)

    for _ in range(n_iterations):
        r1, r2 = np.random.uniform(0, 1, (n_particles, d)), np.random.uniform(0, 1, (n_particles, d))
        # Updating the velocity
        particles_velocity = (inertia_weight * particles_velocity +  # Momentum part
                              cognitive_weight * r1 * (local_best_positions - particles_positions) +  # Cognitive part
                              social_weight * r2 * (global_best_position - particles_positions))  # Social part
        # Updating the position
        particles_positions += particles_velocity

        # Clipping the positions to be within the bounds
        if clip == 1:
            particles_positions = np.clip(particles_positions, bounds[0], bounds[1])

        # Calculating particles fitness values
        current_fitness_values = np.array([objective_function(p) for p in particles_positions])

        # Updating the local best position
        improved_particles_indices = np.where(current_fitness_values < local_best_fitness)
        local_best_positions[improved_particles_indices] = particles_positions[improved_particles_indices]
        local_best_fitness[improved_particles_indices] = current_fitness_values[improved_particles_indices]

        # Updating the global best position
        if np.min(current_fitness_values) < global_best_fitness:
            global_best_position = particles_positions[np.argmin(current_fitness_values)]
            global_best_fitness = np.min(current_fitness_values)

    return global_best_position, global_best_fitness