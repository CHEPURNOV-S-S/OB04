from ..entities.base import Entity, Position

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