import numpy as np


class Atom:
    symbol = " "
    Certesian_coordinate = np.zeros(1, 3)
    direct_coordinate = np.zeros(1, 3)

    
class Lattice:
    a = np.zeros(1, 3)
    b = np.zeros(1, 3)
    c = np.zeros(1, 3)
    lattice = np.zeros(3, 3)
