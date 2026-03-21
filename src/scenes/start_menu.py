from components.Button import Button
from scene import Scene, SceneName
import pygame

class StartMenu(Scene):
    __start_button: Button
    
    def __init__(self):
        self.__start_button = Button(540, 335, 200,50, "START")
        pass

    def draw(self, screen, events):
        self.__start_button.draw(screen, events)

    def next_scene(self):
        if self.__start_button.isClicked:
            return SceneName.MAIN_GAME

    pass