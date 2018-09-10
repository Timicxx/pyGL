from game.Display.DisplayManager import DisplayManager
from game.RenderEngine.MasterRenderer import MasterRenderer
from game.Entities.Light import Light
from game.Entities.Camera import Camera
from game.Entities.Thing import Player
from game.Display.InputManager import InputManager
import numpy as np

display_manager = DisplayManager(1280, 720, "pyGL")
input_manager = InputManager()
renderer = MasterRenderer()


def main():
    light = Light([20000, 20000, 20000], [1, 1, 1])
    camera = Camera()
    terrains = renderer.gen_terrains()
    objects = renderer.gen_objects()

    player_model_texture = renderer.gen_texture("transparent")
    player_model = renderer.gen_model("zt", player_model_texture, [0, 10])
    player = Player(
        player_model,
        [100, 0, -50],
        [0, 0, 0],
        [0.25, 0.25, 0.25]
    )
    objects.append(player)

    input_manager.setup()
    while not display_manager.should_close():
        camera.position[0] = player.position[0]
        camera.position[1] = player.position[1] + 5
        camera.position[2] = player.position[2]
        camera.yaw = -player.rotY + 180
        player.move_player()
        for object in objects:
            renderer.process_entity(object)
        for terrain in terrains:
            renderer.process_terrain(terrain)
        renderer.render(light, camera)
        display_manager.render_window()
    renderer.clean()
    display_manager.terminate()


if __name__ == '__main__':
    main()
