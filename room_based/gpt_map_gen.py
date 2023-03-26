import re

from room_based.game_logic import Game
from room_based.map_data import *
from gpt.gpt import prompt_completion_chat


LIST_GUIDANCE = "shortened names"


def get_next_room_details(game: Game, previous_rooms: list[Room], target_biome: Biome):
    messages = [
        {"role": "system", "content": """
You are a helpful assistant that writes descriptions for a fantasy game. You help create a map for the game which is exciting and fun. You like to write in the style of Piers Anthony. You are not very verbose. You are funny and like to include jokes. You love making lists in this style:
* Item 1
* Item 2
* Item 3
""".strip()},
        {"role": "user", "content": """
The player character has embarked on an adventure into a scary world. They've just gotten to a new place, and I want you to describe it.

First, I want you to write a description of the new place in the second person. Then, I want you to list any interesting objects that appear in the scene. Then, I want you to list any monsters that appear in the scene, if any. Then, I want you to describe any structures, doorways, or paths in the place. Use a structured grammar.
""".strip()},
        {"role": "assistant", "content": f"""
You enter a vast and strange desert. Amidst the shifting sands of the desert lies an ancient edifice of stone, adorned with hieroglyphs and guarded by the spirits of the pharaohs.

Items ({LIST_GUIDANCE}):

* stone edifice
* hieroglyphics
* shifting sands

Monsters ({LIST_GUIDANCE}):

* spirits {{attitude: hostile, objective: fear}}
* dragon {{attitude: neutral, objective: acquire gold}}

Structures, Doorways, and Paths ({LIST_GUIDANCE}):

* Stone room {{width: 10, height: 5, material: stone}}
* Hidden staircase {{skill check: 15, material: stone}}
* Sandy path {{path: east-to-west, material: sand, tag: narrow}}
""".strip()},
        {"role": "user", "content": """
The character has surpassed the obstacles of the previous place, and enters a new one. This new place is a {biome}. It surely contains both danger and opportunity.

First, I want you to write a description of the new place in the second person. Then, I want you to list any interesting objects that appear in the scene. Then, I want you to list any monsters that appear in the scene, if any. Then, I want you to describe any structures, doorways, or paths in the place. Use a structured grammar.
""".format(biome=target_biome.name).strip()},
    ]
    response = prompt_completion_chat(messages=messages, n=1, temperature=0.9)
    print(response)
    return response


def parse_structured_line(string: str):
    # Define a regular expression pattern to match the dictionary-like substring
    pattern = r"{(.+)}"

    # Find the dictionary-like substring in the string
    match = re.search(pattern, string)

    text = string  # Fallback
    match_non_alphanumeric = re.search(r"[^a-zA-Z0-9]", string)
    if match_non_alphanumeric:
        text = string[:match_non_alphanumeric.start()]

    dictionary = {}

    if match:
        # Extract the dictionary-like substring
        dictionary_str = match.group(1)

        # Convert the dictionary-like substring to a dictionary
        for pair in dictionary_str.split(","):
            key, value = pair.strip().split(":")
            dictionary[key.strip()] = value.strip()

        # Extract the text before the dictionary-like substring
        text = string[:match.start()]

    dictionary["name"] = text.strip()

    return dictionary


def parse_response(game: Game, response: str):
    unknown = []
    monsters = []
    items = []
    structures = []

    current_list = unknown
    description = ""
    on_description = True

    for line in response.splitlines():
        if line.strip() == "":
            on_description = False
            continue
        line = line.strip()
        if on_description:
            description += line
        elif any(line.startswith(n) for n in ["Monsters", "Enemies", "Creatures", "Characters", "NPCs"]):
            current_list = monsters
        elif any(line.startswith(n) for n in ["Items", "Objects", "Stuff", "Things"]):
            current_list = items
        elif any(line.startswith(n) for n in ["Structures", "Doors", "Paths", "Rooms", "Areas", "Places", "Locations", "Exits"]):
            current_list = structures
        if line.startswith("* "):
            line = line[2:]
            current_list.append(parse_structured_line(line))
        else:
            pass
    return description, monsters, items, structures


if __name__ == "__main__":
    from room_based.config_loader import get_map_gen_config
    config = get_map_gen_config()
    biome = config.biomes[0]
    desc = get_next_room_details(None, [], biome)
    description, monsters, items, structures = parse_response(None, desc)
