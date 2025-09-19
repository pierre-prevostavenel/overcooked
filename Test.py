import pygame
import sys
import math

# --- Initialisation de Pygame ---
pygame.init()

# --- Constantes du jeu ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- Couleurs ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

# --- Configuration de l'écran ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Prototype Overcooked - Agent Autonome")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# --- CHEMINS DES IMAGES (À REMPLACER PAR VOS PROPRES IMAGES) ---
# NOTE: Créez des fichiers .png simples (ex: un carré de 50x50 pixels) avec ces noms
# pour que le jeu puisse se lancer.
PLAYER_IMG_PATH = 'assets/player.png'
CUTTING_BOARD_IMG_PATH = 'assets/gas.png'
STOVE_IMG_PATH = 'assets/gas.png'
PLATING_STATION_IMG_PATH = 'assets/white_tile.png'


class Player(pygame.sprite.Sprite):
    """
    Représente le joueur/agent. Dans ce prototype, il se déplace de manière autonome.
    """
    def __init__(self, x, y):
        super().__init__()
        try:
            # Tente de charger l'image fournie par l'utilisateur
            self.image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_PATH).convert_alpha(), (40, 40))
        except pygame.error:
            # Si l'image n'est pas trouvée, crée un carré bleu en remplacement
            print(f"Attention: Image '{PLAYER_IMG_PATH}' non trouvée. Utilisation d'un carré bleu.")
            self.image = pygame.Surface((40, 40))
            self.image.fill(BLUE)
            
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.speed = 3

        self.order = None
        self.current_task_index = -1
        self.target_station = None
        
        self.state = 'IDLE'  # 'IDLE', 'MOVING', 'WORKING'
        self.work_timer = 0
        self.work_duration = 120 # 2 secondes à 60 FPS

    def set_order(self, order):
        """Définit une nouvelle commande à suivre pour l'agent."""
        self.order = order
        self.current_task_index = 0
        self.state = 'MOVING'
        print(f"Nouvelle commande reçue: {self.order.recipe}")

    def update(self, stations):
        if self.state == 'IDLE':
            return

        if self.state == 'MOVING':
            # Si on n'a pas de cible, on en trouve une
            if self.target_station is None:
                if self.current_task_index < len(self.order.recipe):
                    target_type = self.order.recipe[self.current_task_index]
                    for station in stations:
                        if station.station_type == target_type:
                            self.target_station = station
                            print(f"Déplacement vers: {self.target_station.station_type}")
                            break
                else:
                    # Commande terminée
                    print("Commande terminée !")
                    self.state = 'IDLE'
                    self.order.complete = True
                    return
            
            # Déplacement vers la cible
            if self.target_station:
                direction = pygame.math.Vector2(self.target_station.rect.center) - self.pos
                if direction.length() > self.speed:
                    direction.scale_to_length(self.speed)
                    self.pos += direction
                    self.rect.center = self.pos
                else:
                    # Arrivé à la station
                    print(f"Arrivé à: {self.target_station.station_type}. Début du travail.")
                    self.state = 'WORKING'
                    self.work_timer = self.work_duration

        elif self.state == 'WORKING':
            self.work_timer -= 1
            if self.work_timer <= 0:
                print(f"Tâche '{self.target_station.station_type}' terminée.")
                self.current_task_index += 1
                self.target_station = None
                self.state = 'MOVING'


class Station(pygame.sprite.Sprite):
    """
    Représente un poste de travail (découpe, cuisson, etc.).
    """
    def __init__(self, x, y, station_type, image_path):
        super().__init__()
        self.station_type = station_type
        try:
            self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (60, 60))
        except pygame.error:
            print(f"Attention: Image '{image_path}' non trouvée. Utilisation d'un carré gris.")
            self.image = pygame.Surface((60, 60))
            self.image.fill(GREY)

        self.rect = self.image.get_rect(center=(x, y))


class Order:
    """
    Représente une commande simple.
    """
    def __init__(self):
        # Une recette est une séquence de types de stations à visiter
        self.recipe = ['cutting_board', 'stove', 'plating_station']
        self.complete = False


class Game:
    """
    Classe principale pour gérer le jeu.
    """
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.stations = pygame.sprite.Group()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.all_sprites.add(self.player)
        self.current_order = None
        self.setup_level()

    def setup_level(self):
        """Crée et positionne les stations pour le niveau."""
        cutting_board = Station(100, 100, 'cutting_board', CUTTING_BOARD_IMG_PATH)
        stove = Station(SCREEN_WIDTH - 100, 100, 'stove', STOVE_IMG_PATH)
        plating_station = Station(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100, 'plating_station', PLATING_STATION_IMG_PATH)

        self.stations.add(cutting_board, stove, plating_station)
        self.all_sprites.add(self.stations)

    def start_new_order(self):
        """Génère une nouvelle commande et la donne au joueur."""
        self.current_order = Order()
        self.player.set_order(self.current_order)

    def run(self):
        """Boucle principale du jeu."""
        running = True
        # Démarre la première commande au lancement
        self.start_new_order()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Mettre à jour les sprites
            self.all_sprites.update(self.stations)
            
            # Si la commande actuelle est terminée, en lancer une nouvelle après un délai
            if self.current_order and self.current_order.complete:
                 self.start_new_order()


            # Dessiner
            screen.fill(WHITE)
            self.all_sprites.draw(screen)
            self.draw_ui()
            pygame.display.flip()

            clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def draw_ui(self):
        """Dessine l'interface utilisateur (informations sur la commande)."""
        if self.current_order:
            recipe_text = "Commande: " + " -> ".join(self.current_order.recipe)
            text_surf = font.render(recipe_text, True, BLACK)
            screen.blit(text_surf, (10, 10))

            if self.player.state == 'WORKING' and self.player.target_station:
                progress = 1 - (self.player.work_timer / self.player.work_duration)
                bar_width = 100
                bar_height = 15
                progress_width = bar_width * progress
                
                # Position de la barre de progression au-dessus de la station
                bar_x = self.player.target_station.rect.centerx - bar_width / 2
                bar_y = self.player.target_station.rect.top - 20

                pygame.draw.rect(screen, BLACK, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
                pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height))
                pygame.draw.rect(screen, GREEN, (bar_x, bar_y, progress_width, bar_height))


if __name__ == '__main__':
    game = Game()
    game.run()
