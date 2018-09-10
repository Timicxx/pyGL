from OpenGL.GL import *
from game.Shaders.StaticShader import StaticShader
from game.RenderEngine.EntityRenderer import EntityRenderer
from game.RenderEngine.TerrainRenderer import TerrainRenderer
from game.Shaders.TerrainShader import TerrainShader
from game.Terrain.Terrain import Terrain, TerrainTexture, TerrainTexturePack
from game.Model.Model import TextureModel
from game.Model.Loader import Loader
from game.Entities.Thing import Thing
import random
import numpy as np


class MasterRenderer:
    def __init__(self):
        self.static_shader = StaticShader()
        self.terrain_shader = TerrainShader()

        self.loader = Loader()

        self.entity_renderer = EntityRenderer(self.static_shader, self.loader)
        self.terrain_renderer = TerrainRenderer(self.terrain_shader, self.loader)

        self.entities = {}
        self.terrains = []

        self.sky_color = [0.5, 0.75, 0.9]

    def prepare(self):
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glClearColor(self.sky_color[0], self.sky_color[1], self.sky_color[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def render(self, light, camera):
        self.prepare()

        self.static_shader.start()
        self.static_shader.load_light(light)
        self.static_shader.load_view_matrix(camera)
        self.static_shader.load_sky_color(self.sky_color)
        self.entity_renderer.render(self.entities)
        self.static_shader.stop()

        self.terrain_shader.start()
        self.terrain_shader.load_light(light)
        self.terrain_shader.load_view_matrix(camera)
        self.terrain_shader.load_sky_color(self.sky_color)
        self.terrain_renderer.render(self.terrains)
        self.terrain_shader.stop()

        self.entities.clear()
        self.terrains.clear()

    def process_terrain(self, terrain):
        if terrain not in self.terrains:
            self.terrains.append(terrain)

    def process_entity(self, entity):
        entity_model = entity.model
        batch = self.entities.get(entity_model)
        if batch is not None:
            batch.append(entity)
        else:
            new_batch = []
            new_batch.append(entity)
            self.entities.update({entity_model: new_batch})

    def gen_model(self, model_name, texture, shine):
        return self.entity_renderer.create_model(model_name, texture, shine)

    def gen_terrains(self):
        terrains = []
        loader = self.loader
        bg_terrain_texmodel = TextureModel(self.gen_texture("grassy2"))
        bg_terrain = TerrainTexture(loader.setup_textures(bg_terrain_texmodel))
        r_terrain_texmodel = TextureModel(self.gen_texture("mud"))
        r_terrain = TerrainTexture(loader.setup_textures(r_terrain_texmodel))
        g_terrain_texmodel = TextureModel(self.gen_texture("grassFlowers"))
        g_terrain = TerrainTexture(loader.setup_textures(g_terrain_texmodel))
        b_terrain_texmodel = TextureModel(self.gen_texture("path"))
        b_terrain = TerrainTexture(loader.setup_textures(b_terrain_texmodel))

        texture_pack = TerrainTexturePack(bg_terrain, r_terrain, g_terrain, b_terrain)

        blend_map_texmodel = TextureModel(self.gen_texture("blendMap"))
        blend_map = TerrainTexture(loader.setup_textures(blend_map_texmodel))

        terrain1 = Terrain([0, 0], loader, texture_pack, blend_map)
        terrains.append(terrain1)
        terrain2 = Terrain([0, -1], loader, texture_pack, blend_map)
        terrains.append(terrain2)
        terrain3 = Terrain([-1, 0], loader, texture_pack, blend_map)
        terrains.append(terrain3)
        terrain4 = Terrain([-1, -1], loader, texture_pack, blend_map)
        terrains.append(terrain4)
        return terrains

    def gen_texture(self, file):
        from PIL import Image
        import numpy as np
        path = "F:\\GitHub\\pyGL\\game\\Assets\\res\\" + file + ".png"
        image = Image.open(path)
        tex = np.array(list(image.convert('RGBA').getdata()), np.uint8)
        size = [
            image.size[0],
            image.size[1]
        ]
        texture = [
            tex,
            size
        ]
        return texture

    def gen_objects(self):
        objects = []
        tree_model = self.gen_model("tree", self.gen_texture("tree"), [0, 100])
        #low_poly_tree_model = self.gen_model("lowPolyTree", self.gen_texture("lowPolyTree"), [0, 10])
        #grass_model = self.gen_model("grassModel", self.gen_texture("grassTexture"), [0, 10])
        #flower_model = self.gen_model("grassModel", self.gen_texture("flower"), [0, 10])
        #fern_model = self.gen_model("fern", self.gen_texture("fern"), [0, 10])

        for i in range(0, 500):
            x = random.uniform(-800, 800)
            z = random.uniform(-800, 800)
            tree = Thing(
                tree_model,
                [x, 0, z],
                0, 0, 0,
                [5, 5, 5]
            )
            objects.append(tree)
            # x = random.uniform(-800, 800)
            # z = random.uniform(-800, 800)
            # tree = Thing(
            #     low_poly_tree_model,
            #     [x, 0, z],
            #     0, 0, 0,
            #     [1, 1, 1]
            # )
            # objects.append(tree)
            # x = random.uniform(-800, 800)
            # z = random.uniform(-800, 800)
            # grass = Thing(
            #     grass_model,
            #     [x, 0, z],
            #     0, 0, 0,
            #     [1, 1, 1]
            # )
            # objects.append(grass)
            # x = random.uniform(-800, 800)
            # z = random.uniform(-800, 800)
            # flower = Thing(
            #     flower_model,
            #     [x, 0, z],
            #     0, 0, 0,
            #     [1, 1, 1]
            # )
            # objects.append(flower)
            # x = random.uniform(-800, 800)
            # z = random.uniform(-800, 800)
            # fern = Thing(
            #     fern_model,
            #     [x, 0, z],
            #     0, 0, 0,
            #     [1, 1, 1]
            # )
            # objects.append(fern)
        #grass_model.has_transparency = True
        #grass_model.fake_lightning = True
        #flower_model.has_transparency = True
        #flower_model.fake_lightning = True
        #fern_model.has_transparency = True

        return objects

    def clean(self):
        self.loader.clean()
