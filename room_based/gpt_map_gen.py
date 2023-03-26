from room_based.game_logic import Game
from room_based.map_data import *
from gpt.gpt import prompt_completion_chat

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
        {"role": "assistant", "content": """
You enter a vast and strange desert. Amidst the shifting sands of the desert lies an ancient edifice of stone, adorned with hieroglyphs and guarded by the spirits of the pharaohs.

Items:

* stone edifice
* hieroglyphics
* shifting sands

Monsters:

* spirits {attitude: hostile, objective: fear}
* dragon {attitude: neutral, objective: acquire gold}

Structures, Doorways, and Paths:

* Stone room {width: 10, height: 5, material: stone}
* Hidden staircase {skill check: 15, material: stone}
* Sandy path {path: east-to-west, material: sand, tag: narrow}
""".strip()},
        {"role": "user", "content": """
The character has surpassed the obstacles of the previous place, and enters a new one. This new place is a {biome}. It surely contains both danger and opportunity.

First, I want you to write a description of the new place in the second person. Then, I want you to list any interesting objects that appear in the scene. Then, I want you to list any monsters that appear in the scene, if any. Then, I want you to describe any structures, doorways, or paths in the place. Use a structured grammar.
""".format(biome=target_biome.name).strip()},
    ]
    response = prompt_completion_chat(messages=messages, n=1, temperature=0.9)
    print(response)
    print(response)

if __name__ == "__main__":
    from room_based.config_loader import get_map_gen_config
    config = get_map_gen_config()
    biome = config.biomes[0]
    get_next_room_details(None, [], biome)
