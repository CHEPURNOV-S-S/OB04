from random import randint
from rpg_game.entities.base import Entity
from rpg_game.weapons.base import Weapon


class Bow(Weapon):
    def is_valid_attack(self, attacker: Entity, target: Entity) -> bool:
        distance = self._calculate_distance(attacker, target)
        return 2 <= distance <= 5

    def execute_attack(self, attacker: Entity, target: Entity) -> bool:
        distance = self._calculate_distance(attacker, target)
        chance = max(0, 100 - (distance - 2) * 20)

        if randint(1, 100) <= chance:
            damage = randint(10, 20)
            target.take_damage(damage)
            print(f"Лук попадает! {damage} урона.")
            return True
        print("Промах!")
        return False

    def _calculate_distance(self, attacker: Entity, target: Entity) -> int:
        return abs(attacker.position.x - target.position.x) + \
            abs(attacker.position.y - target.position.y)