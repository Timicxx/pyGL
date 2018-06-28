import glfw


class Camera:
    def __init__(self):
        self.position = [0, 0, 0]
        self.pitch = 0
        self.yaw = 0
        self.roll = 0

    def move(self):
        window = glfw.get_current_context()
        move_speed = 0.2
        if glfw.get_key(window, glfw.KEY_LEFT_SHIFT):
            move_speed = 0.75
        if glfw.get_key(window, glfw.KEY_W):
            self.position[2] -= move_speed
        if glfw.get_key(window, glfw.KEY_S):
            self.position[2] += move_speed
        if glfw.get_key(window, glfw.KEY_A):
            self.position[0] -= move_speed
        if glfw.get_key(window, glfw.KEY_D):
            self.position[0] += move_speed
        if glfw.get_key(window, glfw.KEY_SPACE):
            self.position[1] += move_speed
        if glfw.get_key(window, glfw.KEY_LEFT_CONTROL):
            self.position[1] -= move_speed
