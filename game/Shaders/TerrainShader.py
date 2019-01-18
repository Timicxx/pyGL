from OpenGL.GL import *
from OpenGL.GL.shaders import *
from pyrr import matrix44
import numpy as np


class TerrainShader:
    def __init__(self, vert_file='F:\\Git Repos\\pyGL\\game\\Assets\\shaders\\terrain.vert', frag_file='F:\\Git Repos\\pyGL\\game\\Assets\\shaders\\terrain.frag'):
        self.vert_file = vert_file
        self.frag_file = frag_file
        self.vertex_shader = None
        self.fragment_shader = None
        self.program = None

        self.create_program()
        self.uniforms = self.get_uniform_locations()

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

    def get_uniform_locations(self):
        uniforms = {}
        uniforms['light_position_loc'] = glGetUniformLocation(self.program, "lightPosition")
        uniforms['light_color_loc'] = glGetUniformLocation(self.program, "lightColor")
        uniforms['shine_damp_loc'] = glGetUniformLocation(self.program, "shineDamp")
        uniforms['reflectivity_loc'] = glGetUniformLocation(self.program, "reflectivity")
        uniforms['sky_color_loc'] = glGetUniformLocation(self.program, "skyColor")
        uniforms['view_matrix_loc'] = glGetUniformLocation(self.program, "view_matrix")
        uniforms['projection_matrix_loc'] = glGetUniformLocation(self.program, "projection_matrix")
        uniforms['model_matrix_loc'] = glGetUniformLocation(self.program, "model_matrix")
        uniforms['bg_texture_loc'] = glGetUniformLocation(self.program, "bgTexture")
        uniforms['r_texture_loc'] = glGetUniformLocation(self.program, "rTexture")
        uniforms['g_texture_loc'] = glGetUniformLocation(self.program, "gTexture")
        uniforms['b_texture_loc'] = glGetUniformLocation(self.program, "bTexture")
        uniforms['blend_map_loc'] = glGetUniformLocation(self.program, "blendMap")

        return uniforms

    def connect_texture_units(self):
        glUniform1i(self.uniforms['bg_texture_loc'], 0)
        glUniform1i(self.uniforms['r_texture_loc'], 1)
        glUniform1i(self.uniforms['g_texture_loc'], 2)
        glUniform1i(self.uniforms['b_texture_loc'], 3)
        glUniform1i(self.uniforms['blend_map_loc'], 4)

    def load_light(self, light):
        glUniform3fv(self.uniforms['light_position_loc'], 1, light.position)
        glUniform3fv(self.uniforms['light_color_loc'], 1, light.color)

    def load_shine(self, damp, reflect):
        glUniform1fv(self.uniforms['shine_damp_loc'], 1, damp)
        glUniform1fv(self.uniforms['reflectivity_loc'], 1, reflect)

    def load_sky_color(self, sky_color):
        glUniform3fv(self.uniforms['sky_color_loc'], 1, sky_color)

    def load_view_matrix(self, camera):
        matrix = self.view_matrix(camera)
        glUniformMatrix4fv(self.uniforms['view_matrix_loc'], 1, GL_FALSE, matrix)

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

        rot = np.dot(rotation_matrix_x, np.dot(rotation_matrix_y, rotation_matrix_z))
        txy = matrix44.multiply(rot, translation_matrix)
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
        glUniformMatrix4fv(self.uniforms['projection_matrix_loc'], 1, GL_FALSE, projection_matrix)
