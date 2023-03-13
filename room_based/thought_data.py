
class Thought:
    def __init__(self, text: str, perceptions: list[str] = None):
        if perceptions is None:
            perceptions = []
        self.text: str = text
        self.perceptions: list[str] = perceptions


class ThoughtBrain:
    def __init__(self):
        self.thought_history: list[Thought] = []
        self.current_thought_options: list[Thought] = []
        self.current_perceptions: list[str] = []
        for i in range(3):
            # thought = prompt_completion_chat(character.description, n=1, temperature=0.9)
            thought = Thought(f"Loading thought {i+1}...")
            self.current_thought_options.append(thought)

    def think_thought(self, thought: Thought):
        thought.perceptions.extend(self.current_perceptions)
        self.current_perceptions = []
        self.thought_history.append(thought)

    def get_thought_history(self, length: int):
        return list(reversed(self.thought_history[-length:]))

    def generate_thought_options(self):
        pass

    def think_thought_options(self, option_number:int):
        self.think_thought(self.current_thought_options[option_number])