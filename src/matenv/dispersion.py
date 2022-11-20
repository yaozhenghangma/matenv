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
        self.energies = np.zeros(number_bands, number_kpoints)
        for i in range(0, number_kpoints):
            self.kpoints[i] = KPoint()

class Band:
    def __init__(self, kpath:KPath=KPath(), energies:np.ndarray=np.array([])):
        if len(kpath.distance) != len(energies):
            raise ValueError(f'The number of k-points should be equal to the number of energies.')
        self.kpath = kpath
        self.energies = energies

class DOS:
    def __init__(self, energies:np.ndarray=np.array([]), dos:np.ndarray=np.array([])):
        if len(energies) != len(dos):
            raise ValueError(f'The number of points should match.')
        self.energies = energies
        self.dos = dos

class Projection:
    def __init__(self, number_kpoints:int=0, number_bands:int=0, number_ions:int=0, number_orbitals:int=0, number_directions:int=0):
        self.projection = np.zeros((number_kpoints, number_bands, number_ions, number_orbitals, number_directions), dtype=np.complex128)
        self.kpoints = Dispersion(number_kpoints, number_bands)