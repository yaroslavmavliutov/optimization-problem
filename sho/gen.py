import numpy as np
import math
from . import pb

########################################################################
# Objective functions
########################################################################

# Decoupled from objective functions, so as to be used in display.
def to_sensors(sol):
    """Convert a vector of n*2 dimension to an array of n 2-tuples.

    >>> to_sensors([0,1,2,3])
    [(0, 1), (2, 3)]
    """
    assert (len(sol) > 0)
    sensors = []
    for i in range(0, len(sol), 2):
        sensors.append((int(math.floor(sol[i])), int(math.floor(sol[i + 1]))))
    return sensors


def cover_sum(sol, domain_width, sensor_range, dim):
    """Compute the coverage quality of the given vector."""
    assert (0 < sensor_range <= domain_width * math.sqrt(2))
    assert (0 < domain_width)
    assert (dim > 0)
    assert (len(sol) >= dim)
    domain = np.zeros((domain_width, domain_width))
    sensors = to_sensors(sol)
    cov = pb.coverage(domain, sensors, sensor_range * domain_width)
    s = np.sum(cov)
    assert (s >= len(sensors))
    return s


########################################################################
# Initialization
########################################################################

def rand(dim, scale):
    """Draw a random vector in [0,scale]**dim."""
    return np.random.random(dim) * scale

def population(p_size, dim, scale):
    P = []
    for i in range(p_size):
        P.append(np.random.random(dim) * scale)
    return P

########################################################################
# Generation
########################################################################

# selection
def tournament(population, num_parent):
    idx = []
    for i in range(num_parent):
        idx.append(max(population, key=population.get))
        del population[idx[-1]]
    return idx

def crossover(population, idx_parents, mutation, scale):
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

        for gen in range(0, nb_gens):
            parent = np.random.randint(2)
            child1.append(choice[parent][gen])
            child2.append(choice[1-parent][gen])

            if np.random.random() <= mutation:
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