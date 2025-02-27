from rpg_game.weapons.base import Weapon
from rpg_game.entities.base import Entity
import random

class Sword(Weapon):
    def is_valid_attack(self, attacker: Entity, target: Entity) -> bool:
        distance = attacker.position.distance_to(target.position)
        return distance == 1

    def execute_attack(self, attacker: Entity, target: Entity) -> bool:
        damage = random.randint(15, 25)
        target.take_damage(damage)
        print(f"Меч наносит {damage} урона!")
        return True