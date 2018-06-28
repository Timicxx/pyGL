import glfw
from OpenGL.GL import *


maximized = False
wireframe = False


def setup():
    glfw.set_key_callback(glfw.get_current_context(), key_callback)


def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if key == glfw.KEY_F11 and action == glfw.PRESS:
        global maximized
        if maximized:
            glfw.restore_window(window)
            maximized = False
        else:
            glfw.maximize_window(window)
            maximized = True
    if key == glfw.KEY_F and action == glfw.PRESS:
        global wireframe
        if wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            wireframe = False
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            wireframe = True
