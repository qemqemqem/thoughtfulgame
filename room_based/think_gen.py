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
    prompt += "\nPlease write a short one sentence thought that a brave adventurer might have in this place."
    thoughts = prompt_completion_chat(prompt, n=num_thoughts, temperature=0.8)
    character.thought_brain.current_thought_options = [Thought(t, perceptions=[prompt]) for t in thoughts]


def _specific_thought_gen_helper(character: Character, prompt: str, thought_topic: ThoughtTopic):
    thoughts = prompt_completion_chat(prompt, n=1, temperature=0.8)
    character.thought_brain.add_thought_option(Thought(thoughts, perceptions=[prompt], topic=thought_topic))


def generate_specific_thoughts(character: Character, room: Room, num_thoughts=3):
    thought_topics: list[ThoughtTopic] = []
    possible_moods = ["happy", "sad", "angry", "confused", "surprised", "disgusted", "scared"]
    dedup = []
    for thing in room.things:
        if thing.type not in dedup:
            dedup.append(thing.type)
            thought_topics.append(ThoughtTopic(random.choice(possible_moods), thing))
    for ch in room.characters:
        if ch.type not in dedup:
            dedup.append(ch.type)
            thought_topics.append(ThoughtTopic(random.choice(possible_moods), ch))
    for th in thought_topics[:num_thoughts]:
        prompt = "You are a brave adventurer, a " + character.type + ".\n"
        prompt += "You have arrived in a place with " + room.landscape_description + ".\nIt contains these things:\n"
        dedup = []
        for thing in room.things:
            if thing.type not in dedup:
                dedup.append(thing.type)
                prompt += " * " + thing.type + ": " + thing.description + "\n"
        prompt += "\nYou are feeling " + th.mood + " about the " + th.target.type + ".\n"
        prompt += "\nPlease write a short one sentence thought that a brave adventurer might have about the " + th.target.type + "."
        t = threading.Thread(target=_specific_thought_gen_helper, args=(character, prompt, th))
        t.start()


def generate_thoughts(character: Character, room: Room, num_thoughts=3):
    # t = threading.Thread(target=_thought_gen_helper, args=(character, room, num_thoughts))
    # t.start()
    generate_specific_thoughts(character, room, num_thoughts)

def update_thought_timers(character: Character):
    for thought in character.thought_brain.thought_history:
        thought.time_start += 1