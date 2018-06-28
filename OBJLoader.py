import os
import numpy as np


class OBJLoader:
    def __init__(self, model_name, texture_name):
        self.model_path = os.getcwd() + "\\res\\" + model_name + '.obj'
        self.data = None

        self.textures = []
        self.normals = []

        tex = 'res\\' + texture_name + '.png'
        self.load_model(tex)

    def load_model(self, texture_name):
        raw_vertices = []
        raw_textures = []
        raw_normals = []
        raw_indices = []
        raw_image = texture_name

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
                        raw_vertices.append(vertex)
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

            self.textures = [None] * len(raw_vertices) * 2
            self.normals = [None] * len(raw_vertices) * 3

            with open(self.model_path) as obj:
                for line in obj:
                    if not line.startswith('f '):
                        continue
                    current_line = line.split(' ')
                    vertex1 = current_line[1].split('/')
                    vertex2 = current_line[2].split('/')
                    vertex3 = current_line[3].split('/')
                    self.process_vertex(vertex1, raw_textures, raw_normals, raw_indices)
                    self.process_vertex(vertex2, raw_textures, raw_normals, raw_indices)
                    self.process_vertex(vertex3, raw_textures, raw_normals, raw_indices)
        except IOError:
            print("Obj file not found.")

        vertices = [None] * len(raw_vertices) * 3
        indices = [None] * len(raw_indices)

        i = 0
        for vertex in raw_vertices:
            vertices[i] = vertex[0]
            i += 1
            vertices[i] = vertex[1]
            i += 1
            vertices[i] = vertex[2]
            i += 1

        for j, index in enumerate(raw_indices):
            indices[j] = raw_indices[j]

        self.data = np.array([
            vertices,
            self.textures,
            self.normals,
            indices,
            raw_image
        ])

    def process_vertex(self, vertex, raw_textures, raw_normals, raw_indices):
        vertex_pointer = int(vertex[0]) - 1
        raw_indices.append(vertex_pointer)

        current_texture = raw_textures[int(vertex[1]) - 1]

        self.textures[vertex_pointer * 2] = current_texture[0]
        self.textures[vertex_pointer * 2 + 1] = 1 - current_texture[1]

        current_normal = raw_normals[int(vertex[2]) - 1]
        self.normals[vertex_pointer * 3] = current_normal[0]
        self.normals[vertex_pointer * 3 + 1] = current_normal[1]
        self.normals[vertex_pointer * 3 + 2] = current_normal[2]
