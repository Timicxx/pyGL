from OpenGL.GL import *
from OpenGL.GL.shaders import *
from pyrr import matrix44
import numpy as np


class TerrainShader:
    def __init__(self, vert_file = 'terrain.vert', frag_file = 'terrain.frag'):
        self.vert_file = vert_file
        self.frag_file = frag_file
        self.vertex_shader = None
        self.fragment_shader = None
        self.program = None

        self.create_program()

    def create_program(self):
        with open(self.vert_file, 'r') as vert:
            self.vertex_shader = compileShader(vert, GL_VERTEX_SHADER)
        with open(self.frag_file, 'r') as frag:
            self.fragment_shader = compileShader(frag, GL_FRAGMENT_SHADER)

        self.program = compileProgram(self.vertex_shader, self.fragment_shader)
        glUseProgram(self.program)

    def start(self):
        glUseProgram(self.program)

    @staticmethod
    def stop():
        glUseProgram(0)

    def load_light(self, light):
        lightPosition = glGetUniformLocation(self.program, "lightPosition")
        glUniform3fv(lightPosition, 1, light.position)
        lightColor = glGetUniformLocation(self.program, "lightColor")
        glUniform3fv(lightColor, 1, light.color)

    def load_shine(self, tex_model):
        shine_damp = glGetUniformLocation(self.program, "shineDamp")
        glUniform1fv(shine_damp, 1, tex_model.shine_damp)
        reflectivity = glGetUniformLocation(self.program, "reflectivity")
        glUniform1fv(reflectivity, 1, tex_model.reflectivity)

    def load_view_matrix(self, camera):
        matrix = self.view_matrix(camera)
        matrix_loc = glGetUniformLocation(self.program, "view_matrix")
        glUniformMatrix4fv(matrix_loc, 1, GL_FALSE, matrix)

    @staticmethod
    def view_matrix(camera):
        translation_matrix = np.matrix([
            [1, 0, 0, -camera.position[0]],
            [0, 1, 0, -camera.position[1]],
            [0, 0, 1, -camera.position[2]],
            [0, 0, 0, 1]
        ])
        rotation_matrix_x = matrix44.create_from_x_rotation(np.radians(camera.pitch))
        rotation_matrix_y = matrix44.create_from_y_rotation(np.radians(camera.yaw))
        rotation_matrix_z = matrix44.create_from_z_rotation(np.radians(camera.roll))

        tx = matrix44.multiply(translation_matrix, rotation_matrix_x)
        txy = matrix44.multiply(tx, rotation_matrix_y)
        view_matrix = matrix44.multiply(txy, rotation_matrix_z)

        return view_matrix

    @staticmethod
    def projection_matrix(fov, aspect_ratio, near, far):
        projection_matrix = np.matrix([
            [(1 / np.tan(fov / 2)) / aspect_ratio, 0, 0, 0],
            [0, 1 / np.tan(fov / 2), 0, 0],
            [0, 0, -(far + near) / (far - near), -(2 * far * near) / (far - near)],
            [0, 0, -1, 0]
        ])
        return projection_matrix

    def load_projection_matrix(self):
        projection_matrix = self.projection_matrix(45.0, (16 / 9), 0.1, 1000.0)
        matrix_loc = glGetUniformLocation(self.program, "projection_matrix")
        glUniformMatrix4fv(matrix_loc, 1, GL_FALSE, projection_matrix)