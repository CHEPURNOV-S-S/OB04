from ..entities.base import Entity, Position
from ..weapons.base import Weapon


class Fighter(Entity):
    def __init__(self, position: Position, max_ap: int):
        super().__init__(position, health=100)
        self.max_ap = max_ap
        self.current_ap = max_ap
        self.weapon = None  # Начальное оружие
        self.carried_over_ap = 0

    def reset_ap(self):
        """Пересчет ОД после хода"""
        remaining = self.current_ap
        self.carried_over_ap = remaining // 2
        max_possible = int(self.max_ap * 1.5)
        self.current_ap = min(self.max_ap + self.carried_over_ap, max_possible)

    def move(self, direction: str) -> bool:
        """Перемещение с проверкой границ"""
        new_x, new_y = self.position.x, self.position.y
        if direction == 'n': new_y -= 1
        elif direction == 's': new_y += 1
        elif direction == 'e': new_x += 1
        elif direction == 'w': new_x -= 1
        else: return False

        if 0 <= new_x < 10 and 0 <= new_y < 10:
            self.position = Position(new_x, new_y)
            self.current_ap -= 1
            return True
        return False

    def change_weapon(self, weapon) -> bool:
        """Смена оружия (1 ОД)"""
        if self.current_ap >= 1:
            self.weapon = weapon
            self.current_ap -= 1
            return True
        return False

    def attack(self, target: Entity) -> bool:
        if not self.weapon:  # Дополнительная проверка
            return False
        if self.current_ap < 1:
            return False

        if self.weapon.is_valid_attack(self, target):
            if self.weapon.execute_attack(self, target):
                self.current_ap -= 1
                return True
        return False

    def take_damage(self, damage: int):
        self.health -= damage
        if self.health < 0: self.health = 0