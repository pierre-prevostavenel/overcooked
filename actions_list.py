
from Action import Action

class Cook(Action):
    def __init__(self, targets):
        super().__init__(targets)
    def __repr__(self):
        return f"Cook({', '.join(str(t) for t in self.targets)})"


class Chop(Action):
    def __repr__(self):
        return f"Chop({', '.join(str(t) for t in self.targets)})"


class Fry(Action):
    def __repr__(self):
        return f"Fry({', '.join(str(t) for t in self.targets)})"


class Assemble(Action):
    def __repr__(self):
        return f"Assemble({', '.join(str(t) for t in self.targets)})"
