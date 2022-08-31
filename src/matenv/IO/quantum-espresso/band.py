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

def allocate_space(input):
    split_line = input.readline().strip().split()
    split_line[2] = split_line[2][0:-1]
    number_bands = int(split_line[2])
    number_kpoints = int(split_line[4])

    number_loops = number_bands // 10
    if (number_bands % 10) != 0:
        number_loops += 1


    kpoints = []
    bands = []

    for _ in range(0, number_kpoints):
        kpoints.append(copy.deepcopy(KPoint()))

    kpoints = np.array(kpoints)
    kpath = KPath(np.zeros_like(kpoints, dtype=np.float64))
    energies = np.zeros_like(kpoints, dtype=np.float64)
    for _ in range(0, number_bands):
        bands.append(copy.deepcopy(Band(kpath, energies)))

    return kpoints, bands, number_loops

def load_band(file_name:str="band.dat"):
    input = open(file_name, 'r')

    kpoints, bands, number_loops = allocate_space(input)
    kpath = KPath(np.zeros_like(kpoints, dtype=np.float64))
    for i in range(0, len(kpoints)):
        split_line = input.readline().strip().split()
        kpoints[i].coordinate[0] = float(split_line[0])
        kpoints[i].coordinate[1] = float(split_line[1])
        kpoints[i].coordinate[2] = float(split_line[2])
        if i == 0:
            kpath.distance[i] = 0
        else :
            kpath.distance[i] = np.linalg.norm(kpoints[i].coordinate - kpoints[i-1].coordinate) + kpath.distance[i-1]
        band_number = 0
        for _ in range(0, number_loops):
            j = 0
            split_line = input.readline().strip().split()
            while band_number < len(bands):
                bands[band_number].energies[i] = float(split_line[j])
                j += 1
                band_number += 1

    for band in bands:
        band.kpath = kpath

    input.close()
    return bands