import matenv

atom1 = matenv.c_cell.Atom()
atom1.symbol = "C"
atom1.coordinate = [1,1,1]
atom2 = matenv.c_cell.Atom()
atom2.symbol = "O"
atom2.coordinate = [0.5,0.5,0.5]
lattice = matenv.c_cell.Lattice()
lattice.lattice = [[1,0,0],[0,1,0],[0,0,1]]
atoms = matenv.c_cell.Atoms()
atoms.atoms = [atom1, atom2]
cell = matenv.c_cell.Cell()
cell.lattice = lattice
cell.atoms = atoms

def test_Atom():
    assert atom1.symbol == "C"
    assert atom2.coordinate[0] == 0.5

def test_Lattice():
    assert lattice.lattice[0][0] == 1

def test_Atoms():
    assert atoms.atoms[0].symbol =="C"

def test_Cell():
    assert cell.lattice.lattice[1][1] == 1