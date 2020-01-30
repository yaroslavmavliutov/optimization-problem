########################################################################
# Algorithms
########################################################################
import numpy as np

def random(func, init, again):
    """Iterative random search template."""
    best_sol = init()
    best_val = func(best_sol)
    val,sol = best_val,best_sol
    i = 0
    while again(i, best_val, best_sol):
        sol = init()
        val = func(sol)
        if val >= best_val:
            best_val = val
            best_sol = sol
        i += 1
    return best_val, best_sol


def greedy(func, init, neighb, again):
    """Iterative randomized greedy heuristic template."""
    best_sol = init()
    best_val = func(best_sol)
    val,sol = best_val,best_sol
    i = 1
    while again(i, best_val, best_sol):
        sol = neighb(best_sol)
        val = func(sol)
        # Use >= and not >, so as to avoid random walk on plateus.
        if val >= best_val:
            best_val = val
            best_sol = sol
        i += 1
    return best_val, best_sol


def sa(func, init, neighb, again):
    best_sol = init()
    best_val = func(best_sol)
    val,sol = best_val,best_sol
    i = 1
    k = 1
    T = 1000
    while again(i, best_val, best_sol) and T>=0:
        alpha = 0.9
        #T = max(0.01, min(1, 1 - alpha))
        r_sol = neighb(sol)
        r_val = func(r_sol)
        deltaE = val - r_val
        p = np.random.uniform()
        if deltaE < 0.0 or p < np.exp(-deltaE/T):
            sol = r_sol
        if func(sol) > best_val:
            best_val, best_sol = func(sol), sol
        print(i)
        T = T*alpha
        i += 1
        k += 1
    return best_val, best_sol


def genetic(func, init, tournament, crossover, again):
    population = init()
    dict_population = {i:func(element) for i,element in enumerate(population)}
    best_val, best_sol = dict_population.get(max(dict_population, key=dict_population.get)), population[max(dict_population, key=dict_population.get)]
    i = 1
    while again(i, best_val, best_sol):
        parents_idx = tournament(dict_population.copy())
        childs = crossover(population, parents_idx)

        # we are creating new population consisting childs and parents
        for idx in parents_idx:
            childs.append(population[idx])

        population = np.asarray(childs)

        dict_population.clear()
        dict_population = {m: func(element) for m, element in enumerate(population)}

        if dict_population.get(max(dict_population, key=dict_population.get)) > best_val:
            best_val, best_sol = dict_population.get(max(dict_population, key=dict_population.get)), \
                                            population[max(dict_population, key=dict_population.get)]
        i += 1
    return best_val, best_sol
