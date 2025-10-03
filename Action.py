from abc import ABC, abstractmethod

class Action(ABC):
    def __init__(self, targets):
        if not isinstance(targets, list):
            targets = [targets]
        self.targets = targets  # Liste d’Ingredients ou d’Actions

    @abstractmethod
    def __repr__(self):
        pass

