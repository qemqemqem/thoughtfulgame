import threading
import pygame

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
        if thing.type not in dedup and thing.interesting:
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


def generate_thoughts(character: Character, room: Room):
    num_empty_thoughts = 0
    for t in character.thought_brain.current_thought_options:
        if t.empty and not t.being_replaced:
            num_empty_thoughts += 1
            t.being_replaced = True
    # t = threading.Thread(target=_thought_gen_helper, args=(character, room, num_thoughts))
    # t.start()
    generate_specific_thoughts(character, room, num_empty_thoughts)


def update_thought_timers(character: Character, game):
    # See if any thoughts get thunk
    for thought in character.thought_brain.current_thought_options:
        if thought.time_start_countdown is not None and not thought.empty:
            age = time.get_ticks() - thought.time_start_countdown
            if age > thought.appear_duration:
                if thought == character.thought_brain.default_thought:
                    character.thought_brain.think_thought(thought)
                else:
                    character.thought_brain.remove_thought_option(thought)

    # If the player pressed a number key, then think that thought
    # Check if the player pressed the number 1 key, using pygame:
    pressed_keys = pygame.key.get_pressed()
    keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
    for i in range(len(keys)):
        if pressed_keys[keys[i]]:
            if i < len(character.thought_brain.current_thought_options):
                if not character.thought_brain.current_thought_options[i].empty:
                    character.thought_brain.think_thought(character.thought_brain.current_thought_options[i])

    # Replace any thoughts that need it
    generate_thoughts(character, game.room)

    # Assign a default if none
    if character.thought_brain.default_thought is None or character.thought_brain.default_thought.empty:
        for to in character.thought_brain.current_thought_options:
            if not to.empty:
                character.thought_brain.default_thought = to
                to.time_start_countdown = time.get_ticks()
                break
