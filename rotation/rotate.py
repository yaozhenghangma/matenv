import ase 
from ase.build import bulk
from ase import Atoms
import numpy as np

def BandDirection(positions, lattice):
    positions_atom1 = positions[0:2, :]
    positions_atom2 = positions[2:, :]
    atom1_number = positions_atom1.shape[0]
    atom2_number = positions_atom2.shape[0]
    list = []
    for i in range(0, atom1_number):
        directions = []
        for j in range(0, atom2_number):
            temp_list = []
            temp_list.append((positions_atom2[j]-positions_atom1[i], np.linalg.norm(positions_atom2[j]-positions_atom1[i])))
            temp_list.append((positions_atom2[j]-positions_atom1[i]+lattice[0,:], np.linalg.norm(positions_atom2[j]-positions_atom1[i]+lattice[0,:])))
            temp_list.append((positions_atom2[j]-positions_atom1[i]-lattice[0,:], np.linalg.norm(positions_atom2[j]-positions_atom1[i]-lattice[0,:])))
            temp_list.append((positions_atom2[j]-positions_atom1[i]+lattice[1,:], np.linalg.norm(positions_atom2[j]-positions_atom1[i]+lattice[1,:])))
            temp_list.append((positions_atom2[j]-positions_atom1[i]-lattice[1,:], np.linalg.norm(positions_atom2[j]-positions_atom1[i]-lattice[1,:])))
            temp_list.append((positions_atom2[j]-positions_atom1[i]+lattice[2,:], np.linalg.norm(positions_atom2[j]-positions_atom1[i]+lattice[2,:])))
            temp_list.append((positions_atom2[j]-positions_atom1[i]-lattice[2,:], np.linalg.norm(positions_atom2[j]-positions_atom1[i]-lattice[2,:])))
            directions.append(min(temp_list, key=lambda x: x[1]))
        directions.sort(key=lambda x: x[1])
        directions = directions[0:6]
        list.append(directions)
    return list

def FindTransformedXYZ(directions):
    return 0

def RotateTo(lattice, transform_matrix):
    return 0

def Rotate(cell):
    positions = cell.get_positions()
    lattice = cell.cell.array
    rotational_invariant_positions = positions.dot(np.linalg.inv(lattice))
    directions = BandDirection(positions, lattice)
    transform_matrix = FindTransformedXYZ(directions)
    RotateTo(lattice, transform_matrix)
    positions = rotational_invariant_positions.dot(lattice)
    cell.set_positions(positions)
    cell.cell[:] = lattice
    return 0