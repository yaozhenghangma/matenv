//   Copyright (C) 2022  Yaozhenghang Ma
//
//   This program is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
//
//   You should have received a copy of the GNU General Public License
//   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#ifndef CELL
#define CELL

#include <string>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

class PYBIND11_EXPORT Atom {
    public:
    std::string symbol = "";
    std::vector<double> coordinate = {0, 0, 0};
};

class PYBIND11_EXPORT Atoms {
    public:
    std::vector<Atom> atoms;
    int number = 0;
};

class PYBIND11_EXPORT Lattice {
    public:
    std::vector<std::vector<double>> lattice = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
};

class PYBIND11_EXPORT Cell {
    public:
    Lattice lattice;
    Atoms atoms;
};

PYBIND11_MODULE(c_cell, m) {
    py::class_<Atom>(m, "Atom")
        .def_readwrite("symbol", &Atom::symbol)
        .def_readwrite("coordinate", &Atom::coordinate)
        .def(py::init<>());
    py::class_<Atoms>(m, "Atoms")
        .def_readwrite("atoms", &Atoms::atoms)
        .def_readwrite("number", &Atoms::number)
        .def(py::init<>());
    py::class_<Lattice>(m, "Lattice")
        .def_readwrite("lattice", &Lattice::lattice)
        .def(py::init<>());
    py::class_<Cell>(m, "Cell")
        .def_readwrite("lattice", &Cell::lattice)
        .def_readwrite("atoms", &Cell::atoms)
        .def(py::init<>());
}

#endif