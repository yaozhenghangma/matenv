import numpy as np
import matenv

atom1 = matenv.Atom("C", [1, 1, 1])
atom2 = matenv.Atom("O", [0.5, 0.5, 0.5])
lattice = matenv.Lattice(np.eye(3))
atoms = matenv.Atoms(atom1, atom2)
cell = matenv.Cell(lattice, atoms)

c_atom1 = matenv.atom_conversion(atom1)
c_atom2 = matenv.atom_conversion(atom2)
c_lattice = matenv.lattice_conversion(lattice)
c_atoms = matenv.atoms_conversion(atoms)
c_cell = matenv.cell_conversion(cell)

def test_Atom():
    assert atom1.symbol == "C"
    assert atom2.coordinate[0] == 0.5
    assert c_atom1.coordinate[2] == 1
    assert c_atom2.symbol == "O"

def test_Lattice():
    assert lattice.a()[0] == 1
    assert lattice.b()[1] == 1
    assert lattice.c()[2] == 1
    assert c_lattice.lattice[2][2] == 1

def test_Atoms():
    for atom in atoms:
        assert atom.symbol != "Fe"
    assert c_atoms.atoms[0].symbol == "C"
    assert c_atoms.atoms[1].symbol == "O"

def test_Cell():
    assert cell.lattice.volume() == 1
    assert len(cell.atoms) == 2
    assert c_cell.lattice.lattice[1][0] == 0