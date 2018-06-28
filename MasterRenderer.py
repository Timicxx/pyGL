from OpenGL.GL import *
from ShaderManager import ShaderManager
from EntityManager import EntityManager
from TerrainRenderer import TerrainRenderer
from TerrainShader import TerrainShader
import random


class MasterRenderer:
    def __init__(self):
        self.static_shader = ShaderManager()
        self.terrain_shader = TerrainShader()

        self.static_shader.load_projection_matrix()
        self.terrain_shader.load_projection_matrix()

        self.entity_renderer = EntityManager(self.static_shader)
        self.terrain_renderer = TerrainRenderer(self.terrain_shader)

        self.entities = {}
        self.terrains = []

    @staticmethod
    def prepare():
        #glEnable(GL_BLEND)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def render(self, light, camera):
        self.prepare()
        self.static_shader.start()
        self.static_shader.load_light(light)
        self.static_shader.load_view_matrix(camera)
        self.entity_renderer.render(self.entities)
        self.static_shader.stop()

        self.terrain_shader.start()
        self.terrain_shader.load_light(light)
        self.terrain_shader.load_view_matrix(camera)
        self.terrain_renderer.render(self.terrains)
        self.terrain_shader.stop()

        self.entities.clear()
        self.terrains.clear()

    def process_terrain(self, terrain):
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

    def gen_entity(self, model, transform):
        return self.entity_renderer.create_thing(model, transform)

    def gen_model(self, model_name, texture_name, shine):
        return self.entity_renderer.create_model(model_name, texture_name, shine)

    @staticmethod
    def gen_objects(renderer):
        objects = []
        # trees
        tree_model = renderer.gen_model("tree", "tree", [0, 10])
        for i in range(0, 100):
            x = random.uniform(0, -800)
            z = random.uniform(0, -400)
            tree = renderer.gen_entity(
                tree_model,
                [
                    [x, 0, z],
                    [0, 0, 0],
                    [5, 5, 5]
                ]
            )
            objects.append(tree)
        # low poly trees
        low_poly_tree_model = renderer.gen_model("lowPolyTree", "lowPolyTree", [0, 10])
        for i in range(0, 20):
            x = random.uniform(0, -800)
            z = random.uniform(0, -400)
            tree = renderer.gen_entity(
                low_poly_tree_model,
                [
                    [x, 0, z],
                    [0, 0, 0],
                    [1, 1, 1]
                ]
            )
            objects.append(tree)
        # grass
        grass_model = renderer.gen_model("grassModel", "grassTexture", [0, 10])
        grass_model.has_transparency = True
        grass_model.fake_lightning = True
        for i in range(0, 100):
            x = random.uniform(0, -800)
            z = random.uniform(0, -400)
            grass = renderer.gen_entity(
                grass_model,
                [
                    [x, 0, z],
                    [0, 0, 0],
                    [1, 1, 1]
                ]
            )
            grass.model.tex_model.has_transparency = True
            grass.model.tex_model.fake_lightning = True
            objects.append(grass)
        # flower
        flower_model = renderer.gen_model("grassModel", "flower", [0, 10])
        flower_model.has_transparency = True
        flower_model.fake_lightning = True
        for i in range(0, 100):
            x = random.uniform(0, -800)
            z = random.uniform(0, -400)
            flower = renderer.gen_entity(
                flower_model,
                [
                    [x, 0, z],
                    [0, 0, 0],
                    [1, 1, 1]
                ]
            )
            flower.model.tex_model.has_transparency = True
            flower.model.tex_model.fake_lightning = True
            objects.append(flower)
        # fern
        fern_model = renderer.gen_model("fern", "fern", [0, 10])
        fern_model.has_transparency = True
        for i in range(0, 100):
            x = random.uniform(0, -800)
            z = random.uniform(0, -400)
            fern = renderer.gen_entity(
                fern_model,
                [
                    [x, 0, z],
                    [0, 0, 0],
                    [1, 1, 1]
                ]
            )
            objects.append(fern)
        return objects

    def clean(self):
        self.entity_renderer.loader.clean()
        self.terrain_renderer.loader.clean()
