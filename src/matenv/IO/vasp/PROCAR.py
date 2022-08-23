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
from matenv import Band
import numpy as np

def allocate_space(input):
    split_line = input.readline().strip().split()
    number_kpoints = int(split_line[3])
    number_bands = int(split_line[7])
    number_ions = int(split_line[11])

    kpoints = []
    bands = []

    for _ in range(0, number_kpoints):
        kpoints.append(KPoint())

    kpoints = np.array(kpoints)
    energies = np.zeros_like(kpoints, dtype=np.float64)
    for _ in range(0, number_bands):
        bands.append(Band(kpoints, energies))

    return kpoints, bands, number_ions


def read_weight(input, kpoints, bands, number_ions):
    for i in range(0, len(kpoints)):
        input.readline()    #blank line
        split_line = input.readline().strip().split()
        kpoints[i].coordinate[0] = int(split_line[3])
        kpoints[i].coordinate[1] = int(split_line[4])
        kpoints[i].coordinate[2] = int(split_line[5])
        kpoints[i].weight = int(split_line[8])
        for j in range(0, len(bands)):
            input.readline()    #blank line
            split_line = input.readline().strip().split()
            bands[j].energies[i] = float(split_line[4])
            input.readline()
            for _ in range(0, 4*(number_ions+1)):
                input.readline()

    for band in bands:
        band.kpoints = kpoints

    return bands


def load_PROCAR(file_name:str = "PROCAR", noncollinear=False):
    input = open(file_name, 'r')
    split_line = input.readline().strip().split()   # comment line, with phase or not

    if noncollinear:
        pass
    else :
        kpoints, bands, number_ions = allocate_space(input)
        bands = read_weight(input, kpoints, bands, number_ions)

    return bands
