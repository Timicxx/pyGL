class Thing:
    def __init__(self, model, position, rotX, rotY, rotZ, scale):
        self.id = id
        self.model = model
        self.position = position
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
        self.scale = scale

    def move(self, dx, dy, dz):
        self.position[0] += dx
        self.position[1] += dy
        self.position[2] += dz

    def rotate(self, dx, dy, dz):
        self.rotX += dx
        self.rotY += dy
        self.rotZ += dz

    def rescale(self, dx, dy, dz):
        self.scale[0] += dx
        self.scale[1] += dy
        self.scale[2] += dz

