import glfw
from OpenGL.GL import *


class DisplayManager:
    def __init__(self, width, height, title):
        self.window = None

        self.nbFrames = 0
        self.lastTime = 0
        self.title = ''

        self.create_window(width, height, title)

    def create_window(self, width, height, title):
        if not glfw.init():
            return
        self.set_hints()
        self.window = glfw.create_window(width, height, title, None, None)
        glfw.make_context_current(self.window)
        glViewport(0, 0, width, height)

    def render_window(self):
        self.setWindowFPS()
        glfw.poll_events()
        glfw.swap_buffers(self.window)

    def setWindowFPS(self):
        currentTime = glfw.get_time()
        self.nbFrames += 1
        if currentTime - self.lastTime > 1.0:
            fps = str(self.nbFrames) + "fps"
            ms = str("%.2f" % (1000/self.nbFrames)) + "ms"
            self.title = fps + " | " + ms + " - pyGL"
            self.nbFrames = 0
            self.lastTime += 1.0
        glfw.set_window_title(self.window, self.title)

    def should_close(self):
        if glfw.window_should_close(self.window):
            return True
        else:
            return False

    @staticmethod
    def set_hints():
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    @staticmethod
    def terminate():
        glfw.terminate()
