#   Copyright (C) 2022  Yaozhenghang Ma
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from matenv import Projection
from matenv import DOS
import numpy as np

def gaussian(x:float, x0:float, sigma:float=0.05):
    return 1.0/np.sqrt(2*np.pi)/sigma * np.exp(-(x-x0)**2 / (2*sigma**2))

def lorentz(x:float, x0:float, gamma:float=0.03):
    return gamma / np.pi / ((x-x0)**2 + gamma**2)

def generate_dos(projection:Projection, distribution=gaussian, number_energy:int=3000):
    dos = DOS(number_energy)
    dos.energies = np.linspace(np.min(projection.dispersion.energies), np.max(projection.dispersion.energies), number_energy)
    dos.dos = np.zeros_like(dos.energies)
    for i in range(0, projection.dispersion.energies.shape[0]):
        for j in range(0, projection.dispersion.energies.shape[1]):
            dos.dos += distribution(dos.energies, projection.dispersion.energies[i, j]) * projection.dispersion.kpoints[j].weight
    return dos

def generate_pdos(projection:Projection, ions, orbitals, distribution=gaussian, number_energy:int=3000):
    dos = DOS(number_energy)
    dos.energies = np.linspace(np.min(projection.dispersion.energies), np.max(projection.dispersion.energies), number_energy)
    dos.dos = np.zeros_like(dos.energies)
    for i in range(0, projection.dispersion.energies.shape[0]):
        for j in range(0, projection.dispersion.energies.shape[1]):
            dos.dos += distribution(dos.energies, projection.dispersion.energies[i, j]) * projection.dispersion.kpoints[j].weight \
                * np.sum(projection.projection_square[j, i, ions, orbitals, 0])
    return dos

def distinguish_spin(projection:Projection, axis:int=3, phase=False):
    projection_up = Projection(projection.number_kpoints, 0, projection.number_ions, projection.number_orbitals, 1)
    projection_dn = Projection(projection.number_kpoints, 0, projection.number_ions, projection.number_orbitals, 1)
    projection_up.dispersion.kpoints = projection.dispersion.kpoints
    projection_dn.dispersion.kpoints = projection.dispersion.kpoints
    projection_square = projection.projection_square.transpose(1,0,2,3,4)
    projection_up.projection_square = projection_up.projection_square.transpose(1,0,2,3,4)
    projection_dn.projection_square = projection_up.projection_square.transpose(1,0,2,3,4)
    if phase:
        projection_phase = projection.projection.transpose(1,0,2,3)
        projection_up.projection = projection_up.projection.transpose(1,0,2,3)
        projection_dn.projection = projection_dn.projection.transpose(1,0,2,3)
    for i in range(0, projection.number_bands):
        if np.sum(projection_square[i, :, :, :, axis]) >= 0:
            projection_up.number_bands += 1
            projection_up.projection_square = np.insert(projection_up.projection_square, 0, values=projection_square[i, :, :, :, 0:1], axis=0)
            projection_up.dispersion.energies = np.insert(projection_up.dispersion.energies, 0, projection.dispersion.energies[i, :], axis=0)
            if phase:
                projection_up.projection = np.insert(projection_up.projection, 0, values=projection_phase[i, :, :, :], axis=0)
        else:
            projection_dn.number_bands += 1
            projection_dn.projection_square = np.insert(projection_dn.projection_square, 0, values=projection_square[i, :, :, :, 0:1], axis=0)
            projection_dn.dispersion.energies = np.insert(projection_dn.dispersion.energies, 0, projection.dispersion.energies[i, :], axis=0)
            if phase:
                projection_dn.projection = np.insert(projection_dn.projection, 0, values=projection_phase[i, :, :, :], axis=0)

    projection_up.projection_square = np.flip(projection_up.projection_square, 0)
    projection_up.dispersion.energies = np.flip(projection_up.dispersion.energies, 0)
    projection_dn.projection_square = np.flip(projection_dn.projection_square, 0)
    projection_dn.dispersion.energies = np.flip(projection_dn.dispersion.energies, 0)
    projection_up.projection_square = projection_up.projection_square.transpose(1,0,2,3,4)
    projection_dn.projection_square = projection_dn.projection_square.transpose(1,0,2,3,4)
    if phase:
        projection_up.projection = np.flip(projection_up.projection, 0)
        projection_dn.projection = np.flip(projection_dn.projection, 0)
        projection_up.projection = projection_up.projection.transpose(1,0,2,3)
        projection_dn.projection = projection_dn.projection.transpose(1,0,2,3)

    return projection_up, projection_dn

def transform(projection:Projection, matrix:np.ndarray=np.eye(5, dtype=np.complex128)):
    for i in range(0, projection.number_kpoints):
        for j in range(0, projection.number_bands):
            for k in range(0, projection.number_ions):
                projection.projection[i, j, k, 4:9] = np.matmul(matrix, projection[i, j, k, 4:9])
                projection.projection_square[i, j, k, 4:9, 0] = np.abs(projection.projection[i, j, k, 4:9])
    return projection