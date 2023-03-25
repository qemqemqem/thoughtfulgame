
class ThoughtTopic:
    # Target could be a Character or a Thing
    def __init__(self, mood: str, target):
        self.mood = mood
        self.target = target


class Thought:
    def __init__(self, text: str, perceptions: list[str] = None, topic: ThoughtTopic = None):
        if perceptions is None:
            perceptions = []
        self.text: str = text
        self.perceptions: list[str] = perceptions
        self.topic: ThoughtTopic = topic

    def __str__(self):
        if self.topic is not None:
            return f"[{self.topic.mood.capitalize()} about {self.topic.target}]: {self.text}"
        else:
            return self.text


class ThoughtBrain:
    def __init__(self):
        self.thought_history: list[Thought] = []
        self.current_thought_options: list[Thought] = []
        self.current_perceptions: list[str] = []
        for i in range(3):
            # thought = prompt_completion_chat(character.description, n=1, temperature=0.9)
            thought = Thought(f"Loading thought {i+1}...")
            self.current_thought_options.append(thought)
        self.thoughts_about: dict[object, list[Thought]] = {}

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