import openai
import os
import time
import requests
import pygame
from io import BytesIO
import threading

openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_images(prompt_list, suffix_text="White background."):
    output_dict = {}

    def generate_image(prompt):
        response = openai.Image.create(
            prompt="Pixel art " + prompt + ", suitable for use in a tile map. Stylistically similar to classic Nintendo games like Zelda. " + suffix_text,
            n=1,
            size="256x256"
        )
        image_url = response['data'][0]['url']
        image_bytes = requests.get(image_url).content
        output_dict[prompt] = image_bytes

    threads = []
    for prompt in prompt_list:
        thread = threading.Thread(target=generate_image, args=(prompt,))
        thread.start()
        threads.append(thread)
        # Note that there's a rate limit of 50 requests per second

    for thread in threads:
        thread.join()

    return output_dict


def replace_white_with_transparency(image_surface):
    if not pygame.get_init():
        pygame.display.set_mode((1, 1))  # set a temporary video mode
        pygame.init()
    image_surface.set_colorkey((255, 255, 255))
    return image_surface.convert_alpha()


def replace_mostly_white_with_transparency(image_surface, threshold=247):
    if not pygame.get_init():
        pygame.display.set_mode((1, 1))  # set a temporary video mode
    new_surface = pygame.Surface(image_surface.get_size(), pygame.SRCALPHA)
    new_surface.blit(image_surface, (0, 0))
    pixels = pygame.PixelArray(new_surface)
    for x in range(image_surface.get_width()):
        for y in range(image_surface.get_height()):
            color = pixels[x, y]
            a = (color >> 24) & 0xFF
            g = (color >> 16) & 0xFF
            b = (color >> 8) & 0xFF
            r = color & 0xFF
            if r > threshold and g > threshold and b > threshold:
                pixels[x, y] = pygame.Color(0, 0, 0, 0)  # set pixel to transparent black
    del pixels  # delete PixelArray to release lock on the surface
    return new_surface




def save_image_bytes_with_transparency(image_bytes, filename, convert_alpha=True):
    # Load the bytes into a Pygame surface
    image_io = BytesIO(image_bytes)
    image_surface = pygame.image.load(image_io)

    # Replace white with transparency
    if convert_alpha:
        image_surface = replace_mostly_white_with_transparency(image_surface)

    # Save the image with transparency to a file
    pygame.image.save(image_surface, filename)


def generate_and_save_images(prompt_list, convert_alpha = True, suffix_text="White background."):
    # Filter out prompts which are already saved as files
    prompt_list = [prompt for prompt in prompt_list if not os.path.exists(f"../images/generated/{prompt}.png")]

    output_dict = generate_images(prompt_list, suffix_text=suffix_text)

    # Save images to disk
    for prompt, image_bytes in output_dict.items():
        save_image_bytes_with_transparency(image_bytes, f"../images/generated/{prompt}.png", convert_alpha=convert_alpha)
        # with open(f"../images/generated/{prompt}.png", "wb") as f:
        #     f.write(image_bytes)


def preload_images(things):
    # Don't waste time generating images for things which already exist
    things = [th for th in things if not os.path.exists(f"../images/generated/{th}.png")]

    # Split the list into chunks of 50, because the API has a rate limit of 50 requests per second
    chunk_size = 50
    chunks = [things[i:i + chunk_size] for i in range(0, len(things), chunk_size)]
    for chunk in chunks:
        generate_and_save_images(chunk, convert_alpha=True)
        # Sleep for 1 minute
        if chunk != chunks[-1]:
            time.sleep(60)


def preload_images_from_cache():
    from gpt.file_cache_manager import StringCache
    str_cache = StringCache(cache_file="../gpt/cache.json")
    things = list(str_cache.cache.keys())
    preload_images(things)


if __name__ == "__main__":
    # unit_prompt_list = ["happy wizard", "sad wizard", "angry wizard", "duck wizard", "potato wizard"]
    # tile_prompt_list = ["tree", "rock", "water", "grass", "sand", "lava", "bridge", "door", "stairs", "chest", "sign", "torch", "fence", "wall", "house", "castle", "cave", "bridge"]
    # # Unit prompts
    # tile_prompt_list.extend(["goblin", "elf", "human", "dwarf", "orc", "dragon", "giant", "troll", "golem", "skeleton", "zombie", "ghost", "vampire", "werewolf", "demon", "angel", "unicorn"])
    # # Exotic prompts
    # tile_prompt_list.extend(["ancient arch", "imposing statue", "dark throne", "enchanted fountain", "mysterious portal", "magical tree", "enchanted forest", "enchanted castle", "enchanted cave", "enchanted bridge", "enchanted door", "enchanted stairs", "enchanted chest", "strange runes", "dragon egg", "handwritten letter", "mysterious object", "spellbook", "deck of cards"])
    # generate_and_save_images(tile_prompt_list, convert_alpha=True)  # , suffix_text="Fully colored in background.")
    preload_images_from_cache()