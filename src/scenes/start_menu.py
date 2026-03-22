from pygame import Vector2
from components.Button import Button
from scene import Scene, SceneName
from draw_menu_background import draw_menu_background
from load_image import load_image

from constants import LOGO_WIDTH, LOGO_HEIGHT, LOGO, CENTER_OF_SCREEN

LOGO = load_image(LOGO, Vector2(LOGO_WIDTH, LOGO_HEIGHT))

START_BUTTON_X = 540
START_BUTTON_Y = 335
START_BUTTON_W = 200
START_BUTTON_H = 50

class StartMenu(Scene):
    __start_button: Button
    
    def __init__(self):
        self.__start_button = Button(START_BUTTON_X, START_BUTTON_Y, START_BUTTON_W, START_BUTTON_H, "START")
        pass

    def draw(self, screen, events):
        draw_menu_background(screen)

        screen.blit(LOGO, (CENTER_OF_SCREEN[0] - LOGO_WIDTH / 2, START_BUTTON_Y - LOGO_HEIGHT - 30))    

        self.__start_button.draw(screen, events)

    def next_scene(self):
        if self.__start_button.isClicked:
            return SceneName.NARRATOR

    pass