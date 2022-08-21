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

class KPoint:
    def __init__(self, coordinate:np.ndarray=np.zeros(3), weight:float=1.0):
        if len(coordinate) != 3:
            raise ValueError(f'Input coordinate should be 3 dimensional.')
        self.coordinate = coordinate
        self.weight = weight

    def __repr__(self):
        return 'K-Point(weight:{},\tcoordinate:{})'.format(self.weight, self.coordinate)

class KPath:
    def __init__(self, distance:np.ndarray=np.array([])):
        self.distance = distance
