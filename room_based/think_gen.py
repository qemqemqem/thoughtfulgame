import threading

from gpt.gpt import *
from room_based.thought_data import *
from room_based.map_data import *


def _thought_gen_helper(character: Character, room: Room, num_thoughts=3):
    prompt = "You are a brave adventurer, a " + character.type + ".\n"
    prompt += "You have arrived in a place with " + room.landscape_description + ".\nIt contains these things:\n"
    dedup = []
    for th in room.things:
        if th.type not in dedup:
            dedup.append(th.type)
            prompt += "A " + th.type + ": " + th.description + "\n"
    prompt += "\nWhat do you think about this place?"
    prompt += "\nPlease write a one sentence thought that a brave adventurer might have in this place."
    thoughts = prompt_completion_chat(prompt, n=num_thoughts, temperature=0.8)
    character.thought_brain.current_thought_options = [Thought(t, perceptions=[prompt]) for t in thoughts]


def generate_thoughts(character: Character, room: Room, num_thoughts=3):
    t = threading.Thread(target=_thought_gen_helper, args=(character, room, num_thoughts))
    t.start()
