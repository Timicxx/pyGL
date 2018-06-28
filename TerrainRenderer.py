from OpenGL.GL import *
import numpy as np
from pyrr import matrix44
from Loader import Loader


class TerrainRenderer:
    def __init__(self, shader):
        self.shader = shader
        self.shader.start()
        self.loader = Loader()
        self.shader.load_projection_matrix()
        self.shader.stop()

    def render(self, terrains):
        for terrain in terrains:
            self.prepare_terrain(terrain)
            self.load_model_matrix(terrain)
            glDrawElements(GL_TRIANGLES, terrain.indices, GL_UNSIGNED_INT, None)
            self.unbind_model(terrain)

    def prepare_terrain(self, terrain):
        glBindVertexArray(terrain.model)
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        self.shader.load_shine(terrain.texture)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, terrain.texture.TEX)

    @staticmethod
    def unbind_model(terrain):
        glDisableVertexArrayAttrib(terrain.model, 0)
        glDisableVertexArrayAttrib(terrain.model, 1)
        glDisableVertexArrayAttrib(terrain.model, 2)
        glBindVertexArray(0)

    def load_model_matrix(self, terrain):
        model_matrix = self.model_matrix(terrain)
        matrix_loc = glGetUniformLocation(self.shader.program, "model_matrix")
        glUniformMatrix4fv(matrix_loc, 1, GL_FALSE, model_matrix)

    @staticmethod
    def model_matrix(terrain):
        translation_matrix = np.matrix([
            [1, 0, 0, terrain.x],
            [0, 1, 0, 0],
            [0, 0, 1, terrain.z],
            [0, 0, 0, 1]
        ])
        rotation_matrix_x = matrix44.create_from_x_rotation(np.radians(0))
        rotation_matrix_y = matrix44.create_from_y_rotation(np.radians(0))
        rotation_matrix_z = matrix44.create_from_z_rotation(np.radians(0))
        scale_matrix = matrix44.create_from_scale([1, 1, 1])

        tx = matrix44.multiply(translation_matrix, rotation_matrix_x)
        txy = matrix44.multiply(tx, rotation_matrix_y)
        tr = matrix44.multiply(txy, rotation_matrix_z)
        model_matrix = matrix44.multiply(tr, scale_matrix)

        return model_matrix
