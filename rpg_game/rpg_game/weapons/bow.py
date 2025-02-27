from random import randint
from rpg_game.entities.base import Entity
from rpg_game.weapons.base import Weapon


class Bow(Weapon):
    def is_valid_attack(self, attacker: Entity, target: Entity) -> bool:
        distance = attacker.position.distance_to(target.position)
        return 2 <= distance <= 10

    def execute_attack(self, attacker: Entity, target: Entity) -> bool:
        distance = attacker.position.distance_to(target.position)
        chance = max(0, 100 - (distance - 2) * 10)

        if randint(1, 100) <= chance:
            damage = randint(10, 20)
            target.take_damage(damage)
            print(f"Лук попадает! {damage} урона.")
            return True
        print("Промах!")
        return False
