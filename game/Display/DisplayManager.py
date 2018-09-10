import glfw
from OpenGL.GL import *


class DisplayManager:
    delta = 0

    def __init__(self, width, height, title):
        self.window = None
        self.title = ''
        self.last_time = 0
        self.create_window(width, height, title)

    def create_window(self, width, height, title):
        if not glfw.init():
            return
        self.set_hints()
        self.window = glfw.create_window(width, height, title, None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(0)
        glViewport(0, 0, width, height)

    def render_window(self):
        self.set_window_fps()
        self.update_delta()
        glfw.poll_events()
        glfw.swap_buffers(self.window)

    def update_delta(self):
        current_time = glfw.get_time() * 1000
        DisplayManager.delta = (current_time - self.last_time) / 1000
        self.last_time = current_time

    __nb_frames = 0
    __last_time = 0

    def set_window_fps(self):
        current_time = glfw.get_time()
        DisplayManager.__nb_frames += 1
        if current_time - DisplayManager.__last_time > 1.0:
            fps = str(DisplayManager.__nb_frames) + "fps"
            ms = str("%.2f" % (1000/DisplayManager.__nb_frames)) + "ms"
            self.title = fps + " | " + ms + " - pyGL"
            DisplayManager.__nb_frames = 0
            DisplayManager.__last_time += 1.0
        glfw.set_window_title(self.window, self.title)

    def should_close(self):
        if glfw.window_should_close(self.window):
            return True
        else:
            return False

    @staticmethod
    def set_hints():
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    @staticmethod
    def terminate():
        glfw.terminate()
