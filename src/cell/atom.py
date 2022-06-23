import numpy as np


class Atom:
    symbol = " "
    Certesian_coordinate = np.zeros((1, 3))
    direct_coordinate = np.zeros((1, 3))

    def __init__(self, sym, direct_coor=np.zeros((1, 3)), Certesian_coor=np.zeros((1, 3))):
        self.symbol = sym
        self.Certesian_coordinate = Certesian_coor
        self.direct_coordinate = direct_coor

    
class Lattice:
    a = np.zeros((1, 3))
    b = np.zeros((1, 3))
    c = np.zeros((1, 3))
    lattice = np.zeros((3, 3))


class Cell:
    lattice = Lattice()
    atoms = []
    symbols = []
    numbers = []
