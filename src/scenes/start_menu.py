from Button import Button
from scene import Scene
import pygame

class StartMenu(Scene):
    testButton: Button
    
    def __init__(self):
        self.testButton = Button(540, 335, 200,50, "START")
        pass

    def draw(self, screen, events):
        pygame.draw.circle(screen, "red", pygame.Vector2(15, 15), 20)
        self.testButton.draw(screen, events)

    

    def next_scene(self):
        return super().next_scene()

    pass