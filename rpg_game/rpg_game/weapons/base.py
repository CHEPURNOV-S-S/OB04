from abc import ABC, abstractmethod
from rpg_game.entities.base import Entity

class Weapon(ABC):
    @abstractmethod
    def is_valid_attack(self, attacker: Entity, target: Entity) -> bool:
        pass

    @abstractmethod
    def execute_attack(self, attacker: Entity, target: Entity) -> bool:
        pass