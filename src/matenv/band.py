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
import numpy as np

class Band:
    def __init__(self, kpath:KPath=KPath(), energies:np.ndarray=np.array([])):
        if len(kpath.distance) != len(energies):
            raise ValueError(f'The number of k-points should be equal to the number of energies.')
        self.kpath = kpath
        self.energies = energies