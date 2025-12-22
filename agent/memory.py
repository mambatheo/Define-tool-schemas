class SessionMemory:
    def __init__(self):
        self.context = []

    def store_context(self, message):
        self.context.append(message)
