from components.Button import Button
from scene import Scene
from scenes.main_game import MainGame
import pygame

class StartMenu(Scene):
    __start_button: Button
    
    def __init__(self):
        self.__start_button = Button(540, 335, 200,50, "START")
        pass

    def draw(self, screen, events):
        pygame.draw.circle(screen, "red", pygame.Vector2(15, 15), 20)
        self.__start_button.draw(screen, events)

    def next_scene(self):
        if self.__start_button.isClicked:
            return MainGame()

    pass