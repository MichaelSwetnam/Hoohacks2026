import pygame

from pygame import Surface
from pygame import Vector2

from constants import *
from load_image import load_image   

HEART_PATH = "heart.png"
HEART_DEAD_PATH = "heart_dead.png"

HEART_HEIGHT = 20
HEART_SIZE = 40

HEART_IMAGE      = load_image(HEART_PATH, Vector2(HEART_SIZE, HEART_SIZE))
DEAD_HEART_IMAGE = load_image(HEART_DEAD_PATH, Vector2(HEART_SIZE, HEART_SIZE))

def __draw_heart(screen: Surface, position: Vector2, isAlive: bool):
    if isAlive:
        screen.blit(HEART_IMAGE, (position.x, position.y))
    else:
        screen.blit(DEAD_HEART_IMAGE, (position.x, position.y))


def draw_health(screen: pygame.Surface, playerMaxHealth: int, enemyMaxHealth: int, playerHealth: int, enemyHealth: int):
    # Draw hearts
    for i in range(0, playerMaxHealth):
        isHeartAlive =  i < playerHealth
        __draw_heart(screen, Vector2(20 + i * HEART_SIZE, HEART_HEIGHT), isHeartAlive)
        
    for i in range(0, enemyMaxHealth):
        isHeartAlive =  i < enemyHealth
        __draw_heart(screen, Vector2(SCREEN_WIDTH - 60 - i * HEART_SIZE, HEART_HEIGHT), isHeartAlive)
