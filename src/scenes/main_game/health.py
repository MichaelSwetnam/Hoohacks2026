import pygame

from pygame import Surface
from pygame import Vector2

from constants import *
from load_image import load_image   

HEART_HEIGHT = 20
HEART_SIZE = 40

HEART_IMAGE      = load_image(HEART_ALIVE, Vector2(HEART_SIZE, HEART_SIZE))
DEAD_HEART_IMAGE = load_image(HEART_DEAD, Vector2(HEART_SIZE, HEART_SIZE))

def __draw_heart(screen: Surface, position: Vector2, isAlive: bool):
    if isAlive:
        screen.blit(HEART_IMAGE, (position.x, position.y))
    else:
        screen.blit(DEAD_HEART_IMAGE, (position.x, position.y))

def calculate_player_bounding(pMaxHealth: int):
    # Player hearts start at x = 20 and extend rightward
    x = 20
    y = HEART_HEIGHT

    width  = pMaxHealth * HEART_SIZE
    height = HEART_SIZE

    return pygame.Rect(x, y, width, height)

def calculate_enemy_bounding(eMaxHealth: int):
    # Enemy hearts start at SCREEN_WIDTH - 60 and extend leftward
    # The leftmost heart is at:
    x = (SCREEN_WIDTH - 60) - (eMaxHealth - 1) * HEART_SIZE
    y = HEART_HEIGHT

    width  = eMaxHealth * HEART_SIZE
    height = HEART_SIZE

    return pygame.Rect(x, y, width, height)

def draw_health(screen: pygame.Surface, playerMaxHealth: int, enemyMaxHealth: int, playerHealth: int, enemyHealth: int):
    # Draw hearts
    for i in range(0, playerMaxHealth):
        isHeartAlive =  i < playerHealth
        __draw_heart(screen, Vector2(20 + i * HEART_SIZE, HEART_HEIGHT), isHeartAlive)
        
    for i in range(0, enemyMaxHealth):
        isHeartAlive =  i < enemyHealth
        __draw_heart(screen, Vector2(SCREEN_WIDTH - 60 - i * HEART_SIZE, HEART_HEIGHT), isHeartAlive)
