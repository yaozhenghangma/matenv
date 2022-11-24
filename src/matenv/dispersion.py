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

from matenv import KPath
from matenv import KPoint
import numpy as np

class Dispersion:
    def __init__(self, number_kpoints:int=0, number_bands:int=0):
        self.kpoints = np.ndarray(number_kpoints, KPoint)
        self.energies = np.zeros((number_bands, number_kpoints))
        for i in range(0, number_kpoints):
            self.kpoints[i] = KPoint()

class Band:
    def __init__(self, kpath:KPath=KPath(), energies:np.ndarray=np.array([])):
        if len(kpath.distance) != len(energies):
            raise ValueError(f'The number of k-points should be equal to the number of energies.')
        self.kpath = kpath
        self.energies = energies

class DOS:
    def __init__(self, number_energy:int=0):
        self.energies = np.zeros(number_energy)
        self.dos = np.zeros(number_energy)

class Projection:
    def __init__(self, number_kpoints:int=0, number_bands:int=0, number_ions:int=0, number_orbitals:int=0, number_directions:int=0):
        self.projection = np.zeros((number_kpoints, number_bands, number_ions, number_orbitals), dtype=np.complex128)
        self.projection_square = np.zeros((number_kpoints, number_bands, number_ions, number_orbitals, number_directions), dtype=np.float64)
        self.dispersion = Dispersion(number_kpoints, number_bands)
        self.number_kpoints = number_kpoints
        self.number_bands = number_bands
        self.number_ions = number_ions
        self.number_orbitals = number_orbitals
        self.number_directions = number_directions