from abc import ABC, abstractmethod
from dataclasses import dataclass

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Entity(ABC):
    def __init__(self, position: Position, health: int):
        self.position = position
        self.health = health

    def take_damage(self, damage: int):
        self.health -= damage
        return self.health <= 0

    def is_alive(self) -> bool:
        return self.health > 0

    def _calculate_distance(self, other: 'Entity') -> int:
        return abs(self.position.x - other.position.x) + \
            abs(self.position.y - other.position.y)