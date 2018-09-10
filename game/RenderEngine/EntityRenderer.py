from game.Model.Model import Model, TextureModel
from game.Model.OBJLoader import OBJLoader
from OpenGL.GL import *
import numpy as np
import sys
from pyrr import matrix44, Vector3


class EntityRenderer:
    def __init__(self, shader, loader):
        self.shader = shader
        self.loader = loader
        self.shader.start()
        self.shader.load_projection_matrix()
        self.shader.stop()

    def render(self, entities):
        for model in entities.keys():
            self.prepare_model(model)
            batch = entities.get(model)
            size = len(batch[0].model.vertices)
            print(size)
            for entity in batch:
                self.prepare_instance(entity)
                glDrawElements(GL_TRIANGLES, size, GL_UNSIGNED_INT, None)
            self.unbind_model(model)

    def prepare_model(self, model):
        glBindVertexArray(model.VAO)
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        if model.tex_model.has_transparency:
            self.disable_culling()
        self.load_fake_lightning_bool(model.tex_model.fake_lightning)
        self.shader.load_shine(model.tex_model)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, model.tex_model.TEX)

    def unbind_model(self, model):
        self.enable_culling()
        glDisableVertexArrayAttrib(model.VAO, 0)
        glDisableVertexArrayAttrib(model.VAO, 1)
        glDisableVertexArrayAttrib(model.VAO, 2)
        glBindVertexArray(0)

    def prepare_instance(self, entity):
        model_matrix = self.model_matrix(entity)
        glUniformMatrix4fv(self.shader.uniforms['model_matrix_loc'], 1, GL_FALSE, model_matrix)

    def create_model(self, model_name, texture, shine):
        obj = OBJLoader(model_name)
        tex_model = TextureModel(texture, shine[0], shine[1])
        model = Model(
            self.loader,
            obj.data[0],
            obj.data[1],
            obj.data[2],
            obj.data[3],
            obj.data[4],
            tex_model
        )
        return model

    @staticmethod
    def model_matrix(thing):
        translation_matrix = np.matrix([
            [1, 0, 0, thing.position[0]],
            [0, 1, 0, thing.position[1]],
            [0, 0, 1, thing.position[2]],
            [0, 0, 0, 1]
        ])
        rotation_matrix_x = matrix44.create_from_x_rotation(np.radians(thing.rotX))
        rotation_matrix_y = matrix44.create_from_y_rotation(np.radians(thing.rotY))
        rotation_matrix_z = matrix44.create_from_z_rotation(np.radians(thing.rotZ))
        scale_matrix = matrix44.create_from_scale(thing.scale)

        tx = matrix44.multiply(translation_matrix, rotation_matrix_x)
        txy = matrix44.multiply(tx, rotation_matrix_y)
        tr = matrix44.multiply(txy, rotation_matrix_z)
        model_matrix = matrix44.multiply(tr, scale_matrix)

        return model_matrix

    @staticmethod
    def enable_culling():
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

    @staticmethod
    def disable_culling():
        glDisable(GL_CULL_FACE)

    def load_fake_lightning_bool(self, _bool):
        if _bool:
            value = 1.0
        else:
            value = 0.0
        glUniform1fv(self.shader.uniforms['fake_lightning_loc'], 1, value)
