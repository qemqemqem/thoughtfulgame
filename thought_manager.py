

class ThoughtManager:
    def __init__(self):
        self.thought_history = []

    def think_thought(self, thought):
        self.thought_history.append(thought)