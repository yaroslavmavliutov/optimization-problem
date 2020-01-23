import numpy as np

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
    sensors = []
    for i in range(0,len(sol),2):
        sensors.append( ( int(round(sol[i])), int(round(sol[i+1])) ) )
    return sensors


def cover_sum(sol, domain_width, sensor_range):
    """Compute the coverage quality of the given vector."""
    domain = np.zeros((domain_width,domain_width))
    sensors = to_sensors(sol)
    return np.sum(pb.coverage(domain, sensors, sensor_range))




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
# Neighborhood
########################################################################

def neighb_square(sol, scale, domain_width):
    """Draw a random vector in a square of witdh `scale`
    around the given one."""
    # TODO handle constraints
    new = sol + (np.random.random(len(sol)) * scale - scale/2)
    return new

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
    nb = len(idx_parents)
    np.random.shuffle(idx_parents)
    for i in range(0, nb, 2):
        mom = population[idx_parents[i]]
        dad = population[idx_parents[i+1]]

        # childs.append(np.array([mom[0], dad[1], dad[2], mom[3]]))
        childs.append(np.array([mom[0], mom[1], dad[2], dad[3]]))
        #print("1: ", childs[-1])
        for gen in [0, 1, 2, 3]:
            if np.random.random() <= mutation:
                #gen = np.random.choice([0, 1, 2, 3], 1)
                while True:
                    childs[-1][gen] = childs[-1][gen] + np.random.uniform(low=-2.0, high=2.0)
                    if childs[-1][gen] >= 0.0 and childs[-1][gen] < scale:
                        break
        #print("2: ", childs[-1])

        childs.append(np.array([dad[0], mom[1], mom[2], dad[3]]))
        for gen in [0, 1, 2, 3]:
            if np.random.random() <= mutation:
                #gen = np.random.choice([0, 1, 2, 3], 1)
                while True:
                    childs[-1][gen] = childs[-1][gen] + np.random.uniform(low=-2.0, high=2.0)
                    if childs[-1][gen] >= 0.0 and childs[-1][gen] < scale:
                        break

    return childs

