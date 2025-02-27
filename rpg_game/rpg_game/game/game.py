#/game/game
import random
import msvcrt
import time
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
        self.fighter = Fighter(Position(5, 0), max_ap=5)
        self.monster = self._generate_monster()
        self.movement = MovementManager(MAP_SIZE)
        self.running = True

    def _generate_monster(self):
        while True:
            x, y = random.randint(0,9), random.randint(0,9)
            if not (x == 5 and y == 0):
                return Monster(Position(x, y))

    def _check_game_over(self) -> bool:
        if not self.fighter.is_alive():
            self.renderer.add_history_msg("Вы погибли...")
            return True
        if not self.monster.is_alive():
            self.renderer.add_history_msg("Монстр повержен!")
            return True
        return False

    def _handle_movement(self, direction):
        if self.movement.move_entity(self.fighter, direction):
            self.renderer.add_history_msg(f"Игрок переместился на {direction}")

    def _handle_attack(self):
        if self.fighter.current_ap >= 1:
            if self.fighter.attack(self.monster):
                self.renderer.add_history_msg("Успешная атака!")
            else:
                self.renderer.add_history_msg("Атака провалена")
        else:
            self.renderer.add_history_msg("Недостаточно ОД")

    def _handle_weapon_change(self):
        # Создаём список доступных типов оружия
        weapon_classes = [Sword, Bow]

        # Определяем текущий тип оружия
        current_weapon_class = type(self.fighter.weapon) if self.fighter.weapon else None

        # Находим индекс текущего типа оружия
        current_index = weapon_classes.index(current_weapon_class) if current_weapon_class in weapon_classes else 0

        # Переключаемся на следующий тип
        new_index = (current_index + 1) % len(weapon_classes)
        new_weapon = weapon_classes[new_index]()  # Создаём новый экземпляр
        if self.fighter.change_weapon(new_weapon):
            self.renderer.add_history_msg(f"Оружие изменено на {type(new_weapon).__name__}")

    def _process_input(self):
        while self.fighter.current_ap > 0 and self.running:

            self.renderer.render()
            # Ожидание нажатия клавиши
            key = msvcrt.getch()
            if key == b'\x08':  # ESC
                self.running = False
                break
            elif key == b'\r':  # Enter
                break  # Игрок завершил ход вручную
            elif key == b'\xe0':  # Стрелочные клавиши
                self.fighter.current_ap -= 1
                arrow_key = msvcrt.getch()
                if arrow_key == b'H':  # Up
                    self._handle_movement('n')
                elif arrow_key == b'P':  # Down
                    self._handle_movement('s')
                elif arrow_key == b'K':  # Left
                    self._handle_movement('w')
                elif arrow_key == b'M':  # Right
                    self._handle_movement('e')
            elif key == b' ':  # Space
                self._handle_attack()
            elif key == b'c' or key == b'C':  # C
                self._handle_weapon_change()

        # сброс AP игрока

        self.fighter.reset_ap()

    def run(self):
        while self.running:
            self.renderer.render()
            if self._check_game_over():
                break
            self._process_input()
            self._monster_turn()
            time.sleep(0.1)

    def _monster_turn(self):
        if not self.monster.is_alive():
            return
        if self.movement.move_monster_towards_target(self.monster, self.fighter):
            self.renderer.add_history_msg("Монстр приблизился")
        else:
            self.monster.attack(self.fighter)