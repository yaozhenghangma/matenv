import ase
import numpy as np
import copy

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
    list = []
    for i in range(0, len(directions)):
        # right hand helix
        xyz = np.eye(3)
        xyz[2,:] = directions[i][0][0]
        xyz[0,:] = directions[i][1][0]
        cross_value = np.cross(xyz[2,:], xyz[0,:])
        possible_y = []
        for j in range(2, 6):
            possible_y.append((directions[i][j][0], cross_value.dot(directions[i][j][0])))
        right_y = max(possible_y, key=lambda x: x[1])
        xyz[1,:] = right_y[0]
        # Gram-Schmidt orthogonalization
        xyz[2,:] = xyz[2,:]/np.linalg.norm(xyz[2,:])
        xyz[1,:] = xyz[1,:] - np.dot(xyz[2,:], xyz[1,:])*xyz[2,:]
        xyz[1,:] = xyz[1,:]/np.linalg.norm(xyz[1,:])
        xyz[0,:] = xyz[0,:] - np.dot(xyz[2,:], xyz[0,:])*xyz[2,:] - np.dot(xyz[1,:], xyz[0,:])*xyz[1,:]
        xyz[0,:] = xyz[0,:]/np.linalg.norm(xyz[0,:])
        list.append(xyz)
    return list

def RotateTo(lattice, transform_matrix):
    list = []
    for matrix in transform_matrix:
        list.append(np.dot(lattice, np.linalg.inv(matrix)))
    return list

def Rotate(cell):
    positions = cell.get_positions()
    lattice = cell.cell.array
    rotational_invariant_positions = positions.dot(np.linalg.inv(lattice))
    directions = BandDirection(positions, lattice)
    transform_matrix = FindTransformedXYZ(directions)
    lattice_list = RotateTo(lattice, transform_matrix)
    cell_list = []
    for new_lattice in lattice_list:
        positions = rotational_invariant_positions.dot(new_lattice)
        cell.set_positions(positions)
        cell.cell[:] = new_lattice
        cell_list.append(copy.deepcopy(cell))
    return cell_list