

class ThoughtManager:
    def __init__(self):
        self.thought_history = []
        self.current_thought_options = []

    def think_thought(self, thought):
        self.thought_history.append(thought)

    def get_thought_history(self, length):
        return list(reversed(self.thought_history[-length:]))

    def generate_thought_options(self):
        pass

    def think_thought_options(self, option_number:int):
        self.think_thought(self.current_thought_options[option_number])