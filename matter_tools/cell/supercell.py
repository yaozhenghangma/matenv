import copy
import numpy as np
from atom import *


def enlarge(cell, n=np.ones(3)):
    n_diag = np.diag(n)
    original_lattice = copy.deepcopy(cell.lattice.lattice)
    cell.lattice.lattice = n_diag @ cell.lattice.lattice
    cell.lattice.a = cell.lattice.lattice[0, 0:3]
    cell.lattice.b = cell.lattice.lattice[1, 0:3]
    cell.lattice.c = cell.lattice.lattice[2, 0:3]

    inverse_lattice = np.linalg.inv(cell.lattice.lattice)

    for atom in cell.atoms:
        atom.direct_coordinate = atom.Certesian_coordinate @ inverse_lattice

    atoms_add = []
    for i in range(0, n[0]):
        for j in range(0, n[1]):
            for k in range(0, n[2]):
                for atom in cell.atoms:
                    new_atom = copy.deepcopy(atom)
                    new_atom.Certesian_coordinate = new_atom.Certesian_coordinate + np.diag([i, j, k]) @ original_lattice
                    new_atom.direct_coordinate = atom.Certesian_coordinate @ inverse_lattice
                    atoms_add.append(copy.deepcopy(new_atom))
    cell.atoms = cell.atoms + atoms_add

    N = n[0]*n[1]*n[2]
    for i in range(0, len(cell.numbers)):
        cell.numbers[i] = cell.numbers[i] * N
    return cell