from pygame import Surface
from pygame import Vector2
from pygame import Rect
import pygame

from scene import Scene
from resource_path import resource_path

from constants import *

from scenes.end_game_failure import EndGame as EndGameFailure
from scenes.end_game_success import EndGame as EndGameSuccess

def load_image(name: str, size: Vector2) -> pygame.Surface:
    resource = pygame.image.load(resource_path(name))
    scaled = pygame.transform.scale(resource, (size.x, size.y))
    return scaled    

HEART_PATH = "heart.png"
HEART_DEAD_PATH = "heart_dead.png"

HEART_HEIGHT = 20
HEART_SIZE = 40
PLAYER_HEARTS = [
    Vector2(20, HEART_HEIGHT),
    Vector2(60, HEART_HEIGHT),
    Vector2(100, HEART_HEIGHT)
]

ENEMY_HEARTS = [
    Vector2(SCREEN_WIDTH - 140, HEART_HEIGHT),
    Vector2(SCREEN_WIDTH - 100, HEART_HEIGHT),
    Vector2(SCREEN_WIDTH - 60, HEART_HEIGHT)
]

HEART_IMAGE      = load_image(HEART_PATH, Vector2(HEART_SIZE, HEART_SIZE))
DEAD_HEART_IMAGE = load_image(HEART_DEAD_PATH, Vector2(HEART_SIZE, HEART_SIZE))

def draw_heart(screen: Surface, position: Vector2, isAlive: bool):
    if isAlive:
        screen.blit(HEART_IMAGE, (position.x, position.y))
    else:
        screen.blit(DEAD_HEART_IMAGE, (position.x, position.y))

class MainGame(Scene):   
    # Game state 
    isUserAlive: bool
    isEnemyAlive: bool

    # X out of 3 hearts
    playerHealth: int
    enemyHealth: int

    def __init__(self):
        self.isUserAlive = True
        self.isEnemyAlive = True
        self.playerHealth = len(PLAYER_HEARTS)
        self.enemyHealth = len(ENEMY_HEARTS)

    def draw(self, screen, events):
        # Draw hearts
        for i in range(0, len(PLAYER_HEARTS)):
            isHeartAlive =  i < self.playerHealth
            draw_heart(screen, PLAYER_HEARTS[i], isHeartAlive)

            
        for i in range(0, len(ENEMY_HEARTS)):
            isHeartAlive =  i < self.playerHealth
            draw_heart(screen, PLAYER_HEARTS[i], isHeartAlive)

    def next_scene(self):
        if not self.isUserAlive:
            return EndGameFailure()

        if not self.isEnemyAlive:
            return EndGameSuccess()

        return super().next_scene()