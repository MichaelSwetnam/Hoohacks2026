from scene import Scene
import pygame

class Menu(Scene):
    def __init__(self):
        pass

    def draw(self, screen):
        pygame.draw.circle(screen, "red", pygame.Vector2(15, 15), 20)

    def next_scene(self):
        return super().next_scene()

    pass