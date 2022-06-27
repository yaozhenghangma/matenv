import numpy as np
import matenv

atom1 = matenv.Atom("C", [1, 1, 1])
atom2 = matenv.Atom("O", [0.5, 0.5, 0.5])
lattice = matenv.Lattice(np.eye(3))
atoms = matenv.Atoms(atom1, atom2)
cell = matenv.Cell(lattice, atoms)

def test_Atom():
    assert atom1.symbol == "C"
    assert atom2.coordinate[0] == 0.5

def test_Lattice():
    assert lattice.a()[0] == 1
    assert lattice.b()[1] == 1
    assert lattice.c()[2] == 1

def test_Atoms():
    for atom in atoms:
        assert atom.symbol != "Fe"

def test_Cell():
    assert cell.lattice.volume() == 1
    assert len(cell.atoms) == 2