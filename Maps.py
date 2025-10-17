import pygame
import heapq
import math
from pygame.sprite import LayeredUpdates
from Tile import Tile

class Node:
    """
    Une classe pour représenter un nœud dans l'algorithme A*.
    Chaque nœud représente une case de la carte.
    """
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position  # (x, y)

        self.g = 0  # Coût du départ à ce nœud
        self.h = 0  # Coût estimé de ce nœud à la fin (heuristique)
        self.f = 0  # Coût total (g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

class Maps:
    """Classe qui contient toutes les maps et gère l'accès par niveau."""
    def __init__(self, tile_size=72):
        self.tile_size = tile_size
        self.levels = []
        self._load_maps()

    def _load_maps(self):
        """Charge ou définit toutes les maps ici."""
        # Exemple Map 1
        map1 = [
            ["workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench"],
            ["workbench", "table",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "table",     "workbench"],
            ["workbench", "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "workbench"],
            ["workbench", "floor",     "floor",     "floor",     "floor",      "floor",     "floor",    "floor",     "floor",     "workbench"],
            ["workbench", "gas_station","floor",    "floor",    "floor",     "floor",     "floor",     "floor",     "white_sink", "workbench"],
            ["workbench", "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "workbench"],
            ["workbench", "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",    "workbench"],
            ["workbench", "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "floor",     "workbench"],
            ["workbench", "fridge",     "floor",     "trash1",     "workbench",    "workbench","trash2",     "floor",     "floor",     "workbench"],
            ["workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench", "workbench"],
        ]

        # Exemple Map 2
        map2 = [["blackfloor"]*10 for _ in range(10)]
        map2[1][1] = "whitefloor"
        map2[3][1] = "gas_station"

        self.levels.append(map1)
        self.levels.append(map2)

    def get_level(self, index):
        """Retourne la map demandée sous forme de LayeredUpdates de tiles."""
        grid_data = self.levels[index]
        tiles = LayeredUpdates()
        for r, row in enumerate(grid_data):
            for c, tile_type in enumerate(row):
                # Toujours créer un floor en dessous
                if tile_type != "floor" and tile_type != "blackfloor":
                    floor_tile = Tile(r, c, "floor", self.tile_size)
                    tiles.add(floor_tile, layer=0)
                    tile = Tile(r, c, tile_type, self.tile_size)
                    tiles.add(tile, layer=1)
                else:
                    tile = Tile(r, c, tile_type, self.tile_size)
                    tiles.add(tile, layer=0)

        return tiles


    def num_levels(self):
        return len(self.levels)
    
    def get_nearest(self, from_grid_x, from_grid_y, tile_type, level_index=None):
        """
        Retourne les coordonnées de la grille (col, row) de la tuile du type 'tile_type' la plus proche 
        de la position de grille (from_grid_x, from_grid_y).
        Renvoie un tuple (x, y) ou None si aucune tuile de ce type n'est trouvée.
        """
        if level_index is None:
            level_index = self.current_level_index if hasattr(self, 'current_level_index') else 0

        map_grid = self.levels[level_index]
        map_height = len(map_grid)
        map_width = len(map_grid[0])
        
        nearest_coords = None
        min_dist = float('inf')

        # On parcourt directement la structure de données de la carte (la grille)
        for r in range(map_height):
            for c in range(map_width):
                if map_grid[r][c] == tile_type:
                    # Calcul de la distance euclidienne sur la grille
                    dist = math.hypot(c - from_grid_x, r - from_grid_y)
                    if dist < min_dist:
                        min_dist = dist
                        # On stocke les coordonnées de la grille (colonne, ligne)
                        nearest_coords = (c, r)

        return nearest_coords

    def get_path(self, from_x, from_y, tile, map_index):
        """
        Calcule le chemin le plus court en utilisant l'algorithme A*.
        Renvoie une liste de tuples (x, y) représentant les coordonnées des cases du chemin.
        Renvoie None si aucun chemin n'est trouvé.
        Les coordonnées sont en indices de grille (colonne, ligne).
        """
        map_grid = self.levels[map_index]
        map_height = len(map_grid)
        map_width = len(map_grid[0])

        # Création des nœuds de départ et d'arrivée
        start_node = Node(None, (from_x, from_y))
        end_node = Node(None, self.get_nearest(from_x, from_y, tile, map_index))

        open_list = []
        closed_set = set()

        # Le tas (heap) permet de toujours récupérer le nœud avec le plus petit f de manière efficace
        heapq.heapify(open_list)
        heapq.heappush(open_list, start_node)

        # Mouvements possibles (4 directions : haut, bas, gauche, droite)
        movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        while len(open_list) > 0:
            current_node = heapq.heappop(open_list)
            closed_set.add(current_node.position)

            # Chemin trouvé, on le reconstruit en remontant les parents
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1][1:]  # On retourne le chemin dans le bon sens (départ -> arrivée)

            # Exploration des voisins
            for move in movements:
                node_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])
                node_x, node_y = node_position

                # Vérifier si le voisin est dans les limites de la carte
                if not (0 <= node_x < map_width and 0 <= node_y < map_height):
                    continue

                # MODIFICATION : Autoriser la destination même si c'est un obstacle
                # On vérifie si la case est un obstacle SEULEMENT si ce n'est PAS la destination finale.
                if node_position != end_node.position and "floor" not in map_grid[node_y][node_x]:
                    continue
                
                # Le voisin a déjà été exploré
                if node_position in closed_set:
                    continue

                new_node = Node(current_node, node_position)
                new_node.g = current_node.g + 1
                # Heuristique: Distance de Manhattan (simple et efficace pour les grilles)
                new_node.h = abs(node_x - end_node.position[0]) + abs(node_y - end_node.position[1])
                new_node.f = new_node.g + new_node.h

                # Si le voisin est déjà dans la liste ouverte avec un meilleur chemin, on ne fait rien
                for open_node in open_list:
                    if new_node == open_node and new_node.g >= open_node.g:
                        break
                else:
                    # Sinon, on l'ajoute à la liste ouverte
                    heapq.heappush(open_list, new_node)

        return None  # Aucun chemin trouvé