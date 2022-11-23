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
import numpy as np
import copy
import re

def allocate_space(input):
    split_line = input.readline().strip().split()
    number_kpoints = int(split_line[3])
    number_bands = int(split_line[7])
    number_ions = int(split_line[11])

    projection = Projection(number_kpoints, number_bands, number_ions, 9, 4)

    return projection


def read_weight(input, phase):
    projection = allocate_space(input)
    pattern = '[0-9]-[0-9]'     #pattern for negative coordinate value of k points
    for i in range(0, projection.number_kpoints):
        input.readline()    #blank line
        line = input.readline().strip()
        while re.search(pattern, line):
            position = re.search(pattern, line).span()
            line = line[0:position[0]+1] + " " + line[position[0]+1:]
        split_line = line.split()
        direct_coordinate = np.array([float(split_line[3]), float(split_line[4]), float(split_line[5])])
        projection.dispersion.kpoints[i].coordinate = copy.deepcopy(direct_coordinate)
        projection.dispersion.kpoints[i].weight = float(split_line[8])
        for j in range(0, projection.number_bands):
            input.readline()    #blank line
            split_line = input.readline().strip().split()
            projection.dispersion.energies[j, i] = float(split_line[4])
            input.readline()    #blank line
            input.readline()    #comment line
            for k in range(0, projection.number_directions):
                for l in range(0, projection.number_ions):
                    split_line = input.readline().strip().split()
                    for m in range(0, projection.number_orbitals):
                        projection.projection_square[i, j, l, m, k] = float(split_line[m+1])
                input.readline()    #tot projection line
            if phase:
                input.readline()    #comment line
                for l in range(0, projection.number_ions):
                    split_line = input.readline().strip().split()
                    for m in range(0, projection.number_orbitals):
                        projection.projection[i, j, l, m] = complex(float(split_line[2*m+1]), float(split_line[2*m+2]))
                input.readline()    #charge line
        input.readline()    #blank line

    return projection


def load_PROCAR(file_name:str = "PROCAR", noncollinear=False):
    input = open(file_name, 'r')
    split_line = input.readline().strip().split()   # comment line, with phase or not
    if 'phase' in split_line:
        phase = True
    else:
        phase = False

    if noncollinear:
        projection = read_weight(input, phase)

    input.close()
    return projection
