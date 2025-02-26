from abc import ABC, abstractmethod
import random


# Базовый класс сущности (SRP)
class Entity:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} получает {damage} урона!")

    def is_alive(self):
        return self.health > 0


# Интерфейс для атак (ISP)
class AttackStrategy(ABC):
    @abstractmethod
    def execute(self, attacker: Entity, target: Entity):
        pass


# Реализации атак для монстра (OCP)
class ClawAttack(AttackStrategy):
    def execute(self, attacker, target):
        damage = random.randint(10, 20)
        target.take_damage(damage)
        return f"{attacker.name} атакует когтями!"


class FireBreath(AttackStrategy):
    def execute(self, attacker, target):
        damage = random.randint(15, 25)
        target.take_damage(damage)
        return f"{attacker.name} использует огненное дыхание!"


# Реализации оружия для игрока (OCP)
class Sword:
    def attack(self, attacker, target):
        damage = random.randint(12, 22)
        target.take_damage(damage)
        return f"{attacker.name} бьёт мечом!"


class Bow:
    def attack(self, attacker, target):
        damage = random.randint(8, 18)
        target.take_damage(damage)
        return f"{attacker.name} стреляет из лука!"


# Класс игрока (SRP)
class Fighter(Entity):
    def __init__(self, name, health=100):
        super().__init__(name, health)
        self.weapon = Sword()

    def change_weapon(self, weapon):
        self.weapon = weapon
        print(f"Оружие изменено на {type(weapon).__name__}")

    def attack(self, target):
        return self.weapon.attack(self, target)


# Класс монстра (SRP)
class Monster(Entity):
    def __init__(self, name, health=50):
        super().__init__(name, health)
        self.attack_strategy = random.choice([ClawAttack(), FireBreath()])

    def set_attack_strategy(self, strategy):
        self.attack_strategy = strategy

    def attack(self, target):
        return self.attack_strategy.execute(self, target)


# Класс игры (DIP)
class Game:
    def __init__(self):
        self.player = Fighter("Герой")
        self.monster = Monster("Дракон")

    def show_status(self):
        print("\n" + "=" * 30)
        print(f"Здоровье {self.player.name}: {self.player.health}")
        print(f"Здоровье {self.monster.name}: {self.monster.health}")
        print("=" * 30)

    def player_turn(self):
        print("\nВаш ход:")
        print("1. Атаковать")
        print("2. Сменить оружие")

        choice = input("Выберите действие: ")
        if choice == '1':
            print(self.player.attack(self.monster))
        elif choice == '2':
            self.player.change_weapon(random.choice([Sword(), Bow()]))
        else:
            print("Неверный выбор!")

    def monster_turn(self):
        print("\nХод монстра:")
        print(self.monster.attack(self.player))

    def run(self):
        print("Битва начинается!")

        while self.player.is_alive() and self.monster.is_alive():
            self.show_status()
            self.player_turn()

            if self.monster.is_alive():
                self.monster_turn()

        if self.player.is_alive():
            print(f"\n{self.player.name} победил!")
        else:
            print(f"\n{self.monster.name} победил!")

# Демонстрация работы программы
if __name__ == "__main__":
    game = Game()
    game.run()