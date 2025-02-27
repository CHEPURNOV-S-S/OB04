import random

from rpg_game.entities.fighter import Fighter
from rpg_game.entities.monster import Monster
from rpg_game.weapons.sword import Sword
from rpg_game.weapons.bow import Bow
from rpg_game.entities.base import Position

from .movement import MovementManager
from .renderer import Renderer
from .constants import MAP_SIZE


class Game:
    def __init__(self):
        self.renderer = Renderer(self)
        # Начальная позиция игрока (центр северной границы)
        self.fighter = Fighter(Position(5, 0), max_ap=5)
        # Случайная позиция монстра
        while True:
            x, y = random.randint(0,9), random.randint(0,9)
            if not (x == 5 and y == 0):
                break
        self.monster = Monster(Position(x, y))

        self.movement = MovementManager(MAP_SIZE)

    def _check_game_over(self) -> bool:
        """Проверка условий окончания игры"""
        if not self.fighter.is_alive():
            print("Вы погибли...")
            return True
        if not self.monster.is_alive():
            print("Монстр повержен!")
            return True
        return False

    def _process_player_input(self):
        """Обработка действий игрока"""
        while True:
            try:
                action = input("Выберите действие (1-4): ")
                if action == '1':
                    self._handle_movement()
                elif action == '2':
                    self._handle_weapon_change()
                elif action == '3':
                    self._handle_attack()
                elif action == '4':
                    self._save_game()
                else:
                    print("Неверный ввод!")
                break
            except Exception as e:
                print(f"Ошибка: {str(e)}")

    def _handle_movement(self):
        direction = input("Направление (n/s/e/w): ")
        if self.movement.move_entity(self.fighter, direction):
            print("Перемещение выполнено.")
        else:
            print("Невозможно переместиться!")

    def _handle_weapon_change(self):
        weapon_type = input("Выберите оружие (sword/bow): ")
        new_weapon = Sword() if weapon_type == 'sword' else Bow()
        if self.fighter.change_weapon(new_weapon):
            print(f"Оружие изменено на {type(new_weapon).__name__}")

    def _handle_attack(self):
        """Обработка атаки игрока"""
        if self.fighter.current_ap < 1:
            print("Недостаточно ОД для атаки!")
            return

        if self.fighter.weapon.is_valid_attack(self.fighter, self.monster):
            if self.fighter.attack(self.monster):
                print("Атака успешна!")
                if not self.monster.is_alive():
                    print("Монстр повержен!")
            else:
                print("Атака не удалась!")
        else:
            print("Слишком далеко для атаки этим оружием!")

    def show_status(self):
        print(f"\nИгрок: ({self.fighter.position.x},{self.fighter.position.y}) | Здоровье: {self.fighter.health}")
        print(f"Монстр: ({self.monster.position.x},{self.monster.position.y}) | Здоровье: {self.monster.health}")
        print(f"ОД: {self.fighter.current_ap}/{self.fighter.max_ap} (+{self.fighter.carried_over_ap} перенесено)")

    def player_turn(self):
        while self.fighter.current_ap > 0:
            self.show_status()
            print("\nДействия:")
            print("1. Двигаться [1 ОД]")
            print("2. Сменить оружие [1 ОД]")
            print("3. Атаковать [1 ОД]")
            choice = input("> ")

            if choice == '1':
                direction = input("Направление (n/s/e/w): ")
                if self.fighter.move(direction):
                    print("Перемещение выполнено.")
                else:
                    print("Невозможно переместиться!")

            elif choice == '2':
                weapon = input("Выберите оружие (sword/bow): ")
                if weapon == 'sword' and self.fighter.change_weapon(Sword()):
                    print("Оружие изменено на меч.")
                elif weapon == 'bow' and self.fighter.change_weapon(Bow()):
                    print("Оружие изменено на лук.")
                else:
                    print("Ошибка смены оружия!")

            elif choice == '3':
                if self.fighter.attack(self.monster):
                    print("Атака успешна!")
                    if self.monster.health <= 0:
                        print("Монстр повержен!")
                        return True
                else:
                    print("Атака невозможна!")

            else:
                print("Неверный выбор!")

        self.fighter.reset_ap()
        return False

    def _monster_turn(self):
        """Ход монстра"""
        if not self.monster.is_alive():
            return

        # Простая логика ИИ:
        # 1. Если рядом - атакует
        # 2. Иначе приближается
        distance = self.monster.calculate_distance(self.fighter)

        if distance == 1:
            self.monster.attack(self.fighter)
        else:
            if self.movement.move_monster_towards_target(self.monster, self.fighter):
                print("Монстр переместился.")


    def run(self):
        while True:
            self.renderer.render()
            if self._check_game_over():
                break
            self._process_player_input()
            self._monster_turn()