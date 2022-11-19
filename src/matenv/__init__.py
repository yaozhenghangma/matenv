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

import sys


if sys.version_info[0] == 2:
    raise ImportError('matenv requires Python3. This is Python2.')


__author__ = 'Yaozhenghang Ma'
__version__ = '0.0.1'

from matenv.cell import *
from matenv.kpoint import *
from matenv.dispersion import *
from matenv.IO.vasp.PROCAR import load_PROCAR
#import matenv.c_cell
