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
    all_atoms = []
    for i in range(0, n[0]):
        for j in range(0, n[1]):
            for k in range(0, n[2]):
                for atom in cell.atoms:
                    new_atom = copy.deepcopy(atom)
                    new_atom.Certesian_coordinate = new_atom.Certesian_coordinate + np.array([[i, j, k]]) @ original_lattice
                    new_atom.direct_coordinate = new_atom.Certesian_coordinate @ inverse_lattice
                    atoms_add.append(copy.deepcopy(new_atom))
    all_atoms = all_atoms + atoms_add
    cell.atoms = all_atoms

    N = n[0]*n[1]*n[2]
    for i in range(0, len(cell.numbers)):
        cell.numbers[i] = cell.numbers[i] * N
    return cell


def slice(cell, miller_index=np.ones(3)):
    # slice for at least one Miller index being 1
    non_zero = (miller_index != 0)
    non_zero_factor = []
    non_zero_lattice = []
    zero_lattice = []
    for i in range(0, 3):
        if non_zero[i]:
            non_zero_lattice.append(copy.deepcopy(cell.lattice.lattice[i, 0:3]))
            non_zero_factor.append(miller_index[i])
        else :
            zero_lattice.append(copy.deepcopy(cell.lattice.lattice[i, 0:3]))
    
    # a,b: in-plane. c: out-plane
    if len(non_zero_lattice) == 1:
        cell.lattice.lattice[2, 0:3] = non_zero_lattice[0]
        cell.lattice.lattice[0, 0:3] = zero_lattice[0]
        cell.lattice.lattice[1, 0:3] = zero_lattice[1]
    elif len(non_zero_lattice) == 2:
        cell.lattice.lattice[0, 0:3] = zero_lattice[0]
        if non_zero_factor[0] == 1:
            cell.lattice.lattice[1, 0:3] = non_zero_factor[1] * non_zero_lattice[0] - non_zero_lattice[1]
            cell.lattice.lattice[2, 0:3] = non_zero_lattice[0]
        else :
            cell.lattice.lattice[1, 0:3] = non_zero_factor[0] * non_zero_lattice[1] - non_zero_lattice[0]
            cell.lattice.lattice[2, 0:3] = non_zero_lattice[1]
    elif len(non_zero_lattice) == 3:
        index = 0
        for i in range(0, 3):
            if non_zero_factor[i] == 1:
                index = i
                break
        temp_lattice = copy.deepcopy(non_zero_lattice[0])
        non_zero_lattice[0] = copy.deepcopy(non_zero_lattice[index])
        non_zero_lattice[index] = temp_lattice
        temp_factor = non_zero_factor[0]
        non_zero_factor[0] = non_zero_factor[index]
        non_zero_factor[index] = temp_factor
        cell.lattice.lattice[0, 0:3] = non_zero_factor[1] * non_zero_lattice[0] - non_zero_lattice[1]
        cell.lattice.lattice[1, 0:3] = non_zero_factor[2] * non_zero_lattice[0] - non_zero_lattice[2]
        cell.lattice.lattice[2, 0:3] = non_zero_lattice[0]


    if np.linalg.det(cell.lattice.lattice) < 0:
        temp_a = copy.deepcopy(cell.lattice.lattice[0, 0:3])
        cell.lattice.lattice[0, 0:3] = copy.deepcopy(cell.lattice.lattice[1, 0:3])
        cell.lattice.lattice[1, 0:3] = temp_a
    
    cell.lattice.a = cell.lattice.lattice[0, 0:3]
    cell.lattice.b = cell.lattice.lattice[1, 0:3]
    cell.lattice.v = cell.lattice.lattice[2, 0:3]

    reciprocal_lattice = np.linalg.inv(cell.lattice.lattice)
    for atom in cell.atoms:
        atom.direct_coordinate = atom.Certesian_coordinate @ reciprocal_lattice
        atom.direct_coordinate = atom.direct_coordinate - np.floor(atom.direct_coordinate)
        atom.Certesian_coordinate = atom.direct_coordinate @ cell.lattice.lattice
    return cell


def add_shift(cell, shift=0):
    shift_vector = cell.lattice.c * shift
    reciprocal_lattice = np.linalg.inv(cell.lattice.lattice)
    for atom in cell.atoms:
        atom.Certesian_coordinate = atom.Certesian_coordinate - shift_vector
        atom.direct_coordinate = atom.Certesian_coordinate @ reciprocal_lattice
    return cell


def add_vacuum(cell, vacuum=0):
    vacuum_vector = cell.lattice.c * vacuum
    cell.lattice.lattice[2, 0:3] = cell.lattice.lattice[2, 0:3] + vacuum_vector
    cell.lattice.c = cell.lattice.lattice[2, 0:3]
    reciprocal_lattice = np.linalg.inv(cell.lattice.lattice)
    for atom in cell.atoms:
        atom.direct_coordinate = atom.Certesian_coordinate @ reciprocal_lattice
    return cell


def normalize_cell(cell):
    for atom in cell.atoms:
        for i in range(0, 3):
            atom.direct_coordinate[0, i] = atom.direct_coordinate[0, i] - np.floor(atom.direct_coordinate[0, i])
            atom.Certesian_coordinate = atom.direct_coordinate @ cell.lattice.lattice
    return cell


def slap(cell, miller_index=np.ones(3), layer=1, shift=0, vacuum=0):
    cell = slice(cell, miller_index)
    cell = enlarge(cell, np.array([1, 1, layer]))
    cell = add_shift(cell, shift)
    cell = normalize_cell(cell)
    cell = add_vacuum(cell, vacuum)
    return cell
