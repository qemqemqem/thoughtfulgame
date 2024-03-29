from pygame import time

from audio.speech_synthesis import speak


class ThoughtTopic:
    # Target could be a Character or a Thing
    def __init__(self, mood: str, target):
        self.mood = mood
        self.target = target


class Thought:
    def __init__(self, text: str, perceptions: list[str] = None, topic: ThoughtTopic = None, time_start: int = None, empty=False):
        if perceptions is None:
            perceptions = []
        self.text: str = text
        self.perceptions: list[str] = perceptions
        self.topic: ThoughtTopic = topic
        self.time_start_countdown: int = time_start
        self.appear_duration: int = 15_000  # ms
        self.empty = empty  # True if it's just a placeholder thought
        self.being_replaced = False  # True if another thought has been ordered to replace this one

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
            thought = Thought(f"Loading thought {i+1}...", empty=True)
            self.current_thought_options.append(thought)
        self.default_thought: Thought = self.current_thought_options[0]
        self.thoughts_about: dict[object, list[Thought]] = {}

    def think_thought(self, thought: Thought):
        thought.perceptions.extend(self.current_perceptions)
        self.current_perceptions = []
        self.thought_history.append(thought)
        print("Thought a thought " + str(thought))

        if thought == self.default_thought:
            self.default_thought = None

        if self.default_thought is not None:
            self.default_thought.time_start_countdown = time.get_ticks()

        # Replace that thought with an empty one
        self.remove_thought_option(thought)

        # Audio
        speak(thought.text)

    def remove_thought_option(self, thought: Thought):
        for i in range(len(self.current_thought_options)):
            if self.current_thought_options[i] == thought:
                self.current_thought_options[i] = Thought(f"Loading thought {i+1}...", empty=True)
                break

    def add_thought_option(self, thought: Thought):
        thought.time_start_countdown = time.get_ticks()
        for i in range(len(self.current_thought_options)):
            if self.current_thought_options[i].empty:
                self.current_thought_options[i] = thought
                return
        self.current_thought_options.append(thought)

    def get_thought_history(self, length: int):
        return list(reversed(self.thought_history[-length:]))

    def generate_thought_options(self):
        pass

    def think_thought_options(self, option_number:int):
        self.think_thought(self.current_thought_options[option_number])