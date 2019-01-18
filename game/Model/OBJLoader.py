import os
import numpy as np


class OBJLoader:
    def __init__(self, model_name):
        self.model_path = "F:\\Git Repos\\pyGL\\game\\Assets\\res\\" + model_name + '.obj'
        self.data = None
        self.load_model()

    def load_model(self):
        raw_vertices = []
        raw_textures = []
        raw_normals = []
        raw_indices = []

        try:
            with open(self.model_path) as obj:
                for line in obj:
                    current_line = line.split(' ')
                    if line.startswith('v '):
                        vertex = np.array([
                            current_line[1],
                            current_line[2],
                            current_line[3]
                        ], dtype='float32')
                        new_vertex = Vertex(len(raw_vertices), vertex)
                        raw_vertices.append(new_vertex)
                    elif line.startswith('vt '):
                        texture = np.array([
                        current_line[1],
                        current_line[2]
                    ], dtype='float32')
                        raw_textures.append(texture)
                    elif line.startswith('vn '):
                        normal = np.array([
                        current_line[1],
                        current_line[2],
                        current_line[3]
                    ], dtype='float32')
                        raw_normals.append(normal)

            with open(self.model_path) as obj:
                for line in obj:
                    if not line.startswith('f '):
                        continue
                    current_line = line.split(' ')
                    vertex1 = current_line[1].split('/')
                    vertex2 = current_line[2].split('/')
                    vertex3 = current_line[3].split('/')
                    self.process_vertex(vertex1, raw_vertices, raw_indices)
                    self.process_vertex(vertex2, raw_vertices, raw_indices)
                    self.process_vertex(vertex3, raw_vertices, raw_indices)
        except IOError:
            print("Obj file not found: " + self.model_path)

        self.remove_unused(raw_vertices)
        vertices = [None] * len(raw_vertices) * 3
        textures = [None] * len(raw_vertices) * 2
        normals = [None] * len(raw_vertices) * 3
        furthest = self.convert_data(raw_vertices, raw_textures, raw_normals, vertices, textures, normals)
        indices = self.convert_indices(raw_indices)
        self.data = np.array([
            vertices,
            textures,
            normals,
            indices,
            furthest
        ])

    def process_vertex(self, vertex, vertices, indices):
        index = int(vertex[0]) - 1
        current_vertex = vertices[index]
        texture_index = int(vertex[1]) - 1
        normal_index = int(vertex[2]) - 1

        if not current_vertex.is_set():
            current_vertex.texture_index = texture_index
            current_vertex.normal_index = normal_index
            indices.append(index)
        else:
            self.deal_with_processed(current_vertex, texture_index, normal_index, indices, vertices)

    def deal_with_processed(self, previous_vertex, new_texture_index, new_normal_index, indices, vertices):
        if previous_vertex.has_same(new_texture_index, new_normal_index):
            indices.append(previous_vertex.index)
        else:
            another_vertex = previous_vertex.duplicate_vertex
            if another_vertex is not None:
                self.deal_with_processed(another_vertex, new_texture_index, new_normal_index, indices, vertices)
            else:
                duplicate_vertex = Vertex(len(vertices), previous_vertex.position)
                duplicate_vertex.texture_index = new_texture_index
                duplicate_vertex.normal_index = new_normal_index
                previous_vertex.duplicate_vertex = duplicate_vertex
                vertices.append(duplicate_vertex)
                indices.append(duplicate_vertex.index)

    @staticmethod
    def remove_unused(vertices):
        for vertex in vertices:
            if not vertex.is_set():
                vertex.texture_index = 0
                vertex.normal_index = 0

    @staticmethod
    def convert_indices(indices):
        new_indices = [None] * len(indices)
        for i in range(0, len(new_indices)):
            new_indices[i] = indices[i]
        return new_indices

    @staticmethod
    def convert_data(raw_vertices, raw_textures, raw_normals, vertices, textures, normals):
        furthest_point = 0
        for i in range(0, len(raw_vertices)):
            current_vertex = raw_vertices[i]
            if current_vertex.length > furthest_point:
                furthest_point = current_vertex.length
            position = current_vertex.position
            texture_coord = raw_textures[current_vertex.texture_index]
            normal = raw_normals[current_vertex.normal_index]
            vertices[i * 3] = position[0]
            vertices[i * 3 + 1] = position[1]
            vertices[i * 3 + 2] = position[2]
            textures[i * 2] = texture_coord[0]
            textures[i * 2 + 1] = 1 - texture_coord[1]
            normals[i * 3] = normal[0]
            normals[i * 3 + 1] = normal[1]
            normals[i * 3 + 2] = normal[2]

        return furthest_point


class Vertex:
    def __init__(self, index, position):
        self.NO_INDEX = -1

        self.index = index
        self.position = position
        self.length = len(position)

        self.duplicate_vertex = None

        self.texture_index = self.NO_INDEX
        self.normal_index = self.NO_INDEX

    def is_set(self):
        val = self.texture_index != self.NO_INDEX and self.normal_index != self.NO_INDEX
        return val

    def has_same(self, texture_index, normal_index):
        val = texture_index == self.texture_index and normal_index == self.normal_index
        return val
