import os
import platform
from rpg_game.entities.base import Position

class Renderer:
    def __init__(self, game):
        self.game = game
        self.history = []

    def render(self):
        self._clear_console()
        self._draw_map()
        self._draw_status()
        self._draw_contols()
        self._draw_history()


    def add_history_msg(self, msg:str):
        self.history.append(msg)

    def _clear_console(self):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def _draw_map(self):
        print("   " + " ".join([str(i) for i in range(10)]))
        for y in range(10):
            row = [self._get_cell_symbol(x, y) for x in range(10)]
            print(f"{y:2d} " + " ".join(row))
        print()

    def _get_cell_symbol(self, x, y):
        if Position(x, y) == self.game.fighter.position:
            return "P"
        if Position(x, y) == self.game.monster.position:
            return "M"
        return "·"

    def _draw_status(self):
        print(f"Игрок: ♥{self.game.fighter.health} | ОД: {self.game.fighter.current_ap}/{self.game.fighter.max_ap}")
        print(f"Монстр: ♥{self.game.monster.health}")
        print("-" * 30)

    def _draw_history(self):
        for msg in self.history:
            print(msg)

    def _draw_contols(self):
        print("=== Управление ===")
        print("Двигаться: ↑ ↓ ← →")
        print("С - сменить оружие")
        print("Enter - Завершить ход")
        print("Backspace - Выход")
        print("Space - Атака")
        print('------------------------------')

