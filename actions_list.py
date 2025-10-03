
from Action import Action

class Cook(Action):
    def __repr__(self):
        return f"Cook({', '.join(str(t) for t in self.targets)})"


class Chop(Action):
    def __repr__(self):
        return f"Chop({', '.join(str(t) for t in self.targets)})"


class Fry(Action):
    def __repr__(self):
        return f"Fry({', '.join(str(t) for t in self.targets)})"


class Assemble(Action):
    def __init__(self, t1,t2):
        self.target = (t1,t2)

    def __repr__(self):
        return f"Assemble({', '.join(str(t) for t in self.targets)})"
