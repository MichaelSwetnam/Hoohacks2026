from Button import Button
from scene import Scene
import pygame

class StartMenu(Scene):
    testButton: Button
    
    def __init__(self):
        self.testButton = Button(100, 100, 200,50)
        pass

    def draw(self, screen, events):
        pygame.draw.circle(screen, "red", pygame.Vector2(15, 15), 20)
        self.testButton.draw(screen, events)

        print(self.testButton.isClicked)
    # if button is clicked go to next secene

    

    def next_scene(self):
        return super().next_scene()

    pass