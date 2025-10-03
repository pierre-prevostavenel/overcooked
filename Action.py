from abc import ABC, abstractmethod

class Action(ABC):
    def __init__(self, target):
        self.target = target

    @abstractmethod
    def __repr__(self):
        pass

