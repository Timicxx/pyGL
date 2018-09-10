import numpy as np


class Model:
    def __init__(self, loader, vertices, texture_coords, normals, indices, furthest, tex_model):
        self.tex_model = tex_model
        self.vertices = np.array(vertices, dtype='float32')
        self.texture_coords = np.array(texture_coords, dtype='float32')
        self.normals = np.array(normals, dtype='float32')
        self.indices = np.array(indices, dtype='uint32')
        self.furthest = furthest
        self.VAO = loader.load(self)

        if tex_model is not None:
            self.tex_model.TEX = loader.setup_textures(self.tex_model)


class TextureModel:
    def __init__(self, texture, reflectivity=0, shine_damp=1):
        self.size = [
            texture[1][0],
            texture[1][1]
        ]
        self.texture = texture[0]
        self.reflectivity = reflectivity
        self.shine_damp = shine_damp
        self.has_transparency = False
        self.fake_lightning = False
        self.TEX = None
