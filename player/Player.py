from __future__ import annotations

import heapq
import json
import math
from typing import List, Optional, TYPE_CHECKING

import pygame

import food.Ingredient as Ingredient
from food.Dish import Plate
from maps.Station import Station

if TYPE_CHECKING:
    from utils.Blackboard import Blackboard


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        json_path,
        *,
        agent_id: int = 1,
        start: tuple[int, int] = (1, 2),
        tile_size: int = 50,
        map_size: tuple[int, int] = (10, 10),
        blackboard: Optional["Blackboard"] = None,
        color: tuple[int, int, int] = (255, 255, 255),
    ):
        super().__init__()
        self.agent_id = agent_id
        self.name = f"Agent-{agent_id}"
        self.blackboard = blackboard
        self.map_width, self.map_height = map_size
        self.tile_size = tile_size
        self.x, self.y = start
        self.position = self._to_index(self.x, self.y)
        self.manual_control = False
        self.color = color

        self.transitions: dict[tuple[str, str], List[tuple[tuple[str, str], str]]] = {}
        self.init_transitions(json_path)

        self.move_timer = 0
        self.move_period = 15
        self.interaction_progress = 0

        self.state = "IDLE"
        self.itemHeld = None
        self.current_plan: Optional[List[tuple[str, tuple[str, str]]]] = None
        self.current_task: Optional[tuple[str, str]] = None
        self.current_order = None
        self.itemWanted: Optional[str] = None
        self.pending_action: Optional[str] = None
        self.path: List[tuple[int, int]] = []
        self.target_station: Optional[Station] = None
        self.target_game = None
        self.idle_message_cooldown = 0
        self.ready_to_plate = False
        self.delivery_reserved = False
        self.env = None
        self.blocked_steps = 0

        self.image = self._build_image(tile_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * tile_size, self.y * tile_size)

    def _build_image(self, size: int):
        try:
            image = pygame.image.load("assets/player.png").convert_alpha()
        except pygame.error:
            image = pygame.Surface((size, size), pygame.SRCALPHA)
            image.fill((255, 255, 255))
        image = pygame.transform.scale(image, (size, size))
        tint = pygame.Surface((size, size), pygame.SRCALPHA)
        r, g, b = self.color
        tint.fill((r, g, b, 90))
        image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return image

    def update(self, env):
        self.env = env
        if self.manual_control:
            return
        self.move_timer = (self.move_timer + 1) % self.move_period
        if self.move_timer == 0:
            perception = self.see(env)
            self.next(perception)
            self.action()
        if self.idle_message_cooldown > 0:
            self.idle_message_cooldown -= 1
        if self.blackboard:
            self.blackboard.set_agent_state(self.agent_id, self.state)

    def see(self, env):
        return {
            "orders": env.get_orders(),
            "game": env,
            "map": env.get_maps(),
        }

    def next(self, perception):
        orders = perception["orders"]
        game = perception["game"]
        map_obj = perception["map"]

        if self.blackboard:
            for order in orders:
                plan = self.create_plan(order)
                self.blackboard.ensure_order_plan(order, plan)

        if not orders:
            self._notify_idle("Je reste disponible, aucune commande en cuisine.")
            self.reset_plan(silent=True)
            return

        if self.current_order and self.current_order not in orders:
            self.say(f"La commande « {self.current_order.desired_dish.name} » vient d'être retirée, je lâche la tâche.")
            self.reset_plan()
            return

        if self.ready_to_plate:
            if self.go_to(map_obj, "table"):
                self.state = "PLATING"
            return

        if self.state == "SENDING":
            return

        if self.current_order is None:
            order = self._request_order(orders)
            if order is None:
                self._notify_idle("Aucune tâche disponible pour le moment.")
                return
            self.current_order = order
            self.say(f"Je rejoins la commande « {order.desired_dish.name} ».")

        if self.current_plan is None:
            if not self._assign_task():
                if self.blackboard and self.blackboard.order_ready(self.current_order):
                    if self.blackboard.reserve_delivery(self.agent_id, self.current_order):
                        self.delivery_reserved = True
                        if self.go_to(map_obj, "table"):
                            self.state = "SENDING"
                            self.target_game = game
                            self.say(f"Je livre « {self.current_order.desired_dish.name} » au passe.")
                    else:
                        self.say(f"La livraison de « {self.current_order.desired_dish.name} » est prise, je cherche une autre tâche.")
                        self.reset_plan()
                else:
                    self.say(f"Plus de tâche sur « {self.current_order.desired_dish.name} », je cherche ailleurs.")
                    self.reset_plan()
                return

        if not self.current_plan:
            self.ready_to_plate = True
            if self.go_to(map_obj, "table"):
                self.state = "PLATING"
            return

        action, (item_name, _) = self.current_plan[0]
        self.itemWanted = item_name
        self.pending_action = action

        destinations = {
            "fetch": "fridge",
            "cook": "oven",
            "fry": "oven",
            "chop": "workbench",
            "wash": "white_sink",
        }

        target_type = destinations.get(action)
        if target_type is None:
            self.say(f"Action inconnue « {action} », je me mets en pause.")
            self.state = "IDLE"
            return

        if self.go_to(map_obj, target_type):
            state_map = {
                "fetch": "COLLECT",
                "cook": "COOKING",
                "fry": "COOKING",
                "chop": "CHOPPING",
                "wash": "WASHING",
            }
            self.state = state_map.get(action, "IDLE")

    def action(self):
        match self.state:
            case "WALKING":
                if not self.path:
                    self.state = "IDLE"
                    return
                next_pos = self.path[0]
                if not self._can_move_to(next_pos):
                    self.blocked_steps += 1
                    if self.blocked_steps >= 3 and self.env and self.target_station:
                        occupied = self._occupied_positions()
                        new_path = self.get_path(self.env.maps, self.target_station, occupied_positions=occupied)
                        if new_path:
                            self.path = new_path
                        else:
                            self.state = "IDLE"
                            self.path = []
                        self.blocked_steps = 0
                    return
                self.blocked_steps = 0
                self.path.pop(0)
                self.x, self.y = next_pos
                self.position = self._to_index(self.x, self.y)
                self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)
                if not self.path:
                    self.state = "IDLE"

            case "COLLECT" | "COOKING" | "CHOPPING" | "WASHING":
                if self.target_station is None:
                    self.state = "IDLE"
                    return
                remaining = self.interact(self.target_station)
                if remaining == 0 and self.current_plan:
                    self.current_plan.pop(0)
                    self.pending_action = None
                    self.interaction_progress = 0
                    if not self.current_plan:
                        self.ready_to_plate = True
                    self.state = "IDLE"

            case "PLATING":
                if self.interact("plate") == 0:
                    if self.blackboard and self.itemHeld and self.current_order:
                        self.blackboard.add_to_plate(self.current_order, self.itemHeld)
                        if self.current_task:
                            self.blackboard.complete_task(self.agent_id, self.current_order, self.current_task)
                            self.say(
                                f"Ingrédient {self.current_task[0]} ({self.current_task[1]}) ajouté pour « {self.current_order.desired_dish.name} »."
                            )
                    self.itemHeld = None
                    self.current_plan = None
                    self.current_task = None
                    self.ready_to_plate = False
                    self.state = "IDLE"

            case "SENDING":
                if self.interact("plate") == 0:
                    plate = self.blackboard.get_plate(self.current_order) if self.blackboard else None
                    if self.target_game and plate and self.current_order:
                        success = self.target_game.accept_plate(plate, self.current_order)
                        result = "réussie" if success else "échouée"
                        self.say(f"Commande « {self.current_order.desired_dish.name} » {result}.")
                    if self.blackboard and self.current_order:
                        self.blackboard.release_delivery(self.agent_id, self.current_order)
                    self.reset_plan()

            case "IDLE":
                pass

    def init_transitions(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for ing_data in data.get("ingredients", []):
            name = ing_data["name"]
            for state_data in ing_data.get("states", []):
                state = state_data["state"]
                src = (name, state)
                actions = state_data.get("actions", {})
                if state == "raw":
                    self.transitions[src] = [(None, "fetch")]
                for action, result in actions.items():
                    dst = (result["name"], result["state"])
                    self.transitions.setdefault(dst, []).append((src, action))

    def create_plan(self, order):
        if order is None:
            return None
        plans = []
        for ingredient in order.desired_dish.ingredients:
            path = []
            current = ingredient.as_tuple()
            visited = set()
            while current in self.transitions and current not in visited:
                visited.add(current)
                src, action = self.transitions[current][0]
                path.append((action, current))
                current = src
            plans.append(path[::-1])
        return plans

    def go_to(self, map_obj, target: str):
        self.target_station = self.get_nearest(map_obj, target)
        if self.target_station is None:
            self.say(f"Impossible de trouver {target} sur la carte.")
            self.state = "IDLE"
            return False

        occupied = self._occupied_positions()
        self.path = self.get_path(map_obj, self.target_station, occupied_positions=occupied)
        if self.path is None:
            self.say(f"Aucun chemin vers {target} depuis ma position.")
            self.state = "IDLE"
            return False

        if not self.path:
            return True

        self.state = "WALKING"
        return False

    def get_nearest(self, map_obj, tile_type):
        nearest = None
        min_dist = float("inf")
        for r in range(map_obj.height):
            for c in range(map_obj.width):
                tile = map_obj.grid[r][c]
                if tile.tile_type == tile_type:
                    dist = math.hypot(c - self.x, r - self.y)
                    if dist < min_dist:
                        min_dist = dist
                        nearest = tile
        return nearest

    def get_path(self, map_obj, target_tile, occupied_positions=None):
        occupied_positions = occupied_positions or set()
        start_node = Node(None, (self.x, self.y))
        end_pos = (target_tile.col, target_tile.row)
        open_list = [start_node]
        closed_set = set()
        movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        while open_list:
            current = heapq.heappop(open_list)
            closed_set.add(current.position)

            if abs(current.position[0] - end_pos[0]) + abs(current.position[1] - end_pos[1]) == 1:
                path = []
                c = current
                while c:
                    path.append(c.position)
                    c = c.parent
                result = path[::-1][1:]
                return result

            for move in movements:
                nx, ny = current.position[0] + move[0], current.position[1] + move[1]
                if not (0 <= nx < map_obj.width and 0 <= ny < map_obj.height):
                    continue
                if (nx, ny) in closed_set:
                    continue
                if (nx, ny) in occupied_positions and (nx, ny) != (self.x, self.y):
                    continue
                tile = map_obj.grid[ny][nx]
                if tile.tile_type != "floor":
                    continue
                new_node = Node(current, (nx, ny))
                new_node.g = current.g + 1
                new_node.h = abs(nx - end_pos[0]) + abs(ny - end_pos[1])
                new_node.f = new_node.g + new_node.h

                if any(new_node == n and new_node.g >= n.g for n in open_list):
                    continue
                heapq.heappush(open_list, new_node)
        return None

    def _assign_task(self) -> bool:
        if not self.blackboard or not self.current_order:
            return False
        reservation = self.blackboard.reserve_task(self.agent_id, self.current_order)
        if reservation is None:
            return False
        self.current_task = reservation["ingredient"]
        self.current_plan = list(reservation["plan"])
        if not self.current_plan:
            self.ready_to_plate = True
        else:
            self.ready_to_plate = False
        item_name, item_state = self.current_task
        self.say(f"Je prépare {item_name} ({item_state}) pour « {self.current_order.desired_dish.name} ».")
        return True

    def grab(self, item):
        if self.itemHeld is None:
            self.itemHeld = item
            self.say(f"Je tiens maintenant {item}.")
        else:
            self.say("Je ne peux pas prendre un objet supplémentaire.")

    def interact(self, station: Station | str):
        if station == "plate":
            self.interaction_progress = 0
            return 0 if self.itemHeld is not None else 0
        return station.interact(self)

    def draw(self, surface):
        if self.itemHeld is not None:
            item_rect = self.itemHeld.image.get_rect(center=self.rect.center)
            surface.blit(self.itemHeld.image, item_rect.topleft)

    def say(self, message: str):
        if self.blackboard:
            self.blackboard.post(self.agent_id, message)

    def reset_plan(self, *, silent: bool = False):
        if self.blackboard and self.current_order and self.current_task:
            self.blackboard.release_task(self.agent_id, self.current_order, self.current_task)
        if self.blackboard and self.current_order and self.delivery_reserved:
            self.blackboard.release_delivery(self.agent_id, self.current_order)
        self.current_order = None
        self.current_plan = None
        self.current_task = None
        self.ready_to_plate = False
        self.pending_action = None
        self.itemWanted = None
        self.target_station = None
        self.target_game = None
        self.path = []
        self.state = "IDLE"
        self.interaction_progress = 0
        self.itemHeld = None
        self.delivery_reserved = False
        if not silent and self.blackboard:
            self.blackboard.set_agent_state(self.agent_id, self.state)

    def _request_order(self, orders):
        if self.blackboard:
            return self.blackboard.request_order(self.agent_id, orders)
        return orders[0] if orders else None

    def _notify_idle(self, message: str):
        if self.idle_message_cooldown == 0:
            self.say(message)
            self.idle_message_cooldown = 240

    def _can_move_to(self, pos: tuple[int, int]) -> bool:
        if self.env is None:
            return True
        target_x, target_y = pos
        if not (0 <= target_x < self.map_width and 0 <= target_y < self.map_height):
            return False
        if self.env.maps.grid[target_y][target_x].tile_type != "floor":
            return False
        for agent in self.env.players:
            if agent is self:
                continue
            if (agent.x, agent.y) == pos:
                return False
        return True

    def _occupied_positions(self):
        if self.env is None:
            return set()
        return {
            (agent.x, agent.y)
            for agent in self.env.players
            if agent is not self
        }

    def _to_index(self, x: int, y: int):
        return y * self.map_width + x


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f