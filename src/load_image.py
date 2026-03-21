import pygame
from pygame import Vector2

def resource_path(resource_name: str):
    return f"resources/{resource_name}"

def load_image(name: str, size: Vector2) -> pygame.Surface:
    resource = pygame.image.load(resource_path(name))
    scaled = pygame.transform.scale(resource, (size.x, size.y))
    return scaled    