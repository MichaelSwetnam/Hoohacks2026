import pygame
from pygame import Vector2

from constants import WHEAT_FIELDS_BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT 
from load_image import load_image

LOADED_IMAGE = load_image(WHEAT_FIELDS_BACKGROUND, Vector2(SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_menu_background(scene: pygame.Surface):
    
    scene.blit(LOADED_IMAGE, (0, 0))

# ← ADD THIS NEW FUNCTION BELOW
def draw_darkened_background(scene: pygame.Surface, opacity: int = 140):
    """
    Draws the background then a dark overlay on top so text is readable.
    opacity: 0 = fully transparent, 255 = fully black. 140 is a good default.
    """
    draw_menu_background(scene)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, opacity))
    scene.blit(overlay, (0, 0))

# ← ADD THIS NEW FUNCTION BELOW
def draw_darkened_background(scene: pygame.Surface, opacity: int = 140):
    """
    Draws the background then a dark overlay on top so text is readable.
    opacity: 0 = fully transparent, 255 = fully black. 140 is a good default.
    """
    draw_menu_background(scene)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, opacity))
    scene.blit(overlay, (0, 0))