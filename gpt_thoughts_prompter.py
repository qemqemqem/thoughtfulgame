import thing_class


def generate_prompt_from_unknown_items(unknown_items: list[thing_class.Thing]):
    descriptions = {}
    for item in unknown_items:
        descriptions[item.name] = item.description

    examples = {"cat, dog, bird": "I would like to pet that cat",
                "dragon, sword, shield": "I would like to attack that dragon with my sword",
                "wizard, gate, cat": "I should ask that wizard about the gate",
                "stable, pylon, djinn": "That djinn looks dangerous",
                "village, traffic cone": "I'm hungry",
                "evil looking tree, bat, ghost": "I'm scared"}

    descriptions_prompt = "Here are detailed descriptions of some of the things around you:\n"
    present_things = "I see: "
    thought_prompt = "\nAnd I think that: "
    thought_terminator = ". DONE\n\n"

    demonstration_with_examples = ""
    demonstration_with_examples += descriptions_prompt + "\n".join([item_name + ", " + descriptions[item_name] for item_name in descriptions.keys()]) + "\n\n"
    for example in examples:
        demonstration_with_examples += present_things + example + thought_prompt + examples[example] + thought_terminator

    full_prompt = demonstration_with_examples + present_things + ", ".join([th.name for th in unknown_items]) + thought_prompt
    return full_prompt

# The target is something like this:

# Descriptions:
# cat: A small furry animal that likes to eat mice and sleep on your bed.
# dog: A large furry animal that likes to eat bones and sleep on your bed.
# bird: A small flying animal that likes to eat worms and sleep on your bed.
# dragon: A large flying animal that likes to eat princesses and sleep on your bed.
# Examples:
# "cat, dog, bird": "I would like to pet that cat",
# "dragon, sword, shield": "I would like to attack that dragon with my sword",
# "wizard, gate, cat": "I should ask that wizard about the gate",
# "stable, pylon, djinn": "That djinn looks dangerous",
# "village, traffic cone": # AUTOCOMPLETION HAPPENS HERE

# Here's a version that's more location-description specific:

# You are in: A sun filled chamber with arches that open out to the vast rolling hills of Almandine.
# You see:
# A man in gold sits upon a marble throne and eyes you suspiciously.
# His parrot squawks at you