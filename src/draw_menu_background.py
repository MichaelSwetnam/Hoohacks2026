import pygame
from pygame import Vector2

from constants import WHEAT_FIELDS_BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT 
from load_image import load_image

LOADED_IMAGE = load_image(WHEAT_FIELDS_BACKGROUND, Vector2(SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_menu_background(scene: pygame.Surface):
    scene.blit(LOADED_IMAGE, (0, 0))