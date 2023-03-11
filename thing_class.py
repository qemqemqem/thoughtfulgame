from gpt import prompt_completion

class Thing:
    def fill_description(self):
        prompt = "What is the description of " + self.name + "?"
        self.description = prompt_completion(prompt)

    def __init__(self, name, cache=None):
        self.name = name
        self.description = "A thing."
        self.tags = []
        if cache is not None:
            self.description = cache.get(name)
        else:
            self.fill_description()

    def __repr__(self):
        return self.name