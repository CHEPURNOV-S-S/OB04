from ..entities.base import Entity, Position
from ..weapons.base import Weapon
import random

class Monster(Entity):
    def __init__(self, position: Position):
        super().__init__(position, health=50)

    def take_damage(self, damage: int):
        self.health -= damage
        if self.health < 0: self.health = 0

    def attack(self, target: Entity):
        if self.calculate_distance(target) == 1:
            damage = random.randint(10, 20)
            target.take_damage(damage)
            print(f"Монстр атакует! {damage} урона.")