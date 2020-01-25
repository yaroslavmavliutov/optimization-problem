import numpy as np
import copy
import math
from . import x,y,pb

########################################################################
# Objective functions
########################################################################

def to_sensors(sol):
    """Convert an square array of d lines/columns containing n ones
    to an array of n 2-tuples with related coordinates.

    >>> to_sensors([[1,0],[1,0]])
    [(0, 0), (0, 1)]
    """
    assert (len(sol) > 0)
    sensors = []
    for i in range(len(sol)):
        for j in range(len(sol[i])):
            if sol[i][j] == 1:
                sensors.append( (j,i) )
    return sensors

def cover_sum(sol, domain_width, sensor_range, dim):
    """Compute the coverage quality of the given array of bits."""
    assert(0 < sensor_range <= math.sqrt(2))
    assert(0 < domain_width)
    assert(dim > 0)
    assert(len(sol) >= dim)
    domain = np.zeros((domain_width,domain_width))
    sensors = to_sensors(sol)
    cov = pb.coverage(domain, sensors, sensor_range*domain_width)
    s = np.sum(cov)
    assert(s >= len(sensors))
    return s

########################################################################
# Initialization
########################################################################

def rand(domain_width, nb_sensors):
    """"Draw a random domain containing nb_sensors ones."""
    domain = np.zeros( (domain_width,domain_width) )
    for x,y in np.random.randint(0, domain_width, (nb_sensors, 2)):
        domain[y][x] = 1
    return domain


########################################################################
# Neighborhood
########################################################################

def neighb_square(sol, scale, domain_width):
    """Draw a random array by moving ones to adjacent cells."""
    assert (0 < scale <= 1)
    # Copy, because Python pass by reference
    # and we may not want to alter the original solution.
    new = copy.copy(sol)
    for py in range(len(sol)):
        for px in range(len(sol[py])):
            # Indices order is (y,x) in order to match
            # coordinates of images (row,col).
            if sol[py][px] == 1:
                # Add a one somewhere around.
                w = scale / 2 * domain_width
                ny = np.random.randint(py - w, py + w)
                nx = np.random.randint(px - w, px + w)
                ny = min(max(0, ny), domain_width - 1)
                nx = min(max(0, nx), domain_width - 1)

                if new[nx][ny] != 1:
                    new[py][px] = 0  # Remove original position.
                    new[ny][nx] = 1
                # else pass
    return new

