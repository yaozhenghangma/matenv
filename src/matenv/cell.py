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
    def __init__(self, symbol:str="", coordinate:np.ndarray=np.zeros(3)):
        if len(coordinate) != 3:
            raise ValueError(f'Input coordinate should be 3 dimensional.')
        self.symbol = symbol
        self.coordinate = np.array(coordinate)

    def __repr__(self):
        return 'Atom({}\t{})'.format(self.symbol, self.coordinate)


class Atoms:
    def __init__(self, *atoms:Atom):
        self.atoms = list(atoms)
        self.__number = len(self.atoms)
        self.__index = -1

    def __len__(self):
        return self.__number

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index == self.__number-1:
            self.__index = -1
            raise StopIteration
        self.__index = self.__index + 1
        return self.atoms[self.__index]

    def __repr__(self):
        string = 'Number of atoms: {}\n'.format(self.__number)
        i = 1
        for atom in self:
            string += 'Atom {}:\t{}\t{}\n'.format(i, atom.symbol, atom.coordinate)
            i += 1
        return string


class Lattice:
    def __init__(self, lattice:np.ndarray=np.zeros((3,3))):
        if type(lattice) != np.ndarray:
            raise TypeError(f'Input type should be numpy\'s ndarray.')
        if np.shape(lattice) != (3,3):
            raise ValueError(f'Lattice matrix should be a 3*3 matrix.')
        self.lattice = lattice

    def a(self) -> np.ndarray:
        return self.lattice[0,0:3]

    def b(self) -> np.ndarray:
        return self.lattice[1,0:3]

    def c(self) -> np.ndarray:
        return self.lattice[2,0:3]

    def volume(self) -> int:
        return np.linalg.det(self.lattice)

    def __repr__(self):
        return 'Lattice: \n{}'.format(self.lattice)


class Cell:
    def __init__(self, lattice:Lattice=Lattice(), atoms:Atoms=Atoms()):
        self.lattice = lattice
        self.atoms = atoms

    def __repr__(self):
        return '{}\n{}'.format(self.lattice, self.atoms)