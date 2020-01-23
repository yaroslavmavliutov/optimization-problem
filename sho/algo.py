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

# TODO add a simulated-annealing template.
def simul(func, init, neighb, again):
    T = 100
    best_sol = init()
    print("sol: ", best_sol)
    best_val = func(best_sol)
    val,sol = best_val,best_sol
    i = 1
    while again(i, best_val, best_sol) or T > 0:
        #sol = neighb(best_sol)
        val = func(sol)
        r = neighb(best_sol)
        valr = func(r)
        deltaE = val - valr
        p = np.random.uniform()
        if deltaE <0 or p < (np.exp(-deltaE/T)):
            sol = r
        if val >= best_val:
            best_val = val
            best_sol = sol
        T = 0.01*T
        i += 1
    return best_val, best_sol


# TODO add a population-based stochastic heuristic template.
def genetic(func, init, selection, crossover, again):
    population = init()
    dict_population = {i:func(element) for i,element in enumerate(population)}
    best_val, best_sol = dict_population.get(max(dict_population, key=dict_population.get)), population[max(dict_population, key=dict_population.get)]
    i = 1
    #F = []
    while again(i, best_val, best_sol):
        print(i)
        parents_idx = selection(dict_population)
        childs = crossover(population, parents_idx)
        #for k,idx in enumerate(parents_idx):
        #    population[idx] = childs[k]
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
