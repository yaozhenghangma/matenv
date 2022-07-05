import copy
from tokenize import String
import numpy as np
import matenv


def load_POSCAR(file_name:String = "POSCAR"):
    poscar_in = open(file_name, 'r')
    line = poscar_in.readline()
    line = poscar_in.readline()
    constant = float(line.strip())
    cell = matenv.Cell()
    for i in range(0, 3, 1):
        line = poscar_in.readline()
        line = line.strip()
        line_split = line.split()
        for j in range(0, 3, 1):
            cell.lattice.lattice[i, j] = float(line_split[j]) * constant

    line = poscar_in.readline()
    symbols = line.strip().split()
    numbers = []
    line = poscar_in.readline()
    line_split = line.strip().split()
    line = poscar_in.readline()
    direct = False
    if line[0] == 'D' or line[0] == 'd':
        direct = True
    for i in range(0, len(symbols)):
        numbers.append(int(line_split[i]))
        for j in range(0, numbers[i]):
            atom = matenv.Atom(symbols[i])
            line = poscar_in.readline()
            line = line.strip()
            if direct:
                atom.coordinate = np.array(line.split(), dtype=np.float64)
            else:
                atom.coordinate = np.array(line.split(), dtype=np.float64) @ np.linalg.inv(cell.lattice.lattice)
            cell.atoms.append(copy.deepcopy(atom))
    cell.symbols = symbols
    cell.numbers = numbers
    poscar_in.close()
    return cell


def save_POSCAR(file_name, cell, comment="output_structure"):
    poscar_out = open(file_name, 'w')
    poscar_out.write(comment + "\n")
    poscar_out.write("1.0\n")
    for i in range(0, 3):
        poscar_out.write(" %.5f\t" % cell.lattice.lattice[i, 0])
        poscar_out.write(" %.5f\t" % cell.lattice.lattice[i, 1])
        poscar_out.write(" %.5f\n" % cell.lattice.lattice[i, 2])
    for i in range(0, len(cell.symbols)):
        poscar_out.write(cell.symbols[i] + " ")
    poscar_out.write("\n")
    for i in range(0, len(cell.symbols)):
        poscar_out.write("%d " % cell.numbers[i])
    poscar_out.write("\nDirect\n")
    for i in range(0, len(cell.symbols)):
        for atom in cell.atoms:
            if atom.symbol == cell.symbols[i]:
                poscar_out.write(" %.5f\t" % atom.coordinate[0, 0])
                poscar_out.write(" %.5f\t" % atom.coordinate[0, 1])
                poscar_out.write(" %.5f\n" % atom.coordinate[0, 2])

    poscar_out.close()
    return None