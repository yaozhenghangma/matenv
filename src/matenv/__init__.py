import sys


if sys.version_info[0] == 2:
    raise ImportError('matenv requires Python3. This is Python2.')


__author__ = 'Yaozhenghang Ma'
__version__ = '0.0.1'

from matenv.cell import *
import matenv.c_cell
