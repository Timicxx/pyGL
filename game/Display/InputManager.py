import glfw
from OpenGL.GL import *


class InputManager:
    maximized = False
    wireframe = False

    def setup(self):
        glfw.set_key_callback(glfw.get_current_context(), self.key_callback)

    @staticmethod
    def key_callback(window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        if key == glfw.KEY_F11 and action == glfw.PRESS:
            if InputManager.maximized:
                glfw.restore_window(window)
                InputManager.maximized = False
            else:
                glfw.maximize_window(window)
                InputManager.maximized = True
        if key == glfw.KEY_F and action == glfw.PRESS:
            if InputManager.wireframe:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                InputManager.wireframe = False
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                InputManager.wireframe = True
