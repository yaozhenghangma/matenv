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
#ifndef GRAPH
#define GRAPH

#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

class PYBIND11_EXPORT Edge {
};

class PYBIND11_EXPORT Vertex{
    public:
    std::vector<Edge *> edges;
};

class PYBIND11_EXPORT DirectedEdge : public Edge {
    public:
    Vertex * vertex;
};

class PYBIND11_EXPORT UndirectedEdge : public Edge {
    public:
    Vertex * vertex1;
    Vertex * vertex2;
};

class PYBIND11_EXPORT Graph {
};

class PYBIND11_EXPORT DirectedGraph : public Graph {
    public:
    std::vector<DirectedEdge> edges;
    std::vector<Vertex> vertexes;
};

class PYBIND11_EXPORT UndirectedGraph : public Graph {
    public:
    std::vector<UndirectedEdge> edges;
    std::vector<Vertex> vertexes;
};

#endif