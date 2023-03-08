

def generate_prompt_from_unknown_items(unknown_items):
    examples = {"cat, dog, bird": "I would like to pet that cat",
                "dragon, sword, shield": "I would like to attack that dragon with my sword",
                "wizard, gate, cat": "I should ask that wizard about the gate",
                "stable, pylon, djinn": "That djinn looks dangerous",
                "village, traffic cone": "I'm hungry",
                "evil looking tree, bat, ghost": "I'm scared"}

    present_things = "I see: "
    thought_prompt = "\nAnd I think that: "
    thought_terminator = ". DONE\n\n"

    demonstration_with_examples = ""
    for example in examples:
        demonstration_with_examples += present_things + example + thought_prompt + examples[example] + thought_terminator

    full_prompt = demonstration_with_examples + present_things + ", ".join(unknown_items) + thought_prompt
    return full_prompt