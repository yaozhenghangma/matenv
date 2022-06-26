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

import numpy as np


class Atom:
    symbol:str = ""
    coordinate:np.ndarray = np.zeros(3)

    def __init__(self, sym:str, coordinate):
        if len(coordinate) != 3:
            raise ValueError(f'Input coordinate should be 3 dimensional.')
        self.symbol = sym
        self.coordinate = np.array(coordinate)


class Atoms:
    atoms:Atom = []
    __number:int = 0
    __index:int = 0

    def __init__(self, *atoms:Atom):
        self.atoms = list(atoms)
        self.__number = len(self.atoms)

    def __len__(self):
        return self.__number

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index == self.__number:
            raise StopIteration
        self.__index = self.__index + 1
        return self.atoms[self.__index]


class Lattice:
    lattice:np.ndarray = np.zeros((3, 3))

    def __init__(self, lattice:np.ndarray):
        if type(lattice) != np.ndarray:
            raise TypeError(f'Input type should be numpy\'s ndarray.')
        if np.shape(lattice) != (3,3):
            raise ValueError(f'Lattice matrix should be a 3*3 matrix.')
        self.lattice = lattice

    def a(self):
        return self.lattice[0,0:2]

    def b(self):
        return self.lattice[1,0:2]

    def c(self):
        return self.lattice[2,0:2]

    def volume(self):
        return np.linalg.det(self.lattice)


class Cell:
    lattice:Lattice = Lattice()
    atoms:Atoms = Atoms()

    def __init__(self, lattice:Lattice, atoms:Atoms):
        self.lattice = lattice
        self.atoms = atoms

    def lattice(self):
        return self.lattice.lattice
