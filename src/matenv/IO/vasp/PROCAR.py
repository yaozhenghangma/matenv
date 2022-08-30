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

from matenv import KPoint
from matenv import KPath
from matenv import Band
import numpy as np
import copy
import re

def allocate_space(input):
    split_line = input.readline().strip().split()
    number_kpoints = int(split_line[3])
    number_bands = int(split_line[7])
    number_ions = int(split_line[11])

    kpoints = []
    bands = []

    for _ in range(0, number_kpoints):
        kpoints.append(copy.deepcopy(KPoint()))

    kpoints = np.array(kpoints)
    kpath = KPath(np.zeros_like(kpoints, dtype=np.float64))
    energies = np.zeros_like(kpoints, dtype=np.float64)
    for _ in range(0, number_bands):
        bands.append(copy.deepcopy(Band(kpath, energies)))

    return kpoints, bands, number_ions


def read_weight(input, kpoints, bands, number_ions):
    pattern = '[0-9]-[0-9]'     #pattern for negative coordinate value of k points
    kpath = KPath(np.zeros_like(kpoints, dtype=np.float64))
    for i in range(0, len(kpoints)):
        input.readline()    #blank line
        line = input.readline().strip()
        while re.search(pattern, line):
            position = re.search(pattern, line).span()
            line = line[0:position[0]+1] + " " + line[position[0]+1:]
        split_line = line.split()
        kpoints[i].coordinate[0] = float(split_line[3])
        kpoints[i].coordinate[1] = float(split_line[4])
        kpoints[i].coordinate[2] = float(split_line[5])
        kpoints[i].weight = float(split_line[8])
        if i == 0:
            kpath.distance[i] = 0
        else :
            kpath.distance[i] = np.linalg.norm(kpoints[i].coordinate - kpoints[i-1].coordinate) + kpath.distance[i-1]
        for j in range(0, len(bands)):
            input.readline()    #blank line
            split_line = input.readline().strip().split()
            bands[j].energies[i] = float(split_line[4])
            input.readline()    #blank line
            input.readline()    #comment line
            for _ in range(0, 4*(number_ions+1)):
                input.readline()
        input.readline()    #blank line

    for band in bands:
        band.kpath = kpath

    return bands


def load_PROCAR(file_name:str = "PROCAR", noncollinear=False):
    input = open(file_name, 'r')
    split_line = input.readline().strip().split()   # comment line, with phase or not

    if noncollinear:
        kpoints, bands, number_ions = allocate_space(input)
        bands = read_weight(input, kpoints, bands, number_ions)

    input.close()
    return bands, kpoints
