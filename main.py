from DisplayManager import DisplayManager
from MasterRenderer import MasterRenderer
from Light import Light
from Terrain import Terrain
from Camera import Camera
import InputManager as im
import random

display_manager = DisplayManager(1280, 720, "pyGL")
renderer = MasterRenderer()


def main():
    light = Light([20000, 20000, 20000], [1, 1, 1])
    camera = Camera()
    camera.position[1] = 5
    terrain = Terrain([-0.5, -0.5], renderer.terrain_renderer.loader, "grass")
    objects = renderer.gen_objects(renderer)

    im.setup()
    while not display_manager.should_close():
        camera.move()
        for object in objects:
            renderer.process_entity(object)
        renderer.process_terrain(terrain)
        renderer.render(light, camera)
        display_manager.render_window()
    renderer.clean()
    display_manager.terminate()


if __name__ == __name__:
    main()
