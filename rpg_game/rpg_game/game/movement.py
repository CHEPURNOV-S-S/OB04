# game/movement.py
from rpg_game.entities.base import Entity
from rpg_game.entities.fighter import Fighter
from rpg_game.entities.monster import Monster
from rpg_game.entities.base import Position

class MovementManager:
    def __init__(self, map_size: int):
        self.map_size = map_size  # Например, из constants.py

    def move_entity(self, entity: Entity, direction: str) -> bool:
        """Перемещение игрока по направлению"""
        new_x, new_y = entity.position.x, entity.position.y
        if direction == 'n': new_y -= 1
        elif direction == 's': new_y += 1
        elif direction == 'e': new_x += 1
        elif direction == 'w': new_x -= 1
        else: return False

        if 0 <= new_x < self.map_size and 0 <= new_y < self.map_size:
            entity.position = Position(new_x, new_y)
            return True
        return False

    def move_monster_towards_target(self, monster: Monster, target: Entity) -> bool:
        """ИИ-перемещение монстра на 1 шаг ближе к цели"""
        dx = target.position.x - monster.position.x
        dy = target.position.y - monster.position.y

        new_x = monster.position.x + (1 if dx > 0 else -1 if dx < 0 else 0)
        new_y = monster.position.y + (1 if dy > 0 else -1 if dy < 0 else 0)

        if 0 <= new_x < self.map_size and 0 <= new_y < self.map_size:
            monster.position = Position(new_x, new_y)
            return True
        return False