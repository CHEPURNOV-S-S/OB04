from rpg_game.entities.fighter import Fighter
from rpg_game.entities.monster import Monster
from rpg_game.weapons.sword import Sword
from rpg_game.weapons.bow import Bow
from rpg_game.entities.base import Position
from .renderer import Renderer
from .constants import MAP_SIZE
import random

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
        if self.fighter.move(direction):
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

        distance = self.fighter._calculate_distance(self.monster)
        if self.fighter.weapon.is_valid_attack(distance):
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
        distance = self._calculate_distance(
            self.fighter.position,
            self.monster.position
        )

        if distance == 1:
            self.monster.attack(self.fighter)
        else:
            self._monster_move_towards(self.fighter.position)

    def _monster_move_towards(self, target_pos: Position):
        """Монстр движется к цели"""
        dx = target_pos.x - self.monster.position.x
        dy = target_pos.y - self.monster.position.y

        new_x = self.monster.position.x + (1 if dx > 0 else -1 if dx < 0 else 0)
        new_y = self.monster.position.y + (1 if dy > 0 else -1 if dy < 0 else 0)

        if 0 <= new_x < MAP_SIZE and 0 <= new_y < MAP_SIZE:
            self.monster.position = Position(new_x, new_y)

    def _calculate_distance(self, pos1: Position, pos2: Position) -> int:
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)

    def run(self):
        while True:
            self.renderer.render()
            if self._check_game_over():
                break
            self._process_player_input()
            self._monster_turn()