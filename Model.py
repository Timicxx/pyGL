import numpy as np
from PIL import Image


class Model:
    def __init__(self, vertices, texture_coords, normals, indices, tex_model):
        self.tex_model = tex_model
        self.vertices = np.array(vertices, dtype='float32')
        self.texture_coords = np.array(texture_coords, dtype='float32')
        self.normals = np.array(normals, dtype='float32')
        self.indices = np.array(indices, dtype='uint32')
        self.VAO = None


class TextureModel:
    def __init__(self, texture, reflectivity=0, shine_damp=1):
        self.size = [
            Image.open(texture).size[0],
            Image.open(texture).size[1]
        ]
        self.texture = np.array(list(Image.open(texture).convert('RGBA').getdata()), np.uint8)
        self.reflectivity = reflectivity
        self.shine_damp = shine_damp
        self.has_transparency = False
        self.fake_lightning = False
        self.TEX = None
