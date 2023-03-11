

class Thing:
    def __init__(self, name):
        self.name = name
        self.description = "A thing."
        self.tags = []

    def __repr__(self):
        return self.name