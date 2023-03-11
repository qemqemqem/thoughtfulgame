

class ActionLogManager:
    def __init__(self):
        self.action_history = []

    def log_action(self, action):
        self.action_history.append(action)

    def get_action_history(self, length):
        return self.action_history