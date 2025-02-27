from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Position():
    x: int
    y: int

    def distance_to(self, other: 'Position') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def is_at(self, x: int, y: int) -> bool:
        return self.x == x and self.y == y

    def is_adjacent_to(self, other: 'Position') -> bool:
        return self.distance_to(other) == 1



class Entity(ABC):
    def __init__(self, position: Position, health: int):
        self._position = position
        self.health = health

    def take_damage(self, damage: int):
        self.health -= damage
        return self.health <= 0

    def is_alive(self) -> bool:
        return self.health > 0

    def _calculate_distance(self, other: 'Entity') -> int:
       return self.position.distance_to(other.position)

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, new_pos: Position):
        # Только простая проверка типа
        if not isinstance(new_pos, Position):
            raise TypeError("Ожидался Position")
        if new_pos != self._position:
            self._on_position_change(new_pos)
        self._position = new_pos

    def _on_position_change(self, new_pos: Position):
        print(f"{type(self).__name__} moved to {new_pos}")