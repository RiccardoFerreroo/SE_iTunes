from dataclasses import dataclass


@dataclass
class Album:

    title: str
    id: int
    durata: float

    def __str__(self):
        return self.title
    def __repr__(self):
        return self.title
    def __hash__(self):
        return hash(self.id)