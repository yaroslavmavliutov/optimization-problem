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

########################################################################
# Neighborhood
########################################################################

def neighb_square(sol, scale, domain_width):
    """Draw a random vector in a square of witdh `scale`
    around the given one."""
    # TODO handle constraints
    new = sol + (np.random.random(len(sol)) * scale - scale/2)
    return new
