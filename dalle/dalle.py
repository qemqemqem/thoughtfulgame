import openai
import os
import time
import requests
import pygame
from io import BytesIO
import threading

openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_images(prompt_list: list[str], prompt_str=""):
    output_dict = {}
    if prompt_str == "":
        prompt_str = "Pixel art {thing}. 8 bit. Classic Nintendo. White Background. "

    def generate_image(prompt):
        response = openai.Image.create(
            prompt=prompt_str.format(thing=prompt.capitalize()),
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


# This function does two things at once because it's faster to do them together
def postprocess_image(image_surface, threshold=247, desaturation=0.0, lighten=0.0, decontrast=0.0):
    if not pygame.get_init():
        pygame.display.set_mode((1, 1))  # set a temporary video mode
    new_surface = pygame.Surface(image_surface.get_size(), pygame.SRCALPHA)
    new_surface.blit(image_surface, (0, 0))
    pixels = pygame.PixelArray(new_surface)
    if desaturation > 0.0 and lighten != 0.0:
        decontrast = (desaturation + abs(lighten)) / 2
    for x in range(image_surface.get_width()):
        for y in range(image_surface.get_height()):
            color = pixels[x, y]
            a = (color >> 24) & 0xFF
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            # Convert white to transparency before messing with it
            if r > threshold and g > threshold and b > threshold:
                pixels[x, y] = pygame.Color(0, 0, 0, 0)  # set pixel to transparent black
                continue
            if desaturation > 0.0:
                # Desaturate the color
                avg = (r + g + b) / 3
                r = int(r * (1 - desaturation) + avg * desaturation)
                g = int(g * (1 - desaturation) + avg * desaturation)
                b = int(b * (1 - desaturation) + avg * desaturation)
            if lighten > 0.0:
                # Lighten the color
                r = int(r * (1 - lighten) + 255 * lighten)
                g = int(g * (1 - lighten) + 255 * lighten)
                b = int(b * (1 - lighten) + 255 * lighten)
            if lighten < 0.0:
                # Darken the color
                r = int(r * (1 + lighten))
                g = int(g * (1 + lighten))
                b = int(b * (1 + lighten))
            if decontrast > 0.0:
                # Decontrast the color
                avg = 100
                r = int(r * (1 - decontrast) + avg * decontrast)
                g = int(g * (1 - decontrast) + avg * decontrast)
                b = int(b * (1 - decontrast) + avg * decontrast)
            if lighten > 0.0 or desaturation > 0.0:
                pixels[x, y] = pygame.Color(r, g, b, a)
    del pixels  # delete PixelArray to release lock on the surface
    return new_surface


def save_image_bytes_with_transparency(image_bytes, filename, convert_alpha=True, desaturation=0.0, lighten=0.0):
    # Load the bytes into a Pygame surface
    image_io = BytesIO(image_bytes)
    image_surface = pygame.image.load(image_io)

    # Replace white with transparency
    if convert_alpha or desaturation > 0 or lighten > 0:
        image_surface = postprocess_image(image_surface, desaturation=desaturation, lighten=lighten, threshold=250 if convert_alpha else 256)

    # Save the image with transparency to a file
    pygame.image.save(image_surface, filename)


def generate_and_save_images(prompt_list, convert_alpha=True, force_reload=False, desaturation=0.0, lighten=0.0, prompt_str=""):
    # Filter out prompts which are already saved as files
    if not force_reload:
        prompt_list = [prompt for prompt in prompt_list if not os.path.exists(f"../images/generated/{prompt}.png")]

    output_dict = generate_images(prompt_list, prompt_str=prompt_str)

    # Save images to disk
    for prompt, image_bytes in output_dict.items():
        save_image_bytes_with_transparency(image_bytes, f"../images/generated/{prompt}.png", convert_alpha=convert_alpha, desaturation=desaturation, lighten=lighten)
        print("Saving image: ", prompt, "to file", f"../images/generated/{prompt}.png")
        # with open(f"../images/generated/{prompt}.png", "wb") as f:
        #     f.write(image_bytes)


def preload_images(things, force_reload=False, desaturation=0.0, prompt_str="", convert_alpha=True, lighten=0.0):
    # Don't waste time generating images for things which already exist
    if not force_reload:
        things = [th for th in things if not os.path.exists(f"../images/generated/{th}.png")]

    # Split the list into chunks of 50, because the API has a rate limit of 50 requests per second
    chunk_size = 49
    chunks = [things[i:i + chunk_size] for i in range(0, len(things), chunk_size)]
    for chunk in chunks:
        generate_and_save_images(chunk, convert_alpha=convert_alpha, force_reload=force_reload, desaturation=desaturation, lighten
        =lighten, prompt_str=prompt_str)
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
