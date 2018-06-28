from OpenGL.GL import *


class Loader:
    def __init__(self):
        self.vao_list = []
        self.vbo_list = []
        self.tex_list = []

    def load(self, model):
        VAO_ID = self.create_VAO()
        self.bind_indices(model.indices)
        self.store_data(0, 3, model.vertices)
        self.store_data(1, 2, model.texture_coords)
        self.store_data(2, 3, model.normals)
        self.unbind_VAO()
        return VAO_ID

    def create_VAO(self):
        VAO_ID = glGenVertexArrays(1)
        self.vao_list.append(VAO_ID)
        glBindVertexArray(VAO_ID)
        return VAO_ID

    @staticmethod
    def unbind_VAO():
        glBindVertexArray(0)

    def setup_textures(self, model):
        TEX_ID = glGenTextures(1)
        self.tex_list.append(TEX_ID)
        glBindTexture(GL_TEXTURE_2D, TEX_ID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            model.tex_model.size[0],
            model.tex_model.size[1],
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            model.tex_model.texture
        )
        return TEX_ID

    def get_indices(self, model):
        return model.indices

    def store_data(self, attrib_index, length, data):
        VBO_ID = glGenBuffers(1)
        self.vbo_list.append(VBO_ID)
        glBindBuffer(GL_ARRAY_BUFFER, VBO_ID)
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        glVertexAttribPointer(attrib_index, length, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def bind_indices(self, data):
        VBO_ID = glGenBuffers(1)
        self.vbo_list.append(VBO_ID)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, VBO_ID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, data, GL_STATIC_DRAW)

    def clean(self):
        for vao in self.vao_list:
            glDeleteVertexArrays(1, int(vao))
        for vbo in self.vbo_list:
            glDeleteBuffers(1, int(vbo))
        for tex in self.tex_list:
            glDeleteTextures(1, int(tex))
