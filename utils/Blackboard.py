from __future__ import annotations

import pygame

from collections import deque
from copy import deepcopy

from food.Dish import Plate


class Blackboard:
    def __init__(self, max_messages: int = 8):
        self.messages = deque(maxlen=max_messages)
        self.agent_states: dict[int, str] = {}
        self.order_tasks: dict[int, dict] = {}
        self.visual_effects: list[VisualEffect] = []

    def post(self, agent_id: int, message: str) -> str:
        entry = f"[Agent {agent_id}] {message}"
        self.messages.appendleft(entry)
        print(entry)
        return entry

    def announce(self, message: str) -> str:
        entry = f"[Système] {message}"
        self.messages.appendleft(entry)
        print(entry)
        return entry

    def ensure_order_plan(self, order, plan):
        key = id(order)
        if key in self.order_tasks:
            return
        tasks = []
        if plan:
            for recipe in plan:
                if not recipe:
                    continue
                ingredient = recipe[-1][1]
                tasks.append(
                    {
                        "ingredient": ingredient,
                        "plan": deepcopy(recipe),
                        "status": "pending",
                        "agent": None,
                    }
                )
        self.order_tasks[key] = {
            "order": order,
            "tasks": tasks,
            "plate": Plate(order.desired_dish.name),
            "delivery_agent": None,
        }

    def request_order(self, agent_id: int, orders):
        for order in orders:
            entry = self.order_tasks.get(id(order))
            if not entry:
                continue
            tasks = entry["tasks"]
            if any(task["status"] == "pending" for task in tasks):
                return order
            if any(task["status"] == "in_progress" and task["agent"] == agent_id for task in tasks):
                return order
            if self.order_ready(order) and entry["delivery_agent"] in (None, agent_id):
                return order
        return None

    def reserve_task(self, agent_id: int, order):
        entry = self.order_tasks.get(id(order))
        if not entry:
            return None
        for task in entry["tasks"]:
            if task["status"] == "pending":
                task["status"] = "in_progress"
                task["agent"] = agent_id
                return {"ingredient": task["ingredient"], "plan": deepcopy(task["plan"])}
        return None

    def release_task(self, agent_id: int, order, ingredient):
        entry = self.order_tasks.get(id(order))
        if not entry:
            return
        for task in entry["tasks"]:
            if (
                task["ingredient"] == ingredient
                and task["agent"] == agent_id
                and task["status"] == "in_progress"
            ):
                task["status"] = "pending"
                task["agent"] = None
                break

    def complete_task(self, agent_id: int, order, ingredient):
        entry = self.order_tasks.get(id(order))
        if not entry:
            return
        for task in entry["tasks"]:
            if task["ingredient"] == ingredient and task["agent"] == agent_id:
                task["status"] = "done"
                task["agent"] = None
                break

    def add_to_plate(self, order, ingredient, position=None):
        entry = self.order_tasks.get(id(order))
        if entry and ingredient:
            entry["plate"].add_ingr(ingredient)
            
            # Handle visual representation of the ingredient on the plate
            if position:
                if "visuals" not in entry:
                    entry["visuals"] = []
                
                # Offset slightly for stacking effect
                offset_x = (len(entry["visuals"]) % 2) * 5 - 2
                offset_y = (len(entry["visuals"]) // 2) * 5 - 2
                visual_pos = (position[0] + offset_x, position[1] + offset_y)
                
                entry["visuals"].append((ingredient.image, visual_pos))

            # Check if dish is complete to show the final dish visual
            if self.order_ready(order):
                # Double check if the plate matches the order
                if entry["plate"].verify(order):
                    dish_name = order.desired_dish.name
                    image_path = None
                    if dish_name == "burger":
                        image_path = "assets/ingredients/burger_fries.png"
                    elif dish_name == "salad":
                        image_path = "assets/ingredients/chopped_salad.png"
                    elif dish_name == "ice_cream":
                        image_path = "assets/ingredients/ice_cream.png"
                    elif dish_name == "coffee":
                        image_path = "assets/ingredients/coffee_cup.png"
                    
                    if image_path and position:
                        self.visual_effects.append(VisualEffect(image_path, position, duration=240)) # 2 seconds at 120 FPS

    def get_plate(self, order):
        entry = self.order_tasks.get(id(order))
        return entry["plate"] if entry else None

    def order_ready(self, order) -> bool:
        entry = self.order_tasks.get(id(order))
        if not entry or not entry["tasks"]:
            return False
        return all(task["status"] == "done" for task in entry["tasks"])

    def reserve_delivery(self, agent_id: int, order) -> bool:
        entry = self.order_tasks.get(id(order))
        if not entry or not self.order_ready(order):
            return False
        current = entry["delivery_agent"]
        if current in (None, agent_id):
            entry["delivery_agent"] = agent_id
            return True
        return False

    def release_delivery(self, agent_id: int, order):
        entry = self.order_tasks.get(id(order))
        if entry and entry["delivery_agent"] == agent_id:
            entry["delivery_agent"] = None

    def finalize_order(self, order):
        self.order_tasks.pop(id(order), None)

    def release_order(self, order):
        self.finalize_order(order)

    def drop_missing_orders(self, orders):
        valid_ids = {id(order) for order in orders}
        for key in list(self.order_tasks.keys()):
            if key not in valid_ids:
                self.order_tasks.pop(key, None)

    def set_agent_state(self, agent_id: int, state: str):
        self.agent_states[agent_id] = state

    def draw(self, surface, font, x: int, y: int):
        header = font.render("BlackBoard", True, (255, 255, 0), (0, 0, 0))
        surface.blit(header, (x, y))

        for idx, message in enumerate(list(self.messages)[:6]):
            text = font.render(message, True, (200, 200, 200), (0, 0, 0))
            surface.blit(text, (x, y + 22 + idx * 18))

        state_y = y + 22 + min(len(self.messages), 6) * 18 + 10
        state_title = font.render("États agents :", True, (180, 200, 255), (0, 0, 0))
        surface.blit(state_title, (x, state_y))
        for offset, (agent_id, state) in enumerate(sorted(self.agent_states.items())):
            text = font.render(f"{agent_id}: {state}", True, (200, 200, 200), (0, 0, 0))
            surface.blit(text, (x, state_y + 18 + offset * 18))

    def update_visuals(self):
        for effect in self.visual_effects[:]:
            effect.timer -= 1
            if effect.timer <= 0:
                self.visual_effects.remove(effect)

    def draw_visuals(self, surface):
        for effect in self.visual_effects:
            if effect.image:
                rect = effect.image.get_rect(center=effect.position)
                surface.blit(effect.image, rect)

    def draw_plated_ingredients(self, surface):
        for entry in self.order_tasks.values():
            plate = entry["plate"]
            # We need a position for the plate. Since we don't store it explicitly in the plate,
            # we rely on the last added ingredient's position or a default if available.
            # However, the plan was to store position in add_to_plate.
            # Let's check where we store it.
            # We will store a list of (image, position) in the entry for rendering.
            if "visuals" in entry:
                for img, pos in entry["visuals"]:
                    rect = img.get_rect(center=pos)
                    surface.blit(img, rect)


class VisualEffect:
    def __init__(self, image_path, position, duration=60):
        self.position = position
        self.timer = duration
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            # Scale up a bit for visibility if needed, or keep as is.
            # Let's scale it to be clear.
            self.image = pygame.transform.scale(self.image, (100, 100))
        except Exception as e:
            print(f"Failed to load visual effect image: {image_path} - {e}")
            self.image = None