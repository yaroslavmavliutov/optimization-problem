import numpy as np

########################################################################
# Objective functions
########################################################################

# We use the same function as num_greedy


########################################################################
# Initialization
########################################################################

def population(p_size, dim, scale):
    assert (p_size > 0)
    P = []
    for i in range(p_size):
        P.append(np.random.random(dim) * scale)
    return P

########################################################################
# Generation
########################################################################

# selection
def tournament(population, num_parent):
    assert ((num_parent % 2) == 0)
    assert (0 < num_parent < len(population))
    idx = []
    for i in range(num_parent):
        idx.append(max(population, key=population.get))
        # to avoid a element repetition, we need to delete the element
        # we use population.copy() here
        del population[idx[-1]]
    return idx

def crossover(population, idx_parents, mutation, scale):
    assert (0 <= mutation <= 1)
    childs = []
    nb_parents = len(idx_parents)
    np.random.shuffle(idx_parents)
    for i in range(0, nb_parents, 2):
        mom = population[idx_parents[i]]
        dad = population[idx_parents[i+1]]
        nb_gens = len(mom)
        child1 = []
        child2 = []
        choice = [mom, dad]

        # numbers of genes is numbers of coordinates
        for gen in range(0, nb_gens):
            parent = np.random.randint(2)
            child1.append(choice[parent][gen])
            child2.append(choice[1-parent][gen])

            if np.random.random() <= mutation:
                # to avoid going outside the area
                while True:
                    child1[gen] = child1[gen] + np.random.uniform(low=-2.0, high=2.0)
                    if child1[gen] >= 0.0 and child1[gen] < scale:
                        break

            if np.random.random() <= mutation:
                while True:
                    child2[gen] = child2[gen] + np.random.uniform(low=-2.0, high=2.0)
                    if child2[gen] >= 0.0 and child2[gen] < scale:
                        break
        childs.append(np.asarray(child1))
        childs.append(np.asarray(child2))
    return childs