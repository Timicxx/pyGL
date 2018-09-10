from game.Display.DisplayManager import DisplayManager
import glfw
import numpy as np


class Thing:
    def __init__(self, model, position, rotX, rotY, rotZ, scale):
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


class Player(Thing):
    MOVE_SPEED = 20
    TURN_SPEED = 160
    JUMP_FORCE = 30
    GRAVITY = -50

    TERRAIN_HEIGHT = 0

    def __init__(self, model, position, rotation, scale):
        Thing.__init__(self, model, position, rotation[0], rotation[1], rotation[2], scale)
        self.window = glfw.get_current_context()
        self.current_speed = 0
        self.current_turn_speed = 0
        self.up_speed = 0
        self.isGrounded = True

    def move_player(self):
        self.key_callback()
        delta = DisplayManager.delta

        distance = self.current_speed * delta
        dx = distance * np.sin(np.radians(self.rotY))
        dz = distance * np.cos(np.radians(self.rotY))
        self.up_speed += Player.GRAVITY * delta

        self.move(dx, self.up_speed * delta, dz)
        self.rotate(0, self.current_turn_speed * delta, 0)

        if self.position[1] < Player.TERRAIN_HEIGHT:
            self.isGrounded = True
            self.up_speed = 0
            self.position[1] = Player.TERRAIN_HEIGHT

    def key_callback(self):
        if self.get_key_state(glfw.KEY_LEFT_SHIFT) is glfw.PRESS:
            Player.MOVE_SPEED = 40
        else:
            Player.MOVE_SPEED = 20

        if self.get_key_state(glfw.KEY_SPACE) is glfw.PRESS and self.isGrounded:
            self.up_speed = Player.JUMP_FORCE
            self.isGrounded = False

        if self.get_key_state(glfw.KEY_W) is glfw.PRESS:
            self.current_speed = Player.MOVE_SPEED
        elif self.get_key_state(glfw.KEY_S) is glfw.PRESS:
            self.current_speed = -Player.MOVE_SPEED
        else:
            self.current_speed = 0

        if self.get_key_state(glfw.KEY_A) is glfw.PRESS:
            self.current_turn_speed = Player.TURN_SPEED
        elif self.get_key_state(glfw.KEY_D) is glfw.PRESS:
            self.current_turn_speed = -Player.TURN_SPEED
        else:
            self.current_turn_speed = 0

    def get_key_state(self, key):
        return glfw.get_key(self.window, key)
