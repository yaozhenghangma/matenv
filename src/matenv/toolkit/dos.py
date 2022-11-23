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
from matenv import DOS
import numpy as np

def gaussian(x:float, x0:float, sigma:float=0.05):
    return 1.0/np.sqrt(2*np.pi)/sigma * np.exp(-(x-x0)**2 / (2*sigma**2))

def lorentz(x:float, x0:float, gamma:float=0.03):
    return gamma / np.pi / ((x-x0)**2 + gamma**2)

def generate_dos(projection:Projection, distribution:function=gaussian, number_energy:int=3000):
    dos = DOS(number_energy)
    dos.energies = np.linspace(np.min(projection.dispersion.energies), np.max(projection.dispersion.energies), number_energy)
    dos.dos = []
    for energy in dos.energies:
        dos_value = 0
        for i in range(0, projection.dispersion.energies.shape[0]):
            for j in range(0, projection.dispersion.energies.shape[1]):
                dos_value += distribution(energy, projection.dispersion.energies[i, j]) * projection.dispersion.kpoints[j].weight
        dos.dos.append(dos_value)
    dos.dos = np.array(dos.dos)
    return dos

def generate_pdos(projection:Projection, ions, orbitals, distribution, number_energy:int=3000):
    dos = DOS(number_energy)
    dos.energies = np.linspace(np.min(projection.dispersion.energies), np.max(projection.dispersion.energies), number_energy)
    dos.dos = []
    for energy in dos.energies:
        dos_value = 0
        for i in range(0, projection.dispersion.energies.shape[0]):
            for j in range(0, projection.dispersion.energies.shape[1]):
                dos_value += distribution(energy, projection.dispersion.energies[i, j]) * projection.dispersion.kpoints[j].weight
        dos.dos.append(dos_value)
    dos.dos = np.array(dos.dos)
    return dos