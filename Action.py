from abc import ABC, abstractmethod
from Ingredient import *

class Action(ABC):
    def __init__(self, target):
        self.target = target
    def get_super_name(self):
        return "Action"
    @abstractmethod
    def __str__(self):
        pass

class Cook(Action):
    def __str__(self):
        return f"Cook({str(self.target)})"


class Chop(Action):
    def __str__(self):
        return f"Chop({str(self.target)})"


class Fry(Action):
    def __str__(self):
        return f"Fry({str(self.target)})"


class Assemble(Action):
    def __init__(self, t1,t2):
        self.target = (t1,t2)

    def __str__(self):
        return f"Assemble {self.target[0]} {self.target[1]}"
