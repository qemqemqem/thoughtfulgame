import json

from gpt.file_cache_manager import DEFAULT_CACHE_FILE_NAME
from room_based.map_data import *
from gpt.preload_descriptions import generate_descriptions
from dalle.dalle import preload_images

DEFAULT_MAP_GEN_CONFIG_FILE = "map_gen_config.json"


def save_mapgenconfig(config, file_path):
    with open(file_path, 'w') as f:
        json.dump(config.__dict__, f, default=serialize_biome, indent=4)


def load_mapgenconfig(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        config = MapGenConfig()
        for biome_data in data['biomes']:
            config.biomes.append(deserialize_biome(biome_data))
        return config


def serialize_biome(biome):
    if isinstance(biome, Biome):
        return biome.__dict__
    return biome


def deserialize_biome(biome_data):
    if 'name' in biome_data:
        biome = Biome(biome_data['name'])
        biome.__dict__.update(biome_data)
        return biome
    return biome_data


class CacheFiller:
    def __init__(self):
        self.names = []

    def cache_image_and_text(self, biome: Biome, image):
        self.names.append(biome.format_name(image))

    def cache_image_and_text_for_config(self, config):
        for biome in config.biomes:
            for image in biome.tree_images:
                self.cache_image_and_text(biome, image)
            for image in biome.rock_images:
                self.cache_image_and_text(biome, image)
            for image in biome.ground_images:
                self.cache_image_and_text(biome, image)
            for image in biome.water_images:
                self.cache_image_and_text(biome, image)
            for image in biome.wall_images:
                self.cache_image_and_text(biome, image)
        self.preload_descriptions()
        self.preload_images()

    def preload_descriptions(self):
        generate_descriptions(self.names, "../gpt/" + DEFAULT_CACHE_FILE_NAME)

    def preload_images(self):
        preload_images(self.names)


if __name__ == "__main__":
    gen_data = MapGenConfig()
    b1 = Biome("Forest")
    b1.tree_level = 0.7
    b1.water_level = 0.15
    b1.rock_density = 0.05
    b1.monster_types = ["goblin", "orc", "troll", "giant spider", "giant rat", "bat", "wolf", "elf", "velociraptor", "centipede"]
    b1.object_types = ["gemstones", "hut", "eyestalk", "great pyramid", "crypt entrance", "cave entrance", "bird house", "tree house", "well", "fountain", "statue", "grave"]
    b1.tree_images = ["gnarled tree", "acorn tree", "yew tree", "fruit tree", "oak tree", "beech tree"]
    b1.rock_images = ["boulder", "rock", "stone"]
    b1.ground_images = ["grass", "dirt", "fallen leaves", "moss"]
    b1.water_images = ["still water", "stagnant water", "swamp water"]
    b1.wall_images = ["wooden wall", "stone wall", "brick wall", "cobblestone wall"]
    gen_data.biomes.append(b1)

    # Save to file
    save_mapgenconfig(gen_data, "map_gen_config.json")

    # Load from file
    gen_data = load_mapgenconfig("map_gen_config.json")

    # Cache filler
    filler = CacheFiller()
    filler.cache_image_and_text_for_config(gen_data)
