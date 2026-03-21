from Button import Button
from scene import Scene
import pygame

class Menu(Scene):
    testButton: Button
    
    def __init__(self):
        self.testButton = Button()
        pass

    def draw(self, screen):
        pygame.draw.circle(screen, "red", pygame.Vector2(15, 15), 20)
        self.testButton.draw(screen)
    # if button is clicked go to next secene

    

    def next_scene(self):
        return super().next_scene()

    pass